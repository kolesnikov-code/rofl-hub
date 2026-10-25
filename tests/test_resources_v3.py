"""
Волна 27.10 «ресурсы v3»: новые ресурсы, Лаборатория (инструменты и технологии), лошади и телеги,
заряд Шаттла, Аптечка и болезни, Ядро только из командных активностей, сезоны, подарки из админки.
Чистые юнит-тесты (без БД); интеграционные — в test_db_integration.py.
"""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from shared import economy
from shared.economy import (ALL_KINDS, EXTRA_KINDS, RESOURCE_KINDS, TECH_ORDER, TECHS, TOOL_COSTS, TRADEABLE_KINDS,
                            WORKSHOP_RECIPES, market_lots, raid_candidates, raid_cooldown_hours, raid_loot_percent,
                            season_bounds, season_key, tech_cooldown_days, tech_cost, tech_tool_required)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- ресурсы

def test_resource_sets_are_consistent():
    assert ALL_KINDS == RESOURCE_KINDS + EXTRA_KINDS and len(set(ALL_KINDS)) == len(ALL_KINDS)
    assert "core" not in TRADEABLE_KINDS                      # Ядро не продаётся — только командная игра
    assert set(TRADEABLE_KINDS) == set(ALL_KINDS) - {"core"}
    from shared.resources import RESOURCE_ICONS
    assert set(RESOURCE_ICONS) >= set(ALL_KINDS)
    for asset in ("stone", "wood", "fire", "energy", "battery", "cow"):
        assert asset in economy.MARKET_ASSETS, asset
    assert "core" not in economy.MARKET_ASSETS
    assert economy.market_min_price("cow") == economy.MARKET_COW_MIN_PRICE > 1


def test_station_drone_removed_no_resources_from_air():
    """Решение владельца: «не надо из воздуха создавать ресурсы»."""
    assert "station_drone" not in WORKSHOP_RECIPES
    assert "station_drone" not in economy.ITEM_EFFECTS
    assert not hasattr(economy, "STATION_DRONE_PERCENT")
    src = (ROOT / "shared" / "team_station.py").read_text(encoding="utf-8")
    assert "station_drone" not in src and "station_boost" not in src


def test_sources_of_new_resources():
    assert economy.DUEL_RESOURCE_KIND == "stone"
    assert economy.QUEST_EXTRA_BUNDLE == {"wood": 10, "cow": 1}
    assert 0 < economy.ENERGY_WIN_CHANCE_PERCENT < 100
    assert {k for k, _ in economy.CHEST_SPECIALS} == {"wood", "stone", "energy"}
    assert economy.CHEST_STREAK_COW >= 1
    assert set(economy.MINE_KINDS) == set(RESOURCE_KINDS) | {"stone", "wood", "energy"}


def test_core_only_from_team_activities_and_small():
    """Ядро — только битвы/рудники/командный ТОП сезона; немного на бойца."""
    assert not hasattr(economy, "BATTLE_CORE_REWARD")   # призы битв назначает владелец
    assert economy.MINE_CORE_MAX <= 3
    for rid, r in WORKSHOP_RECIPES.items():                   # ни один рецепт не производит Ядро
        assert "core" not in (r.get("make") or {}), rid
    from shared.weekly_recipes import WEEKLY_RECIPES
    for rid, r in WEEKLY_RECIPES.items():
        for e in r["effects"]:
            assert e.get("kind") != "core", rid
    for src in ("shared/duels.py", "bots/main_bot/handlers/games.py", "bots/main_bot/handlers/quests.py"):
        assert '"core"' not in (ROOT / src).read_text(encoding="utf-8"), src


def test_chest_special_is_deterministic_and_rotates():
    from shared.daily_goals import chest_special
    day = date(2026, 10, 27)
    assert chest_special(5, day) == chest_special(5, day)
    seen = {chest_special(5, day + timedelta(days=i))[0] for i in range(3)}
    assert seen == {"wood", "stone", "energy"}


# ---------------------------------------------------------------- мастерская

