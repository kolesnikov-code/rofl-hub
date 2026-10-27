"""
📣 События и 🔨 аукционы в приложении (решение владельца 26.10: каналов нет — все анонсы внутри игры).

GET  /api/news          — лента «События» внизу паспорта: идущие битвы и акции, цели на карте мира,
                          открытые аукционы и итоги ТЕКУЩЕГО СЕЗОНА (с 1-го числа месяца — владелец 27.10: новичок видит, что каждый
                          месяц шансы всех уравниваются), с кнопкой в нужную вкладку.
GET  /api/auctions      — вкладка «Аукционы»: открытые лоты владельца и последние закрытые.
POST /api/auction/bid   — ставка {id, step} (shared/auctions.place_bid; перебитому — личное сообщение).
"""
from __future__ import annotations

import json

from aiohttp import web

from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared.analytics import track
from shared.database import db
from shared.economy import season_bounds, utcnow
from shared.locales import t
from shared.titles import localized_title

EVENTS_LIMIT = 30


def _iso(v):
    return v.isoformat() if v else None


EVENTS_PRIZE_ITEMS = 3        # в ленте — первые 3 награды 1-го места, остальное «… +N» (полный список — во вкладке)


def short_rewards_label(rewards: list[dict], limit: int = EVENTS_PRIZE_ITEMS) -> str:
    """Короткая подпись приза для ленты: длинный список наград не распирает карточку."""
    from shared.prizes import reward_label
    head = " + ".join(reward_label(r) for r in rewards[:limit])
    return head + (f" … +{len(rewards) - limit}" if len(rewards) > limit else "")


def _rewards_label(raw) -> str:
    from shared.battles import prizes_by_place
    prizes = prizes_by_place(raw)
    return short_rewards_label(prizes[min(prizes)]) if prizes else ""


def _winner(results) -> str:
    results = json.loads(results) if isinstance(results, str) else (results or {})
    places = results.get("places") or []
    return str(places[0].get("name") or "") if places else ""


async def handle_news(request: web.Request) -> web.Response:
    from shared.feature_flags import get_flag
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    now = utcnow()
    since = season_bounds(now)[0]     # завершённые — за текущий сезон (календарный месяц UTC)
    items = []
    async with db.pool.acquire() as conn:
        for b in await conn.fetch(
                "SELECT battle_id, title, title_tpl, scope, prizes, starts_at, ends_at, status, results, mine_ids FROM battles "
                "WHERE status = 'active' OR (status = 'finished' AND ends_at >= $1) ORDER BY ends_at DESC LIMIT 20", since):
            live = b["status"] == "active"
            items.append({"kind": "battle", "icon": "⛏" if list(b["mine_ids"] or []) else "⚔️",
                          "title": localized_title(b["title"], b["title_tpl"], ctx.lang),
                          "sub": t(ctx.lang, f"post.scope_{b['scope'] or 'teams'}"), "live": live,
                          "soon": live and b["starts_at"] > now, "at": _iso(b["ends_at"] if live else b["ends_at"]),
                          "prize": _rewards_label(b["prizes"]), "winner": "" if live else _winner(b["results"]),
                          "tab": "mines" if list(b["mine_ids"] or []) else "top"})
        if await get_flag("expeditions"):
            for r in await conn.fetch(
                    "SELECT id, title, title_tpl, icon, scope, prizes, resolve_at, status, results FROM expedition_targets "
                    "WHERE status = 'open' OR (status = 'finished' AND resolve_at >= $1) ORDER BY resolve_at DESC LIMIT 20",
                    since):
                live = r["status"] == "open"
                items.append({"kind": "exp", "icon": r["icon"] or "🗺",
                              "title": localized_title(r["title"], r["title_tpl"], ctx.lang),
                              "sub": t(ctx.lang, f"post.scope_{r['scope']}"), "live": live, "soon": False,
                              "at": _iso(r["resolve_at"]), "prize": _rewards_label(r["prizes"]),
                              "winner": "" if live else _winner(r["results"]), "tab": "map"})
        if await get_flag("auctions"):
            for a in await conn.fetch("SELECT auction_id, item_title, current_price, ends_at FROM auctions "
                                      "WHERE status = 'open' ORDER BY ends_at NULLS LAST LIMIT 10"):
                items.append({"kind": "auction", "icon": "🔨", "title": a["item_title"], "sub": "", "live": True,
                              "soon": False, "at": _iso(a["ends_at"]), "prize": f"{a['current_price']:,} 🪙".replace(",", " "),
                              "winner": "", "tab": "auctions"})
    live = sorted((x for x in items if x["live"]), key=lambda x: x["at"] or "9999")    # скоро финиш — выше
    done = sorted((x for x in items if not x["live"]), key=lambda x: x["at"] or "", reverse=True)
    return web.json_response({"items": (live + done)[:EVENTS_LIMIT]})


async def handle_auctions(request: web.Request) -> web.Response:
    from shared.auctions import list_auctions
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("auctions", ctx.lang)) is not None:
        return off
    async with db.pool.acquire() as conn:
        lots = await list_auctions(conn, ctx.user_id)
        balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
    return web.json_response({"lots": lots, "balance": balance})


async def handle_auction_bid(request: web.Request) -> web.Response:
    from shared.auctions import AuctionError, notify_outbid, place_bid
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("auctions", ctx.lang)) is not None:
        return off
    data = await _json(request)
    auction_id, step = _int(data.get("id")), _int(data.get("step"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await place_bid(conn, ctx.user_id, auction_id, step)
    except AuctionError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "auction_bid", auction_id=auction_id, amount=result["charge"])
    await notify_outbid(request.app.get("bot"), result)
    return web.json_response({"ok": True, "price": result["price"], "charge": result["charge"]})


def register_events_routes(app: web.Application) -> None:
    app.router.add_get("/api/news", handle_news)
    app.router.add_get("/api/auctions", handle_auctions)
    app.router.add_post("/api/auction/bid", handle_auction_bid)
