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
    ARMOR_MAX_LEVEL,
    WORKSHOP_RECIPES,
    armor_cost,
    extend_expiry_hours,
)
from shared.farm_logic import apply_lazy_farm
from shared.locales import t
from shared.resources import InsufficientResources, spend_bundle

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


def recipe_cost(recipe_id: str, armor_level: int = 0) -> dict[str, int] | None:
    """Цена рецепта; для брони зависит от текущего уровня. None — рецепт недоступен."""
    recipe = WORKSHOP_RECIPES.get(recipe_id)
    if recipe is None:
        return None
    if recipe["effect"] == "armor":
        return armor_cost(armor_level + 1)
    return dict(recipe["cost"])


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
    if effect == "armor" and user["farm_armor_level"] >= ARMOR_MAX_LEVEL:
        raise WorkshopError("ws.err_armor_max", max=ARMOR_MAX_LEVEL)

    cost = recipe_cost(recipe_id, user["farm_armor_level"])
    if cost is None:
        raise WorkshopError("ws.err_unknown")
    try:
        stock = await spend_bundle(conn, user_id, cost, f"craft:{recipe_id}")
    except InsufficientResources as e:
        raise WorkshopError("ws.err_resources", need=e.need, have=e.have,
                            kind=t("ru", f"res.{e.kind}")) from e

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
        result.level = user["farm_armor_level"] + 1
        await conn.execute("UPDATE users SET farm_armor_level = $2 WHERE user_id = $1",
                           user_id, result.level)
    elif effect == "shuttle":
        await conn.execute("UPDATE users SET has_shuttle = TRUE WHERE user_id = $1", user_id)
    logger.info("[WORKSHOP] user=%s crafted %s cost=%s", user_id, recipe_id, cost)
    return result
