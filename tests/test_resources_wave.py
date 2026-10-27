"""
Волна 22.10 (вечер): ресурсы, мастерская, налёты, ежедневные цели, станция команды.
Чистые правила без БД; сделки с БД — в test_db_integration.
"""
from datetime import date, datetime, timedelta, timezone

import pytest

from shared import economy
from shared.daily_goals import GOAL_POOL, all_done, chest_coins, chest_resource_kind, goals_for, next_streak
from shared.economy import (
    ARMOR_LEVEL_COSTS,
    ARMOR_MAX_LEVEL,
    GAME_RESOURCE,
    RESOURCE_KINDS,
    WORKSHOP_RECIPES,
    farm_bonus_percent,
    market_fee,
    market_limits,
    miner_hourly_rate,
    raid_fail_loss,
    raid_loot,
    station_level_cost,
)
from shared.farm_logic import MinerState, integrate_rate_micros, simulate_farm
from shared.locales import STRINGS, t
from shared.raids import attack_cooldown_left, raid_outcome, shield_active
from shared.resources import format_bundle, game_resource_gain
from shared.team_station import apply_level_ups, progress_to_next
from shared.workshop import can_afford, recipe_cost

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- ресурсы
def test_every_game_mines_its_own_resource():
    classic = {g: GAME_RESOURCE[g] for g in ("rps", "hl", "quiz", "safe")}
    assert set(classic.values()) == set(RESOURCE_KINDS)          # четыре старые игры — четыре ресурса, без повторов
    assert set(GAME_RESOURCE.values()) <= set(RESOURCE_KINDS)    # 27.10: игры за раунд дают только базовые ресурсы
    assert "math" not in GAME_RESOURCE                           # ➗ — только ⚡ за каждые 10 побед
    assert game_resource_gain("safe") == ("parts", 3)           # сейф реже выигрывается — даёт больше
    assert game_resource_gain("rps") == ("metal", 1)
    assert game_resource_gain("unknown") is None


def test_duel_fee_is_lower_with_unlimited():
    """Дуэли — только монеты (владелец 27.10): комиссия 20%, с ⚡ Безлимитом 10%; ресурсов нет."""
    assert economy.duel_payout(100) == (160, 40)
    assert economy.duel_payout(100, premium=True) == (180, 20)
    assert not hasattr(economy, "DUEL_RESOURCE_KIND")


def test_format_bundle_orders_by_kind_and_skips_zero():
    text = format_bundle("ru", {"parts": 2, "metal": 5, "crystal": 0})
    assert text.startswith("⛏ 5") and "⚙️ 2" in text and "💎" not in text
    assert format_bundle("en", {}) == "—"


# ---------------------------------------------------------------- мастерская
def test_recipes_have_prices_and_known_effects():
    for rid, recipe in WORKSHOP_RECIPES.items():
        assert recipe["effect"] in economy.ITEM_EFFECTS or recipe["effect"] in ("cutlet", "armor", "storage", "shuttle", "make", "cart", "bdrone")
        cost = recipe_cost(rid)
        assert cost and all(k in economy.ALL_KINDS and v > 0 for k, v in cost.items()), rid
        if recipe["effect"] in economy.ITEM_EFFECTS and recipe["effect"] not in ("forsage", *economy.ONE_SHOT_COLUMNS):
            assert recipe["hours"] > 0, rid


def test_armor_cost_escalates_and_stops_at_max():
    costs = [sum(ARMOR_LEVEL_COSTS[lvl].values()) for lvl in range(1, ARMOR_MAX_LEVEL + 1)]
    assert costs == sorted(costs) and costs[0] < costs[-1]
    assert recipe_cost("armor", armor_level=0) == ARMOR_LEVEL_COSTS[1]
    # На максимуме — продление максимального уровня ещё на 30 дней по его же цене
    assert recipe_cost("armor", armor_level=ARMOR_MAX_LEVEL) == ARMOR_LEVEL_COSTS[ARMOR_MAX_LEVEL]