def test_new_recipes_fire_battery_cart_meds():
    bon = WORKSHOP_RECIPES["bonfire"]
    assert bon["effect"] == "make" and set(bon["cost"]) == {"wood", "stone"} and bon["make"] == {"fire": 5}
    bat = WORKSHOP_RECIPES["battery"]
    assert bat["effect"] == "make" and bat["make"] == {"battery": 2} and "fire" in bat["cost"]
    assert WORKSHOP_RECIPES["cart"]["effect"] == "cart" and "wood" in WORKSHOP_RECIPES["cart"]["cost"]
    assert WORKSHOP_RECIPES["meds_72h"]["effect"] == "meds"
    assert economy.ITEM_COLUMNS["meds"] == "meds_until"
    # котлета требует корову и огонь
    assert WORKSHOP_RECIPES["cutlet"]["cost"]["cow"] == 1 and WORKSHOP_RECIPES["cutlet"]["cost"]["fire"] > 0


def test_unlock_order_starts_simple_ends_legendary():
    order = economy.WORKSHOP_UNLOCK_ORDER
    assert sorted(order) == sorted(WORKSHOP_RECIPES)
    assert order.index("bonfire") < order.index("battery") < order.index("cart")   # огонь раньше батареек
    assert order.index("bonfire") < order.index("cutlet")
    assert order[-1] == "shuttle"


def test_team_items_expensive_and_clan_pays_multiple():
    from shared.workshop import recipe_cost, team_cost_multiplier
    dome, banner = WORKSHOP_RECIPES["dome_12h"], WORKSHOP_RECIPES["banner_24h"]
    assert dome.get("team") and banner.get("team")
    assert dome["cost"]["core"] >= 3 and dome["cost"]["battery"] >= 10       # дорогой и сложный
    assert all(dome["cost"][k] >= 300 for k in RESOURCE_KINDS)
    assert team_cost_multiplier(50) == 1
    assert team_cost_multiplier(economy.MEGA_CLAN_MAX_MEMBERS) == economy.TEAM_ITEM_CLAN_MULTIPLIER >= 3
    team = recipe_cost("dome_12h")
    clan = recipe_cost("dome_12h", team_mult=team_cost_multiplier(economy.MEGA_CLAN_MAX_MEMBERS))
    assert clan == {k: v * economy.TEAM_ITEM_CLAN_MULTIPLIER for k, v in team.items()}
    assert recipe_cost("nitro_6h", team_mult=5) == recipe_cost("nitro_6h")   # личные рецепты не множатся


def test_recipe_tool_levels():
    from shared.workshop import recipe_tool
    assert recipe_tool("bonfire") == 0                       # костёр — голыми руками
    assert recipe_tool("battery") == 1
    assert recipe_tool("dome_12h") == 3 and recipe_tool("shuttle") == 3
    assert recipe_tool("armor", 0) == 1 and recipe_tool("armor", 2) == 3
    assert recipe_tool("nope") == 0
    for rid, r in WORKSHOP_RECIPES.items():
        assert 0 <= int(r.get("tool", 0)) <= len(TOOL_COSTS), rid


# ---------------------------------------------------------------- Лаборатория

def test_tool_kits_four_tiers_need_progressively_rarer_inputs():
    assert sorted(TOOL_COSTS) == [1, 2, 3, 4]
    assert set(economy.TOOL_ICONS) == {1, 2, 3, 4}
    assert "fire" in TOOL_COSTS[1] and "battery" in TOOL_COSTS[3] and "core" in TOOL_COSTS[4]
    totals = [sum(TOOL_COSTS[i].values()) for i in (1, 2, 3, 4)]
    assert totals == sorted(totals)


def test_tech_tool_requirements():
    """Все технологии, включая связь, — одинаковые 5 уровней и одинаковые наборы инструментов."""
    for key in ("comm", "scout", "attack", "defense"):
        assert TECHS[key]["max"] == 5, key
        assert [tech_tool_required(key, lvl) for lvl in (1, 2, 3, 4, 5)] == [1, 1, 2, 3, 4], key
    assert [tech_tool_required("science", lvl) for lvl in (1, 2, 3, 4, 5)] == [2, 2, 3, 4, 4]
    for key in TECH_ORDER:
        for lvl in range(1, TECHS[key]["max"] + 1):
            assert 1 <= tech_tool_required(key, lvl) <= len(TOOL_COSTS)


def test_tech_cost_grows_and_science_is_linear_with_core():
    assert tech_cost("attack", 2) == {k: v * 4 for k, v in TECHS["attack"]["base"].items()}
    assert tech_cost("science", 3) == {k: v * 3 for k, v in TECHS["science"]["base"].items()}
    assert tech_cost("science", 1)["core"] == TECHS["science"]["base"]["core"]
    assert "battery" not in tech_cost("comm", 1)
    assert [tech_cost("comm", lvl)["battery"] for lvl in (2, 3, 4, 5)] == [2, 4, 6, 8]
    for key in TECH_ORDER:
        sums = [sum(tech_cost(key, lvl).values()) for lvl in range(1, TECHS[key]["max"] + 1)]
        assert sums == sorted(sums) and all(v > 0 for v in tech_cost(key, 1).values()), key


