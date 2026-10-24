"""
🤝 Взаимопомощь в команде (решение владельца 26.10): тиммейт просит ресурс — остальные дарят.

Правила (всё внутри транзакции вызывающего, ресурсы — через change_resource):
- просить и помогать можно только своей команде; у игрока одна открытая просьба;
- дарят только РЕСУРСЫ: котлеты — топливо из магазина, их не дарят;
- дарить может только АКТИВНЫЙ аккаунт (как отправитель монет: 3 уровень интеллекта + 3 котлеты),
  не больше TEAM_HELP_DAILY_GIVE за сутки UTC — фейки не сольют ресурсы на основной аккаунт;
- подарок не больше остатка просьбы и свободного места на складе просящего.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from shared.economy import RESOURCE_KINDS, TEAM_HELP_DAILY_GIVE, TEAM_HELP_LIST_LIMIT, TEAM_HELP_MAX_QTY
from shared.locales import t
from shared.resources import InsufficientResources, change_resource, free_space, lock_resources

GIVE_REASON = "team_help_give"
GET_REASON = "team_help_get"


class HelpError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def _day_start(now: datetime) -> datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


async def given_today(conn, user_id: int, now: datetime) -> int:
    """Сколько ресурсов игрок уже подарил тиммейтам сегодня (по resource_ledger)."""
    start = _day_start(now)
    return int(await conn.fetchval(
        "SELECT COALESCE(-SUM(delta), 0) FROM resource_ledger WHERE user_id = $1 AND reason = $2 "
        "AND created_at >= $3 AND created_at < $4", user_id, GIVE_REASON, start, start + timedelta(days=1)) or 0)


async def _team_of(conn, user_id: int) -> int:
    team_id = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
    if team_id is None:
        raise HelpError("mk.err_no_team")
    return team_id


async def request_help(conn, user_id: int, kind: str, qty: int) -> int:
    """Открывает просьбу «нужно qty ресурса kind». Возвращает id."""
    if kind not in RESOURCE_KINDS:
        raise HelpError("mk.err_asset")
    if not 0 < qty <= TEAM_HELP_MAX_QTY:
        raise HelpError("help.err_qty", max=TEAM_HELP_MAX_QTY)
    team_id = await _team_of(conn, user_id)
    await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if await conn.fetchval("SELECT 1 FROM team_help WHERE user_id = $1 AND status = 'open'", user_id):
        raise HelpError("help.err_open")
    return await conn.fetchval(
        "INSERT INTO team_help (team_id, user_id, kind, qty) VALUES ($1, $2, $3, $4) RETURNING id",
        team_id, user_id, kind, qty)


async def cancel_help(conn, user_id: int, help_id: int) -> None:
    done = await conn.execute(
        "UPDATE team_help SET status = 'cancelled' WHERE id = $1 AND user_id = $2 AND status = 'open'",
        help_id, user_id)
    if not done.endswith(" 1"):
        raise HelpError("help.err_not_found")


async def give_help(conn, giver_id: int, help_id: int, qty: int, now: datetime) -> dict:
    """Дарит ресурс по просьбе тиммейта. Возвращает {qty, kind, receiver_id, filled, done}."""
    from shared.transfers import TransferError, ensure_sender_active
    req = await conn.fetchrow("SELECT * FROM team_help WHERE id = $1 FOR UPDATE", help_id)
    if not req or req["status"] != "open":
        raise HelpError("help.err_not_found")
    if req["user_id"] == giver_id:
        raise HelpError("help.err_self")
    if await _team_of(conn, giver_id) != req["team_id"]:
        raise HelpError("mk.err_team_only")
    try:
        await ensure_sender_active(conn, giver_id)
    except TransferError as e:
        raise HelpError(e.key, **e.kwargs) from e
    left_today = TEAM_HELP_DAILY_GIVE - await given_today(conn, giver_id, now)
    if left_today <= 0:
        raise HelpError("help.err_limit", max=TEAM_HELP_DAILY_GIVE)
    room = await free_space(conn, req["user_id"], req["kind"])
    qty = min(qty, req["qty"] - req["filled"], left_today, room)
    if qty <= 0:
        raise HelpError("mk.err_buyer_full", free=room)
    # Блокировки ресурсов — по возрастанию user_id (анти-дедлок, как в обмене на бирже)
    for uid in sorted((giver_id, req["user_id"])):
        await lock_resources(conn, uid)
    try:
        await change_resource(conn, giver_id, req["kind"], -qty, GIVE_REASON, str(help_id))
    except InsufficientResources as e:
        raise HelpError("mk.err_no_resource", have=e.have) from e
    await change_resource(conn, req["user_id"], req["kind"], qty, GET_REASON, str(help_id))
    filled = req["filled"] + qty
    done = filled >= req["qty"]
    await conn.execute("UPDATE team_help SET filled = $2, status = $3 WHERE id = $1",
                       help_id, filled, "done" if done else "open")
    return {"qty": qty, "kind": req["kind"], "receiver_id": req["user_id"], "filled": filled, "done": done}


async def open_requests(conn, team_id: int, limit: int = TEAM_HELP_LIST_LIMIT) -> list[dict]:
    rows = await conn.fetch(
        """SELECT h.id, h.user_id, h.kind, h.qty, h.filled, u.username, u.display_name
           FROM team_help h JOIN users u ON u.user_id = h.user_id
           WHERE h.team_id = $1 AND h.status = 'open' ORDER BY h.created_at LIMIT $2""", team_id, limit)
    return [dict(r) for r in rows]
