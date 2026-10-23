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
import os
import re
import time

from aiohttp import web

from shared.analytics import track
from shared.daily_goals import GoalsError, all_done, chest_coins, claim_chest, claimed_today, goal_progress, goals_for
from shared.database import db
from shared.economy import (
    REFERRAL_QUALIFIED_BONUS,
    REFERRAL_QUALIFIED_CUTLETS,
    REFERRAL_QUALIFY_ROUNDS,
    REFERRAL_SIGNUP_BONUS,
    REFERRAL_TOP_LIMIT,
    RES_CAPACITY_BASE,
    next_storage_level,
    ARMOR_DAYS,
    armor_level_active,
    ARMOR_BONUS_PER_LEVEL,
    ARMOR_MAX_LEVEL,
    DAILY_CHEST_RESOURCE,
    DAILY_STREAK_BONUS_COINS,
    DAILY_STREAK_BONUS_EVERY,
    MARKET_ASSETS,
    MARKET_CUTLET_MIN_PRICE,
    MARKET_MAX_PRICE,
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
    market_min_price,
    station_level_cost,
    utcnow,
)
from shared.farm_logic import apply_lazy_farm
from shared.feature_flags import FLAG_DEFAULTS, get_flag
from shared.locales import resolve_lang, t
from shared.market import (
    MarketError,
    accept_swap,
    cancel_order,
    cancel_swap,
    create_swap,
    fill_order,
    index_change,
    list_open_orders,
    list_swaps,
    market_stats,
    my_open_orders,
    my_swaps,
    place_order,
    price_history,
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
from shared.workshop import WorkshopError, can_afford, craft, recipe_coins, recipe_cost
from shared.weekly_recipes import WEEKLY_RECIPES, WeeklyError, active_weekly_ids, craft_weekly, crafted_this_week, recipe_title

logger = logging.getLogger(__name__)

RECIPE_ORDER = ("nitro_6h", "nuclear_3h", "drone_24h", "shield_24h", "cutlet", "armor", "storage", "shuttle")
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
def build_workshop_payload(stock: dict, armor_level: int, has_shuttle: bool, lang: str,
                           balance: int = 0, armor_until=None, capacity: int = RES_CAPACITY_BASE,
                           weekly: list | None = None) -> dict:
    """Чистый сборщик витрины мастерской (юнит-тесты без aiohttp). armor_level — действующий."""
    recipes = []
    for rid in RECIPE_ORDER:
        recipe = WORKSHOP_RECIPES[rid]
        effect = recipe["effect"]
        done = (effect == "shuttle" and has_shuttle) or (effect == "storage" and next_storage_level(capacity) is None)
        cost = None if done else recipe_cost(rid, armor_level, capacity)
        coins = recipe_coins(rid)
        recipes.append({
            "id": rid,
            "effect": effect,
            "title": t(lang, f"ws.recipe_{rid}", level=min(armor_level + 1, ARMOR_MAX_LEVEL),
                       cap=(next_storage_level(capacity) or (capacity, None))[0]),
            "cost": cost or {},
            "coins": coins,
            "hours": recipe.get("hours"),
            "days": ARMOR_DAYS if effect == "armor" else None,
            "done": done,
            "affordable": bool(cost) and can_afford(stock, cost) and balance >= coins,
        })
    return {
        "stock": stock,
        "balance": balance,
        "res_names": resource_labels(lang),
        "armor_level": armor_level,
        "armor_until": armor_until.isoformat() if armor_until and armor_level else None,
        "capacity": capacity,
        "weekly": weekly or [],
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
        user = await conn.fetchrow(
            "SELECT farm_armor_level, armor_until, has_shuttle, balance, res_capacity FROM users WHERE user_id = $1",
            ctx.user_id)
        now = utcnow()
        weekly = []
        for rid in await active_weekly_ids():
            recipe = WEEKLY_RECIPES[rid]
            done = await crafted_this_week(conn, ctx.user_id, rid, now)
            weekly.append({"id": rid, "title": recipe_title(ctx.lang, rid), "cost": recipe["cost"],
                           "limit": recipe["limit"], "left": max(0, recipe["limit"] - done),
                           "affordable": can_afford(stock, recipe["cost"]) and done < recipe["limit"]})
    armor = armor_level_active(user["farm_armor_level"], user["armor_until"], now)
    return web.json_response(build_workshop_payload(stock, armor, bool(user["has_shuttle"]), ctx.lang,
                                                    balance=user["balance"], armor_until=user["armor_until"],
                                                    capacity=user["res_capacity"], weekly=weekly))


async def handle_craft_weekly(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("workshop", ctx.lang):
        return off
    rid = str((await _json(request)).get("recipe", ""))[:32]
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await craft_weekly(conn, ctx.user_id, rid, utcnow())
    except WeeklyError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "craft_weekly", recipe=rid, source="webapp")
    return web.json_response({"ok": True, "left": res["left"]})


# ============================================================================
# 🤝 Друзья: реферальная ссылка, статистика, рейтинг «у кого больше друзей»
# ============================================================================
_bot_username: str | None = None


async def _bot_name(request: web.Request) -> str:
    global _bot_username
    if _bot_username:
        return _bot_username
    bot = request.app.get("bot")
    if bot is not None:
        try:
            _bot_username = (await bot.me()).username
            return _bot_username
        except Exception:
            pass
    return os.getenv("MAIN_BOT_USERNAME", "").lstrip("@")


async def handle_referral(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    now = utcnow()
    async with db.pool.acquire() as conn:
        stats = await conn.fetchrow(
            """SELECT COUNT(*) AS invited, COUNT(*) FILTER (WHERE qualified_at IS NOT NULL) AS qualified
               FROM users WHERE referred_by = $1""", ctx.user_id)
        earned = await conn.fetchval(
            "SELECT COALESCE(SUM(delta), 0) FROM ledger WHERE user_id = $1 "
            "AND reason IN ('referral_signup', 'referral_qualified')", ctx.user_id)
        rows = await conn.fetch(
            """SELECT r.user_id, r.username, r.display_name, r.created_at,
                      COUNT(*) FILTER (WHERE u.qualified_at IS NOT NULL) AS qualified, COUNT(*) AS invited
               FROM users u JOIN users r ON r.user_id = u.referred_by
               WHERE NOT r.is_blocked
               GROUP BY r.user_id HAVING COUNT(*) > 0
               ORDER BY qualified DESC, invited DESC, r.user_id ASC LIMIT $1""", REFERRAL_TOP_LIMIT)
    username = await _bot_name(request)
    link = f"https://t.me/{username}?start={ctx.user_id}" if username else ""
    return web.json_response({
        "link": link,
        "share_text": plain(t(ctx.lang, "ref.share_text")),
        "invited": int(stats["invited"]), "qualified": int(stats["qualified"]),
        "earned": int(earned), "cutlets": int(stats["qualified"]) * REFERRAL_QUALIFIED_CUTLETS,
        "rules": {"signup": REFERRAL_SIGNUP_BONUS, "qualified": REFERRAL_QUALIFIED_BONUS,
                  "rounds": REFERRAL_QUALIFY_ROUNDS, "cutlets": REFERRAL_QUALIFIED_CUTLETS},
        "top": [{"name": f"@{r['username']}" if r["username"] else (r["display_name"] or "#" + str(r["user_id"])[-4:]),
                 "rank": rank_label(ctx.lang, r["created_at"], now),
                 "qualified": int(r["qualified"]), "invited": int(r["invited"]),
                 "me": r["user_id"] == ctx.user_id} for r in rows],
    })


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
ASSET_ICONS = {"cutlet": "🥩", "metal": "⛏", "hydrogen": "💧", "crystal": "💎", "parts": "⚙️"}


async def _asset_stock(conn, user_id: int, asset: str) -> int:
    if asset == "cutlet":
        return await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = $1", user_id) or 0
    return (await get_resources(conn, user_id))[asset]


async def handle_market(request: web.Request) -> web.Response:
    """Биржа v2: стакан выбранного товара, мои ордера, график 7 дней, индекс, обмен ресурсов."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    asset = request.query.get("asset", "cutlet")
    if asset not in MARKET_ASSETS:
        asset = "cutlet"
    now = utcnow()
    async with db.pool.acquire() as conn:
        stats = await market_stats(conn, asset)
        asks = await list_open_orders(conn, MARKET_SHOWCASE_LIMIT * 2, exclude_user=ctx.user_id,
                                      asset=asset, side="sell")
        bids = await list_open_orders(conn, MARKET_SHOWCASE_LIMIT * 2, exclude_user=ctx.user_id,
                                      asset=asset, side="buy")
        mine = await my_open_orders(conn, ctx.user_id)
        user = await conn.fetchrow("SELECT inv_cutlets, balance, has_shuttle FROM users WHERE user_id = $1",
                                   ctx.user_id)
        stock = await get_resources(conn, ctx.user_id)
        history = await price_history(conn, asset, now)
        index = {}
        for a in MARKET_ASSETS:
            index[a] = index_change(history if a == asset else await price_history(conn, a, now))
        swaps = await list_swaps(conn, 20, exclude_user=ctx.user_id)
        my_sw = await my_swaps(conn, ctx.user_id)
    shuttle = bool(user["has_shuttle"])
    max_qty, max_orders = market_limits(shuttle, asset)
    slim = lambda o: {"id": o["id"], "qty": o["qty"], "price": o["price"]}  # noqa: E731
    return web.json_response({
        "asset": asset,
        "stats": {"orders": stats["orders"], "qty": stats["qty"], "best_price": stats["best_price"],
                  "bids": stats["bids"], "best_bid": stats["best_bid"]},
        "asks": [slim(o) for o in asks], "bids": [slim(o) for o in bids],
        "my": [{"id": o["id"], "qty": o["qty"], "price": o["price"], "asset": o["asset"], "side": o["side"]}
               for o in mine],
        "have": user["inv_cutlets"] if asset == "cutlet" else stock[asset],
        "inv": user["inv_cutlets"], "stock": stock, "balance": user["balance"],
        "shuttle": shuttle,
        "fee": SHUTTLE_MARKET_FEE_PERCENT if shuttle else MARKET_FEE_PERCENT,
        "max_qty": max_qty, "max_orders": max_orders,
        "min_price": market_min_price(asset), "max_price": MARKET_MAX_PRICE,
        "cutlet_floor": MARKET_CUTLET_MIN_PRICE,
        "history": history, "index": index,
        "swaps": [{"id": s["id"], "give_kind": s["give_kind"], "give_qty": s["give_qty"],
                   "want_kind": s["want_kind"], "want_qty": s["want_qty"]} for s in swaps],
        "my_swaps": my_sw,
        "res_names": resource_labels(ctx.lang),
    })


async def handle_market_order(request: web.Request) -> web.Response:
    """Новый ордер: продажа (товар в эскроу) или заявка на покупку (монеты в эскроу)."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    data = await _json(request)
    asset, side = str(data.get("asset", "cutlet")), str(data.get("side", "sell"))
    qty, price = _int(data.get("qty")), _int(data.get("price"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                order_id = await place_order(conn, ctx.user_id, asset, side, qty, price)
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "market_order", asset=asset, side=side, qty=qty, price=price, source="webapp")
    return web.json_response({"ok": True, "order_id": order_id})


async def handle_market_fill(request: web.Request) -> web.Response:
    """Сделка по чужому ордеру: купить из продажи или продать в заявку."""
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
                deal = await fill_order(conn, ctx.user_id, order_id, qty)
            maker_lang = resolve_lang(await conn.fetchval(
                "SELECT lang FROM users WHERE user_id = $1", deal["maker_id"]))
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "market_buy" if deal["side"] == "sell" else "market_sell",
                asset=deal["asset"], order_id=order_id, qty=deal["qty"], total=deal["total"], source="webapp")
    bot = request.app.get("bot")
    if bot is not None:
        asyncio.create_task(_notify_maker(bot, deal, order_id, maker_lang))
    return web.json_response({"ok": True, "qty": deal["qty"], "total": deal["total"], "fee": deal["fee"],
                              "side": deal["side"], "asset": deal["asset"],
                              "got": deal["seller_got"] if deal["side"] == "buy" else None})


async def _notify_maker(bot, deal: dict, order_id: int, lang: str) -> None:
    """ЛС автору ордера на его языке: продажа состоялась или заявка на покупку исполнена."""
    try:
        if deal["side"] == "sell":
            text = t(lang, "mk.sold_notify", id=order_id, qty=deal["qty"], price=deal["price"],
                     got=deal["seller_got"], fee=deal["fee"])
        else:
            text = t(lang, "mk.bid_filled_notify", id=order_id, qty=deal["qty"],
                     icon=ASSET_ICONS[deal["asset"]], price=deal["price"])
        await bot.send_message(deal["maker_id"], text, parse_mode="HTML")
    except Exception:
        pass


# Совместимость со старыми клиентами приложения (кэш WebView): котлеты как раньше
async def handle_market_buy(request: web.Request) -> web.Response:
    return await handle_market_fill(request)


async def handle_market_sell(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                order_id = await place_order(conn, ctx.user_id, "cutlet", "sell",
                                             _int(data.get("qty")), _int(data.get("price")))
    except MarketError as e:
        return fail(e.localized(ctx.lang))
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


# ---------------------------------------------------------------- обмен ресурс ↔ ресурс
async def handle_swap_create(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                swap_id = await create_swap(conn, ctx.user_id, str(data.get("give_kind", "")),
                                            _int(data.get("give_qty")), str(data.get("want_kind", "")),
                                            _int(data.get("want_qty")))
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "swap_created", source="webapp")
    return web.json_response({"ok": True, "swap_id": swap_id})


async def handle_swap_accept(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("market", ctx.lang):
        return off
    swap_id = _int((await _json(request)).get("swap_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                swap = await accept_swap(conn, ctx.user_id, swap_id)
            maker_lang = resolve_lang(await conn.fetchval(
                "SELECT lang FROM users WHERE user_id = $1", swap["maker_id"]))
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "swap_accepted", source="webapp")
    bot = request.app.get("bot")
    if bot is not None:
        asyncio.create_task(_notify_swap(bot, swap, maker_lang))
    return web.json_response({"ok": True})


async def _notify_swap(bot, swap: dict, lang: str) -> None:
    try:
        await bot.send_message(swap["maker_id"], t(
            lang, "sw.done_notify", id=swap["id"],
            give=f"{swap['give_qty']} {ASSET_ICONS[swap['give_kind']]}",
            want=f"{swap['want_qty']} {ASSET_ICONS[swap['want_kind']]}"), parse_mode="HTML")
    except Exception:
        pass


async def handle_swap_cancel(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    swap_id = _int((await _json(request)).get("swap_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await cancel_swap(conn, ctx.user_id, swap_id)
    except MarketError as e:
        return fail(e.localized(ctx.lang))
    return web.json_response({"ok": True})


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
    app.router.add_post("/api/craft_weekly", handle_craft_weekly)
    app.router.add_get("/api/referral", handle_referral)
    app.router.add_get("/api/raids", handle_raids)
    app.router.add_post("/api/raid/stance", handle_raid_stance)
    app.router.add_post("/api/raid/scout", handle_raid_scout)
    app.router.add_post("/api/raid/go", handle_raid_go)
    app.router.add_get("/api/market", handle_market)
    app.router.add_post("/api/market/order", handle_market_order)
    app.router.add_post("/api/market/fill", handle_market_fill)
    app.router.add_post("/api/market/buy", handle_market_buy)      # старые клиенты
    app.router.add_post("/api/market/sell", handle_market_sell)    # старые клиенты
    app.router.add_post("/api/market/cancel", handle_market_cancel)
    app.router.add_post("/api/swap/create", handle_swap_create)
    app.router.add_post("/api/swap/accept", handle_swap_accept)
    app.router.add_post("/api/swap/cancel", handle_swap_cancel)
    app.router.add_get("/api/team", handle_team)
    app.router.add_post("/api/station/donate", handle_station_donate)
    app.router.add_get("/api/goals", handle_goals)
    app.router.add_post("/api/goals/claim", handle_goals_claim)
    app.router.add_post("/api/refuel", handle_refuel)