def test_tech_cooldown_is_30_days_and_science_follows_the_rest():
    """Решение владельца 27.10: следующий уровень той же технологии — ровно через 30 дней;
    наука N — когда все остальные технологии изучены до N."""
    from shared.economy import TECH_COOLDOWN_DAYS, science_gate_ok
    assert TECH_COOLDOWN_DAYS == 30
    for key in TECH_ORDER:
        for lvl in range(1, TECHS[key]["max"]):
            assert tech_cooldown_days(key, lvl) == 30, (key, lvl)
    assert not science_gate_ok({}, 1)
    assert not science_gate_ok({"comm": 1, "scout": 1, "attack": 1}, 1)            # оборона ещё 0
    assert science_gate_ok({"comm": 1, "scout": 1, "attack": 1, "defense": 1}, 1)
    assert not science_gate_ok({"comm": 2, "scout": 2, "attack": 2, "defense": 1}, 2)
    assert science_gate_ok({"comm": 3, "scout": 2, "attack": 5, "defense": 2, "science": 0}, 2)


def test_raid_tech_formulas():
    assert raid_loot_percent(1, 0, 0) == 100
    assert raid_loot_percent(3, 0, 0) == 100 + 2 * economy.RAID_ATTACK_BONUS_PER_LEVEL
    assert raid_loot_percent(1, 2, 0) == 100 - 2 * economy.RAID_DEFENSE_PER_LEVEL
    assert raid_loot_percent(1, 0, 5) == 105
    assert raid_loot_percent(1, 5, 0) >= 50 and raid_loot_percent(0, 50, 0) == 50   # пол 50%
    assert raid_candidates(1) == 3 and raid_candidates(5) == 7 and raid_candidates(0) == 3
    assert raid_cooldown_hours(1) == economy.RAID_ATTACK_COOLDOWN_HOURS
    assert raid_cooldown_hours(3) == pytest.approx(economy.RAID_ATTACK_COOLDOWN_HOURS - 40 / 60)


def test_attack_cooldown_uses_comm_level():
    from shared.raids import attack_cooldown_left
    last = NOW - timedelta(hours=2, minutes=30)
    assert attack_cooldown_left(last, NOW, 1) > 0             # 3 ч ещё не прошли
    assert attack_cooldown_left(last, NOW, 3) == 0            # 2 ч 20 мин — прошли


def test_next_tech_at():
    from shared.tech import next_tech_at
    assert next_tech_at("attack", 0, None) is None
    assert next_tech_at("attack", 1, None) is None
    assert next_tech_at("attack", 2, NOW) == NOW + timedelta(days=tech_cooldown_days("attack", 2))


def _state(**levels):
    st = {k: {"level": 0, "updated_at": None} for k in (*TECH_ORDER, "tools")}
    for k, v in levels.items():
        st[k] = {"level": v, "updated_at": NOW - timedelta(days=1)}
    return st


def test_build_tech_payload():
    from bots.main_bot.webapp_game import build_tech_payload
    rich = {k: 100_000 for k in ALL_KINDS}
    p = build_tech_payload(_state(tools=1, comm=1, scout=1, attack=1), rich, NOW)
    assert p["tools"]["level"] == 1 and p["tools"]["next"] == 2 and p["tools"]["affordable"]
    by = {x["key"]: x for x in p["techs"]}
    assert [x["key"] for x in p["techs"]] == list(TECH_ORDER)
    assert by["comm"]["next"] == 2 and by["comm"]["wait"] > 0 and not by["comm"]["affordable"]   # 30 дней
    assert by["comm"]["cooldown_days"] == 30
    assert by["defense"]["level"] == 0 and by["defense"]["affordable"]        # 1 уровень — сразу
    assert not by["science"]["gate_ok"] and not by["science"]["affordable"]   # оборона ещё 0
    ready = build_tech_payload(_state(tools=2, comm=1, scout=1, attack=1, defense=1), rich, NOW)
    sci = {x["key"]: x for x in ready["techs"]}["science"]
    assert sci["gate_ok"] and sci["affordable"] and sci["tool"] == 2
    maxed = build_tech_payload(_state(tools=4, comm=5), {}, NOW)
    assert maxed["tools"]["next"] is None and not maxed["tools"]["affordable"]
    m = {x["key"]: x for x in maxed["techs"]}
    assert m["comm"]["next"] is None and m["comm"]["cost"] == {} and not m["comm"]["affordable"]
    poor = build_tech_payload(_state(), {}, NOW)
    assert not any(x["affordable"] for x in poor["techs"])


