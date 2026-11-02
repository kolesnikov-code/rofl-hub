"""
Робот-Стажёр и звания по стажу (решения владельца 22.10.2026).

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
    # владелец 02.11: каждое звание — через N часов после предыдущего
    def at(hours):
        return rank_key_for(T0 - timedelta(hours=hours), T0)
    assert rank_key_for(None, T0) is None
    assert at(0) == "rookie" and at(71) == "rookie"        # Новичок — сразу, первые 72 ч (защита от налётов)
    assert rank_key_for(T0 + timedelta(minutes=1), T0) == "rookie"   # часы сервера чуть врут — всё равно Новичок
    assert at(72) == "private"
    assert at(72 + 359) == "private" and at(72 + 360) == "fighter"
    assert at(432 + 720) == "captain"
    assert at(1152 + 2399) == "captain" and at(1152 + 2400) == "general"
    assert at(3552 + 4800) == "legend"
    assert at(8352 + 7199) == "legend" and at(8352 + 7200) == "overlord"
    assert at(100_000) == "overlord"                        # выше Властелина званий нет
    from shared.economy import RAID_NEWBIE_SHIELD_DAYS, RANKS
    assert RANKS[1][0] == RAID_NEWBIE_SHIELD_DAYS * 24      # Новичок кончается вместе с защитой от налётов


def test_rank_labels_are_translated_in_every_language():
    from shared.locales import t
    from shared.locales import SUPPORTED_LANGS
    from shared.economy import RANKS
    from shared.ranks import name_with_rank, rank_label
    assert rank_label("ru", T0 - timedelta(days=20), T0) == "Боец"
    assert rank_label("en", T0 - timedelta(days=20), T0) == "Fighter"
    for lang in SUPPORTED_LANGS:
        labels = [t(lang, f"rank.{key}") for _, key in RANKS]
        assert len(set(labels)) == 7, lang
        assert not {"ROFL", "LMAO", "KING"} & set(labels), lang
    assert name_with_rank("@tolya", "ru", T0 - timedelta(days=700), T0) == "@tolya · 🎖 Властелин"
    assert name_with_rank("@tolya", "ru", T0 - timedelta(hours=10), T0) == "@tolya · 🎖 Новичок"
    assert name_with_rank("@tolya", "ru", None, T0) == "@tolya"          # дата неизвестна — без хвоста


def test_account_deletion_rules():
    import shared.economy as e
    from shared.feature_flags import FLAG_DEFAULTS, FLAG_TITLES
    assert e.ACCOUNT_DELETE_GRACE_DAYS == 7
    assert e.ACCOUNT_DELETE_CONFIRM_SECONDS >= 5
    assert FLAG_DEFAULTS["account_delete"] is True and "account_delete" in FLAG_TITLES
    # переводы — тот же порог активности, что и у активного друга в рефералке
    assert (e.TRANSFER_SENDER_MIN_QUIZ_LEVEL, e.TRANSFER_SENDER_MIN_BONUS_CLAIMS) == \
        (e.REFERRAL_QUALIFY_QUIZ_LEVEL, e.REFERRAL_QUALIFY_BONUS_CLAIMS)


def test_account_deletion_texts_exist_in_ru_and_en():
    from shared.locales import t
    for lang in ("ru", "en"):
        warn = t(lang, "acct.warn", days=7, seconds=10)
        assert "7" in warn and "10" in warn and "Stars" in warn
        for key in ("profile.btn_delete", "acct.btn_keep", "acct.btn_confirm", "acct.btn_undo",
                    "acct.undone", "acct.purged", "acct.deleted_notice", "acct.welcome_back"):
            assert t(lang, key) and t(lang, key) != key
        assert "/start" in t(lang, "acct.purged")


def test_deletion_middleware_lets_through_only_undo_and_start():
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    import pytest
    pytest.importorskip("aiogram")
    from types import SimpleNamespace
    from aiogram.types import CallbackQuery, Message
    from bots.main_bot.middleware import _is_callback, _is_start
    cb = CallbackQuery.model_construct(data="acct_undo")
    msg = Message.model_construct(text="/start p_x")
    assert _is_callback(SimpleNamespace(callback_query=cb), "acct_undo")
    assert not _is_callback(SimpleNamespace(callback_query=cb), "games_hub")
    assert _is_start(SimpleNamespace(message=msg))
    assert not _is_start(SimpleNamespace(message=Message.model_construct(text="/farm")))


async def test_paid_update_passes_maintenance_and_block(monkeypatch):
    """Аудит 1.5: Stars уже списаны — техработы и блокировка не должны глушить доставку."""
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    import pytest
    pytest.importorskip("aiogram")
    from types import SimpleNamespace
    from aiogram.types import Message, SuccessfulPayment
    from bots.main_bot import middleware as mw

    class Pool:
        async def fetchrow(self, *a):
            return {"lang": "ru", "is_blocked": True, "deletion_requested_at": None, "deleted_at": None}

    async def flag_on(key):
        return True

    async def silent(*a, **k):
        return None

    monkeypatch.setattr(mw, "db", SimpleNamespace(is_connected=True, pool=Pool()))
    monkeypatch.setattr(mw, "get_flag", flag_on)
    m = mw.ActivityMiddleware()
    monkeypatch.setattr(m, "_reply_to_event", silent)
    calls = []

    async def handler(event, data):
        calls.append(event)

    user = SimpleNamespace(id=5, language_code="ru")
    paid = SimpleNamespace(message=Message.model_construct(successful_payment=SuccessfulPayment.model_construct()))
    plain = SimpleNamespace(message=Message.model_construct(text="/farm", successful_payment=None))
    await m(handler, paid, {"event_from_user": user})
    await m(handler, plain, {"event_from_user": user})
    assert calls == [paid]                      # оплата прошла, обычное сообщение — заглушено техработами
