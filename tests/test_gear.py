"""
🧍 Персонаж и костюмы, ротация квестов v3, ничья без списания (решения владельца 30.10) — чистые правила без БД.
Интеграционные сценарии (сумка, биржа деталей, бонус шахтёра) — в test_db_integration.py.
"""
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from shared import economy  # noqa: E402
from shared.economy import (  # noqa: E402
    GEAR_ASSETS, GEAR_EXO, GEAR_MIN_PRICE, GEAR_SEASON_CAP, GEAR_SLOTS, GEAR_SUITS, SUIT_BONUS,
    discounted_cost, energy_chance_percent, gear_asset, market_limits, market_min_price, miner_bonus,
    parse_gear_asset, suit_bonus,
)
from shared.locales import PACK_CODES, t  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------- костюмы
def test_six_suits_five_slots_and_one_suit_per_season():
    assert GEAR_SUITS == ("el", "mn", "ml", "st", "sc", "en")
    assert GEAR_SLOTS == ("head", "body", "hands", "legs", "feet")
    assert GEAR_SEASON_CAP == len(GEAR_SLOTS)          # за сезон — ровно один костюм деталей
    assert set(SUIT_BONUS) == set(GEAR_SUITS)
    for line, lv in SUIT_BONUS.items():
        assert 0 < lv[1] < lv[2], line                 # 2-й уровень всегда сильнее


def test_suit_bonus_only_for_its_own_line_exo_gives_all_at_level_two():
    assert suit_bonus("el", 1, "el") == 50 and suit_bonus("el", 2, "el") == 60
    assert suit_bonus("el", 2, "mn") == 0                # костюм электрика не помогает шахте
    assert suit_bonus(None, None, "el") == 0 and suit_bonus("mn", 0, "mn") == 0
    for line in GEAR_SUITS:
        assert suit_bonus(GEAR_EXO, 2, line) == SUIT_BONUS[line][2]
    assert energy_chance_percent(None, None) == economy.ENERGY_WIN_CHANCE_PERCENT == 25
    assert energy_chance_percent("el", 1) == 50          # «энергия в 2 раза чаще» — слово владельца


def test_rounding_always_in_favour_of_the_ecosystem():
    assert discounted_cost({"metal": 15, "parts": 7}, 10) == {"metal": 14, "parts": 7}   # вверх: 13.5 → 14, 6.3 → 7
    assert discounted_cost({"metal": 100}, 0) == {"metal": 100}
    assert miner_bonus(199, 5) == 9 and miner_bonus(19, 5) == 0 and miner_bonus(-5, 5) == 0   # вниз
    assert economy.tech_cooldown_cut(30, 20) == 24


def test_gear_assets_fit_market_column_and_parse_back():
    assert len(GEAR_ASSETS) == len(GEAR_SUITS) * len(GEAR_SLOTS)
    for asset in GEAR_ASSETS:
        assert len(asset) <= 16                          # market_orders.asset VARCHAR(16)
        suit, slot = parse_gear_asset(asset)
        assert gear_asset(suit, slot) == asset
    for bad in ("g_exo_head", "g_mn_hat", "metal", "g_mn", "", "g_xx_head"):
        assert parse_gear_asset(bad) is None             # экзо-броня на бирже не торгуется


def test_parts_market_floor_and_limits():
    from shared.market import MarketError, validate_order
    assert market_min_price("g_mn_head") == GEAR_MIN_PRICE == 500
    assert market_limits(False, "g_mn_head")[0] == economy.GEAR_MARKET_MAX_QTY
    validate_order(1, 500, asset="g_mn_head")
    with pytest.raises(MarketError):
        validate_order(1, 499, asset="g_mn_head")      # дешевле 500 не продать
    with pytest.raises(MarketError):
        validate_order(1, 500, asset="g_exo_head")
    with pytest.raises(MarketError):
        validate_order(economy.GEAR_MARKET_MAX_QTY + 1, 500, asset="g_el_feet")


def test_full_set_needs_five_parts_of_one_suit():
    from shared.gear import full_set
    worn = {p: {"suit": "mn", "level": 2} for p in GEAR_SLOTS}
    assert full_set(worn) == ("mn", 2)
    worn["feet"] = {"suit": "mn", "level": 1}
    assert full_set(worn) == ("mn", 1)                   # уровень костюма — по слабой детали
    worn["feet"] = {"suit": "el", "level": 2}
    assert full_set(worn) == (None, 0)                   # перчатки шахтёра с ботинками электрика — без бонуса
    del worn["feet"]
    assert full_set(worn) == (None, 0)


def test_upgrade_and_exo_recipes_use_real_resources_and_burn_coins():
    for suit, cost in economy.GEAR_UPGRADE_COST.items():
        assert cost and set(cost) <= set(economy.ALL_KINDS), suit
    assert economy.GEAR_UPGRADE_COINS > 0 and economy.GEAR_EXO_COINS > 0
    assert set(economy.GEAR_EXO_COST) <= set(economy.ALL_KINDS)


def test_workshop_engineer_discount_and_scientist_cooldown():
    from shared.tech import next_tech_at
    from shared.workshop import recipe_cost
    base = recipe_cost("nitro_6h")
    cheap = recipe_cost("nitro_6h", discount=SUIT_BONUS["en"][1])
    assert base and all(cheap[k] <= base[k] for k in base) and cheap != base
    at = datetime(2026, 10, 1, tzinfo=timezone.utc)
    assert next_tech_at("comm", 1, at) == at + timedelta(days=30)
    assert next_tech_at("comm", 1, at, 20) == at + timedelta(days=24)


