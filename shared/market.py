"""
Биржа котлет: игроки продают кибер-котлеты со склада за монеты (решение владельца 22.10).

Ядро без Telegram — только asyncpg-соединение внутри транзакции вызывающего кода.

Правила:
- продавец выставляет ордер: qty котлет со СКЛАДА (inv_cutlets) по цене price монет
  за штуку; котлеты уходят в эскроу ордера сразу (отмена возвращает их на склад);
- покупатель платит qty*price монет: MARKET_FEE_PERCENT сгорает (дефляция — списано,
  но не зачислено), остальное получает продавец; котлеты падают покупателю на склад;
- частичная покупка допустима; ордер закрывается, когда qty = 0;
- все движения монет — через ledger: market_buy / market_sell; строки users
  блокируются FOR UPDATE в порядке возрастания user_id (анти-дедлок, как в переводах).
"""
from __future__ import annotations

import logging

from shared.economy import (
    MARKET_FEE_PERCENT,
    MARKET_MAX_OPEN_ORDERS,
    MARKET_MAX_PRICE,
    MARKET_MAX_QTY,
    MARKET_MIN_PRICE,
    market_fee,
)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t

logger = logging.getLogger(__name__)


class MarketError(Exception):
    """Причина отказа: ключ локали + параметры (локализуется в обработчике)."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(t("ru", key, **kwargs))

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def validate_order(qty: int, price: int) -> None:
    if qty <= 0 or qty > MARKET_MAX_QTY:
        raise MarketError("mk.err_qty", max=MARKET_MAX_QTY)
    if price < MARKET_MIN_PRICE or price > MARKET_MAX_PRICE:
        raise MarketError("mk.err_price", min=MARKET_MIN_PRICE, max=MARKET_MAX_PRICE)


async def place_sell_order(conn, seller_id: int, qty: int, price: int) -> int:
    """Выставляет котлеты со склада на продажу. Возвращает id ордера."""
    validate_order(qty, price)
    user = await conn.fetchrow(
        "SELECT inv_cutlets, is_blocked FROM users WHERE user_id = $1 FOR UPDATE", seller_id)
    if not user:
        raise MarketError("common.no_profile")
    if user["inv_cutlets"] < qty:
        raise MarketError("mk.err_no_cutlets", have=user["inv_cutlets"])
    open_orders = await conn.fetchval(
        "SELECT COUNT(*) FROM market_orders WHERE seller_id = $1 AND status = 'open'", seller_id)
    if open_orders >= MARKET_MAX_OPEN_ORDERS:
        raise MarketError("mk.err_too_many", max=MARKET_MAX_OPEN_ORDERS)

    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets - $2 WHERE user_id = $1",
                       seller_id, qty)
    order_id = await conn.fetchval(
        "INSERT INTO market_orders (seller_id, qty, price) VALUES ($1, $2, $3) RETURNING id",
        seller_id, qty, price)
    logger.info("[MARKET] sell order #%s: user=%s qty=%s price=%s", order_id, seller_id, qty, price)
    return order_id


async def cancel_order(conn, seller_id: int, order_id: int) -> int:
    """Снимает свой открытый ордер, котлеты возвращаются на склад. Возвращает qty."""
    order = await conn.fetchrow(
        "SELECT seller_id, qty, status FROM market_orders WHERE id = $1 FOR UPDATE", order_id)
    if not order or order["seller_id"] != seller_id or order["status"] != "open":
        raise MarketError("mk.err_not_found")
    await conn.execute("UPDATE market_orders SET status = 'cancelled' WHERE id = $1", order_id)
    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                       seller_id, order["qty"])
    return order["qty"]


async def buy_from_order(conn, buyer_id: int, order_id: int, qty: int) -> dict:
    """
    Покупка qty котлет из ордера. Возвращает {qty, price, total, fee, seller_id, seller_got}.
    Бросает MarketError.
    """
    if qty <= 0:
        raise MarketError("mk.err_qty", max=MARKET_MAX_QTY)
    order = await conn.fetchrow(
        "SELECT seller_id, qty, price, status FROM market_orders WHERE id = $1 FOR UPDATE", order_id)
    if not order or order["status"] != "open":
        raise MarketError("mk.err_not_found")
    if order["seller_id"] == buyer_id:
        raise MarketError("mk.err_own")
    if qty > order["qty"]:
        qty = order["qty"]          # «купить всё» — берём остаток

    seller_id = order["seller_id"]
    rows = await conn.fetch(
        "SELECT user_id, is_blocked FROM users WHERE user_id = ANY($1::bigint[]) "
        "ORDER BY user_id FOR UPDATE", [buyer_id, seller_id])
    by_id = {r["user_id"]: r for r in rows}
    if buyer_id not in by_id:
        raise MarketError("common.no_profile")

    total = qty * order["price"]
    fee = market_fee(total)
    try:
        await change_balance(conn, buyer_id, -total, "market_buy", str(order_id))
    except InsufficientFunds:
        raise MarketError("mk.err_insufficient", total=total)
    seller_got = total - fee
    if seller_id in by_id and seller_got > 0:
        await change_balance(conn, seller_id, seller_got, "market_sell", str(order_id))
    # Если продавец исчез — его доля тоже сгорает; котлеты покупателю всё равно уходят

    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                       buyer_id, qty)
    remaining = order["qty"] - qty
    await conn.execute(
        "UPDATE market_orders SET qty = $2, status = CASE WHEN $2 = 0 THEN 'done' ELSE 'open' END "
        "WHERE id = $1", order_id, remaining)
    logger.info("[MARKET] buy #%s: buyer=%s qty=%s total=%s fee=%s", order_id, buyer_id, qty, total, fee)
    return {"qty": qty, "price": order["price"], "total": total, "fee": fee,
            "seller_id": seller_id, "seller_got": seller_got}


async def list_open_orders(conn, limit: int = 10, exclude_user: int | None = None) -> list[dict]:
    """Лучшие предложения сверху (дешевле → раньше выставлен)."""
    rows = await conn.fetch(
        """SELECT id, seller_id, qty, price, created_at FROM market_orders
           WHERE status = 'open' AND qty > 0 AND ($2::bigint IS NULL OR seller_id <> $2)
           ORDER BY price ASC, created_at ASC LIMIT $1""", limit, exclude_user)
    return [dict(r) for r in rows]


async def my_open_orders(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch(
        "SELECT id, qty, price, created_at FROM market_orders "
        "WHERE seller_id = $1 AND status = 'open' ORDER BY created_at", user_id)
    return [dict(r) for r in rows]


async def market_stats(conn) -> dict:
    """Для витрины: сколько ордеров и лучшая цена."""
    row = await conn.fetchrow(
        "SELECT COUNT(*) AS orders, COALESCE(SUM(qty), 0) AS cutlets, MIN(price) AS best "
        "FROM market_orders WHERE status = 'open' AND qty > 0")
    return {"orders": int(row["orders"]), "cutlets": int(row["cutlets"]), "best_price": row["best"]}
