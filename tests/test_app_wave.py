"""
Волна 23.10: игровое приложение вместо простыней в чате, монетка 🪙, Стажёр первым на ферме.
"""
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytest.importorskip("aiogram")
os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from shared.locales import EN, MINIAPP_PACKS, PACK_CODES, RU  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- ссылки в приложение
def test_app_url_builds_tab_query_and_validates_tab():
    from bots.main_bot.webapp_links import app_url
    assert app_url("farm", base="https://x.app") == "https://x.app?tab=farm"
    assert app_url("raids", base="https://x.app/?v=2") == "https://x.app/?v=2&tab=raids"
    assert app_url(None, base="https://x.app") == "https://x.app"
    assert app_url("farm", base="") is None
    with pytest.raises(ValueError):
        app_url("nope", base="https://x.app")


# ---------------------------------------------------------------- чат: короче и по одной кнопке
def test_games_hub_is_one_button_per_row_without_raids_and_workshop():
    from bots.main_bot.handlers.menu import get_games_inline_keyboard
    for lang in ("ru", "en", "de", "ar"):
        kb = get_games_inline_keyboard(lang)
        assert all(len(row) == 1 for row in kb.inline_keyboard), lang
        data = {b.callback_data for row in kb.inline_keyboard for b in row}
        assert "open_raids" not in data and "open_workshop" not in data


def _farm_user(**over):
    user = {
        "boost_nuclear_until": None, "boost_nitrogen_until": None, "drone_until": None,
        "farm_armor_level": 0, "armor_until": None, "intern_claimed": True, "interns_pending": 0, "fridge_cutlets": 1, "fridge_capacity": 1,
        "inv_cutlets": 0,
    }
    user.update(over)
    return user


def test_farm_dashboard_lists_intern_first_and_uses_coin_emoji():
    from bots.main_bot.handlers.farm import render_farm_text
    from shared.farm_logic import MinerState
    miners = [MinerState(1, "intern", NOW - timedelta(days=1), NOW + timedelta(days=36500))]
    for lang in ("ru", "en"):
        text = render_farm_text(_farm_user(), miners, NOW, lang)
        intern_pos = text.index("Стажёр" if lang == "ru" else "Intern")
        junior_pos = text.index("Младшие Майнеры" if lang == "ru" else "Miner")
        assert intern_pos < junior_pos, lang
        assert "🪙/ч" in text or "🪙/h" in text
    ru = render_farm_text(_farm_user(), miners, NOW, "ru")
    assert "Кибер-Бурильщиков в /shop" not in ru and "помощнее" in ru


def test_farm_shows_intern_line_even_with_zero_robots():
    from bots.main_bot.handlers.farm import render_farm_text
    text = render_farm_text(_farm_user(intern_claimed=False), [], NOW, "ru")
    assert "Роботы-Стажёры" in text and "Бесплатный" not in text


# ---------------------------------------------------------------- 🪙 вместо слова при числе
@pytest.mark.parametrize("lang,word", [("ru", r"монет[а-яё]*"), ("en", r"coins?\b")])
def test_no_coin_word_after_numbers(lang, word):
    strings = RU if lang == "ru" else EN
    pattern = re.compile(r"(?:\d|\})(?:</b>|</code>)?[  ]+" + word, re.I)
    offenders = [k for k, v in strings.items() if k != "img.balance" and pattern.search(v)]
    assert not offenders, offenders


def test_passport_image_text_keeps_word():
    """Картинка паспорта рисуется шрифтом без эмодзи — там слово остаётся."""
    assert "🪙" not in RU["img.balance"] and "🪙" not in EN["img.balance"]


# ---------------------------------------------------------------- приложение
def _miniapp_ru_keys() -> set[str]:
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    block = html[html.index("    ru: {"):html.index("    en: {")]
    return set(re.findall(r"(?:^|[\s,{])([A-Za-z_][A-Za-z0-9_]*):\s*\"", block))


def test_miniapp_ru_and_en_have_same_keys():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    en_block = html[html.index("    en: {"):html.index("// I18N_EXTRA_START")]
    en_keys = set(re.findall(r"(?:^|[\s,{])([A-Za-z_][A-Za-z0-9_]*):\s*\"", en_block))
    assert _miniapp_ru_keys() == en_keys
    for key in ("tab_farm", "tab_workshop", "tab_raids", "tab_market", "raid_rule1", "ws_craft", "mk_sell"):
        assert key in en_keys


