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
from datetime import timedelta
import html
import json
import logging
import os
import re
import time

from aiohttp import web

from shared.analytics import referral_reward_text
from shared.analytics import track
from shared.daily_goals import GoalsError, all_done, chest_coins, claim_chest, claimed_today, goal_progress, goals_for
from shared.database import db
from shared.economy import (
    DRONE_COIN_PRICE,
    DRONE_EXP_CARGO_PCT,
    DRONE_EXP_GUARD_PCT,
    DRONE_EXP_SPEED_PCT,
    DRONE_RAID_ATTACK_PCT,
    DRONE_RAID_GUARD_PCT,
    DRONE_SPY_TARGETS,
    REFERRAL_QUALIFIED_BONUS,
    REFERRAL_QUALIFY_BONUS_CLAIMS,
    REFERRAL_QUALIFY_QUIZ_LEVEL,
    REFERRAL_TOP_LIMIT,
    RES_CAPACITY_BASE,
    BATTLE_BATTERY_FEE_CLAN,
    BATTLE_BATTERY_FEE_TEAM,
    season_bounds,
    season_key,
    next_storage_level,
    items_capacity,
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
    MARKET_APP_LIST_LIMIT,
    MARKET_APP_SWAPS_LIMIT,
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
    team_market_fee_percent,
    TEAM_HELP_MAX_QTY,
    TEAM_HELP_DAILY_GIVE,
    TEAM_HELP_GIVER_MIN_BONUS_CLAIMS,
    TEAM_HELP_GIVER_MIN_QUIZ_LEVEL,
    ITEM_COLUMNS,
    ITEM_EFFECTS,
    ALL_KINDS,
    TRADEABLE_KINDS,
    HORSE_PRICES,
    MAX_HORSES,
    MAX_CARTS,
    TECHS,
    TECH_ORDER,
    TOOL_COSTS,
    market_lots,
    raid_candidates,
    tech_cost,
    tech_tool_required,
    tech_cooldown_days,
    science_gate_ok,
    RAID_ATTACK_BONUS_PER_LEVEL,
    RAID_DEFENSE_PER_LEVEL,
    SCIENCE_PERCENT_PER_LEVEL,
    COMM_COOLDOWN_MINUTES_PER_LEVEL,
    SHUTTLE_CHARGE_DAYS,
    ONE_SHOT_COLUMNS,
    FORSAGE_COOLDOWN_HOURS,
    MINE_HOLD_HOURS,
    MINE_YIELD_PER_MEMBER_HOUR,
    WORKSHOP_UNLOCK_ORDER,
    recipe_unlock_at,
    MEGA_CLAN_MAX_MEMBERS,
    CLAN_MARKET_FEE_PERCENT,
    TEAM_SYMBOL_MAX_LEN,
    TEAM_NAME_MAX_LEN,
    TEAM_MOTTO_MAX_LEN,
    TEAM_CREATE_COST,
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
    RaidError,
    scout as raid_scout,
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
from shared.team_help import HelpError, can_give, cancel_help, give_help, given_today, open_requests, request_help
from shared.items import ItemError, activate_item, list_items
from shared.mines import list_mines, mine_battles
from shared.tech import (TechError, buy_horse, charge_shuttle, get_tech, next_tech_at, shuttle_active,
                         tech_levels, upgrade_tech, upgrade_tools)
from shared.workshop import recipe_tool, team_cost_multiplier
from shared.db_clans import (TeamError, create_team, join_team, leave_team, public_team, random_teams,
                             search_teams, team_members)
from shared.resources import get_resources
from shared.team_station import StationError, donate, get_station, progress_to_next, recent_donations, team_member_ids
from shared.webapp_auth import validate_init_data
from shared.workshop import WorkshopError, can_afford, craft, recipe_coins, recipe_cost
from shared.weekly_recipes import (WEEKLY_RECIPES, WeeklyError, active_weekly_ids, craft_weekly, crafted_this_week,
                                   recipe_title, week_start)

logger = logging.getLogger(__name__)

RECIPE_ORDER = WORKSHOP_UNLOCK_ORDER   # от самого простого к легендарному (порядок открытия новичку)
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
        row = await conn.fetchrow(
            "SELECT lang, is_blocked, deletion_requested_at, deleted_at FROM users WHERE user_id = $1", user_id)
    if not row or row["deleted_at"] is not None:
        return web.json_response({"error": "no_profile"}, status=404)
    if row["is_blocked"]:
        return web.json_response({"error": "blocked"}, status=403)
    if row["deletion_requested_at"] is not None:
        return web.json_response({"error": "deleting"}, status=403)
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
    return {k: t(lang, f"res.{k}") for k in ALL_KINDS}


# ============================================================================
# Мастерская
# ============================================================================
# Сила одного боевого дрона — для подписей в мастерской (числа только из economy)
DRONE_FX = {"ra": DRONE_RAID_ATTACK_PCT, "rg": DRONE_RAID_GUARD_PCT, "st": DRONE_SPY_TARGETS,
            "ec": DRONE_EXP_CARGO_PCT, "eg": DRONE_EXP_GUARD_PCT, "es": DRONE_EXP_SPEED_PCT}


def build_workshop_payload(stock: dict, armor_level: int, has_shuttle: bool, lang: str,
                           balance: int = 0, armor_until=None, capacity: int = RES_CAPACITY_BASE,
                           weekly: list | None = None, created_at=None, now=None,
                           disabled=(), week_done: dict | None = None, tools_level: int = 0,
                           team_mult: int = 1, in_team: bool = True, drones: dict | None = None) -> dict:
    """
    Чистый сборщик витрины мастерской (юнит-тесты без aiohttp). armor_level — действующий.
    created_at/now — поэтапное открытие (по рецепту в сутки); disabled — выключенные владельцем.
    """
    recipes = []
    week_done = week_done or {}
    for rid in RECIPE_ORDER:
        if rid in disabled:
            continue
        recipe = WORKSHOP_RECIPES[rid]
        opens = recipe_unlock_at(rid, created_at) if created_at is not None and now is not None else None
        locked = opens is not None and opens > now
        limit = recipe.get("week_limit")
        week_left = max(0, limit - week_done.get(rid, 0)) if limit else None
        effect = recipe["effect"]
        done = (effect == "shuttle" and has_shuttle) or (effect == "storage" and next_storage_level(capacity) is None)
        cost = None if done else recipe_cost(rid, armor_level, capacity, team_mult)
        need_tool = recipe_tool(rid, armor_level)
        team_ok = in_team or not recipe.get("team")
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
            "affordable": (bool(cost) and can_afford(stock, cost) and balance >= coins and not locked
                           and week_left != 0 and tools_level >= need_tool and team_ok),
            "tool": need_tool, "tool_ok": tools_level >= need_tool, "team": bool(recipe.get("team")),
            "team_ok": team_ok,
            "locked": locked,
            "unlock_in": int((opens - now).total_seconds()) if locked else 0,
            "week_limit": limit, "week_left": week_left,
            "stored": effect in ITEM_EFFECTS,
            "drone": recipe.get("drone"),
            "buy_coins": DRONE_COIN_PRICE if effect == "bdrone" else 0,
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
        "tools_level": tools_level, "team_mult": team_mult,
        "armor_pct": ARMOR_BONUS_PER_LEVEL,
        "has_shuttle": has_shuttle,
        "shuttle_fee": SHUTTLE_MARKET_FEE_PERCENT,
        "market_fee": MARKET_FEE_PERCENT,
        "recipes": recipes,
        "drones": drones or {"guard": 0, "attack": 0, "spy": 0},
        "drone_fx": DRONE_FX,
    }


