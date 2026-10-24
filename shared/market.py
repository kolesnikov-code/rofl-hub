"""
Биржа экосистемы (v2, решение владельца 24.10): котлеты и ресурсы за монеты + обмен ресурсов.

Ядро без Telegram — только asyncpg-соединение внутри транзакции вызывающего кода.

Товары (MARKET_ASSETS): cutlet (кибер-котлета со СКЛАДА, inv_cutlets) и 4 ресурса.
Стороны ордера:
- sell — «продаю»: товар уходит в эскроу ордера сразу (отмена возвращает);
- buy  — «куплю»: монеты qty×price уходят в эскроу сразу (ledger market_bid; отмена — market_bid_refund).
Сделка (fill_order): покупатель получает товар, продавец — сумму минус комиссия.
КОМИССИЯ ПЛАТИТ ПРОДАВЕЦ и она СГОРАЕТ (дефляция). Льгота 5% — только если Шаттл у самого
продавца: чужим Шаттлом не воспользоваться.
ПОЛ ЦЕНЫ КОТЛЕТЫ (MARKET_CUTLET_MIN_PRICE, обоснование — economy.py и docs/ECONOMY_AUDIT.md):
топливо из магазина за Звёзды всегда выгоднее биржи. Пол действует для обеих сторон.
Каждая сделка пишется в market_trades — из неё строятся график цены и индекс биржи.

Обмен ресурс ↔ ресурс (resource_swaps): «отдам X металла за Y водорода», ресурс мейкера
в эскроу, принимающий отдаёт свой и забирает чужой целиком. Без комиссии и без монет.

БИРЖА КОМАНДЫ (26.10): ордер или обмен с team_id видят и принимают только участники этой
команды; комиссия — team_market_fee_percent (5%, Мега-Клан 2%). Ушедший из команды снимает свои
командные лоты (leave_team), так что продавец всегда тиммейт покупателя.

Строки users блокируются FOR UPDATE в порядке возрастания user_id (анти-дедлок).
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from shared.economy import (
    MARKET_ASSETS,
    MARKET_HISTORY_DAYS,
    MARKET_MAX_PRICE,
    RESOURCE_KINDS,
    SWAP_MAX_OPEN,
    SWAP_MAX_QTY,
    market_fee,
    market_limits,
    market_min_price,
    team_market_fee_percent,
)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t
from shared.resources import InsufficientResources, change_resource, free_space, lock_resources

logger = logging.getLogger(__name__)

SIDES = ("sell", "buy")


class MarketError(Exception):
    """Причина отказа: ключ локали + параметры (локализуется в обработчике)."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(t("ru", key, **kwargs))

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


# ============================================================================
# Проверки
# ============================================================================
def validate_order(qty: int, price: int, shuttle: bool = False, asset: str = "cutlet") -> None:
    if asset not in MARKET_ASSETS:
        raise MarketError("mk.err_asset")
    max_qty, _ = market_limits(shuttle, asset)
    if qty <= 0 or qty > max_qty:
        raise MarketError("mk.err_qty", max=max_qty)
    min_price = market_min_price(asset)
    if price < min_price or price > MARKET_MAX_PRICE:
        raise MarketError("mk.err_price", min=min_price, max=MARKET_MAX_PRICE)


async def _team_scope(conn, user_id: int, team_only: bool) -> int | None:
    """team_id для командного лота (игрок обязан быть в команде) или None для общей биржи."""
    if not team_only:
        return None
    team_id = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
    if team_id is None:
        raise MarketError("mk.err_no_team")
    return team_id


async def _check_team_access(conn, user_id: int, team_id: int | None) -> int | None:
    """Командный лот — только для участников этой команды. Возвращает ставку комиссии команды."""
    if team_id is None:
        return None
    row = await conn.fetchrow(
        "SELECT u.team_id, t.max_members FROM users u LEFT JOIN teams t ON t.team_id = u.team_id "
        "WHERE u.user_id = $1", user_id)
    if not row or row["team_id"] != team_id:
        raise MarketError("mk.err_team_only")
    return team_market_fee_percent(row["max_members"] or 0)


async def _lock_users(conn, ids: list[int]) -> dict:
    rows = await conn.fetch(
        "SELECT user_id, inv_cutlets, has_shuttle, is_blocked, market_free_sales FROM users "
        "WHERE user_id = ANY($1::bigint[]) ORDER BY user_id FOR UPDATE", sorted(set(ids)))
    return {r["user_id"]: r for r in rows}