@pytest.mark.parametrize("code", PACK_CODES)
def test_every_pack_covers_the_whole_app(code):
    missing = _miniapp_ru_keys() - set(MINIAPP_PACKS[code])
    assert not missing, f"{code}: нет ключей приложения {sorted(missing)[:10]}"


def test_index_has_no_slash_commands_in_ru_app_texts():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    block = html[html.index("    ru: {"):html.index("    en: {")]
    texts = re.findall(r":\s*\"([^\"]*)\"", block)
    commands = [x for x in texts if re.search(r"(?<![\w/])/[a-z_]{3,}", x) and "noProfile" not in x]
    assert all("/start" in x for x in commands), commands   # единственное исключение — «нажми /start»


def test_workshop_payload_marks_affordable_and_done():
    from bots.main_bot.webapp_game import build_workshop_payload
    stock = {"metal": 25, "hydrogen": 20, "crystal": 10, "parts": 0}
    payload = build_workshop_payload(stock, armor_level=3, has_shuttle=True, lang="ru", balance=5000)
    by_id = {r["id"]: r for r in payload["recipes"]}
    assert by_id["nitro_6h"]["affordable"] and by_id["shield_24h"]["affordable"]
    assert not by_id["nuclear_3h"]["affordable"]
    assert not by_id["armor"]["done"] and by_id["armor"]["days"] == 30   # броню можно продлить
    assert by_id["shuttle"]["done"]
    rich = {k: 5000 for k in stock}
    poor = build_workshop_payload(rich, armor_level=0, has_shuttle=False, lang="ru", balance=999)
    assert not {r["id"]: r for r in poor["recipes"]}["shuttle"]["affordable"]   # нет 1000 🪙
    assert {r["id"]: r for r in poor["recipes"]}["shuttle"]["coins"] == 1000
    assert [r["id"] for r in payload["recipes"]][0] == "nitro_6h"
    assert payload["res_names"]["metal"] == "Металл"


def test_sell_preview_matches_market_fee():
    from bots.main_bot.webapp_game import sell_preview
    assert sell_preview(10, 50, shuttle=False) == {"total": 500, "fee": 50, "got": 450}
    assert sell_preview(10, 50, shuttle=True) == {"total": 500, "fee": 25, "got": 475}
    assert sell_preview(-1, 50, shuttle=False)["total"] == 0


def test_game_routes_are_registered():
    from bots.main_bot.webapp import create_webapp
    app = create_webapp("123456:TEST")
    paths = {r.resource.canonical for r in app.router.routes() if r.resource is not None}
    for path in ("/api/workshop", "/api/craft", "/api/raids", "/api/raid/scout", "/api/raid/go",
                 "/api/market", "/api/market/buy", "/api/market/sell", "/api/market/cancel",
                 "/api/team", "/api/station/donate", "/api/goals", "/api/goals/claim", "/api/refuel"):
        assert path in paths, path


def test_raid_scout_slots_hide_ids_and_expire():
    from bots.main_bot import webapp_game as wg
    wg._remember_slots(1, [777, 888])
    assert wg._slot_target(1, 1) == 888
    assert wg._slot_target(1, 5) is None and wg._slot_target(2, 0) is None
    wg._scout_slots[1] = (wg.time.monotonic() - wg.SCOUT_TTL_SECONDS - 1, [777])
    assert wg._slot_target(1, 0) is None


def test_plain_strips_tags_for_alerts():
    from bots.main_bot.webapp_game import plain
    assert plain("❌ <b>Нет</b> &amp; всё") == "❌ Нет & всё"


def test_wide_screen_layout_is_a_grid_and_the_chart_is_capped():
    """Решение владельца 26.10: компьютер — до 3 колонок, планшет — 2, уже 720px — одна; график не на весь экран."""
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "@media (min-width: 720px)" in html and "@media (min-width: 1100px)" in html
    assert '#app[data-cols="3"]' in html and "box.dataset.cols" in html
    assert "align-items: stretch" in html                     # плашки одного ряда — одной высоты
    chart_css = next(line for line in html.splitlines() if line.strip().startswith(".chart {"))
    assert "max-width" in chart_css and "max-height" in chart_css


def test_long_lists_are_paged_and_the_shop_has_three_panels():
    """Лоты биржи, ТОП и рейтинг друзей листаются страницами; магазин — ферма | игровые | описания."""
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for pager_id in ('scopeKey + "asks-"', 'scopeKey + "bids-"', 'scopeKey + "swaps"', 'pager("top"', 'pager("reftop"'):
        assert pager_id in html
    assert "span-tablet" in html and 'pager("shopinfo"' in html