def test_market_lots_from_horses_and_carts():
    """1 лошадь = +1 лот, 1 телега = +1 лот (телег не больше, чем лошадей); по 5 максимум."""
    assert economy.MAX_HORSES == 5 and economy.MAX_CARTS == 5
    assert market_lots(0, 0, False) == economy.MARKET_BASE_LOTS
    assert market_lots(2, 0, False) == economy.MARKET_BASE_LOTS + 2
    assert market_lots(1, 3, False) == economy.MARKET_BASE_LOTS + 1 + 1
    assert market_lots(5, 5, False) == economy.MARKET_BASE_LOTS + 10
    assert market_lots(0, 0, True) == economy.SHUTTLE_MARKET_MAX_OPEN_ORDERS
    assert market_lots(economy.MAX_HORSES, economy.MAX_CARTS, False) <= economy.SHUTTLE_MARKET_MAX_OPEN_ORDERS


def test_horse_prices_burn_coins_and_grow():
    assert list(economy.HORSE_PRICES) == sorted(economy.HORSE_PRICES) and economy.HORSE_PRICES[0] > 0
    assert economy.MAX_HORSES == len(economy.HORSE_PRICES)
    src = (ROOT / "shared" / "tech.py").read_text(encoding="utf-8")
    assert '"horse_buy"' in src and "change_balance" in src


def test_shuttle_active_needs_charge():
    from shared.tech import shuttle_active
    assert shuttle_active({"has_shuttle": True, "shuttle_until": NOW + timedelta(days=1)}, NOW)
    assert not shuttle_active({"has_shuttle": True, "shuttle_until": NOW - timedelta(seconds=1)}, NOW)
    assert not shuttle_active({"has_shuttle": True, "shuttle_until": None}, NOW)
    assert not shuttle_active({"has_shuttle": False, "shuttle_until": NOW + timedelta(days=9)}, NOW)
    assert economy.SHUTTLE_CHARGE_DAYS == 30


# ---------------------------------------------------------------- рудники: болезни и Ядро

def test_mine_sick_hours():
    from shared.mines import sick_hours
    every = economy.MINE_SICK_EVERY_HOURS
    assert sick_hours(0, every) == 1
    assert sick_hours(0, every - 1) == 0
    assert sick_hours(0, 72) == 72 // every
    assert sum(sick_hours(h, 1) for h in range(72)) == sick_hours(0, 72)      # по частям — столько же


def test_mine_core_marks_capped():
    from shared.mines import core_marks
    day = economy.MINE_CORE_EVERY_HOURS
    assert core_marks(0, day - 1, 0) == 0
    assert core_marks(0, day, 0) == 1
    assert core_marks(0, 72, 0) == min(3, economy.MINE_CORE_MAX)
    assert core_marks(0, 10 * day, 0) == economy.MINE_CORE_MAX
    assert core_marks(0, 72, economy.MINE_CORE_MAX) == 0
    assert sum(core_marks(h, 1, 0) for h in range(72)) == 3


# ---------------------------------------------------------------- сезоны

def test_season_key_and_bounds_calendar_month():
    assert season_key(NOW) == "2026-10"
    start, end = season_bounds(NOW)
    assert start == datetime(2026, 10, 1, tzinfo=timezone.utc) and end == datetime(2026, 11, 1, tzinfo=timezone.utc)
    s, e = season_bounds(datetime(2026, 12, 31, 23, 59, tzinfo=timezone.utc))
    assert s.month == 12 and e == datetime(2027, 1, 1, tzinfo=timezone.utc)
    s, e = season_bounds(datetime(2027, 2, 10, tzinfo=timezone.utc))
    assert (e - s).days == 28
    assert economy.SEASON_FIRST <= season_key(NOW)


def test_previous_season_moment():
    from shared.seasons import previous_season_moment
    prev = previous_season_moment(datetime(2026, 11, 1, 0, 5, tzinfo=timezone.utc))
    assert season_key(prev) == "2026-10"
    prev = previous_season_moment(datetime(2027, 1, 15, tzinfo=timezone.utc))
    assert season_key(prev) == "2026-12"


