"""
🗺 Карта мира в приложении (решение владельца 28.10): цели экспедиций, отряды в пути, развилки.

GET  /api/map        — цели, отряды на карте (маркеры движутся пропорционально пройденному времени),
                       мои отряды с текущей развилкой и голосами, время пути и «успеешь ли».
POST /api/exp/solo   — соло-вылазка; /api/exp/gear — внести 🔋/🥩 в отряд команды; /api/exp/vote — голос.
Механика — shared/expeditions.py; здесь только сборка ответа на языке игрока.
"""
from __future__ import annotations

import html
import json
import logging

from aiohttp import web

from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared.database import db
from shared.economy import (
    EXP_BATTERIES,
    EXP_CLAN_CUTLETS,
    EXP_MAP_H,
    EXP_MAP_W,
    EXP_SOLO_HYDROGEN,
    exp_mode_allowed,
    exp_travel_minutes,
    utcnow,
)
from shared.expedition_events import EVENTS_BY_ID, event_for, event_text
from shared.expeditions import (
    ExpError,
    contribute,
    current_fork,
    distance,
    fork_schedule,
    fork_window,
    gear_needed,
    origin_for,
    peek,
    peek_state,
    resolve_due_forks,
    squad_effects,
    squad_members,
    squad_mode,
    start_solo,
    vote,
)
from shared.locales import t
from shared.titles import localized_title

logger = logging.getLogger(__name__)
MAX_SQUADS_ON_MAP = 300


def _iso(v):
    return v.isoformat() if v else None


def _rewards(raw) -> list:
    from shared.prizes import normalize_rewards
    return normalize_rewards(json.loads(raw) if isinstance(raw, str) else (raw or []))


async def _resolve_overdue(conn, now) -> None:
    """Ленивая развязка развилок, до которых отряды уже дошли (выбор заранее или закрытое голосование)."""
    rows = await conn.fetch(
        """SELECT e.id, e.departed_at, e.planned_minutes, e.arrive_at, e.forks_done, t.forks
           FROM expeditions e JOIN expedition_targets t ON t.id = e.target_id
           WHERE e.status = 'marching' AND t.status = 'open' AND e.forks_done < t.forks
           ORDER BY e.id LIMIT 500""")
    for r in rows:
        open_at, _ = fork_schedule(r["departed_at"], r["planned_minutes"], r["forks"])[r["forks_done"]]
        if open_at <= now or open_at >= r["arrive_at"]:
            async with conn.transaction():
                await resolve_due_forks(conn, r["id"], now)


def _fork_payload(exp: dict, forks: int, now, lang: str, votes: list, my_id: int, peeked: list) -> dict | None:
    k = current_fork(exp, forks, now)
    if k is None:
        return None
    hint = k in peeked          # 🔎 последствия видны только у разведанной развилки
    event = event_for(exp["id"], k)
    open_at, close_at = fork_window(exp, forks, k)
    counts: dict[int, int] = {}
    mine = None
    for v in votes:
        if v["fork_no"] == k:
            counts[v["option"]] = counts.get(v["option"], 0) + 1
            if v["user_id"] == my_id:
                mine = v["option"]
    return {
        "no": k, "of": forks, "icon": event["icon"], "text": event_text(event["text"], lang), "peeked": hint,
        "opens_at": _iso(open_at), "closes_at": _iso(close_at), "reached": now >= open_at,
        "options": [{"i": i, "text": event_text(o["text"], lang), "votes": counts.get(i, 0), "mine": mine == i,
                     "hint": ({"cargo": o.get("cargo", 0), "loss": o.get("loss", 0), "delay": o.get("delay", 0),
                               "fight": bool(o.get("fight"))} if hint else None)}
                    for i, o in enumerate(event["options"])],
    }


def _log_payload(rows: list, lang: str) -> list:
    out = []
    for r in rows:
        event = EVENTS_BY_ID.get(r["event_id"])
        if not event:
            continue
        option = event["options"][r["option"]] if r["option"] < len(event["options"]) else None
        out.append({"no": r["fork_no"], "icon": event["icon"], "text": event_text(event["text"], lang),
                    "choice": event_text(option["text"], lang) if option else "—", "votes": r["votes"],
                    "cargo": r["cargo_delta"], "delay": r["delay_min"]})
    return out


