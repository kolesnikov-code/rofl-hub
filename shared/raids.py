"""
Налёты (волна 22.10, вечер): решение против решения, добыча — только ресурсы.

Правила (числа — shared/economy.py):
- атакующий тратит RAID_FUEL_HYDROGEN водорода на вылет и выбирает жест КНБ;
  исход решает жест против ОБОРОНИТЕЛЬНОЙ СТОЙКИ цели (users.raid_stance — игрок
  выставляет заранее; не выставил — случайная). Победа: атакующий забирает
  RAID_LOOT_PERCENT каждого ресурса цели (не больше RAID_LOOT_CAP). Провал: отдаёт цели
  RAID_FAIL_PERCENT своих (не больше RAID_FAIL_CAP). Ничья — топливо сгорело, добычи нет;
- монеты, роботы, котлеты и котлеты в ордерах НЕПРИКОСНОВЕННЫ — грабятся только ресурсы;
- защита: щит из мастерской (raid_shield_until), новички RAID_NEWBIE_SHIELD_DAYS дней,
  тиммейты не грабят друг друга, одну цель — не чаще RAID_VICTIM_COOLDOWN_HOURS;
- кулдаун атакующего RAID_ATTACK_COOLDOWN_HOURS; реванш за удачный налёт на тебя —
  бесплатно и без кулдауна в течение RAID_REVENGE_HOURS (один раз на налёт).
Всё — внутри транзакции вызывающего кода; обе строки users блокируются по возрастанию id.
"""
from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from shared.economy import SUIT_BONUS, user_bonus
from shared.economy import (
    CARGO_LOOT_PERCENT,
    drone_raid_loot_percent,
    drone_spy_targets,
    RAID_SICK_LOSS_PERCENT,
    raid_candidates,
    raid_cooldown_hours,
    raid_loot_percent,
    TRAP_FAIL_MULTIPLIER,
    RAID_ATTACK_COOLDOWN_HOURS,
    RAID_CANDIDATES,
    RAID_FUEL_HYDROGEN,
    RAID_MIN_TARGET_RESOURCES,
    RAID_NEWBIE_SHIELD_DAYS,
    RAID_REVENGE_HOURS,
    RAID_TARGET_ACTIVE_DAYS,
    RAID_VICTIM_COOLDOWN_HOURS,
    RESOURCE_KINDS,
    is_active,
    raid_fail_loss,
    raid_loot,
)
from shared.locales import t
from shared.resources import InsufficientResources, change_resource, lock_resources, resource_capacity

logger = logging.getLogger(__name__)

STANCES = ("rock", "scissors", "paper")
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}


class RaidError(Exception):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


@dataclass
class RaidResult:
    raid_id: int
    result: str                  # win / draw / lose
    move: str
    stance: str
    defender_id: int
    loot: dict[str, int] = field(default_factory=dict)   # что перешло (win: к атакующему, lose: к цели)
    is_revenge: bool = False
    notes: list[str] = field(default_factory=list)       # сработавшие изделия: economizer/cargo/trap/drill


def raid_outcome(move: str, stance: str) -> str:
    """Чистое правило: жест атакующего против стойки обороны."""
    if move == stance:
        return "draw"
    return "win" if BEATS[move] == stance else "lose"


def shield_active(user, now: datetime, dome_until: datetime | None = None) -> bool:
    """Щит из мастерской, Купол команды (dome_until) или защита новичка."""
    if is_active(user["raid_shield_until"], now) or is_active(dome_until, now):
        return True
    created = user["created_at"]
    return created is not None and created > now - timedelta(days=RAID_NEWBIE_SHIELD_DAYS)


def attack_cooldown_left(last_raid_at: datetime | None, now: datetime, comm_level: int = 1) -> int:
    """Секунд до следующего вылета (0 — можно лететь). 📡 связь укорачивает перезарядку."""
    if last_raid_at is None:
        return 0
    left = last_raid_at + timedelta(hours=raid_cooldown_hours(comm_level)) - now
    return max(0, int(left.total_seconds()))


def display_name_of(user) -> str:
    """Имя цели БЕЗ username и ID — чтобы налёты не превращались в травлю."""
    name = (user["display_name"] or "").strip()
    return name or f"#{str(user['user_id'])[-4:]}"


