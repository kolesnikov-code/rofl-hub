"""
📦 Склад изделий (решение владельца 26.10): собранное в мастерской приложения не включается
сразу, а ложится на склад — игрок активирует изделие, когда ему удобно (щит перед сном,
Азот перед долгим отсутствием и т.п.).

Изделие = (эффект, часы): «Азот 6 ч», «Щит 48 ч»… Одинаковые складываются в стопку (qty).
Активация продлевает ту же лицензию, что и покупка за Stars (extend_expiry_hours), для бустов
и дрона прошлое время фермы сначала закрывается по старым ставкам — задним числом ничего.
Всё — внутри транзакции вызывающего кода.
"""
from __future__ import annotations

from datetime import datetime

from shared.economy import ITEM_COLUMNS, ITEM_EFFECTS, ITEM_FARM_EFFECTS, extend_expiry_hours
from shared.locales import t


class ItemError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def is_item_effect(effect: str) -> bool:
    return effect in ITEM_EFFECTS


async def add_item(conn, user_id: int, effect: str, hours: int, qty: int = 1) -> None:
    if effect not in ITEM_EFFECTS or hours <= 0 or qty <= 0:
        raise ValueError(f"bad item {effect}/{hours}/{qty}")
    await conn.execute(
        """INSERT INTO user_items (user_id, effect, hours, qty) VALUES ($1, $2, $3, $4)
           ON CONFLICT (user_id, effect, hours) DO UPDATE SET qty = user_items.qty + EXCLUDED.qty""",
        user_id, effect, hours, qty)


async def list_items(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch(
        "SELECT effect, hours, qty FROM user_items WHERE user_id = $1 AND qty > 0 ORDER BY effect, hours",
        user_id)
    return [dict(r) for r in rows]


async def activate_item(conn, user_id: int, effect: str, hours: int, now: datetime) -> datetime:
    """Включает одно изделие со склада. Возвращает новый срок действия."""
    from shared.farm_logic import apply_lazy_farm
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
    column = ITEM_COLUMNS[effect]
    until = extend_expiry_hours(user[column], now, hours)
    await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1", user_id, until)
    await conn.execute("UPDATE user_items SET qty = qty - 1 WHERE user_id = $1 AND effect = $2 AND hours = $3",
                       user_id, effect, hours)
    return until
