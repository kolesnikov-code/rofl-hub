"""
🧍 Персонаж и костюмы (решение владельца 30.10).

Сумка (user_gear) и надетое (user_equip) — отдельно от склада ресурсов. Журнал gear_ledger: каждое движение детали
(выпадение, биржа, прокачка, сплав). Дисциплина как у ресурсов: всё внутри транзакции вызывающего, количество не
уходит в минус (CHECK + проверка UPDATE ... WHERE qty >= n).

Бонус даёт только ПОЛНЫЙ комплект одного костюма (5 слотов). Действующий костюм денормализован в users.suit /
suit_level / suit_since — его дёшево читают игры, налёты, экспедиции, лаборатория и мастерская
(economy.suit_bonus). suit_since — с какого момента надет комплект: бонус шахтёра считается только по добыче после
этого момента, переодеться «перед выплатой» не выйдет.

Выпадение деталей — случайное (костюм и слот), не больше GEAR_SEASON_CAP за сезон на игрока: так каждый
собирает за сезон ровно один костюм, но детали у всех разные — одинаковые добирают на бирже.
"""
from __future__ import annotations

import logging
import random
from datetime import datetime, timedelta

from shared.economy import (
    GEAR_EXO,
    GEAR_EXO_COINS,
    GEAR_EXO_COST,
    GEAR_MAX_LEVEL,
    GEAR_SEASON_CAP,
    GEAR_SLOTS,
    GEAR_SUITS,
    GEAR_UPGRADE_COINS,
    GEAR_UPGRADE_COST,
    miner_bonus,
    season_bounds,
    suit_bonus,
)
from shared.ledger import InsufficientFunds, change_balance
from shared.resources import RESOURCE_ICONS, InsufficientResources, spend_bundle

logger = logging.getLogger(__name__)

ALL_GEAR_SUITS = GEAR_SUITS + (GEAR_EXO,)
GENDERS = ("m", "f")


