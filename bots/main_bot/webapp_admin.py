"""
🎛 Пульт владельца — Mini App (решение 27.10): битвы и акции, призы, подарки, VIP-аукционы, тумблеры.

Открывается из ГЛАВНОГО бота командой /admin (initData подписан его токеном), доступ — только ID из
переменной ADMIN_ID. Пульт лишь пишет в базу: анонсы и итоги в канал публикует демон админ-бота
(битвы с announced = FALSE, аукционы с announced = FALSE, закрытие по ends_at). Тексты — по-русски.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

from aiohttp import web

from shared.database import db
from shared.economy import ALL_KINDS, ITEM_EFFECTS, MINE_HOLD_HOURS, utcnow
from shared.webapp_auth import validate_init_data

VIP_PREFIX = "ROFL-HUB-"
VIP_POOL = ("777", "888", "999", "100", "007", "001", "2026", "1000", "1111", "7777", "8888", "9999", "1337",
            "SHARK", "KING", "BOSS", "LEGEND", "TIGER", "WOLF", "DRAGON", "GHOST", "NINJA", "PHOENIX", "TITAN",
            "ROCKET", "CYBER", "ALPHA", "OMEGA", "GOLD", "DIAMOND", "STAR", "HERO", "CHAMP", "MASTER", "ACE")
AUCTION_MAX_HOURS = 24 * 30


def admin_ids() -> set[int]:
    raw = os.getenv("ADMIN_ID", "")
    return {int(x) for x in raw.replace(" ", "").split(",") if x.isdigit()}


def _admin(request: web.Request) -> int | web.Response:
    parsed = validate_init_data(request.headers.get("X-Telegram-Init-Data", ""), request.app["bot_token"])
    if not parsed or "user" not in parsed:
        return web.json_response({"error": "unauthorized"}, status=401)
    uid = int(parsed["user"]["id"])
    if uid not in admin_ids():
        return web.json_response({"error": "forbidden"}, status=403)
    return uid


def _fail(message: str, status: int = 400) -> web.Response:
    return web.json_response({"error": "bad_request", "message": message}, status=status)


async def _body(request: web.Request) -> dict:
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _int(v, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _iso(v):
    return v.isoformat() if isinstance(v, datetime) else v


# ---------------------------------------------------------------- проверка формы битвы (чистая)
def validate_battle_form(data: dict, free_mines: set[int], now: datetime) -> tuple[dict | None, str | None]:
    """Проверяет форму пульта. Возвращает (поля для INSERT, None) или (None, текст ошибки)."""
    from shared.battles import BATTLE_NOMINATIONS, BATTLE_SCOPES, MANUAL_NOMINATIONS, MAX_BATTLE_PLACES
    from shared.prizes import normalize_rewards
    title = str(data.get("title") or "").strip()
    if not 1 <= len(title) <= 100:
        return None, "Название — от 1 до 100 символов"
    scope = data.get("scope")
    if scope not in BATTLE_SCOPES:
        return None, "Выбери зачёт"
    key = data.get("nomination") or ""
    custom = str(data.get("custom") or "").strip()
    if key == "custom":
        if not 3 <= len(custom) <= 200:
            return None, "Своя номинация — от 3 до 200 символов"
        nom_text = custom
    elif key in BATTLE_NOMINATIONS:
        nom_text = BATTLE_NOMINATIONS[key]["title"]
    elif key in MANUAL_NOMINATIONS:
        nom_text = MANUAL_NOMINATIONS[key]
    else:
        return None, "Выбери номинацию"
    if key in MANUAL_NOMINATIONS and scope != "solo":
        return None, "Соцсети — личный зачёт"
    start_raw = data.get("starts_at")
    if not start_raw or start_raw == "now":
        starts = now
    else:
        try:
            starts = datetime.fromisoformat(str(start_raw).replace("Z", "+00:00"))
            if starts.tzinfo is None:
                starts = starts.replace(tzinfo=timezone.utc)
        except ValueError:
            return None, "Неверная дата старта"
    if starts < now - timedelta(minutes=10):
        return None, "Старт не может быть в прошлом"
    hours = _int(data.get("hours"))
    if not 1 <= hours <= 24 * 365:
        return None, "Длительность — от 1 часа до года"
    places = _int(data.get("places"))
    if not 0 <= places <= MAX_BATTLE_PLACES:
        return None, f"Призовых мест — от 0 до {MAX_BATTLE_PLACES}"
    prizes_raw = data.get("prizes") or {}
    prizes = {}
    if not isinstance(prizes_raw, dict):
        return None, "Призы — по местам"
    for p, items in prizes_raw.items():
        p = _int(p)
        if not 1 <= p <= max(places, 1):
            continue
        clean = normalize_rewards(items)
        if clean:
            prizes[str(p)] = clean
    mines = []
    for m in data.get("mine_ids") or []:
        m = _int(m)
        if m and m not in mines:
            mines.append(m)
    if mines and scope == "solo":
        return None, "Рудники — только в командном зачёте"
    if any(m not in free_mines for m in mines):
        return None, "Можно выбрать только свободные рудники"
    if len(mines) > max(places, 0) and places:
        return None, "Рудников не больше, чем призовых мест"
    places = max(places, len(mines))
    return {"title": title, "scope": scope, "nomination_key": key, "nomination_text": nom_text,
            "starts_at": starts, "ends_at": starts + timedelta(hours=hours), "places": places,
            "prizes": prizes, "mine_ids": mines}, None


def vip_candidates(taken: set[str], limit: int = 10, offset: int = 0) -> list[str]:
    """Свободные красивые VIP ID (не заняты игроками и не на открытых аукционах)."""
    free = [VIP_PREFIX + x for x in VIP_POOL if (VIP_PREFIX + x) not in taken]
    if not free:
        return []
    offset %= len(free)
    return (free[offset:] + free[:offset])[:limit]


# ---------------------------------------------------------------- страница и справочники
async def handle_admin_page(request: web.Request) -> web.Response:
    from bots.main_bot.webapp import WEBAPP_DIR
    return web.FileResponse(WEBAPP_DIR / "admin.html")


async def handle_admin_meta(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from bots.main_bot.webapp_game import resource_labels
    from shared.battles import BATTLE_NOMINATIONS, MANUAL_NOMINATIONS, battery_fee
    from shared.feature_flags import all_feature_flags
    from shared.mines import free_mine_ids, list_mines
    from shared.prizes import BOOST_COLUMNS, ROBOT_KINDS
    now = utcnow()
    async with db.pool.acquire() as conn:
        mines = await list_mines(conn)
        free = set(await free_mine_ids(conn, now))
    flags = await all_feature_flags()
    return web.json_response({
        "nominations": [{"key": k, "title": v["title"], "unit": v["unit"], "manual": False} for k, v in BATTLE_NOMINATIONS.items()]
        + [{"key": k, "title": v, "unit": "", "manual": True} for k, v in MANUAL_NOMINATIONS.items()],
        "resources": [{"key": k, "name": v} for k, v in resource_labels("ru").items() if k in ALL_KINDS],
        "items": list(ITEM_EFFECTS), "robots": list(ROBOT_KINDS), "boosts": list(BOOST_COLUMNS),
        "mines": [{"id": m["id"], "kind": m["kind"], "free": m["id"] in free,
                   "team": m["team_name"] if m["team_id"] and m["captured_until"] and m["captured_until"] > now else None,
                   "until": _iso(m["captured_until"]) if m["captured_until"] and m["captured_until"] > now else None}
                  for m in mines],
        "fee": {"team": battery_fee(False), "clan": battery_fee(True)}, "hold_hours": MINE_HOLD_HOURS,
        "flags": flags,
    })


# ---------------------------------------------------------------- битвы
async def handle_admin_battles(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM battles ORDER BY battle_id DESC LIMIT 40")
        entries = {(r["battle_id"], r["team_id"]): r["batteries"] for r in await conn.fetch(
            "SELECT battle_id, team_id, batteries FROM battle_entries WHERE battle_id = ANY($1::bigint[])",
            [r["battle_id"] for r in rows])}
    out = []
    for r in rows:
        results = r["results"]
        results = json.loads(results) if isinstance(results, str) else (results or {})
        out.append({
            "id": r["battle_id"], "title": r["title"], "status": r["status"], "scope": r["scope"],
            "nomination": r["nomination_text"], "nomination_key": r["nomination_key"],
            "starts_at": _iso(r["starts_at"]), "ends_at": _iso(r["ends_at"]), "places": r["places"],
            "mine_ids": list(r["mine_ids"] or []), "announced": r["announced"],
            "entries": sum(1 for (b, _), _v in entries.items() if b == r["battle_id"]),
            "manual_results": r["manual_results"] if not isinstance(r["manual_results"], str) else json.loads(r["manual_results"]),
            "results": [{"place": x.get("place"), "name": x.get("name"), "score": x.get("score")}
                        for x in (results.get("places") or [])][:20],
        })
    return web.json_response({"battles": out})


async def handle_admin_battle_create(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.mines import free_mine_ids
    data = await _body(request)
    now = utcnow()
    async with db.pool.acquire() as conn:
        free = set(await free_mine_ids(conn, now))
        form, err = validate_battle_form(data, free, now)
        if err:
            return _fail(err)
        battle_id = await conn.fetchval(
            """INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, prizes, scope, places,
                                    mine_ids, announced, results_posted)
               VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8, $9, FALSE, FALSE) RETURNING battle_id""",
            form["title"], form["nomination_key"], form["nomination_text"], form["starts_at"], form["ends_at"],
            json.dumps(form["prizes"], ensure_ascii=False), form["scope"], form["places"], form["mine_ids"])
    return web.json_response({"ok": True, "id": battle_id})


async def handle_admin_battle_close(request: web.Request) -> web.Response:
    """finish — подвести итоги сейчас (демон админ-бота опубликует их в канал); cancel — отменить без призов."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    battle_id, mode = _int(data.get("id")), data.get("mode")
    async with db.pool.acquire() as conn:
        if mode == "cancel":
            done = await conn.fetchval("UPDATE battles SET status = 'cancelled' WHERE battle_id = $1 AND status = 'active' "
                                       "RETURNING 1", battle_id)
        elif mode == "finish":
            done = await conn.fetchval("UPDATE battles SET ends_at = LEAST(ends_at, NOW()) WHERE battle_id = $1 "
                                       "AND status = 'active' RETURNING 1", battle_id)
        else:
            return _fail("Неизвестное действие")
    return web.json_response({"ok": bool(done)}) if done else _fail("Битва уже закрыта")