async def handle_map(request: web.Request) -> web.Response:
    from shared.battles import prizes_by_place
    from shared.prizes import rewards_label
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("expeditions", ctx.lang):
        return off
    now = utcnow()
    async with db.pool.acquire() as conn:
        await _resolve_overdue(conn, now)
        me = await conn.fetchrow(
            "SELECT u.team_id, u.inv_cutlets, u.drones_guard, u.drones_attack, u.drones_spy, t.max_members, t.team_name "
            "FROM users u LEFT JOIN teams t ON t.team_id = u.team_id WHERE u.user_id = $1", ctx.user_id)
        team_id = me["team_id"]
        team_mode = squad_mode(me["max_members"]) if team_id else None
        stock = {r["kind"]: r["qty"] for r in await conn.fetch(
            "SELECT kind, qty FROM user_resources WHERE user_id = $1 AND kind IN ('hydrogen', 'battery')", ctx.user_id)}
        solo_eff = await squad_effects(conn, "solo", ctx.user_id, None)
        team_eff = await squad_effects(conn, team_mode, None, team_id) if team_id else None
        targets = await conn.fetch("SELECT * FROM expedition_targets WHERE status = 'open' ORDER BY resolve_at, id")
        target_ids = [r["id"] for r in targets]
        squads = await conn.fetch(
            """SELECT e.*, tm.team_name, tm.school_num FROM expeditions e LEFT JOIN teams tm ON tm.team_id = e.team_id
               WHERE e.target_id = ANY($1::int[]) AND e.status IN ('gathering', 'marching')
               ORDER BY e.id LIMIT $2""", target_ids, MAX_SQUADS_ON_MAP)
        my_rows = [s for s in squads if (s["mode"] == "solo" and s["user_id"] == ctx.user_id)
                   or (s["mode"] != "solo" and team_id is not None and s["team_id"] == team_id)]
        my_ids = [s["id"] for s in my_rows]
        votes = await conn.fetch("SELECT expedition_id, fork_no, user_id, option FROM expedition_votes "
                                 "WHERE expedition_id = ANY($1::bigint[])", my_ids)
        logs = await conn.fetch("SELECT * FROM expedition_log WHERE expedition_id = ANY($1::bigint[]) ORDER BY fork_no",
                                my_ids)
        peeks = {s["id"]: await peek_state(conn, s) for s in my_rows if s["status"] == "marching"}
        sizes = {s["id"]: len(await squad_members(conn, s)) for s in my_rows if s["mode"] != "solo"}
    by_target = {}
    for s in squads:
        by_target[s["target_id"]] = by_target.get(s["target_id"], 0) + 1
    tmap = {r["id"]: r for r in targets}
    out_targets = []
    for r in targets:
        options = []
        for mode, eff in (("solo", solo_eff), (team_mode, team_eff)):
            if mode is None or not exp_mode_allowed(r["scope"], mode):
                continue
            ox, oy = origin_for(mode, ctx.user_id if mode == "solo" else team_id)
            minutes = exp_travel_minutes(distance(ox, oy, r["x"], r["y"]), mode, eff["speed"])
            options.append({"mode": mode, "minutes": minutes, "ok": now.timestamp() + minutes * 60 <= r["resolve_at"].timestamp()})
        prizes = prizes_by_place(r["prizes"])
        reward_all = _rewards(r["reward_all"])
        out_targets.append({
            "id": r["id"], "title": localized_title(r["title"], r["title_tpl"], ctx.lang), "descr": r["descr"], "icon": r["icon"], "x": r["x"], "y": r["y"],
            "scope": r["scope"], "scope_label": t(ctx.lang, f"post.scope_{r['scope']}"), "forks": r["forks"],
            "resolve_at": _iso(r["resolve_at"]), "places": r["places"], "squads": by_target.get(r["id"], 0),
            "prizes": [{"place": p, "label": rewards_label(prizes[p])} for p in sorted(prizes)][:20],
            "reward_all": rewards_label(reward_all) if reward_all else "", "options": options,
        })
    out_squads = []
    for s in squads:
        mine = s["id"] in my_ids
        name = html.unescape(s["team_name"] or "") if s["mode"] != "solo" else ""
        out_squads.append({"id": s["id"], "target_id": s["target_id"], "mode": s["mode"], "status": s["status"],
                           "ox": s["ox"], "oy": s["oy"], "departed_at": _iso(s["departed_at"]),
                           "arrive_at": _iso(s["arrive_at"]), "name": name,
                           "symbol": html.unescape(s["school_num"] or "") if s["mode"] != "solo" else "", "mine": mine})
    my = []
    for s in my_rows:
        exp = dict(s)
        target = tmap[s["target_id"]]
        eff = solo_eff if s["mode"] == "solo" else team_eff
        exp_votes = [v for v in votes if v["expedition_id"] == s["id"]]
        my.append({
            "id": s["id"], "target_id": s["target_id"], "mode": s["mode"], "status": s["status"],
            "batteries": s["batteries"], "cutlets": s["cutlets"], "need": gear_needed(s["mode"]),
            "departed_at": _iso(s["departed_at"]), "arrive_at": _iso(s["arrive_at"]), "cargo": s["cargo"],
            "forks_done": s["forks_done"], "forks": target["forks"],
            "late": bool(s["arrive_at"] and s["arrive_at"] > target["resolve_at"]),
            "arrived": bool(s["arrive_at"] and s["arrive_at"] <= now),
            "fork": (_fork_payload(exp, target["forks"], now, ctx.lang, exp_votes, ctx.user_id, peeks[s["id"]]["peeked"])
                     if s["status"] == "marching" else None),
            "peeks": peeks.get(s["id"]),
            "members": sizes.get(s["id"], 1),
            "log": _log_payload([l for l in logs if l["expedition_id"] == s["id"]], ctx.lang),
            "effects": {k: eff[k] for k in ("cargo", "guard", "speed")},
        })
    return web.json_response({
        "map": {"w": EXP_MAP_W, "h": EXP_MAP_H}, "now": _iso(now),
        "targets": out_targets, "squads": out_squads, "my": my,
        "me": {"in_team": team_id is not None, "team_mode": team_mode,
               "team": html.unescape(me["team_name"] or "") if team_id else "",
               "hydrogen": stock.get("hydrogen", 0), "batteries": stock.get("battery", 0), "cutlets": me["inv_cutlets"],
               "drones": {"guard": me["drones_guard"], "attack": me["drones_attack"], "spy": me["drones_spy"]},
               "home": {"solo": origin_for("solo", ctx.user_id),
                        "team": origin_for(team_mode, team_id) if team_id else None}},
        "rules": {"solo_h2": EXP_SOLO_HYDROGEN, "batteries": EXP_BATTERIES, "clan_cutlets": EXP_CLAN_CUTLETS},
    })


