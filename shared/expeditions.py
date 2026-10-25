"""
🗺 Экспедиции (решение владельца 28.10): цели на карте мира, отряды, развилки, общий час итогов.

- Цели ставит владелец в пульте (до EXP_MAX_TARGETS сразу): координаты, зачёт (соло / команды / кланы /
  команды и кланы), число развилок, ЧАС ИТОГОВ, призы по местам и награда каждому дошедшему.
- Отряд выходит со своей стороны карты (точка на краю, детерминированно по игроку/команде) и идёт к цели
  со скоростью EXP_SPEED[вид]; путь укорачивают 🛰 шпионы. Кто не успевает к часу итогов, выйти не может;
  кого задержали развилки — «опоздал» и в итогах не участвует.
- Снаряжение: соло — EXP_SOLO_HYDROGEN водорода сразу; команда — EXP_BATTERIES["team"] батареек, клан —
  EXP_BATTERIES["clan"] батареек + EXP_CLAN_CUTLETS котлет. Вносят бойцы по одной; полный комплект — отряд
  выходит сам. Не собрали к итогам — всё вносившим возвращается.
- Развилки: на равных долях планового пути (open_i = выход + путь·i/(forks+1)), голосование открыто до
  следующей развилки. Решает большинство голосов команды (ничья — вариант, за который проголосовали раньше;
  никто не голосовал — первый, самый осторожный); в соло — сам игрок, сразу. Срезав дорогу, отряд может
  прийти раньше — тогда оставшиеся развилки он просто не встречает (меньше шансов добыть груз).
- Места в итогах — по грузу (cargo), при равенстве раньше пришедший выше. Награды получают участники отряда:
  вносившие снаряжение и голосовавшие (expedition_members), — пассажиры ничего не получают.
Развилки разрешаются «лениво» (при открытии карты, голосе или итогах) — без отдельного демона.
"""
from __future__ import annotations

import json
import logging
import math
import zlib
from datetime import datetime, timedelta

from shared.economy import (
    EXP_BASE_CARGO,
    EXP_BATTERIES,
    EXP_CLAN_CUTLETS,
    EXP_MAP_H,
    EXP_MAP_W,
    EXP_SOLO_HYDROGEN,
    MEGA_CLAN_MAX_MEMBERS,
    drone_exp_effects,
    exp_peek_budget,
    exp_mode_allowed,
    exp_travel_minutes,
)
from shared.expedition_events import event_for
from shared.locales import t

logger = logging.getLogger(__name__)

ALIVE = "NOT u.is_blocked AND u.deleted_at IS NULL AND u.deletion_requested_at IS NULL"


class ExpError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


# ============================================================================ чистые правила
def origin_for(mode: str, key_id: int) -> tuple[float, float]:
    """Стартовая точка отряда на краю карты: у каждого игрока/команды своя сторона света."""
    angle = (zlib.crc32(f"{'u' if mode == 'solo' else 't'}{key_id}".encode()) % 3600) / 3600 * 2 * math.pi
    return (round(EXP_MAP_W / 2 + (EXP_MAP_W / 2 - 4) * math.cos(angle), 1),
            round(EXP_MAP_H / 2 + (EXP_MAP_H / 2 - 4) * math.sin(angle), 1))


