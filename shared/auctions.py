"""
🔨 Аукционы владельца (VIP ID, свои лоты): общая механика ставок для чата и игрового приложения.

Возвратный аукцион — математика в shared/auction_logic.compute_bid: ставка списывается сразу, перебитому
лидеру взнос возвращается целиком, монеты победителя сгорают при закрытии (дефляция). Закрывает лоты по
ends_at демон админ-бота (close_auction). Каналов нет (26.10): лоты видны во вкладке «Аукционы».
"""
from __future__ import annotations

from shared.auction_logic import compute_bid
from shared.ledger import change_balance
from shared.locales import t

AUCTION_BID_MULTIPLIERS = (1, 5)        # кнопки ставок: +шаг и +5 шагов
AUCTION_LIST_CLOSED = 10                # сколько закрытых лотов показывать под открытыми


class AuctionError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


async def place_bid(conn, user_id: int, auction_id: int, bid_step: int) -> dict:
    """
    Ставка (внутри транзакции вызывающего; лот и игрок блокируются). Возвращает
    {price, charge, previous_bidder_id, refund, title}. Ошибки — AuctionError(ключ локали).
    """
    auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
    if auction is None:
        raise AuctionError("auc.err_none")
    user = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if user is None:
        raise AuctionError("common.no_profile")
    result = compute_bid(current_price=auction["current_price"], min_step=auction["min_step"], bid_step=bid_step,
                         bidder_id=user_id, bidder_balance=user["balance"],
                         highest_bidder_id=auction["highest_bidder_id"], status=auction["status"])
    if not result.ok:
        if result.reason == "closed":
            raise AuctionError("auc.err_closed")
        if result.reason == "insufficient_funds":
            raise AuctionError("auc.err_funds", need=result.bidder_charge, have=user["balance"])
        raise AuctionError("auc.err_step", step=auction["min_step"])
    await change_balance(conn, user_id, -result.bidder_charge, "auction_bid", str(auction_id))
    if result.refund_to_previous and result.previous_bidder_id:
        await change_balance(conn, result.previous_bidder_id, result.refund_to_previous, "auction_refund", str(auction_id))
    await conn.execute("UPDATE auctions SET current_price = $1, highest_bidder_id = $2, previous_bidder_id = $3 "
                       "WHERE auction_id = $4", result.new_price, user_id, result.previous_bidder_id, auction_id)
    return {"price": result.new_price, "charge": result.bidder_charge, "previous_bidder_id": result.previous_bidder_id,
            "refund": result.refund_to_previous, "title": auction["item_title"]}


async def notify_outbid(bot, result: dict) -> None:
    """Перебитому лидеру — личное сообщение на его языке (взнос уже вернулся). Сбой не важен."""
    prev = result.get("previous_bidder_id")
    if not prev or bot is None:
        return
    import html

    from shared.database import db
    try:
        async with db.pool.acquire() as conn:
            lang = await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", prev) or "en"
        await bot.send_message(prev, t(lang, "auc.outbid", title=html.escape(result["title"]), refund=result["refund"],
                                       price=result["price"]), parse_mode="HTML")
    except Exception:
        pass


async def list_auctions(conn, user_id: int) -> list[dict]:
    """Открытые лоты (скорее заканчивающиеся сверху) и последние закрытые. Лидер — по имени, без ID."""
    rows = await conn.fetch(
        f"""(SELECT a.*, u.display_name, u.username FROM auctions a LEFT JOIN users u ON u.user_id = a.highest_bidder_id
             WHERE a.status = 'open' ORDER BY a.ends_at NULLS LAST, a.auction_id)
            UNION ALL
            (SELECT a.*, u.display_name, u.username FROM auctions a LEFT JOIN users u ON u.user_id = a.highest_bidder_id
             WHERE a.status <> 'open' ORDER BY a.auction_id DESC LIMIT {AUCTION_LIST_CLOSED})""")
    out = []
    for r in rows:
        leader = None
        if r["highest_bidder_id"]:
            leader = r["display_name"] or (r["username"] and "@" + r["username"]) or "—"
        out.append({"id": r["auction_id"], "title": r["item_title"], "descr": r["item_desc"] or "",
                    "vip": r["vip_alias"], "price": r["current_price"], "step": r["min_step"], "status": r["status"],
                    "ends_at": r["ends_at"].isoformat() if r["ends_at"] else None, "leader": leader,
                    "mine": r["highest_bidder_id"] == user_id,
                    "bids": [r["min_step"] * m for m in AUCTION_BID_MULTIPLIERS]})
    return out
