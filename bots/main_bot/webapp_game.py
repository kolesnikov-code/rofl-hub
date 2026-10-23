"""
Игровые разделы Mini App (решение владельца 23.10): мастерская, налёты, биржа, станция команды,
ежедневные цели и заправка фермы — полноценное приложение вместо простыней текста в чате.

Вся логика и деньги переиспользуются из shared/* (те же функции, что у чат-обработчиков):
workshop.craft, raids.execute_raid, market.*, team_station.donate, daily_goals.claim_chest.
Каждый раздел уважает тумблер пульта (/features): выключен — 503 feature_off.
Ошибки игровой логики отдаются как {"ok": false, "message": "<текст на языке игрока>"}.

Налёты: ID целей не уходят в браузер — разведка выдаёт номера слотов, соответствие
слот → игрок хранится на сервере (анти-травля, как и в чате).
"""
from __future__ import annotations

import asyncio
import html
import json
import logging
import re
import time

from aiohttp import web

from shared.analytics import track
from shared.daily_goals import GoalsError, all_done, chest_coins, claim_chest, claimed_today, goal_progress, goals_for
from shared.database import db
from shared.economy import (
    ARMOR_BONUS_PER_LEVEL,
    ARMOR_MAX_LEVEL,
    DAILY_CHEST_RESOURCE,
    DAILY_STREAK_BONUS_COINS,
    DAILY_STREAK_BONUS_EVERY,
    MARKET_MAX_PRICE,
    MARKET_MIN_PRICE,
    MARKET_SHOWCASE_LIMIT,
    RAID_ATTACK_COOLDOWN_HOURS,
    RAID_FAIL_CAP,
    RAID_FAIL_PERCENT,
    RAID_FUEL_HYDROGEN,
    RAID_LOOT_CAP,
    RAID_LOOT_PERCENT,
    RAID_NEWBIE_SHIELD_DAYS,
    RAID_REVENGE_HOURS,
    RAID_VICTIM_COOLDOWN_HOURS,
    RESOURCE_KINDS,
    SHUTTLE_MARKET_FEE_PERCENT,
    MARKET_FEE_PERCENT,
    STATION_BONUS_PER_LEVEL,
    STATION_MAX_LEVEL,
    WORKSHOP_RECIPES,
    market_fee,
    market_limits,
    station_level_cost,
    utcnow,
)
from shared.farm_logic import apply_lazy_farm
from shared.feature_flags import FLAG_DEFAULTS, get_flag
from shared.locales import resolve_lang, t
from shared.market import (
    MarketError,
    buy_from_order,
    cancel_order,
    list_open_orders,
    market_stats,
    my_open_orders,
    place_sell_order,
)
from shared.raids import (
    STANCES,
    RaidError,
    attack_cooldown_left,
    display_name_of,
    execute_raid,
    find_targets,
    raid_stats,
    revenge_options,
    set_stance,
    shield_active,
)
from shared.ranks import rank_label
from shared.resources import get_resources
from shared.team_station import StationError, donate, get_station, progress_to_next, recent_donations, team_member_ids
from shared.webapp_auth import validate_init_data
from shared.workshop import WorkshopError, can_afford, craft, recipe_cost

logger = logging.getLogger(__name__)

RECIPE_ORDER = ("nitro_6h", "nuclear_3h", "drone_24h", "shield_24h", "cutlet", "armor", "shuttle")
SCOUT_TTL_SECONDS = 15 * 60
_scout_slots: dict[int, tuple[float, list[int]]] = {}   # атакующий → (время, [id целей по слотам])
_TAG = re.compile(r"<[^>]+>")


def plain(text: str) -> str:
    """Текст ошибки для alert в приложении: без HTML-тегов."""
    return html.unescape(_TAG.sub("", text))


# ============================================================================
# Общие помощники
# ============================================================================
class Ctx:
    def __init__(self, user_id: int, lang: str):
        self.user_id = user_id
        self.lang = lang


async def _ctx(request: web.Request) -> Ctx | web.Response:
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    parsed = validate_init_data(init_data, request.app["bot_token"])
    if not parsed or "user" not in parsed:
        return web.json_response({"error": "unauthorized"}, status=401)
    user_id = int(parsed["user"]["id"])
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT lang, is_blocked FROM users WHERE user_id = $1", user_id)
    if not row:
        return web.json_response({"error": "no_profile"}, status=404)
    if row["is_blocked"]:
        return web.json_response({"error": "blocked"}, status=403)
    return Ctx(user_id, resolve_lang(row["lang"]))


