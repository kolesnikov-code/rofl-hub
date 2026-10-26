"""
🗺 Экспедиции и 🤖 боевые дроны (решение владельца 28.10): чистые правила, тексты, маршруты, пульт.
Сценарии с базой (выход, развилки, голосование, итоги, возвраты, покупка дронов) — в test_db_integration.py.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from shared import economy
from shared.expedition_events import EVENTS, EVENTS_BY_ID, event_for, event_text
from shared.expeditions import (apply_option, decide, distance, fork_schedule, gear_needed, origin_for, progress,
                                squad_mode)

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 28, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- дроны
def test_drone_raid_percent_stacks_with_caps_and_floor():
    f = economy.drone_raid_loot_percent
    assert f(100, 0, 0) == 100                       # без дронов — как было
    assert f(100, 3, 0) == 115 and f(100, 0, 2) == 90 and f(100, 2, 2) == 100
    assert f(100, 50, 0) == 100 + economy.DRONE_RAID_CAP_PCT          # потолок бонуса
    assert f(60, 0, 50) == economy.DRONE_RAID_MIN_LOOT_PCT            # пол трофея
    assert economy.drone_spy_targets(2) == 2 and economy.drone_spy_targets(99) == economy.DRONE_SPY_TARGETS_CAP


def test_drone_expedition_effects_capped():
    eff = economy.drone_exp_effects(2, 3, 4)
    assert eff == {"cargo": 6, "guard": 15, "speed": 8}
    big = economy.drone_exp_effects(1000, 1000, 1000)
    assert big == {"cargo": economy.DRONE_EXP_CARGO_CAP, "guard": economy.DRONE_EXP_GUARD_CAP,
                   "speed": economy.DRONE_EXP_SPEED_CAP}


def test_drones_are_exclusive_like_the_shuttle():
    shuttle = economy.WORKSHOP_RECIPES["shuttle"]
    for kind in economy.DRONE_KINDS:
        r = economy.WORKSHOP_RECIPES[f"drone_{kind}"]
        assert r["effect"] == "bdrone" and r["drone"] == kind and r["tool"] == 3
        assert all(r["cost"][k] >= v for k, v in shuttle["cost"].items())   # не дешевле Шаттла
        assert r["coins"] >= shuttle["coins"]
        assert r["effect"] not in economy.ITEM_EFFECTS                     # не лежат на складе изделий
    assert economy.DRONE_COIN_PRICE >= 50_000                              # купить — только за большие монеты


# ---------------------------------------------------------------- экспедиции: правила
def test_scope_and_travel_rules():
    assert economy.exp_mode_allowed("solo", "solo") and not economy.exp_mode_allowed("solo", "team")
    assert economy.exp_mode_allowed("teams", "team") and economy.exp_mode_allowed("teams", "clan")
    assert not economy.exp_mode_allowed("teams", "solo") and not economy.exp_mode_allowed("clan", "team")
    solo, team, clan = (economy.exp_travel_minutes(100, m) for m in ("solo", "team", "clan"))
    assert solo < team < clan                         # большой отряд идёт медленнее
    assert economy.exp_travel_minutes(100, "team", 20) < team   # шпионы сокращают путь
    assert economy.exp_travel_minutes(0.1, "solo") == economy.EXP_MIN_TRAVEL_MINUTES
    assert economy.exp_travel_minutes(100, "solo", 999) == economy.exp_travel_minutes(100, "solo", economy.DRONE_EXP_SPEED_CAP)


def test_gear_by_squad_type():
    assert gear_needed("solo") == {"hydrogen": economy.EXP_SOLO_HYDROGEN}
    assert gear_needed("team") == {"battery": economy.EXP_BATTERIES["team"]}           # командам котлеты не нужны
    assert gear_needed("clan") == {"battery": economy.EXP_BATTERIES["clan"], "cutlet": economy.EXP_CLAN_CUTLETS}
    assert squad_mode(50) == "team" and squad_mode(1000) == "clan" and squad_mode(None) == "team"


def test_origins_on_map_edge_and_stable():
    seen = set()
    for i in range(1, 60):
        x, y = origin_for("team", i)
        assert 0 <= x <= economy.EXP_MAP_W and 0 <= y <= economy.EXP_MAP_H
        assert distance(x, y, economy.EXP_MAP_W / 2, economy.EXP_MAP_H / 2) > 30   # на краю, а не в центре
        seen.add((round(x), round(y)))
    assert len(seen) > 40                                              # с разных направлений
    assert origin_for("solo", 7) == origin_for("solo", 7) and origin_for("solo", 7) != origin_for("team", 7)


def test_fork_schedule_equal_parts():
    sched = fork_schedule(NOW, 400, 3)
    assert [o for o, _ in sched] == [NOW + timedelta(minutes=100 * i) for i in (1, 2, 3)]
    assert sched[-1][1] == NOW + timedelta(minutes=400)               # последнее голосование — до прибытия
    assert all(c > o for o, c in sched)


def test_decide_majority_tie_earliest_and_default():
    t = lambda m: NOW + timedelta(minutes=m)    # noqa: E731
    assert decide([], 3) == (0, 0)                                    # молчание — самый осторожный вариант
    assert decide([(2, t(5)), (2, t(6)), (1, t(1))], 3) == (2, 2)     # большинство
    assert decide([(1, t(3)), (2, t(1))], 3) == (2, 1)                # ничья — кто раньше
    assert decide([(9, t(1)), (1, t(2))], 3) == (1, 1)                # мусорный вариант не считается


def test_apply_option_drones_change_outcome():
    fight = {"cargo": 40, "loss": 20, "delay": 10, "fight": True}
    assert apply_option(100, fight, {}) == (120, 10)                  # +40 − 20% от 100
    assert apply_option(100, fight, {"cargo": 50, "guard": 50}) == (150, 10)   # +60 − 10
    calm = {"cargo": 10, "loss": 0, "delay": -30}
    assert apply_option(100, calm, {"cargo": 60}) == (110, -30)       # не силовой — атакующие не помогают
    assert apply_option(0, {"cargo": -10}, {}) == (0, 0)              # груз не уходит в минус


def test_progress_of_marker():
    exp = {"departed_at": NOW, "arrive_at": NOW + timedelta(hours=4)}
    assert progress(exp, NOW) == 0 and progress(exp, NOW + timedelta(hours=1)) == 0.25
    assert progress(exp, NOW + timedelta(hours=9)) == 1 and progress({"departed_at": None, "arrive_at": None}, NOW) == 0


def test_events_are_decisions_with_texts():
    assert len(EVENTS) >= 10 and len(EVENTS_BY_ID) == len(EVENTS)
    for e in EVENTS:
        assert e["text"]["ru"] and e["text"]["en"] and 2 <= len(e["options"]) <= 3
        outcomes = {(o.get("cargo", 0), o.get("loss", 0), o.get("delay", 0)) for o in e["options"]}
        assert len(outcomes) == len(e["options"])                      # варианты действительно разные
        for o in e["options"]:
            assert o["text"]["ru"] and o["text"]["en"] and 0 <= o.get("loss", 0) <= 30
            assert "рофл" not in o["text"]["ru"].lower()
    assert event_text({"ru": "А", "en": "B"}, "de") == "B"


def test_event_sequence_has_no_repeats_within_squad():
    for exp_id in range(1, 40):
        ids = [event_for(exp_id, k)["id"] for k in range(1, economy.EXP_FORKS_MAX + 1)]
        assert len(set(ids)) == len(ids)


# ---------------------------------------------------------------- пульт, маршруты, тексты
def test_admin_target_form_validation():
    from bots.main_bot.webapp_admin import validate_target_form
    base = {"title": "Цитадель", "scope": "solo", "x": 80, "y": 50, "forks": 3, "hours": 24, "places": 2,
            "prizes": {"1": [{"kind": "coins", "amount": 500}], "5": [{"kind": "coins", "amount": 5}]},
            "reward_all": [{"kind": "resource", "res": "core", "qty": 1}]}
    form, err = validate_target_form(base, NOW, 0)
    assert err is None and form["resolve_at"] == NOW + timedelta(hours=24)
    assert form["prizes"] == {"1": [{"kind": "coins", "amount": 500}]} and form["reward_all"][0]["res"] == "core"
    for patch, needle in (({"title": ""}, "Название"), ({"scope": "x"}, "зачёт"), ({"x": None}, "карте"),
                          ({"x": 1}, "края"), ({"forks": 9}, "Развилок"), ({"hours": 0}, "Итоги"), ({"places": 101}, "мест")):
        form, err = validate_target_form({**base, **patch}, NOW, 0)
        assert form is None and needle in err, (patch, err)
    form, err = validate_target_form(base, NOW, economy.EXP_MAX_TARGETS)
    assert form is None and str(economy.EXP_MAX_TARGETS) in err       # не больше 10 целей сразу


def test_routes_registered():
    from bots.main_bot.webapp import create_webapp
    app = create_webapp("123456:TEST")
    paths = {r.resource.canonical for r in app.router.routes() if r.resource is not None}
    for p in ("/api/map", "/api/exp/solo", "/api/exp/gear", "/api/exp/vote", "/api/drone/buy",
              "/api/admin/targets", "/api/admin/target", "/api/admin/target/close"):
        assert p in paths, p


def test_feature_flag_and_tab():
    from shared.feature_flags import FLAG_DEFAULTS, FLAG_TITLES
    assert FLAG_DEFAULTS["expeditions"] is True and "expeditions" in FLAG_TITLES
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert '"mines", "map", "friends"' in html and 'map: "expeditions"' in html and "function viewMap" in html
    for needle in ("/api/map", "/api/exp/solo", "/api/exp/gear", "/api/exp/vote", "/api/drone/buy", "L.dr_title",
                   "data-countdown", "mapPos("):
        assert needle in html, needle
    admin = (ROOT / "static" / "webapp" / "admin.html").read_text(encoding="utf-8")
    for needle in ("viewExp", "/api/admin/targets", "/api/admin/target/close", '["bdrone",'):
        assert needle in admin, needle


def test_expedition_texts_in_every_language():
    from shared.locales import MINIAPP_PACKS, PACK_CODES, t
    for lang in ("ru", "en") + tuple(PACK_CODES):
        for key in ("post.scope_teams", "rn.place", "exp.err_late", "ws.recipe_drone_spy"):
            assert t(lang, key, scope="X", need=1, have=0, title="T", place=1) != key, (lang, key)
    for code in PACK_CODES:
        assert "tab_map" in MINIAPP_PACKS[code] and "dr_eff_spy" in MINIAPP_PACKS[code]
    ru = t("ru", "rn.where")
    assert "Railway" not in ru and "рофл" not in ru.lower() and "/" not in ru     # без слэш-команд в приложении


def test_fork_can_be_chosen_ahead_and_fires_at_the_fork():
    """26.10: ближайшую развилку видно сразу (выбор заранее), срабатывает выбор, когда отряд до неё дошёл."""
    from shared.expeditions import current_fork, decided_early, fork_window
    exp = {"status": "marching", "forks_done": 0, "departed_at": NOW, "planned_minutes": 90,
           "arrive_at": NOW + timedelta(minutes=90)}
    assert current_fork(exp, 2, NOW + timedelta(minutes=1)) == 1           # ещё в пути — уже можно выбрать
    open_at, close_at = fork_window(exp, 2, 1)
    assert open_at == NOW + timedelta(minutes=30) and close_at == NOW + timedelta(minutes=60)
    assert current_fork(exp, 2, NOW + timedelta(minutes=91)) is None        # пришли — развилок больше нет
    assert decided_early("solo", 1, 1) and not decided_early("solo", 0, 1)
    assert decided_early("team", 3, 3) and not decided_early("team", 2, 3) and not decided_early("team", 0, 0)


def test_events_and_auctions_in_the_app():
    from bots.main_bot.webapp import create_webapp
    app = create_webapp("123456:TEST")
    paths = {r.resource.canonical for r in app.router.routes() if r.resource is not None}
    assert {"/api/news", "/api/auctions", "/api/auction/bid"} <= paths
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert '"market", "auctions", "team"' in html and "function viewAuctions" in html and 'auctions: "auctions"' in html
    assert "function newsCard" in html and '"/api/news"' in html and "map_forkAhead" in html and "L.map_cargoHint" in html
    assert 'class="hint fr-hint"' in html                                    # отступ под холодильником
    from shared.feature_flags import FLAG_DEFAULTS
    assert FLAG_DEFAULTS["auctions"] is True
    admin = (ROOT / "static" / "webapp" / "admin.html").read_text(encoding="utf-8")
    assert "function flushRewards" in admin and admin.count("flushRewards()") >= 3 and "confirmPrizes(" in admin
    assert 'kind: "lot"' in admin and "канал" not in admin


def test_admin_lot_form():
    from bots.main_bot.webapp_admin import validate_lot_form
    form, err = validate_lot_form({"title": " VIP-пост ", "descr": "x" * 900})
    assert err is None and form["title"] == "VIP-пост" and len(form["descr"]) == 500
    assert validate_lot_form({"title": ""})[0] is None


@pytest.mark.parametrize("kind", ["guard", "attack", "spy"])
def test_drone_reward_kind(kind):
    from shared.prizes import normalize_reward, rewards_label
    r = normalize_reward({"kind": "bdrone", "drone": kind, "qty": 3})
    assert r == {"kind": "bdrone", "drone": kind, "qty": 3} and "×3" in rewards_label([r])


# ---------------------------------------------------------------- 28.10 (вечер): разведка развилок, большие карты
def test_peek_budget_is_min_of_spies_and_scouting():
    f = economy.exp_peek_budget
    assert f(5, 5, 5, False) == 5                      # 5 шпионов и разведка 5 — видно все 5 развилок
    assert f(1, 1, 5, False) == 1 and f(5, 1, 5, False) == 1 and f(1, 5, 5, False) == 1   # по меньшему
    assert f(5, 5, 3, False) == 3                      # не больше развилок
    assert f(5, 5, 5, True) == 0 and f(0, 5, 5, False) == 0   # первая экспедиция сезона — вслепую


def test_compact_maps_ten_targets_thirty_mines():
    """Карты целиком на экране, до 10 целей (26.10: соло И командные), 30 рудников (6 ресурсов по 5) — только командам."""
    assert economy.EXP_MAX_TARGETS == 10 and economy.MINES_COUNT == 30
    assert economy.EXP_SCOPES == ("solo", "team", "clan", "teams")
    assert (economy.EXP_MAP_W, economy.EXP_MAP_H) == (160, 100)
    from shared.database import SCHEMA_STATEMENTS
    seed = next(x for x in SCHEMA_STATEMENTS if "INSERT INTO mines" in x)
    assert "generate_series(1, 30)" in seed and "'energy'" not in seed and "'core'" not in seed
    assert any("migr:mines_30" in x and "DELETE FROM mines WHERE id > 30" in x for x in SCHEMA_STATEMENTS)
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "dragScroll" not in html and "minemap-scroll" not in html            # без перетаскивания
    assert "/api/exp/peek" in html and "L.map_peekBlind" in html


def test_row_labels_never_wrap_values_do():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert ".row .k { color: var(--muted); white-space: nowrap;" in html
    assert ".row .k:only-child { white-space: normal;" in html


def test_rules_mention_only_the_safe_as_random():
    rules = (ROOT / "static" / "webapp" / "rules.html").read_text(encoding="utf-8")
    assert "кубики" not in rules.lower() and "подбрасывание монеты" not in rules.lower()
    assert "Кибер-Сейф" in rules and "28.10.2026" in rules


def test_long_prize_is_shortened_in_events_and_never_widens_the_page():
    """26.10: приз из 20+ наград растягивал паспорт вбок — в ленте только первые 3 и «… +N»."""
    from bots.main_bot.webapp_events import short_rewards_label
    rewards = [{"kind": "resource", "res": r, "qty": 10} for r in ("metal", "hydrogen", "crystal", "parts", "stone")]
    label = short_rewards_label(rewards)
    assert label.count("+ ") == 2 and label.endswith("… +2")
    assert short_rewards_label(rewards[:2]) == "10 ⛏ + 10 💧"
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "#app { overflow-x: clip; }" in html and 'class="nw"' not in html
