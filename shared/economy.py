"""
Единый источник чисел экономики ROFL HUB.

Все спорные величины из ТЗ живут ЗДЕСЬ и только здесь. Меняется константа —
меняется поведение всего бота. Никаких «магических чисел» в обработчиках.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------
# Валюта и стартовые бонусы
# --------------------------------------------------------------------------
START_BALANCE = 1000          # рофлов при регистрации
START_CUTLETS_INVENTORY = 1   # кибер-котлет на склад при регистрации
REFERRAL_SIGNUP_BONUS = 1000  # рофлов рефереру за регистрацию друга
REFERRAL_REVENUE_SHARE = 0.20  # доля от трат реферала (учёт для выплат)
REFERRAL_SHARE_DAYS = 365

# --------------------------------------------------------------------------
# Ферма: роботы
# --------------------------------------------------------------------------
MINER_RATE_PER_HOUR = {
    "junior": 5,    # Младший Майнер, топливо не нужно
    "premium": 10,  # Кибер-Бурильщик, ест котлеты
}
MINER_LICENSE_DAYS = 30
CUTLET_ENERGY_SECONDS = 24 * 3600   # одна котлета = 24 часа работы одного бурильщика
PREMIUM_CUTLETS_PER_CYCLE_BASE = 1  # котлет на цикл 24ч без буста
NUCLEAR_FUEL_MULTIPLIER = 3         # расход котлет при Ядерном разгоне
NUCLEAR_SPEED_MULTIPLIER = 5        # скорость добычи при Ядерном разгоне
NITROGEN_BONUS_PERCENT = 40         # Азотное охлаждение: +40% к базовой мощности
BOOST_DAYS = 30
DRONE_DAYS = 365
DAILY_CUTLET_BONUS_COOLDOWN_SECONDS = 24 * 3600

# Внутренняя точность начислений: копим рофло-микросекунды, чтобы ни одна
# «копейка времени» не терялась между ленивыми пересчётами.
MINING_ACC_PER_ROFL = 3600 * 1_000_000  # µs работы на 1 рофл при ставке 1 рофл/ч

# --------------------------------------------------------------------------
# Игры и лимиты
# --------------------------------------------------------------------------
WIN_REWARD = 2
LOSE_PENALTY = 1
DAILY_WIN_LIMITS = {
    "quiz": 30,
    "rps": 15,
    "hl": 15,
    "coin": 15,
    "dice": 15,
    "safe": 15,
}
DEFAULT_DAILY_WIN_LIMIT = 15
QUIZ_ANSWER_SECONDS = 10
QUIZ_ANSWERS_PER_LEVEL = 30
QUIZ_LEVEL_UP_BONUS = 500
UNLIMIT_DAY_HOURS = 24
UNLIMIT_MONTH_DAYS = 30

# --------------------------------------------------------------------------
# Команды, дуэли, турниры
# --------------------------------------------------------------------------
TEAM_CREATE_COST = 100_000
TEAM_MAX_MEMBERS = 50
MEGA_CLAN_MAX_MEMBERS = 1000
DUEL_BURN_PERCENT = 20
TOURNAMENT_ENTRY_FEE = 5000
TOURNAMENT_WINNERS_PERCENT = 1


# --------------------------------------------------------------------------
# Общие чистые помощники (без БД, без Telegram)
# --------------------------------------------------------------------------
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def extend_expiry(current: datetime | None, now: datetime, days: int) -> datetime:
    """
    Продление срочной лицензии (буст, безлимит, дрон).

    Если лицензия ещё активна — прибавляем дни к её концу (покупки складываются).
    Если истекла или не было — отсчитываем от «сейчас».
    """
    if days <= 0:
        raise ValueError("days must be positive")
    base = now
    if current is not None and current > now:
        base = current
    return base + timedelta(days=days)


def extend_expiry_hours(current: datetime | None, now: datetime, hours: int) -> datetime:
    if hours <= 0:
        raise ValueError("hours must be positive")
    base = now
    if current is not None and current > now:
        base = current
    return base + timedelta(hours=hours)


def is_active(expiry: datetime | None, now: datetime) -> bool:
    return expiry is not None and expiry > now


def miner_hourly_rate(kind: str, *, nuclear_active: bool = False, nitrogen_active: bool = False) -> int:
    """
    Ставка робота в рофлах/час с учётом бустов. Эффекты складываются:
    Азот +40% к базе (5→7, 10→14), затем Ядерный разгон ×5 (7→35, 14→70).
    """
    rate = MINER_RATE_PER_HOUR[kind]
    if nitrogen_active:
        rate = rate * (100 + NITROGEN_BONUS_PERCENT) // 100
    if nuclear_active:
        rate *= NUCLEAR_SPEED_MULTIPLIER
    return rate


def cutlets_per_cycle(nuclear_active: bool) -> int:
    """Сколько котлет съедает один бурильщик при старте цикла 24ч."""
    return PREMIUM_CUTLETS_PER_CYCLE_BASE * (NUCLEAR_FUEL_MULTIPLIER if nuclear_active else 1)


def daily_bonus_seconds_left(last_claim: datetime | None, now: datetime) -> int:
    """0 — бонус доступен; иначе сколько секунд ждать (округление вверх)."""
    if last_claim is None:
        return 0
    passed = (now - last_claim).total_seconds()
    left = DAILY_CUTLET_BONUS_COOLDOWN_SECONDS - passed
    return max(0, -int(-left // 1))  # ceil


def tournament_winners_count(participants: int) -> int:
    """1% участников, округление вверх в пользу игрока: 30 участников → 1 победитель."""
    if participants <= 0:
        return 0
    return -(-participants * TOURNAMENT_WINNERS_PERCENT // 100)  # ceil


def duel_payout(stake_each: int) -> tuple[int, int]:
    """Возвращает (выплата победителю, сожжено) для дуэли с равными ставками."""
    if stake_each <= 0:
        raise ValueError("stake must be positive")
    bank = stake_each * 2
    burned = bank * DUEL_BURN_PERCENT // 100
    return bank - burned, burned
