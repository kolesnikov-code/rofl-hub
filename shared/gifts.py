"""
🎁 Подарки от разработчика (решение владельца 30.10).

«Подарить всем» в пульте создаёт РАЗДАЧУ (gift_campaigns), а не рассылку: тысячи личных сообщений разом — прямой путь
к ограничениям Telegram. Игрок видит подарок на плашке паспорта и забирает кнопкой; подарки копятся до expires_at.

Справедливость сезонных лимитов: деталь костюма (GEAR_SEASON_CAP) и артефакт (ARTIFACT_SEASON_CAP) бесплатно — не
больше лимита за сезон. Раздача, в которой есть только такие вещи, НЕ показывается тому, кто уже добрал лимит: вторая
раздача в конце месяца дойдёт до новичков и тех, кто ещё не получал, — старожилы второй раз не получат.
Выдача — shared/prizes.grant (идемпотентно по reward_grants, ключ GC<раздача>_U<игрок>) внутри транзакции.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from shared.economy import ARTIFACT_SEASON_CAP, GEAR_SEASON_CAP, GIFT_LIST_LIMIT

logger = logging.getLogger(__name__)

LIMITED_KINDS = ("gear", "artifact")


class GiftError(Exception):
    def __init__(self, key: str):
        self.key = key
        super().__init__(key)


def _rewards(raw) -> list[dict]:
    return json.loads(raw) if isinstance(raw, str) else list(raw or [])


async def caps_left(conn, user_id: int, now: datetime) -> dict[str, int]:
    """Сколько бесплатных деталей и артефактов игрок ещё может получить в этом сезоне."""
    from shared.gear import season_drops
    return {"gear": max(0, GEAR_SEASON_CAP - await season_drops(conn, user_id, now)),
            "artifact": max(0, ARTIFACT_SEASON_CAP - await season_drops(conn, user_id, now, artifacts=True))}


def worth_claiming(rewards: list[dict], left: dict[str, int]) -> bool:
    """Подарок имеет смысл: в нём есть что-то без лимита или лимит по его виду ещё не исчерпан."""
    return any(r.get("kind") not in LIMITED_KINDS or left.get(r["kind"], 0) > 0 for r in rewards)


async def create_campaign(conn, title: str, rewards: list[dict], expires_at: datetime) -> int:
    return await conn.fetchval(
        "INSERT INTO gift_campaigns (title, rewards, expires_at) VALUES ($1, $2::jsonb, $3) RETURNING id",
        title[:100], json.dumps(rewards, ensure_ascii=False), expires_at)


async def pending(conn, user_id: int, now: datetime) -> list[dict]:
    """Подарки игрока на плашке: открытые раздачи, которые он ещё не забрал и которые ему что-то дадут."""
    rows = await conn.fetch(
        """SELECT c.id, c.title, c.rewards, c.expires_at FROM gift_campaigns c
           WHERE NOT c.cancelled AND c.expires_at > $2
             AND NOT EXISTS (SELECT 1 FROM gift_claims g WHERE g.campaign_id = c.id AND g.user_id = $1)
           ORDER BY c.id LIMIT $3""", user_id, now, GIFT_LIST_LIMIT)
    if not rows:
        return []
    left = await caps_left(conn, user_id, now)
    out = []
    for r in rows:
        rewards = _rewards(r["rewards"])
        if worth_claiming(rewards, left):
            out.append({"id": r["id"], "title": r["title"], "rewards": rewards, "expires_at": r["expires_at"]})
    return out


async def claim(conn, user_id: int, campaign_id: int, now: datetime) -> dict:
    """Забрать подарок (внутри транзакции вызывающего). Возвращает {"rewards": …, "gear": [...], "artifacts": [...]}."""
    from shared.prizes import grant
    row = await conn.fetchrow("SELECT id, rewards, expires_at, cancelled FROM gift_campaigns WHERE id = $1", campaign_id)
    if row is None or row["cancelled"] or row["expires_at"] <= now:
        raise GiftError("gift.err_gone")
    user = await conn.fetchrow("SELECT is_blocked, deleted_at FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if user is None or user["is_blocked"] or user["deleted_at"] is not None:
        raise GiftError("common.no_profile")
    rewards = _rewards(row["rewards"])
    if not worth_claiming(rewards, await caps_left(conn, user_id, now)):
        raise GiftError("gift.err_limit")
    if not await conn.fetchval("INSERT INTO gift_claims (campaign_id, user_id) VALUES ($1, $2) ON CONFLICT DO NOTHING "
                               "RETURNING 1", campaign_id, user_id):
        raise GiftError("gift.err_taken")
    ref = f"GC{campaign_id}_U{user_id}"
    await grant(conn, user_id, rewards, ref, now)
    # что именно выпало (детали и артефакты случайны) — для окна «Подарок получен»
    got = await conn.fetch("SELECT suit, slot FROM gear_ledger WHERE user_id = $1 AND reason = 'drop' AND ref = $2 "
                           "ORDER BY id", user_id, ref)
    return {"rewards": rewards,
            "gear": [{"suit": g["suit"], "slot": g["slot"]} for g in got if g["slot"] != "art"],
            "artifacts": [g["suit"][1:] for g in got if g["slot"] == "art"]}


async def campaigns_admin(conn, limit: int = 20) -> list[dict]:
    rows = await conn.fetch(
        """SELECT c.id, c.title, c.rewards, c.created_at, c.expires_at, c.cancelled,
                  (SELECT COUNT(*) FROM gift_claims g WHERE g.campaign_id = c.id) AS claimed
           FROM gift_campaigns c ORDER BY c.id DESC LIMIT $1""", limit)
    return [{"id": r["id"], "title": r["title"], "rewards": _rewards(r["rewards"]), "claimed": r["claimed"],
             "created_at": r["created_at"].isoformat(), "expires_at": r["expires_at"].isoformat(),
             "cancelled": r["cancelled"]} for r in rows]


async def cancel(conn, campaign_id: int) -> bool:
    return bool(await conn.fetchval("UPDATE gift_campaigns SET cancelled = TRUE WHERE id = $1 AND NOT cancelled "
                                    "RETURNING 1", campaign_id))
