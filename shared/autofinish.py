"""
⏱ Досрочные итоги «по N» (решение владельца 30.10): у экспедиции, битвы/акции (и битвы за рудники) и аукциона кроме
точного времени окончания можно задать finish_count — итоги подводятся, как только наберётся N (10/100/1000/10000):
- экспедиция — игроков, ДОШЕДШИХ до цели (участники отрядов, чей марш закончился);
- битва/акция — участников в таблице (личный зачёт — игроков, командный — команд с очками);
- аукцион — игроков, сделавших ставку.
Что наступит раньше — время или N. Шаг демона админ-бота только «переводит часы» (ends_at / resolve_at = сейчас),
дальше работают обычные, уже идемпотентные итоги.
"""
from __future__ import annotations

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def exp_arrived_players(conn, target_id: int, now: datetime) -> int:
    return await conn.fetchval(
        """SELECT COUNT(*) FROM expedition_members m JOIN expeditions e ON e.id = m.expedition_id
           WHERE e.target_id = $1 AND e.status IN ('marching', 'done') AND e.arrive_at <= $2""", target_id, now)


async def battle_participants(conn, battle) -> int:
    from shared.battles import battle_standings
    rows = await battle_standings(conn, battle, limit=max(int(battle["finish_count"] or 0), 1))
    return sum(1 for r in rows if r["score"] > 0)


async def auction_bidders(conn, auction_id: int) -> int:
    return await conn.fetchval("SELECT COUNT(DISTINCT user_id) FROM ledger WHERE reason = 'auction_bid' AND ref = $1",
                               str(auction_id))


async def autofinish_step(conn, now: datetime) -> list[str]:
    """Переводит на «сейчас» итоги всего, где набралось N. Возвращает подписи для сводки владельцу."""
    done: list[str] = []
    for t in await conn.fetch("SELECT id, title, finish_count FROM expedition_targets WHERE status = 'open' "
                              "AND finish_count IS NOT NULL AND resolve_at > $1", now):
        if await exp_arrived_players(conn, t["id"], now) >= t["finish_count"]:
            # отряды судим по моменту, когда набралось N: кто ещё в пути — опоздал (решает скорость)
            if await conn.fetchval("UPDATE expedition_targets SET planned_resolve_at = $2, resolve_at = $2 "
                                   "WHERE id = $1 AND status = 'open' RETURNING 1", t["id"], now):
                done.append(f"🗺 цель №{t['id']} «{t['title']}» — дошли {t['finish_count']}")
    for b in await conn.fetch("SELECT * FROM battles WHERE status = 'active' AND finish_count IS NOT NULL "
                              "AND starts_at <= $1 AND ends_at > $1", now):
        if await battle_participants(conn, b) >= b["finish_count"]:
            if await conn.fetchval("UPDATE battles SET ends_at = $2 WHERE battle_id = $1 AND status = 'active' "
                                   "RETURNING 1", b["battle_id"], now):
                done.append(f"⚔️ битва №{b['battle_id']} «{b['title']}» — участников {b['finish_count']}")
    for a in await conn.fetch("SELECT auction_id, item_title, finish_count FROM auctions WHERE status = 'open' "
                              "AND finish_count IS NOT NULL AND ends_at > $1", now):
        if await auction_bidders(conn, a["auction_id"]) >= a["finish_count"]:
            if await conn.fetchval("UPDATE auctions SET ends_at = $2 WHERE auction_id = $1 AND status = 'open' "
                                   "RETURNING 1", a["auction_id"], now):
                done.append(f"🔨 аукцион №{a['auction_id']} «{a['item_title']}» — ставок {a['finish_count']}")
    for line in done:
        logger.info("[AUTOFINISH] %s", line)
    return done
