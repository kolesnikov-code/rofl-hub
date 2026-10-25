"""
Станция команды (волна 22.10, вечер): общий проект на ресурсах всей команды.

- любой участник вкладывает ресурсы (change_resource reason='station_donate');
- уровень L закрывается, когда вложено station_level_cost(L) КАЖДОГО ресурса;
  излишек переносится на следующий уровень; максимум STATION_MAX_LEVEL;
- каждый уровень даёт ВСЕМ участникам команды +STATION_BONUS_PER_LEVEL% к добыче фермы
  (читается движком фермы по users.team_id — вышел из команды, потерял бонус);
- лента последних вкладов — для чувства общего дела.
Всё — внутри транзакции вызывающего кода.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from shared.economy import RESOURCE_KINDS, STATION_FEED_LIMIT, STATION_MAX_LEVEL, station_level_cost
from shared.locales import t
from shared.resources import InsufficientResources, change_resource

logger = logging.getLogger(__name__)


class StationError(Exception):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


@dataclass
class DonateResult:
    level: int
    levels_gained: int
    stock: dict[str, int]              # вложено на текущий уровень (после переходов)
    need: dict[str, int] = field(default_factory=dict)   # сколько ещё до следующего уровня
    credited: int = 0                  # засчитано станции (ровно вложенное)


def progress_to_next(level: int, stock: dict[str, int]) -> dict[str, int]:
    """Сколько каждого ресурса не хватает до уровня level+1 (пусто — максимум)."""
    if level >= STATION_MAX_LEVEL:
        return {}
    cost = station_level_cost(level + 1)
    return {k: max(0, cost - stock.get(k, 0)) for k in RESOURCE_KINDS}


def apply_level_ups(level: int, stock: dict[str, int]) -> tuple[int, dict[str, int], int]:
    """Чистая логика: закрывает все уровни, на которые хватает. Возвращает (уровень, остаток, +уровней)."""
    gained = 0
    stock = dict(stock)
    while level < STATION_MAX_LEVEL:
        cost = station_level_cost(level + 1)
        if all(stock.get(k, 0) >= cost for k in RESOURCE_KINDS):
            for k in RESOURCE_KINDS:
                stock[k] -= cost
            level += 1
            gained += 1
        else:
            break
    return level, stock, gained


async def get_station(conn, team_id: int, lock: bool = False):
    await conn.execute("INSERT INTO team_stations (team_id) VALUES ($1) ON CONFLICT DO NOTHING", team_id)
    return await conn.fetchrow(
        f"SELECT * FROM team_stations WHERE team_id = $1{' FOR UPDATE' if lock else ''}", team_id)


async def station_level(conn, team_id: int | None) -> int:
    if team_id is None:
        return 0
    return await conn.fetchval("SELECT level FROM team_stations WHERE team_id = $1", team_id) or 0


async def donate(conn, user_id: int, kind: str, qty: int) -> DonateResult:
    """Вклад ресурса в станцию своей команды."""
    if kind not in RESOURCE_KINDS or qty <= 0:
        raise StationError("st.err_qty")
    me = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    team_id = me["team_id"] if me else None
    if team_id is None:
        raise StationError("st.err_no_team")
    station = await get_station(conn, team_id, lock=True)
    if station["level"] >= STATION_MAX_LEVEL:
        raise StationError("st.err_max", max=STATION_MAX_LEVEL)
    try:
        await change_resource(conn, user_id, kind, -qty, "station_donate", str(team_id))
    except InsufficientResources as e:
        raise StationError("st.err_resources", have=e.have) from e

    credited = qty   # ресурсы из воздуха не создаём (решение владельца 27.10)
    stock = {k: station[k] for k in RESOURCE_KINDS}
    stock[kind] += credited
    level, stock, gained = apply_level_ups(station["level"], stock)
    await conn.execute(
        "UPDATE team_stations SET level = $2, metal = $3, hydrogen = $4, crystal = $5, parts = $6, "
        "updated_at = NOW() WHERE team_id = $1",
        team_id, level, stock["metal"], stock["hydrogen"], stock["crystal"], stock["parts"])
    await conn.execute(
        "INSERT INTO team_donations (team_id, user_id, kind, qty) VALUES ($1, $2, $3, $4)",
        team_id, user_id, kind, credited)
    logger.info("[STATION] team=%s user=%s +%s %s → level %s (+%s)", team_id, user_id, qty, kind, level, gained)
    return DonateResult(level=level, levels_gained=gained, stock=stock,
                        need=progress_to_next(level, stock), credited=credited)


async def recent_donations(conn, team_id: int, limit: int = STATION_FEED_LIMIT) -> list[dict]:
    rows = await conn.fetch(
        """SELECT d.user_id, d.kind, d.qty, d.created_at, u.display_name, u.username
           FROM team_donations d LEFT JOIN users u ON u.user_id = d.user_id
           WHERE d.team_id = $1 ORDER BY d.created_at DESC LIMIT $2""", team_id, limit)
    return [dict(r) for r in rows]


async def team_member_ids(conn, team_id: int) -> list[int]:
    rows = await conn.fetch("SELECT user_id FROM users WHERE team_id = $1 AND NOT is_blocked", team_id)
    return [r["user_id"] for r in rows]