def test_team_text_filter_and_app_team_hub():
    """Команды в приложении — как в чате: рулетка, поиск, создание, выход; FAQ и соглашение — вкладки."""
    import pytest
    from shared.db_clans import TeamError, validate_team_text
    assert validate_team_text("  <Банда>  ", 32) == "&lt;Банда&gt;"
    for bad, key in (("", "team.err_len"), ("x" * 33, "team.err_len"), ("@spam", "team.err_link"),
                     ("+7 999 123 45 67", "team.err_link")):
        with pytest.raises(TeamError) as e:
            validate_team_text(bad, 32)
        assert e.value.key == key
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for needle in ('"/api/teams"', '"/api/team/join"', '"/api/team/leave"', '"/api/team/create"',
                   '"top", "info"]', 'viewDoc("/" + infoDoc)', 'TAB_ALIAS'):
        assert needle in html


def test_team_market_fees_and_help_ui():
    """Биржа команды дешевле общей (Мега-Клан ещё дешевле), Шаттл не суммируется; взаимопомощь есть в приложении."""
    from shared.economy import (CLAN_MARKET_FEE_PERCENT, MARKET_FEE_PERCENT, MEGA_CLAN_MAX_MEMBERS,
                                SHUTTLE_MARKET_FEE_PERCENT, TEAM_MARKET_FEE_PERCENT, market_fee,
                                team_market_fee_percent)
    assert CLAN_MARKET_FEE_PERCENT < TEAM_MARKET_FEE_PERCENT < MARKET_FEE_PERCENT
    assert team_market_fee_percent(50) == TEAM_MARKET_FEE_PERCENT
    assert team_market_fee_percent(MEGA_CLAN_MAX_MEMBERS) == CLAN_MARKET_FEE_PERCENT
    assert market_fee(1000) == 1000 * MARKET_FEE_PERCENT // 100
    assert market_fee(1000, team_percent=TEAM_MARKET_FEE_PERCENT) == 1000 * TEAM_MARKET_FEE_PERCENT // 100
    assert market_fee(1000, shuttle=True, team_percent=CLAN_MARKET_FEE_PERCENT) == \
        1000 * min(SHUTTLE_MARKET_FEE_PERCENT, CLAN_MARKET_FEE_PERCENT) // 100
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for needle in ('mkScope', 'data-scope', '/api/team/help', '/api/team/help/give', 'L.mk_yourStock',
                   'L.mk_yourCoins', 'L.hp_title', 'L.tm_market', 'pager("tmroster"'):
        assert needle in html, needle
    from shared.locales import t
    for lang in ("ru", "en", "de", "zh", "ar"):
        assert "{" not in t(lang, "help.err_limit", max=100)


def test_storage_tab_shield_timer_and_giver_threshold():
    """Склад после фермы (серые пустые плашки, «лава» у заполненных), щит с таймером, порог дарения 7/10."""
    from shared.economy import (ITEM_COLUMNS, ITEM_EFFECTS, TEAM_HELP_GIVER_MIN_BONUS_CLAIMS,
                                TEAM_HELP_GIVER_MIN_QUIZ_LEVEL, TRANSFER_SENDER_MIN_QUIZ_LEVEL)
    assert (TEAM_HELP_GIVER_MIN_QUIZ_LEVEL, TEAM_HELP_GIVER_MIN_BONUS_CLAIMS) == (7, 10)
    assert TEAM_HELP_GIVER_MIN_QUIZ_LEVEL > TRANSFER_SENDER_MIN_QUIZ_LEVEL
    assert set(ITEM_COLUMNS) <= set(ITEM_EFFECTS)
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert '"farm", "storage"' in html
    for needle in ("viewStorage", "/api/storage", "/api/item/use", "card.lava", "card.dim", "shield-card",
                   'id="shTimer"', "L.raid_noFuel", "fuel-pill", "L.hp_who", "res.stored ? L.it_stored"):
        assert needle in html, needle


