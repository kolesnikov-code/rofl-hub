"""
🧍 Вкладка «Персонаж» (решение владельца 30.10): аватар М/Ж, 5 слотов, сумка деталей костюмов, прокачка до 2-го
уровня, сплав нано-экзо-брони и рынок деталей. Механика — shared/gear.py; торговля деталями идёт через общую биржу
(/api/market/order|fill|cancel, товар g_<костюм>_<слот>, пол цены GEAR_MIN_PRICE, комиссия сгорает).

GET  /api/gear            — всё для вкладки (надето, сумка, бонусы, цены прокачки, экзо, лимит сезона, лоты деталей)
POST /api/gear/gender     — {"gender": "m"|"f"}
POST /api/gear/equip      — {"suit", "slot", "level"}
POST /api/gear/unequip    — {"slot"}
POST /api/gear/upgrade    — {"suit", "slot"}
POST /api/gear/exo        — сплав нано-экзо-брони
POST /api/gear/art        — {"kind", "slot"?} артефакт из сумки на пояс (снять — /api/gear/unequip со слотом a1…a3)
GET  /api/gifts           — 🎁 подарки от разработчика на плашке паспорта (shared/gifts.py)
POST /api/gifts/claim     — {"id"} забрать подарок
"""
from __future__ import annotations

from aiohttp import web

from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared import gear
from shared.database import db
from shared.economy import (
    ARTIFACT_BONUS, ARTIFACT_MIN_PRICE, ARTIFACT_SEASON_CAP, ARTIFACT_SLOTS, art_kind, art_of, parse_art_asset,
    user_bonus,
    GEAR_EXO, GEAR_EXO_COINS, GEAR_EXO_COST, GEAR_MARKET_MAX_QTY, GEAR_MIN_PRICE, GEAR_SEASON_CAP, GEAR_SLOTS,
    GEAR_SUITS, GEAR_UPGRADE_COINS, GEAR_UPGRADE_COST, MARKET_FEE_PERCENT, MARKET_MAX_PRICE, SUIT_BONUS,
    parse_gear_asset, utcnow,
)
from shared.locales import t

GEAR_MARKET_LIST = 100     # лучших лотов деталей во вкладке


async def _guard(request: web.Request):
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("gear", ctx.lang)) is not None:
        return off
    return ctx


def _lots(rows) -> list[dict]:
    out = []
    for r in rows:
        suit_slot = parse_gear_asset(r["asset"])
        kind = parse_art_asset(r["asset"])
        if suit_slot:
            out.append({"id": r["id"], "suit": suit_slot[0], "slot": suit_slot[1], "qty": r["qty"], "price": r["price"]})
        elif kind:
            out.append({"id": r["id"], "art": kind, "qty": r["qty"], "price": r["price"]})
    return out