async def _exp_call(request: web.Request, action) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if off := await _feature_off("expeditions", ctx.lang):
        return off
    data = await _json(request)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await action(conn, ctx.user_id, data)
    except ExpError as e:
        return fail(e.localized(ctx.lang))
    return web.json_response({"ok": True, **result})


async def handle_exp_solo(request: web.Request) -> web.Response:
    return await _exp_call(request, lambda conn, uid, d: start_solo(conn, uid, _int(d.get("target_id")), utcnow()))


async def handle_exp_gear(request: web.Request) -> web.Response:
    return await _exp_call(request, lambda conn, uid, d: contribute(
        conn, uid, _int(d.get("target_id")), str(d.get("what") or "battery"), utcnow()))


async def handle_exp_peek(request: web.Request) -> web.Response:
    return await _exp_call(request, lambda conn, uid, d: peek(conn, uid, _int(d.get("expedition_id")), utcnow()))


async def handle_exp_vote(request: web.Request) -> web.Response:
    return await _exp_call(request, lambda conn, uid, d: vote(
        conn, uid, _int(d.get("expedition_id")), _int(d.get("option"), -1), utcnow()))


def register_map_routes(app: web.Application) -> None:
    app.router.add_get("/api/map", handle_map)
    app.router.add_post("/api/exp/solo", handle_exp_solo)
    app.router.add_post("/api/exp/gear", handle_exp_gear)
    app.router.add_post("/api/exp/vote", handle_exp_vote)
    app.router.add_post("/api/exp/peek", handle_exp_peek)
