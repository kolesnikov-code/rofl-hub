"""
Робот Стажёр и звания по стажу (решения владельца 22.10.2026).

- Стажёр: бесплатный, вечный, 1 монета/ч, без топлива, бусты действуют;
- +1 Стажёр за каждый уровень интеллекта, кратный 10;
- звания: 1 день → Новичок … 1 год → KING; меньше суток — без звания.
"""
from datetime import datetime, timedelta, timezone

from shared.economy import (
    INTERN_LEVEL_STEP,
    INTERN_UPGRADE_REFERRALS,
    MINER_RATE_PER_HOUR,
    interns_for_level,
    miner_hourly_rate,
    permanent_expiry,
    rank_key_for,
)
from shared.farm_logic import MinerState, farm_counts, simulate_farm

T0 = datetime(2026, 10, 22, 0, 0, tzinfo=timezone.utc)


def intern(miner_id=1, bought=T0) -> MinerState:
    return MinerState(miner_id, "intern", bought, permanent_expiry(bought))


# ---------------------------------------------------------------- Стажёр в движке
def test_intern_rate_is_one_coin_and_boosts_apply():
    assert MINER_RATE_PER_HOUR["intern"] == 1
    assert miner_hourly_rate("intern") == 1
    assert miner_hourly_rate("intern", nitrogen_active=True) == 1       # +40% от 1 → 1 (целые)
    assert miner_hourly_rate("intern", nuclear_active=True) == 5        # ×5 — буст работает и на бесплатном


def test_intern_mines_one_coin_per_hour_without_fuel():
    tick = simulate_farm(last_update=T0, now=T0 + timedelta(hours=24), fridge_cutlets=0,
                         acc=0, miners=[intern()])
    assert tick.earned == 24
    assert tick.cutlets_consumed == 0
    assert tick.expired_ids == []


def test_intern_is_eternal_even_after_years():
    tick = simulate_farm(last_update=T0, now=T0 + timedelta(days=365 * 3), fridge_cutlets=0,
                         acc=0, miners=[intern()])
    assert tick.expired_ids == []
    assert tick.earned == 24 * 365 * 3


def test_intern_counts_separately_from_juniors():
    miners = [intern(1), intern(2), MinerState(3, "junior", T0, T0 + timedelta(days=30))]
    assert farm_counts(miners, T0) == {"intern": 2, "junior": 1, "premium": 0, "premium_fueled": 0}


def test_permanent_expiry_is_far_future():
    assert permanent_expiry(T0).year == T0.year + 100


# ---------------------------------------------------------------- Стажёры за интеллект
def test_intern_only_for_every_tenth_intellect_level():
    """Решение владельца 26.10 (вечер): Стажёр при активации + за уровни 10, 20, 30… — и всё."""
    assert INTERN_LEVEL_STEP == 10
    assert interns_for_level(0) == 0
    assert interns_for_level(9) == 0
    assert interns_for_level(10) == 1
    assert interns_for_level(25) == 2
    assert interns_for_level(50) == 5


def test_referral_pays_only_for_an_active_friend():
    """Решение владельца 26.10: за регистрацию — ничего; +500 один раз за активного друга."""
    import shared.economy as e
    assert not hasattr(e, "REFERRAL_SIGNUP_BONUS")
    assert e.REFERRAL_QUALIFIED_BONUS == 500
    assert (e.REFERRAL_QUALIFIED_CUTLETS, e.REFERRAL_QUALIFIED_RESOURCES) == (1, 10)
    assert e.REFERRAL_QUALIFY_QUIZ_LEVEL == 3
    assert e.REFERRAL_QUALIFY_BONUS_CLAIMS == 3
    # 3 уровень интеллекта = 10 + 20 + 30 верных ответов — больше суточного лимита викторины
    assert sum(e.quiz_answers_required(n) for n in range(1, e.REFERRAL_QUALIFY_QUIZ_LEVEL + 1)) > \
        e.DAILY_WIN_LIMITS["quiz"]


def test_claim_button_texts_exist():
    from shared.locales import STRINGS
    for lang in ("ru", "en"):
        assert "{n}" in STRINGS[lang]["farm.btn_claim_intern"]
        assert STRINGS[lang]["games.intern_ready"].strip()


def test_upgrade_requires_three_qualified_referrals():
    assert INTERN_UPGRADE_REFERRALS == 3


# ---------------------------------------------------------------- Звания
def test_rank_thresholds():
    assert rank_key_for(None, T0) is None
    assert rank_key_for(T0 - timedelta(hours=23), T0) is None          # меньше суток — без звания
    assert rank_key_for(T0 - timedelta(days=1), T0) == "rookie"
    assert rank_key_for(T0 - timedelta(days=6), T0) == "rookie"
    assert rank_key_for(T0 - timedelta(days=7), T0) == "fighter"
    assert rank_key_for(T0 - timedelta(days=30), T0) == "legend"
    assert rank_key_for(T0 - timedelta(days=90), T0) == "rofl"
    assert rank_key_for(T0 - timedelta(days=180), T0) == "lmao"
    assert rank_key_for(T0 - timedelta(days=365), T0) == "king"
    assert rank_key_for(T0 - timedelta(days=3000), T0) == "king"      # выше KING звания нет


def test_rank_labels_localized_and_latin_top_ranks():
    from shared.locales import t
    from shared.ranks import name_with_rank, rank_label
    assert rank_label("ru", T0 - timedelta(days=7), T0) == "Боец"
    assert rank_label("en", T0 - timedelta(days=7), T0) == "Fighter"
    for lang in ("ru", "en", "es", "zh", "ar"):
        assert t(lang, "rank.rofl") == "ROFL" and t(lang, "rank.king") == "KING"
    assert name_with_rank("@tolya", "ru", T0 - timedelta(days=400), T0) == "@tolya · 🎖 KING"
    assert name_with_rank("@tolya", "ru", T0, T0) == "@tolya"           # новичок без звания — без хвоста
