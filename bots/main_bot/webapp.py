"""
Веб-сервер Telegram Mini App: статика + JSON-API в одном процессе с ботом (aiohttp).

Аутентификация: каждый API-запрос несёт заголовок X-Telegram-Init-Data,
подпись проверяется shared/webapp_auth.validate_init_data (HMAC токена бота).
Вся экономика переиспользуется: открытие приложения прогоняет ленивый пересчёт
фермы точно так же, как команда /farm в чате.
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from aiohttp import web

from shared.database import db
from shared.economy import (
    daily_bonus_seconds_left,
    is_active,
    miner_hourly_rate,
    quiz_answers_required,
    quiz_level_reward,
    utcnow,
)
from shared.farm_logic import apply_lazy_farm, farm_counts
from shared.locales import resolve_lang
from shared.webapp_auth import validate_init_data

logger = logging.getLogger(__name__)

WEBAPP_DIR = Path(__file__).resolve().parents[2] / "static" / "webapp"


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() if moment else None


def build_me_payload(user, miners, quiz_row, team_row, vip_aliases, now) -> dict:
    """Чистый сборщик ответа /api/me — на нём юнит-тесты без aiohttp."""
    counts = farm_counts(miners, now)
    nuclear = is_active(user["boost_nuclear_until"], now)
    nitrogen = is_active(user["boost_nitrogen_until"], now)
    junior_rate = miner_hourly_rate("junior", nuclear_active=nuclear, nitrogen_active=nitrogen)
    premium_rate = miner_hourly_rate("premium", nuclear_active=nuclear, nitrogen_active=nitrogen)
    speed_hour = counts["junior"] * junior_rate + counts["premium_fueled"] * premium_rate

    quiz_level = quiz_row["quiz_level"] if quiz_row else 0
    quiz_progress = quiz_row["quiz_level_progress"] if quiz_row else 0
    next_level = quiz_level + 1
    alive = [m for m in miners if m.expires_at > now]

    return {
        "user_id": user["user_id"],
        "lang": resolve_lang(user["lang"]),
        "display_name": user["display_name"] or user["username"] or f"ID {user['user_id']}",
        "balance": user["balance"],
        "vip_aliases": list(vip_aliases),
        "quiz": {
            "level": quiz_level,
            "progress": quiz_progress,
            "required": quiz_answers_required(next_level),
            "next_level": next_level,
            "next_reward": quiz_level_reward(next_level),
        },
        "farm": {
            "junior": counts["junior"],
            "premium": counts["premium"],
            "premium_fueled": counts["premium_fueled"],
            "speed_hour": speed_hour,
            "fridge": user["fridge_cutlets"],
            "fridge_capacity": user["fridge_capacity"],
            "inv_cutlets": user["inv_cutlets"],
            "nearest_burnout": _iso(min((m.expires_at for m in alive), default=None)),
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


async def handle_me(request: web.Request) -> web.Response:
    user_id = await _auth_user_id(request)
    if user_id is None:
        return _unauthorized()

    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, miners = await apply_lazy_farm(conn, user_id, now)
            if not user:
                return web.json_response({"error": "no_profile"}, status=404)
            if user["is_blocked"]:
                return web.json_response({"error": "blocked"}, status=403)
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

    return web.json_response(build_me_payload(user, miners, quiz_row, team_row, vip, now))


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
                "UPDATE users SET inv_cutlets = inv_cutlets + 1, last_bonus_claim_at = $2 "
                "WHERE user_id = $1", user_id, now)
    return web.json_response({"ok": True, "seconds_left": 0})


async def handle_top(request: web.Request) -> web.Response:
    """Топ-100 игроков по балансу (витрина богатства и интеллекта)."""
    if await _auth_user_id(request) is None:
        return _unauthorized()
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT u.user_id, u.username, u.display_name, u.balance,
                   COALESCE(g.quiz_level, 0) AS quiz_level,
                   (SELECT STRING_AGG(alias, ', ') FROM vip_aliases v WHERE v.user_id = u.user_id) AS vip
            FROM users u
            LEFT JOIN game_stats g ON g.user_id = u.user_id
            WHERE NOT u.is_blocked
            ORDER BY u.balance DESC, u.user_id ASC
            LIMIT 100
            """)
    top = [{
        "name": (f"@{r['username']}" if r["username"] else (r["display_name"] or f"ID {r['user_id']}")),
        "balance": r["balance"],
        "quiz_level": r["quiz_level"],
        "vip": r["vip"],
    } for r in rows]
    return web.json_response({"top": top})


def create_webapp(bot_token: str) -> web.Application:
    app = web.Application()
    app["bot_token"] = bot_token
    app.router.add_get("/", handle_index)
    app.router.add_get("/faq", handle_faq)
    app.router.add_get("/api/me", handle_me)
    app.router.add_post("/api/bonus", handle_bonus)
    app.router.add_get("/api/top", handle_top)
    app.router.add_get("/health", lambda r: web.json_response({"ok": True}))
    return app


async def start_webapp_server(bot_token: str, port: int) -> web.AppRunner:
    runner = web.AppRunner(create_webapp(bot_token))
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logger.info("Mini App сервер слушает порт %s", port)
    return runner