def distance(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(bx - ax, by - ay)


def fork_schedule(departed_at: datetime, planned_minutes: int, forks: int) -> list[tuple[datetime, datetime]]:
    """(открытие, закрытие) каждой развилки: равные доли планового пути, голосование — до следующей."""
    step = planned_minutes / (forks + 1)
    return [(departed_at + timedelta(minutes=step * i), departed_at + timedelta(minutes=step * (i + 1)))
            for i in range(1, forks + 1)]


def decide(votes: list[tuple[int, datetime]], n_options: int) -> tuple[int, int]:
    """Решение отряда: (вариант, голосов за него). Ничья — кто раньше проголосовал; без голосов — вариант 0."""
    tally: dict[int, list] = {}
    for option, at in votes:
        if 0 <= option < n_options:
            entry = tally.setdefault(option, [0, at])
            entry[0] += 1
            entry[1] = min(entry[1], at)
    if not tally:
        return 0, 0
    option, (count, _) = min(tally.items(), key=lambda kv: (-kv[1][0], kv[1][1]))
    return option, count


def apply_option(cargo: int, option: dict, effects: dict) -> tuple[int, int]:
    """(новый груз, задержка в минутах). Атакующие дроны усиливают силовую добычу, защитники режут потери."""
    gain = int(option.get("cargo", 0))
    if option.get("fight") and gain > 0:
        gain = gain * (100 + effects.get("cargo", 0)) // 100
    loss = cargo * int(option.get("loss", 0)) * (100 - effects.get("guard", 0)) // 10000
    return max(0, cargo + gain - loss), int(option.get("delay", 0))


def squad_mode(max_members: int | None) -> str:
    return "clan" if (max_members or 0) >= MEGA_CLAN_MAX_MEMBERS else "team"


def gear_needed(mode: str) -> dict[str, int]:
    """Снаряжение отряда: {'battery': N, 'cutlet': M} (у соло — водород, тратится сразу)."""
    if mode == "solo":
        return {"hydrogen": EXP_SOLO_HYDROGEN}
    return {"battery": EXP_BATTERIES[mode], **({"cutlet": EXP_CLAN_CUTLETS} if mode == "clan" else {})}


def progress(exp, now: datetime) -> float:
    """Доля пройденного пути 0…1 (для маркера на карте)."""
    if not exp["departed_at"] or not exp["arrive_at"]:
        return 0.0
    total = (exp["arrive_at"] - exp["departed_at"]).total_seconds()
    if total <= 0:
        return 1.0
    return max(0.0, min(1.0, (now - exp["departed_at"]).total_seconds() / total))


# ============================================================================ отряд: дроны и разведка
async def squad_members(conn, exp) -> list[int]:
    """Живые бойцы отряда сейчас: соло — сам игрок, команда — её текущий состав."""
    if exp["mode"] == "solo":
        return [exp["user_id"]]
    rows = await conn.fetch(f"SELECT u.user_id FROM users u WHERE u.team_id = $1 AND {ALIVE}", exp["team_id"])
    return [r["user_id"] for r in rows]


async def squad_effects(conn, mode: str, user_id: int | None, team_id: int | None) -> dict:
    """Суммарные дроны отряда → проценты (cargo/guard/speed)."""
    if mode == "solo":
        where, arg = "u.user_id = $1", user_id
    else:
        where, arg = f"u.team_id = $1 AND {ALIVE}", team_id
    row = await conn.fetchrow(
        f"""SELECT COALESCE(SUM(u.drones_attack), 0) AS a, COALESCE(SUM(u.drones_guard), 0) AS g,
                   COALESCE(SUM(u.drones_spy), 0) AS s
            FROM users u WHERE {where}""", arg)
    eff = drone_exp_effects(int(row["a"]), int(row["g"]), int(row["s"]))
    eff["drones"] = {"attack": int(row["a"]), "guard": int(row["g"]), "spy": int(row["s"])}
    return eff


async def peek_state(conn, exp) -> dict:
    """
    🔎 Разведка развилок отряда: {total, used, left, blind, peeked: [номера развилок]}.
    Первая экспедиция отряда в сезоне — вслепую; дальше min(🛰 шпионов, 🔭 разведки) лидера отряда.
    """
    from shared.economy import season_bounds
    start, _ = season_bounds(exp["created_at"])
    if exp["mode"] == "solo":
        leader, same = exp["user_id"], "user_id = $2 AND mode = 'solo'"
        key = exp["user_id"]
    else:
        leader = await conn.fetchval("SELECT captain_id FROM teams WHERE team_id = $1", exp["team_id"])
        same, key = "team_id = $2 AND mode <> 'solo'", exp["team_id"]
    blind = not await conn.fetchval(
        f"""SELECT 1 FROM expeditions WHERE {same} AND id < $1 AND created_at >= $3
              AND status IN ('marching', 'done', 'late') LIMIT 1""", exp["id"], key, start)
    row = await conn.fetchrow(
        "SELECT u.drones_spy, COALESCE(t.level, 0) AS scout FROM users u "
        "LEFT JOIN user_tech t ON t.user_id = u.user_id AND t.tech = 'scout' WHERE u.user_id = $1", leader)
    forks = await conn.fetchval("SELECT forks FROM expedition_targets WHERE id = $1", exp["target_id"])
    total = exp_peek_budget(int(row["drones_spy"]) if row else 0, int(row["scout"]) if row else 0, forks, blind)
    peeked = [r["fork_no"] for r in await conn.fetch(
        "SELECT fork_no FROM expedition_peeks WHERE expedition_id = $1 ORDER BY fork_no", exp["id"])]
    return {"total": total, "used": len(peeked), "left": max(0, total - len(peeked)), "blind": blind, "peeked": peeked}


# ============================================================================ развилки
async def resolve_due_forks(conn, exp_id: int, now: datetime, force_fork: int | None = None) -> dict | None:
    """
    Разрешает развилки, чьё голосование закрылось к моменту now (в транзакции вызывающего; строка
    отряда блокируется). force_fork — разрешить эту развилку сразу (соло-выбор или проголосовали все).
    Возвращает свежую строку отряда.
    """
    exp = await conn.fetchrow("SELECT * FROM expeditions WHERE id = $1 FOR UPDATE", exp_id)
    if exp is None or exp["status"] != "marching":
        return dict(exp) if exp else None
    target = await conn.fetchrow("SELECT forks, resolve_at FROM expedition_targets WHERE id = $1", exp["target_id"])
    exp = dict(exp)
    schedule = fork_schedule(exp["departed_at"], exp["planned_minutes"], target["forks"])
    effects = None
    while exp["forks_done"] < target["forks"]:
        k = exp["forks_done"] + 1
        open_at, close_at = schedule[k - 1]
        if open_at >= exp["arrive_at"]:          # срезали дорогу — оставшихся развилок отряд не встретит
            exp["forks_done"] = target["forks"]
            break
        close_at = min(close_at, exp["arrive_at"])
        forced = force_fork == k and now >= open_at
        if not forced and now < close_at:
            break
        event = event_for(exp_id, k)
        votes = await conn.fetch("SELECT option, created_at FROM expedition_votes WHERE expedition_id = $1 "
                                 "AND fork_no = $2", exp_id, k)
        option, count = decide([(v["option"], v["created_at"]) for v in votes], len(event["options"]))
        if effects is None:
            effects = await squad_effects(conn, exp["mode"], exp["user_id"], exp["team_id"])
        cargo, delay = apply_option(exp["cargo"], event["options"][option], effects)
        moment = now if forced else close_at
        arrive = max(exp["arrive_at"] + timedelta(minutes=delay), moment + timedelta(minutes=1))
        await conn.execute(
            """INSERT INTO expedition_log (expedition_id, fork_no, event_id, option, votes, cargo_delta, delay_min, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8) ON CONFLICT DO NOTHING""",
            exp_id, k, event["id"], option, count, cargo - exp["cargo"], delay, moment)
        exp.update(cargo=cargo, arrive_at=arrive, forks_done=k)
    await conn.execute("UPDATE expeditions SET cargo = $2, arrive_at = $3, forks_done = $4 WHERE id = $1",
                       exp_id, exp["cargo"], exp["arrive_at"], exp["forks_done"])
    return exp


def current_fork(exp, forks: int, now: datetime) -> int | None:
    """Номер развилки, за которую сейчас можно голосовать (None — ждём следующую или путь окончен)."""
    if exp["status"] != "marching" or exp["forks_done"] >= forks:
        return None
    k = exp["forks_done"] + 1
    open_at, _ = fork_schedule(exp["departed_at"], exp["planned_minutes"], forks)[k - 1]
    return k if open_at <= now < exp["arrive_at"] else None


# ============================================================================ выход отряда
async def _target(conn, target_id: int, now: datetime):
    target = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", target_id)
    if target is None or target["status"] != "open" or target["resolve_at"] <= now:
        raise ExpError("exp.err_closed")
    return target


async def _depart(conn, exp_id: int, target, mode: str, ox: float, oy: float, user_id, team_id, now: datetime) -> dict:
    effects = await squad_effects(conn, mode, user_id, team_id)
    minutes = exp_travel_minutes(distance(ox, oy, target["x"], target["y"]), mode, effects["speed"])
    if now + timedelta(minutes=minutes) > target["resolve_at"]:
        raise ExpError("exp.err_late")
    arrive = now + timedelta(minutes=minutes)
    await conn.execute("UPDATE expeditions SET status = 'marching', departed_at = $2, planned_minutes = $3, "
                       "arrive_at = $4 WHERE id = $1", exp_id, now, minutes, arrive)
    logger.info("[EXP] отряд %s вышел к цели %s (%s), путь %s мин", exp_id, target["id"], mode, minutes)
    return {"expedition_id": exp_id, "departed": True, "minutes": minutes, "arrive_at": arrive.isoformat()}


async def _active_elsewhere(conn, column: str, value: int, target_id: int) -> bool:
    return bool(await conn.fetchval(
        f"""SELECT 1 FROM expeditions e JOIN expedition_targets t ON t.id = e.target_id
            WHERE e.{column} = $1 AND e.target_id <> $2 AND e.status IN ('gathering', 'marching')
              AND t.status = 'open' {"AND e.mode = 'solo'" if column == "user_id" else "AND e.mode <> 'solo'"}
            LIMIT 1""", value, target_id))


async def start_solo(conn, user_id: int, target_id: int, now: datetime) -> dict:
    """👤 Соло-вылазка: водород сразу, выход сразу. Одна активная вылазка на игрока."""
    from shared.resources import InsufficientResources, change_resource
    target = await _target(conn, target_id, now)
    if not exp_mode_allowed(target["scope"], "solo"):
        raise ExpError("exp.err_scope")
    user = await conn.fetchrow("SELECT user_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if user is None:
        raise ExpError("common.no_profile")
    if await conn.fetchval("SELECT 1 FROM expeditions WHERE target_id = $1 AND user_id = $2 AND mode = 'solo'",
                           target_id, user_id):
        raise ExpError("exp.err_already")
    if await _active_elsewhere(conn, "user_id", user_id, target_id):
        raise ExpError("exp.err_busy")
    ox, oy = origin_for("solo", user_id)
    effects = await squad_effects(conn, "solo", user_id, None)
    minutes = exp_travel_minutes(distance(ox, oy, target["x"], target["y"]), "solo", effects["speed"])
    if now + timedelta(minutes=minutes) > target["resolve_at"]:
        raise ExpError("exp.err_late")
    try:
        await change_resource(conn, user_id, "hydrogen", -EXP_SOLO_HYDROGEN, "exp_fuel", str(target_id))
    except InsufficientResources as e:
        raise ExpError("exp.err_hydrogen", need=EXP_SOLO_HYDROGEN, have=e.have) from e
    exp_id = await conn.fetchval(
        "INSERT INTO expeditions (target_id, mode, user_id, ox, oy, cargo, created_at) "
        "VALUES ($1, 'solo', $2, $3, $4, $5, $6) RETURNING id", target_id, user_id, ox, oy, EXP_BASE_CARGO, now)
    await conn.execute("INSERT INTO expedition_members (expedition_id, user_id) VALUES ($1, $2)", exp_id, user_id)
    return await _depart(conn, exp_id, target, "solo", ox, oy, user_id, None, now)


async def contribute(conn, user_id: int, target_id: int, what: str, now: datetime) -> dict:
    """
    🔋/🥩 Боец вносит снаряжение в отряд своей команды. Полный комплект — отряд выходит сам.
    Возвращает {expedition_id, batteries, cutlets, need, departed}.
    """
    from shared.resources import InsufficientResources, change_resource
    if what not in ("battery", "cutlet"):
        raise ExpError("exp.err_closed")
    target = await _target(conn, target_id, now)
    user = await conn.fetchrow(
        "SELECT u.team_id, u.inv_cutlets, t.max_members FROM users u LEFT JOIN teams t ON t.team_id = u.team_id "
        "WHERE u.user_id = $1 FOR UPDATE OF u", user_id)
    if user is None or user["team_id"] is None:
        raise ExpError("exp.err_no_team")
    mode = squad_mode(user["max_members"])
    team_id = user["team_id"]
    if not exp_mode_allowed(target["scope"], mode):
        raise ExpError("exp.err_scope")
    need = gear_needed(mode)
    if what == "cutlet" and "cutlet" not in need:
        raise ExpError("exp.err_no_cutlets_needed")
    exp = await conn.fetchrow("SELECT * FROM expeditions WHERE target_id = $1 AND team_id = $2 AND mode <> 'solo' "
                              "FOR UPDATE", target_id, team_id)
    if exp is None:
        if await _active_elsewhere(conn, "team_id", team_id, target_id):
            raise ExpError("exp.err_team_busy")
        ox, oy = origin_for(mode, team_id)
        exp_id = await conn.fetchval(
            """INSERT INTO expeditions (target_id, mode, team_id, ox, oy, cargo, created_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING RETURNING id""",
            target_id, mode, team_id, ox, oy, EXP_BASE_CARGO, now)
        if exp_id is None:   # гонка двух бойцов — строку уже вставил тиммейт
            raise ExpError("exp.err_retry")
        exp = await conn.fetchrow("SELECT * FROM expeditions WHERE id = $1 FOR UPDATE", exp_id)
    if exp["status"] != "gathering":
        raise ExpError("exp.err_departed")
    # Успеет ли отряд, если выйдет прямо сейчас (иначе снаряжение не принимаем)
    effects = await squad_effects(conn, mode, None, team_id)
    minutes = exp_travel_minutes(distance(exp["ox"], exp["oy"], target["x"], target["y"]), mode, effects["speed"])
    if now + timedelta(minutes=minutes) > target["resolve_at"]:
        raise ExpError("exp.err_late")
    column = "batteries" if what == "battery" else "cutlets"
    have = exp[column]
    if have >= need[what]:
        raise ExpError("exp.err_full")
    if what == "battery":
        try:
            await change_resource(conn, user_id, "battery", -1, "exp_gear", str(exp["id"]))
        except InsufficientResources as e:
            raise ExpError("exp.err_battery") from e
    else:
        if (user["inv_cutlets"] or 0) < 1:
            raise ExpError("exp.err_cutlet")
        await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets - 1 WHERE user_id = $1", user_id)
    row = await conn.fetchrow(f"UPDATE expeditions SET {column} = {column} + 1 WHERE id = $1 "
                              "RETURNING batteries, cutlets", exp["id"])
    await conn.execute(
        f"""INSERT INTO expedition_members (expedition_id, user_id, {column}) VALUES ($1, $2, 1)
            ON CONFLICT (expedition_id, user_id) DO UPDATE SET {column} = expedition_members.{column} + 1""",
        exp["id"], user_id)
    out = {"expedition_id": exp["id"], "batteries": row["batteries"], "cutlets": row["cutlets"],
           "need": need, "departed": False}
    ready = row["batteries"] >= need["battery"] and row["cutlets"] >= need.get("cutlet", 0)
    if ready:
        out.update(await _depart(conn, exp["id"], target, mode, exp["ox"], exp["oy"], None, team_id, now))
    return out


# ============================================================================ голосование
async def _open_fork(conn, user_id: int, exp_id: int, now: datetime) -> tuple[dict, int]:
    """Отряд игрока и номер развилки, открытой сейчас (с проверкой, что игрок — боец этого отряда)."""
    exp = await resolve_due_forks(conn, exp_id, now)
    if exp is None:
        raise ExpError("exp.err_closed")
    if exp["mode"] == "solo":
        if exp["user_id"] != user_id:
            raise ExpError("exp.err_not_member")
    else:
        team_id = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
        if team_id is None or team_id != exp["team_id"]:
            raise ExpError("exp.err_not_member")
    target = await conn.fetchrow("SELECT forks, status FROM expedition_targets WHERE id = $1", exp["target_id"])
    if target["status"] != "open":
        raise ExpError("exp.err_closed")
    k = current_fork(exp, target["forks"], now)
    if k is None:
        raise ExpError("exp.err_no_fork")
    return exp, k


async def peek(conn, user_id: int, exp_id: int, now: datetime) -> dict:
    """🔎 Разведать текущую развилку: последствия вариантов видны всему отряду. Тратит одну разведку."""
    exp, k = await _open_fork(conn, user_id, exp_id, now)
    state = await peek_state(conn, exp)
    if k in state["peeked"]:
        raise ExpError("exp.err_peeked")
    if state["left"] <= 0:
        raise ExpError("exp.err_no_peeks")
    await conn.execute("INSERT INTO expedition_peeks (expedition_id, fork_no, user_id, created_at) VALUES ($1, $2, $3, $4)",
                       exp_id, k, user_id, now)
    await conn.execute("INSERT INTO expedition_members (expedition_id, user_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                       exp_id, user_id)
    return {"fork": k, "left": state["left"] - 1}


async def vote(conn, user_id: int, exp_id: int, option: int, now: datetime) -> dict:
    """🗳 Голос за вариант на текущей развилке. Соло — решение сразу; команда — когда проголосовали все."""
    exp, k = await _open_fork(conn, user_id, exp_id, now)
    if not 0 <= option < len(event_for(exp_id, k)["options"]):
        raise ExpError("exp.err_no_fork")
    await conn.execute(
        """INSERT INTO expedition_votes (expedition_id, fork_no, user_id, option, created_at) VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (expedition_id, fork_no, user_id) DO UPDATE SET option = EXCLUDED.option""",
        exp_id, k, user_id, option, now)
    await conn.execute("INSERT INTO expedition_members (expedition_id, user_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                       exp_id, user_id)
    resolved = False
    if exp["mode"] == "solo":
        resolved = True
    else:
        voted = await conn.fetchval("SELECT COUNT(*) FROM expedition_votes WHERE expedition_id = $1 AND fork_no = $2",
                                    exp_id, k)
        resolved = voted >= len(await squad_members(conn, exp))
    if resolved:
        exp = await resolve_due_forks(conn, exp_id, now, force_fork=k)
    return {"fork": k, "resolved": resolved, "cargo": exp["cargo"], "arrive_at": exp["arrive_at"].isoformat()}


# ============================================================================ итоги
async def _refund_gathering(conn, exp) -> None:
    from shared.resources import change_resource
    for m in await conn.fetch("SELECT * FROM expedition_members WHERE expedition_id = $1", exp["id"]):
        if m["batteries"]:
            await change_resource(conn, m["user_id"], "battery", m["batteries"], "exp_refund", str(exp["id"]))
        if m["cutlets"]:
            await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                               m["user_id"], m["cutlets"])
    await conn.execute("UPDATE expeditions SET status = 'refunded' WHERE id = $1", exp["id"])


async def squad_name(conn, exp) -> str:
    if exp["mode"] == "solo":
        row = await conn.fetchrow("SELECT username, display_name, user_id FROM users WHERE user_id = $1", exp["user_id"])
        if row is None:
            return "—"
        return "@" + row["username"] if row["username"] else (row["display_name"] or f"ID {row['user_id']}")
    import html
    return html.unescape(await conn.fetchval("SELECT team_name FROM teams WHERE team_id = $1", exp["team_id"]) or "—")


async def finalize_target(conn, target, now: datetime) -> dict:
    """
    Итоги цели (один раз — по статусу): развилки до часа итогов, места по грузу среди дошедших,
    призы по местам и награда каждому дошедшему (участникам отряда), возврат несобранного снаряжения.
    conn — соединение из пула (каждая выдача — своя транзакция).
    """
    from shared.battles import prizes_by_place
    from shared.prizes import grant_many, normalize_rewards
    tid = target["id"]
    if not await conn.fetchval("UPDATE expedition_targets SET status = 'finished' WHERE id = $1 AND status = 'open' "
                               "RETURNING 1", tid):
        return {"skipped": True}
    resolve_at = target["resolve_at"]
    moment = min(now, resolve_at)
    arrived, late = [], 0
    for exp in await conn.fetch("SELECT * FROM expeditions WHERE target_id = $1 ORDER BY id", tid):
        async with conn.transaction():
            if exp["status"] == "gathering":
                await _refund_gathering(conn, exp)
                continue
            if exp["status"] != "marching":
                continue
            fresh = await resolve_due_forks(conn, exp["id"], moment)
            if fresh["arrive_at"] <= resolve_at:
                await conn.execute("UPDATE expeditions SET status = 'done' WHERE id = $1", exp["id"])
                arrived.append(fresh)
            else:
                await conn.execute("UPDATE expeditions SET status = 'late' WHERE id = $1", exp["id"])
                late += 1
    arrived.sort(key=lambda e: (-e["cargo"], e["arrive_at"], e["id"]))
    prizes = prizes_by_place(target["prizes"])
    raw_all = target["reward_all"]
    reward_all = normalize_rewards(json.loads(raw_all) if isinstance(raw_all, str) else (raw_all or []))
    rows = []
    for place, exp in enumerate(arrived, start=1):
        members = [r["user_id"] for r in await conn.fetch(
            f"SELECT m.user_id FROM expedition_members m JOIN users u ON u.user_id = m.user_id "
            f"WHERE m.expedition_id = $1 AND NOT u.is_blocked AND u.deleted_at IS NULL", exp["id"])]
        given = 0
        rewards = prizes.get(place, [])
        if rewards and any(r["kind"] != "text" for r in rewards):
            given, _ = await grant_many(conn, members, rewards, f"E{tid}_P{place}", now)
        if place > (target["places"] or 0) and reward_all and any(r["kind"] != "text" for r in reward_all):
            await grant_many(conn, members, reward_all, f"E{tid}_ALL", now)   # 🎒 за участие — без призового места
        rows.append({"place": place, "name": await squad_name(conn, exp), "mode": exp["mode"], "cargo": exp["cargo"],
                     "members": len(members), "rewards": rewards, "given": given})
    results = {"places": rows, "arrived": len(arrived), "late": late}
    await conn.execute("UPDATE expedition_targets SET results = $2::jsonb WHERE id = $1",
                       tid, json.dumps(results, ensure_ascii=False, default=str))
    logger.info("[EXP] цель %s: итоги — дошли %s, опоздали %s", tid, len(arrived), late)
    return results


async def cancel_target(conn, target_id: int) -> bool:
    """⛔ Отмена цели владельцем: без призов, всё снаряжение (и водород соло) возвращается участникам."""
    from shared.resources import change_resource
    async with conn.transaction():
        if not await conn.fetchval("UPDATE expedition_targets SET status = 'cancelled' WHERE id = $1 AND status = 'open' "
                                   "RETURNING 1", target_id):
            return False
        for exp in await conn.fetch("SELECT * FROM expeditions WHERE target_id = $1 AND status IN ('gathering', 'marching')",
                                    target_id):
            if exp["mode"] == "solo":
                await change_resource(conn, exp["user_id"], "hydrogen", EXP_SOLO_HYDROGEN, "exp_refund", str(exp["id"]))
                await conn.execute("UPDATE expeditions SET status = 'refunded' WHERE id = $1", exp["id"])
            else:
                await _refund_gathering(conn, exp)
    logger.info("[EXP] цель %s отменена владельцем, снаряжение возвращено", target_id)
    return True
