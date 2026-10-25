"""
Мастерская: ресурсы из игр превращаются в пользу для фермы, биржи и обороны.

Рецепты — в shared/economy.WORKSHOP_RECIPES (цены только там). Эффекты:
- nitrogen / nuclear / drone — ЧАСЫ существующих лицензий (бусты, дрон). Перед продлением
  прошлое время фермы закрывается по старым ставкам (apply_lazy_farm) — ничего задним числом;
- shield — щит от налётов (users.raid_shield_until);
- cutlet — кибер-котлета на склад (inv_cutlets);
- armor — Кибер-броня: постоянный +10% к добыче за уровень (users.farm_armor_level, макс 3);
- shuttle — Шаттл: постоянная льгота на бирже (комиссия 5%, лимиты шире), один на игрока.

Всё — внутри транзакции вызывающего кода; списание ресурсов — spend_bundle (всё или ничего).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

from shared.economy import (
    ARMOR_DAYS,
    MAX_CARTS,
    MEGA_CLAN_MAX_MEMBERS,
    TEAM_ITEM_CLAN_MULTIPLIER,
    WORKSHOP_UNLOCK_ORDER,
    recipe_unlock_at,
    ARMOR_MAX_LEVEL,
    RES_CAPACITY_BASE,
    WORKSHOP_RECIPES,
    next_storage_level,
    armor_cost,
    armor_level_active,
    extend_expiry,
    extend_expiry_hours,
)
from shared.ledger import InsufficientFunds, change_balance
from shared.farm_logic import apply_lazy_farm
from shared.locales import t
from shared.items import add_item, is_item_effect
from shared.resources import RESOURCE_ICONS, InsufficientResources, spend_bundle

logger = logging.getLogger(__name__)

EFFECT_COLUMNS = {
    "nitrogen": "boost_nitrogen_until",
    "nuclear": "boost_nuclear_until",
    "drone": "drone_until",
    "shield": "raid_shield_until",
}


class WorkshopError(Exception):
    """Причина отказа: ключ локали + параметры."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


@dataclass
class CraftResult:
    recipe_id: str
    effect: str
    cost: dict[str, int]
    until: datetime | None = None
    qty: int = 0
    level: int = 0
    stock: dict[str, int] = field(default_factory=dict)
    stored: bool = False   # изделие легло на склад (активируется игроком позже)


def team_cost_multiplier(max_members: int | None) -> int:
    """Командные изделия у Мега-Клана дороже в TEAM_ITEM_CLAN_MULTIPLIER раз."""
    return TEAM_ITEM_CLAN_MULTIPLIER if (max_members or 0) >= MEGA_CLAN_MAX_MEMBERS else 1


def recipe_tool(recipe_id: str, armor_level: int = 0) -> int:
    """Какой набор инструментов нужен рецепту (броня: уровень = набор)."""
    recipe = WORKSHOP_RECIPES.get(recipe_id) or {}
    if recipe.get("effect") == "armor":
        return min(armor_level + 1, ARMOR_MAX_LEVEL)
    return int(recipe.get("tool", 0))


def recipe_cost(recipe_id: str, armor_level: int = 0, capacity: int = RES_CAPACITY_BASE,
                team_mult: int = 1) -> dict[str, int] | None:
    """
    Цена рецепта в ресурсах; для брони зависит от ДЕЙСТВУЮЩЕГО уровня
    (на максимуме — цена продления максимального уровня). None — рецепта нет.
    """
    recipe = WORKSHOP_RECIPES.get(recipe_id)
    if recipe is None:
        return None
    if recipe["effect"] == "armor":
        return armor_cost(armor_level + 1)
    if recipe["effect"] == "storage":
        nxt = next_storage_level(capacity)
        return nxt[1] if nxt else None
    mult = team_mult if recipe.get("team") else 1
    return {k: v * mult for k, v in recipe["cost"].items()}


def recipe_coins(recipe_id: str) -> int:
    """Сколько 🪙 стоит рецепт помимо ресурсов (Шаттл)."""
    return int((WORKSHOP_RECIPES.get(recipe_id) or {}).get("coins", 0))


def can_afford(stock: dict[str, int], cost: dict[str, int] | None) -> bool:
    if cost is None:
        return False
    return all(stock.get(k, 0) >= v for k, v in cost.items())


