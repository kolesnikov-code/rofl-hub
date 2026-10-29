"""
🎛 Пульт владельца — Mini App (решение 27.10): битвы и акции, призы, подарки, VIP-аукционы, тумблеры,
квесты (ротация до 10 + эпики) и ⚡ Безлимит игроку по @username.

Открывается из ГЛАВНОГО бота командой /admin (initData подписан его токеном), доступ — только ID из
переменной ADMIN_ID. Пульт лишь пишет в базу: игроки видят битвы, цели и лоты в приложении (Паспорт → События,
вкладка «Аукционы»), итоги по времени подводит демон админ-бота и пишет получившим награды в личку
(каналов нет — решение владельца 26.10). Тексты — по-русски.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

from aiohttp import web

from shared.database import db
from shared.economy import ALL_KINDS, ITEM_EFFECTS, MINE_HOLD_HOURS, finish_count_ok, utcnow
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
def form_title(data: dict) -> tuple[str, dict | None]:
    """Название из формы: заготовка (слово + слово + число → русская версия и шаблон) или свой текст."""
    from shared.titles import build_title, normalize_tpl
    tpl = normalize_tpl(data.get("title_tpl"))
    if tpl:
        return build_title("ru", tpl["a"], tpl["n"], tpl["num"]), tpl
    return str(data.get("title") or "").strip(), None


def validate_battle_form(data: dict, free_mines: set[int], now: datetime) -> tuple[dict | None, str | None]:
    """Проверяет форму пульта. Возвращает (поля для INSERT, None) или (None, текст ошибки)."""
    from shared.battles import BATTLE_NOMINATIONS, BATTLE_SCOPES, MANUAL_NOMINATIONS, MAX_BATTLE_PLACES
    from shared.prizes import normalize_rewards
    title, tpl = form_title(data)
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
    ends, err = end_time(data, starts, 24 * 365, "Длительность — от 1 часа до года")
    if err:
        return None, err
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
    reward_all = normalize_rewards(data.get("reward_all"))
    return {"title": title, "title_tpl": tpl, "scope": scope, "nomination_key": key, "reward_all": reward_all,
            "nomination_text": nom_text,
            "starts_at": starts, "ends_at": ends, "places": places,
            "prizes": prizes, "mine_ids": mines, "finish_count": finish_count_ok(data.get("finish_count"))}, None


def end_time(data: dict, start: datetime, max_hours: int, hours_err: str) -> tuple[datetime | None, str | None]:
    """⏱ Окончание: точная дата ends_at (UTC, из пульта) или start + hours. (момент, None) или (None, ошибка)."""
    raw = data.get("ends_at")
    if raw:
        try:
            ends = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            return None, "Неверная дата окончания"
        if ends.tzinfo is None:
            ends = ends.replace(tzinfo=timezone.utc)
        if ends <= start + timedelta(minutes=10):
            return None, "Окончание — хотя бы через 10 минут после старта"
        if ends > start + timedelta(hours=max_hours):
            return None, "Окончание слишком далеко"
        return ends, None
    hours = _int(data.get("hours"))
    if not 1 <= hours <= max_hours:
        return None, hours_err
    return start + timedelta(hours=hours), None


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
    from shared.titles import admin_options
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
        "flags": flags, "titles": admin_options(),
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
            "mine_ids": list(r["mine_ids"] or []), "announced": r["announced"], "finish_count": r["finish_count"],
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
                                    mine_ids, announced, results_posted, reward_all, title_tpl, finish_count)
               VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8, $9, TRUE, FALSE, $10::jsonb, $11::jsonb, $12)
               RETURNING battle_id""",
            form["title"], form["nomination_key"], form["nomination_text"], form["starts_at"], form["ends_at"],
            json.dumps(form["prizes"], ensure_ascii=False), form["scope"], form["places"], form["mine_ids"],
            json.dumps(form["reward_all"], ensure_ascii=False),
            json.dumps(form["title_tpl"]) if form["title_tpl"] else None, form["finish_count"])
    return web.json_response({"ok": True, "id": battle_id})