async def _take_asset(conn, user_id: int, asset: str, qty: int, reason: str, ref: str) -> None:
    """Списывает товар у игрока (в эскроу ордера или продавцу-тейкеру). MarketError при нехватке."""
    if asset == "cutlet":
        left = await conn.fetchval(
            "UPDATE users SET inv_cutlets = inv_cutlets - $2 WHERE user_id = $1 AND inv_cutlets >= $2 "
            "RETURNING inv_cutlets", user_id, qty)
        if left is None:
            have = await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = $1", user_id) or 0
            raise MarketError("mk.err_no_cutlets", have=have)
        return
    try:
        await change_resource(conn, user_id, asset, -qty, reason, ref)
    except InsufficientResources as e:
        raise MarketError("mk.err_no_resource", have=e.have) from e


async def _ensure_room(conn, user_id: int, asset: str, qty: int, key: str = "mk.err_storage_full") -> None:
    """Ресурс купят/получат только если он влезет на склад (котлеты склад не ограничивает)."""
    if asset == "cutlet":
        return
    room = await free_space(conn, user_id, asset)
    if room < qty:
        raise MarketError(key, free=room)


async def _give_asset(conn, user_id: int, asset: str, qty: int, reason: str, ref: str) -> None:
    if asset == "cutlet":
        await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1", user_id, qty)
    else:
        await change_resource(conn, user_id, asset, qty, reason, ref)


# ============================================================================
# Ордера
# ============================================================================
async def place_order(conn, user_id: int, asset: str, side: str, qty: int, price: int,
                      team_only: bool = False) -> int:
    """
    Выставляет ордер (продажа — товар в эскроу, покупка — монеты в эскроу). Возвращает id.
    team_only — лот на бирже команды: видят и принимают только тиммейты.
    """
    if side not in SIDES:
        raise MarketError("mk.err_asset")
    users = await _lock_users(conn, [user_id])
    user = users.get(user_id)
    if not user:
        raise MarketError("common.no_profile")
    team_id = await _team_scope(conn, user_id, team_only)
    validate_order(qty, price, shuttle=bool(user["has_shuttle"]), asset=asset)
    _, max_orders = market_limits(bool(user["has_shuttle"]), asset)
    open_orders = await conn.fetchval(
        "SELECT COUNT(*) FROM market_orders WHERE seller_id = $1 AND status = 'open'", user_id)
    if open_orders >= max_orders:
        raise MarketError("mk.err_too_many", max=max_orders)
    # Проверяем запас ДО создания ордера: отказ не оставляет следов даже вне транзакции
    if side == "sell":
        have = user["inv_cutlets"] if asset == "cutlet" else (await lock_resources(conn, user_id))[asset]
        if have < qty:
            raise MarketError("mk.err_no_cutlets" if asset == "cutlet" else "mk.err_no_resource", have=have)
    else:
        balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", user_id)
        if balance < qty * price:
            raise MarketError("mk.err_insufficient", total=qty * price)
        await _ensure_room(conn, user_id, asset, qty)

    order_id = await conn.fetchval(
        "INSERT INTO market_orders (seller_id, qty, price, asset, side, team_id) "
        "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
        user_id, qty, price, asset, side, team_id)
    if side == "sell":
        await _take_asset(conn, user_id, asset, qty, "market_escrow", str(order_id))
    else:
        try:
            await change_balance(conn, user_id, -qty * price, "market_bid", str(order_id))
        except InsufficientFunds:
            raise MarketError("mk.err_insufficient", total=qty * price)
    logger.info("[MARKET] order #%s %s %s: user=%s qty=%s price=%s", order_id, side, asset, user_id, qty, price)
    return order_id


async def place_sell_order(conn, seller_id: int, qty: int, price: int) -> int:
    """Совместимость с чатом /sell: продажа котлет."""
    return await place_order(conn, seller_id, "cutlet", "sell", qty, price)


async def cancel_order(conn, user_id: int, order_id: int) -> int:
    """Снимает свой открытый ордер, эскроу возвращается. Возвращает qty."""
    order = await conn.fetchrow(
        "SELECT seller_id, qty, price, status, asset, side FROM market_orders WHERE id = $1 FOR UPDATE", order_id)
    if not order or order["seller_id"] != user_id or order["status"] != "open":
        raise MarketError("mk.err_not_found")
    await conn.execute("UPDATE market_orders SET status = 'cancelled' WHERE id = $1", order_id)
    if order["side"] == "sell":
        await _give_asset(conn, user_id, order["asset"], order["qty"], "market_refund", str(order_id))
    elif order["qty"] > 0:
        await change_balance(conn, user_id, order["qty"] * order["price"], "market_bid_refund", str(order_id))
    return order["qty"]


