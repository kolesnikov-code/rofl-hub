"""
🤝 Социальная волна приложения (решения владельца 27.10 после оценки экосистемы 9 агентами):

- 🧭 режим приложения: «🧩 Головоломки и истории» или «🌐 Вся экосистема» (POST /api/mode);
- 💸 перевод монет из приложения (раньше — только /transfer в чате): /api/transfer/preview, /api/transfer;
- ⚔️ вызов друга на дуэль по ссылке: /api/duel/invite (создать), GET /api/duel/invite?code= (кто зовёт),
  /api/duel/accept, /api/duel/decline — приватный стол ждёт именно друга (shared/duels.py);
- 🕵️ дело дня: GET /api/case, /api/case/clue, /api/case/accuse (shared/daily_case.py);
- 📸 карточка достижений: GET /api/card (все достижения игрока + реферальная ссылка), POST /api/card/upload
  (картинку рисует приложение, сервер держит её в памяти час и отдаёт по /card/<token>.png для «историй»);
- 🛡 отряд → команда: POST /api/team/upgrade.
"""
from __future__ import annotations

import base64
import logging
import secrets
import time

from aiohttp import web

from bots.main_bot.handlers.duels import _lang_of, notify_matched, start_round_watchdog
from bots.main_bot.handlers.transfer import _recipient_label, _resolve_recipient
from bots.main_bot.utils.quest_loader import all_quests
from bots.main_bot.webapp_game import _bot_name, _ctx, _feature_off, _int, _json, fail, plain
from shared import daily_case
from shared import quest_engine as qe
from shared.database import db
from shared.db_clans import TeamError, upgrade_squad
from shared.duels import (DuelError, accept_invite_duel, create_invite_duel, invite_info)
from shared.economy import (DUEL_INVITE_TTL_HOURS, SHARE_CARD_MAX_BYTES, SHARE_CARD_TTL_SECONDS,
                            TRANSFER_MIN_AMOUNT, TRANSFER_SENDER_MIN_BONUS_CLAIMS, TRANSFER_SENDER_MIN_QUIZ_LEVEL,
                            duel_payout, transfer_fee, utcnow)
from shared.locales import resolve_lang, t
from shared.ranks import rank_label
from shared.seasons import user_badges
from shared.transfers import TransferError, ensure_sender_active, is_active_account, transfer_coins

logger = logging.getLogger(__name__)

APP_MODES = ("puzzle", "full")


