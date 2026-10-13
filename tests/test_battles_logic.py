"""
Битвы команд и кланов: чистая логика (номинации, парсер моментов, посты, призы).
"""
from datetime import datetime, timedelta, timezone

import pytest

from shared.battles import (
    BATTLE_NOMINATIONS,
    MAX_PRIZE_PLACES,
    build_announce_post,
    build_results_post,
    medals,
    parse_battle_moment,
    prizes_from_row,
    prizes_to_json,
)

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- номинации
def test_nominations_catalog_is_rich_and_well_formed():
    assert len(BATTLE_NOMINATIONS) >= 8  # владелец просил больше номинаций и азарта
    for key, nom in BATTLE_NOMINATIONS.items():
        assert nom["title"] and nom["unit"], key
        assert nom["kind"] in ("ledger_sum", "ledger_count", "ledger_sum_positive",
                               "ledger_count_like", "referrals", "stars"), key
        if nom["kind"] in ("ledger_sum", "ledger_count"):
            assert nom.get("reason"), key
        if nom["kind"] == "ledger_count_like":
            assert nom.get("reason_like"), key


def test_key_owner_nominations_present():
    """Номинации из ТЗ владельца: нафармить, дуэли, КНБ, викторина."""
    assert "farm_mined" in BATTLE_NOMINATIONS
    assert "duel_wins" in BATTLE_NOMINATIONS and "duels_played" in BATTLE_NOMINATIONS
    assert "rps_wins" in BATTLE_NOMINATIONS
    assert "quiz_wins" in BATTLE_NOMINATIONS


# ---------------------------------------------------------------- парсер моментов
def test_parse_moment_zero_hours_means_now():
    assert parse_battle_moment("0", base=NOW) == NOW


def test_parse_moment_hours_from_base():
    assert parse_battle_moment("168", base=NOW) == NOW + timedelta(hours=168)


def test_parse_moment_absolute_date_utc():
    parsed = parse_battle_moment("07.11.2026 18:00")
    assert parsed == datetime(2026, 11, 7, 18, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize("raw", ["завтра", "7d", "2026-11-07", "", "18:00"])
def test_parse_moment_rejects_garbage(raw):
    assert parse_battle_moment(raw, base=NOW) is None


# ---------------------------------------------------------------- призы
def test_prizes_json_round_trip():
    prizes = {1: {"mode": "sku", "value": "cutlet_50"},
              2: {"mode": "manual", "value": "Telegram Premium на месяц"}}
    restored = prizes_from_row(prizes_to_json(prizes))
    assert restored == prizes
    assert all(isinstance(k, int) for k in restored)


def test_max_prize_places_is_ten():
    assert MAX_PRIZE_PLACES == 10  # призы за 1–10 места по ТЗ владельца


# ---------------------------------------------------------------- посты
def _battle(nom_key="farm_mined"):
    return {"title": "Осенний Кубок", "nomination_key": nom_key,
            "nomination_text": "⛏️ Больше всех нафармить монет фермой",
            "starts_at": NOW, "ends_at": NOW + timedelta(days=7)}


def _scores(n):
    return [{"team_id": i, "team_name": f"Банда {i}", "is_clan": i == 1, "score": 1000 - i * 50}
            for i in range(1, n + 1)]


def test_medals():
    assert [medals(i) for i in (1, 2, 3, 4, 10)] == ["🥇", "🥈", "🥉", "4.", "10."]


def test_results_post_top3_bright_rest_modest():
    post = build_results_post(_battle(), _scores(10),
                              {1: "каждому бойцу — 🥩 Запас котлет (выдано: 12)"})
    assert "🥇 <b>Банда 1</b>" in post and "👑 КЛАН" in post
    assert "🥈 <b>Банда 2</b>" in post and "🥉 <b>Банда 3</b>" in post
    assert "4. Банда 4" in post and "<b>Банда 4</b>" not in post  # 4-10 скромнее тройки
    assert "10. Банда 10" in post
    assert "🎁 каждому бойцу — 🥩 Запас котлет" in post


def test_results_post_handles_empty_scores():
    post = build_results_post(_battle(), [], {})
    assert "Ни одна команда" in post


def test_announce_post_mentions_dates_and_team_motivation():
    post = build_announce_post(_battle())
    assert "Осенний Кубок" in post
    assert "01.11.2026 12:00" in post and "08.11.2026 12:00" in post
    assert "ОБЩИЙ результат" in post