async def gear_state(conn, user_id: int) -> dict:
    user = await conn.fetchrow("SELECT gender, suit, suit_level, art_bonus, balance FROM users WHERE user_id = $1", user_id)
    worn = await gear.equipped(conn, user_id)
    belt = {s: art_kind(worn.pop(s)["suit"]) for s in ARTIFACT_SLOTS if s in worn}
    items = await gear.bag(conn, user_id)
    now = utcnow()
    asks = await conn.fetch(
        "SELECT id, asset, qty, price FROM market_orders WHERE status = 'open' AND side = 'sell' AND qty > 0 "
        "AND (asset LIKE 'g\\_%' OR asset LIKE 'a\\_%') AND team_id IS NULL AND seller_id <> $1 "
        "ORDER BY price, created_at LIMIT $2",
        user_id, GEAR_MARKET_LIST)
    mine = await conn.fetch(
        "SELECT id, asset, qty, price FROM market_orders WHERE status = 'open' AND side = 'sell' AND qty > 0 "
        "AND (asset LIKE 'g\\_%' OR asset LIKE 'a\\_%') AND seller_id = $1 ORDER BY created_at", user_id)
    suit, level = user["suit"], user["suit_level"] or 0
    return {
        "ok": True, "gender": user["gender"], "balance": user["balance"],
        "suits": list(GEAR_SUITS), "slots": list(GEAR_SLOTS), "exo_key": GEAR_EXO,
        "worn": worn, "bag": [b for b in items if b["slot"] != "art"],
        "arts": [{"kind": art_kind(b["suit"]), "qty": b["qty"]} for b in items if b["slot"] == "art"],
        "belt": belt, "belt_slots": list(ARTIFACT_SLOTS), "art_bonus": ARTIFACT_BONUS,
        "active": {"suit": suit, "level": level,
                   # итог по линиям: костюм + артефакты пояса
                   "effects": {line: user_bonus(user, line) for line in GEAR_SUITS if user_bonus(user, line)},
                   "belt": art_of(user)},
        "bonus": SUIT_BONUS,
        "upgrade": {s: {"cost": GEAR_UPGRADE_COST[s], "coins": GEAR_UPGRADE_COINS} for s in GEAR_SUITS},
        "exo": {**await gear.exo_ready(conn, user_id), "cost": GEAR_EXO_COST, "coins": GEAR_EXO_COINS},
        "season": {"got": await gear.season_drops(conn, user_id, now), "cap": GEAR_SEASON_CAP,
                   "arts": await gear.season_drops(conn, user_id, now, artifacts=True), "arts_cap": ARTIFACT_SEASON_CAP},
        "market": {"asks": _lots(asks), "mine": _lots(mine), "min_price": GEAR_MIN_PRICE, "art_min_price": ARTIFACT_MIN_PRICE,
                   "max_price": MARKET_MAX_PRICE,
                   "max_qty": GEAR_MARKET_MAX_QTY, "fee": MARKET_FEE_PERCENT},
    }


async def handle_gear(request: web.Request) -> web.Response:
    ctx = await _guard(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        return web.json_response(await gear_state(conn, ctx.user_id))


async def _act(request: web.Request, action) -> web.Response:
    ctx = await _guard(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await action(conn, ctx.user_id, data)
            return web.json_response(await gear_state(conn, ctx.user_id))
    except gear.GearError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))


async def handle_gender(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.set_gender(conn, uid, str(d.get("gender") or "")))


async def handle_equip(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.equip(
        conn, uid, str(d.get("suit") or ""), str(d.get("slot") or ""), max(1, _int(d.get("level"), 1)), utcnow()))


async def handle_unequip(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.unequip(conn, uid, str(d.get("slot") or ""), utcnow()))


async def handle_upgrade(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.upgrade(
        conn, uid, str(d.get("suit") or ""), str(d.get("slot") or ""), utcnow()))


async def handle_exo(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.merge_exo(conn, uid, utcnow()))


async def handle_art(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.equip_artifact(
        conn, uid, str(d.get("kind") or ""), (str(d["slot"]) if d.get("slot") else None), utcnow()))


# ---------------------------------------------------------------- 🎁 подарки от разработчика
def _gift_json(g: dict) -> dict:
    return {"id": g["id"], "title": g["title"], "rewards": g["rewards"], "expires_at": g["expires_at"].isoformat()}


async def handle_gifts(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    from shared.gifts import pending
    async with db.pool.acquire() as conn:
        return web.json_response({"ok": True, "gifts": [_gift_json(g) for g in await pending(conn, ctx.user_id, utcnow())]})


async def handle_gift_claim(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    from shared.gifts import GiftError, claim, pending
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                got = await claim(conn, ctx.user_id, _int(data.get("id")), utcnow())
            left = [_gift_json(g) for g in await pending(conn, ctx.user_id, utcnow())]
    except GiftError as e:
        return fail(t(ctx.lang, e.key))
    return web.json_response({"ok": True, "got": got, "gifts": left})


def register_gear_routes(app: web.Application) -> None:
    app.router.add_get("/api/gear", handle_gear)
    app.router.add_post("/api/gear/gender", handle_gender)
    app.router.add_post("/api/gear/equip", handle_equip)
    app.router.add_post("/api/gear/unequip", handle_unequip)
    app.router.add_post("/api/gear/upgrade", handle_upgrade)
    app.router.add_post("/api/gear/exo", handle_exo)
    app.router.add_post("/api/gear/art", handle_art)
    app.router.add_get("/api/gifts", handle_gifts)
    app.router.add_post("/api/gifts/claim", handle_gift_claim)
