"""
🧍 Вкладка «Персонаж» (решение владельца 30.10): аватар М/Ж, 5 слотов, сумка деталей костюмов, прокачка по трём
уровням (Базовый → Улучшенный → Легендарный, 31.10), сплав нано-экзо-брони и рынок деталей. Механика — shared/gear.py; торговля деталями идёт через общую биржу
(/api/market/order|fill|cancel, товар g_<костюм>_<слот>, пол цены GEAR_MIN_PRICE, комиссия сгорает).

GET  /api/gear            — всё для вкладки (надето, сумка, бонусы, цены прокачки, экзо, лимит сезона, лоты деталей)
POST /api/gear/gender     — {"gender": "m"|"f"}
POST /api/gear/equip      — {"suit", "slot", "level"}
POST /api/gear/unequip    — {"slot"}
POST /api/gear/upgrade    — {"suit", "slot", "level"} (level — текущий уровень детали)
POST /api/gear/exo        — сплав нано-экзо-брони
POST /api/gear/art        — {"kind", "slot"?} артефакт из сумки на пояс (снять — /api/gear/unequip со слотом a1…a3)
GET  /api/gifts           — 🎁 подарки от разработчика на плашке паспорта (shared/gifts.py)
POST /api/gifts/claim     — {"id"} забрать подарок
GET  /api/skins           — ✨ Гараж: свои скины (номер тиража, закалка, история), витрина за ★ с остатком тиража,
                            коллекции сезона, рынок скинов, зал славы
POST /api/skins/equip|unequip — {"id"} экземпляра; /api/skins/absorb — {"id", "fodder"} закалка
GET  /api/pass            — 🎟 пропуск сезона: уровень, опыт, обе дорожки наград, что продаётся
POST /api/pass/claim      — забрать все открытые награды
GET  /api/gear/history    — 🏆 трофейная история деталей костюма
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
    GEAR_LEVEL_KEYS, GEAR_MAX_LEVEL, GEAR_SUITS, MARKET_FEE_PERCENT, MARKET_MAX_PRICE, SUIT_BONUS,
    parse_gear_asset, utcnow,
)
from shared.locales import t
from shared.tech import tech_levels

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
    from shared.trophies import gear_history
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
        # прокачка: что нужно для каждого следующего уровня; опыт детали — сумма её трофейной истории (history)
        "max_level": GEAR_MAX_LEVEL, "level_keys": GEAR_LEVEL_KEYS,
        "upgrade": {s: {lv: gear.upgrade_need(s, lv) for lv in range(2, GEAR_MAX_LEVEL + 1)} for s in GEAR_SUITS},
        "tech": await tech_levels(conn, user_id),
        "exo": {**await gear.exo_ready(conn, user_id), "cost": GEAR_EXO_COST, "coins": GEAR_EXO_COINS},
        "season": {"got": await gear.season_drops(conn, user_id, now), "cap": GEAR_SEASON_CAP,
                   "arts": await gear.season_drops(conn, user_id, now, artifacts=True), "arts_cap": ARTIFACT_SEASON_CAP},
        "market": {"asks": _lots(asks), "mine": _lots(mine), "min_price": GEAR_MIN_PRICE, "art_min_price": ARTIFACT_MIN_PRICE,
                   "max_price": MARKET_MAX_PRICE,
                   "max_qty": GEAR_MARKET_MAX_QTY, "fee": MARKET_FEE_PERCENT},
        "history": await gear_history(conn, user_id),   # 🏆 что пережила каждая деталь
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


async def handle_ref_suit(request: web.Request) -> web.Response:
    """🤝 Полный костюм на выбор за активных друзей (вкладка «Друзья»)."""
    return await _act(request, lambda conn, uid, d: gear.claim_referral_suit(conn, uid, str(d.get("suit") or "")))


async def handle_gender(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.set_gender(conn, uid, str(d.get("gender") or "")))


async def handle_equip(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.equip(
        conn, uid, str(d.get("suit") or ""), str(d.get("slot") or ""), max(1, _int(d.get("level"), 1)), utcnow()))


async def handle_unequip(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.unequip(conn, uid, str(d.get("slot") or ""), utcnow()))


async def handle_upgrade(request: web.Request) -> web.Response:
    return await _act(request, lambda conn, uid, d: gear.upgrade(
        conn, uid, str(d.get("suit") or ""), str(d.get("slot") or ""), utcnow(),
        _int(d.get("level"), 0) or None))


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


# ---------------------------------------------------------------- ✨ Гараж: скины
async def skins_state(conn, user_id: int, lang: str) -> dict:
    from shared import skins as sk
    now = utcnow()
    mine = await sk.owned(conn, user_id)
    counts = {r["skin_id"]: r["n"] for r in await conn.fetch(
        "SELECT skin_id, COUNT(*) AS n FROM user_skins GROUP BY skin_id")}
    shop = [{"id": sid, "sku": sk.skin_sku(sid), "stars": s["stars"], "edition": s.get("edition"),
             "left": (s["edition"] - counts.get(sid, 0)) if s.get("edition") else None,
             "until": s["until"].isoformat() if s.get("until") else None}
            for sid, s in sk.SKINS.items() if sk.for_sale(sid, now)]
    sets = {}
    have_ids = {m["skin_id"] for m in mine}
    for set_id, reward in sk.SET_REWARDS.items():
        need = [sid for sid, s in sk.SKINS.items() if s["set"] == set_id]
        sets[set_id] = {"need": need, "have": [x for x in need if x in have_ids], "reward": reward}
    lots = await conn.fetch(
        "SELECT o.id, o.price, o.asset, o.seller_id, u.skin_id, u.serial, u.xp, u.merged, u.stats FROM market_orders o "
        "JOIN user_skins u ON u.id::text = substr(o.asset, 3) "
        "WHERE o.status = 'open' AND o.side = 'sell' AND o.qty > 0 AND o.asset LIKE 's\\_%' AND o.team_id IS NULL "
        "ORDER BY o.price, o.created_at LIMIT 100")
    user = await conn.fetchrow("SELECT gender, suit, created_at FROM users WHERE user_id = $1", user_id)
    from shared.seasons import user_badges
    exo = await conn.fetchval("SELECT 1 FROM user_equip WHERE user_id = $1 AND suit = 'exo' LIMIT 1", user_id)
    stats = await conn.fetchrow("SELECT games_won, quiz_level FROM game_stats WHERE user_id = $1", user_id)
    best_cargo = await conn.fetchval("SELECT MAX(cargo) FROM expeditions WHERE user_id = $1 AND status = 'done'", user_id)
    duels_won = await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE user_id = $1 AND reason = 'duel_win'", user_id)
    return {
        "ok": True, "catalog": sk.public_catalog(lang), "mine": mine, "shop": shop, "sets": sets,
        "rarity_color": sk.RARITY_COLOR, "levels": [list(x) for x in sk.SKIN_LEVELS], "merge_xp": sk.SKIN_MERGE_XP,
        "event_xp": sk.SKIN_EVENT_XP, "stages": [list(x) for x in sk.SKIN_STAGES],
        "min_price": sk.SKIN_MIN_PRICE, "gender": user["gender"],
        "lots": [{"id": r["id"], "price": r["price"], "skin": r["skin_id"], "serial": r["serial"],
                  "level": sk.skin_level(r["xp"], r["merged"]), "stage": sk.skin_stage(sk.skin_level(r["xp"], r["merged"])),
                  "stats": sk._stats(r["stats"]), "own": r["seller_id"] == user_id}
                 for r in lots],
        "glory": {"badges": await user_badges(conn, user_id), "exo": bool(exo),
                  "games_won": (stats["games_won"] if stats else 0) or 0, "quiz_level": (stats["quiz_level"] if stats else 0) or 0,
                  "best_cargo": best_cargo or 0, "duels_won": duels_won or 0,
                  "days": max(0, (now - user["created_at"]).days)},
    }


async def handle_skins(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        return web.json_response(await skins_state(conn, ctx.user_id, ctx.lang))


async def _skin_act(request: web.Request, action) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    from shared.skins import SkinError
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                extra = await action(conn, ctx.user_id, data)
            out = await skins_state(conn, ctx.user_id, ctx.lang)
    except SkinError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    if isinstance(extra, dict):
        out["result"] = extra
    return web.json_response(out)


async def handle_skin_equip(request: web.Request) -> web.Response:
    from shared.skins import equip
    return await _skin_act(request, lambda conn, uid, d: equip(conn, uid, _int(d.get("id"))))


async def handle_skin_unequip(request: web.Request) -> web.Response:
    from shared.skins import unequip
    return await _skin_act(request, lambda conn, uid, d: unequip(conn, uid, _int(d.get("id"))))


async def handle_skin_absorb(request: web.Request) -> web.Response:
    from shared.skins import absorb
    return await _skin_act(request, lambda conn, uid, d: absorb(conn, uid, _int(d.get("id")), _int(d.get("fodder"))))


# ---------------------------------------------------------------- 🎟 пропуск сезона
async def pass_payload(conn, user_id: int, lang: str) -> dict:
    from shared import season_pass as sp
    from shared.prizes import rewards_label
    now = utcnow()
    season = sp.active_season(now)
    st = await sp.state(conn, user_id, season)
    sale = sp.sale_season(now)
    sale_st = st if sale == season else await sp.state(conn, user_id, sale)
    end = sp.season_end(season)
    levels = [{"level": n, "free": sp.rewards(season, "free", n), "paid": sp.rewards(season, "paid", n),
               "free_label": rewards_label(sp.rewards(season, "free", n), lang),
               "paid_label": rewards_label(sp.rewards(season, "paid", n), lang)}
              for n in range(1, sp.PASS_LEVELS + 1)]
    return {"ok": True, **st, "levels": levels, "per_level": sp.PASS_XP_PER_LEVEL, "max": sp.PASS_LEVELS,
            "ends_at": end.isoformat(), "xp_table": sp.PASS_XP, "stars": sp.PASS_STARS,
            "theme": sp.PASS_THEMES[int(season[5:7])][0 if lang == "ru" else 1],
            "sale": {"season": sale, "sku": sp.pass_sku(sale), "owned": sale_st["premium"]},
            "skins": sp.pass_skin_ids(season)}


async def handle_pass(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        return web.json_response(await pass_payload(conn, ctx.user_id, ctx.lang))


async def handle_pass_claim(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    from shared import season_pass as sp
    from shared.prizes import rewards_label
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                got = await sp.claim(conn, ctx.user_id, sp.active_season(utcnow()), utcnow())
            out = await pass_payload(conn, ctx.user_id, ctx.lang)
    except sp.PassError as e:
        return fail(t(ctx.lang, e.key))
    out["got"] = rewards_label(got, ctx.lang)
    return web.json_response(out)


async def handle_gear_history(request: web.Request) -> web.Response:
    ctx = await _guard(request)
    if isinstance(ctx, web.Response):
        return ctx
    from shared.trophies import gear_history
    async with db.pool.acquire() as conn:
        return web.json_response({"ok": True, "history": await gear_history(conn, ctx.user_id)})


def register_gear_routes(app: web.Application) -> None:
    app.router.add_get("/api/gear", handle_gear)
    app.router.add_post("/api/gear/gender", handle_gender)
    app.router.add_post("/api/gear/ref_suit", handle_ref_suit)
    app.router.add_post("/api/gear/equip", handle_equip)
    app.router.add_post("/api/gear/unequip", handle_unequip)
    app.router.add_post("/api/gear/upgrade", handle_upgrade)
    app.router.add_post("/api/gear/exo", handle_exo)
    app.router.add_post("/api/gear/art", handle_art)
    app.router.add_get("/api/gifts", handle_gifts)
    app.router.add_post("/api/gifts/claim", handle_gift_claim)
    app.router.add_get("/api/skins", handle_skins)
    app.router.add_post("/api/skins/equip", handle_skin_equip)
    app.router.add_post("/api/skins/unequip", handle_skin_unequip)
    app.router.add_post("/api/skins/absorb", handle_skin_absorb)
    app.router.add_get("/api/pass", handle_pass)
    app.router.add_post("/api/pass/claim", handle_pass_claim)
    app.router.add_get("/api/gear/history", handle_gear_history)
