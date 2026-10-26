"""
🏆 Сезоны (решение владельца 27.10): сезон = календарный месяц UTC.

Сбрасываются только соревновательные таблицы — монеты, роботы, склад и покупки остаются:
- ТОП игроков «заработано за сезон»: положительные начисления монет из ИГРЫ (ферма, победы, дуэли,
  квесты, сундук, продажи на бирже, награда за друга) — без переводов, подарков и покупок монет;
- рейтинг команд: очки за места в битвах сезона (SEASON_BATTLE_POINTS);
- рейтинг друзей: друзья, ставшие активными в этом месяце.
Итоги прошлого месяца подводит демон админ-бота (finalize_season, идемпотентно через season_results):
значки ТОП-10 в паспорт. Призы владелец назначает сам — /reward «ТОП прошлого сезона».
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta

from shared.economy import (SEASON_BADGE_PLACES, SEASON_BATTLE_POINTS, SEASON_FIRST, SEASON_EARN_REASONS,
                            SEASON_TOP_SIZE, season_bounds, season_key)

logger = logging.getLogger(__name__)

_EARN_SQL = """
    SELECT l.user_id, SUM(l.delta)::bigint AS earned
    FROM ledger l JOIN users u ON u.user_id = l.user_id
    WHERE l.created_at >= $1 AND l.created_at < $2 AND l.delta > 0
      AND (l.reason = ANY($3::text[]) OR l.reason LIKE 'game_win:%')
      AND NOT u.is_blocked AND u.deleted_at IS NULL AND u.deletion_requested_at IS NULL
    GROUP BY l.user_id
"""


async def season_top(conn, moment: datetime, limit: int = SEASON_TOP_SIZE) -> list[dict]:
    start, end = season_bounds(moment)
    rows = await conn.fetch(
        f"""SELECT e.user_id, e.earned, u.username, u.display_name, u.created_at, COALESCE(g.quiz_level, 0) AS quiz_level
            FROM ({_EARN_SQL}) e JOIN users u ON u.user_id = e.user_id
            LEFT JOIN game_stats g ON g.user_id = e.user_id
            ORDER BY e.earned DESC, e.user_id ASC LIMIT $4""",
        start, end, list(SEASON_EARN_REASONS), limit)
    return [dict(r) for r in rows]


async def season_place(conn, user_id: int, moment: datetime) -> dict:
    """Место и заработок игрока в сезоне (place 0 — ещё ничего не заработал)."""
    start, end = season_bounds(moment)
    rows = await conn.fetch(f"SELECT user_id, earned FROM ({_EARN_SQL}) e ORDER BY earned DESC, user_id ASC",
                            start, end, list(SEASON_EARN_REASONS))
    for i, r in enumerate(rows, start=1):
        if r["user_id"] == user_id:
            return {"place": i, "earned": int(r["earned"]), "total": len(rows)}
    return {"place": 0, "earned": 0, "total": len(rows)}


async def season_teams(conn, moment: datetime, limit: int = 20) -> list[dict]:
    """Очки команд за битвы, закончившиеся в этом сезоне."""
    start, end = season_bounds(moment)
    rows = await conn.fetch(
        "SELECT results FROM battles WHERE status = 'finished' AND ends_at >= $1 AND ends_at < $2 AND results IS NOT NULL",
        start, end)
    from shared.battles import result_entries
    points: dict[int, dict] = {}
    for r in rows:
        scope, entries = result_entries(r["results"])
        if scope == "solo":                       # личный зачёт очков команде не даёт
            continue
        for place, sc in enumerate(entries, start=1):
            pts = SEASON_BATTLE_POINTS.get(place, 0)
            if not pts:
                continue
            entry = points.setdefault(sc["id"], {"team_id": sc["id"], "name": sc["name"], "points": 0})
            entry["points"] += pts
    return sorted(points.values(), key=lambda x: (-x["points"], x["team_id"]))[:limit]


def previous_season_moment(now: datetime) -> datetime:
    start, _ = season_bounds(now)
    return start - timedelta(seconds=1)


async def finalize_season(conn, moment: datetime) -> dict | None:
    """
    Итоги сезона, в который попадает moment (вызывать после его конца). Идемпотентно.
    Выдаёт только значки ТОП-10 (призы — вручную владельцем). None — сезон уже подведён или до первого.
    """
    key = season_key(moment)
    if key < SEASON_FIRST:
        return None
    # Одна транзакция (аудит 1.3): сбой посередине откатывает и отметку «сезон подведён» — повтор доделает значки
    async with conn.transaction():
        if not await conn.fetchval(
                "INSERT INTO season_results (season) VALUES ($1) ON CONFLICT DO NOTHING RETURNING 1", key):
            return None
        top = await season_top(conn, moment, limit=SEASON_BADGE_PLACES)
        winners = []
        for place, row in enumerate(top, start=1):
            await conn.execute("INSERT INTO user_badges (user_id, season, place) VALUES ($1, $2, $3) "
                               "ON CONFLICT DO NOTHING", row["user_id"], key, place)
            winners.append({"place": place, "user_id": row["user_id"], "earned": int(row["earned"]),
                            "name": ("@" + row["username"]) if row["username"] else (row["display_name"] or "")})
        teams = await season_teams(conn, moment, limit=3)
        payload = {"players": winners, "teams": teams}
        await conn.execute("UPDATE season_results SET payload = $2::jsonb WHERE season = $1", key, json.dumps(payload))
    logger.info("[SEASON] %s подведён: %s игроков, %s команд", key, len(winners), len(teams))
    return payload


async def user_badges(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch("SELECT season, place FROM user_badges WHERE user_id = $1 ORDER BY season DESC", user_id)
    return [dict(r) for r in rows]
