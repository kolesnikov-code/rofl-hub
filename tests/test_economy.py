from datetime import datetime, timedelta, timezone

import pytest

from shared import economy
from shared.economy import (
    duel_payout,
    extend_expiry,
    extend_expiry_hours,
    is_active,
    tournament_winners_count,
)

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


def test_tz_constants():
    assert economy.MINER_RATE_PER_HOUR == {"intern": 1, "junior": 5, "premium": 10}
    assert economy.MINER_LICENSE_DAYS == 30
    assert economy.DAILY_WIN_LIMITS["quiz"] == 30
    assert economy.TEAM_CREATE_COST == 100_000
    assert economy.MEGA_CLAN_MAX_MEMBERS == 1000
    assert economy.DUEL_BURN_PERCENT == 20
    assert economy.TOURNAMENT_ENTRY_FEE == 5000


def test_extend_expiry_from_now_when_no_license():
    assert extend_expiry(None, NOW, 30) == NOW + timedelta(days=30)


def test_extend_expiry_from_now_when_expired():
    expired = NOW - timedelta(days=3)
    assert extend_expiry(expired, NOW, 30) == NOW + timedelta(days=30)


def test_extend_expiry_stacks_when_active():
    active = NOW + timedelta(days=10)
    assert extend_expiry(active, NOW, 30) == NOW + timedelta(days=40)


def test_extend_expiry_hours():
    assert extend_expiry_hours(None, NOW, 24) == NOW + timedelta(hours=24)
    assert extend_expiry_hours(NOW + timedelta(hours=5), NOW, 24) == NOW + timedelta(hours=29)


def test_extend_expiry_rejects_nonpositive():
    with pytest.raises(ValueError):
        extend_expiry(None, NOW, 0)
    with pytest.raises(ValueError):
        extend_expiry_hours(None, NOW, -1)


def test_is_active():
    assert not is_active(None, NOW)
    assert not is_active(NOW, NOW)
    assert is_active(NOW + timedelta(seconds=1), NOW)


@pytest.mark.parametrize("participants,winners", [
    (0, 0), (1, 1), (30, 1), (99, 1), (100, 1), (101, 2), (1000, 10), (10_000, 100), (12_345, 124),
])
def test_tournament_winners_round_up_in_favor_of_players(participants, winners):
    assert tournament_winners_count(participants) == winners


def test_duel_payout_burns_20_percent():
    assert duel_payout(10) == (16, 4)
    assert duel_payout(5000) == (8000, 2000)
    payout, burned = duel_payout(7)
    assert payout + burned == 14
    with pytest.raises(ValueError):
        duel_payout(0)