async def _feature_off(flag: str, lang: str) -> web.Response | None:
    if await get_flag(flag):
        return None
    return web.json_response({"error": "feature_off", "message": plain(t(lang, "common.feature_off"))},
                             status=503)


async def _json(request: web.Request) -> dict:
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def fail(message: str) -> web.Response:
    return web.json_response({"ok": False, "message": plain(message)})


def resource_labels(lang: str) -> dict[str, str]:
    return {k: t(lang, f"res.{k}") for k in RESOURCE_KINDS}


# ============================================================================
# Мастерская
# ============================================================================
def build_workshop_payload(stock: dict, armor_level: int, has_shuttle: bool, lang: str) -> dict:
    """Чистый сборщик витрины мастерской (юнит-тесты без aiohttp)."""
    recipes = []
    for rid in RECIPE_ORDER:
        recipe = WORKSHOP_RECIPES[rid]
        effect = recipe["effect"]
        done = (effect == "shuttle" and has_shuttle) or (effect == "armor" and armor_level >= ARMOR_MAX_LEVEL)
        cost = None if done else recipe_cost(rid, armor_level)
        recipes.append({
            "id": rid,
            "effect": effect,
            "title": t(lang, f"ws.recipe_{rid}", level=min(armor_level + 1, ARMOR_MAX_LEVEL)),
            "cost": cost or {},
            "hours": recipe.get("hours"),
            "done": done,
            "affordable": bool(cost) and can_afford(stock, cost),
        })
    return {
        "stock": stock,
        "res_names": resource_labels(lang),
        "armor_level": armor_level,
        "armor_max": ARMOR_MAX_LEVEL,
        "armor_pct": ARMOR_BONUS_PER_LEVEL,
        "has_shuttle": has_shuttle,
        "shuttle_fee": SHUTTLE_MARKET_FEE_PERCENT,
        "market_fee": MARKET_FEE_PERCENT,
        "recipes": recipes,
    }


