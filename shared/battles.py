"""
Битвы команд и кланов — событийные состязания, запускаемые владельцем вручную.

Принципы (решения владельца 13.10.2026):
- битвы ПЕРИОДИЧЕСКИЕ, а не ежедневные: событие, как ЧМ по футболу;
- считается ТОЛЬКО общий результат всех игроков команды — мотивация звать актив;
- зачёт по журналу ledger за окно [starts_at, ends_at] — задним числом не накрутишь;
- команда игрока определяется на момент подведения итогов;
- призы, места, зачёт и рудники задаёт владелец в пульте (см. «БИТВЫ И АКЦИИ v2» ниже).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from shared.economy import SEASON_EARN_REASONS

logger = logging.getLogger(__name__)
# «Заработано в игре» — та же формула, что у ТОПа сезона (аргумент $3 — список причин журнала)
EARN_CONDITION = "l.delta > 0 AND (l.reason = ANY($3::text[]) OR l.reason LIKE 'game_win:%')"

MAX_PRIZE_PLACES = 10

# Номинации: kind определяет формулу подсчёта по ledger/users за окно битвы
BATTLE_NOMINATIONS: dict[str, dict] = {
    "farm_mined": {"title": "⛏️ Больше всех нафармить монет фермой",
                   "kind": "ledger_sum", "reason": "mining", "unit": "монет"},
    "coins_earned": {"title": "💰 Больше всех заработать монет в игре",
                     "kind": "ledger_sum_positive", "unit": "монет"},
    "duel_wins": {"title": "⚔️ Больше всех побед в дуэлях",
                  "kind": "ledger_count", "reason": "duel_win", "unit": "побед"},
    "duels_played": {"title": "🎲 Больше всех сыгранных дуэлей",
                     "kind": "ledger_count", "reason": "duel_stake", "unit": "дуэлей"},
    "quiz_wins": {"title": "🧠 Больше всех верных ответов в Викторине",
                  "kind": "ledger_count", "reason": "game_win:quiz", "unit": "ответов"},
    "rps_wins": {"title": "🪨 Больше всех побед в КНБ",
                 "kind": "ledger_count", "reason": "game_win:rps", "unit": "побед"},
    "safe_wins": {"title": "🔐 Больше всех вскрытых Кибер-Сейфов",
                  "kind": "ledger_count", "reason": "game_win:safe", "unit": "сейфов"},
    "game_wins_total": {"title": "🏆 Больше всех побед во всех играх против бота",
                        "kind": "ledger_count_like", "reason_like": "game_win:%", "unit": "побед"},
    "referrals": {"title": "🤝 Больше всех привести активных новичков в экосистему",
                  "kind": "referrals", "unit": "активных новичков"},
    "stars_spent": {"title": "💵 Больше всех поддержать экосистему (Stars)",
                    "kind": "stars", "unit": "★"},
}


async def battle_team_scores(conn, nomination_key: str, starts_at: datetime,
                             ends_at: datetime, limit: int = MAX_PRIZE_PLACES) -> list[dict]:
    """
    ТОП команд по номинации за окно битвы:
    [{team_id, team_name, is_clan, score}] по убыванию. Нулевые результаты не попадают.
    """
    nom = BATTLE_NOMINATIONS[nomination_key]
    kind = nom["kind"]

    if kind in ("ledger_sum", "ledger_count", "ledger_sum_positive", "ledger_count_like"):
        if kind == "ledger_sum":
            metric, condition = "SUM(l.delta)", "l.reason = $3"
            args = [starts_at, ends_at, nom["reason"]]
        elif kind == "ledger_count":
            metric, condition = "COUNT(*)", "l.reason = $3"
            args = [starts_at, ends_at, nom["reason"]]
        elif kind == "ledger_count_like":
            metric, condition = "COUNT(*)", "l.reason LIKE $3"
            args = [starts_at, ends_at, nom["reason_like"]]
        else:  # ledger_sum_positive — заработок в игре, как в сезоне (без биржи, переводов и подарков)
            metric, condition = "SUM(l.delta)", EARN_CONDITION
            args = [starts_at, ends_at, list(SEASON_EARN_REASONS)]
        query = f"""
            SELECT u.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   {metric}::bigint AS score
            FROM ledger l
            JOIN users u ON u.user_id = l.user_id
            JOIN teams t ON t.team_id = u.team_id
            WHERE l.created_at >= $1 AND l.created_at < $2 AND {condition}
            GROUP BY u.team_id, t.team_name, t.max_members
            HAVING {metric} > 0
            ORDER BY {metric} DESC, u.team_id ASC
            LIMIT {int(limit)}
        """
        rows = await conn.fetch(query, *args)
    elif kind == "referrals":
        rows = await conn.fetch(
            """
            SELECT ref.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   COUNT(*)::bigint AS score
            FROM users newbie
            JOIN users ref ON ref.user_id = newbie.referred_by
            JOIN teams t ON t.team_id = ref.team_id
            WHERE newbie.qualified_at >= $1 AND newbie.qualified_at < $2   -- фейки не в счёт
            GROUP BY ref.team_id, t.team_name, t.max_members
            ORDER BY COUNT(*) DESC, ref.team_id ASC
            LIMIT {limit}
            """.replace("{limit}", str(int(limit))),
            starts_at, ends_at)
    elif kind == "stars":
        rows = await conn.fetch(
            """
            SELECT u.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   SUM(p.stars_amount)::bigint AS score
            FROM star_payments p
            JOIN users u ON u.user_id = p.user_id
            JOIN teams t ON t.team_id = u.team_id
            WHERE p.created_at >= $1 AND p.created_at < $2
            GROUP BY u.team_id, t.team_name, t.max_members
            HAVING SUM(p.stars_amount) > 0
            ORDER BY SUM(p.stars_amount) DESC, u.team_id ASC
            LIMIT {limit}
            """.replace("{limit}", str(int(limit))),
            starts_at, ends_at)
    else:
        raise ValueError(f"Неизвестный вид номинации: {kind}")

    return [dict(r) for r in rows]


def medals(place: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, f"{place}.")


# ==========================================================================
# БИТВЫ И АКЦИИ v2 (решение владельца 27.10): всё создаётся в пульте владельца.
# - зачёт: team (команды), clan (кланы), teams (команды и кланы вместе), solo (личный);
# - номинации — из списка (подсчёт по журналам) или ручные (соцсети, своя формулировка):
#   у ручных победителей по местам вписывает владелец;
# - призовых мест — сколько угодно, награда на каждое место — любая комбинация (shared/prizes.py),
#   командным — КАЖДОМУ бойцу команды-призёра;
# - рудники: сколько рудников, столько призовых мест за них (mine_ids по порядку мест);
#   в битве за рудники участвуют только команды, внёсшие заявку батарейками (5, клан — 25).
# ==========================================================================
BATTLE_SCOPES = ("team", "clan", "teams", "solo")
MANUAL_NOMINATIONS = {
    "insta_reels": "📸 Чей рилс в Instagram залетит лучше",
    "youtube_shorts": "▶️ Чьё видео в YouTube Shorts залетит лучше",
    "tiktok": "🎵 Чьё видео в TikTok залетит лучше",
}
MAX_BATTLE_PLACES = 100
MAX_PARTICIPANTS = 100_000      # награда «за участие» — всем в зачёте (командам — каждому бойцу)


def battle_reward_all(battle) -> list[dict]:
    """Награда «за участие» битвы (всем без призового места) — список наград или []."""
    from shared.prizes import normalize_rewards
    raw = battle["reward_all"] if "reward_all" in battle.keys() else None
    return normalize_rewards(json.loads(raw) if isinstance(raw, str) else (raw or []))


class BattleError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        from shared.locales import t
        return t(lang, self.key, **self.kwargs)


def nomination_title(key: str, custom: str | None = None) -> str:
    if key in BATTLE_NOMINATIONS:
        return BATTLE_NOMINATIONS[key]["title"]
    if key in MANUAL_NOMINATIONS:
        return MANUAL_NOMINATIONS[key]
    return custom or "—"


def is_manual(key: str) -> bool:
    return key not in BATTLE_NOMINATIONS


def battery_fee(is_clan: bool) -> int:
    from shared.economy import BATTLE_BATTERY_FEE_CLAN, BATTLE_BATTERY_FEE_TEAM
    return BATTLE_BATTERY_FEE_CLAN if is_clan else BATTLE_BATTERY_FEE_TEAM


def battle_mines(battle) -> list[int]:
    keys = battle.keys()
    ids = list(battle["mine_ids"] or []) if "mine_ids" in keys else []
    if not ids and "mine_id" in keys and battle["mine_id"]:
        ids = [battle["mine_id"]]
    return ids


async def battle_solo_scores(conn, nomination_key: str, starts_at: datetime, ends_at: datetime,
                             limit: int = MAX_BATTLE_PLACES) -> list[dict]:
    """Личный зачёт по той же формуле, что и командный: [{user_id, name, score}]."""
    nom = BATTLE_NOMINATIONS[nomination_key]
    kind = nom["kind"]
    name_sql = "COALESCE('@' || u.username, NULLIF(u.display_name, ''), 'ID ' || u.user_id::text)"
    alive = "NOT u.is_blocked AND u.deleted_at IS NULL AND u.deletion_requested_at IS NULL"
    if kind in ("ledger_sum", "ledger_count", "ledger_sum_positive", "ledger_count_like"):
        metric = "SUM(l.delta)" if kind in ("ledger_sum", "ledger_sum_positive") else "COUNT(*)"
        if kind == "ledger_sum_positive":
            condition, args = EARN_CONDITION, [starts_at, ends_at, list(SEASON_EARN_REASONS)]
        elif kind == "ledger_count_like":
            condition, args = "l.reason LIKE $3", [starts_at, ends_at, nom["reason_like"]]
        else:
            condition, args = "l.reason = $3", [starts_at, ends_at, nom["reason"]]
        rows = await conn.fetch(f"""
            SELECT u.user_id, {name_sql} AS name, {metric}::bigint AS score
            FROM ledger l JOIN users u ON u.user_id = l.user_id
            WHERE l.created_at >= $1 AND l.created_at < $2 AND {condition} AND {alive}
            GROUP BY u.user_id HAVING {metric} > 0
            ORDER BY {metric} DESC, u.user_id ASC LIMIT {int(limit)}""", *args)
    elif kind == "referrals":
        rows = await conn.fetch(f"""
            SELECT u.user_id, {name_sql} AS name, COUNT(*)::bigint AS score
            FROM users n JOIN users u ON u.user_id = n.referred_by
            WHERE n.qualified_at >= $1 AND n.qualified_at < $2 AND {alive}
            GROUP BY u.user_id ORDER BY COUNT(*) DESC, u.user_id ASC LIMIT {int(limit)}""", starts_at, ends_at)
    elif kind == "stars":
        rows = await conn.fetch(f"""
            SELECT u.user_id, {name_sql} AS name, SUM(p.stars_amount)::bigint AS score
            FROM star_payments p JOIN users u ON u.user_id = p.user_id
            WHERE p.created_at >= $1 AND p.created_at < $2 AND p.refunded_at IS NULL
              AND p.telegram_charge_id NOT LIKE 'TEST%' AND p.stars_amount > 0 AND {alive}
            GROUP BY u.user_id ORDER BY SUM(p.stars_amount) DESC, u.user_id ASC LIMIT {int(limit)}""",
            starts_at, ends_at)
    else:
        raise ValueError(f"Неизвестный вид номинации: {kind}")
    return [dict(r) for r in rows]


def result_entries(results) -> tuple[str, list[dict]]:
    """
    Места из сохранённых итогов битвы: (зачёт, [{id, name}] по порядку мест). Понимает формат v2
    ({"scope", "places": [{id, name, …}]}) и старый ({"scores": [{team_id, team_name}]}) — аудит 1.8:
    сезон и подарки читали только старый, и командный рейтинг сезона был всегда пустым.
    """
    data = json.loads(results) if isinstance(results, str) else (results or {})
    if "places" in data:
        return data.get("scope") or "teams", [{"id": p["id"], "name": p.get("name") or "—"} for p in data["places"]
                                               if p.get("id") is not None]
    return "teams", [{"id": s["team_id"], "name": s.get("team_name") or "—"} for s in data.get("scores", [])]


async def registered_teams(conn, battle_id: int) -> set[int]:
    """Команды, внёсшие полную заявку батарейками."""
    rows = await conn.fetch(
        """SELECT e.team_id FROM battle_entries e JOIN teams t ON t.team_id = e.team_id
           WHERE e.battle_id = $1 AND e.batteries >= CASE WHEN t.max_members >= 1000 THEN $2::int ELSE $3::int END""",
        battle_id, battery_fee(True), battery_fee(False))
    return {r["team_id"] for r in rows}


async def battle_standings(conn, battle, limit: int | None = None) -> list[dict]:
    """
    Таблица битвы: [{id, name, score, is_clan}] (у личного зачёта id = user_id, is_clan = False).
    Для командного зачёта учитывается scope; в битве за рудники — только команды с заявкой.
    """
    limit = limit or max(int(battle["places"] or MAX_PRIZE_PLACES), MAX_PRIZE_PLACES, len(battle_mines(battle)))
    key, scope = battle["nomination_key"], battle["scope"] or "teams"
    if is_manual(key):
        return []
    if scope == "solo":
        rows = await battle_solo_scores(conn, key, battle["starts_at"], battle["ends_at"], limit)
        return [{"id": r["user_id"], "name": r["name"], "score": int(r["score"]), "is_clan": False} for r in rows]
    rows = await battle_team_scores(conn, key, battle["starts_at"], battle["ends_at"], limit=1000)
    if scope == "team":
        rows = [r for r in rows if not r["is_clan"]]
    elif scope == "clan":
        rows = [r for r in rows if r["is_clan"]]
    if battle_mines(battle):
        allowed = await registered_teams(conn, battle["battle_id"])
        rows = [r for r in rows if r["team_id"] in allowed]
    return [{"id": r["team_id"], "name": r["team_name"], "score": int(r["score"]), "is_clan": bool(r["is_clan"])}
            for r in rows[:limit]]


async def resolve_manual_winner(conn, scope: str, value) -> dict | None:
    """Ручной победитель: игрок (ID, @username, VIP ID) или команда (ID или название)."""
    value = str(value or "").strip()
    if not value:
        return None
    if scope == "solo":
        raw = value.lstrip("@")
        row = None
        if raw.isdigit():
            row = await conn.fetchrow("SELECT user_id, username, display_name FROM users WHERE user_id = $1", int(raw))
        if row is None:
            row = await conn.fetchrow(
                "SELECT user_id, username, display_name FROM users WHERE lower(username) = lower($1)", raw)
        if row is None:
            row = await conn.fetchrow(
                "SELECT u.user_id, u.username, u.display_name FROM vip_aliases v JOIN users u ON u.user_id = v.user_id "
                "WHERE lower(v.alias) = lower($1)", raw)
        if row is None:
            return None
        name = "@" + row["username"] if row["username"] else (row["display_name"] or f"ID {row['user_id']}")
        return {"id": row["user_id"], "name": name, "score": None, "is_clan": False}
    row = (await conn.fetchrow("SELECT team_id, team_name, max_members FROM teams WHERE team_id = $1", int(value))
           if value.isdigit() else
           await conn.fetchrow("SELECT team_id, team_name, max_members FROM teams WHERE lower(team_name) = lower($1)", value))
    if row is None:
        return None
    return {"id": row["team_id"], "name": row["team_name"], "score": None, "is_clan": row["max_members"] >= 1000}


def prizes_by_place(value) -> dict[int, list[dict]]:
    """Призы битвы по местам в формате v2 ({"1": [rewards]}); старый формат (sku/manual) переводится."""
    from shared.prizes import normalize_rewards
    data = json.loads(value) if isinstance(value, str) else (value or {})
    out: dict[int, list[dict]] = {}
    for k, v in data.items():
        if isinstance(v, list):
            out[int(k)] = normalize_rewards(v)
        elif isinstance(v, dict) and v.get("mode") == "manual":
            out[int(k)] = normalize_rewards([{"kind": "text", "text": v.get("value")}])
    return out


async def finish_battle(conn, battle, now: datetime) -> dict:
    """
    Подводит итоги (один раз — по статусу): таблица (или ручные победители), призы каждому
    победителю/бойцу, рудники командам по местам. Возвращает итоги для поста.
    """
    from shared.economy import FINISH_RETRY_MINUTES
    from shared.mines import capture_mine
    from shared.prizes import grant_many
    battle_id = battle["battle_id"]
    # 'active' → 'finishing' → 'finished'. Зависший 'finishing' (рестарт посреди выдачи) повторяется безопасно:
    # призы — по ключам reward_grants, рудник не захватывается второй раз, батарейки возвращаются по журналу (аудит 1.3)
    if not await conn.fetchval(
            "UPDATE battles SET status = 'finishing', finishing_at = $2::timestamptz WHERE battle_id = $1 AND (status = 'active' "
            "OR (status = 'finishing' AND finishing_at < $2::timestamptz - make_interval(mins => $3::int))) RETURNING 1",
            battle_id, now, FINISH_RETRY_MINUTES):
        return {"skipped": True}
    if battle_mines(battle):
        await refund_entries(conn, battle_id, only_incomplete=True)   # неполные заявки — батарейки назад (аудит 1.7)
    scope = battle["scope"] or "teams"
    places = int(battle["places"] or 0)
    mines = battle_mines(battle)
    if is_manual(battle["nomination_key"]):
        raw = battle["manual_results"]
        manual = json.loads(raw) if isinstance(raw, str) else (raw or {})
        standings = []
        for place in sorted(int(p) for p in manual):
            winner = await resolve_manual_winner(conn, scope, manual[str(place)])
            if winner:
                standings.append(winner)
    else:
        standings = await battle_standings(conn, battle)
    prizes = prizes_by_place(battle["prizes"])
    rows, notices = [], []

    async def members_of(entry) -> list[int]:
        if scope == "solo":
            return [entry["id"]]
        return [m["user_id"] for m in await conn.fetch(
            "SELECT user_id FROM users WHERE team_id = $1 AND NOT is_blocked AND deleted_at IS NULL", entry["id"])]

    prize_rows = max(places, len(mines))
    for place, entry in enumerate(standings[:prize_rows], start=1):
        rewards = prizes.get(place, [])
        given = 0
        mine_id = until = None
        if scope != "solo" and place <= len(mines):
            mine_id = mines[place - 1]
            async with conn.transaction():
                held = await conn.fetchrow("SELECT team_id, battle_id, captured_until FROM mines WHERE id = $1 FOR UPDATE",
                                           mine_id)
                if held and held["battle_id"] == battle_id and held["team_id"] == entry["id"]:
                    until = held["captured_until"]            # повтор итогов: рудник уже наш, срок не продлеваем
                else:
                    until = await capture_mine(conn, mine_id, entry["id"], battle_id, now)
        got: list[int] = []
        if rewards:
            given, _ = await grant_many(conn, await members_of(entry), rewards, f"B{battle_id}_P{place}", now, got)
        if mine_id and not rewards:
            got = await members_of(entry)
        notices += [{"user_id": u, "title": battle["title"], "tpl": dict(battle).get("title_tpl"), "place": place, "rewards": rewards, "all": False,
                     "mine_id": mine_id} for u in got]
        rows.append({"place": place, **entry, "rewards": rewards, "given": given,
                     "mine_id": mine_id, "until": until.isoformat() if until else None})
    # 🎒 «За участие» (28.10): всем, кто в зачёте, но без призового места, — награда владельца
    participants = 0
    reward_all = battle_reward_all(battle)
    if reward_all and not is_manual(battle["nomination_key"]):
        everyone = await battle_standings(conn, battle, limit=MAX_PARTICIPANTS)
        for place, entry in enumerate(everyone[prize_rows:], start=prize_rows + 1):
            got = []
            given, _ = await grant_many(conn, await members_of(entry), reward_all, f"B{battle_id}_ALL", now, got)
            participants += given
            notices += [{"user_id": u, "title": battle["title"], "tpl": dict(battle).get("title_tpl"), "place": place, "rewards": reward_all, "all": True,
                         "mine_id": None} for u in got]
    results = {"scope": scope, "places": rows, "participants_rewarded": participants}
    await conn.execute("UPDATE battles SET results = $2::jsonb, status = 'finished' WHERE battle_id = $1",
                       battle_id, json.dumps(results, ensure_ascii=False, default=str))
    logger.info("[BATTLE] №%s итоги: %s мест, рудников %s, наград %s", battle_id, len(rows), len(mines), len(notices))
    results["notices"] = notices
    return results


async def refund_entries(conn, battle_id: int, only_incomplete: bool) -> int:
    """
    🔋 Батарейки заявки — назад тем, кто вносил (аудит 1.7): при отмене битвы — всем, при итогах — командам
    с неполной заявкой. Идемпотентно: возвращённая запись журнала удаляется. Возвращает число батареек.
    """
    from shared.resources import change_resource
    keep = await registered_teams(conn, battle_id) if only_incomplete else set()
    async with conn.transaction():
        rows = await conn.fetch("SELECT id, team_id, user_id FROM battle_entry_log WHERE battle_id = $1 FOR UPDATE",
                                battle_id)
        back = [r for r in rows if r["team_id"] not in keep]
        for r in back:
            await change_resource(conn, r["user_id"], "battery", 1, "battle_entry", f"{battle_id}:refund")
        if back:
            await conn.execute("DELETE FROM battle_entry_log WHERE id = ANY($1::bigint[])", [r["id"] for r in back])
            await conn.execute("DELETE FROM battle_entries WHERE battle_id = $1 AND team_id = ANY($2::bigint[])",
                               battle_id, list({r["team_id"] for r in back}))
    if back:
        logger.info("[BATTLE] №%s: возвращено батареек %s", battle_id, len(back))
    return len(back)


async def contribute_battery(conn, battle_id: int, user_id: int, now: datetime) -> dict:
    """
    🔋 Боец вносит батарейку в заявку своей команды на битву за рудники.
    Возвращает {batteries, fee, registered}. Ошибки — BattleError(ключ локали).
    """
    from shared.resources import InsufficientResources, change_resource
    battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", battle_id)
    if battle is None or battle["status"] != "active" or battle["ends_at"] <= now:
        raise BattleError("bt.err_closed")
    if not battle_mines(battle) or (battle["scope"] or "teams") == "solo":
        raise BattleError("bt.err_no_entry")
    user = await conn.fetchrow(
        "SELECT u.team_id, t.max_members FROM users u LEFT JOIN teams t ON t.team_id = u.team_id "
        "WHERE u.user_id = $1 FOR UPDATE OF u", user_id)
    if user is None or user["team_id"] is None:
        raise BattleError("bt.err_no_team")
    is_clan = (user["max_members"] or 0) >= 1000
    scope = battle["scope"] or "teams"
    if (scope == "team" and is_clan) or (scope == "clan" and not is_clan):
        raise BattleError("bt.err_scope")
    fee = battery_fee(is_clan)
    have = await conn.fetchval(
        "SELECT batteries FROM battle_entries WHERE battle_id = $1 AND team_id = $2 FOR UPDATE",
        battle_id, user["team_id"]) or 0
    if have >= fee:
        raise BattleError("bt.err_full")
    try:
        await change_resource(conn, user_id, "battery", -1, "battle_entry", str(battle_id))
    except InsufficientResources as e:
        raise BattleError("bt.err_battery") from e
    total = await conn.fetchval(
        """INSERT INTO battle_entries (battle_id, team_id, batteries) VALUES ($1, $2, 1)
           ON CONFLICT (battle_id, team_id) DO UPDATE SET batteries = battle_entries.batteries + 1
           RETURNING batteries""", battle_id, user["team_id"])
    await conn.execute("INSERT INTO battle_entry_log (battle_id, team_id, user_id) VALUES ($1, $2, $3)",
                       battle_id, user["team_id"], user_id)
    return {"batteries": total, "fee": fee, "registered": total >= fee}