def test_recipes_unlock_one_per_day_and_cover_every_recipe():
    """Поэтапное открытие: каждый рецепт мастерской в порядке, первый — сразу, по одному в сутки."""
    from datetime import timedelta
    from shared.economy import WORKSHOP_RECIPES, WORKSHOP_UNLOCK_HOURS, WORKSHOP_UNLOCK_ORDER, recipe_unlock_at, utcnow
    assert sorted(WORKSHOP_UNLOCK_ORDER) == sorted(WORKSHOP_RECIPES)
    assert WORKSHOP_UNLOCK_ORDER[0] == "nitro_6h" and WORKSHOP_UNLOCK_ORDER[-4] == "shuttle"   # дальше — боевые дроны
    start = utcnow()
    assert recipe_unlock_at("nitro_6h", start) == start
    assert recipe_unlock_at(WORKSHOP_UNLOCK_ORDER[3], start) == start + timedelta(hours=3 * WORKSHOP_UNLOCK_HOURS)
    from bots.main_bot.webapp_game import build_workshop_payload
    stock = {k: 5000 for k in ("metal", "hydrogen", "crystal", "parts")}
    p = build_workshop_payload(stock, 0, False, "ru", balance=5000, created_at=start, now=start + timedelta(hours=25),
                               disabled=("cargo",), week_done={"stamp": 1})
    by_id = {r["id"]: r for r in p["recipes"]}
    assert "cargo" not in by_id                                         # выключен владельцем
    assert not by_id["nitro_6h"]["locked"] and not by_id["bonfire"]["locked"] and by_id["shield_24h"]["locked"]
    assert by_id["shield_24h"]["locked"] and not by_id["shield_24h"]["affordable"]
    assert 0 < by_id["shield_24h"]["unlock_in"] <= 24 * 3600
    veteran = build_workshop_payload(stock, 0, False, "ru", balance=5000, created_at=start - timedelta(days=60),
                                     now=start, week_done={"stamp": 1})
    vet = {r["id"]: r for r in veteran["recipes"]}
    assert not any(r["locked"] for r in veteran["recipes"])
    assert vet["stamp"]["week_left"] == 0 and not vet["stamp"]["affordable"]   # недельный лимит
    assert vet["camo_12h"]["stored"] and not vet["armor"]["stored"]


def test_new_items_raid_formulas_and_mines_seed():
    """Трюм и Приманка в формулах налёта, сид рудников совпадает с MINES_COUNT, ресурсы по кругу."""
    from shared import economy
    assert economy.raid_loot(1000) == economy.RAID_LOOT_CAP
    assert economy.raid_loot(1000, economy.CARGO_LOOT_PERCENT) == economy.RAID_LOOT_CAP * 3 // 2
    assert economy.raid_loot(50, 150) == 50 * economy.RAID_LOOT_PERCENT * 150 // 10000
    assert economy.raid_fail_loss(1000, economy.TRAP_FAIL_MULTIPLIER) == economy.RAID_FAIL_CAP * 2
    assert economy.THERMOS_FUEL_CYCLE_SECONDS == 32 * 3600
    assert [economy.mine_kind(i) for i in (1, 2, 3, 4, 5)] == ["metal", "hydrogen", "crystal", "parts", "stone"]
    from shared.database import SCHEMA_STATEMENTS
    seed = next(x for x in SCHEMA_STATEMENTS if "INSERT INTO mines" in x)
    assert f"generate_series(1, {economy.MINES_COUNT})" in seed
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for needle in ("viewMines", "/api/mines", "L.mn_closed", "map-lock", "pumpRing", "goalsCard(g)", "viewInfo",
                   "L.ws_locked", "raid_note_", "forsageBtn"):
        assert needle in html, needle


def test_banner_window_and_thermos_cycle_in_farm_engine():
    """Знамя даёт бонус только внутри окна; Термос растягивает цикл котлеты до 32 ч."""
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.farm_logic import MinerState, integrate_rate_micros, simulate_farm
    t0 = utcnow()
    base = integrate_rate_micros(t0, t0 + timedelta(hours=10), "junior", None, None)
    win = integrate_rate_micros(t0, t0 + timedelta(hours=10), "junior", None, None,
                                windows=((t0 + timedelta(hours=5), t0 + timedelta(hours=20), 5),))
    assert win == base + base // 2 * 5 // 100
    driller = MinerState(1, "premium", t0, t0 + timedelta(days=30), None)
    plain = simulate_farm(last_update=t0, now=t0 + timedelta(hours=48), fridge_cutlets=10, acc=0, miners=[driller])
    thermos = simulate_farm(last_update=t0, now=t0 + timedelta(hours=48), fridge_cutlets=10, acc=0, miners=[driller],
                            thermos_from=t0, thermos_until=t0 + timedelta(hours=24))
    assert plain.cutlets_consumed == 2 and thermos.cutlets_consumed == 2
    assert thermos.miners[0].fuel_until == t0 + timedelta(hours=32 + 24)