async def fill_order(conn, taker_id: int, order_id: int, qty: int) -> dict:
    """
    Сделка по чужому ордеру: по ордеру-продаже тейкер покупает, по ордеру-покупке — продаёт.
    Возвращает {qty, price, total, fee, asset, side, buyer_id, seller_id, maker_id, seller_got, shuttle}.
    """
    if qty <= 0:
        raise MarketError("mk.err_qty", max=market_limits(False)[0])
    order = await conn.fetchrow(
        "SELECT seller_id, qty, price, status, asset, side, team_id FROM market_orders WHERE id = $1 FOR UPDATE",
        order_id)
    if not order or order["status"] != "open" or order["qty"] <= 0:
        raise MarketError("mk.err_not_found")
    maker_id = order["seller_id"]
    if maker_id == taker_id:
        raise MarketError("mk.err_own")
    team_percent = await _check_team_access(conn, taker_id, order["team_id"])
    qty = min(qty, order["qty"])          # «всё» — берём остаток
    asset, price = order["asset"], order["price"]
    users = await _lock_users(conn, [taker_id, maker_id])
    if taker_id not in users:
        raise MarketError("common.no_profile")

    total = qty * price
    await _ensure_room(conn, taker_id if order["side"] == "sell" else maker_id, asset, qty,
                       "mk.err_storage_full" if order["side"] == "sell" else "mk.err_buyer_full")
    if order["side"] == "sell":
        buyer_id, seller_id = taker_id, maker_id
        try:
            await change_balance(conn, buyer_id, -total, "market_buy", str(order_id))
        except InsufficientFunds:
            raise MarketError("mk.err_insufficient", total=total)
    else:
        buyer_id, seller_id = maker_id, taker_id   # монеты покупателя уже в эскроу ордера
        await _take_asset(conn, seller_id, asset, qty, "market_sell", str(order_id))

    seller = users.get(seller_id)
    shuttle = bool(seller and seller["has_shuttle"])   # льгота — только Шаттл самого продавца
    stamp = bool(seller and seller["market_free_sales"] > 0)   # 📜 Штамп биржи продавца: без комиссии
    fee = 0 if stamp else market_fee(total, shuttle=shuttle, team_percent=team_percent)
    if stamp:
        await conn.execute("UPDATE users SET market_free_sales = market_free_sales - 1 WHERE user_id = $1",
                           seller_id)
    seller_got = total - fee
    if seller is not None and seller_got > 0:
        await change_balance(conn, seller_id, seller_got, "market_sell", str(order_id))
    # Если продавец исчез — его доля сгорает; товар покупатель получает в любом случае
    await _give_asset(conn, buyer_id, asset, qty, "market_buy", str(order_id))

    remaining = order["qty"] - qty
    await conn.execute(
        "UPDATE market_orders SET qty = $2, status = CASE WHEN $2 = 0 THEN 'done' ELSE 'open' END "
        "WHERE id = $1", order_id, remaining)
    await conn.execute(
        "INSERT INTO market_trades (asset, qty, price, buyer_id, seller_id, order_id) VALUES ($1, $2, $3, $4, $5, $6)",
        asset, qty, price, buyer_id, seller_id, order_id)
    logger.info("[MARKET] fill #%s %s %s: buyer=%s seller=%s qty=%s total=%s fee=%s",
                order_id, order["side"], asset, buyer_id, seller_id, qty, total, fee)
    return {"qty": qty, "price": price, "total": total, "fee": fee, "asset": asset, "side": order["side"],
            "buyer_id": buyer_id, "seller_id": seller_id, "maker_id": maker_id,
            "seller_got": seller_got, "shuttle": shuttle, "team": order["team_id"] is not None, "stamp": stamp}


async def buy_from_order(conn, buyer_id: int, order_id: int, qty: int) -> dict:
    """Совместимость с чатом /market: покупка по ордеру-продаже."""
    return await fill_order(conn, buyer_id, order_id, qty)


