"""
⛏ Рудники (решение владельца 26.10): карта на MINES_COUNT рудников, у каждого свой ресурс.

- Рудник захватывается ТОЛЬКО победой в битве команд: каждая битва — ровно за один рудник
  (battles.mine_id). Победитель (1-е место) держит его MINE_HOLD_HOURS часов.
- Пока рудник у команды, КАЖДЫЙ её боец получает MINE_YIELD_PER_MEMBER_HOUR ресурса рудника
  в час (в пределах своего склада) — мотивация звать людей в команду.
- Через 72 ч рудник свободен, но взять его можно только в новой битве.
Начисления — фоновым циклом mine_payout_loop (целые часы, переживает рестарты: last_paid_at).
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from shared.economy import (team_veteran_sql, MINE_CORE_EVERY_HOURS, MINE_CORE_MAX, MINE_HOLD_HOURS, MINE_PAYOUT_INTERVAL_SECONDS,
                            MINE_SICK_EVERY_HOURS, MINE_YIELD_PER_MEMBER_HOUR, utcnow)
from shared.resources import change_resource, resource_capacity

logger = logging.getLogger(__name__)
HOUR = timedelta(hours=1)


async def list_mines(conn) -> list[dict]:
    rows = await conn.fetch(
        """SELECT m.*, t.team_name, t.school_num AS team_symbol, t.members_count
           FROM mines m LEFT JOIN teams t ON t.team_id = m.team_id ORDER BY m.id""")
    return [dict(r) for r in rows]


async def mine_battles(conn) -> list[dict]:
    """Активные битвы, у которых есть рудники-призы (mine_ids — по порядку призовых мест)."""
    rows = await conn.fetch(
        "SELECT * FROM battles WHERE status = 'active' AND cardinality(mine_ids) > 0 ORDER BY ends_at")
    return [dict(r) for r in rows]


async def free_mine_ids(conn, now: datetime) -> list[int]:
    """Рудники, которые сейчас никто не держит и за которые не идёт битва."""
    rows = await conn.fetch(
        """SELECT id FROM mines m
           WHERE (m.team_id IS NULL OR m.captured_until <= $1)
             AND NOT EXISTS (SELECT 1 FROM battles b WHERE b.status = 'active' AND m.id = ANY(b.mine_ids))
           ORDER BY id""", now)
    return [r["id"] for r in rows]


async def _members(conn, team_id: int) -> list[dict]:
    """Бойцы, которым идёт доход рудника: живые и с 📡 связью (командные активности без связи невозможны)."""
    rows = await conn.fetch(
        """SELECT u.user_id, u.meds_until FROM users u
           JOIN user_tech tc ON tc.user_id = u.user_id AND tc.tech = 'comm' AND tc.level >= 1
           WHERE u.team_id = $1 AND NOT u.is_blocked AND u.deletion_requested_at IS NULL
             AND u.deleted_at IS NULL AND """ + team_veteran_sql("u", "NOW()") + """
           ORDER BY u.user_id""", team_id)
    return [dict(r) for r in rows]


def sick_hours(first_hour: int, hours: int) -> int:
    """Сколько часов из [first_hour, first_hour + hours) «больных» (каждый MINE_SICK_EVERY_HOURS-й)."""
    return sum(1 for h in range(first_hour, first_hour + hours) if h % MINE_SICK_EVERY_HOURS == MINE_SICK_EVERY_HOURS - 1)


def core_marks(first_hour: int, hours: int, already: int) -> int:
    """☢️ Сколько суточных отметок удержания пройдено за эти часы (не больше MINE_CORE_MAX за рудник)."""
    marks = sum(1 for h in range(first_hour, first_hour + hours) if (h + 1) % MINE_CORE_EVERY_HOURS == 0)
    return max(0, min(marks, MINE_CORE_MAX - already))


async def pay_mine(conn, mine_id: int, now: datetime) -> int:
    """
    Начисляет бойцам команды-владельца целые часы добычи с last_paid_at. Сначала «забирает»
    часы (отдельная транзакция), потом раздаёт по бойцу — повтор после сбоя не заплатит дважды.
    Отпускает рудник, когда срок вышел. Возвращает число оплаченных часов.
    """
    async with conn.transaction():
        mine = await conn.fetchrow("SELECT * FROM mines WHERE id = $1 FOR UPDATE", mine_id)
        if not mine or mine["team_id"] is None:
            return 0
        until = mine["captured_until"]
        end = min(now, until)
        hours = int((end - mine["last_paid_at"]) / HOUR) if end > mine["last_paid_at"] else 0
        first_hour = int((mine["last_paid_at"] - mine["captured_at"]) / HOUR)
        cores = core_marks(first_hour, hours, mine["cores_paid"]) if hours > 0 else 0
        if hours > 0:
            await conn.execute("UPDATE mines SET last_paid_at = last_paid_at + $2, cores_paid = cores_paid + $3 "
                               "WHERE id = $1", mine_id, hours * HOUR, cores)
        if now >= until and mine["last_paid_at"] + hours * HOUR + HOUR > until:
            await conn.execute("UPDATE mines SET team_id = NULL, battle_id = NULL, captured_at = NULL, "
                               "captured_until = NULL, last_paid_at = NULL, cores_paid = 0 WHERE id = $1", mine_id)
    if hours <= 0:
        return 0
    sick = sick_hours(first_hour, hours)
    for m in await _members(conn, mine["team_id"]):
        uid = m["user_id"]
        # 💊 Аптечка спасает от «болезней» в походе: без неё каждый 7-й час добычи пропадает
        healthy = m["meds_until"] is not None and m["meds_until"] > now
        qty = (hours - (0 if healthy else sick)) * MINE_YIELD_PER_MEMBER_HOUR
        try:
            async with conn.transaction():
                cap = await resource_capacity(conn, uid)
                if qty > 0:
                    await change_resource(conn, uid, mine["kind"], qty, f"mine:{mine_id}", cap=cap)
                if cores:
                    await change_resource(conn, uid, "core", cores, f"mine:{mine_id}", cap=cap)
        except Exception:
            logger.exception("[MINES] не удалось начислить user=%s mine=%s", uid, mine_id)
    return hours


async def capture_mine(conn, mine_id: int, team_id: int, battle_id: int | None, now: datetime) -> datetime:
    """Отдаёт рудник команде-победителю на MINE_HOLD_HOURS (прежний владелец получает заработанное)."""
    await pay_mine(conn, mine_id, now)
    until = now + timedelta(hours=MINE_HOLD_HOURS)
    await conn.execute(
        "UPDATE mines SET team_id = $2, battle_id = $3, captured_at = $4, captured_until = $5, last_paid_at = $4, "
        "cores_paid = 0 WHERE id = $1", mine_id, team_id, battle_id, now, until)
    logger.info("[MINES] рудник %s → команда %s до %s (битва %s)", mine_id, team_id, until, battle_id)
    return until


async def payout_all(pool, now: datetime | None = None) -> int:
    now = now or utcnow()
    async with pool.acquire() as conn:
        ids = [r["id"] for r in await conn.fetch("SELECT id FROM mines WHERE team_id IS NOT NULL")]
        total = 0
        for mine_id in ids:
            try:
                total += await pay_mine(conn, mine_id, now)
            except Exception:
                logger.exception("[MINES] сбой начисления по руднику %s", mine_id)
    return total


async def mine_payout_loop() -> None:
    """Фоновый цикл главного бота: раз в несколько минут платит рудникам за прошедшие часы."""
    from shared.database import db
    while True:
        try:
            await payout_all(db.pool)
        except Exception:
            logger.exception("[MINES] сбой цикла начислений")
        await asyncio.sleep(MINE_PAYOUT_INTERVAL_SECONDS)