async def find_targets(conn, attacker_id: int, attacker_team: int | None, now: datetime,
                       limit: int = RAID_CANDIDATES) -> list[dict]:
    """«Разведка»: случайные подходящие цели с суммарным запасом ресурсов."""
    rows = await conn.fetch(
        """
        SELECT u.user_id, u.display_name, u.created_at, SUM(r.qty) AS total
        FROM users u JOIN user_resources r ON r.user_id = u.user_id
        LEFT JOIN teams tm ON tm.team_id = u.team_id
        WHERE u.user_id <> $1 AND NOT u.is_blocked AND u.deletion_requested_at IS NULL
          AND u.deleted_at IS NULL
          AND ($2::int IS NULL OR u.team_id IS DISTINCT FROM $2::int)
          AND u.last_seen_at > $3::timestamptz - make_interval(days => $4::int)
          AND u.created_at < $3::timestamptz - make_interval(days => $5::int)
          AND (u.raid_shield_until IS NULL OR u.raid_shield_until <= $3::timestamptz)
          AND (u.raid_camo_until IS NULL OR u.raid_camo_until <= $3::timestamptz)
          AND (tm.dome_until IS NULL OR tm.dome_until <= $3::timestamptz)
          -- 🥷 костюм маскировки (и экзо-броня): с шансом цель не попадает в разведку (30.10)
          AND NOT (random() * 100 < (CASE WHEN u.suit = 'exo' OR (u.suit = 'st' AND u.suit_level >= 2) THEN $10::int
                                          WHEN u.suit = 'st' THEN $9::int ELSE 0 END)
                                    + COALESCE((u.art_bonus->>'st')::int, 0))
          AND NOT EXISTS (SELECT 1 FROM raids x WHERE x.defender_id = u.user_id
                          AND x.created_at > $3::timestamptz - make_interval(hours => $6::int))
        GROUP BY u.user_id HAVING SUM(r.qty) >= $7::int
        ORDER BY random() LIMIT $8::int
        """,
        attacker_id, attacker_team, now, RAID_TARGET_ACTIVE_DAYS, RAID_NEWBIE_SHIELD_DAYS,
        RAID_VICTIM_COOLDOWN_HOURS, RAID_MIN_TARGET_RESOURCES, limit, SUIT_BONUS["st"][1], SUIT_BONUS["st"][2])
    return [dict(r) for r in rows]