def test_owner_rules_24_10_for_workshop():
    """Решения владельца: котлеты из коровы (26.10: 🐄 + 2 🔥 → 3 🥩), броня на 30 дней, Шаттл — 1000 всего + 1000 🪙."""
    assert WORKSHOP_RECIPES["cutlet"]["cost"] == {"cow": 1, "fire": 2} and WORKSHOP_RECIPES["cutlet"]["qty"] == 3
    assert economy.ARMOR_DAYS == 30
    assert WORKSHOP_RECIPES["shuttle"]["cost"] == {k: 1000 for k in RESOURCE_KINDS}
    assert WORKSHOP_RECIPES["shuttle"]["coins"] == 1000
    # Ни один рецепт мастерской не даёт «навсегда», кроме Шаттла (льгота биржи, не добыча)
    assert all(r["effect"] != "armor" or economy.ARMOR_DAYS for r in WORKSHOP_RECIPES.values())


def test_armor_expires_after_30_days_in_engine():
    from shared.economy import armor_level_active
    until = NOW + timedelta(days=30)
    assert armor_level_active(2, until, NOW) == 2
    assert armor_level_active(2, until, until + timedelta(seconds=1)) == 0
    assert armor_level_active(2, None, NOW) == 0
    miner = MinerState(1, "junior", NOW, NOW + timedelta(days=60))
    # 10 часов: первые 5 с бронёй +30%, потом броня кончилась
    tick = simulate_farm(last_update=NOW, now=NOW + timedelta(hours=10), fridge_cutlets=0, acc=0,
                         miners=[miner], armor_percent=30, armor_until=NOW + timedelta(hours=5))
    assert tick.earned == 5 * 5 * 130 // 100 + 5 * 5   # 32 + 25 = 57 (дробь — в остатке)


def test_can_afford():
    assert can_afford({"metal": 20, "hydrogen": 20}, WORKSHOP_RECIPES["nitro_6h"]["cost"])
    assert not can_afford({"metal": 19, "hydrogen": 20}, WORKSHOP_RECIPES["nitro_6h"]["cost"])
    assert not can_afford({}, None)


def test_workshop_boost_is_small_versus_stars_item():
    """6 часов азота за ресурсы ≪ 30 дней за Stars — мастерская не каннибализирует магазин."""
    assert WORKSHOP_RECIPES["nitro_6h"]["hours"] * 10 < economy.BOOST_DAYS * 24


# ---------------------------------------------------------------- постоянный бонус фермы
def test_farm_bonus_percent_caps():
    assert farm_bonus_percent(0, 0) == 0
    assert farm_bonus_percent(1, 0) == economy.ARMOR_BONUS_PER_LEVEL
    assert farm_bonus_percent(ARMOR_MAX_LEVEL + 5, economy.STATION_MAX_LEVEL + 5) == \
        ARMOR_MAX_LEVEL * economy.ARMOR_BONUS_PER_LEVEL + economy.STATION_MAX_LEVEL * economy.STATION_BONUS_PER_LEVEL


def test_bonus_percent_applies_to_rate_and_micros():
    assert miner_hourly_rate("premium", bonus_percent=10) == 11
    assert miner_hourly_rate("junior", bonus_percent=10) == 5   # витрина округляет вниз…
    base = integrate_rate_micros(NOW, NOW + timedelta(hours=1), "junior", None, None)
    boosted = integrate_rate_micros(NOW, NOW + timedelta(hours=1), "junior", None, None, bonus_percent=10)
    assert boosted == base * 110 // 100                         # …а движок считает точно


def test_simulate_farm_with_bonus_earns_more():
    miner = MinerState(1, "junior", NOW, NOW + timedelta(days=30))
    plain = simulate_farm(last_update=NOW, now=NOW + timedelta(hours=10), fridge_cutlets=0, acc=0,
                          miners=[miner])
    armored = simulate_farm(last_update=NOW, now=NOW + timedelta(hours=10), fridge_cutlets=0, acc=0,
                            miners=[miner], bonus_percent=30)
    assert plain.earned == 50 and armored.earned == 65