async def handle_workshop(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("workshop", ctx.lang):
        return off
    async with db.pool.acquire() as conn:
        stock = await get_resources(conn, ctx.user_id, ALL_KINDS)
        user = await conn.fetchrow(
            "SELECT farm_armor_level, armor_until, has_shuttle, balance, res_capacity, created_at, team_id, "
            "drones_guard, drones_attack, drones_spy FROM users WHERE user_id = $1", ctx.user_id)
        tools_level = (await tech_levels(conn, ctx.user_id))["tools"]
        team_mult = team_cost_multiplier(await conn.fetchval(
            "SELECT max_members FROM teams WHERE team_id = $1", user["team_id"])) if user["team_id"] else 1
        now = utcnow()
        week_done = {r["recipe_id"][3:]: r["n"] for r in await conn.fetch(
            "SELECT recipe_id, COUNT(*) AS n FROM weekly_crafts WHERE user_id = $1 AND recipe_id LIKE 'ws:%' "
            "AND created_at >= $2 GROUP BY recipe_id", ctx.user_id, week_start(now))}
        disabled = [rid for rid in RECIPE_ORDER if not await get_flag(f"wsr:{rid}")]
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
                                                    capacity=user["res_capacity"], weekly=weekly,
                                                    created_at=user["created_at"], now=now, disabled=disabled,
                                                    week_done=week_done, tools_level=tools_level,
                                                    team_mult=team_mult, in_team=user["team_id"] is not None,
                                                    drones={k: user[f"drones_{k}"] for k in ("guard", "attack", "spy")}))