class GearError(Exception):
    """Причина отказа: ключ локали + параметры (локализуется в API)."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)


def _check(suit: str, slot: str) -> None:
    if suit not in ALL_GEAR_SUITS or slot not in GEAR_SLOTS:
        raise GearError("gear.err_unknown")


# ============================================================================
# Сумка
# ============================================================================
async def change_gear(conn, user_id: int, suit: str, slot: str, level: int, delta: int, reason: str,
                      ref: str | None = None) -> int:
    """Атомарно меняет количество детали в сумке. Возвращает остаток; GearError("gear.err_none") при нехватке."""
    _check(suit, slot)
    if delta >= 0:
        qty = await conn.fetchval(
            "INSERT INTO user_gear (user_id, suit, slot, level, qty) VALUES ($1, $2, $3, $4, $5) "
            "ON CONFLICT (user_id, suit, slot, level) DO UPDATE SET qty = user_gear.qty + EXCLUDED.qty "
            "RETURNING qty", user_id, suit, slot, level, delta)
    else:
        qty = await conn.fetchval(
            "UPDATE user_gear SET qty = qty + $5 WHERE user_id = $1 AND suit = $2 AND slot = $3 AND level = $4 "
            "AND qty >= $6 RETURNING qty", user_id, suit, slot, level, delta, -delta)
        if qty is None:
            raise GearError("gear.err_none")
    if delta:
        await conn.execute(
            "INSERT INTO gear_ledger (user_id, suit, slot, level, delta, reason, ref) VALUES ($1, $2, $3, $4, $5, $6, $7)",
            user_id, suit, slot, level, delta, reason, ref)
    return qty


async def have(conn, user_id: int, suit: str, slot: str, level: int = 1) -> int:
    return await conn.fetchval("SELECT qty FROM user_gear WHERE user_id = $1 AND suit = $2 AND slot = $3 AND level = $4",
                               user_id, suit, slot, level) or 0


async def bag(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch("SELECT suit, slot, level, qty FROM user_gear WHERE user_id = $1 AND qty > 0 "
                            "ORDER BY suit, slot, level", user_id)
    return [dict(r) for r in rows]


async def equipped(conn, user_id: int) -> dict[str, dict]:
    rows = await conn.fetch("SELECT slot, suit, level FROM user_equip WHERE user_id = $1", user_id)
    return {r["slot"]: {"suit": r["suit"], "level": r["level"]} for r in rows}


def full_set(worn: dict[str, dict]) -> tuple[str | None, int]:
    """Действующий костюм: все 5 слотов — детали одного костюма. (костюм, уровень = меньший) или (None, 0)."""
    if set(worn) != set(GEAR_SLOTS):
        return None, 0
    suits = {w["suit"] for w in worn.values()}
    if len(suits) != 1:
        return None, 0
    return suits.pop(), min(w["level"] for w in worn.values())


async def _refresh_suit(conn, user_id: int, now: datetime) -> tuple[str | None, int]:
    """Пересчитывает users.suit/suit_level; suit_since сбрасывается, если сменился сам костюм."""
    suit, level = full_set(await equipped(conn, user_id))
    await conn.execute(
        "UPDATE users SET suit_since = CASE WHEN suit IS DISTINCT FROM $2 THEN $4 ELSE suit_since END, "
        "suit = $2, suit_level = $3 WHERE user_id = $1", user_id, suit, level if suit else None, now)
    return suit, level


async def _lock(conn, user_id: int):
    row = await conn.fetchrow("SELECT user_id, gender, suit, suit_level FROM users WHERE user_id = $1 "
                              "AND deleted_at IS NULL FOR UPDATE", user_id)
    if row is None:
        raise GearError("common.no_profile")
    return row


async def set_gender(conn, user_id: int, gender: str) -> None:
    if gender not in GENDERS:
        raise GearError("gear.err_unknown")
    await conn.execute("UPDATE users SET gender = $2 WHERE user_id = $1", user_id, gender)


async def equip(conn, user_id: int, suit: str, slot: str, level: int, now: datetime) -> tuple[str | None, int]:
    """Надеть деталь из сумки; то, что было в слоте, возвращается в сумку. Возвращает действующий костюм."""
    _check(suit, slot)
    await _lock(conn, user_id)
    await change_gear(conn, user_id, suit, slot, level, -1, "equip")
    old = await conn.fetchrow("DELETE FROM user_equip WHERE user_id = $1 AND slot = $2 RETURNING suit, level",
                              user_id, slot)
    if old:
        await change_gear(conn, user_id, old["suit"], slot, old["level"], 1, "unequip")
    await conn.execute("INSERT INTO user_equip (user_id, slot, suit, level) VALUES ($1, $2, $3, $4)",
                       user_id, slot, suit, level)
    return await _refresh_suit(conn, user_id, now)


async def unequip(conn, user_id: int, slot: str, now: datetime) -> tuple[str | None, int]:
    if slot not in GEAR_SLOTS:
        raise GearError("gear.err_unknown")
    await _lock(conn, user_id)
    old = await conn.fetchrow("DELETE FROM user_equip WHERE user_id = $1 AND slot = $2 RETURNING suit, level",
                              user_id, slot)
    if old is None:
        raise GearError("gear.err_none")
    await change_gear(conn, user_id, old["suit"], slot, old["level"], 1, "unequip")
    return await _refresh_suit(conn, user_id, now)


async def _spend(conn, user_id: int, cost: dict[str, int], coins: int, reason: str, ref: str) -> None:
    try:
        await spend_bundle(conn, user_id, cost, reason, ref)
    except InsufficientResources as e:
        raise GearError("ws.err_resources", need=e.need, have=e.have, kind=RESOURCE_ICONS[e.kind]) from e
    try:
        await change_balance(conn, user_id, -coins, reason, ref)
    except InsufficientFunds as e:
        raise GearError("gear.err_coins", need=coins) from e


async def upgrade(conn, user_id: int, suit: str, slot: str, now: datetime) -> tuple[str | None, int]:
    """Прокачка детали 1 → 2: сначала из сумки, иначе — надетую. Ресурсы и монеты сгорают."""
    _check(suit, slot)
    if suit == GEAR_EXO:
        raise GearError("gear.err_max")
    await _lock(conn, user_id)
    ref = f"{suit}:{slot}"
    if await have(conn, user_id, suit, slot, 1) > 0:
        await _spend(conn, user_id, GEAR_UPGRADE_COST[suit], GEAR_UPGRADE_COINS, "gear_upgrade", ref)
        await change_gear(conn, user_id, suit, slot, 1, -1, "gear_upgrade", ref)
        await change_gear(conn, user_id, suit, slot, GEAR_MAX_LEVEL, 1, "gear_upgrade", ref)
        return await _refresh_suit(conn, user_id, now)
    worn = await conn.fetchrow("SELECT suit, level FROM user_equip WHERE user_id = $1 AND slot = $2", user_id, slot)
    if not worn or worn["suit"] != suit:
        raise GearError("gear.err_none")
    if worn["level"] >= GEAR_MAX_LEVEL:
        raise GearError("gear.err_max")
    await _spend(conn, user_id, GEAR_UPGRADE_COST[suit], GEAR_UPGRADE_COINS, "gear_upgrade", ref)
    await conn.execute("UPDATE user_equip SET level = $3 WHERE user_id = $1 AND slot = $2", user_id, slot, GEAR_MAX_LEVEL)
    await conn.execute(
        "INSERT INTO gear_ledger (user_id, suit, slot, level, delta, reason, ref) VALUES ($1, $2, $3, $4, 0, $5, $6)",
        user_id, suit, slot, GEAR_MAX_LEVEL, "gear_upgrade_worn", ref)
    return await _refresh_suit(conn, user_id, now)


async def exo_ready(conn, user_id: int) -> dict:
    """Сколько из 30 деталей 2-го уровня есть (в сумке или надето) — для сплава нано-экзо-брони."""
    rows = await conn.fetch(
        """SELECT suit, slot FROM user_gear WHERE user_id = $1 AND level = $2 AND qty > 0 AND suit <> $3
           UNION SELECT suit, slot FROM user_equip WHERE user_id = $1 AND level = $2 AND suit <> $3""",
        user_id, GEAR_MAX_LEVEL, GEAR_EXO)
    got = {(r["suit"], r["slot"]) for r in rows}
    return {"have": len(got), "need": len(GEAR_SUITS) * len(GEAR_SLOTS),
            "missing": [f"{s}:{p}" for s in GEAR_SUITS for p in GEAR_SLOTS if (s, p) not in got]}


async def merge_exo(conn, user_id: int, now: datetime) -> tuple[str | None, int]:
    """Сплав: по одной детали 2-го уровня каждого костюма и слота (30 шт.) + цена → 5 деталей экзо-брони (надеваются)."""
    await _lock(conn, user_id)
    state = await exo_ready(conn, user_id)
    if state["missing"]:
        raise GearError("gear.err_exo_missing", have=state["have"], need=state["need"])
    await _spend(conn, user_id, GEAR_EXO_COST, GEAR_EXO_COINS, "gear_exo", "exo")
    # Снимаем всё надетое в сумку, потом списываем по одной детали каждого вида
    for row in await conn.fetch("DELETE FROM user_equip WHERE user_id = $1 RETURNING slot, suit, level", user_id):
        await change_gear(conn, user_id, row["suit"], row["slot"], row["level"], 1, "unequip")
    for suit in GEAR_SUITS:
        for slot in GEAR_SLOTS:
            await change_gear(conn, user_id, suit, slot, GEAR_MAX_LEVEL, -1, "gear_exo", "exo")
    for slot in GEAR_SLOTS:
        await conn.execute("INSERT INTO user_equip (user_id, slot, suit, level) VALUES ($1, $2, $3, $4)",
                           user_id, slot, GEAR_EXO, GEAR_MAX_LEVEL)
        await conn.execute(
            "INSERT INTO gear_ledger (user_id, suit, slot, level, delta, reason, ref) VALUES ($1, $2, $3, $4, 1, $5, $6)",
            user_id, GEAR_EXO, slot, GEAR_MAX_LEVEL, "gear_exo", "exo")
    logger.info("[GEAR] %s сплавил(а) нано-экзо-броню", user_id)
    return await _refresh_suit(conn, user_id, now)


# ============================================================================
# Выпадение деталей
# ============================================================================
async def season_drops(conn, user_id: int, now: datetime) -> int:
    start, end = season_bounds(now)
    return await conn.fetchval(
        "SELECT COALESCE(SUM(delta), 0) FROM gear_ledger WHERE user_id = $1 AND reason = 'drop' "
        "AND created_at >= $2 AND created_at < $3", user_id, start, end)


async def drop_random(conn, user_id: int, qty: int, ref: str, now: datetime,
                      rng: random.Random | None = None) -> list[tuple[str, str]]:
    """Случайные детали 1-го уровня, не больше остатка сезонного лимита. Возвращает [(костюм, слот)]."""
    rng = rng or random.SystemRandom()
    left = GEAR_SEASON_CAP - await season_drops(conn, user_id, now)
    out = []
    for _ in range(max(0, min(qty, left))):
        suit, slot = rng.choice(GEAR_SUITS), rng.choice(GEAR_SLOTS)
        await change_gear(conn, user_id, suit, slot, 1, 1, "drop", ref)
        out.append((suit, slot))
    return out


# ============================================================================
# ⛏ Бонус шахтёра: раз в сутки — % от монет фермы, добытых за прошлые сутки UTC (после того, как надет костюм)
# ============================================================================
async def pay_miner_bonus(conn, user_id: int, day_start: datetime) -> int:
    """Начисляет бонус за сутки [day_start, +1 день). Идемпотентно: users.miner_bonus_day. Возвращает сумму."""
    user = await conn.fetchrow("SELECT suit, suit_level, suit_since, miner_bonus_day FROM users WHERE user_id = $1 "
                               "AND deleted_at IS NULL AND NOT is_blocked FOR UPDATE", user_id)
    day = day_start.date()
    if user is None or (user["miner_bonus_day"] is not None and user["miner_bonus_day"] >= day):
        return 0
    await conn.execute("UPDATE users SET miner_bonus_day = $2 WHERE user_id = $1", user_id, day)
    pct = suit_bonus(user["suit"], user["suit_level"], "mn")
    if not pct or user["suit_since"] is None:
        return 0
    since = max(day_start, user["suit_since"])
    mined = await conn.fetchval(
        "SELECT COALESCE(SUM(delta), 0) FROM ledger WHERE user_id = $1 AND reason = 'mining' "
        "AND created_at >= $2 AND created_at < $3", user_id, since, day_start + timedelta(days=1))
    bonus = miner_bonus(int(mined), pct)
    if bonus > 0:
        await change_balance(conn, user_id, bonus, "suit_miner", day.isoformat())
    return bonus


async def miner_bonus_round(pool, now: datetime) -> int:
    """Демон: всем в костюме шахтёра (или экзо) — бонус за вчерашние сутки UTC. Каждый — своя транзакция."""
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    rows = await pool.fetch("SELECT user_id FROM users WHERE suit IN ('mn', 'exo') AND deleted_at IS NULL "
                            "AND (miner_bonus_day IS NULL OR miner_bonus_day < $1)", day_start.date())
    paid = 0
    for r in rows:
        try:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    paid += await pay_miner_bonus(conn, r["user_id"], day_start)
        except Exception:
            logger.exception("[GEAR] бонус шахтёра %s не начислен", r["user_id"])
    return paid


GEAR_LOOP_SECONDS = 15 * 60


async def miner_bonus_loop() -> None:
    """Фоновый цикл главного бота: раз в 15 минут доплачивает бонус шахтёра за прошлые сутки (повтор безопасен)."""
    import asyncio
    from shared.database import db
    from shared.economy import utcnow
    while True:
        try:
            await miner_bonus_round(db.pool, utcnow())
        except Exception:
            logger.exception("[GEAR] сбой цикла бонуса шахтёра")
        await asyncio.sleep(GEAR_LOOP_SECONDS)