async def list_open_orders(conn, limit: int = 10, exclude_user: int | None = None,
                           asset: str = "cutlet", side: str = "sell", team_id: int | None = None) -> list[dict]:
    """
    Стакан: продажи — дешевле сверху, покупки — дороже сверху; при равной цене — кто раньше.
    team_id=None — общая биржа (командные лоты не видны), иначе — биржа этой команды.
    """
    order_by = "price ASC" if side == "sell" else "price DESC"
    rows = await conn.fetch(
        f"""SELECT id, seller_id, qty, price, asset, side, created_at FROM market_orders
           WHERE status = 'open' AND qty > 0 AND asset = $3 AND side = $4
             AND ($2::bigint IS NULL OR seller_id <> $2)
             AND team_id IS NOT DISTINCT FROM $5::int
           ORDER BY {order_by}, created_at ASC LIMIT $1""", limit, exclude_user, asset, side, team_id)
    return [dict(r) for r in rows]


async def my_open_orders(conn, user_id: int, asset: str | None = None) -> list[dict]:
    rows = await conn.fetch(
        "SELECT id, qty, price, asset, side, created_at, team_id IS NOT NULL AS team FROM market_orders "
        "WHERE seller_id = $1 AND status = 'open' AND ($2::text IS NULL OR asset = $2) ORDER BY created_at",
        user_id, asset)
    return [dict(r) for r in rows]


async def market_stats(conn, asset: str = "cutlet") -> dict:
    """Для витрины: сколько продаж, сколько товара, лучшая цена продажи и лучшая заявка на покупку."""
    row = await conn.fetchrow(
        """SELECT COUNT(*) FILTER (WHERE side = 'sell') AS orders,
                  COALESCE(SUM(qty) FILTER (WHERE side = 'sell'), 0) AS qty,
                  MIN(price) FILTER (WHERE side = 'sell') AS best,
                  COUNT(*) FILTER (WHERE side = 'buy') AS bids,
                  MAX(price) FILTER (WHERE side = 'buy') AS best_bid
           FROM market_orders WHERE status = 'open' AND qty > 0 AND asset = $1 AND team_id IS NULL""", asset)
    return {"orders": int(row["orders"]), "cutlets": int(row["qty"]), "qty": int(row["qty"]),
            "best_price": row["best"], "bids": int(row["bids"]), "best_bid": row["best_bid"]}


# ============================================================================
# История цены и индекс биржи
# ============================================================================
async def price_history(conn, asset: str, now: datetime, days: int = MARKET_HISTORY_DAYS) -> list[dict]:
    """Средняя цена и объём по дням (UTC) за последние days дней; дни без сделок — avg=None."""
    start = (now - timedelta(days=days - 1)).date()
    rows = await conn.fetch(
        """SELECT (created_at AT TIME ZONE 'UTC')::date AS day,
                  SUM(qty * price)::float / NULLIF(SUM(qty), 0) AS avg, SUM(qty) AS volume
           FROM market_trades WHERE asset = $1 AND created_at >= $2
           GROUP BY 1 ORDER BY 1""", asset, datetime(start.year, start.month, start.day, tzinfo=now.tzinfo))
    by_day = {r["day"]: r for r in rows}
    out = []
    for i in range(days):
        day = start + timedelta(days=i)
        r = by_day.get(day)
        out.append({"day": day.isoformat(), "avg": round(r["avg"], 1) if r and r["avg"] is not None else None,
                    "volume": int(r["volume"]) if r else 0})
    return out


def index_change(history: list[dict]) -> dict:
    """Индекс товара: последняя средняя цена и изменение к средней за неделю (в процентах)."""
    prices = [d["avg"] for d in history if d["avg"] is not None]
    if not prices:
        return {"last": None, "week_avg": None, "change_pct": None, "volume": 0}
    week_avg = sum(prices) / len(prices)
    last = prices[-1]
    change = round((last - week_avg) / week_avg * 100, 1) if week_avg else None
    return {"last": last, "week_avg": round(week_avg, 1), "change_pct": change,
            "volume": sum(d["volume"] for d in history)}


# ============================================================================
# Обмен ресурс ↔ ресурс
# ============================================================================
def validate_swap(give_kind: str, give_qty: int, want_kind: str, want_qty: int) -> None:
    if give_kind not in RESOURCE_KINDS or want_kind not in RESOURCE_KINDS:
        raise MarketError("mk.err_asset")
    if give_kind == want_kind:
        raise MarketError("sw.err_same")
    if not (0 < give_qty <= SWAP_MAX_QTY and 0 < want_qty <= SWAP_MAX_QTY):
        raise MarketError("sw.err_qty", max=SWAP_MAX_QTY)


