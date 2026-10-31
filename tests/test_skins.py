"""
✨ Скины, 🎟 пропуск сезона и 🏆 трофеи (решения владельца 30.10) — чистые правила без БД.
Интеграционный сценарий (тираж, коллекция, закалка, рынок, трофеи, пропуск) — в test_db_integration.py.
"""
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from shared import season_pass as sp  # noqa: E402
from shared import skins as sk  # noqa: E402
from shared.locales import PACK_CODES, t  # noqa: E402
from shared.trophies import EVENTS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static/webapp/index.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------- многоступенчатая прокачка
def test_levels_need_both_battle_xp_and_merges():
    assert sk.SKIN_MAX_LEVEL == len(sk.SKIN_LEVELS) == 10
    xs, ms = [x for x, _ in sk.SKIN_LEVELS], [m for _, m in sk.SKIN_LEVELS]
    assert xs == sorted(xs) and ms == sorted(ms) and len(set(xs)) == len(xs)
    # одной игрой не дойти: без слияний потолок — 3 уровень, сколько ни играй
    assert sk.skin_level(10 ** 9, 0) == 3
    # одними слияниями тоже: без опыта — 1 уровень
    assert sk.skin_level(0, 1000) == 1
    assert sk.skin_level(10 ** 9, 10 ** 3) == sk.SKIN_MAX_LEVEL
    assert sk.next_level_need(10 ** 9, 10 ** 3) is None
    assert sk.next_level_need(150, 0) == {"level": 4, "xp": 0, "merged": 1}       # опыта хватает — ждёт слияния
    assert sk.next_level_need(150, 1) == {"level": 5, "xp": 150, "merged": 0}


def test_six_stages_from_factory_to_immortal():
    assert [k for _, k in sk.SKIN_STAGES] == ["factory", "tempered", "combat", "veteran", "legend", "immortal"]
    assert sk.skin_stage(1) == "factory" and sk.skin_stage(3) == "tempered" and sk.skin_stage(10) == "immortal"
    # зеркало ступеней в приложении совпадает с сервером
    m = re.search(r"const SK_STAGES = (\[.*?\]\]);", HTML)
    assert m and eval(m.group(1)) == [list(x) for x in sk.SKIN_STAGES]
    for _, st in sk.SKIN_STAGES:
        assert f".st-c-{st}" in HTML or st == "factory"


def test_merge_xp_grows_with_rarity_and_floors_on_market():
    order = ["common", "rare", "epic", "legendary", "mythic"]
    assert [sk.SKIN_MERGE_XP[r] for r in order] == sorted(sk.SKIN_MERGE_XP.values())
    assert [sk.SKIN_MIN_PRICE[r] for r in order] == sorted(sk.SKIN_MIN_PRICE.values())
    assert set(sk.RARITY_COLOR) == set(order)


def test_trophy_events_are_the_same_everywhere():
    assert set(sk.SKIN_EVENT_XP) == set(sp.PASS_XP) == set(EVENTS)
    icons = re.search(r"const TR_ICON = \{(.*?)\};", HTML, re.S).group(1)
    assert set(re.findall(r"(\w+): \"", icons)) == set(EVENTS)
    for ev in EVENTS:
        assert f"tr_{ev}:" in HTML


def test_skins_give_no_power_and_paid_ones_are_concrete():
    for sid, s in sk.SKINS.items():
        assert s["target"] in sk.TARGETS and s["rarity"] in sk.RARITY_COLOR
        assert set(s) <= {"set", "target", "rarity", "look", "name", "name_en", "stars", "edition", "until", "pass",
                          "text", "text_en"}, sid
        assert {"c1", "c2", "fx"} <= set(s["look"]), sid


# ---------------------------------------------------------------- 🎟 пропуск сезона
def test_pass_paid_track_has_four_exclusive_skins_that_are_never_sold():
    season = "2026-11"
    ids = sp.pass_skin_ids(season)
    paid_skins = {lvl: r["skin"] for lvl in range(1, sp.PASS_LEVELS + 1)
                  for r in sp.rewards(season, "paid", lvl) if r["kind"] == "skin"}
    assert paid_skins == {5: ids["marker"], 10: ids["frame"], 20: ids["title"], 30: ids["suit"]}
    for sid in ids.values():
        assert sid in sk.SKINS and sk.SKINS[sid]["stars"] is None
        assert not sk.for_sale(sid, datetime(2026, 11, 5, tzinfo=timezone.utc))
    # бесплатная дорожка — без скинов, платная на каждом уровне щедрее
    for lvl in range(1, sp.PASS_LEVELS + 1):
        free, paid = sp.rewards(season, "free", lvl), sp.rewards(season, "paid", lvl)
        assert all(r["kind"] != "skin" for r in free)
        assert paid[0]["amount"] > free[0]["amount"]


