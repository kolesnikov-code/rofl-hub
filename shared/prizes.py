"""
🎁 Призы на выбор владельца (решение 27.10): любая награда — одиночная или комбинация.

Награда — список элементов (rewards). Каждый элемент — словарь с полем kind:
- coins     {amount}                 — монеты (ledger 'prize');
- resource  {res, qty}               — любой ресурс, включая Ядро (без лимита склада: приз владельца);
- cutlets   {qty}                    — кибер-котлеты на склад;
- item      {effect, hours}          — изделие на склад (часовое; у разовых hours = 0);
- robot     {robot, hours}           — робот junior/premium на свой срок (часы; годы = 8760 ч);
- boost     {boost, hours}           — сразу включить: nitrogen/nuclear/drone/unlimit/shield на срок;
- bdrone    {drone, qty}             — боевой дрон guard/attack/spy (навсегда, 28.10);
- text      {text}                   — ручной приз (вручает владелец: телефон, Premium…) — только в посте.
Выдача идемпотентна: ключ ref (битва/место/игрок) пишется в reward_grants, повтор — пропуск.
Всё — внутри транзакции вызывающего; для ферменных наград сначала закрывается прошлое время фермы.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta

from shared.economy import ALL_KINDS, ITEM_COLUMNS, ITEM_EFFECTS, ONE_SHOT_COLUMNS, extend_expiry_hours

logger = logging.getLogger(__name__)

REWARD_KINDS = ("coins", "resource", "cutlets", "item", "robot", "boost", "bdrone", "text")
DRONE_ICONS = {"guard": "🛡🤖", "attack": "⚔️🤖", "spy": "🛰🤖"}
ROBOT_KINDS = ("junior", "premium")
BOOST_COLUMNS = {"nitrogen": "boost_nitrogen_until", "nuclear": "boost_nuclear_until", "drone": "drone_until",
                 "unlimit": "unlimit_until", "shield": "raid_shield_until"}
FARM_BOOSTS = ("nitrogen", "nuclear", "drone")
MAX_REWARD_HOURS = 10 * 8760      # не больше 10 лет
MAX_REWARD_QTY = 10_000_000


def _int(v) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def normalize_reward(r: dict) -> dict | None:
    """Проверка и очистка одного элемента награды (ввод из пульта). None — элемент негоден."""
    if not isinstance(r, dict):
        return None
    kind = r.get("kind")
    if kind == "coins":
        n = _int(r.get("amount"))
        return {"kind": "coins", "amount": n} if 0 < n <= MAX_REWARD_QTY else None
    if kind == "resource":
        n = _int(r.get("qty"))
        return {"kind": "resource", "res": r.get("res"), "qty": n} if r.get("res") in ALL_KINDS and 0 < n <= MAX_REWARD_QTY else None
    if kind == "cutlets":
        n = _int(r.get("qty"))
        return {"kind": "cutlets", "qty": n} if 0 < n <= 100_000 else None
    if kind == "item":
        effect, hours, qty = r.get("effect"), _int(r.get("hours")), max(1, _int(r.get("qty")) or 1)
        if effect not in ITEM_EFFECTS or qty > 1000:
            return None
        one_shot = effect == "forsage" or effect in ONE_SHOT_COLUMNS
        if one_shot:
            return {"kind": "item", "effect": effect, "hours": 0, "qty": qty}
        return {"kind": "item", "effect": effect, "hours": hours, "qty": qty} if 0 < hours <= MAX_REWARD_HOURS else None
    if kind == "robot":
        robot, hours, qty = r.get("robot"), _int(r.get("hours")), max(1, _int(r.get("qty")) or 1)
        return ({"kind": "robot", "robot": robot, "hours": hours, "qty": qty}
                if robot in ROBOT_KINDS and 0 < hours <= MAX_REWARD_HOURS and qty <= 100 else None)
    if kind == "boost":
        boost, hours = r.get("boost"), _int(r.get("hours"))
        return {"kind": "boost", "boost": boost, "hours": hours} if boost in BOOST_COLUMNS and 0 < hours <= MAX_REWARD_HOURS else None
    if kind == "bdrone":
        drone, qty = r.get("drone"), max(1, _int(r.get("qty")) or 1)
        return {"kind": "bdrone", "drone": drone, "qty": qty} if drone in DRONE_ICONS and qty <= 100 else None
    if kind == "text":
        text = str(r.get("text") or "").strip()[:200]
        return {"kind": "text", "text": text} if text else None
    return None


def normalize_rewards(items) -> list[dict]:
    out = [normalize_reward(r) for r in (items or [])]
    return [r for r in out if r]


def needs_farm_close(rewards: list[dict]) -> bool:
    return any(r["kind"] == "robot" or (r["kind"] == "boost" and r["boost"] in FARM_BOOSTS) for r in rewards)


def reward_label(r: dict) -> str:
    """Короткая подпись награды эмодзи и числами (для постов на всех языках и пульта)."""
    from shared.resources import RESOURCE_ICONS
    k = r["kind"]
    dur = _dur(r.get("hours", 0))
    if k == "coins":
        return f"{r['amount']:,} 🪙".replace(",", " ")
    if k == "resource":
        return f"{r['qty']} {RESOURCE_ICONS.get(r['res'], r['res'])}"
    if k == "cutlets":
        return f"{r['qty']} 🥩"
    if k == "item":
        icon = {"nitrogen": "❄️", "nuclear": "☢️", "drone": "🛸", "shield": "🛡", "unlimit": "⚡", "camo": "🎭",
                "trap": "🪤", "drill": "🎯", "thermos": "🧊", "banner": "🏳️", "dome": "🛡", "meds": "💊",
                "forsage": "🔥", "economizer": "⛽", "cargo": "📦", "stamp": "📜"}.get(r["effect"], "🧪")
        return f"{icon}{' ' + dur if r['hours'] else ''}" + (f" ×{r['qty']}" if r.get("qty", 1) > 1 else "")
    if k == "robot":
        icon = "🤖" if r["robot"] == "junior" else "⚡🤖"
        return f"{icon} {dur}" + (f" ×{r['qty']}" if r.get("qty", 1) > 1 else "")
    if k == "boost":
        icon = {"nitrogen": "❄️", "nuclear": "☢️", "drone": "🛸", "unlimit": "♾", "shield": "🛡"}[r["boost"]]
        return f"{icon} {dur}"
    if k == "bdrone":
        return DRONE_ICONS[r["drone"]] + (f" ×{r['qty']}" if r.get("qty", 1) > 1 else "")
    return "🎁 " + r.get("text", "")


def rewards_label(rewards: list[dict]) -> str:
    return " + ".join(reward_label(r) for r in rewards) or "—"


def _dur(hours: int) -> str:
    if not hours:
        return ""
    if hours % 8760 == 0:
        return f"{hours // 8760}y"
    if hours % 24 == 0:
        return f"{hours // 24}d"
    return f"{hours}h"


async def grant(conn, user_id: int, rewards: list[dict], ref: str, now: datetime) -> bool:
    """
    Выдаёт награду одному игроку (внутри транзакции вызывающего). False — уже выдано по этому ref
    (или игрока нет). Ручные призы (text) только фиксируются.
    """
    from shared.items import add_item
    from shared.ledger import change_balance
    from shared.resources import change_resource
    if not await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1 AND deleted_at IS NULL", user_id):
        return False
    if not await conn.fetchval(
            "INSERT INTO reward_grants (ref, user_id, payload) VALUES ($1, $2, $3::jsonb) "
            "ON CONFLICT DO NOTHING RETURNING 1", ref, user_id, json.dumps(rewards, ensure_ascii=False)):
        return False
    if needs_farm_close(rewards):
        from shared.farm_logic import apply_lazy_farm
        await apply_lazy_farm(conn, user_id, now)
    else:
        await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    for r in rewards:
        k = r["kind"]
        if k == "coins":
            await change_balance(conn, user_id, r["amount"], "prize", ref)
        elif k == "resource":
            await change_resource(conn, user_id, r["res"], r["qty"], "prize", ref)
        elif k == "cutlets":
            await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1", user_id, r["qty"])
        elif k == "item":
            await add_item(conn, user_id, r["effect"], r["hours"], r.get("qty", 1))
        elif k == "robot":
            for _ in range(r.get("qty", 1)):
                await conn.execute(
                    "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, $2, $3, $4)",
                    user_id, r["robot"], now, now + timedelta(hours=r["hours"]))
        elif k == "bdrone":
            from shared.workshop import add_drone
            await add_drone(conn, user_id, r["drone"], r.get("qty", 1))
        elif k == "boost":
            column = BOOST_COLUMNS[r["boost"]]
            current = await conn.fetchval(f"SELECT {column} FROM users WHERE user_id = $1", user_id)
            await conn.execute(f"UPDATE users SET {column} = $2 WHERE user_id = $1",
                               user_id, extend_expiry_hours(current, now, r["hours"]))
    return True


async def grant_many(pool_conn, user_ids: list[int], rewards: list[dict], ref_prefix: str, now: datetime) -> tuple[int, int]:
    """Каждому игроку — своя транзакция (сбой одного не отменяет остальных). (выдано, сбоев)."""
    ok = bad = 0
    for uid in user_ids:
        try:
            async with pool_conn.transaction():
                if await grant(pool_conn, uid, rewards, f"{ref_prefix}_U{uid}", now):
                    ok += 1
        except Exception:
            bad += 1
            logger.exception("[PRIZE] %s игроку %s не выдан", ref_prefix, uid)
    return ok, bad