async def create_swap(conn, maker_id: int, give_kind: str, give_qty: int, want_kind: str, want_qty: int,
                      team_only: bool = False) -> int:
    validate_swap(give_kind, give_qty, want_kind, want_qty)
    await _lock_users(conn, [maker_id])
    team_id = await _team_scope(conn, maker_id, team_only)
    open_swaps = await conn.fetchval(
        "SELECT COUNT(*) FROM resource_swaps WHERE maker_id = $1 AND status = 'open'", maker_id)
    if open_swaps >= SWAP_MAX_OPEN:
        raise MarketError("mk.err_too_many", max=SWAP_MAX_OPEN)
    swap_id = await conn.fetchval(
        "INSERT INTO resource_swaps (maker_id, give_kind, give_qty, want_kind, want_qty, team_id) "
        "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id", maker_id, give_kind, give_qty, want_kind, want_qty, team_id)
    await _take_asset(conn, maker_id, give_kind, give_qty, "swap_escrow", str(swap_id))
    return swap_id


async def accept_swap(conn, taker_id: int, swap_id: int) -> dict:
    swap = await conn.fetchrow("SELECT * FROM resource_swaps WHERE id = $1 FOR UPDATE", swap_id)
    if not swap or swap["status"] != "open":
        raise MarketError("mk.err_not_found")
    if swap["maker_id"] == taker_id:
        raise MarketError("mk.err_own")
    await _check_team_access(conn, taker_id, swap["team_id"])
    await _lock_users(conn, [taker_id, swap["maker_id"]])
    await _ensure_room(conn, taker_id, swap["give_kind"], swap["give_qty"])
    await _ensure_room(conn, swap["maker_id"], swap["want_kind"], swap["want_qty"], "mk.err_buyer_full")
    first, second = sorted((taker_id, swap["maker_id"]))
    await lock_resources(conn, first)
    await lock_resources(conn, second)
    await _take_asset(conn, taker_id, swap["want_kind"], swap["want_qty"], "swap_give", str(swap_id))
    await _give_asset(conn, swap["maker_id"], swap["want_kind"], swap["want_qty"], "swap_get", str(swap_id))
    await _give_asset(conn, taker_id, swap["give_kind"], swap["give_qty"], "swap_get", str(swap_id))
    await conn.execute("UPDATE resource_swaps SET status = 'done', taker_id = $2 WHERE id = $1", swap_id, taker_id)
    return dict(swap)


async def cancel_swap(conn, user_id: int, swap_id: int) -> None:
    swap = await conn.fetchrow("SELECT * FROM resource_swaps WHERE id = $1 FOR UPDATE", swap_id)
    if not swap or swap["maker_id"] != user_id or swap["status"] != "open":
        raise MarketError("mk.err_not_found")
    await conn.execute("UPDATE resource_swaps SET status = 'cancelled' WHERE id = $1", swap_id)
    await _give_asset(conn, user_id, swap["give_kind"], swap["give_qty"], "swap_refund", str(swap_id))


async def list_swaps(conn, limit: int = 20, exclude_user: int | None = None,
                     team_id: int | None = None) -> list[dict]:
    rows = await conn.fetch(
        "SELECT id, maker_id, give_kind, give_qty, want_kind, want_qty FROM resource_swaps "
        "WHERE status = 'open' AND ($2::bigint IS NULL OR maker_id <> $2) "
        "AND team_id IS NOT DISTINCT FROM $3::int ORDER BY created_at DESC LIMIT $1",
        limit, exclude_user, team_id)
    return [dict(r) for r in rows]


async def my_swaps(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch(
        "SELECT id, give_kind, give_qty, want_kind, want_qty, team_id IS NOT NULL AS team FROM resource_swaps "
        "WHERE maker_id = $1 AND status = 'open' ORDER BY created_at", user_id)
    return [dict(r) for r in rows]


async def close_team_lots(conn, user_id: int) -> None:
    """Игрок ушёл из команды — его командные ордера и обмены снимаются, эскроу возвращается."""
    for r in await conn.fetch(
            "SELECT id FROM market_orders WHERE seller_id = $1 AND status = 'open' AND team_id IS NOT NULL", user_id):
        await cancel_order(conn, user_id, r["id"])
    for r in await conn.fetch(
            "SELECT id FROM resource_swaps WHERE maker_id = $1 AND status = 'open' AND team_id IS NOT NULL", user_id):
        await cancel_swap(conn, user_id, r["id"])