def test_pass_sale_switches_to_next_month_in_the_last_week():
    assert sp.sale_season(datetime(2026, 11, 10, tzinfo=timezone.utc)) == "2026-11"
    assert sp.sale_season(datetime(2026, 11, 27, tzinfo=timezone.utc)) == "2026-12"
    assert sp.can_buy("2026-11", datetime(2026, 11, 27, tzinfo=timezone.utc))
    assert not sp.can_buy("2026-10", datetime(2026, 11, 2, tzinfo=timezone.utc))
    assert sp.season_of_sku(sp.pass_sku("2026-12")) == "2026-12"
    assert sp.season_of_sku("seasonpass_202613") is None and sp.season_of_sku("seasonpass_x") is None
    oct30 = datetime(2026, 10, 30, tzinfo=timezone.utc)
    assert sp.active_season(oct30) == sp.PASS_FIRST and not sp.can_buy("2026-10", oct30) and sp.can_buy("2026-11", oct30)
    assert sp.season_end("2026-11") > datetime(2026, 11, 30, 23, tzinfo=timezone.utc)
    assert sp.pass_level(0) == 0 and sp.pass_level(250) == 2 and sp.pass_level(10 ** 6) == sp.PASS_LEVELS


def test_future_pass_skins_are_hidden_from_the_catalog(monkeypatch):
    import shared.economy as economy
    monkeypatch.setattr(economy, "utcnow", lambda: datetime(2026, 11, 3, tzinfo=timezone.utc))
    cat = sk.public_catalog("ru")
    assert sp.pass_skin_ids("2026-11")["suit"] in cat
    assert sp.pass_skin_ids("2027-01")["suit"] not in cat


def test_pass_order_builds_only_for_the_season_on_sale():
    from bots.main_bot.catalog import CatalogError, get_item
    from shared.economy import utcnow
    item = get_item(sp.pass_sku(sp.sale_season(utcnow())))
    assert item["type"] == "season_pass" and item["stars"] == sp.PASS_STARS
    with pytest.raises(CatalogError):
        get_item(sp.pass_sku("2026-01"))


# ---------------------------------------------------------------- приложение и тексты
def test_avatar_is_drawn_with_hands_not_balls_and_no_param_shadowing():
    body = HTML[HTML.index("function avatarSvg(gender, worn, look, skLvl)"):HTML.index("const effText =")]
    assert "const look" not in body and "const skin " not in body and "const worn" not in body
    assert re.search(r"const hand = \w+ =>", body) and "fingers" in body
    assert 'filterUnits="userSpaceOnUse"' in body          # свечение не обрезается прямоугольником


def test_avatar_is_one_silhouette_and_scientist_suit_is_drawn():
    """Владелец 31.10: руки и ноги не «отдельно от туловища», у Ж без акцента на груди; учёный — свой рисунок."""
    body = HTML[HTML.index("function avatarSvg(gender, worn, look, skLvl)"):HTML.index("const effText =")]
    # контур всей фигуры одним проходом под заливками — стыков рук/ног с туловищем не видно
    assert "[leg(-1), leg(1), boot(-1), boot(1), neck, arm(-1), arm(1), torso, hand(-1), hand(1), headD].map(" in body
    assert "q4.5,5 9,0" not in body                          # линии груди больше нет
    assert "kn:" in body                                     # колено/икра/лодыжка от параметра фигуры
    # рисунки костюмов — общая карта SUIT_DECO; деталь без рисунка красится цветом костюма
    for slot in ("head", "body", "hands", "legs", "feet"):
        assert 'deco("' + slot + '")' in body, slot
    # учёный: халат, шлем с визором-дисплеем (моргает), штаны с лампасом, ботинки
    assert "sc: { head: () => scHead(), body: () => scBody(), legs: () => scLegs(), feet: () => scFeet() }" in body
    assert 'attributeName="height"' in body                  # моргание на визоре
    # электрик: каска с фонарём, куртка со светоотражающими полосами, краги с искрой, полосы на голенях, жёлтые носы
    assert "el: { head: elHead, body: elBody, hands: elHands, legs: elLegs, feet: elFeet }" in body
    paint = re.search(r"const SUIT_PAINT = (\{.*?\} \});", HTML, re.S).group(1)
    for suit in ("sc", "el"):
        assert re.search(suit + r": \{ head: .*?, body: .*?, hands: .*?, legs: .*?, feet: .*? \}", paint), suit


def test_shop_has_separate_skins_category_and_persona_has_pass_tab():
    assert '["skins", L.shopSkins]' in HTML and "viewShopSkins" in HTML
    assert '["pass", L.gr_tabPass]' in HTML and "async function viewPass(" in HTML


def test_pass_texts_in_every_language():
    for lang in ("ru", "en", *PACK_CODES):
        for key in ("pass.err_nothing", "pass.err_owned"):
            assert t(lang, key) != key, (lang, key)
        assert "11.2026" in t(lang, "pass.delivered", season="11.2026")


def test_pass_xp_goes_to_the_season_shown_on_screen(monkeypatch):
    """30–31.10 экран показывает ноябрьский пропуск — опыт должен капать туда же, а не в «октябрь»."""
    import asyncio
    monkeypatch.setattr(sp, "utcnow", lambda: datetime(2026, 10, 30, 12, tzinfo=timezone.utc))
    calls = []

    class Conn:
        async def execute(self, sql, *args):
            calls.append(args)
    asyncio.run(sp.add_xp(Conn(), 1, "quest"))
    assert calls and calls[0][1] == sp.PASS_FIRST == sp.active_season(datetime(2026, 10, 30, tzinfo=timezone.utc))