def test_season_has_no_automatic_prizes_only_badges():
    """Решение владельца 27.10: призы сезона назначает он сам; автоматически — только значок ТОП-10."""
    assert not hasattr(economy, "SEASON_PRIZES") and not hasattr(economy, "SEASON_TEAM_CORES")
    assert economy.SEASON_BADGE_PLACES == 10
    import inspect
    from shared import seasons
    src = inspect.getsource(seasons.finalize_season)
    assert "deliver" not in src and "change_resource" not in src and "change_balance" not in src
    assert set(economy.SEASON_BATTLE_POINTS) == set(range(1, 11))
    assert list(economy.SEASON_BATTLE_POINTS.values()) == sorted(economy.SEASON_BATTLE_POINTS.values(), reverse=True)
    from shared.rewards import TARGETS
    assert "season_prev" in TARGETS


def test_parse_gift():
    from shared.rewards import parse_gift
    assert parse_gift("coins", "500") == {"kind": "coins", "amount": 500}
    assert parse_gift("coins", "0") is None and parse_gift("coins", "-5") is None and parse_gift("coins", "x") is None
    assert parse_gift("resource", "core 3") == {"kind": "resource", "res": "core", "qty": 3}
    assert parse_gift("resource", "gold 3") is None and parse_gift("resource", "wood") is None
    assert parse_gift("item", "shield 24")["effect"] == "shield"
    assert parse_gift("item", "station_drone 5") is None
    assert parse_gift("sku", "cutlet_10") == {"kind": "sku", "sku": "cutlet_10"}
    assert parse_gift("sku", "nope") is None
    assert parse_gift("bogus", "1") is None and parse_gift("coins", "") is None


# ---------------------------------------------------------------- тексты и фронт

def test_new_locale_keys_ru_en():
    from shared.locales import t
    for lang in ("ru", "en"):
        for k in ALL_KINDS:
            assert t(lang, f"res.{k}") != f"res.{k}", (lang, k)
        for k in TECH_ORDER:
            assert t(lang, f"tech.{k}") != f"tech.{k}", (lang, k)
        assert "2" in t(lang, "tech.err_tool", tool=2)
        assert "5" in t(lang, "tech.err_cooldown", hours=5)
        assert "1500" in t(lang, "horse.err_coins", price=1500)
        assert "X" in t(lang, "raid.err_need_tech", tech="X")
        for rid in ("bonfire", "battery", "cart", "meds_72h"):
            assert t(lang, f"ws.recipe_{rid}") != f"ws.recipe_{rid}"
    assert "Камень" in t("ru", "duel.metal_gain", metal=2)
    assert "рофл" not in t("ru", "games.energy_gain").lower()


def test_tech_errors_localize():
    from shared.tech import TechError
    assert "3" in TechError("tech.err_tool", tool=3).localized("ru")
    assert TechError("tech.err_max").localized("en")


def test_frontend_has_lab_season_top_stable():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for needle in ("viewLab", "/api/tech", "/api/tech/up", "/api/horse/buy", "/api/shuttle/charge",
                   "topMode", "mode=rich", "my_mines", "raid_needTech", "lab_rule1", "lab_sciGate", "gate_ok"):
        assert needle in html, needle
    assert "station_drone" not in html and "prize_" not in html
    # сцена фермы и узлы карты рудников — разные классы (иначе сцена «уезжает» влево-вверх)
    assert 'class="mine-scene"' in html and html.count(".mine-scene {") == 1
    assert html.count("  .mine { ") == 1
    assert "/quiz" not in html.split("I18N_EXTRA")[0].split("<script")[0]   # без слэш-команд в разметке


def test_api_routes_registered():
    from bots.main_bot.webapp import create_webapp
    app = create_webapp("123456:TEST")
    paths = {r.resource.canonical for r in app.router.routes() if r.resource is not None}
    for p in ("/api/tech", "/api/tech/up", "/api/horse/buy", "/api/shuttle/charge", "/api/top"):
        assert p in paths, p


def test_admin_has_reward_and_season():
    src = (ROOT / "bots" / "admin_notifier_bot" / "bot.py").read_text(encoding="utf-8")
    for needle in ('Command("reward")', 'Command("season")', "check_season_end", "give_all"):
        assert needle in src, needle
    assert "award_battle_cores" not in src          # автоматического Ядра за битвы больше нет


