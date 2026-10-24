"""
Рецепты недели (решение владельца 25.10): временные рецепты мастерской, которые владелец
включает и выключает в админ-боте (/recipes) — «ежедневное — обыденность, редкое — событие».

Каталог — WEEKLY_RECIPES ниже (40 вариантов). Каждый рецепт: цена в ресурсах, список эффектов
и лимит сборок на игрока за неделю (неделя UTC с понедельника 00:00). Видимость — тумблер
feature_flags "recipe:<id>" (по умолчанию ВЫКЛЮЧЕН — запуск только владельцем).

Типы эффектов:
- nitrogen / nuclear / drone / shield / unlimit — часы соответствующей лицензии
  (прошлое время фермы закрывается ДО продления, задним числом бусты не действуют);
- cutlet — котлеты на склад (qty);
- resource — ресурс kind на склад (qty), в пределах вместимости склада.
Названия рецептов собираются из эффектов (локализованные шаблоны wk.eff_*) — новый рецепт
не требует переводов.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from shared.economy import extend_expiry_hours, utcnow
from shared.locales import t
from shared.resources import RESOURCE_ICONS, InsufficientResources, change_resource, spend_bundle

logger = logging.getLogger(__name__)


def _e(effect_type: str, **kw) -> dict:
    return {"type": effect_type, **kw}


# fmt: off
WEEKLY_RECIPES: dict[str, dict] = {
    # ---- Азотное Охлаждение
    "w_nitro_12h":      {"cost": {"metal": 30, "hydrogen": 30}, "effects": [_e("nitrogen", hours=12)], "limit": 2},
    "w_nitro_24h":      {"cost": {"metal": 50, "hydrogen": 50, "crystal": 10}, "effects": [_e("nitrogen", hours=24)], "limit": 1},
    "w_nitro_metal":    {"cost": {"metal": 60}, "effects": [_e("nitrogen", hours=6)], "limit": 3},
    "w_nitro_crystal":  {"cost": {"crystal": 40}, "effects": [_e("nitrogen", hours=6)], "limit": 3},
    "w_nitro_3days":    {"cost": {"metal": 150, "hydrogen": 150}, "effects": [_e("nitrogen", hours=72)], "limit": 1},
    # ---- Ядерный Разгон
    "w_nuclear_6h":     {"cost": {"metal": 70, "hydrogen": 50, "parts": 20}, "effects": [_e("nuclear", hours=6)], "limit": 1},
    "w_nuclear_parts":  {"cost": {"parts": 90}, "effects": [_e("nuclear", hours=3)], "limit": 2},
    "w_nuclear_hydro":  {"cost": {"hydrogen": 80}, "effects": [_e("nuclear", hours=3)], "limit": 2},
    "w_weekend_rush":   {"cost": {"hydrogen": 60, "parts": 60}, "effects": [_e("nuclear", hours=6)], "limit": 1},
    # ---- Мастер-дрон
    "w_drone_48h":      {"cost": {"metal": 40, "parts": 40}, "effects": [_e("drone", hours=48)], "limit": 1},
    "w_drone_crystal":  {"cost": {"crystal": 50}, "effects": [_e("drone", hours=24)], "limit": 2},
    "w_drone_72h":      {"cost": {"metal": 60, "parts": 60, "crystal": 20}, "effects": [_e("drone", hours=72)], "limit": 1},
    "w_drone_week":     {"cost": {"parts": 150}, "effects": [_e("drone", hours=168)], "limit": 1},
    # ---- Щит от налётов
    "w_shield_48h":     {"cost": {"metal": 15, "crystal": 15}, "effects": [_e("shield", hours=48)], "limit": 1},
    "w_shield_metal":   {"cost": {"metal": 30}, "effects": [_e("shield", hours=24)], "limit": 2},
    "w_shield_parts":   {"cost": {"parts": 25}, "effects": [_e("shield", hours=12)], "limit": 3},
    "w_shield_week":    {"cost": {"metal": 60, "crystal": 60, "parts": 30}, "effects": [_e("shield", hours=168)], "limit": 1},
    # ---- Котлеты (лимит 1 в неделю: топливо — право магазина)
    "w_cutlet_metal":   {"cost": {"metal": 100}, "effects": [_e("cutlet", qty=1)], "limit": 1},
    "w_cutlet_hydro":   {"cost": {"hydrogen": 100}, "effects": [_e("cutlet", qty=1)], "limit": 1},
    "w_cutlet_crystal": {"cost": {"crystal": 100}, "effects": [_e("cutlet", qty=1)], "limit": 1},
    "w_cutlet_parts":   {"cost": {"parts": 100}, "effects": [_e("cutlet", qty=1)], "limit": 1},
    "w_cutlet_pair":    {"cost": {"metal": 120, "hydrogen": 120, "crystal": 60, "parts": 60}, "effects": [_e("cutlet", qty=2)], "limit": 1},
    # ---- Комбо
    "w_combo_guard":    {"cost": {"metal": 40, "hydrogen": 30, "crystal": 20}, "effects": [_e("nitrogen", hours=12), _e("shield", hours=12)], "limit": 1},
    "w_combo_keeper":   {"cost": {"metal": 40, "parts": 40, "crystal": 20}, "effects": [_e("drone", hours=24), _e("shield", hours=24)], "limit": 1},
    "w_combo_turbo":    {"cost": {"metal": 80, "hydrogen": 70, "parts": 30}, "effects": [_e("nitrogen", hours=6), _e("nuclear", hours=3)], "limit": 1},
    "w_combo_full":     {"cost": {"metal": 120, "hydrogen": 100, "crystal": 60, "parts": 60},
                         "effects": [_e("nitrogen", hours=24), _e("nuclear", hours=6), _e("drone", hours=24)], "limit": 1},
    "w_fortress":       {"cost": {"metal": 100, "crystal": 100}, "effects": [_e("shield", hours=168), _e("drone", hours=24)], "limit": 1},
    "w_raider_kit":     {"cost": {"crystal": 40, "parts": 20}, "effects": [_e("resource", kind="hydrogen", qty=25), _e("shield", hours=12)], "limit": 2},
    "w_lucky_cutlet":   {"cost": {"metal": 40, "hydrogen": 40, "crystal": 40, "parts": 40}, "effects": [_e("cutlet", qty=1), _e("shield", hours=24)], "limit": 1},
    # ---- Переплавка ресурсов (курс 2:1 — сток ресурсов)
    "w_conv_metal_hydro":   {"cost": {"metal": 40}, "effects": [_e("resource", kind="hydrogen", qty=20)], "limit": 5},
    "w_conv_hydro_metal":   {"cost": {"hydrogen": 40}, "effects": [_e("resource", kind="metal", qty=20)], "limit": 5},
    "w_conv_crystal_parts": {"cost": {"crystal": 40}, "effects": [_e("resource", kind="parts", qty=20)], "limit": 5},
    "w_conv_parts_crystal": {"cost": {"parts": 40}, "effects": [_e("resource", kind="crystal", qty=20)], "limit": 5},
    "w_conv_metal_crystal": {"cost": {"metal": 40}, "effects": [_e("resource", kind="crystal", qty=20)], "limit": 5},
    "w_conv_parts_hydro":   {"cost": {"parts": 40}, "effects": [_e("resource", kind="hydrogen", qty=20)], "limit": 5},
    "w_hydro_reactor":      {"cost": {"metal": 20, "crystal": 20, "parts": 20}, "effects": [_e("resource", kind="hydrogen", qty=30)], "limit": 3},
    "w_hydro_split":        {"cost": {"hydrogen": 45},
                             "effects": [_e("resource", kind="metal", qty=10), _e("resource", kind="crystal", qty=10),
                                         _e("resource", kind="parts", qty=10)], "limit": 3},
    # ---- Пробники Безлимита (короткие — продают суточный Безлимит за ★)
    "w_unlimit_1h":     {"cost": {"crystal": 60, "parts": 40}, "effects": [_e("unlimit", hours=1)], "limit": 1},
    "w_unlimit_2h":     {"cost": {"crystal": 120}, "effects": [_e("unlimit", hours=2)], "limit": 1},
    "w_unlimit_3h":     {"cost": {"metal": 80, "hydrogen": 60, "crystal": 60, "parts": 60}, "effects": [_e("unlimit", hours=3)], "limit": 1},
}
# fmt: on

HOURS_COLUMNS = {
    "nitrogen": "boost_nitrogen_until",
    "nuclear": "boost_nuclear_until",
    "drone": "drone_until",
    "shield": "raid_shield_until",
    "unlimit": "unlimit_until",
}
FARM_EFFECTS = ("nitrogen", "nuclear", "drone")


class WeeklyError(Exception):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def week_start(now: datetime) -> datetime:
    """Понедельник 00:00 UTC текущей недели."""
    monday = now - timedelta(days=now.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def effect_label(lang: str, effect: dict) -> str:
    kind = effect["type"]
    if kind in HOURS_COLUMNS:
        return t(lang, f"wk.eff_{kind}", h=effect["hours"])
    if kind == "cutlet":
        return t(lang, "wk.eff_cutlet", n=effect["qty"])
    return t(lang, "wk.eff_resource", icon=RESOURCE_ICONS[effect["kind"]], n=effect["qty"])


def recipe_title(lang: str, rid: str) -> str:
    return " + ".join(effect_label(lang, e) for e in WEEKLY_RECIPES[rid]["effects"])


async def active_weekly_ids() -> list[str]:
    from shared.feature_flags import get_flag
    return [rid for rid in WEEKLY_RECIPES if await get_flag(f"recipe:{rid}")]


async def crafted_this_week(conn, user_id: int, rid: str, now: datetime) -> int:
    return await conn.fetchval(
        "SELECT COUNT(*) FROM weekly_crafts WHERE user_id = $1 AND recipe_id = $2 AND created_at >= $3",
        user_id, rid, week_start(now))


async def craft_weekly(conn, user_id: int, rid: str, now: datetime | None = None,
                       enabled: bool | None = None, to_storage: bool = False) -> dict:
    """
    Собирает рецепт недели. enabled=None — проверить тумблер. Внутри транзакции вызывающего.
    to_storage=True (приложение): часовые эффекты ложатся на склад изделий.
    """
    from shared.items import add_item
    from shared.farm_logic import apply_lazy_farm
    from shared.resources import resource_capacity
    now = now or utcnow()
    recipe = WEEKLY_RECIPES.get(rid)
    if recipe is None:
        raise WeeklyError("ws.err_unknown")
    if enabled is None:
        from shared.feature_flags import get_flag
        enabled = await get_flag(f"recipe:{rid}")
    if not enabled:
        raise WeeklyError("wk.err_gone")

    effects = recipe["effects"]
    if not to_storage and any(e["type"] in FARM_EFFECTS for e in effects):
        user, _ = await apply_lazy_farm(conn, user_id, now)
    else:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        raise WeeklyError("common.no_profile")
    done = await crafted_this_week(conn, user_id, rid, now)
    if done >= recipe["limit"]:
        raise WeeklyError("wk.err_limit", limit=recipe["limit"])
    try:
        await spend_bundle(conn, user_id, recipe["cost"], f"weekly:{rid}")
    except InsufficientResources as e:
        raise WeeklyError("ws.err_resources", need=e.need, have=e.have, kind=RESOURCE_ICONS[e.kind]) from e

    cap = await resource_capacity(conn, user_id)
    for effect in effects:
        kind = effect["type"]
        if kind in HOURS_COLUMNS and to_storage:
            await add_item(conn, user_id, kind, effect["hours"])
        elif kind in HOURS_COLUMNS:
            column = HOURS_COLUMNS[kind]
            current = await conn.fetchval(f"SELECT {column} FROM users WHERE user_id = $1", user_id)
            until = extend_expiry_hours(current, now, effect["hours"])
            await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1", user_id, until)
        elif kind == "cutlet":
            await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                               user_id, effect["qty"])
        elif kind == "resource":
            await change_resource(conn, user_id, effect["kind"], effect["qty"], f"weekly:{rid}", cap=cap)
    await conn.execute("INSERT INTO weekly_crafts (user_id, recipe_id, created_at) VALUES ($1, $2, $3)",
                       user_id, rid, now)
    logger.info("[WEEKLY] user=%s crafted %s", user_id, rid)
    return {"recipe": rid, "left": recipe["limit"] - done - 1}