async def handle_drone_buy(request: web.Request) -> web.Response:
    """🤖 Купить боевого дрона за монеты (монеты сгорают)."""
    from shared.workshop import WorkshopError, buy_drone
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("workshop", ctx.lang):
        return off
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                count = await buy_drone(conn, ctx.user_id, str(data.get("kind") or ""))
    except WorkshopError as e:
        return fail(e.localized(ctx.lang))
    return web.json_response({"ok": True, "count": count})


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
                res = await craft_weekly(conn, ctx.user_id, rid, utcnow(), to_storage=True)
    except WeeklyError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "craft_weekly", recipe=rid, source="webapp")
    stored = any(e["type"] in ITEM_COLUMNS for e in WEEKLY_RECIPES[rid]["effects"])
    return web.json_response({"ok": True, "left": res["left"], "stored": stored})


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
        # 🏆 Рейтинг друзей — сезонный (27.10): считаются друзья, приглашённые или ставшие
        # активными в этом месяце; личная статистика выше — за всё время.
        start, end = season_bounds(now)
        rows = await conn.fetch(
            """SELECT r.user_id, r.username, r.display_name, r.created_at,
                      COUNT(*) FILTER (WHERE u.qualified_at >= $2 AND u.qualified_at < $3) AS qualified,
                      COUNT(*) FILTER (WHERE u.created_at >= $2 AND u.created_at < $3) AS invited
               FROM users u JOIN users r ON r.user_id = u.referred_by
               WHERE NOT r.is_blocked AND r.deleted_at IS NULL AND r.deletion_requested_at IS NULL
                 AND ((u.created_at >= $2 AND u.created_at < $3) OR (u.qualified_at >= $2 AND u.qualified_at < $3))
               GROUP BY r.user_id
               ORDER BY qualified DESC, invited DESC, r.user_id ASC LIMIT $1""", REFERRAL_TOP_LIMIT, start, end)
    username = await _bot_name(request)
    link = f"https://t.me/{username}?start={ctx.user_id}" if username else ""
    return web.json_response({
        "link": link,
        "share_text": plain(t(ctx.lang, "ref.share_text")),
        "invited": int(stats["invited"]), "qualified": int(stats["qualified"]),
        "earned": int(earned),
        "rules": {"qualified": REFERRAL_QUALIFIED_BONUS, "reward": referral_reward_text(),
                  "level": REFERRAL_QUALIFY_QUIZ_LEVEL,
                  "claims": REFERRAL_QUALIFY_BONUS_CLAIMS},
        "season": season_key(now), "ends_at": end.isoformat(),
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
                result = await craft(conn, ctx.user_id, rid, utcnow(), to_storage=True)
    except WorkshopError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "craft", recipe=rid, source="webapp")
    return web.json_response({"ok": True, "effect": result.effect,
                              "until": result.until.isoformat() if result.until else None,
                              "level": result.level, "qty": result.qty, "stored": result.stored})


# ============================================================================
# 📦 Склад: ресурсы, котлеты, изделия мастерской (включаются кнопкой), постоянные улучшения
# ============================================================================
async def handle_storage(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    now = utcnow()
    async with db.pool.acquire() as conn:
        stock = await get_resources(conn, ctx.user_id)
        items = await list_items(conn, ctx.user_id)
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", ctx.user_id)
        team_fx = await _team_effects(conn, user["team_id"], now)
        stock = await get_resources(conn, ctx.user_id, ALL_KINDS)
    armor = armor_level_active(user["farm_armor_level"], user["armor_until"], now)
    iso = lambda v: v.isoformat() if v and v > now else None   # noqa: E731
    active = {e: iso(user[c]) for e, c in ITEM_COLUMNS.items()}
    active.update(thermos=iso(user["thermos_until"]), banner=iso(team_fx["banner"]), dome=iso(team_fx["dome"]))
    charges = {e: int(user[c]) for e, c in ONE_SHOT_COLUMNS.items()}
    return web.json_response({
        "stock": stock, "capacity": user["res_capacity"], "cutlets": user["inv_cutlets"],
        "items_count": sum(it["qty"] for it in items), "items_cap": items_capacity(user["res_capacity"]),
        "res_names": resource_labels(ctx.lang),
        "items": items, "effects": list(ITEM_EFFECTS), "active": active, "charges": charges,
        "in_team": user["team_id"] is not None,
        "kinds": list(ALL_KINDS),
        "stable": {"horses": user["horses"], "carts": user["carts"], "max_horses": MAX_HORSES,
                   "max_carts": MAX_CARTS,
                   "next_price": HORSE_PRICES[user["horses"]] if user["horses"] < MAX_HORSES else None,
                   "lots": market_lots(user["horses"], user["carts"], shuttle_active(user, now)),
                   "balance": user["balance"]},
        "shuttle": {"owned": bool(user["has_shuttle"]), "active": shuttle_active(user, now),
                    "until": iso(user["shuttle_until"]), "days": SHUTTLE_CHARGE_DAYS},
        "perm": {"shuttle": bool(user["has_shuttle"]), "shuttle_fee": SHUTTLE_MARKET_FEE_PERCENT,
                 "armor_level": armor, "armor_max": ARMOR_MAX_LEVEL, "armor_pct": ARMOR_BONUS_PER_LEVEL,
                 "armor_until": user["armor_until"].isoformat() if armor and user["armor_until"] else None,
                 "capacity": user["res_capacity"], "capacity_base": RES_CAPACITY_BASE,
                 "capacity_max": next_storage_level(user["res_capacity"]) is None},
        "drones": {k: user[f"drones_{k}"] for k in ("guard", "attack", "spy")},
    })


async def handle_item_use(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    effect, hours = str(data.get("effect", ""))[:16], _int(data.get("hours"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await activate_item(conn, ctx.user_id, effect, hours, utcnow())
    except ItemError as e:
        return fail(plain(e.localized(ctx.lang)))
    await track(ctx.user_id, "item_used", effect=effect, hours=hours, source="webapp")
    return web.json_response({"ok": True, "effect": effect, "charges": res["charges"],
                              "until": res["until"].isoformat() if res["until"] else None})


# ============================================================================
# 🔬 Лаборатория: инструменты и технологии; 🐎 конюшня; 🔋 заряд Шаттла
# ============================================================================
def _raid_err(e: RaidError, lang: str) -> str:
    if e.key == "raid.err_need_tech":
        return t(lang, "raid.err_need_tech", tech=TECHS[e.kwargs["tech"]]["icon"] + " " + t(lang, f"tech.{e.kwargs['tech']}"))
    return e.localized(lang)


def build_tech_payload(state: dict, stock: dict, now) -> dict:
    """Чистый сборщик витрины Лаборатории (юнит-тесты без aiohttp)."""
    tools = state["tools"]["level"]
    levels = {k: v["level"] for k, v in state.items()}
    techs = []
    for key in TECH_ORDER:
        level = state[key]["level"]
        nxt = level + 1 if level < TECHS[key]["max"] else None
        ready = next_tech_at(key, level, state[key]["updated_at"])
        cost = tech_cost(key, nxt) if nxt else {}
        tool = tech_tool_required(key, nxt) if nxt else 0
        wait = int((ready - now).total_seconds()) if ready and ready > now else 0
        gate = not (key == "science" and nxt) or science_gate_ok(levels, nxt)
        techs.append({"key": key, "icon": TECHS[key]["icon"], "level": level, "max": TECHS[key]["max"],
                      "next": nxt, "cost": cost, "tool": tool, "tool_ok": tools >= tool, "wait": wait,
                      "gate_ok": gate, "cooldown_days": tech_cooldown_days(key, nxt) if nxt else 0,
                      "affordable": bool(nxt) and gate and tools >= tool and not wait and can_afford(stock, cost)})
    nxt_tool = tools + 1 if tools < len(TOOL_COSTS) else None
    return {
        "tools": {"level": tools, "next": nxt_tool, "cost": TOOL_COSTS.get(nxt_tool, {}),
                  "affordable": bool(nxt_tool) and can_afford(stock, TOOL_COSTS.get(nxt_tool, {}))},
        "techs": techs, "stock": stock,
        "effects": {"attack": RAID_ATTACK_BONUS_PER_LEVEL, "defense": RAID_DEFENSE_PER_LEVEL,
                    "science": SCIENCE_PERCENT_PER_LEVEL, "comm": COMM_COOLDOWN_MINUTES_PER_LEVEL},
    }


async def handle_tech(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        state = await get_tech(conn, ctx.user_id)
        stock = await get_resources(conn, ctx.user_id, ALL_KINDS)
    payload = build_tech_payload(state, stock, utcnow())
    payload["res_names"] = resource_labels(ctx.lang)
    return web.json_response(payload)


async def _tech_call(request: web.Request, action) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await action(conn, ctx.user_id, data)
    except TechError as e:
        return fail(plain(e.localized(ctx.lang)))
    return web.json_response({"ok": True, **result})


async def handle_tech_up(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        tech = str(data.get("tech", ""))[:16]
        if tech == "tools":
            return {"tech": tech, "level": await upgrade_tools(conn, uid, utcnow())}
        return {"tech": tech, "level": await upgrade_tech(conn, uid, tech, utcnow())}
    return await _tech_call(request, action)


async def handle_horse_buy(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        return {"horses": await buy_horse(conn, uid)}
    return await _tech_call(request, action)


async def handle_shuttle_charge(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        return {"until": (await charge_shuttle(conn, uid, utcnow())).isoformat()}
    return await _tech_call(request, action)


async def _team_effects(conn, team_id, now) -> dict:
    """Действующие командные изделия: конец Знамени и Купола (None — не действуют)."""
    if team_id is None:
        return {"banner": None, "dome": None}
    dome = await conn.fetchval("SELECT dome_until FROM teams WHERE team_id = $1", team_id)
    banner = await conn.fetchval(
        "SELECT MAX(ends_at) FROM team_banners WHERE team_id = $1 AND starts_at <= $2", team_id, now)
    return {"banner": banner, "dome": dome}


# ============================================================================
# ⛏ Рудники: карта, битвы за рудники, свои рудники команды
# ============================================================================
_leaders_cache: dict[int, tuple[float, list]] = {}


async def _battle_leaders(conn, battle: dict, limit: int = 3) -> list[dict]:
    """ТОП текущей битвы по её правилам (зачёт, заявки на рудники); кэш 60 с — карту открывают часто."""
    from shared.battles import battle_standings, is_manual
    if is_manual(battle["nomination_key"]) or battle["starts_at"] > utcnow():
        return []
    key = (battle["battle_id"], limit)
    hit = _leaders_cache.get(key)
    if hit and time.monotonic() - hit[0] < 60:
        return hit[1]
    live = {**battle, "ends_at": min(battle["ends_at"], utcnow())}
    rows = await battle_standings(conn, _Row(live), limit=limit)
    top = [{"id": r["id"], "name": html.unescape(str(r["name"])), "score": r["score"], "is_clan": r["is_clan"]}
           for r in rows]
    _leaders_cache[key] = (time.monotonic(), top)
    return top


class _Row(dict):
    """dict с .keys()/[] как у asyncpg.Record — для battle_standings на «живом» окне."""


async def _entry_info(conn, battle: dict, team_id: int | None, is_clan: bool) -> dict | None:
    """Заявка моей команды на битву за рудники: внесено/нужно батареек."""
    from shared.battles import battery_fee, battle_mines
    if team_id is None or not battle_mines(_Row(battle)) or (battle.get("scope") or "teams") == "solo":
        return None
    scope = battle.get("scope") or "teams"
    if (scope == "team" and is_clan) or (scope == "clan" and not is_clan):
        return {"allowed": False}
    have = await conn.fetchval("SELECT batteries FROM battle_entries WHERE battle_id = $1 AND team_id = $2",
                               battle["battle_id"], team_id) or 0
    fee = battery_fee(is_clan)
    return {"allowed": True, "batteries": int(have), "fee": fee, "registered": have >= fee}


async def handle_mines(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("mines", ctx.lang):
        return off
    now = utcnow()
    async with db.pool.acquire() as conn:
        me = await conn.fetchrow("SELECT u.team_id, t.max_members FROM users u LEFT JOIN teams t "
                                 "ON t.team_id = u.team_id WHERE u.user_id = $1", ctx.user_id)
        team_id = me["team_id"] if me else None
        is_clan = bool(me and (me["max_members"] or 0) >= 1000)
        batteries = (await get_resources(conn, ctx.user_id, ("battery",)))["battery"]
        mines = await list_mines(conn)
        battles = await mine_battles(conn)
        for b in battles:
            b["leaders"] = await _battle_leaders(conn, b)
            b["entry"] = await _entry_info(conn, b, team_id, is_clan)
        my_mines = []
        for m in mines:
            if team_id is not None and m["team_id"] == team_id and m["captured_until"] and m["captured_until"] > now:
                mined = await conn.fetchval(
                    "SELECT COALESCE(SUM(delta), 0) FROM resource_ledger WHERE reason = $1 AND kind = $2 "
                    "AND created_at >= $3", f"mine:{m['id']}", m["kind"], m["captured_at"])
                my_mines.append({"id": m["id"], "kind": m["kind"], "mined": int(mined),
                                 "captured_at": m["captured_at"].isoformat(), "until": m["captured_until"].isoformat()})
    target = {mid: b["battle_id"] for b in battles for mid in (b["mine_ids"] or [])}
    place_of = {mid: i for b in battles for i, mid in enumerate(b["mine_ids"] or [], start=1)}
    out, my_income = [], 0
    for m in mines:
        held = m["team_id"] is not None and m["captured_until"] and m["captured_until"] > now
        mine = held and m["team_id"] == team_id
        if mine:
            my_income += (m["members_count"] or 0) * MINE_YIELD_PER_MEMBER_HOUR
        out.append({
            "id": m["id"], "kind": m["kind"], "target": target.get(m["id"]), "place": place_of.get(m["id"]),
            "team": ({"name": html.unescape(m["team_name"] or ""), "symbol": html.unescape(m["team_symbol"] or ""),
                      "members": m["members_count"] or 0} if held else None),
            "until": m["captured_until"].isoformat() if held else None, "mine": bool(mine),
        })
    return web.json_response({
        "mines": out, "in_team": team_id is not None, "my_income": my_income, "my_mines": my_mines,
        "hold_hours": MINE_HOLD_HOURS, "yield": MINE_YIELD_PER_MEMBER_HOUR,
        "res_names": resource_labels(ctx.lang), "batteries": batteries,
        "fee": {"team": BATTLE_BATTERY_FEE_TEAM, "clan": BATTLE_BATTERY_FEE_CLAN},
        "battles": [{"id": b["battle_id"], "title": b["title"], "nomination": _nom_text(ctx.lang, b),
                     "starts_at": b["starts_at"].isoformat(), "ends_at": b["ends_at"].isoformat(),
                     "mine_ids": list(b["mine_ids"] or []), "mine_id": (b["mine_ids"] or [None])[0],
                     "started": b["starts_at"] <= now, "entry": b["entry"],
                     "leaders": [{"name": x["name"], "score": x["score"], "mine": x["id"] == team_id}
                                 for x in b["leaders"]]} for b in battles],
    })


def _nom_text(lang: str, battle: dict) -> str:
    """Название номинации на языке игрока (свои формулировки владельца — как есть)."""
    from shared.battles import BATTLE_NOMINATIONS, MANUAL_NOMINATIONS
    key = battle["nomination_key"]
    if key in BATTLE_NOMINATIONS or key in MANUAL_NOMINATIONS:
        return t(lang, f"nom.{key}")
    return battle["nomination_text"]


async def handle_events(request: web.Request) -> web.Response:
    """🎯 Акции и битвы, идущие сейчас: зачёт, сроки, призы по местам, моё место, заявка на рудники."""
    from shared.battles import battle_mines, is_manual, prizes_by_place
    from shared.prizes import rewards_label
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    now = utcnow()
    out = []
    async with db.pool.acquire() as conn:
        me = await conn.fetchrow("SELECT u.team_id, t.max_members FROM users u LEFT JOIN teams t "
                                 "ON t.team_id = u.team_id WHERE u.user_id = $1", ctx.user_id)
        team_id = me["team_id"] if me else None
        is_clan = bool(me and (me["max_members"] or 0) >= 1000)
        rows = await conn.fetch("SELECT * FROM battles WHERE status = 'active' ORDER BY ends_at LIMIT 30")
        for r in rows:
            b = dict(r)
            scope = b["scope"] or "teams"
            leaders = await _battle_leaders(conn, b, limit=max(10, int(b["places"] or 0)))
            my_id = ctx.user_id if scope == "solo" else team_id
            my_place = next((i for i, x in enumerate(leaders, start=1) if x["id"] == my_id), 0)
            prizes = prizes_by_place(b["prizes"])
            out.append({
                "id": b["battle_id"], "title": b["title"], "scope": t(ctx.lang, f"post.scope_{scope}"),
                "solo": scope == "solo", "nomination": _nom_text(ctx.lang, b), "manual": is_manual(b["nomination_key"]),
                "starts_at": b["starts_at"].isoformat(), "ends_at": b["ends_at"].isoformat(),
                "started": b["starts_at"] <= now, "places": int(b["places"] or 0),
                "prizes": [{"place": p, "label": rewards_label(prizes[p])} for p in sorted(prizes)][:20],
                "mines": battle_mines(_Row(b)), "my_place": my_place,
                "leaders": [{"name": x["name"], "score": x["score"], "me": x["id"] == my_id} for x in leaders[:10]],
                "entry": await _entry_info(conn, b, team_id, is_clan),
            })
    return web.json_response({"events": out})


async def handle_battle_battery(request: web.Request) -> web.Response:
    """🔋 Внести батарейку в заявку своей команды на битву за рудники."""
    from shared.battles import BattleError, contribute_battery
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    battle_id = _int(data.get("battle_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await contribute_battery(conn, battle_id, ctx.user_id, utcnow())
    except BattleError as e:
        return fail(e.localized(ctx.lang))
    _leaders_cache.clear()
    return web.json_response(res)


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
        team_fx = await _team_effects(conn, user["team_id"], now)
        tech = await tech_levels(conn, ctx.user_id)
        batteries = (await get_resources(conn, ctx.user_id, ("battery",)))["battery"]
        forsage_qty = await conn.fetchval(
            "SELECT qty FROM user_items WHERE user_id = $1 AND effect = 'forsage' AND hours = 0", ctx.user_id) or 0
    # Щит = личный щит или Купол команды (берём более поздний конец)
    ends = [x for x in (user["raid_shield_until"], team_fx["dome"]) if x and x > now]
    shield_until = max(ends) if ends else None
    used = user["forsage_used_at"]
    iso = lambda v: v.isoformat() if v and v > now else None   # noqa: E731
    return web.json_response({
        "stock": stock,
        "res_names": resource_labels(ctx.lang),
        "cooldown_left": attack_cooldown_left(user["last_raid_at"], now, tech["comm"]),
        "tech": {k: tech[k] for k in ("comm", "scout", "attack", "defense")}, "batteries": batteries,
        "candidates": raid_candidates(tech["scout"]),
        "meds": iso(user["meds_until"]),
        "shield": {
            "active": shield_active(user, now, team_fx["dome"]),
            "dome": iso(team_fx["dome"]),
            "until": shield_until.isoformat() if shield_until and shield_until > now else None,
        },
        "stance": user["raid_stance"] if user["raid_stance"] in STANCES else None,
        "charges": {"economizer": int(user["raid_free_fuel"]), "cargo": int(user["raid_cargo"])},
        "guards": {"camo": iso(user["raid_camo_until"]), "trap": iso(user["raid_trap_until"]),
                   "drill": iso(user["raid_drill_until"])},
        "forsage": {"qty": int(forsage_qty),
                    "ready": used is None or used <= now - timedelta(hours=FORSAGE_COOLDOWN_HOURS)},
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
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():   # разведка тратит батарейку
                targets = await raid_scout(conn, ctx.user_id, now)
    except RaidError as e:
        return fail(plain(_raid_err(e, ctx.lang)))
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
            return fail(plain(_raid_err(e, ctx.lang)))
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
                              "name": display_name_of(defender)[:24], "revenge": result.is_revenge,
                              "notes": result.notes})


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
    team_scope = request.query.get("scope") == "team"
    now = utcnow()
    async with db.pool.acquire() as conn:
        team = await conn.fetchrow(
            "SELECT t.team_id, t.team_name, t.max_members FROM users u JOIN teams t ON t.team_id = u.team_id "
            "WHERE u.user_id = $1", ctx.user_id)
        if team_scope and team is None:
            return fail(plain(t(ctx.lang, "mk.err_no_team")))
        scope_team = team["team_id"] if team_scope else None   # None — общая биржа
        stats = await market_stats(conn, asset)
        asks = await list_open_orders(conn, MARKET_APP_LIST_LIMIT, exclude_user=ctx.user_id,
                                      asset=asset, side="sell", team_id=scope_team)
        bids = await list_open_orders(conn, MARKET_APP_LIST_LIMIT, exclude_user=ctx.user_id,
                                      asset=asset, side="buy", team_id=scope_team)
        mine = await my_open_orders(conn, ctx.user_id)
        user = await conn.fetchrow("SELECT inv_cutlets, balance, has_shuttle, shuttle_until, horses, carts "
                                   "FROM users WHERE user_id = $1", ctx.user_id)
        stock = await get_resources(conn, ctx.user_id, ALL_KINDS)
        history = await price_history(conn, asset, now)
        index = {}
        for a in MARKET_ASSETS:
            index[a] = index_change(history if a == asset else await price_history(conn, a, now))
        swaps = await list_swaps(conn, MARKET_APP_SWAPS_LIMIT, exclude_user=ctx.user_id, team_id=scope_team)
        my_sw = await my_swaps(conn, ctx.user_id)
    shuttle = shuttle_active(user, now)
    max_qty, _ = market_limits(shuttle, asset)
    max_orders = market_lots(user["horses"], user["carts"], shuttle)
    slim = lambda o: {"id": o["id"], "qty": o["qty"], "price": o["price"]}  # noqa: E731
    return web.json_response({
        "asset": asset,
        "stats": {"orders": stats["orders"], "qty": stats["qty"], "best_price": stats["best_price"],
                  "bids": stats["bids"], "best_bid": stats["best_bid"]},
        "asks": [slim(o) for o in asks], "bids": [slim(o) for o in bids],
        "my": [{"id": o["id"], "qty": o["qty"], "price": o["price"], "asset": o["asset"], "side": o["side"],
                "team": o["team"]} for o in mine],
        "scope": "team" if team_scope else "public",
        "team": ({"name": html.unescape(team["team_name"]), "fee": team_market_fee_percent(team["max_members"]),
                  "is_clan": team["max_members"] >= MEGA_CLAN_MAX_MEMBERS} if team else None),
        "have": user["inv_cutlets"] if asset == "cutlet" else stock[asset],
        "inv": user["inv_cutlets"], "stock": stock, "balance": user["balance"],
        "shuttle": shuttle,
        "fee": min(SHUTTLE_MARKET_FEE_PERCENT if shuttle else MARKET_FEE_PERCENT,
                   team_market_fee_percent(team["max_members"]) if team_scope else 100),
        "max_qty": max_qty, "max_orders": max_orders, "open_orders": len(mine),
        "lots": {"horses": user["horses"], "carts": user["carts"]}, "swap_kinds": list(TRADEABLE_KINDS),
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
                order_id = await place_order(conn, ctx.user_id, asset, side, qty, price,
                                             team_only=data.get("scope") == "team")
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
                                            _int(data.get("want_qty")), team_only=data.get("scope") == "team")
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
            # Без команды — тот же хаб, что в чате: рулетка свободных команд, поиск, создание
            balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
            return web.json_response({
                "team": None, "teams": await random_teams(conn), "cost": TEAM_CREATE_COST, "balance": balance,
                "limits": {"name": TEAM_NAME_MAX_LEN, "motto": TEAM_MOTTO_MAX_LEN, "symbol": TEAM_SYMBOL_MAX_LEN},
                "stock": stock, "res_names": resource_labels(ctx.lang)})
        team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1", user["team_id"])
        station = await get_station(conn, user["team_id"])
        feed = await recent_donations(conn, user["team_id"])
        # Состав виден только своим (как в чате) — @username или имя, 🧠 уровень, звание
        members = await team_members(conn, user["team_id"], team["captain_id"])
        now = utcnow()
        help_rows = await open_requests(conn, user["team_id"])
        given = await given_today(conn, ctx.user_id, now)
        giver_ok = await can_give(conn, ctx.user_id)
    station_on = await get_flag("station")
    level = station["level"]
    stored = {k: station[k] for k in RESOURCE_KINDS}
    return web.json_response({
        "team": {**public_team(team), "captain": team["captain_id"] == ctx.user_id,
                 "roster": [{"name": ("@" + m["username"]) if m.get("username")
                             else ((m.get("display_name") or "").strip() or "#" + str(m["user_id"])[-4:]),
                             "level": m["quiz_level"], "rank": rank_label(ctx.lang, m["created_at"], now),
                             "captain": m["user_id"] == team["captain_id"], "me": m["user_id"] == ctx.user_id}
                            for m in members]},
        "station": {
            "enabled": station_on, "level": level, "max": STATION_MAX_LEVEL,
            "per_level": STATION_BONUS_PER_LEVEL, "percent": level * STATION_BONUS_PER_LEVEL,
            "cost": station_level_cost(level + 1) if level < STATION_MAX_LEVEL else 0,
            "stored": stored, "need": progress_to_next(level, stored),
        },
        "help": {
            "requests": [{"id": h["id"], "name": _player_name(h), "kind": h["kind"], "qty": h["qty"],
                          "filled": h["filled"], "mine": h["user_id"] == ctx.user_id} for h in help_rows],
            "given_today": given, "daily": TEAM_HELP_DAILY_GIVE, "max_qty": TEAM_HELP_MAX_QTY,
            "can_give": giver_ok, "giver_level": TEAM_HELP_GIVER_MIN_QUIZ_LEVEL,
            "giver_claims": TEAM_HELP_GIVER_MIN_BONUS_CLAIMS,
        },
        "market": {"fee": team_market_fee_percent(team["max_members"]), "public_fee": MARKET_FEE_PERCENT,
                   "clan_fee": CLAN_MARKET_FEE_PERCENT},
        "feed": [{"name": ("@" + d["username"]) if d.get("username") else
                  ((d.get("display_name") or "").strip() or "#" + str(d["user_id"])[-4:]),
                  "kind": d["kind"], "qty": d["qty"]} for d in feed],
        "stock": stock,
        "res_names": resource_labels(ctx.lang),
    })


def _player_name(row) -> str:
    return ("@" + row["username"]) if row.get("username") else \
        ((row.get("display_name") or "").strip() or "#" + str(row["user_id"])[-4:])


async def _help_call(request: web.Request, action) -> web.Response:
    """Общая обёртка ручек взаимопомощи: авторизация, транзакция, ошибки на языке игрока."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await action(conn, ctx.user_id, data)
    except HelpError as e:
        return fail(plain(e.localized(ctx.lang)))
    return web.json_response({"ok": True, **(result or {})})


async def handle_help_request(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        return {"id": await request_help(conn, uid, str(data.get("kind", "")), _int(data.get("qty")))}
    return await _help_call(request, action)


async def handle_help_give(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        res = await give_help(conn, uid, _int(data.get("help_id")), _int(data.get("qty")), utcnow())
        await track(uid, "team_help_give", kind=res["kind"], qty=res["qty"], source="webapp")
        return {"qty": res["qty"], "kind": res["kind"], "done": res["done"]}
    return await _help_call(request, action)


async def handle_help_cancel(request: web.Request) -> web.Response:
    async def action(conn, uid, data):
        await cancel_help(conn, uid, _int(data.get("help_id")))
    return await _help_call(request, action)


async def handle_teams(request: web.Request) -> web.Response:
    """Рулетка (без q — новый случайный набор при каждом запросе) или поиск по названию."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    query = (request.query.get("q") or "").strip()
    try:
        async with db.pool.acquire() as conn:
            teams = await search_teams(conn, query) if query else await random_teams(conn)
    except TeamError as e:
        return fail(e.localized(ctx.lang))
    return web.json_response({"teams": teams, "query": query})


async def handle_team_join(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    team_id = _int((await _json(request)).get("team_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                team = await join_team(conn, ctx.user_id, team_id)
    except TeamError as e:
        return fail(e.localized(ctx.lang))
    await track(ctx.user_id, "team_joined", team_id=team_id, source="webapp")
    return web.json_response({"ok": True, "team": team})


async def handle_team_leave(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            left = await leave_team(conn, ctx.user_id)
    if left is None:
        return fail(plain(t(ctx.lang, "team.err_not_member")))
    return web.json_response({"ok": True, "outcome": left["outcome"]})


async def handle_team_create(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                team_id = await create_team(conn, ctx.user_id, str(data.get("name", "")),
                                            str(data.get("motto", "")), str(data.get("symbol", "")))
    except TeamError as e:
        return fail(plain(e.localized(ctx.lang)))
    await track(ctx.user_id, "team_joined", role="captain", source="webapp")
    return web.json_response({"ok": True, "team_id": team_id})


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
    app.router.add_post("/api/drone/buy", handle_drone_buy)
    app.router.add_post("/api/craft_weekly", handle_craft_weekly)
    app.router.add_get("/api/storage", handle_storage)
    app.router.add_get("/api/mines", handle_mines)
    app.router.add_get("/api/events", handle_events)
    app.router.add_post("/api/battle/battery", handle_battle_battery)
    app.router.add_get("/api/tech", handle_tech)
    app.router.add_post("/api/tech/up", handle_tech_up)
    app.router.add_post("/api/horse/buy", handle_horse_buy)
    app.router.add_post("/api/shuttle/charge", handle_shuttle_charge)
    app.router.add_post("/api/item/use", handle_item_use)
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
    app.router.add_get("/api/teams", handle_teams)
    app.router.add_post("/api/team/join", handle_team_join)
    app.router.add_post("/api/team/leave", handle_team_leave)
    app.router.add_post("/api/team/create", handle_team_create)
    app.router.add_post("/api/team/help", handle_help_request)
    app.router.add_post("/api/team/help/give", handle_help_give)
    app.router.add_post("/api/team/help/cancel", handle_help_cancel)
    app.router.add_post("/api/station/donate", handle_station_donate)
    app.router.add_get("/api/goals", handle_goals)
    app.router.add_post("/api/goals/claim", handle_goals_claim)
    app.router.add_post("/api/refuel", handle_refuel)