async def handle_admin_battle_close(request: web.Request) -> web.Response:
    """finish — подвести итоги сейчас (демон админ-бота выдаст призы и напишет победителям); cancel — отменить без призов."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    battle_id, mode = _int(data.get("id")), data.get("mode")
    async with db.pool.acquire() as conn:
        if mode == "cancel":
            from shared.battles import refund_entries
            done = await conn.fetchval("UPDATE battles SET status = 'cancelled' WHERE battle_id = $1 AND status = 'active' "
                                       "RETURNING 1", battle_id)
            if done:
                await refund_entries(conn, battle_id, only_incomplete=False)   # заявки батарейками — назад (аудит 1.7)
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


# ---------------------------------------------------------------- 🎁 «Подарить всем» — плашка в паспорте, без рассылки
async def handle_admin_gifts(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.gifts import campaigns_admin
    async with db.pool.acquire() as conn:
        return web.json_response({"ok": True, "campaigns": await campaigns_admin(conn)})


async def handle_admin_gift_all(request: web.Request) -> web.Response:
    """Раздача всем игрокам: подарок ждёт на плашке «Подарки от разработчика» до срока (по умолчанию — конец сезона)."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.economy import season_bounds
    from shared.gifts import create_campaign
    from shared.prizes import normalize_rewards
    data = await _body(request)
    rewards = [r for r in normalize_rewards(data.get("rewards")) if r["kind"] != "text"]
    if not rewards:
        return _fail("Добавь хотя бы одну награду (ручные призы раздачей не выдаются)")
    now = utcnow()
    days = _int(data.get("days"))
    expires = now + timedelta(days=days) if 1 <= days <= 90 else season_bounds(now)[1]
    title = str(data.get("title") or "").strip()[:100]
    async with db.pool.acquire() as conn:
        gift_id = await create_campaign(conn, title, rewards, expires)
    return web.json_response({"ok": True, "id": gift_id, "expires_at": expires.isoformat()})


