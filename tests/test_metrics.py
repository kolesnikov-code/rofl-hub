"""
Юнит-тесты аналитики: чистые формулы метрик, расписание демона, разбор источника
трафика, нарезка отчётов и отказоустойчивость track()/mark_daily_activity().
Крайние случаи обязательны: 0 игроков, деление на ноль, пустые когорты.
"""
import asyncio

import pytest

from shared.analytics import mark_daily_activity, parse_source, track
from shared.economy import PROMOTER_CODE_MAX_LEN
from shared.metrics import (
    TG_MESSAGE_LIMIT,
    arppu,
    arpu,
    build_daily_report,
    build_express_report,
    delta_str,
    k_factor,
    net_inflation,
    pct,
    ratio,
    report_kind_for_hour,
    split_message,
    stickiness,
)


# ---------------------------------------------------------------- формулы
def test_ratio_and_pct_zero_denominator():
    assert ratio(5, 0) == 0.0
    assert pct(5, 0) == 0.0
    assert ratio(0, 0) == 0.0
    assert pct(30, 120) == 25.0


def test_k_factor_empty_cohort_and_normal():
    assert k_factor(10, 0) == 0.0          # пустая когорта не роняет отчёт
    assert k_factor(0, 50) == 0.0
    assert k_factor(25, 50) == 0.5


def test_stickiness_arpu_arppu_division_by_zero():
    assert stickiness(0, 0) == 0.0
    assert stickiness(30, 100) == 30.0
    assert arpu(500, 0) == 0.0
    assert arppu(500, 0) == 0.0            # 0 платящих — никакого ZeroDivisionError
    assert arpu(500, 100) == 5.0
    assert arppu(500, 10) == 50.0


def test_net_inflation_sign():
    assert net_inflation(1000, 400) == 600
    assert net_inflation(400, 1000) == -600
    assert net_inflation(0, 0) == 0


# ---------------------------------------------------------------- расписание
def test_report_schedule_matches_spec():
    assert report_kind_for_hour(0) == "daily"
    for h in (6, 12, 18):
        assert report_kind_for_hour(h) == "express"
    for h in (1, 5, 7, 11, 13, 17, 19, 23):
        assert report_kind_for_hour(h) is None


# ---------------------------------------------------------------- нарезка
def test_split_message_respects_telegram_limit():
    text = "\n".join(f"строка {i} " + "x" * 80 for i in range(300))
    parts = split_message(text)
    assert len(parts) > 1
    assert all(len(p) <= TG_MESSAGE_LIMIT for p in parts)
    assert "".join(p.replace("\n", "") for p in parts) == text.replace("\n", "")


def test_split_message_handles_oversized_single_line():
    text = "y" * (TG_MESSAGE_LIMIT * 2 + 10)
    parts = split_message(text)
    assert all(len(p) <= TG_MESSAGE_LIMIT for p in parts)
    assert sum(len(p) for p in parts) == len(text)


def test_split_message_short_text_single_part():
    assert split_message("привет") == ["привет"]


# ---------------------------------------------------------------- дельты
def test_delta_str():
    assert delta_str(10, 7) == " (+3)"
    assert delta_str(7, 10) == " (-3)"
    assert delta_str(5, 5) == " (=)"
    assert delta_str(5, None) == ""        # первого среза ещё не было
    assert delta_str(None, 5) == ""
    assert delta_str(1.5, 1.25) == " (+0.25)"


# ---------------------------------------------------------------- источники
def test_parse_source_referral_and_organic():
    assert parse_source("123456", referrer_id=123456) == "referral"
    assert parse_source(None, None) == "organic"
    assert parse_source("", None) == "organic"
    assert parse_source("auction_5", None) == "organic"


def test_parse_source_promoter_and_channel_codes():
    assert parse_source("p_blogger1", None) == "p_blogger1"
    assert parse_source("c_tiktok-ad", None) == "c_tiktok-ad"
    assert parse_source("p_BLOGGER1", None) == "p_blogger1"   # регистр нормализуется
    assert parse_source("p_имя", None) == "organic"           # не-латиница — мимо
    assert parse_source("p_" + "a" * (PROMOTER_CODE_MAX_LEN + 1), None) == "organic"
    assert parse_source("p_", None) == "organic"


def test_parse_source_telegram_affiliate_is_separate_channel():
    assert parse_source("_tgr_AbCdEf", None) == "tg_affiliate"


# ---------------------------------------------------------------- отказоустойчивость
def test_track_never_raises_without_database():
    """БД не подключена — track() молча пишет warning и не бросает."""
    asyncio.run(track(1, "game_round", game="rps", result="win"))


def test_mark_daily_activity_never_raises_without_database():
    asyncio.run(mark_daily_activity(1))