async def craft(conn, user_id: int, recipe_id: str, now: datetime, to_storage: bool = False) -> CraftResult:
    """to_storage=True (приложение): часы бустов/дрона/щита ложатся на склад изделий, а не включаются."""
    recipe = WORKSHOP_RECIPES.get(recipe_id)
    if recipe is None:
        raise WorkshopError("ws.err_unknown")
    effect = recipe["effect"]
    # Новые изделия (маскировка, приманка, форсаж…) ВСЕГДА ложатся на склад; четыре старых —
    # на склад только из приложения (чатовая мастерская-фолбэк включает их сразу, как раньше)
    store = is_item_effect(effect) and (to_storage or effect not in EFFECT_COLUMNS)
    from shared.feature_flags import get_flag
    if not await get_flag(f"wsr:{recipe_id}"):
        raise WorkshopError("ws.err_off")

    # Для бустов/дрона/брони сначала закрываем прошлое время фермы по старым ставкам
    if effect in ("nitrogen", "nuclear", "drone", "armor") and not store:
        user, _ = await apply_lazy_farm(conn, user_id, now)
    else:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        raise WorkshopError("common.no_profile")

    # Поэтапное открытие: новичку — по рецепту в сутки (WORKSHOP_UNLOCK_ORDER)
    if recipe_id in WORKSHOP_UNLOCK_ORDER and user["created_at"] is not None:
        opens = recipe_unlock_at(recipe_id, user["created_at"])
        if opens > now:
            raise WorkshopError("ws.err_locked", hours=max(1, -(-int((opens - now).total_seconds()) // 3600)))
    week_limit = recipe.get("week_limit")
    if week_limit:
        from shared.weekly_recipes import week_start
        done = await conn.fetchval(
            "SELECT COUNT(*) FROM weekly_crafts WHERE user_id = $1 AND recipe_id = $2 AND created_at >= $3",
            user_id, f"ws:{recipe_id}", week_start(now))
        if done >= week_limit:
            raise WorkshopError("wk.err_limit", limit=week_limit)
    if effect == "shuttle" and user["has_shuttle"]:
        raise WorkshopError("ws.err_shuttle_owned")
    armor_now = armor_level_active(user["farm_armor_level"], user["armor_until"], now)
    # Наборы инструментов из Лаборатории открывают сложные сборки
    need_tool = recipe_tool(recipe_id, armor_now)
    if need_tool:
        from shared.tech import tech_levels
        if (await tech_levels(conn, user_id))["tools"] < need_tool:
            raise WorkshopError("tech.err_tool", tool=need_tool)
    team_mult = 1
    if recipe.get("team"):   # командное изделие: нужна команда, Мега-Клан платит больше
        if user["team_id"] is None:
            raise WorkshopError("mk.err_no_team")
        team_mult = team_cost_multiplier(await conn.fetchval(
            "SELECT max_members FROM teams WHERE team_id = $1", user["team_id"]))
    if effect == "cart" and (user["carts"] >= MAX_CARTS or user["carts"] >= user["horses"]):
        raise WorkshopError("cart.err_horse", max=MAX_CARTS)
    if store:   # склад изделий: суммарно не больше 10% вместимости
        from shared.items import ItemError, ensure_items_room
        try:
            await ensure_items_room(conn, user_id, user["res_capacity"])
        except ItemError as e:
            raise WorkshopError(e.key, **e.kwargs) from e

    cost = recipe_cost(recipe_id, armor_now, user["res_capacity"], team_mult)
    if cost is None:
        raise WorkshopError("ws.err_storage_max" if effect == "storage" else "ws.err_unknown")
    coins = recipe_coins(recipe_id)
    if coins and user["balance"] < coins:
        raise WorkshopError("ws.err_coins", need=coins, have=user["balance"])
    try:
        stock = await spend_bundle(conn, user_id, cost, f"craft:{recipe_id}")
    except InsufficientResources as e:
        raise WorkshopError("ws.err_resources", need=e.need, have=e.have,
                            kind=RESOURCE_ICONS[e.kind]) from e
    if coins:
        try:
            await change_balance(conn, user_id, -coins, f"craft:{recipe_id}")
        except InsufficientFunds as e:   # гонка с другой тратой: транзакция откатит и ресурсы
            raise WorkshopError("ws.err_coins", need=coins, have=user["balance"]) from e

    result = CraftResult(recipe_id=recipe_id, effect=effect, cost=cost, stock=stock)
    if recipe.get("week_limit"):
        await conn.execute("INSERT INTO weekly_crafts (user_id, recipe_id, created_at) VALUES ($1, $2, $3)",
                           user_id, f"ws:{recipe_id}", now)
    if store:
        await add_item(conn, user_id, effect, recipe.get("hours", 0))
        result.stored = True
    elif effect in EFFECT_COLUMNS:
        column = EFFECT_COLUMNS[effect]
        until = extend_expiry_hours(user[column], now, recipe["hours"])
        await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1", user_id, until)
        result.until = until
    elif effect == "make":   # костёр, батарейки: сырьё → материал на склад (в пределах вместимости)
        from shared.resources import change_resource
        for kind, qty in recipe["make"].items():
            await change_resource(conn, user_id, kind, qty, f"craft:{recipe_id}", cap=user["res_capacity"])
        result.qty = sum(recipe["make"].values())
    elif effect == "cart":
        await conn.execute("UPDATE users SET carts = carts + 1 WHERE user_id = $1", user_id)
        result.level = user["carts"] + 1
    elif effect == "cutlet":
        await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                           user_id, recipe["qty"])
        result.qty = recipe["qty"]
    elif effect == "armor":
        # Уровень вверх (или продление максимального) и +30 дней к сроку брони
        result.level = min(armor_now + 1, ARMOR_MAX_LEVEL)
        result.until = extend_expiry(user["armor_until"] if armor_now else None, now, ARMOR_DAYS)
        await conn.execute("UPDATE users SET farm_armor_level = $2, armor_until = $3 WHERE user_id = $1",
                           user_id, result.level, result.until)
    elif effect == "shuttle":   # новый Шаттл приходит заряженным на месяц
        from shared.economy import SHUTTLE_CHARGE_DAYS
        await conn.execute("UPDATE users SET has_shuttle = TRUE, shuttle_until = $2 WHERE user_id = $1",
                           user_id, extend_expiry(None, now, SHUTTLE_CHARGE_DAYS))
    elif effect == "storage":
        result.level = next_storage_level(user["res_capacity"])[0]   # новая вместимость
        await conn.execute("UPDATE users SET res_capacity = $2 WHERE user_id = $1", user_id, result.level)
    logger.info("[WORKSHOP] user=%s crafted %s cost=%s", user_id, recipe_id, cost)
    return result
