"""
📜 История игрока за HISTORY_DAYS дней (решение владельца 26.10): откуда пришли монеты, куда ушли ресурсы,
что продано и куплено на бирже, какие награды и подарки получены.

GET /api/history?tab=coins|res|market|gifts — только чтение журналов (ledger, resource_ledger, market_trades,
reward_grants); причины журналов переводятся в понятные подписи на языке игрока (ключи hist.*).
"""
from __future__ import annotations

import json
from datetime import timedelta

from aiohttp import web

from bots.main_bot.webapp_game import _ctx
from shared.database import db
from shared.economy import utcnow
from shared.locales import t

HISTORY_DAYS = 30
HISTORY_LIMIT = 500          # записей на вкладку (листаются постранично в приложении)
HISTORY_TOP = 5              # источников/трат в сводке
HISTORY_TABS = ("coins", "res", "market", "gifts")
# Причина журнала (до двоеточия) → ключ подписи hist.<…>; неизвестные — «hist.other»
HISTORY_REASONS = (
    "mining", "game_win", "game_loss", "quiz_level_up", "duel_stake", "duel_win", "duel_refund",
    "market_buy", "market_sell", "market_bid", "market_bid_refund", "market_escrow", "market_refund",
    "swap_escrow", "swap_give", "swap_get", "swap_refund", "transfer_in", "transfer_out", "admin_gift", "prize",
    "daily_chest", "quest_reward", "quest_hint", "quiz_hint", "shop_coins", "auction_bid", "auction_refund", "craft", "weekly",
    "horse_buy", "drone_buy", "team_create", "referral_qualified", "signup_bonus", "account_deleted",
    "raid_loot", "raid_loss", "raid_fail", "raid_defense", "raid_fuel", "exp_fuel", "exp_gear", "exp_refund",
    "station_donate", "battle_entry", "mine", "tools", "tech", "shuttle_charge", "team_help_give", "team_help_get",
    "gear_upgrade", "gear_exo", "suit_miner", "daily_case", "squad_create", "squad_upgrade",
)


def reason_key(reason: str) -> str:
    base = (reason or "").split(":", 1)[0]
    return base if base in HISTORY_REASONS else "other"


def reason_label(lang: str, reason: str) -> str:
    return t(lang, f"hist.{reason_key(reason)}")


def gift_source(lang: str, ref: str) -> str:
    """Откуда награда: битва (B…), поход (E…), подарок из пульта (GIFT…) — по префиксу ключа выдачи."""
    if ref.startswith("GIFT"):
        return t(lang, "hist.src_gift")
    if ref.startswith("B"):
        return t(lang, "hist.src_battle")
    if ref.startswith("E"):
        return t(lang, "hist.src_exp")
    return t(lang, "hist.prize")


def summarize(rows: list, lang: str) -> dict:
    """Сводка: сколько пришло и ушло и главные источники/траты (по подписям)."""
    income, spent, by_label = 0, 0, {}
    for r in rows:
        d = int(r["delta"])
        if d > 0:
            income += d
        else:
            spent -= d
        label = reason_label(lang, r["reason"])
        by_label[label] = by_label.get(label, 0) + d
    top_in = sorted(((k, v) for k, v in by_label.items() if v > 0), key=lambda kv: -kv[1])[:HISTORY_TOP]
    top_out = sorted(((k, v) for k, v in by_label.items() if v < 0), key=lambda kv: kv[1])[:HISTORY_TOP]
    return {"income": income, "spent": spent, "top_in": [{"label": k, "sum": v} for k, v in top_in],
            "top_out": [{"label": k, "sum": v} for k, v in top_out]}


async def handle_history(request: web.Request) -> web.Response:
    from shared.prizes import normalize_rewards, rewards_label
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    tab = request.query.get("tab", "coins")
    tab = tab if tab in HISTORY_TABS else "coins"
    since = utcnow() - timedelta(days=HISTORY_DAYS)
    out: dict = {"tab": tab, "days": HISTORY_DAYS, "items": [], "summary": None}
    async with db.pool.acquire() as conn:
        if tab == "coins":
            rows = await conn.fetch("SELECT delta, reason, created_at FROM ledger WHERE user_id = $1 AND created_at >= $2 "
                                    "AND delta <> 0 ORDER BY created_at DESC, id DESC LIMIT $3", ctx.user_id, since, HISTORY_LIMIT)
            out["items"] = [{"at": r["created_at"].isoformat(), "delta": int(r["delta"]),
                             "label": reason_label(ctx.lang, r["reason"])} for r in rows]
            out["summary"] = summarize(rows, ctx.lang)
        elif tab == "res":
            rows = await conn.fetch("SELECT kind, delta, reason, created_at FROM resource_ledger WHERE user_id = $1 "
                                    "AND created_at >= $2 AND delta <> 0 ORDER BY created_at DESC, id DESC LIMIT $3",
                                    ctx.user_id, since, HISTORY_LIMIT)
            out["items"] = [{"at": r["created_at"].isoformat(), "delta": int(r["delta"]), "kind": r["kind"],
                             "label": reason_label(ctx.lang, r["reason"])} for r in rows]
        elif tab == "market":
            rows = await conn.fetch(
                "SELECT asset, qty, price, buyer_id, seller_id, created_at FROM market_trades "
                "WHERE (buyer_id = $1 OR seller_id = $1) AND created_at >= $2 ORDER BY created_at DESC, id DESC LIMIT $3",
                ctx.user_id, since, HISTORY_LIMIT)
            out["items"] = [{"at": r["created_at"].isoformat(), "side": "buy" if r["buyer_id"] == ctx.user_id else "sell",
                             "asset": r["asset"], "qty": r["qty"], "price": r["price"], "total": r["qty"] * r["price"]}
                            for r in rows]
        else:
            rows = await conn.fetch("SELECT ref, payload, created_at FROM reward_grants WHERE user_id = $1 "
                                    "AND created_at >= $2 ORDER BY created_at DESC LIMIT $3", ctx.user_id, since, HISTORY_LIMIT)
            for r in rows:
                raw = r["payload"]
                rewards = normalize_rewards(json.loads(raw) if isinstance(raw, str) else (raw or []))
                out["items"].append({"at": r["created_at"].isoformat(), "label": gift_source(ctx.lang, r["ref"]),
                                     "what": rewards_label(rewards)})
    return web.json_response(out)


def register_history_routes(app: web.Application) -> None:
    app.router.add_get("/api/history", handle_history)
