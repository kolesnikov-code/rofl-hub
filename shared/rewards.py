"""
🎁 Подарки владельца из админ-бота (решение 27.10): игроку, всей команде или клану, ТОПу сезона,
призёрам битвы — монеты, ресурсы (включая Ядро), товары магазина или изделия на склад.
Каждый получатель — своя транзакция: сбой одного не отменяет подарки остальным.
"""
from __future__ import annotations

import logging
from datetime import timedelta

from shared.economy import ALL_KINDS, ITEM_EFFECTS, season_key, utcnow

logger = logging.getLogger(__name__)

TARGETS = ("player", "team", "season", "season_prev", "battle", "active")
ACTIVE_DAYS = 7   # «все активные» — заходили за последнюю неделю
GIFTS = ("coins", "resource", "sku", "item")


async def resolve_recipients(conn, target: str, value: str) -> tuple[list[int], str]:
    """Список ID получателей и подпись для подтверждения. value — ввод владельца."""
    from shared.seasons import season_top
    value = (value or "").strip()
    if target == "player":
        raw = value.lstrip("@")
        if raw.isdigit():
            uid = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", int(raw))
        else:
            uid = await conn.fetchval("SELECT user_id FROM users WHERE lower(username) = lower($1)", raw)
            if uid is None:
                uid = await conn.fetchval("SELECT user_id FROM vip_aliases WHERE lower(alias) = lower($1)", raw)
        return ([uid] if uid else []), f"игрок {value}"
    if target == "active":
        # 🧥 Раздача всем, кто заходил за последние ACTIVE_DAYS дней (кнопка пульта «раздать детали костюмов»)
        days = max(1, min(int(value) if value.isdigit() else ACTIVE_DAYS, 90))
        rows = await conn.fetch("SELECT user_id FROM users WHERE NOT is_blocked AND deleted_at IS NULL "
                                "AND deletion_requested_at IS NULL AND last_seen_at > $1 ORDER BY user_id",
                                utcnow() - timedelta(days=days))
        return [r["user_id"] for r in rows], f"все активные за {days} дн."
    if target == "team":
        team = (await conn.fetchrow("SELECT team_id, team_name FROM teams WHERE team_id = $1", int(value))
                if value.isdigit() else
                await conn.fetchrow("SELECT team_id, team_name FROM teams WHERE lower(team_name) = lower($1)", value))
        if not team:
            return [], "команда не найдена"
        rows = await conn.fetch("SELECT user_id FROM users WHERE team_id = $1 AND NOT is_blocked "
                                "AND deleted_at IS NULL", team["team_id"])
        return [r["user_id"] for r in rows], f"команда «{team['team_name']}»"
    if target in ("season", "season_prev"):
        from shared.seasons import previous_season_moment
        n = max(1, min(int(value) if value.isdigit() else 10, 100))
        moment = utcnow() if target == "season" else previous_season_moment(utcnow())
        rows = await season_top(conn, moment, limit=n)
        return [r["user_id"] for r in rows], f"ТОП-{n} сезона {season_key(moment)}"
    if target == "battle":
        parts = value.split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            return [], "формат: <битва> <место>"
        from shared.battles import result_entries
        row = await conn.fetchrow("SELECT results FROM battles WHERE battle_id = $1", int(parts[0]))
        scope, entries = result_entries(row["results"] if row else None)
        place = int(parts[1])
        if not 1 <= place <= len(entries):
            return [], "такого места в итогах нет"
        winner = entries[place - 1]
        if scope == "solo":
            return [winner["id"]], f"{place} место битвы №{parts[0]} ({winner['name']})"
        rows = await conn.fetch("SELECT user_id FROM users WHERE team_id = $1 AND NOT is_blocked", winner["id"])
        return [r["user_id"] for r in rows], f"{place} место битвы №{parts[0]} («{winner['name']}»)"
    return [], "неизвестный адресат"


def parse_gift(kind: str, value: str) -> dict | None:
    """Разбор подарка: coins «500», resource «core 3», item «shield 24», sku — ключ каталога."""
    from bots.main_bot.catalog import CATALOG
    parts = (value or "").split()
    if kind == "coins" and len(parts) == 1 and parts[0].isdigit() and int(parts[0]) > 0:
        return {"kind": "coins", "amount": int(parts[0])}
    if kind == "resource" and len(parts) == 2 and parts[0] in ALL_KINDS and parts[1].isdigit() and int(parts[1]) > 0:
        return {"kind": "resource", "res": parts[0], "qty": int(parts[1])}
    if kind == "item" and len(parts) == 2 and parts[0] in ITEM_EFFECTS and parts[1].isdigit():
        return {"kind": "item", "effect": parts[0], "hours": int(parts[1])}
    if kind == "sku" and value in CATALOG:
        return {"kind": "sku", "sku": value}
    return None


async def give(conn, user_id: int, gift: dict, ref: str) -> None:
    """Выдаёт подарок одному игроку (внутри транзакции вызывающего)."""
    from shared.items import add_item
    from shared.ledger import change_balance
    from shared.resources import change_resource
    if gift["kind"] == "coins":
        await change_balance(conn, user_id, gift["amount"], "admin_gift", ref)
    elif gift["kind"] == "resource":
        await change_resource(conn, user_id, gift["res"], gift["qty"], "admin_gift", ref)
    elif gift["kind"] == "item":
        await add_item(conn, user_id, gift["effect"], gift["hours"])
    elif gift["kind"] == "sku":
        from bots.main_bot.catalog import get_item
        from shared.delivery import deliver_order
        await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
        await deliver_order(conn, user_id, {**get_item(gift["sku"]), "stars": 0}, f"GIFT{ref}_U{user_id}")


async def give_all(pool_conn, recipients: list[int], gift: dict) -> tuple[int, int]:
    """Раздаёт подарок всем. Возвращает (выдано, сбоев)."""
    ref = utcnow().strftime("%Y%m%d%H%M%S")
    ok = bad = 0
    for uid in recipients:
        try:
            async with pool_conn.transaction():
                await give(pool_conn, uid, gift, ref)
            ok += 1
        except Exception:
            bad += 1
            logger.exception("[REWARD] подарок %s игроку %s не выдан", gift, uid)
    return ok, bad


UNLIMIT_MAX_DAYS = 3650


async def grant_unlimit(conn, who: str, days: int) -> dict | None:
    """⚡ Подписка-Безлимит от владельца (27.10: «дать доступ себе и жене»): снимает лимиты побед и квестов, открывает
    эпики. who — ID / @username / VIP ID; days > 0 — продлить, 0 — снять. None — игрок не найден."""
    from shared.economy import extend_expiry
    ids, _ = await resolve_recipients(conn, "player", who)
    if not ids:
        return None
    uid = ids[0]
    row = await conn.fetchrow("SELECT unlimit_until, lang FROM users WHERE user_id = $1 FOR UPDATE", uid)
    days = max(0, min(int(days), UNLIMIT_MAX_DAYS))
    until = extend_expiry(row["unlimit_until"], utcnow(), days) if days else None
    await conn.execute("UPDATE users SET unlimit_until = $2 WHERE user_id = $1", uid, until)
    return {"user_id": uid, "until": until, "lang": row["lang"]}