async def handle_admin_gift_cancel(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.gifts import cancel
    async with db.pool.acquire() as conn:
        ok = await cancel(conn, _int((await _body(request)).get("id")))
    return web.json_response({"ok": ok}) if ok else _fail("Раздача не найдена или уже отменена")


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


def validate_lot_form(data: dict) -> tuple[dict | None, str | None]:
    """Свой лот аукциона (kind = lot): название, описание. Выдачу приза владелец делает сам."""
    title = str(data.get("title") or "").strip()
    if not 1 <= len(title) <= 100:
        return None, "Название лота — от 1 до 100 символов"
    return {"title": title, "descr": str(data.get("descr") or "").strip()[:500]}, None


async def handle_admin_vip_auction(request: web.Request) -> web.Response:
    """
    Аукцион: VIP ID (переходит победителю сам) или свой лот (kind = lot — приз вручает владелец).
    Монеты победителя сгорают (дефляция). Лот сразу виден во вкладке «Аукционы» приложения.
    """
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    price, step = _int(data.get("price")), _int(data.get("step"))
    lot = None
    alias = None
    if data.get("kind") == "lot":
        lot, err = validate_lot_form(data)
        if err:
            return _fail(err)
    else:
        alias = str(data.get("alias") or "").strip().upper()[:32]
        if not alias.startswith(VIP_PREFIX) or alias.isdigit():
            return _fail("VIP ID должен начинаться с ROFL-HUB-")
    if not 1 <= price <= 100_000_000 or not 1 <= step <= 10_000_000:
        return _fail("Цена и шаг — положительные числа")
    ends, err = end_time(data, utcnow(), AUCTION_MAX_HOURS, "Длительность — от 1 часа до 30 дней")
    if err:
        return _fail(err)
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("SELECT pg_advisory_xact_lock(271027)")
            if alias and alias in await _taken_aliases(conn):
                return _fail("Этот VIP ID уже занят или на аукционе")
            title = lot["title"] if lot else f"💎 VIP ID {alias}"
            descr = lot["descr"] if lot else "VIP ID — равноправный айдишник в экосистеме: переводы монет и строка в профиле."
            auction_id = await conn.fetchval(
                """INSERT INTO auctions (item_title, item_desc, current_price, min_step, status, vip_alias, ends_at, announced,
                                         finish_count)
                   VALUES ($1, $2, $3, $4, 'open', $5, $6, TRUE, $7) RETURNING auction_id""",
                title, descr, price, step, alias, ends, finish_count_ok(data.get("finish_count")))
    return web.json_response({"ok": True, "id": auction_id})


# ---------------------------------------------------------------- 🗺 экспедиции: цели на карте мира
EXP_ICONS = ("🎯", "💎", "☢️", "🏰", "🛸", "🗿", "🌋", "🧊", "🏝", "⚓", "🛰", "🐉")


def validate_target_form(data: dict, now: datetime, open_count: int) -> tuple[dict | None, str | None]:
    """Проверяет форму цели экспедиции. (поля для INSERT, None) или (None, текст ошибки)."""
    from shared.economy import EXP_FORKS_MAX, EXP_MAP_H, EXP_MAP_W, EXP_MAX_PLACES, EXP_MAX_TARGETS, EXP_SCOPES
    from shared.prizes import normalize_rewards
    if open_count >= EXP_MAX_TARGETS:
        return None, f"На карте уже {EXP_MAX_TARGETS} целей — закрой одну"
    title, tpl = form_title(data)
    if not 1 <= len(title) <= 100:
        return None, "Название — от 1 до 100 символов"
    descr = str(data.get("descr") or "").strip()[:500]
    icon = str(data.get("icon") or "🎯")[:8]
    scope = data.get("scope")
    if scope not in EXP_SCOPES:
        return None, "Выбери зачёт"
    try:
        x, y = float(data.get("x")), float(data.get("y"))
    except (TypeError, ValueError):
        return None, "Поставь цель на карте"
    if not (8 <= x <= EXP_MAP_W - 8 and 8 <= y <= EXP_MAP_H - 8):
        return None, "Цель — подальше от края карты"
    forks = _int(data.get("forks"), 3)
    if not 1 <= forks <= EXP_FORKS_MAX:
        return None, f"Развилок — от 1 до {EXP_FORKS_MAX}"
    resolve_at, err = end_time(data, now, 24 * 60, "Итоги — через 1 час … 60 дней")
    if err:
        return None, err
    places = _int(data.get("places"))
    if not 0 <= places <= EXP_MAX_PLACES:
        return None, f"Призовых мест — от 0 до {EXP_MAX_PLACES}"
    prizes = {}
    for p, items in (data.get("prizes") or {}).items() if isinstance(data.get("prizes"), dict) else []:
        p = _int(p)
        clean = normalize_rewards(items)
        if 1 <= p <= max(places, 1) and clean:
            prizes[str(p)] = clean
    reward_all = normalize_rewards(data.get("reward_all"))
    return {"title": title, "title_tpl": tpl, "descr": descr, "icon": icon, "scope": scope, "x": round(x, 1), "y": round(y, 1),
            "forks": forks, "resolve_at": resolve_at, "places": places, "prizes": prizes,
            "reward_all": reward_all, "finish_count": finish_count_ok(data.get("finish_count")),
            # 🧥/💠 «выдавать детали костюмов / артефакт» каждому дошедшему — только соло-походы (владелец 30.10)
            "give_gear": bool(data.get("give_gear")) and scope == "solo",
            "give_artifact": bool(data.get("give_artifact")) and scope == "solo"}, None


async def handle_admin_targets(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.battles import prizes_by_place
    from shared.economy import EXP_MAP_H, EXP_MAP_W, EXP_MAX_TARGETS
    from shared.prizes import normalize_rewards, rewards_label
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM expedition_targets ORDER BY (status = 'open') DESC, id DESC LIMIT 30")
        counts = {r["target_id"]: (r["n"], r["marching"]) for r in await conn.fetch(
            "SELECT target_id, COUNT(*) AS n, COUNT(*) FILTER (WHERE status = 'marching') AS marching "
            "FROM expeditions GROUP BY target_id")}
    out = []
    for r in rows:
        results = r["results"]
        results = json.loads(results) if isinstance(results, str) else (results or {})
        n, marching = counts.get(r["id"], (0, 0))
        prizes = prizes_by_place(r["prizes"])
        raw_all = r["reward_all"]
        reward_all = normalize_rewards(json.loads(raw_all) if isinstance(raw_all, str) else (raw_all or []))
        out.append({"id": r["id"], "title": r["title"], "icon": r["icon"], "x": r["x"], "y": r["y"], "scope": r["scope"],
                    "forks": r["forks"], "resolve_at": _iso(r["resolve_at"]), "places": r["places"],
                    "status": r["status"], "squads": n, "marching": marching, "finish_count": r["finish_count"],
                    "give_gear": r["give_gear"], "give_artifact": r["give_artifact"],
                    "prizes": [{"place": pl, "label": rewards_label(prizes[pl])} for pl in sorted(prizes)][:20],
                    "reward_all": rewards_label(reward_all) if reward_all else "",
                    "results": [{"place": x.get("place"), "name": x.get("name"), "cargo": x.get("cargo")}
                                for x in (results.get("places") or [])][:20]})
    return web.json_response({"targets": out, "map": {"w": EXP_MAP_W, "h": EXP_MAP_H}, "max": EXP_MAX_TARGETS,
                              "icons": list(EXP_ICONS)})


async def handle_admin_target_create(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("SELECT pg_advisory_xact_lock(281028)")
            open_count = await conn.fetchval("SELECT COUNT(*) FROM expedition_targets WHERE status = 'open'")
            form, err = validate_target_form(data, now, open_count)
            if err:
                return _fail(err)
            target_id = await conn.fetchval(
                """INSERT INTO expedition_targets (title, descr, icon, x, y, scope, forks, resolve_at, places, prizes,
                                                   reward_all, announced, title_tpl, finish_count, give_gear,
                                                   give_artifact)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::jsonb, $11::jsonb, TRUE, $12::jsonb, $13, $14, $15)
                   RETURNING id""",
                form["title"], form["descr"], form["icon"], form["x"], form["y"], form["scope"], form["forks"],
                form["resolve_at"], form["places"], json.dumps(form["prizes"], ensure_ascii=False),
                json.dumps(form["reward_all"], ensure_ascii=False),
                json.dumps(form["title_tpl"]) if form["title_tpl"] else None, form["finish_count"], form["give_gear"],
                form["give_artifact"])
    return web.json_response({"ok": True, "id": target_id})


async def handle_admin_target_close(request: web.Request) -> web.Response:
    """finish — итоги сейчас (демон админ-бота подведёт и напишет получившим награды); cancel — отменить, снаряжение вернуть."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    data = await _body(request)
    target_id, mode = _int(data.get("id")), data.get("mode")
    async with db.pool.acquire() as conn:
        if mode == "finish":
            # плановый час итогов запоминается: отряды в пути, успевавшие к нему, считаются дошедшими (аудит 1.1)
            done = await conn.fetchval("UPDATE expedition_targets SET planned_resolve_at = COALESCE(planned_resolve_at, "
                                       "resolve_at), resolve_at = LEAST(resolve_at, NOW()) "
                                       "WHERE id = $1 AND status = 'open' RETURNING 1", target_id)
        elif mode == "cancel":
            from shared.expeditions import cancel_target
            done = await cancel_target(conn, target_id)
        else:
            return _fail("Неизвестное действие")
    return web.json_response({"ok": True}) if done else _fail("Цель уже закрыта")


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


# ---------------------------------------------------------------- квесты и Безлимит (27.10)
async def handle_admin_quests(request: web.Request) -> web.Response:
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from bots.main_bot.utils.quest_loader import all_quests
    from shared import quest_engine as qe
    from shared.economy import QUEST_DAILY_NEW, QUEST_ROTATION_SIZE
    from shared.feature_flags import get_flag
    async with db.pool.acquire() as conn:
        stats = {r["quest_id"]: (r["started"], r["done"]) for r in await conn.fetch(
            "SELECT quest_id, COUNT(*) AS started, COUNT(*) FILTER (WHERE completed_at IS NOT NULL) AS done "
            "FROM quest_progress GROUP BY quest_id")}
    today = {q["id"] for q in await qe.visible_quests()}
    quests = [{"id": q["id"], "title": q["title"], "genre": q["genre"], "minutes": q["minutes"], "epic": qe.is_epic(q),
               "today": q["id"] in today and not qe.is_epic(q),
               "on": await get_flag(qe.flag_key(q)), "started": stats.get(q["id"], (0, 0))[0],
               "done": stats.get(q["id"], (0, 0))[1]} for q in all_quests()]
    return web.json_response({"ok": True, "quests": quests, "total": len(quests),
                              "rotation_size": QUEST_ROTATION_SIZE, "daily_new": QUEST_DAILY_NEW})


async def handle_admin_quest_toggle(request: web.Request) -> web.Response:
    """Эпик — показать/скрыть; обычный квест — в банке ротации дня или исключён."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from bots.main_bot.utils.quest_loader import get_quest
    from shared import quest_engine as qe
    from shared.feature_flags import set_flag
    data = await _body(request)
    quest = get_quest(str(data.get("id") or ""))
    if quest is None:
        return _fail("Квест не найден")
    enable = bool(data.get("enabled"))
    await set_flag(qe.flag_key(quest), enable)
    return web.json_response({"ok": True})


async def handle_admin_unlimit(request: web.Request) -> web.Response:
    """⚡ Безлимит игроку (ID / @username / VIP ID) на N дней; 0 — снять. Игроку — ЛС на его языке."""
    uid = _admin(request)
    if isinstance(uid, web.Response):
        return uid
    from shared.locales import resolve_lang, t
    from shared.rewards import grant_unlimit
    data = await _body(request)
    who, days = str(data.get("who") or "").strip(), _int(data.get("days"), -1)
    if not who or days < 0:
        return _fail("Укажи игрока и число дней")
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            res = await grant_unlimit(conn, who, days)
    if res is None:
        return _fail("Игрок не найден (он должен хотя бы раз нажать /start)")
    until = f"{res['until']:%d.%m.%Y %H:%M}" if res["until"] else None
    bot = request.app.get("bot")
    if bot is not None and until:
        try:
            await bot.send_message(res["user_id"], "🎁 " + t(resolve_lang(res["lang"]), "dlv.unlimit", until=until),
                                   parse_mode="HTML")
        except Exception:
            pass
    return web.json_response({"ok": True, "until": until})


def register_admin_routes(app: web.Application) -> None:
    app.router.add_get("/admin", handle_admin_page)
    app.router.add_get("/api/admin/meta", handle_admin_meta)
    app.router.add_get("/api/admin/battles", handle_admin_battles)
    app.router.add_post("/api/admin/battle", handle_admin_battle_create)
    app.router.add_post("/api/admin/battle/close", handle_admin_battle_close)
    app.router.add_post("/api/admin/battle/manual", handle_admin_battle_manual)
    app.router.add_post("/api/admin/reward", handle_admin_reward)
    app.router.add_get("/api/admin/gifts", handle_admin_gifts)
    app.router.add_post("/api/admin/gift_all", handle_admin_gift_all)
    app.router.add_post("/api/admin/gift_cancel", handle_admin_gift_cancel)
    app.router.add_get("/api/admin/vip", handle_admin_vip)
    app.router.add_post("/api/admin/vip/auction", handle_admin_vip_auction)
    app.router.add_post("/api/admin/flag", handle_admin_flag)
    app.router.add_get("/api/admin/quests", handle_admin_quests)
    app.router.add_post("/api/admin/quest", handle_admin_quest_toggle)
    app.router.add_post("/api/admin/unlimit", handle_admin_unlimit)
    app.router.add_get("/api/admin/targets", handle_admin_targets)
    app.router.add_post("/api/admin/target", handle_admin_target_create)
    app.router.add_post("/api/admin/target/close", handle_admin_target_close)