# ---------------------------------------------------------------- биржа + Шаттл
def test_shuttle_halves_fee_and_widens_limits():
    assert market_fee(100) == 10 and market_fee(100, shuttle=True) == 5
    assert market_limits(False) == (economy.MARKET_MAX_QTY, economy.MARKET_MAX_OPEN_ORDERS)
    qty, orders = market_limits(True)
    assert qty > economy.MARKET_MAX_QTY and orders > economy.MARKET_MAX_OPEN_ORDERS


# ---------------------------------------------------------------- налёты
@pytest.mark.parametrize("move,stance,expected", [
    ("rock", "scissors", "win"), ("scissors", "paper", "win"), ("paper", "rock", "win"),
    ("rock", "rock", "draw"), ("rock", "paper", "lose"), ("paper", "scissors", "lose"),
])
def test_raid_outcome_is_rps(move, stance, expected):
    assert raid_outcome(move, stance) == expected


def test_raid_loot_is_capped_and_never_touches_small_stocks_fully():
    assert raid_loot(0) == 0
    assert raid_loot(100) == 20
    assert raid_loot(10_000) == economy.RAID_LOOT_CAP
    assert raid_fail_loss(100) == 10
    assert raid_fail_loss(10_000) == economy.RAID_FAIL_CAP
    assert raid_fail_loss(100) < raid_loot(100)   # провал дешевле удачи — атаковать выгодно, но не бесплатно


def test_shield_and_newbie_protection():
    user = {"raid_shield_until": None, "created_at": NOW - timedelta(days=10)}
    assert not shield_active(user, NOW)
    assert shield_active({"raid_shield_until": NOW + timedelta(hours=1), "created_at": NOW - timedelta(days=10)}, NOW)
    assert shield_active({"raid_shield_until": None, "created_at": NOW - timedelta(days=1)}, NOW)


def test_attack_cooldown():
    assert attack_cooldown_left(None, NOW) == 0
    assert attack_cooldown_left(NOW - timedelta(hours=economy.RAID_ATTACK_COOLDOWN_HOURS), NOW) == 0
    assert attack_cooldown_left(NOW - timedelta(hours=1), NOW) == (economy.RAID_ATTACK_COOLDOWN_HOURS - 1) * 3600


# ---------------------------------------------------------------- ежедневные цели
def test_goals_are_deterministic_per_user_and_day():
    day = date(2026, 11, 1)
    a = goals_for(777, day)
    assert a == goals_for(777, day)
    assert len(a) == economy.DAILY_GOALS_PER_DAY and len({g.key for g in a}) == len(a)
    assert goals_for(777, day + timedelta(days=1)) != a or goals_for(778, day) != a


def test_goals_respect_disabled_features():
    only_games = goals_for(777, date(2026, 11, 1), enabled_features={"games"})
    assert all(g.feature in (None, "games") for g in only_games)
    assert all(g.feature is None for g in goals_for(1, date(2026, 11, 1), enabled_features=set()))


def test_goal_pool_covers_every_taste():
    features = {g.feature for g in GOAL_POOL}
    assert {"games", "duels", "workshop", "raids", "market", "station", None} <= features


def test_all_done_and_chest():
    goals = goals_for(5, date(2026, 11, 1))
    assert not all_done(goals, {})
    assert all_done(goals, {g.key: g.target for g in goals})
    assert not all_done([], {})
    assert chest_coins(0) == economy.DAILY_CHEST_COINS
    assert chest_coins(economy.DAILY_STREAK_BONUS_EVERY) == economy.DAILY_CHEST_COINS + economy.DAILY_STREAK_BONUS_COINS
    assert chest_coins(economy.DAILY_STREAK_BONUS_EVERY - 1) == economy.DAILY_CHEST_COINS


def test_streak_logic():
    today = date(2026, 11, 2)
    assert next_streak(None, today, 0) == 1
    assert next_streak(date(2026, 11, 1), today, 4) == 5
    assert next_streak(date(2026, 10, 30), today, 4) == 1
    assert chest_resource_kind(1, today) in RESOURCE_KINDS


