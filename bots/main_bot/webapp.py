"""
Веб-сервер Telegram Mini App: статика + JSON-API в одном процессе с ботом (aiohttp).

Аутентификация: каждый API-запрос несёт заголовок X-Telegram-Init-Data,
подпись проверяется shared/webapp_auth.validate_init_data (HMAC токена бота).
Вся экономика переиспользуется: открытие приложения прогоняет ленивый пересчёт
фермы точно так же, как команда /farm в чате.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

from aiohttp import web

from bots.main_bot.catalog import (CATALOG, CatalogError, SHOP_LAYOUT, build_order, item_button, item_title,
                                   shop_info)
from shared.analytics import notify_referrer_qualified, qualify_referral_if_due, track
from shared.database import db
from shared.economy import (
    armor_level_active,
    farm_bonus_percent,
    daily_bonus_seconds_left,
    is_active,
    miner_hourly_rate,
    quiz_answers_required,
    quiz_level_reward,
    utcnow,
)
from shared.farm_logic import apply_lazy_farm, farm_counts
from shared.locales import resolve_lang, t
from shared.ranks import rank_label
from shared.resources import get_resources
from shared.economy import ALL_KINDS, season_bounds, season_key
from shared.seasons import season_place, season_teams, season_top, user_badges
from shared.webapp_auth import validate_init_data

logger = logging.getLogger(__name__)

WEBAPP_DIR = Path(__file__).resolve().parents[2] / "static" / "webapp"


def fridge_levels(current: int) -> list[dict]:
    """Холодильники из каталога объёмом больше текущего: [{sku, capacity, stars}] по возрастанию."""
    items = [{"sku": sku, "capacity": it["capacity"], "stars": it["stars"]}
             for sku, it in CATALOG.items() if it["type"] == "fridge_upgrade" and it["capacity"] > current]
    return sorted(items, key=lambda x: x["capacity"])


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() if moment else None


def build_me_payload(user, miners, quiz_row, team_row, vip_aliases, now,
                     resources: dict | None = None, station_level: int = 0) -> dict:
    """Чистый сборщик ответа /api/me — на нём юнит-тесты без aiohttp."""
    counts = farm_counts(miners, now)
    nuclear = is_active(user["boost_nuclear_until"], now)
    nitrogen = is_active(user["boost_nitrogen_until"], now)
    armor = armor_level_active(user["farm_armor_level"], user["armor_until"], now)
    bonus = farm_bonus_percent(armor, station_level)
    junior_rate = miner_hourly_rate("junior", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                    bonus_percent=bonus)
    premium_rate = miner_hourly_rate("premium", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                     bonus_percent=bonus)
    intern_rate = miner_hourly_rate("intern", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                    bonus_percent=bonus)
    speed_hour = (counts["intern"] * intern_rate + counts["junior"] * junior_rate
                  + counts["premium_fueled"] * premium_rate)
    lang = resolve_lang(user["lang"])

    quiz_level = quiz_row["quiz_level"] if quiz_row else 0
    quiz_progress = quiz_row["quiz_level_progress"] if quiz_row else 0
    next_level = quiz_level + 1
    alive = [m for m in miners if m.expires_at > now]

    return {
        "user_id": user["user_id"],
        "lang": lang,
        "display_name": user["display_name"] or user["username"] or f"ID {user['user_id']}",
        "balance": user["balance"],
        "rank": rank_label(lang, user["created_at"], now),
        "vip_aliases": list(vip_aliases),
        "resources": dict(resources or {}),
        "armor_level": armor,
        "armor_until": _iso(user["armor_until"]) if armor else None,
        "has_shuttle": bool(user["has_shuttle"]),
        "station_level": station_level,
        "res_capacity": user["res_capacity"],
        "bonus_percent": bonus,
        "quiz": {
            "level": quiz_level,
            "progress": quiz_progress,
            "required": quiz_answers_required(next_level),
            "next_level": next_level,
            "next_reward": quiz_level_reward(next_level),
        },
        "farm": {
            "intern": counts["intern"],
            "intern_claimed": bool(user["intern_claimed"]),
            "interns_pending": int(user["interns_pending"]),
            "junior": counts["junior"],
            "premium": counts["premium"],
            "premium_fueled": counts["premium_fueled"],
            "speed_hour": speed_hour,
            "rates": {"intern": intern_rate, "junior": junior_rate, "premium": premium_rate},
            "fridge": user["fridge_cutlets"],
            "fridge_capacity": user["fridge_capacity"],
            # Холодильники побольше текущего — мягкий намёк на расширение (вкладка «Ферма»)
            "fridge_levels": fridge_levels(user["fridge_capacity"]),
            "inv_cutlets": user["inv_cutlets"],
            "nearest_burnout": _iso(min(
                (m.expires_at for m in alive if m.kind != "intern"), default=None)),
            # Юниты для визуальной сцены фермы в Mini App (без ID — только тип и состояние)
            "units": [{
                "kind": m.kind,
                "fueled": m.kind != "premium" or (m.fuel_until is not None and m.fuel_until > now),
                "eternal": m.expires_at > now + timedelta(days=3650),
            } for m in alive],
            "bonus_seconds_left": daily_bonus_seconds_left(user["last_bonus_claim_at"], now),
            "boosts": {
                "nuclear_until": _iso(user["boost_nuclear_until"]) if nuclear else None,
                "nitrogen_until": _iso(user["boost_nitrogen_until"]) if nitrogen else None,
                "drone_until": _iso(user["drone_until"])
                if is_active(user["drone_until"], now) else None,
            },
        },
        "team": dict(team_row) if team_row else None,
    }


async def _auth_user_id(request: web.Request) -> int | None:
    """Проверяет initData из заголовка; возвращает telegram id или None."""
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    parsed = validate_init_data(init_data, request.app["bot_token"])
    if not parsed or "user" not in parsed:
        return None
    return int(parsed["user"]["id"])


def _unauthorized() -> web.Response:
    return web.json_response({"error": "unauthorized"}, status=401)


async def handle_index(request: web.Request) -> web.Response:
    return web.FileResponse(WEBAPP_DIR / "index.html")


async def handle_faq(request: web.Request) -> web.Response:
    """Полный справочник экосистемы — публичная страница без авторизации."""
    return web.FileResponse(WEBAPP_DIR / "faq.html")


async def handle_rules(request: web.Request) -> web.Response:
    """Пользовательское соглашение — публичная страница без авторизации."""
    return web.FileResponse(WEBAPP_DIR / "rules.html")


async def handle_me(request: web.Request) -> web.Response:
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()

    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, miners = await apply_lazy_farm(conn, user_id, now)
            if not user or user["deleted_at"] is not None:
                return web.json_response({"error": "no_profile"}, status=404)
            if user["is_blocked"]:
                return web.json_response({"error": "blocked"}, status=403)
            if user["deletion_requested_at"] is not None:
                return web.json_response({"error": "deleting"}, status=403)
            quiz_row = await conn.fetchrow(
                "SELECT quiz_level, quiz_level_progress FROM game_stats WHERE user_id = $1", user_id)
            team_row = None
            if user["team_id"] is not None:
                team_row = await conn.fetchrow(
                    "SELECT team_name, members_count, max_members, "
                    "(max_members >= 1000) AS is_clan, (captain_id = $2) AS i_am_captain "
                    "FROM teams WHERE team_id = $1", user["team_id"], user_id)
            vip = [r["alias"] for r in await conn.fetch(
                "SELECT alias FROM vip_aliases WHERE user_id = $1 ORDER BY created_at", user_id)]
            resources = await get_resources(conn, user_id, ALL_KINDS)
            badges = await user_badges(conn, user_id)
            station_level = 0
            if user["team_id"] is not None:
                station_level = await conn.fetchval(
                    "SELECT level FROM team_stations WHERE team_id = $1", user["team_id"]) or 0

    payload = build_me_payload(user, miners, quiz_row, team_row, vip, now,
                               resources=resources, station_level=station_level)
    # Какие разделы включены в пульте — выключенные вкладки приложение прячет
    from shared.feature_flags import all_feature_flags
    payload["features"] = await all_feature_flags()
    payload["badges"] = badges   # 🏅 значки сезонов: [{season, place}]
    return web.json_response(payload)


async def handle_bonus(request: web.Request) -> web.Response:
    """Ежедневная котлета — та же логика и кулдаун, что у кнопки в /farm."""
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()

    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow(
                "SELECT last_bonus_claim_at, is_blocked FROM users WHERE user_id = $1 FOR UPDATE",
                user_id)
            if not user:
                return web.json_response({"error": "no_profile"}, status=404)
            if user["is_blocked"]:
                return web.json_response({"error": "blocked"}, status=403)
            seconds_left = daily_bonus_seconds_left(user["last_bonus_claim_at"], now)
            if seconds_left > 0:
                return web.json_response({"ok": False, "seconds_left": seconds_left})
            await conn.execute(
                "UPDATE users SET inv_cutlets = inv_cutlets + 1, last_bonus_claim_at = $2, "
                "bonus_claims = bonus_claims + 1 WHERE user_id = $1", user_id, now)
            # 3-я ежедневная котлета могла сделать игрока «активным другом» → +500 рефереру
            qualified_referrer = await qualify_referral_if_due(conn, user_id)
    await track(user_id, "bonus_claimed", source="webapp")
    await notify_referrer_qualified(request.app.get("bot"), qualified_referrer)
    return web.json_response({"ok": True, "seconds_left": 0})


def build_shop_payload(lang: str) -> dict:
    """Витрина магазина для Mini App: порядок и состав — строго как в чат-боте."""
    def items_of(category: str) -> list[dict]:
        result = []
        for row in SHOP_LAYOUT[category]:
            for sku in row:
                item = CATALOG[sku]
                result.append({"sku": sku, "label": item_button(item, lang), "stars": item["stars"]})
        return result

    return {"farm": items_of("farm"), "games": items_of("games"), "info": shop_info(lang)}


async def handle_shop(request: web.Request) -> web.Response:
    """Каталог магазина на языке игрока."""
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()
    async with db.pool.acquire() as conn:
        lang = await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", user_id)
    await track(user_id, "shop_opened", category="webapp")
    return web.json_response(build_shop_payload(resolve_lang(lang)))


async def handle_invoice(request: web.Request) -> web.Response:
    """Создание Stars-инвойса из Mini App. При выключенном магазине — 503."""
    from shared.feature_flags import get_flag
    if not await get_flag("shop"):
        return web.json_response({"error": "shop_disabled"}, status=503)
    return await _handle_invoice_impl(request)


async def _handle_invoice_impl(request: web.Request) -> web.Response:
    """
    Создаёт Stars-инвойс для покупки из Mini App (createInvoiceLink).
    Оплата и доставка идут через обычный платёжный контур бота:
    pre_checkout перепроверит заказ, successful_payment доставит товар.
    """
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()
    bot = request.app.get("bot")
    if bot is None:
        return web.json_response({"error": "payments_unavailable"}, status=503)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "bad_request"}, status=400)
    sku = str(data.get("sku", ""))[:64]

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT fridge_capacity, lang, is_blocked FROM users WHERE user_id = $1", user_id)
    if not user:
        return web.json_response({"error": "no_profile"}, status=404)
    if user["is_blocked"]:
        return web.json_response({"error": "blocked"}, status=403)
    lang = resolve_lang(user["lang"])

    try:
        order = build_order(sku, current_capacity=user["fridge_capacity"])
    except CatalogError as e:
        return web.json_response({"error": str(e)}, status=400)

    from aiogram.types import LabeledPrice
    title = item_title(order, lang)
    try:
        link = await bot.create_invoice_link(
            title=title,
            description=t(lang, "pay.invoice_desc"),
            payload=f"{order['sku']}:{order['stars']}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label=title, amount=order["stars"])],
        )
    except Exception:
        logger.exception("[WEBAPP_INVOICE] не удалось создать инвойс user=%s sku=%s", user_id, sku)
        return web.json_response({"error": "invoice_failed"}, status=502)
    logger.info("[WEBAPP_INVOICE] user=%s sku=%s stars=%s", user_id, order["sku"], order["stars"])
    return web.json_response({"link": link})


async def handle_intern(request: web.Request) -> web.Response:
    """Активация бесплатного Робота Стажёра из Mini App (та же логика, что кнопка в /farm)."""
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()
    from bots.main_bot.handlers.farm import activate_intern
    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, _ = await apply_lazy_farm(conn, user_id, now)
            if not user:
                return web.json_response({"error": "no_profile"}, status=404)
            if not user["intern_claimed"]:
                await activate_intern(conn, user_id, now)
            else:
                # Стажёры за уровни интеллекта забираются той же кнопкой
                from bots.main_bot.handlers.farm import claim_pending_intern
                if not await claim_pending_intern(conn, user_id, now):
                    return web.json_response({"ok": False, "error": "already"})
    await track(user_id, "intern_activated", source="webapp")
    return web.json_response({"ok": True})


async def handle_top(request: web.Request) -> web.Response:
    """ТОП-100: по умолчанию — сезон (заработано за месяц), ?mode=rich — по балансу."""
    viewer_id = await _auth_user_id(request)
    if viewer_id is None:
        return _unauthorized()
    now = utcnow()
    async with db.pool.acquire() as conn:
        viewer_lang = resolve_lang(await conn.fetchval(
            "SELECT lang FROM users WHERE user_id = $1", viewer_id))
        if request.query.get("mode") != "rich":
            rows = await season_top(conn, now)
            me_place = await season_place(conn, viewer_id, now)
            teams = await season_teams(conn, now)
            start, end = season_bounds(now)
            return web.json_response({
                "mode": "season", "season": season_key(now), "ends_at": end.isoformat(),
                "me": me_place,
                "top": [{"name": (f"@{r['username']}" if r["username"] else (r["display_name"] or f"ID {r['user_id']}")),
                         "earned": int(r["earned"]), "quiz_level": r["quiz_level"],
                         "rank": rank_label(viewer_lang, r["created_at"], now),
                         "me": r["user_id"] == viewer_id} for r in rows],
                "teams": [{"name": html.unescape(x["name"]), "points": x["points"]} for x in teams],
            })
        rows = await conn.fetch(
            """
            SELECT u.user_id, u.username, u.display_name, u.balance, u.created_at,
                   COALESCE(g.quiz_level, 0) AS quiz_level,
                   (SELECT STRING_AGG(alias, ', ') FROM vip_aliases v WHERE v.user_id = u.user_id) AS vip
            FROM users u
            LEFT JOIN game_stats g ON g.user_id = u.user_id
            WHERE NOT u.is_blocked AND u.deleted_at IS NULL AND u.deletion_requested_at IS NULL
            ORDER BY u.balance DESC, u.user_id ASC
            LIMIT 100
            """)
    top = [{
        "name": (f"@{r['username']}" if r["username"] else (r["display_name"] or f"ID {r['user_id']}")),
        "balance": r["balance"],
        "quiz_level": r["quiz_level"],
        "vip": r["vip"],
        "rank": rank_label(viewer_lang, r["created_at"], now),
    } for r in rows]
    return web.json_response({"top": top})


def create_webapp(bot_token: str, bot=None) -> web.Application:
    app = web.Application()
    app["bot_token"] = bot_token
    app["bot"] = bot  # aiogram Bot для createInvoiceLink (None — покупки из Mini App выключены)
    app.router.add_get("/", handle_index)
    app.router.add_get("/faq", handle_faq)
    app.router.add_get("/rules", handle_rules)
    app.router.add_get("/api/me", handle_me)
    app.router.add_post("/api/bonus", handle_bonus)
    app.router.add_post("/api/intern", handle_intern)
    app.router.add_get("/api/top", handle_top)
    app.router.add_get("/api/shop", handle_shop)
    app.router.add_post("/api/invoice", handle_invoice)
    app.router.add_get("/health", lambda r: web.json_response({"ok": True}))
    from bots.main_bot.webapp_admin import register_admin_routes
    register_admin_routes(app)   # 🎛 пульт владельца (/admin) — только ADMIN_ID
    # Игровые разделы приложения: мастерская, налёты, биржа, станция, цели, заправка
    from bots.main_bot.webapp_game import register_game_routes
    register_game_routes(app)
    from bots.main_bot.webapp_map import register_map_routes
    register_map_routes(app)     # 🗺 карта мира и экспедиции
    # Арты роботов для сцены фермы: img/robots/<kind>.png (арты владельца) или .svg (заглушки)
    app.router.add_static("/img", WEBAPP_DIR / "img")
    return app


async def start_webapp_server(bot_token: str, port: int, bot=None) -> web.AppRunner:
    runner = web.AppRunner(create_webapp(bot_token, bot))
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logger.info("Mini App сервер слушает порт %s", port)
    return runner