def test_schema_has_new_tables_and_migration():
    from shared.database import SCHEMA_STATEMENTS
    sql = "\n".join(SCHEMA_STATEMENTS)
    for needle in ("user_tech", "user_badges", "season_results", "meds_until", "shuttle_until", "horses", "carts",
                   "cores_paid", "migr:resources_v3"):
        assert needle in sql, needle


def test_friends_rating_is_seasonal():
    """«Рейтинг друзей» обнуляется каждый сезон: считаются друзья этого месяца."""
    import inspect
    from bots.main_bot import webapp_game
    src = inspect.getsource(webapp_game.handle_referral)
    assert "season_bounds(now)" in src and "qualified_at >= $2" in src and '"season"' in src
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "fmt(L.top_seasonTitle, { s: d.season })" in html


def test_full_reset_migration_is_last_backed_up_and_keeps_payments():
    """Полный сброс 27.10: последний в схеме, с бэкапом, разовый, платежи и тумблеры не трогает."""
    from shared.database import RESET_ALL_STATEMENT, RESET_TABLES, SCHEMA_STATEMENTS
    assert SCHEMA_STATEMENTS[-1] is RESET_ALL_STATEMENT
    for keep in ("star_payments", "feature_flags", "promoters", "mines"):
        assert keep not in RESET_TABLES
    for t in ("users", "ledger", "miners", "game_stats", "user_resources", "teams", "user_tech", "vip_aliases"):
        assert t in RESET_TABLES
    assert "reset_backup_20261027" in RESET_ALL_STATEMENT and "migr:full_reset_20261027" in RESET_ALL_STATEMENT
    assert "pg_advisory_xact_lock" in RESET_ALL_STATEMENT
    assert RESET_ALL_STATEMENT.index("CREATE TABLE IF NOT EXISTS reset_backup") < RESET_ALL_STATEMENT.index("TRUNCATE")
    import re
    created = set(re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)", "\n".join(SCHEMA_STATEMENTS)))
    assert set(RESET_TABLES) <= created


def test_storage_levels_grow_20_percent_and_one_kind_each():
    """Склад 27.10: 500 → 1000 → 2000 → 3000 → 4000 → 5000; каждое расширение на 20% дороже и на вид сложнее."""
    from shared.economy import RES_CAPACITY_MAX, STORAGE_LEVELS, items_capacity, next_storage_level
    caps = [c for c, _ in STORAGE_LEVELS]
    assert caps == [1000, 2000, 3000, 4000, 5000] and RES_CAPACITY_MAX == 5000
    kinds = [len(cost) for _, cost in STORAGE_LEVELS]
    assert kinds == [2, 3, 4, 5, 6]
    totals = [sum(cost.values()) for _, cost in STORAGE_LEVELS]
    for prev, cur in zip(totals, totals[1:]):
        assert prev * 1.15 <= cur <= prev * 1.30, totals                 # ≈ +20% (округление до десятков)
    capacity = 500
    for cap, cost in STORAGE_LEVELS:                                     # каждое оплачивается в пределах текущей вместимости
        assert all(v <= capacity for v in cost.values()), cap
        capacity = cap
    assert next_storage_level(5000) is None
    assert [items_capacity(c) for c in (500, 1000, 2000, 5000)] == [50, 100, 200, 500]


def test_raid_scout_spends_no_battery_and_ui_matches():
    import inspect
    from shared import raids
    assert '"battery"' not in inspect.getsource(raids.scout)
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "🔋 ' + d.batteries" not in html


def test_storage_ui_merges_cutlets_and_counts_items():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "cutCard" not in html and "L.sk_cutletsName" in html and "L.sk_items" in html
    assert "resCard = '<div class=\"card span-all\">" in html             # одна плашка во всю ширину
    assert ".res-cols {" in html


def test_mines_map_free_brighter_held_armored():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert ".mine.held::before" in html and "repeating-conic-gradient" in html
    assert ".mine.free { opacity: .55; }" not in html


def test_shop_stars_hint_on_both_showcases():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert html.count("'<div class=\"hint\">' + L.shopHint + '</div>'") == 2


def test_workshop_sources_cover_every_resource():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for k in ALL_KINDS:
        assert f"res_{k}_src:" in html, k
    assert 'res_metal_src: "КНБ"' in html                                # дуэли дают камень, не металл