def test_soldier_speeds_up_trips_and_adds_haul():
    from shared.expeditions import apply_option
    assert economy.exp_travel_minutes(100, "solo", 0, 10) < economy.exp_travel_minutes(100, "solo")
    assert apply_option(100, {"cargo": 20}, {"suit": 10}) == (122, 0)
    assert apply_option(100, {"cargo": 20}, {}) == (120, 0)
    assert apply_option(100, {"cargo": -5}, {"suit": 10})[0] == 95   # потери военный не увеличивает


def test_gear_prize_kind_respects_season_cap():
    from shared.prizes import normalize_reward, reward_label
    assert normalize_reward({"kind": "gear", "qty": GEAR_SEASON_CAP}) == {"kind": "gear", "qty": GEAR_SEASON_CAP}
    assert normalize_reward({"kind": "gear", "qty": GEAR_SEASON_CAP + 1}) is None
    assert reward_label({"kind": "gear", "qty": 2}) == "🧥 ×2"
    from shared.rewards import TARGETS
    assert "active" in TARGETS                           # пульт: раздача всем активным


def test_gear_texts_in_every_language():
    for lang in ("ru", "en") + tuple(PACK_CODES):
        for key in ("gear.err_unknown", "gear.err_none", "gear.err_max", "hist.gear_upgrade", "hist.gear_exo",
                    "hist.suit_miner"):
            assert t(lang, key) and t(lang, key) != key, (lang, key)
        assert "{need}" not in t(lang, "gear.err_coins", need=5)
    from bots.main_bot.webapp_history import HISTORY_REASONS
    assert {"gear_upgrade", "gear_exo", "suit_miner"} <= set(HISTORY_REASONS)


def test_app_has_persona_tab_with_gender_switch_and_market():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "persona: viewPersona" in html and 'persona: "gear"' in html
    assert '"/api/gear/gender"' in html and '"/api/market/order"' in html and '"/api/gear/exo"' in html
    for key in ("tab_persona", "ps_m", "ps_f", "ps_slot_head", "ps_suit_exo", "ps_upg_en", "raid_note_suit"):
        assert key + ":" in html, key
    ru = html[html.index("    ru: {"):html.index("    en: {")]
    assert not re.search(r"ps_[A-Za-z_]+: \"[^\"]*(Стажер|[Рр]офл)", ru)


def test_gear_routes_and_flag_registered():
    from bots.main_bot.webapp import create_webapp
    from shared.feature_flags import FLAG_DEFAULTS, FLAG_TITLES
    paths = {r.resource.canonical for r in create_webapp("123456:TEST").router.routes() if r.resource}
    assert {"/api/gear", "/api/gear/gender", "/api/gear/equip", "/api/gear/unequip", "/api/gear/upgrade",
            "/api/gear/exo"} <= paths
    assert FLAG_DEFAULTS["gear"] is True and "gear" in FLAG_TITLES


def test_schema_has_gear_tables_and_deletion_clears_them():
    from shared.database import SCHEMA_STATEMENTS
    sql = "\n".join(SCHEMA_STATEMENTS)
    for table in ("user_gear", "user_equip", "gear_ledger"):
        assert f"CREATE TABLE IF NOT EXISTS {table}" in sql
    assert "qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0)" in sql
    src = (ROOT / "shared" / "account_deletion.py").read_text(encoding="utf-8")
    assert "DELETE FROM user_gear" in src and "DELETE FROM user_equip" in src


# ---------------------------------------------------------------- ротация квестов v3
def test_daily_rotation_same_for_everyone_ten_and_changes_by_day():
    from shared.quest_engine import daily_rotation
    pool = [{"id": f"q{i}"} for i in range(31)]
    d1, d2 = date(2026, 10, 30), date(2026, 10, 31)
    a, b = daily_rotation(pool, d1), daily_rotation(list(reversed(pool)), d1)
    assert len(a) == economy.QUEST_ROTATION_SIZE == 10
    assert [q["id"] for q in a] == [q["id"] for q in b]          # один список на всех, порядок банка не важен
    assert [q["id"] for q in a] != [q["id"] for q in daily_rotation(pool, d2)]
    assert len(daily_rotation(pool[:4], d1)) == 4                  # банк меньше 10 — показываем весь


def test_new_quests_join_the_rotation_bank_epics_stay_hidden():
    from shared.feature_flags import _default_for
    assert _default_for("quest:any_new") is True and _default_for("epic:any_new") is False
    from shared.database import SCHEMA_STATEMENTS
    assert any("migr:quest_pool_20261030" in s for s in SCHEMA_STATEMENTS)


# ---------------------------------------------------------------- ничья
def test_draw_costs_nothing_in_every_language():
    for lang in ("ru", "en") + tuple(PACK_CODES):
        text = t(lang, "games.draw")
        assert "{penalty}" not in text and "-1" not in text, lang
        assert "<b>0</b>" in t(lang, "rps.intro", reward=2, penalty=1, limit=15), lang   # «ничья: 0»
    src = (ROOT / "bots" / "main_bot" / "handlers" / "games.py").read_text(encoding="utf-8")
    body = src[src.index("elif is_draw:"):src.index("            else:\n                try:")]
    assert "change_balance" not in body                            # ничья не трогает баланс


def test_persona_view_does_not_shadow_the_act_helper():
    """Баг стенда 30.10: локальная `act = d.active` перекрывала функцию act() — все кнопки вкладки молчали."""
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    body = html[html.index("async function viewPersona(box)"):html.index("const VIEWS = {")]
    assert not re.search(r"[\s,]act\s*=", body)
    assert "act(b, \"/api/gear/equip\"" in body
