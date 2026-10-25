"""
Ежедневные цели (волна 22.10, вечер): 3 цели на день и сундук за все три.

- набор целей детерминирован по (игрок, дата UTC): у каждого свой, но стабильный в течение дня;
- прогресс считается ТОЛЬКО по транзакционным таблицам (ledger, raids, resource_ledger,
  team_donations, market_trades, users) — аналитика (events) не участвует, цели не зависят от неё;
- сундук забирается один раз в день (daily_goal_claims), монеты — через ledger
  reason='daily_chest', ресурс — через resource_ledger; серия дней подряд (users.goal_streak)
  каждые DAILY_STREAK_BONUS_EVERY дней добавляет DAILY_STREAK_BONUS_COINS.
"""
from __future__ import annotations

import hashlib
import logging
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from shared.economy import (
    DAILY_CHEST_COINS,
    CHEST_SPECIALS,
    CHEST_STREAK_COW,
    DAILY_CHEST_RESOURCE,
    DAILY_STREAK_BONUS_EVERY,
    DAILY_GOALS_PER_DAY,
    DAILY_STREAK_BONUS_COINS,
    DAILY_STREAK_BONUS_EVERY,
    RESOURCE_KINDS,
)
from shared.ledger import change_balance
from shared.locales import t
from shared.resources import change_resource, resource_capacity

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Goal:
    key: str          # ключ локали goal.<key>
    target: int
    feature: str | None = None   # тумблер пульта, без которого цель недостижима


# Пул целей: разнообразие вкусов — игры, дуэли, ферма, мастерская, налёты, биржа, команда
GOAL_POOL: tuple[Goal, ...] = (
    Goal("win_quiz", 5, "games"),
    Goal("win_rps", 5, "games"),
    Goal("win_hl", 5, "games"),
    Goal("win_safe", 2, "games"),
    Goal("play_rounds", 15, "games"),
    Goal("duel", 1, "duels"),
    Goal("bonus", 1),
    Goal("craft", 1, "workshop"),
    Goal("raid", 1, "raids"),
    Goal("market_deal", 1, "market"),
    Goal("donate", 1, "station"),
)


class GoalsError(Exception):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def goals_for(user_id: int, day: date, enabled_features: set[str] | None = None,
              count: int = DAILY_GOALS_PER_DAY) -> list[Goal]:
    """Детерминированный набор целей на день (одинаков при любом числе вызовов)."""
    pool = [g for g in GOAL_POOL
            if enabled_features is None or g.feature is None or g.feature in enabled_features]
    if not pool:
        return []
    seed = int(hashlib.sha256(f"{user_id}:{day.isoformat()}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    return rng.sample(pool, min(count, len(pool)))


def chest_coins(streak: int) -> int:
    """Монеты сундука с учётом серии (каждый 7-й день подряд — жирнее)."""
    bonus = DAILY_STREAK_BONUS_COINS if streak > 0 and streak % DAILY_STREAK_BONUS_EVERY == 0 else 0
    return DAILY_CHEST_COINS + bonus


def next_streak(last_claim: date | None, today: date, current: int) -> int:
    """Серия: вчера забирал — продолжаем, иначе начинаем заново."""
    if last_claim == today - timedelta(days=1):
        return current + 1
    return 1


def chest_resource_kind(user_id: int, day: date) -> str:
    seed = int(hashlib.sha256(f"chest:{user_id}:{day.isoformat()}".encode()).hexdigest()[:16], 16)
    return RESOURCE_KINDS[seed % len(RESOURCE_KINDS)]


async def goal_progress(conn, user_id: int, goals: list[Goal], day: date) -> dict[str, int]:
    """Прогресс каждой цели по транзакционным таблицам за день day (UTC)."""
    start = datetime(day.year, day.month, day.day, tzinfo=__import__("datetime").timezone.utc)
    end = start + timedelta(days=1)
    progress: dict[str, int] = {}
    for g in goals:
        if g.key.startswith("win_"):
            game = g.key[4:]
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM ledger WHERE user_id = $1 AND reason = $2 "
                "AND created_at >= $3 AND created_at < $4", user_id, f"game_win:{game}", start, end)
        elif g.key == "play_rounds":
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM ledger WHERE user_id = $1 "
                "AND (reason LIKE 'game_win:%' OR reason LIKE 'game_loss:%') "
                "AND created_at >= $2 AND created_at < $3", user_id, start, end)
        elif g.key == "duel":
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM ledger WHERE user_id = $1 AND reason = 'duel_stake' "
                "AND created_at >= $2 AND created_at < $3", user_id, start, end)
        elif g.key == "bonus":
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM users WHERE user_id = $1 AND last_bonus_claim_at >= $2 "
                "AND last_bonus_claim_at < $3", user_id, start, end)
        elif g.key == "craft":
            value = await conn.fetchval(
                "SELECT COUNT(DISTINCT reason) FROM resource_ledger WHERE user_id = $1 "
                "AND reason LIKE 'craft:%' AND created_at >= $2 AND created_at < $3",
                user_id, start, end)
        elif g.key == "raid":
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM raids WHERE attacker_id = $1 "
                "AND created_at >= $2 AND created_at < $3", user_id, start, end)
        elif g.key == "market_deal":
            # любая сделка на бирже — как покупатель или как продавец (включая заявки на покупку)
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM market_trades WHERE (buyer_id = $1 OR seller_id = $1) "
                "AND created_at >= $2 AND created_at < $3", user_id, start, end)
        elif g.key == "donate":
            value = await conn.fetchval(
                "SELECT COUNT(*) FROM team_donations WHERE user_id = $1 "
                "AND created_at >= $2 AND created_at < $3", user_id, start, end)
        else:
            value = 0
        progress[g.key] = min(int(value or 0), g.target)
    return progress