# ---------------------------------------------------------------- 🧭 режим
async def handle_mode(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    mode = str((await _json(request)).get("mode") or "")
    if mode not in APP_MODES:
        return fail("bad mode")
    async with db.pool.acquire() as conn:
        await conn.execute("UPDATE users SET app_mode = $2 WHERE user_id = $1", ctx.user_id, mode)
    return web.json_response({"ok": True, "mode": mode})


# ---------------------------------------------------------------- 💸 перевод монет
async def _transfer_check(conn, ctx, data):
    """(получатель, сумма) или текст ошибки на языке игрока."""
    raw, amount = str(data.get("to") or "").strip(), _int(data.get("amount"))
    if not raw:
        return None, plain(t(ctx.lang, "tr.not_found"))
    try:
        await ensure_sender_active(conn, ctx.user_id)
    except TransferError as e:
        return None, plain(e.localized(ctx.lang))
    rec = await _resolve_recipient(conn, raw)
    if rec is None:
        return None, plain(t(ctx.lang, "tr.not_found"))
    if rec["user_id"] == ctx.user_id:
        return None, plain(t(ctx.lang, "tr.self"))
    if rec["is_blocked"]:
        return None, plain(t(ctx.lang, "tr.blocked"))
    if amount < TRANSFER_MIN_AMOUNT:
        return None, plain(t(ctx.lang, "tr.min", min=TRANSFER_MIN_AMOUNT))
    balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
    if balance < amount:
        return None, plain(t(ctx.lang, "tr.insufficient", balance=balance))
    return (rec, amount), None


async def handle_transfer_info(request: web.Request) -> web.Response:
    """Условия перевода для вкладки «Друзья»: открыт ли отправителю, минимум, комиссия."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        active = await is_active_account(conn, ctx.user_id)
    return web.json_response({"ok": True, "active": active, "min": TRANSFER_MIN_AMOUNT,
                              "fee_percent": transfer_fee(100), "need_level": TRANSFER_SENDER_MIN_QUIZ_LEVEL,
                              "need_claims": TRANSFER_SENDER_MIN_BONUS_CLAIMS})


async def handle_transfer_preview(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("transfers", ctx.lang)) is not None:
        return off
    async with db.pool.acquire() as conn:
        res, err = await _transfer_check(conn, ctx, await _json(request))
    if err:
        return fail(err)
    rec, amount = res
    fee = transfer_fee(amount)
    return web.json_response({"ok": True, "to": plain(_recipient_label(rec)), "amount": amount, "fee": fee,
                              "received": amount - fee})


async def handle_transfer(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("transfers", ctx.lang)) is not None:
        return off
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            res, err = await _transfer_check(conn, ctx, data)
            if err:
                return fail(err)
            rec, amount = res
            async with conn.transaction():
                received, balance = await transfer_coins(conn, ctx.user_id, rec["user_id"], amount)
            rec_lang = resolve_lang(await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", rec["user_id"]))
    except TransferError as e:
        return fail(plain(e.localized(ctx.lang)))
    bot = request.app.get("bot")
    if bot is not None:
        try:
            await bot.send_message(rec["user_id"], t(rec_lang, "tr.received", amount=received, sender_id=ctx.user_id),
                                   parse_mode="HTML")
        except Exception:
            logger.info("[TRANSFER] получатель %s недоступен для уведомления", rec["user_id"])
    return web.json_response({"ok": True, "received": received, "balance": balance, "to": plain(_recipient_label(rec))})


# ---------------------------------------------------------------- ⚔️ вызов друга по ссылке
async def _invite_link(request, code: str) -> str:
    username = await _bot_name(request)
    return f"https://t.me/{username}?start=duel_{code}" if username else ""


async def handle_duel_invite_create(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("duels", ctx.lang)) is not None:
        return off
    stake = _int((await _json(request)).get("stake"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                duel_id, code = await create_invite_duel(conn, ctx.user_id, stake)
    except DuelError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    return web.json_response({"ok": True, "duel_id": duel_id, "code": code, "stake": stake,
                              "link": await _invite_link(request, code), "hours": DUEL_INVITE_TTL_HOURS})


async def handle_duel_invite_info(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    code = (request.query.get("code") or "").strip().lower()
    async with db.pool.acquire() as conn:
        inv = await invite_info(conn, code)
    if inv is None:
        return web.json_response({"ok": False, "gone": True, "message": t(ctx.lang, "duel.invite_gone")})
    payout, _ = duel_payout(inv["stake"])
    return web.json_response({"ok": True, "code": code, "stake": inv["stake"], "payout": payout,
                              "from": "@" + inv["username"] if inv["username"] else (inv["display_name"] or "?"),
                              "mine": inv["player1"] == ctx.user_id})


async def handle_duel_accept(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("duels", ctx.lang)) is not None:
        return off
    code = str((await _json(request)).get("code") or "").strip().lower()
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await accept_invite_duel(conn, ctx.user_id, code)
            stake = await conn.fetchval("SELECT stake FROM duels WHERE duel_id = $1", result.duel_id)
            opp_lang = await _lang_of(conn, result.opponent_id)
    except DuelError as e:
        return fail(t(ctx.lang, e.key, **e.kwargs))
    bot = request.app.get("bot")
    if bot is not None:
        await notify_matched(bot, result.duel_id, result.opponent_id, opp_lang, stake)   # тому, кто звал
        start_round_watchdog(bot, result.duel_id)
    return web.json_response({"ok": True, "duel_id": result.duel_id})


async def handle_duel_decline(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    async with db.pool.acquire() as conn:
        await conn.execute("UPDATE users SET pending_duel = NULL WHERE user_id = $1", ctx.user_id)
    return web.json_response({"ok": True})


# ---------------------------------------------------------------- 🕵️ дело дня
async def _case_response(request, ctx, extra: dict | None = None) -> web.Response:
    async with db.pool.acquire() as conn:
        payload = await daily_case.case_payload(conn, ctx.user_id, ctx.lang)
    username = await _bot_name(request)
    payload["link"] = f"https://t.me/{username}?start={ctx.user_id}" if username else ""
    payload.update(extra or {})
    return web.json_response(payload)


async def handle_case(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("quests", ctx.lang)) is not None:
        return off
    return await _case_response(request, ctx)


async def handle_case_clue(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await daily_case.reveal_clue(conn, ctx.user_id)
    except daily_case.CaseError:
        pass   # дело уже закрыто — просто покажем итог
    return await _case_response(request, ctx)


async def handle_case_accuse(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    suspect = _int((await _json(request)).get("suspect"), -1)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await daily_case.accuse(conn, ctx.user_id, suspect)
            balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
    except daily_case.CaseError as e:
        if e.code == "bad":
            return fail("bad suspect")
        return await _case_response(request, ctx)
    return await _case_response(request, ctx, {"result": res, "balance": balance})


# ---------------------------------------------------------------- 📸 карточка достижений
_cards: dict[str, tuple[bytes, float, str]] = {}   # токен → (картинка, срок, тип)
CARD_TYPES = {b"\x89PNG": ("image/png", "png"), b"\xff\xd8\xff": ("image/jpeg", "jpg")}


def card_type(data: bytes) -> tuple[str, str] | None:
    """(content-type, расширение) по сигнатуре файла; не PNG и не JPEG — None."""
    return next((v for sig, v in CARD_TYPES.items() if data.startswith(sig)), None)


async def handle_card(request: web.Request) -> web.Response:
    """Все достижения игрока одним ответом — приложение рисует из них неоновую карточку."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    now = utcnow()
    epic_ids = [q["id"] for q in all_quests() if qe.is_epic(q)]
    async with db.pool.acquire() as conn:
        u = await conn.fetchrow("SELECT user_id, username, display_name, created_at, team_id FROM users WHERE user_id = $1",
                                ctx.user_id)
        level = await conn.fetchval("SELECT quiz_level FROM game_stats WHERE user_id = $1", ctx.user_id) or 0
        team = await conn.fetchrow("SELECT team_name, max_members FROM teams WHERE team_id = $1", u["team_id"]) \
            if u["team_id"] else None
        quests = await conn.fetchrow(
            "SELECT COUNT(*) FILTER (WHERE completed_at IS NOT NULL) AS done, "
            "COUNT(*) FILTER (WHERE completed_at IS NOT NULL AND quest_id = ANY($2::text[])) AS epics "
            "FROM quest_progress WHERE user_id = $1", ctx.user_id, epic_ids)
        duels_won = await conn.fetchval("SELECT COUNT(*) FROM duels WHERE winner_id = $1", ctx.user_id)
        wins = await conn.fetchval("SELECT COALESCE(SUM(wins_total), 0) FROM game_counters WHERE user_id = $1", ctx.user_id)
        cases = await conn.fetchval("SELECT COUNT(*) FROM daily_case_runs WHERE user_id = $1 AND solved", ctx.user_id)
        streak = await daily_case.streak(conn, ctx.user_id, now.date())
        friends = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1 AND qualified_at IS NOT NULL",
                                      ctx.user_id)
        robots = await conn.fetchval("SELECT COUNT(*) FROM miners WHERE user_id = $1 AND expires_at > $2", ctx.user_id, now)
        vip = [r["alias"] for r in await conn.fetch("SELECT alias FROM vip_aliases WHERE user_id = $1 ORDER BY created_at",
                                                    ctx.user_id)]
        badges = await user_badges(conn, ctx.user_id)
    username = await _bot_name(request)
    return web.json_response({
        "ok": True, "name": ("@" + u["username"]) if u["username"] else (u["display_name"] or ""),
        "rank": rank_label(ctx.lang, u["created_at"], now), "level": level, "vip": vip[0] if vip else None,
        "days": max(0, (now - u["created_at"]).days),
        "team": {"name": team["team_name"], "max": team["max_members"]} if team else None,
        "quests": int(quests["done"] or 0), "epics": int(quests["epics"] or 0), "duels": int(duels_won or 0),
        "wins": int(wins or 0), "cases": int(cases or 0), "case_streak": streak, "friends": int(friends or 0),
        "robots": int(robots or 0), "badges": badges,
        "link": f"https://t.me/{username}?start={ctx.user_id}" if username else "",
    })