async def handle_admin_battle_manual(request: web.Request) -> web.Response:
    """Ручные итоги: {"id", "winners": {"1": "@user" | "ID" | "VIP" | "команда"}} — проверяются сразу."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.battles import resolve_manual_winner
    data = await _body(request)
    battle_id = _int(data.get("id"))
    winners = data.get("winners") or {}
    async with db.pool.acquire() as conn:
        battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1 AND status = 'active'", battle_id)
        if not battle:
            return _fail("Активная битва не найдена")
        clean, names = {}, {}
        for place, value in winners.items():
            place = _int(place)
            if not 1 <= place <= max(battle["places"], 1) or not str(value or "").strip():
                continue
            w = await resolve_manual_winner(conn, battle["scope"] or "teams", value)
            if not w:
                return _fail(f"{place} место: «{value}» не найден")
            clean[str(place)], names[str(place)] = str(value).strip(), w["name"]
        if not clean:
            return _fail("Впиши хотя бы одного победителя")
        await conn.execute("UPDATE battles SET manual_results = $2::jsonb WHERE battle_id = $1",
                           battle_id, json.dumps(clean, ensure_ascii=False))
    return web.json_response({"ok": True, "names": names})


# ---------------------------------------------------------------- подарки
async def handle_admin_reward(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.prizes import grant_many, normalize_rewards
    from shared.rewards import TARGETS, resolve_recipients
    data = await _body(request)
    target, value = data.get("target"), str(data.get("value") or "")
    rewards = normalize_rewards(data.get("rewards"))
    if target not in TARGETS:
        return _fail("Выбери, кому")
    if not rewards or all(r["kind"] == "text" for r in rewards):
        return _fail("Добавь хотя бы одну награду")
    now = utcnow()
    async with db.pool.acquire() as conn:
        ids, label = await resolve_recipients(conn, target, value)
        if not ids:
            return _fail(f"Получатели не найдены ({label})")
        if data.get("dry_run"):
            return web.json_response({"ok": True, "count": len(ids), "label": label})
        ok, bad = await grant_many(conn, ids, rewards, f"GIFT{now:%Y%m%d%H%M%S}", now)
    return web.json_response({"ok": True, "given": ok, "failed": bad, "label": label})


# ---------------------------------------------------------------- VIP ID и аукционы
async def _taken_aliases(conn) -> set[str]:
    rows = await conn.fetch("SELECT alias FROM vip_aliases UNION SELECT vip_alias FROM auctions "
                            "WHERE status = 'open' AND vip_alias IS NOT NULL")
    return {r["alias"] for r in rows}


async def handle_admin_vip(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    offset = _int(request.query.get("offset"))
    async with db.pool.acquire() as conn:
        taken = await _taken_aliases(conn)
        auctions = await conn.fetch("SELECT auction_id, item_title, vip_alias, current_price, highest_bidder_id, status, "
                                    "ends_at FROM auctions ORDER BY auction_id DESC LIMIT 15")
    return web.json_response({
        "free": vip_candidates(taken, 10, offset),
        "auctions": [{"id": a["auction_id"], "title": a["item_title"], "alias": a["vip_alias"], "price": a["current_price"],
                      "leader": a["highest_bidder_id"], "status": a["status"], "ends_at": _iso(a["ends_at"])}
                     for a in auctions],
    })


async def handle_admin_vip_auction(request: web.Request) -> web.Response:
    """Аукцион за VIP ID: монеты победителя сгорают (дефляция), ID переходит ему автоматически по окончании."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    alias = str(data.get("alias") or "").strip().upper()[:32]
    price, step, hours = _int(data.get("price")), _int(data.get("step")), _int(data.get("hours"))
    if not alias.startswith(VIP_PREFIX) or alias.isdigit():
        return _fail("VIP ID должен начинаться с ROFL-HUB-")
    if not 1 <= price <= 100_000_000 or not 1 <= step <= 10_000_000:
        return _fail("Цена и шаг — положительные числа")
    if not 1 <= hours <= AUCTION_MAX_HOURS:
        return _fail("Длительность — от 1 часа до 30 дней")
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("SELECT pg_advisory_xact_lock(271027)")
            if alias in await _taken_aliases(conn):
                return _fail("Этот VIP ID уже занят или на аукционе")
            auction_id = await conn.fetchval(
                """INSERT INTO auctions (item_title, item_desc, current_price, min_step, status, vip_alias, ends_at, announced)
                   VALUES ($1, $2, $3, $4, 'open', $5, NOW() + make_interval(hours => $6), FALSE) RETURNING auction_id""",
                f"💎 VIP ID {alias}", "VIP ID — равноправный айдишник в экосистеме: переводы монет и строка в профиле.",
                price, step, alias, hours)
    return web.json_response({"ok": True, "id": auction_id})


# ---------------------------------------------------------------- тумблеры
async def handle_admin_flag(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.feature_flags import FLAG_DEFAULTS, set_flag
    data = await _body(request)
    key = str(data.get("key") or "")
    if key not in FLAG_DEFAULTS and not key.startswith(("quest:", "wsr:", "recipe:")):
        return _fail("Неизвестный тумблер")
    await set_flag(key, bool(data.get("enabled")))
    return web.json_response({"ok": True})


def register_admin_routes(app: web.Application) -> None:
    app.router.add_get("/admin", handle_admin_page)
    app.router.add_get("/api/admin/meta", handle_admin_meta)
    app.router.add_get("/api/admin/battles", handle_admin_battles)
    app.router.add_post("/api/admin/battle", handle_admin_battle_create)
    app.router.add_post("/api/admin/battle/close", handle_admin_battle_close)
    app.router.add_post("/api/admin/battle/manual", handle_admin_battle_manual)
    app.router.add_post("/api/admin/reward", handle_admin_reward)
    app.router.add_get("/api/admin/vip", handle_admin_vip)
    app.router.add_post("/api/admin/vip/auction", handle_admin_vip_auction)
    app.router.add_post("/api/admin/flag", handle_admin_flag)
