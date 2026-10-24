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

from shared.economy import (MINE_HOLD_HOURS, MINE_PAYOUT_INTERVAL_SECONDS, MINE_YIELD_PER_MEMBER_HOUR,
                            utcnow)
from shared.resources import change_resource, resource_capacity

logger = logging.getLogger(__name__)
HOUR = timedelta(hours=1)


async def list_mines(conn) -> list[dict]:
    rows = await conn.fetch(
        """SELECT m.*, t.team_name, t.school_num AS team_symbol, t.members_count
           FROM mines m LEFT JOIN teams t ON t.team_id = m.team_id ORDER BY m.id""")
    return [dict(r) for r in rows]


async def mine_battles(conn) -> list[dict]:
    """Активные битвы, у которых есть рудник-приз."""
    rows = await conn.fetch(
        "SELECT battle_id, title, nomination_key, nomination_text, starts_at, ends_at, mine_id "
        "FROM battles WHERE status = 'active' AND mine_id IS NOT NULL ORDER BY ends_at")
    return [dict(r) for r in rows]


async def free_mine_ids(conn, now: datetime) -> list[int]:
    """Рудники, которые сейчас никто не держит и за которые не идёт битва."""
    rows = await conn.fetch(
        """SELECT id FROM mines m
           WHERE (m.team_id IS NULL OR m.captured_until <= $1)
             AND NOT EXISTS (SELECT 1 FROM battles b WHERE b.status = 'active' AND b.mine_id = m.id)
           ORDER BY id""", now)
    return [r["id"] for r in rows]


async def _members(conn, team_id: int) -> list[int]:
    rows = await conn.fetch(
        "SELECT user_id FROM users WHERE team_id = $1 AND NOT is_blocked "
        "AND deletion_requested_at IS NULL AND deleted_at IS NULL ORDER BY user_id", team_id)
    return [r["user_id"] for r in rows]


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
        if hours > 0:
            await conn.execute("UPDATE mines SET last_paid_at = last_paid_at + $2 WHERE id = $1",
                               mine_id, hours * HOUR)
        if now >= until and mine["last_paid_at"] + hours * HOUR + HOUR > until:
            await conn.execute("UPDATE mines SET team_id = NULL, battle_id = NULL, captured_at = NULL, "
                               "captured_until = NULL, last_paid_at = NULL WHERE id = $1", mine_id)
    if hours <= 0:
        return 0
    qty = hours * MINE_YIELD_PER_MEMBER_HOUR
    for uid in await _members(conn, mine["team_id"]):
        try:
            async with conn.transaction():
                await change_resource(conn, uid, mine["kind"], qty, f"mine:{mine_id}",
                                      cap=await resource_capacity(conn, uid))
        except Exception:
            logger.exception("[MINES] не удалось начислить user=%s mine=%s", uid, mine_id)
    return hours


async def capture_mine(conn, mine_id: int, team_id: int, battle_id: int | None, now: datetime) -> datetime:
    """Отдаёт рудник команде-победителю на MINE_HOLD_HOURS (прежний владелец получает заработанное)."""
    await pay_mine(conn, mine_id, now)
    until = now + timedelta(hours=MINE_HOLD_HOURS)
    await conn.execute(
        "UPDATE mines SET team_id = $2, battle_id = $3, captured_at = $4, captured_until = $5, last_paid_at = $4 "
        "WHERE id = $1", mine_id, team_id, battle_id, now, until)
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
