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

💠 Артефакты (30.10, вечер): в сумке — строка user_gear с suit = a<вид> и slot = 'art'; на поясе — user_equip со
слотом a1/a2/a3. Сумма бонусов пояса — users.art_bonus (JSONB {линия: %}), складывается с костюмом
(economy.user_bonus). Бесплатно — не больше ARTIFACT_SEASON_CAP за сезон.
"""
from __future__ import annotations

import json
import logging
import random
from datetime import datetime, timedelta

from shared.economy import (
    ARTIFACT_BAG_SLOT,
    ARTIFACT_KINDS,
    ARTIFACT_SEASON_CAP,
    ARTIFACT_SLOTS,
    art_bonus_total,
    art_code,
    art_kind,
    gear_bonus,
    GEAR_EXO,
    GEAR_EXO_COINS,
    GEAR_EXO_COST,
    GEAR_MAX_LEVEL,
    GEAR_SEASON_CAP,
    GEAR_SLOTS,
    GEAR_SUITS,
    GEAR_UPGRADE_COINS,
    GEAR_UPGRADE_COST,
    SUIT_BONUS,
    miner_bonus,
    season_bounds,
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
    if slot == ARTIFACT_BAG_SLOT and art_kind(suit):
        return
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
    if not all(p in worn for p in GEAR_SLOTS):
        return None, 0
    suits = {worn[p]["suit"] for p in GEAR_SLOTS}
    if len(suits) != 1:
        return None, 0
    return suits.pop(), min(worn[p]["level"] for p in GEAR_SLOTS)


def belt_bonus(worn: dict[str, dict]) -> dict[str, int]:
    return art_bonus_total(art_kind(worn[s]["suit"]) for s in ARTIFACT_SLOTS if s in worn)


async def _refresh_suit(conn, user_id: int, now: datetime) -> tuple[str | None, int]:
    """Пересчитывает users.suit/suit_level/art_bonus; suit_since сбрасывается, если сменился костюм или пояс."""
    worn = await equipped(conn, user_id)
    suit, level = full_set(worn)
    art = json.dumps(belt_bonus(worn), sort_keys=True)
    await conn.execute(
        "UPDATE users SET suit_since = CASE WHEN suit IS DISTINCT FROM $2 OR art_bonus <> $5::jsonb THEN $4 "
        "ELSE suit_since END, suit = $2, suit_level = $3, art_bonus = $5::jsonb WHERE user_id = $1",
        user_id, suit, level if suit else None, now, art)
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
    if slot not in GEAR_SLOTS:
        raise GearError("gear.err_unknown")   # артефакты — equip_artifact
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
    if slot not in GEAR_SLOTS and slot not in ARTIFACT_SLOTS:
        raise GearError("gear.err_unknown")
    await _lock(conn, user_id)
    old = await conn.fetchrow("DELETE FROM user_equip WHERE user_id = $1 AND slot = $2 RETURNING suit, level",
                              user_id, slot)
    if old is None:
        raise GearError("gear.err_none")
    bag_slot = ARTIFACT_BAG_SLOT if slot in ARTIFACT_SLOTS else slot
    await change_gear(conn, user_id, old["suit"], bag_slot, old["level"], 1, "unequip")
    return await _refresh_suit(conn, user_id, now)


async def equip_artifact(conn, user_id: int, kind: str, slot: str | None, now: datetime) -> tuple[str | None, int]:
    """Артефакт из сумки — на пояс (в указанное окошко или первое свободное; занятое — старый камень в сумку)."""
    if kind not in ARTIFACT_KINDS or (slot is not None and slot not in ARTIFACT_SLOTS):
        raise GearError("gear.err_unknown")
    await _lock(conn, user_id)
    worn = await equipped(conn, user_id)
    if slot is None:
        slot = next((s for s in ARTIFACT_SLOTS if s not in worn), ARTIFACT_SLOTS[0])
    code = art_code(kind)
    await change_gear(conn, user_id, code, ARTIFACT_BAG_SLOT, 1, -1, "equip")
    old = await conn.fetchrow("DELETE FROM user_equip WHERE user_id = $1 AND slot = $2 RETURNING suit, level",
                              user_id, slot)
    if old:
        await change_gear(conn, user_id, old["suit"], ARTIFACT_BAG_SLOT, old["level"], 1, "unequip")
    await conn.execute("INSERT INTO user_equip (user_id, slot, suit, level) VALUES ($1, $2, $3, 1)", user_id, slot, code)
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
        from shared.trophies import move_gear_history
        await move_gear_history(conn, user_id, suit, slot, 1, GEAR_MAX_LEVEL)
        return await _refresh_suit(conn, user_id, now)
    worn = await conn.fetchrow("SELECT suit, level FROM user_equip WHERE user_id = $1 AND slot = $2", user_id, slot)
    if not worn or worn["suit"] != suit:
        raise GearError("gear.err_none")
    if worn["level"] >= GEAR_MAX_LEVEL:
        raise GearError("gear.err_max")
    await _spend(conn, user_id, GEAR_UPGRADE_COST[suit], GEAR_UPGRADE_COINS, "gear_upgrade", ref)
    await conn.execute("UPDATE user_equip SET level = $3 WHERE user_id = $1 AND slot = $2", user_id, slot, GEAR_MAX_LEVEL)
    from shared.trophies import move_gear_history
    await move_gear_history(conn, user_id, suit, slot, 1, GEAR_MAX_LEVEL)
    await conn.execute(
        "INSERT INTO gear_ledger (user_id, suit, slot, level, delta, reason, ref) VALUES ($1, $2, $3, $4, 0, $5, $6)",
        user_id, suit, slot, GEAR_MAX_LEVEL, "gear_upgrade_worn", ref)
    return await _refresh_suit(conn, user_id, now)


async def exo_ready(conn, user_id: int) -> dict:
    """Сколько из 30 деталей 2-го уровня есть (в сумке или надето) — для сплава нано-экзо-брони."""
    rows = await conn.fetch(
        """SELECT suit, slot FROM user_gear WHERE user_id = $1 AND level = $2 AND qty > 0 AND suit = ANY($3::text[])
           UNION SELECT suit, slot FROM user_equip WHERE user_id = $1 AND level = $2 AND suit = ANY($3::text[])""",
        user_id, GEAR_MAX_LEVEL, list(GEAR_SUITS))
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
    for row in await conn.fetch("DELETE FROM user_equip WHERE user_id = $1 AND slot = ANY($2::text[]) "
                                "RETURNING slot, suit, level", user_id, list(GEAR_SLOTS)):
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
async def season_drops(conn, user_id: int, now: datetime, artifacts: bool = False) -> int:
    """Сколько бесплатных деталей (или артефактов) игрок получил в текущем сезоне — для лимита."""
    start, end = season_bounds(now)
    return await conn.fetchval(
        "SELECT COALESCE(SUM(delta), 0) FROM gear_ledger WHERE user_id = $1 AND reason = 'drop' "
        "AND created_at >= $2 AND created_at < $3 AND (slot = 'art') = $4", user_id, start, end, artifacts)


async def drop_artifacts(conn, user_id: int, qty: int, ref: str, now: datetime,
                         rng: random.Random | None = None, capped: bool = True) -> list[str]:
    """Случайные артефакты, не больше остатка сезонного лимита. Возвращает виды.
    capped=False — личный подарок владельца из пульта: лимит не проверяется и не тратится (reason 'gift')."""
    rng = rng or random.SystemRandom()
    left = ARTIFACT_SEASON_CAP - await season_drops(conn, user_id, now, artifacts=True) if capped else qty
    out = []
    for _ in range(max(0, min(qty, left))):
        kind = rng.choice(ARTIFACT_KINDS)
        await change_gear(conn, user_id, art_code(kind), ARTIFACT_BAG_SLOT, 1, 1, "drop" if capped else "gift", ref)
        out.append(kind)
    return out


async def drop_random(conn, user_id: int, qty: int, ref: str, now: datetime,
                      rng: random.Random | None = None, capped: bool = True) -> list[tuple[str, str]]:
    """Случайные детали 1-го уровня, не больше остатка сезонного лимита. Возвращает [(костюм, слот)].
    capped=False — личный подарок владельца из пульта: лимит не проверяется и не тратится (reason 'gift')."""
    rng = rng or random.SystemRandom()
    left = GEAR_SEASON_CAP - await season_drops(conn, user_id, now) if capped else qty
    out = []
    for _ in range(max(0, min(qty, left))):
        suit, slot = rng.choice(GEAR_SUITS), rng.choice(GEAR_SLOTS)
        await change_gear(conn, user_id, suit, slot, 1, 1, "drop" if capped else "gift", ref)
        out.append((suit, slot))
    return out


async def referral_suit_state(conn, user_id: int) -> dict:
    """🤝 Задание «Друзья»: сколько активных друзей и забран ли костюм."""
    from shared.economy import REFERRAL_SUIT_FRIENDS
    friends = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1 AND qualified_at IS NOT NULL", user_id) or 0
    taken = await conn.fetchval("SELECT ref_suit FROM users WHERE user_id = $1", user_id)
    return {"need": REFERRAL_SUIT_FRIENDS, "friends": int(friends), "taken": taken,
            "pct": {k: SUIT_BONUS[k][1] for k in GEAR_SUITS}}


async def claim_referral_suit(conn, user_id: int, suit: str) -> None:
    """Полный костюм (5 деталей 1 ур.) на выбор за REFERRAL_SUIT_FRIENDS активных друзей — один раз.
    Награда, а не «выпадение»: сезонный лимит деталей не тратит (reason 'ref_suit')."""
    if suit not in GEAR_SUITS:
        raise GearError("gear.err_unknown")
    st = await referral_suit_state(conn, user_id)
    if st["friends"] < st["need"]:
        raise GearError("gear.err_ref_need", n=st["need"], have=st["friends"])
    taken = await conn.fetchval("UPDATE users SET ref_suit = $2 WHERE user_id = $1 AND ref_suit IS NULL RETURNING ref_suit",
                                user_id, suit)
    if taken is None:
        raise GearError("gear.err_ref_taken")
    for slot in GEAR_SLOTS:
        await change_gear(conn, user_id, suit, slot, 1, 1, "ref_suit", "friends")


# ============================================================================
# ⛏ Бонус шахтёра: раз в сутки — % от монет фермы, добытых за прошлые сутки UTC (после того, как надет костюм)
# ============================================================================
async def pay_miner_bonus(conn, user_id: int, day_start: datetime) -> int:
    """Начисляет бонус за сутки [day_start, +1 день). Идемпотентно: users.miner_bonus_day. Возвращает сумму."""
    user = await conn.fetchrow("SELECT suit, suit_level, art_bonus, suit_since, miner_bonus_day FROM users WHERE user_id = $1 "
                               "AND deleted_at IS NULL AND NOT is_blocked FOR UPDATE", user_id)
    day = day_start.date()
    if user is None or (user["miner_bonus_day"] is not None and user["miner_bonus_day"] >= day):
        return 0
    await conn.execute("UPDATE users SET miner_bonus_day = $2 WHERE user_id = $1", user_id, day)
    art = user["art_bonus"]
    pct = gear_bonus(user["suit"], user["suit_level"], json.loads(art) if isinstance(art, str) else art, "mn")
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
    rows = await pool.fetch("SELECT user_id FROM users WHERE (suit IN ('mn', 'exo') OR art_bonus ? 'mn') "
                            "AND deleted_at IS NULL "
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
