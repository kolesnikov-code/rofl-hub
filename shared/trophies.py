"""
🏆 Трофейная история (решение владельца 30.10): «каждая деталь должна вмещать все события, которые она пережила».

Одно событие игры (record) пишется сразу в три места:
- в КАЖДЫЙ надетый скин (user_skins.stats) — история экземпляра переходит с ним к покупателю на бирже;
- в КАЖДУЮ надетую деталь костюма (gear_stats по костюму/слоту/уровню) — «шлем шахтёра пережил 12 налётов»;
- в опыт пропуска сезона (shared/season_pass.py).
Вызывается внутри игровых транзакций, но в своей точке сохранения: сбой учёта НИКОГДА не ломает игру.
"""
from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)

# событие → подпись в истории (ключи приложения tr_<событие>)
EVENTS = ("game_win", "duel", "duel_win", "raid", "raid_win", "raid_def", "expedition", "craft", "tech", "quest",
          "chest")


async def record(conn, user_id: int, event: str, n: int = 1) -> None:
    if event not in EVENTS or n <= 0:
        return
    try:
        async with conn.transaction():
            from shared.skins import SKIN_EVENT_XP
            await conn.execute(
                "UPDATE user_skins SET stats = stats || jsonb_build_object($2::text, COALESCE((stats->>$2)::int, 0) + $3), "
                "xp = xp + $4 WHERE user_id = $1 AND equipped", user_id, event, n, SKIN_EVENT_XP.get(event, 0) * n)
            await conn.execute(
                """INSERT INTO gear_stats (user_id, suit, slot, level, stats)
                   SELECT user_id, suit, slot, level, jsonb_build_object($2::text, $3::int) FROM user_equip
                   WHERE user_id = $1 AND slot IN ('head', 'body', 'hands', 'legs', 'feet')
                   ON CONFLICT (user_id, suit, slot, level) DO UPDATE SET stats = gear_stats.stats ||
                       jsonb_build_object($2::text, COALESCE((gear_stats.stats->>$2)::int, 0) + $3)""",
                user_id, event, n)
            from shared.season_pass import add_xp
            await add_xp(conn, user_id, event, n)
    except Exception:
        logger.exception("[TROPHY] событие %s игрока %s не записано", event, user_id)


async def gear_history(conn, user_id: int) -> dict[str, dict]:
    """{"<костюм>:<слот>:<уровень>": {событие: число}} — история деталей игрока."""
    rows = await conn.fetch("SELECT suit, slot, level, stats FROM gear_stats WHERE user_id = $1", user_id)
    return {f"{r['suit']}:{r['slot']}:{r['level']}": (json.loads(r["stats"]) if isinstance(r["stats"], str) else dict(r["stats"]))
            for r in rows}


async def move_gear_history(conn, user_id: int, suit: str, slot: str, from_level: int, to_level: int) -> None:
    """Прокачка детали: её история переезжает на новый уровень (складывается с уже накопленной там)."""
    row = await conn.fetchrow("DELETE FROM gear_stats WHERE user_id = $1 AND suit = $2 AND slot = $3 AND level = $4 "
                              "RETURNING stats", user_id, suit, slot, from_level)
    if row is None:
        return
    await conn.execute(
        """INSERT INTO gear_stats (user_id, suit, slot, level, stats) VALUES ($1, $2, $3, $4, $5::jsonb)
           ON CONFLICT (user_id, suit, slot, level) DO UPDATE SET stats = (
               SELECT jsonb_object_agg(k, v) FROM (
                   SELECT k, SUM(v::int) AS v FROM (
                       SELECT * FROM jsonb_each_text(gear_stats.stats) UNION ALL SELECT * FROM jsonb_each_text(EXCLUDED.stats)
                   ) AS x(k, v) GROUP BY k) AS y)""",
        user_id, suit, slot, to_level, row["stats"] if isinstance(row["stats"], str) else json.dumps(dict(row["stats"])))