async def scout(conn, user_id: int, now: datetime) -> list[dict]:
    """
    «Разведка» с проверками (27.10): нужны 📡 связь, 🔭 разведка и ⚔️ нападение 1-го уровня,
    топливо на вылет (или заряд Экономайзера). Батарейки разведка НЕ тратит (27.10: они для командных активностей).
    Целей в списке = 2 + уровень разведки.
    """
    from shared.tech import tech_levels
    user = await conn.fetchrow("SELECT team_id, last_raid_at, raid_free_fuel, drones_spy FROM users WHERE user_id = $1 "
                               "FOR UPDATE", user_id)
    if user is None:
        raise RaidError("common.no_profile")
    tech = await tech_levels(conn, user_id)
    for need in ("comm", "scout", "attack"):
        if tech[need] < 1:
            raise RaidError("raid.err_need_tech", tech=need)
    left = attack_cooldown_left(user["last_raid_at"], now, tech["comm"])
    if left > 0:
        raise RaidError("raid.err_cooldown", minutes=-(-left // 60))
    stock = await lock_resources(conn, user_id)
    if user["raid_free_fuel"] <= 0 and stock.get("hydrogen", 0) < RAID_FUEL_HYDROGEN:
        raise RaidError("raid.err_fuel", need=RAID_FUEL_HYDROGEN, have=stock.get("hydrogen", 0))
    # 🛰 Дроны-шпионы: +1 цель каждый (с потолком)
    limit = raid_candidates(tech["scout"]) + drone_spy_targets(user["drones_spy"])
    return await find_targets(conn, user_id, user["team_id"], now, limit=limit)


async def revenge_options(conn, user_id: int, now: datetime) -> list[dict]:
    """Удачные налёты на игрока за окно реванша, за которые ещё не отомстили."""
    rows = await conn.fetch(
        """
        SELECT x.id AS raid_id, x.attacker_id, x.loot, x.created_at,
               u.display_name, u.user_id
        FROM raids x JOIN users u ON u.user_id = x.attacker_id
        WHERE x.defender_id = $1 AND x.result = 'win' AND NOT x.revenged AND NOT x.is_revenge   -- реванш на реванш не даётся
          AND x.created_at > $2::timestamptz - make_interval(hours => $3::int)
        ORDER BY x.created_at DESC
        """, user_id, now, RAID_REVENGE_HOURS)
    return [dict(r) for r in rows]


async def set_stance(conn, user_id: int, stance: str) -> None:
    if stance not in STANCES:
        raise RaidError("raid.err_stance")
    await conn.execute("UPDATE users SET raid_stance = $2 WHERE user_id = $1", user_id, stance)


async def execute_raid(conn, attacker_id: int, defender_id: int, move: str, now: datetime,
                       revenge_of: int | None = None) -> RaidResult:
    """Проводит налёт. Бросает RaidError с ключом локали."""
    if move not in STANCES:
        raise RaidError("raid.err_stance")
    if attacker_id == defender_id:
        raise RaidError("raid.err_self")

    rows = await conn.fetch(
        "SELECT * FROM users WHERE user_id = ANY($1::bigint[]) ORDER BY user_id FOR UPDATE",
        [attacker_id, defender_id])
    by_id = {r["user_id"]: r for r in rows}
    attacker, defender = by_id.get(attacker_id), by_id.get(defender_id)
    if attacker is None:
        raise RaidError("common.no_profile")
    if (defender is None or defender["is_blocked"] or defender["deleted_at"] is not None
            or defender["deletion_requested_at"] is not None):
        raise RaidError("raid.err_gone")
    from shared.tech import tech_levels
    a_tech = await tech_levels(conn, attacker_id)
    d_tech = await tech_levels(conn, defender_id)
    if attacker["team_id"] is not None and attacker["team_id"] == defender["team_id"]:
        raise RaidError("raid.err_teammate")
    dome = None
    if defender["team_id"] is not None:
        dome = await conn.fetchval("SELECT dome_until FROM teams WHERE team_id = $1", defender["team_id"])
    if shield_active(defender, now, dome):
        raise RaidError("raid.err_shielded")
    notes: list[str] = []

    is_revenge = False
    if revenge_of is not None:
        original = await conn.fetchrow(
            "SELECT * FROM raids WHERE id = $1 FOR UPDATE", revenge_of)
        if (not original or original["defender_id"] != attacker_id
                or original["attacker_id"] != defender_id or original["result"] != "win"
                or original["revenged"] or original["is_revenge"]
                or original["created_at"] <= now - timedelta(hours=RAID_REVENGE_HOURS)):
            raise RaidError("raid.err_revenge_gone")
        is_revenge = True
    else:
        if a_tech["attack"] < 1:   # реванш — право обороны, без технологий
            raise RaidError("raid.err_need_tech", tech="attack")
        # Цель перепроверяется в самом налёте (аудит 2.9): старая кнопка разведки или подделанный запрос не бьют
        # по игроку под Маскировкой, неактивному или новичку — те же условия, что в разведке
        if ((defender["raid_camo_until"] and defender["raid_camo_until"] > now)
                or defender["last_seen_at"] <= now - timedelta(days=RAID_TARGET_ACTIVE_DAYS)
                or defender["created_at"] >= now - timedelta(days=RAID_NEWBIE_SHIELD_DAYS)):
            raise RaidError("raid.err_gone")
        left = attack_cooldown_left(attacker["last_raid_at"], now, a_tech["comm"])
        if left > 0:
            raise RaidError("raid.err_cooldown", minutes=-(-left // 60))
        recent = await conn.fetchval(
            "SELECT 1 FROM raids WHERE defender_id = $1 AND created_at > $2::timestamptz - make_interval(hours => $3::int)",
            defender_id, now, RAID_VICTIM_COOLDOWN_HOURS)
        if recent:
            raise RaidError("raid.err_victim_cooldown", hours=RAID_VICTIM_COOLDOWN_HOURS)
        if attacker["raid_free_fuel"] > 0:   # ⛽ Экономайзер: вылет без водорода
            await conn.execute("UPDATE users SET raid_free_fuel = raid_free_fuel - 1 WHERE user_id = $1", attacker_id)
            notes.append("economizer")
        else:
            try:
                await change_resource(conn, attacker_id, "hydrogen", -RAID_FUEL_HYDROGEN,
                                      "raid_fuel", str(defender_id))
            except InsufficientResources as e:
                raise RaidError("raid.err_fuel", need=RAID_FUEL_HYDROGEN, have=e.have) from e

    stance = defender["raid_stance"] if defender["raid_stance"] in STANCES else random.choice(STANCES)
    result = raid_outcome(move, stance)
    if result == "draw" and is_active(defender["raid_drill_until"], now):
        result = "lose"   # 🎯 Тренажёр стойки цели: ничья засчитывается как провал налётчика
        notes.append("drill")
    # Технологии: ⚔️ нападение и 📚 наука атакующего против 🛡 обороны цели
    loot_percent = raid_loot_percent(a_tech["attack"], d_tech["defense"], a_tech["science"])
    # 🤖 Боевые дроны: атакующие налётчика против защитников цели (суммируются, с потолком)
    with_drones = drone_raid_loot_percent(loot_percent, attacker["drones_attack"], defender["drones_guard"])
    if with_drones != loot_percent:
        notes.append("drones")
        loot_percent = with_drones
    military = user_bonus(attacker, "ml")
    if military:   # 🪖 костюм военного: +% к трофею (30.10)
        loot_percent = loot_percent * (100 + military) // 100
        notes.append("suit")
    if attacker["raid_cargo"] > 0:   # 📦 Трюм: тратится на этом вылете при любом исходе
        await conn.execute("UPDATE users SET raid_cargo = raid_cargo - 1 WHERE user_id = $1", attacker_id)
        loot_percent = loot_percent * CARGO_LOOT_PERCENT // 100
        if result == "win":
            notes.append("cargo")
    fail_mult = 1
    if result == "lose" and is_active(defender["raid_trap_until"], now):
        fail_mult = TRAP_FAIL_MULTIPLIER   # 🪤 Приманка цели
        notes.append("trap")

    loot: dict[str, int] = {}
    # Блокируем ресурсы обеих сторон в фиксированном порядке (анти-дедлок)
    first, second = sorted((attacker_id, defender_id))
    stocks = {first: await lock_resources(conn, first), second: await lock_resources(conn, second)}
    # Трофей сверх вместимости склада победителя пропадает (склад с лимитом, 25.10)
    caps = {uid: await resource_capacity(conn, uid) for uid in (attacker_id, defender_id)}
    if result == "win":
        # 💊 Без Аптечки часть трофея «пропадает в лазарете»: цель теряет всё, налётчик получает меньше
        sick = not is_active(attacker["meds_until"], now)
        if sick:
            notes.append("sick")
        for kind in RESOURCE_KINDS:
            amount = raid_loot(stocks[defender_id].get(kind, 0), loot_percent)
            if amount > 0:
                got = amount - amount * RAID_SICK_LOSS_PERCENT // 100 if sick else amount
                await change_resource(conn, defender_id, kind, -amount, "raid_loss", str(attacker_id))
                if got > 0:
                    await change_resource(conn, attacker_id, kind, got, "raid_loot", str(defender_id),
                                          cap=caps[attacker_id])
                loot[kind] = got
    elif result == "lose":
        for kind in RESOURCE_KINDS:
            amount = raid_fail_loss(stocks[attacker_id].get(kind, 0), fail_mult)
            if amount > 0:
                await change_resource(conn, attacker_id, kind, -amount, "raid_fail", str(defender_id))
                await change_resource(conn, defender_id, kind, amount, "raid_defense", str(attacker_id),
                                      cap=caps[defender_id])
                loot[kind] = amount

    raid_id = await conn.fetchval(
        """INSERT INTO raids (attacker_id, defender_id, attack_move, stance, result, loot, is_revenge, created_at)
           VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8) RETURNING id""",
        attacker_id, defender_id, move, stance, result, json.dumps(loot), is_revenge, now)
    if is_revenge:
        await conn.execute("UPDATE raids SET revenged = TRUE WHERE id = $1", revenge_of)
    else:
        await conn.execute("UPDATE users SET last_raid_at = $2 WHERE user_id = $1", attacker_id, now)
    logger.info("[RAID] #%s %s→%s move=%s stance=%s result=%s loot=%s revenge=%s",
                raid_id, attacker_id, defender_id, move, stance, result, loot, is_revenge)
    return RaidResult(raid_id=raid_id, result=result, move=move, stance=stance,
                      defender_id=defender_id, loot=loot, is_revenge=is_revenge, notes=notes)


async def raid_stats(conn, user_id: int) -> dict:
    row = await conn.fetchrow(
        """SELECT COUNT(*) FILTER (WHERE attacker_id = $1) AS attacks,
                  COUNT(*) FILTER (WHERE attacker_id = $1 AND result = 'win') AS attack_wins,
                  COUNT(*) FILTER (WHERE defender_id = $1) AS defenses,
                  COUNT(*) FILTER (WHERE defender_id = $1 AND result <> 'win') AS defense_holds
           FROM raids WHERE attacker_id = $1 OR defender_id = $1""", user_id)
    return {k: int(row[k]) for k in ("attacks", "attack_wins", "defenses", "defense_holds")}