# ---------------------------------------------------------------- форматтеры
def _fake_snapshot() -> dict:
    return {
        "period": {"since": "2026-10-12T00:00:00+00:00", "until": "2026-10-13T00:00:00+00:00"},
        "acquisition": {"new_total": 7,
                        "by_source": [{"source": "organic", "n": 4}, {"source": "p_blog", "n": 3}],
                        "by_lang": [{"lang": "ru", "n": 5}, {"lang": "uz", "n": 2}],
                        "top_channels": [{"source": "p_blog", "regs": 3, "qualified": 1}]},
        "funnel": {"registered": 7, "onboarded": 6, "played": 5, "paid": 1},
        "activity": {"dau": 10, "wau": 20, "mau": 40, "stickiness_pct": 25.0},
        "virality_7d": {"cohort_size": 7, "k_raw": 0.43, "k_qualified": 0.14,
                        "inviter_share_pct": 28.6, "median_cycle_hours": 5.5},
        "monetization": {"revenue_stars": 150, "payers": 2, "purchases": 3,
                         "cr_mau_pct": 5.0, "cr_base_pct": 2.0,
                         "arpu_stars": 3.75, "arppu_stars": 75.0,
                         "by_sku": [{"sku": "coins_5k", "n": 1, "stars": 149}],
                         "by_lang": [{"lang": "ru", "stars": 150}],
                         "by_source": [{"source": "organic", "stars": 150}],
                         "first_purchase_sku": [{"sku": "unlimit_24h", "n": 2}],
                         "median_hours_to_first_purchase": 26.0,
                         "repeat_buyers_pct": 50.0,
                         "limit_hit_users": 4, "limit_to_unlimit_pct": 25.0},
        "economy": {"emission": 900, "burn": 300, "net_inflation": 600,
                    "emission_by_reason": [{"reason": "mining", "coins": 700}],
                    "burn_by_reason": [{"reason": "game_loss:quiz", "coins": 200}],
                    "coin_supply": 50_000, "top1pct_share_pct": 40.0},
        "games_farm": {"games": [{"game": "quiz", "rounds": 30, "winrate_pct": 60.0}],
                       "limit_hits": [{"game": "quiz", "n": 4}],
                       "miners_active": 3, "miners_burned": 1,
                       "drill_owners": 2, "hungry_drill_owners_pct": 50.0},
    }


def test_express_report_contains_key_numbers_and_deltas():
    snap, prev = _fake_snapshot(), _fake_snapshot()
    prev["activity"]["dau"] = 7
    text = build_express_report(snap, prev, hour=12)
    assert "DAU: <b>10</b> (+3)" in text
    assert "★ 150" in text and "K-qualified" in text and "p_blog" in text
    assert len(text) <= TG_MESSAGE_LIMIT


def test_express_report_without_previous_snapshot():
    text = build_express_report(_fake_snapshot(), None, hour=6)
    assert "(н/д)" not in text        # нет prev — просто без дельт
    assert "DAU: <b>10</b>" in text


def test_daily_report_renders_all_blocks_and_escapes_html():
    retention = [{"cohort": "2026-10-12", "size": 5, "d1_pct": 40.0,
                  "d3_pct": None, "d7_pct": None, "d30_pct": None}]
    spend = [{"cohort": "f2p", "size": 10, "active_7d_pct": 30.0,
              "favorite_game": "<quiz>", "k_qualified_30d": 0.1}]
    text = build_daily_report(_fake_snapshot(), None, retention, spend)
    for marker in ("ПРИВЛЕЧЕНИЕ", "ВОРОНКА 24 Ч", "RETENTION", "ВИРУСНОСТЬ",
                   "МОНЕТИЗАЦИЯ", "ЭКОНОМИКА МОНЕТ", "ИГРЫ", "КОГОРТЫ ТРАТ"):
        assert marker in text
    assert "D3: —" in text            # несозревший день когорты не рисуется числом
    assert "&lt;quiz&gt;" in text     # html из данных экранируется
    assert all(len(p) <= TG_MESSAGE_LIMIT for p in split_message(text))


def test_reports_survive_empty_database_snapshot():
    """Нулевая экосистема: все списки пусты, все счётчики нули — отчёты не падают."""
    empty = {
        "period": {"since": "", "until": ""},
        "acquisition": {"new_total": 0, "by_source": [], "by_lang": [], "top_channels": []},
        "funnel": {"registered": 0, "onboarded": 0, "played": 0, "paid": 0},
        "activity": {"dau": 0, "wau": 0, "mau": 0, "stickiness_pct": 0.0},
        "virality_7d": {"cohort_size": 0, "k_raw": 0.0, "k_qualified": 0.0,
                        "inviter_share_pct": 0.0, "median_cycle_hours": None},
        "monetization": {"revenue_stars": 0, "payers": 0, "purchases": 0,
                         "cr_mau_pct": 0.0, "cr_base_pct": 0.0,
                         "arpu_stars": 0.0, "arppu_stars": 0.0,
                         "by_sku": [], "by_lang": [], "by_source": [],
                         "first_purchase_sku": [],
                         "median_hours_to_first_purchase": None,
                         "repeat_buyers_pct": 0.0,
                         "limit_hit_users": 0, "limit_to_unlimit_pct": 0.0},
        "economy": {"emission": 0, "burn": 0, "net_inflation": 0,
                    "emission_by_reason": [], "burn_by_reason": [],
                    "coin_supply": 0, "top1pct_share_pct": 0.0},
        "games_farm": {"games": [], "limit_hits": [], "miners_active": 0,
                       "miners_burned": 0, "drill_owners": 0, "hungry_drill_owners_pct": 0.0},
    }
    assert "ЭКСПРЕСС" in build_express_report(empty, None, 6)
    assert "СУТОЧНЫЙ" in build_daily_report(empty, None, [], [])