def _clean_cards(now: float) -> None:
    for k in [k for k, (_, exp, _t) in _cards.items() if exp < now]:
        _cards.pop(k, None)


async def handle_card_upload(request: web.Request) -> web.Response:
    """PNG/JPEG от приложения → временная публичная ссылка (для Telegram Stories нужна картинка по адресу)."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    body = await _json(request)
    raw = str(body.get("image") or body.get("png") or "")
    if raw.startswith("data:image/") and "," in raw:
        raw = raw.split(",", 1)[1]
    try:
        data = base64.b64decode(raw, validate=True)
    except Exception:
        return fail("bad image")
    kind = card_type(data)
    if kind is None or len(data) > SHARE_CARD_MAX_BYTES:
        return fail("bad image")
    now = time.time()
    _clean_cards(now)
    for k in [k for k in _cards if k.startswith(f"{ctx.user_id}-")]:   # у игрока одна свежая карточка
        _cards.pop(k, None)
    token = f"{ctx.user_id}-{secrets.token_urlsafe(10)}"
    _cards[token] = (data, now + SHARE_CARD_TTL_SECONDS, kind[0])
    base = f"{request.scheme}://{request.host}"
    forwarded = request.headers.get("X-Forwarded-Proto")
    if forwarded:
        base = f"{forwarded}://{request.host}"
    return web.json_response({"ok": True, "url": f"{base}/card/{token}.{kind[1]}"})


async def handle_card_image(request: web.Request) -> web.Response:
    token = request.match_info["token"]
    item = _cards.get(token)
    if item is None or item[1] < time.time():
        raise web.HTTPNotFound()
    return web.Response(body=item[0], content_type=item[2], headers={"Cache-Control": "public, max-age=3600"})


# ---------------------------------------------------------------- 🛡 отряд → команда
async def handle_team_upgrade(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await upgrade_squad(conn, ctx.user_id)
    except TeamError as e:
        return fail(plain(e.localized(ctx.lang)))
    return web.json_response({"ok": True, **res})


def register_social_routes(app: web.Application) -> None:
    app.router.add_post("/api/mode", handle_mode)
    app.router.add_get("/api/transfer", handle_transfer_info)
    app.router.add_post("/api/transfer/preview", handle_transfer_preview)
    app.router.add_post("/api/transfer", handle_transfer)
    app.router.add_post("/api/duel/invite", handle_duel_invite_create)
    app.router.add_get("/api/duel/invite", handle_duel_invite_info)
    app.router.add_post("/api/duel/accept", handle_duel_accept)
    app.router.add_post("/api/duel/decline", handle_duel_decline)
    app.router.add_get("/api/case", handle_case)
    app.router.add_post("/api/case/clue", handle_case_clue)
    app.router.add_post("/api/case/accuse", handle_case_accuse)
    app.router.add_get("/api/card", handle_card)
    app.router.add_post("/api/card/upload", handle_card_upload)
    app.router.add_get(r"/card/{token:[0-9]+-[A-Za-z0-9_-]+}.{ext:png|jpg}", handle_card_image)
    app.router.add_post("/api/team/upgrade", handle_team_upgrade)
