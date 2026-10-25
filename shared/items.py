"""
📦 Склад изделий (решение владельца 26.10): собранное в мастерской приложения не включается
сразу, а ложится на склад — игрок активирует изделие, когда ему удобно (щит перед сном,
Азот перед долгим отсутствием и т.п.).

Изделие = (эффект, часы): «Азот 6 ч», «Щит 48 ч»… Одинаковые складываются в стопку (qty).
Разовые изделия (Форсаж, Экономайзер, Трюм, Штамп, Ремдрон) хранятся с hours = 0.
Виды активации (числа и колонки — shared/economy.py):
- часовые личные — продлевают users.<колонка> (как покупка за Stars, extend_expiry_hours);
- Термос — окно thermos_from/thermos_until (котлеты Бурильщиков горят на 25% медленнее);
- командные — Знамя (окно бонуса в team_banners) и Купол (teams.dome_until), нужна команда;
- Форсаж — сразу сбрасывает перезарядку налёта (не чаще раза в сутки);
- остальные разовые — «заряд» (+1 к счётчику users.<колонка>), тратится на следующем действии.
Для бустов, дрона и Термоса прошлое время фермы сначала закрывается по старым ставкам.
Всё — внутри транзакции вызывающего кода.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from shared.economy import (FORSAGE_COOLDOWN_HOURS, ITEM_COLUMNS, ITEM_EFFECTS, ITEM_FARM_EFFECTS,
                            ONE_SHOT_COLUMNS, TEAM_ITEM_EFFECTS, extend_expiry_hours)
from shared.locales import t


class ItemError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def is_item_effect(effect: str) -> bool:
    return effect in ITEM_EFFECTS


def is_one_shot(effect: str) -> bool:
    return effect == "forsage" or effect in ONE_SHOT_COLUMNS


async def add_item(conn, user_id: int, effect: str, hours: int, qty: int = 1) -> None:
    if effect not in ITEM_EFFECTS or hours < 0 or qty <= 0 or (hours == 0) != is_one_shot(effect):
        raise ValueError(f"bad item {effect}/{hours}/{qty}")
    await conn.execute(
        """INSERT INTO user_items (user_id, effect, hours, qty) VALUES ($1, $2, $3, $4)
           ON CONFLICT (user_id, effect, hours) DO UPDATE SET qty = user_items.qty + EXCLUDED.qty""",
        user_id, effect, hours, qty)


async def items_count(conn, user_id: int) -> int:
    """Изделий на складе суммарно (все виды и сроки)."""
    return int(await conn.fetchval("SELECT COALESCE(SUM(qty), 0) FROM user_items WHERE user_id = $1", user_id))


async def ensure_items_room(conn, user_id: int, res_capacity: int, qty: int = 1) -> None:
    """Склад изделий не резиновый: не больше items_capacity(вместимость) суммарно."""
    from shared.economy import items_capacity
    cap = items_capacity(res_capacity)
    if await items_count(conn, user_id) + qty > cap:
        raise ItemError("ws.err_items_full", max=cap)


async def list_items(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch(
        "SELECT effect, hours, qty FROM user_items WHERE user_id = $1 AND qty > 0 ORDER BY effect, hours",
        user_id)
    return [dict(r) for r in rows]


def _extend_window(start: datetime | None, end: datetime | None, now: datetime, hours: int):
    """Окно эффекта: идёт — продлеваем конец; нет — новое окно с этого момента."""
    if start is not None and end is not None and end > now:
        return start, end + timedelta(hours=hours)
    return now, now + timedelta(hours=hours)


async def activate_item(conn, user_id: int, effect: str, hours: int, now: datetime) -> dict:
    """Включает одно изделие со склада. Возвращает {effect, until, charges}."""
    from shared.farm_logic import apply_lazy_farm
    from shared.raids import attack_cooldown_left
    if effect not in ITEM_EFFECTS:
        raise ItemError("it.err_none")
    qty = await conn.fetchval(
        "SELECT qty FROM user_items WHERE user_id = $1 AND effect = $2 AND hours = $3 FOR UPDATE",
        user_id, effect, hours)
    if not qty:
        raise ItemError("it.err_none")
    if effect in ITEM_FARM_EFFECTS:
        user, _ = await apply_lazy_farm(conn, user_id, now)
    else:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        raise ItemError("common.no_profile")

    result = {"effect": effect, "until": None, "charges": None}
    if effect in ITEM_COLUMNS:
        column = ITEM_COLUMNS[effect]
        result["until"] = extend_expiry_hours(user[column], now, hours)
        await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1", user_id, result["until"])
    elif effect == "thermos":
        start, end = _extend_window(user["thermos_from"], user["thermos_until"], now, hours)
        await conn.execute("UPDATE users SET thermos_from = $2, thermos_until = $3 WHERE user_id = $1",
                           user_id, start, end)
        result["until"] = end
    elif effect in TEAM_ITEM_EFFECTS:
        team_id = user["team_id"]
        if team_id is None:
            raise ItemError("mk.err_no_team")
        team = await conn.fetchrow("SELECT team_id, dome_until FROM teams WHERE team_id = $1 FOR UPDATE", team_id)
        if team is None:
            raise ItemError("mk.err_no_team")
        if effect == "dome":
            result["until"] = extend_expiry_hours(team["dome_until"], now, hours)
            await conn.execute("UPDATE teams SET dome_until = $2 WHERE team_id = $1", team_id, result["until"])
        else:   # banner: окно бонуса — без бонуса задним числом
            last = await conn.fetchrow(
                "SELECT id, starts_at, ends_at FROM team_banners WHERE team_id = $1 ORDER BY ends_at DESC LIMIT 1",
                team_id)
            if last and last["ends_at"] > now:
                result["until"] = last["ends_at"] + timedelta(hours=hours)
                await conn.execute("UPDATE team_banners SET ends_at = $2 WHERE id = $1", last["id"], result["until"])
            else:
                result["until"] = now + timedelta(hours=hours)
                await conn.execute("INSERT INTO team_banners (team_id, starts_at, ends_at) VALUES ($1, $2, $3)",
                                   team_id, now, result["until"])
    elif effect == "forsage":
        if attack_cooldown_left(user["last_raid_at"], now) <= 0:
            raise ItemError("it.err_no_cooldown")
        used = user["forsage_used_at"]
        if used is not None and used > now - timedelta(hours=FORSAGE_COOLDOWN_HOURS):
            left = used + timedelta(hours=FORSAGE_COOLDOWN_HOURS) - now
            raise ItemError("it.err_forsage_daily", hours=max(1, -(-int(left.total_seconds()) // 3600)))
        await conn.execute("UPDATE users SET last_raid_at = NULL, forsage_used_at = $2 WHERE user_id = $1",
                           user_id, now)
    else:
        column = ONE_SHOT_COLUMNS[effect]
        result["charges"] = await conn.fetchval(
            f"UPDATE users SET {column} = {column} + 1 WHERE user_id = $1 RETURNING {column}", user_id)
    await conn.execute("UPDATE user_items SET qty = qty - 1 WHERE user_id = $1 AND effect = $2 AND hours = $3",
                       user_id, effect, hours)
    return result