async def handle_workshop(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("workshop", ctx.lang):
        return off
    async with db.pool.acquire() as conn:
        stock = await get_resources(conn, ctx.user_id)
        user = await conn.fetchrow("SELECT farm_armor_level, has_shuttle FROM users WHERE user_id = $1",
                                   ctx.user_id)
    return web.json_response(build_workshop_payload(stock, user["farm_armor_level"],
                                                    bool(user["has_shuttle"]), ctx.lang))


async def handle_craft(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("workshop", ctx.lang):
        return off
    rid = str((await _json(request)).get("recipe", ""))[:32]
    if rid not in WORKSHOP_RECIPES:
        return fail(t(ctx.lang, "ws.err_unknown"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await craft(conn, ctx.user_id, rid, utcnow())
    except WorkshopError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "craft", recipe=rid, source="webapp")
    return web.json_response({"ok": True, "effect": result.effect,
                              "until": result.until.isoformat() if result.until else None,
                              "level": result.level, "qty": result.qty})


# ============================================================================
# Налёты
# ============================================================================
RAID_RULES = {
    "fuel": RAID_FUEL_HYDROGEN, "loot_pct": RAID_LOOT_PERCENT, "loot_cap": RAID_LOOT_CAP,
    "fail_pct": RAID_FAIL_PERCENT, "fail_cap": RAID_FAIL_CAP, "cooldown_h": RAID_ATTACK_COOLDOWN_HOURS,
    "victim_h": RAID_VICTIM_COOLDOWN_HOURS, "newbie_days": RAID_NEWBIE_SHIELD_DAYS,
    "revenge_h": RAID_REVENGE_HOURS,
}


def _loot(raw) -> dict:
    """jsonb из asyncpg приходит строкой — приводим к словарю."""
    if isinstance(raw, dict):
        return raw
    try:
        value = json.loads(raw or "{}")
        return value if isinstance(value, dict) else {}
    except (TypeError, ValueError):
        return {}


def _remember_slots(attacker_id: int, target_ids: list[int]) -> None:
    now = time.monotonic()
    for uid in [u for u, (ts, _) in _scout_slots.items() if now - ts > SCOUT_TTL_SECONDS]:
        _scout_slots.pop(uid, None)
    _scout_slots[attacker_id] = (now, list(target_ids))


def _slot_target(attacker_id: int, slot: int) -> int | None:
    entry = _scout_slots.get(attacker_id)
    if not entry or time.monotonic() - entry[0] > SCOUT_TTL_SECONDS:
        return None
    ids = entry[1]
    return ids[slot] if 0 <= slot < len(ids) else None


async def handle_raids(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("raids", ctx.lang):
        return off
    now = utcnow()
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", ctx.user_id)
        stock = await get_resources(conn, ctx.user_id)
        stats = await raid_stats(conn, ctx.user_id)
        revenges = await revenge_options(conn, ctx.user_id, now)
    shield_until = user["raid_shield_until"]
    return web.json_response({
        "stock": stock,
        "res_names": resource_labels(ctx.lang),
        "cooldown_left": attack_cooldown_left(user["last_raid_at"], now),
        "shield": {
            "active": shield_active(user, now),
            "until": shield_until.isoformat() if shield_until and shield_until > now else None,
        },
        "stance": user["raid_stance"] if user["raid_stance"] in STANCES else None,
        "stats": stats,
        "revenge": [{"raid_id": r["raid_id"], "name": display_name_of(r)[:24],
                     "loot": _loot(r["loot"])} for r in revenges[:5]],
        "rules": RAID_RULES,
    })


async def handle_raid_stance(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("raids", ctx.lang):
        return off
    stance = str((await _json(request)).get("stance", ""))
    if stance not in STANCES:
        return fail(t(ctx.lang, "raid.err_stance"))
    async with db.pool.acquire() as conn:
        await set_stance(conn, ctx.user_id, stance)
    return web.json_response({"ok": True, "stance": stance})


async def handle_raid_scout(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("raids", ctx.lang):
        return off
    now = utcnow()
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id, last_raid_at FROM users WHERE user_id = $1", ctx.user_id)
        left = attack_cooldown_left(user["last_raid_at"], now)
        if left > 0:
            return fail(t(ctx.lang, "raid.err_cooldown", minutes=-(-left // 60)))
        hydrogen = (await get_resources(conn, ctx.user_id))["hydrogen"]
        if hydrogen < RAID_FUEL_HYDROGEN:
            return fail(t(ctx.lang, "raid.err_fuel", need=RAID_FUEL_HYDROGEN, have=hydrogen))
        targets = await find_targets(conn, ctx.user_id, user["team_id"], now)
    _remember_slots(ctx.user_id, [tg["user_id"] for tg in targets])
    return web.json_response({"ok": True, "targets": [{
        "slot": i,
        "name": display_name_of(tg)[:24],
        "rank": rank_label(ctx.lang, tg["created_at"], now),
        "total": int(tg["total"]),
    } for i, tg in enumerate(targets)]})


async def handle_raid_go(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("raids", ctx.lang):
        return off
    data = await _json(request)
    move = str(data.get("move", ""))
    if move not in STANCES:
        return fail(t(ctx.lang, "raid.err_stance"))
    revenge_id = _int(data.get("revenge"), 0)
    now = utcnow()
    async with db.pool.acquire() as conn:
        if revenge_id:
            target_id = await conn.fetchval(
                "SELECT attacker_id FROM raids WHERE id = $1 AND defender_id = $2", revenge_id, ctx.user_id)
        else:
            target_id = _slot_target(ctx.user_id, _int(data.get("slot"), -1))
        if target_id is None:
            return fail(t(ctx.lang, "raid.err_gone"))
        try:
            async with conn.transaction():
                result = await execute_raid(conn, ctx.user_id, target_id, move, now,
                                            revenge_of=revenge_id or None)
        except RaidError as e:
            return fail(e.localized(ctx.lang))
        defender = await conn.fetchrow(
            "SELECT user_id, display_name, lang, created_at FROM users WHERE user_id = $1", target_id)
        attacker = await conn.fetchrow(
            "SELECT user_id, display_name, created_at FROM users WHERE user_id = $1", ctx.user_id)
    _scout_slots.pop(ctx.user_id, None)
    await track(ctx.user_id, "raid", result=result.result, revenge=result.is_revenge, source="webapp")
    bot = request.app.get("bot")
    if bot is not None:
        from bots.main_bot.handlers.raids import _notify_defender
        asyncio.create_task(_notify_defender(bot, defender, attacker, result, now))
    return web.json_response({"ok": True, "result": result.result, "move": result.move,
                              "stance": result.stance, "loot": result.loot,
                              "name": display_name_of(defender)[:24], "revenge": result.is_revenge})


# ============================================================================
# Биржа котлет
# ============================================================================
async def handle_market(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    async with db.pool.acquire() as conn:
        stats = await market_stats(conn)
        orders = await list_open_orders(conn, MARKET_SHOWCASE_LIMIT * 2, exclude_user=ctx.user_id)
        mine = await my_open_orders(conn, ctx.user_id)
        user = await conn.fetchrow("SELECT inv_cutlets, balance, has_shuttle FROM users WHERE user_id = $1",
                                   ctx.user_id)
    max_qty, max_orders = market_limits(bool(user["has_shuttle"]))
    return web.json_response({
        "stats": {"orders": stats["orders"], "cutlets": stats["cutlets"], "best_price": stats["best_price"]},
        "orders": [{"id": o["id"], "qty": o["qty"], "price": o["price"]} for o in orders],
        "my": [{"id": o["id"], "qty": o["qty"], "price": o["price"]} for o in mine],
        "inv": user["inv_cutlets"], "balance": user["balance"],
        "shuttle": bool(user["has_shuttle"]),
        "fee": SHUTTLE_MARKET_FEE_PERCENT if user["has_shuttle"] else MARKET_FEE_PERCENT,
        "max_qty": max_qty, "max_orders": max_orders,
        "min_price": MARKET_MIN_PRICE, "max_price": MARKET_MAX_PRICE,
    })


async def handle_market_buy(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    data = await _json(request)
    order_id, qty = _int(data.get("order_id")), _int(data.get("qty"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                deal = await buy_from_order(conn, ctx.user_id, order_id, qty)
            seller_lang = resolve_lang(await conn.fetchval(
                "SELECT lang FROM users WHERE user_id = $1", deal["seller_id"]))
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "market_buy", order_id=order_id, qty=deal["qty"], total=deal["total"],
                source="webapp")
    bot = request.app.get("bot")
    if bot is not None:
        asyncio.create_task(_notify_seller(bot, deal, order_id, seller_lang))
    return web.json_response({"ok": True, "qty": deal["qty"], "total": deal["total"]})


async def _notify_seller(bot, deal: dict, order_id: int, lang: str) -> None:
    try:
        await bot.send_message(
            deal["seller_id"],
            t(lang, "mk.sold_notify", id=order_id, qty=deal["qty"], price=deal["price"],
              got=deal["seller_got"], fee=deal["fee"]),
            parse_mode="HTML")
    except Exception:
        pass


async def handle_market_sell(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    data = await _json(request)
    qty, price = _int(data.get("qty")), _int(data.get("price"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                order_id = await place_sell_order(conn, ctx.user_id, qty, price)
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "market_sell_order", order_id=order_id, qty=qty, price=price, source="webapp")
    return web.json_response({"ok": True, "order_id": order_id})


async def handle_market_cancel(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    order_id = _int((await _json(request)).get("order_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                qty = await cancel_order(conn, ctx.user_id, order_id)
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    return web.json_response({"ok": True, "qty": qty})


def sell_preview(qty: int, price: int, shuttle: bool) -> dict:
    """Сколько получит продавец (для подсказки в форме продажи)."""
    total = max(0, qty) * max(0, price)
    fee = market_fee(total, shuttle=shuttle)
    return {"total": total, "fee": fee, "got": total - fee}


# ============================================================================
# Команда и станция
# ============================================================================
async def handle_team(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1", ctx.user_id)
        stock = await get_resources(conn, ctx.user_id)
        if user["team_id"] is None:
            return web.json_response({"team": None, "stock": stock, "res_names": resource_labels(ctx.lang)})
        team = await conn.fetchrow(
            "SELECT team_name, members_count, max_members, captain_id FROM teams WHERE team_id = $1",
            user["team_id"])
        station = await get_station(conn, user["team_id"])
        feed = await recent_donations(conn, user["team_id"])
    station_on = await get_flag("station")
    level = station["level"]
    stored = {k: station[k] for k in RESOURCE_KINDS}
    return web.json_response({
        "team": {"name": team["team_name"], "members": team["members_count"],
                 "max": team["max_members"], "is_clan": team["max_members"] >= 1000,
                 "captain": team["captain_id"] == ctx.user_id},
        "station": {
            "enabled": station_on, "level": level, "max": STATION_MAX_LEVEL,
            "per_level": STATION_BONUS_PER_LEVEL, "percent": level * STATION_BONUS_PER_LEVEL,
            "cost": station_level_cost(level + 1) if level < STATION_MAX_LEVEL else 0,
            "stored": stored, "need": progress_to_next(level, stored),
        },
        "feed": [{"name": ("@" + d["username"]) if d.get("username") else
                  ((d.get("display_name") or "").strip() or "#" + str(d["user_id"])[-4:]),
                  "kind": d["kind"], "qty": d["qty"]} for d in feed],
        "stock": stock,
        "res_names": resource_labels(ctx.lang),
    })


async def handle_station_donate(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("station", ctx.lang):
        return off
    data = await _json(request)
    kind, qty = str(data.get("kind", "")), _int(data.get("qty"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await donate(conn, ctx.user_id, kind, qty)
                team_id = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", ctx.user_id)
                members = await team_member_ids(conn, team_id) if result.levels_gained else []
    except StationError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "station_donate", kind=kind, qty=qty, level=result.level, source="webapp")
    bot = request.app.get("bot")
    if result.levels_gained and bot is not None:
        from bots.main_bot.handlers.station import _announce_level
        asyncio.create_task(_announce_level(bot, members, result.level))
    return web.json_response({"ok": True, "level": result.level, "levels_gained": result.levels_gained})


# ============================================================================
# Ежедневные цели
# ============================================================================
async def _enabled_features() -> set[str]:
    return {key for key in FLAG_DEFAULTS if key != "maintenance" and await get_flag(key)}


async def handle_goals(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("goals", ctx.lang):
        return off
    today = utcnow().date()
    goals = goals_for(ctx.user_id, today, await _enabled_features())
    async with db.pool.acquire() as conn:
        progress = await goal_progress(conn, ctx.user_id, goals, today)
        claimed = await claimed_today(conn, ctx.user_id, today)
        streak = await conn.fetchval("SELECT goal_streak FROM users WHERE user_id = $1", ctx.user_id) or 0
    return web.json_response({
        "goals": [{"key": g.key, "target": g.target, "progress": progress.get(g.key, 0),
                   "title": plain(t(ctx.lang, f"goal.{g.key}", n=g.target))} for g in goals],
        "done": all_done(goals, progress), "claimed": claimed, "streak": streak,
        "chest_coins": chest_coins(0), "chest_res": DAILY_CHEST_RESOURCE,
        "every": DAILY_STREAK_BONUS_EVERY, "streak_bonus": DAILY_STREAK_BONUS_COINS,
    })


async def handle_goals_claim(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("goals", ctx.lang):
        return off
    today = utcnow().date()
    goals = goals_for(ctx.user_id, today, await _enabled_features())
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                chest = await claim_chest(conn, ctx.user_id, goals, today)
    except GoalsError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "daily_chest", streak=chest["streak"], source="webapp")
    return web.json_response({"ok": True, **chest, "res_name": t(ctx.lang, f"res.{chest['kind']}")})


# ============================================================================
# Заправка фермы (котлеты со склада → холодильник)
# ============================================================================
async def handle_refuel(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    mode = str((await _json(request)).get("mode", "all"))
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, _ = await apply_lazy_farm(conn, ctx.user_id, utcnow())
            space = user["fridge_capacity"] - user["fridge_cutlets"]
            if user["inv_cutlets"] <= 0:
                return fail(t(ctx.lang, "farm.no_inv_cutlets"))
            if space <= 0:
                return fail(t(ctx.lang, "farm.fridge_full"))
            load = 1 if mode == "one" else min(user["inv_cutlets"], space)
            await conn.execute(
                "UPDATE users SET inv_cutlets = inv_cutlets - $1, fridge_cutlets = fridge_cutlets + $1 "
                "WHERE user_id = $2", load, ctx.user_id)
            # загруженные котлеты сразу уходят в баки голодных бурильщиков
            await apply_lazy_farm(conn, ctx.user_id, utcnow())
    await track(ctx.user_id, "farm_refuel", mode=mode, source="webapp")
    return web.json_response({"ok": True, "loaded": load})


def register_game_routes(app: web.Application) -> None:
    app.router.add_get("/api/workshop", handle_workshop)
    app.router.add_post("/api/craft", handle_craft)
    app.router.add_get("/api/raids", handle_raids)
    app.router.add_post("/api/raid/stance", handle_raid_stance)
    app.router.add_post("/api/raid/scout", handle_raid_scout)
    app.router.add_post("/api/raid/go", handle_raid_go)
    app.router.add_get("/api/market", handle_market)
    app.router.add_post("/api/market/buy", handle_market_buy)
    app.router.add_post("/api/market/sell", handle_market_sell)
    app.router.add_post("/api/market/cancel", handle_market_cancel)
    app.router.add_get("/api/team", handle_team)
    app.router.add_post("/api/station/donate", handle_station_donate)
    app.router.add_get("/api/goals", handle_goals)
    app.router.add_post("/api/goals/claim", handle_goals_claim)
    app.router.add_post("/api/refuel", handle_refuel)
