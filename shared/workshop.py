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


def recipe_cost(recipe_id: str, armor_level: int = 0, capacity: int = RES_CAPACITY_BASE) -> dict[str, int] | None:
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
    return dict(recipe["cost"])


def recipe_coins(recipe_id: str) -> int:
    """Сколько 🪙 стоит рецепт помимо ресурсов (Шаттл)."""
    return int((WORKSHOP_RECIPES.get(recipe_id) or {}).get("coins", 0))


def can_afford(stock: dict[str, int], cost: dict[str, int] | None) -> bool:
    if cost is None:
        return False
    return all(stock.get(k, 0) >= v for k, v in cost.items())


async def craft(conn, user_id: int, recipe_id: str, now: datetime) -> CraftResult:
    recipe = WORKSHOP_RECIPES.get(recipe_id)
    if recipe is None:
        raise WorkshopError("ws.err_unknown")
    effect = recipe["effect"]

    # Для бустов/дрона/брони сначала закрываем прошлое время фермы по старым ставкам
    if effect in ("nitrogen", "nuclear", "drone", "armor"):
        user, _ = await apply_lazy_farm(conn, user_id, now)
    else:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        raise WorkshopError("common.no_profile")

    if effect == "shuttle" and user["has_shuttle"]:
        raise WorkshopError("ws.err_shuttle_owned")
    armor_now = armor_level_active(user["farm_armor_level"], user["armor_until"], now)

    cost = recipe_cost(recipe_id, armor_now, user["res_capacity"])
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
    if effect in EFFECT_COLUMNS:
        column = EFFECT_COLUMNS[effect]
        until = extend_expiry_hours(user[column], now, recipe["hours"])
        await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1", user_id, until)
        result.until = until
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
    elif effect == "shuttle":
        await conn.execute("UPDATE users SET has_shuttle = TRUE WHERE user_id = $1", user_id)
    elif effect == "storage":
        result.level = next_storage_level(user["res_capacity"])[0]   # новая вместимость
        await conn.execute("UPDATE users SET res_capacity = $2 WHERE user_id = $1", user_id, result.level)
    logger.info("[WORKSHOP] user=%s crafted %s cost=%s", user_id, recipe_id, cost)
    return result
