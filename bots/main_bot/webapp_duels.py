"""
⚔️ Дуэли в приложении (шаг 3 плана 27.10). Та же очередь и те же столы, что в чате (shared/duels.py): игрок из
приложения может попасть на игрока из чата. Приложение опрашивает GET /api/duel раз в ~1,5 с (отметка присутствия —
duel_presence), ЛС шлём только тем, кто дуэль в приложении сейчас не смотрит. Соперник анонимен (как в чате).

API: GET /api/duel · POST /api/duel/join {stake} · /api/duel/move {duel_id, move} · /api/duel/cancel {duel_id}.
"""
from __future__ import annotations

from aiohttp import web

from bots.main_bot.duel_presence import mark_in_app
from bots.main_bot.handlers.duels import (_broadcast_round_result, _lang_of, notify_matched, start_round_watchdog)
from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared.database import db
from shared.duels import DuelError, active_duel_of, cancel_waiting_duel, join_or_create_duel, record_move
from shared.economy import (DUEL_BURN_PERCENT, DUEL_INVITE_TTL_HOURS, DUEL_MOVE_TIMEOUT_SECONDS, DUEL_RESOURCE_REWARD, DUEL_TABLES,
                            DUEL_WAITING_TTL_MINUTES, duel_payout, utcnow)
from shared.locales import t

RESULT_SHOW_SECONDS = 120     # итог последней дуэли приложение показывает, если она закончилась недавно


async def duel_state(conn, user_id: int) -> dict:
    now = utcnow()
    out = {"ok": True, "timeout": DUEL_MOVE_TIMEOUT_SECONDS, "ttl": DUEL_WAITING_TTL_MINUTES, "burn": DUEL_BURN_PERCENT,
           "balance": await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", user_id),
           "tables": [{"stake": s, "payout": duel_payout(s)[0], "stone": DUEL_RESOURCE_REWARD.get(s, 0)} for s in DUEL_TABLES],
           "duel": None, "last": None}
    d = await active_duel_of(conn, user_id)
    if d is not None:
        me1 = d["player1"] == user_id
        my_move, opp_move = (d["move1"], d["move2"]) if me1 else (d["move2"], d["move1"])
        info = {"id": d["duel_id"], "status": d["status"], "stake": d["stake"], "payout": duel_payout(d["stake"])[0],
                "round": d["rounds"], "my_move": my_move, "opp_moved": opp_move is not None}
        if d["status"] == "active" and d["round_started_at"]:
            info["left"] = max(0, DUEL_MOVE_TIMEOUT_SECONDS - int((now - d["round_started_at"]).total_seconds()))
        if d["status"] == "waiting":
            ttl = DUEL_INVITE_TTL_HOURS * 3600 if d["invite_code"] else DUEL_WAITING_TTL_MINUTES * 60
            info["waiting_left"] = max(0, ttl - int((now - d["created_at"]).total_seconds()))
            info["invite"] = d["invite_code"]      # приватный стол «вызов друга» — приложение покажет ссылку
        out["duel"] = info
        return out
    last = await conn.fetchrow(
        "SELECT * FROM duels WHERE (player1 = $1 OR player2 = $1) AND status IN ('finished', 'cancelled') "
        "AND finished_at > now() - make_interval(secs => $2) ORDER BY finished_at DESC LIMIT 1",
        user_id, RESULT_SHOW_SECONDS)
    if last is not None:
        if last["status"] == "cancelled":
            out["last"] = {"id": last["duel_id"], "cancelled": True, "stake": last["stake"]}
        else:
            me1 = last["player1"] == user_id
            payout, burned = duel_payout(last["stake"])
            out["last"] = {"id": last["duel_id"], "win": last["winner_id"] == user_id, "stake": last["stake"],
                           "my_move": last["move1"] if me1 else last["move2"],
                           "opp_move": last["move2"] if me1 else last["move1"],
                           "payout": payout, "burned": burned, "rounds": last["rounds"],
                           "stone": DUEL_RESOURCE_REWARD.get(last["stake"], 0)}
    return out


async def _state_response(user_id: int, request: web.Request | None = None) -> web.Response:
    async with db.pool.acquire() as conn:
        state = await duel_state(conn, user_id)
    duel = state.get("duel")
    if request is not None and duel and duel.get("invite"):
        from bots.main_bot.webapp_game import _bot_name
        username = await _bot_name(request)
        duel["link"] = f"https://t.me/{username}?start=duel_{duel['invite']}" if username else ""
    return web.json_response(state)


async def handle_duel(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    mark_in_app(ctx.user_id)
    return await _state_response(ctx.user_id, request)


async def handle_duel_join(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("duels", ctx.lang)) is not None:
        return off
    mark_in_app(ctx.user_id)
    stake = _int((await _json(request)).get("stake"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await join_or_create_duel(conn, ctx.user_id, stake)
            opp_lang = await _lang_of(conn, result.opponent_id) if result.matched else None
    except DuelError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    bot = request.app.get("bot")
    if result.matched and bot is not None:
        await notify_matched(bot, result.duel_id, result.opponent_id, opp_lang, stake)
        start_round_watchdog(bot, result.duel_id)   # без бота раунд доиграет глобальный жнец
    return await _state_response(ctx.user_id)


async def handle_duel_move(request: web.Request) -> web.Response:
    ctx = await _ctx(request)        # начатая дуэль доигрывается и при выключенном тумблере
    if isinstance(ctx, web.Response):
        return ctx
    mark_in_app(ctx.user_id)
    data = await _json(request)
    duel_id = _int(data.get("duel_id"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await record_move(conn, duel_id, ctx.user_id, str(data.get("move") or ""))
    except DuelError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    bot = request.app.get("bot")
    if not result.waiting_opponent and bot is not None:
        await _broadcast_round_result(bot, duel_id, result)   # сопернику из чата — ЛС; в приложении — не шлём
    return await _state_response(ctx.user_id)


async def handle_duel_cancel(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await cancel_waiting_duel(conn, _int((await _json(request)).get("duel_id")), ctx.user_id)
    except DuelError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    return await _state_response(ctx.user_id)


def register_duel_routes(app: web.Application) -> None:
    app.router.add_get("/api/duel", handle_duel)
    app.router.add_post("/api/duel/join", handle_duel_join)
    app.router.add_post("/api/duel/move", handle_duel_move)
    app.router.add_post("/api/duel/cancel", handle_duel_cancel)