def all_done(goals: list[Goal], progress: dict[str, int]) -> bool:
    return bool(goals) and all(progress.get(g.key, 0) >= g.target for g in goals)


async def claimed_today(conn, user_id: int, day: date) -> bool:
    return bool(await conn.fetchval(
        "SELECT 1 FROM daily_goal_claims WHERE user_id = $1 AND day = $2", user_id, day))


async def claim_chest(conn, user_id: int, goals: list[Goal], day: date) -> dict:
    """
    Выдаёт сундук, если все цели закрыты и сегодня ещё не забирали.
    Возвращает {coins, kind, qty, streak}. Внутри транзакции вызывающего кода.
    """
    user = await conn.fetchrow(
        "SELECT goal_streak, goal_last_claim FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        raise GoalsError("common.no_profile")
    inserted = await conn.fetchval(
        "INSERT INTO daily_goal_claims (user_id, day) VALUES ($1, $2) "
        "ON CONFLICT DO NOTHING RETURNING 1", user_id, day)
    if not inserted:
        raise GoalsError("goal.err_claimed")
    progress = await goal_progress(conn, user_id, goals, day)
    if not all_done(goals, progress):
        raise GoalsError("goal.err_not_done")

    streak = next_streak(user["goal_last_claim"], day, user["goal_streak"])
    coins = chest_coins(streak)
    kind = chest_resource_kind(user_id, day)
    await change_balance(conn, user_id, coins, "daily_chest", day.isoformat())
    await change_resource(conn, user_id, kind, DAILY_CHEST_RESOURCE, "daily_chest", day.isoformat(),
                          cap=await resource_capacity(conn, user_id))
    # Особый бонус сундука (27.10): древесина / камень / электричество по дню; 7-й день серии — корова
    sp_kind, sp_qty = chest_special(user_id, day)
    cap = await resource_capacity(conn, user_id)
    await change_resource(conn, user_id, sp_kind, sp_qty, "daily_chest", day.isoformat(), cap=cap)
    cow = CHEST_STREAK_COW if streak % DAILY_STREAK_BONUS_EVERY == 0 else 0
    if cow:
        await change_resource(conn, user_id, "cow", cow, "daily_chest", day.isoformat(), cap=cap)
    await conn.execute("UPDATE users SET goal_streak = $2, goal_last_claim = $3 WHERE user_id = $1",
                       user_id, streak, day)
    logger.info("[GOALS] chest user=%s day=%s coins=%s %s=%s streak=%s",
                user_id, day, coins, kind, DAILY_CHEST_RESOURCE, streak)
    return {"coins": coins, "kind": kind, "qty": DAILY_CHEST_RESOURCE, "streak": streak,
            "special": {sp_kind: sp_qty, **({"cow": cow} if cow else {})}}


def chest_special(user_id: int, day) -> tuple[str, int]:
    """Особый ресурс сундука: детерминирован по (игрок, дата), как и цели."""
    return CHEST_SPECIALS[(user_id + day.toordinal()) % len(CHEST_SPECIALS)]