# ---------------------------------------------------------------- станция команды
def test_station_costs_and_level_ups():
    assert station_level_cost(1) == economy.STATION_LEVEL_BASE_COST
    assert station_level_cost(3) == 3 * economy.STATION_LEVEL_BASE_COST
    full = {k: station_level_cost(1) + station_level_cost(2) for k in RESOURCE_KINDS}
    level, rest, gained = apply_level_ups(0, full)
    assert (level, gained) == (2, 2) and all(v == 0 for v in rest.values())
    partial = {k: station_level_cost(1) for k in RESOURCE_KINDS}
    partial["parts"] -= 1
    assert apply_level_ups(0, partial)[0] == 0
    assert progress_to_next(0, partial)["parts"] == 1 and progress_to_next(0, partial)["metal"] == 0
    assert progress_to_next(economy.STATION_MAX_LEVEL, {}) == {}
    assert apply_level_ups(economy.STATION_MAX_LEVEL, full)[2] == 0


# ---------------------------------------------------------------- локали
def test_new_sections_exist_in_ru_and_en():
    for lang in ("ru", "en"):
        for key in ("ws.header", "raid.header", "goal.header", "st.header", "res.metal",
                    "games.resource_gain", "quest.win_resources"):
            assert key in STRINGS[lang], (lang, key)
        for k in RESOURCE_KINDS:
            assert STRINGS[lang][f"res.{k}"].strip()
        for g in GOAL_POOL:
            assert "{n}" in STRINGS[lang][f"goal.{g.key}"] or g.target == 1, (lang, g.key)
        for rid in WORKSHOP_RECIPES:
            t(lang, f"ws.recipe_{rid}", level=1, cap=1000)
    assert "рофл" not in " ".join(STRINGS["ru"].values()).lower()


# ---------------------------------------------------------------- 25.10: рецепты недели и склад с лимитом
def test_weekly_recipes_catalog_is_rich_and_sane():
    from shared.economy import RES_CAPACITY_BASE
    from shared.weekly_recipes import HOURS_COLUMNS, WEEKLY_RECIPES, recipe_title
    assert 30 <= len(WEEKLY_RECIPES) <= 50
    for rid, r in WEEKLY_RECIPES.items():
        assert len(f"recipe_toggle:{rid}:9") <= 64, rid                       # callback админ-бота
        assert r["limit"] >= 1 and r["effects"], rid
        assert all(k in RESOURCE_KINDS and 0 < v <= RES_CAPACITY_BASE for k, v in r["cost"].items()), rid
        for e in r["effects"]:
            assert e["type"] in (*HOURS_COLUMNS, "cutlet", "resource"), rid
        for lang in ("ru", "en"):
            assert recipe_title(lang, rid).strip(), (lang, rid)
        # котлеты из рецептов недели — не чаще одной-двух в неделю (топливо — право магазина)
        if any(e["type"] == "cutlet" for e in r["effects"]):
            assert r["limit"] == 1, rid


def test_week_starts_on_monday_utc():
    from shared.weekly_recipes import week_start
    sunday = datetime(2026, 11, 1, 23, 59, tzinfo=timezone.utc)      # воскресенье
    assert week_start(sunday) == datetime(2026, 10, 26, tzinfo=timezone.utc)
    assert week_start(datetime(2026, 11, 2, 0, 0, tzinfo=timezone.utc)) == datetime(2026, 11, 2, tzinfo=timezone.utc)


def test_weekly_recipes_are_off_by_default():
    from shared.feature_flags import _default_for
    assert _default_for("recipe:w_nitro_12h") is False


def test_storage_levels_are_reachable():
    """Каждое расширение склада можно оплатить, не превышая текущую вместимость."""
    from shared.economy import RES_CAPACITY_BASE, STORAGE_LEVELS, next_storage_level
    cap = RES_CAPACITY_BASE
    for new_cap, cost in STORAGE_LEVELS:
        assert new_cap > cap and all(v <= cap for v in cost.values())
        assert next_storage_level(cap) == (new_cap, cost)
        cap = new_cap
    assert next_storage_level(cap) is None
    # Шаттл (по 1000 каждого) требует расширенного склада — синергия
    assert max(WORKSHOP_RECIPES["shuttle"]["cost"].values()) > RES_CAPACITY_BASE
