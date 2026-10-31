"""
Волна 27.10 по итогам оценки 9 агентов: Дело дня, вызов друга на дуэль по ссылке, отряды, карточка достижений,
режим приложения и постепенное открытие разделов, перевод монет в приложении. Чистые проверки без БД.
"""
import re
from datetime import date, timedelta
from pathlib import Path

from shared import daily_case
from shared.duels import new_invite_code, valid_invite_code
from shared.economy import (DAILY_CASE_REWARD, SQUAD_CREATE_COST, SQUAD_MAX_MEMBERS,
                            SQUAD_UPGRADE_COST, TEAM_CREATE_COST, TEAM_MAX_MEMBERS)

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------- 🕵️ дело дня
def test_daily_cases_are_well_formed():
    cases = daily_case.load_cases()
    assert len(cases) >= 14
    assert len({c["id"] for c in cases}) == len(cases)
    for c in cases:
        assert daily_case.validate_case(c) == [], c["id"]
        for lang in daily_case.CONTENT_LANGS:
            body = c[lang]
            # виновный назван в разгадке, а не «кто-то»
            first = body["suspects"][c["culprit"]]["name"].split()[-1]
            assert first[:4] in body["solution"], (c["id"], lang, first)
            assert all(len(x) <= 220 for x in body["clues"]), c["id"]
            assert len(body["story"]) <= 400, c["id"]


def test_daily_case_ru_and_en_tell_the_same_story():
    for c in daily_case.load_cases():
        ru, en = c["ru"], c["en"]
        assert [s["emoji"] for s in ru["suspects"]] == [s["emoji"] for s in en["suspects"]], c["id"]
        # одинаковые числа (время, размеры, суммы) в уликах обеих версий
        for a, b in zip(ru["clues"], en["clues"]):
            assert sorted(re.findall(r"\d+", a)) == sorted(re.findall(r"\d+", b)), (c["id"], a)


def test_daily_case_rotation_by_day():
    cases = daily_case.all_cases()
    d0 = daily_case.CASE_EPOCH
    assert daily_case.case_number(d0) == 1
    assert daily_case.case_for_day(d0)["id"] == cases[0]["id"]
    assert daily_case.case_for_day(d0 + timedelta(days=1))["id"] == cases[1]["id"]
    assert daily_case.case_for_day(d0 + timedelta(days=len(cases)))["id"] == cases[0]["id"]   # по кругу
    assert daily_case.case_for_day(date(2026, 10, 27)) is not None                              # и до эпохи


def test_daily_case_reward_drops_with_every_clue():
    rewards = [DAILY_CASE_REWARD[i] for i in range(1, daily_case.CLUES + 1)]
    assert rewards == sorted(rewards, reverse=True) and len(set(rewards)) == len(rewards)
    assert daily_case.text_lang("de") == "en" and daily_case.text_lang("ru") == "ru"


def test_broken_cases_file_does_not_crash(tmp_path):
    bad = tmp_path / "cases.json"
    bad.write_text("{oops", encoding="utf-8")
    assert daily_case.load_cases(bad) == []
    assert daily_case.case_for_day(date(2026, 11, 1)) is None
    daily_case.load_cases()   # вернуть настоящие дела для остальных тестов


# ---------------------------------------------------------------- ⚔️ вызов друга
def test_invite_codes_are_valid_and_unambiguous():
    codes = {new_invite_code() for _ in range(200)}
    assert len(codes) == 200
    for c in codes:
        assert valid_invite_code(c) and not set(c) & set("0o1li")   # без путаницы 0/o, 1/l/i
    for bad in ("", "ab", "UPPER123", "duel_x", "a" * 40, "abc$def1"):
        assert not valid_invite_code(bad)


def test_start_param_duel_code():
    import pytest
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.start import _duel_code_from
    code = new_invite_code()
    assert _duel_code_from("duel_" + code) == code
    assert _duel_code_from("duel_" + code.upper()) == code
    assert _duel_code_from("auc_5") is None and _duel_code_from(None) is None and _duel_code_from("duel_!!") is None


# ---------------------------------------------------------------- 🛡 отряды
def test_squad_prices():
    assert 5_000 <= SQUAD_CREATE_COST <= 10_000                       # вилка владельца
    assert SQUAD_CREATE_COST + SQUAD_UPGRADE_COST == TEAM_CREATE_COST  # отряд → команда не дешевле и не дороже
    assert SQUAD_MAX_MEMBERS < TEAM_MAX_MEMBERS


# ---------------------------------------------------------------- 📸 карточка
def test_card_upload_accepts_png_and_jpeg_only():
    import pytest
    pytest.importorskip("aiogram")
    from bots.main_bot.webapp_social import card_type
    assert card_type(b"\x89PNG\r\n\x1a\n...") == ("image/png", "png")
    assert card_type(b"\xff\xd8\xff\xe0...") == ("image/jpeg", "jpg")
    assert card_type(b"GIF89a") is None and card_type(b"<svg") is None


def test_social_routes_registered():
    import pytest
    pytest.importorskip("aiogram")
    from bots.main_bot.webapp import create_webapp
    paths = {r.resource.canonical for r in create_webapp("123456:TEST").router.routes() if r.resource}
    for p in ("/api/mode", "/api/transfer", "/api/transfer/preview", "/api/duel/invite", "/api/duel/accept",
              "/api/duel/decline", "/api/case", "/api/case/clue", "/api/case/accuse", "/api/card", "/api/card/upload",
              "/api/team/upgrade"):
        assert p in paths, p


# ---------------------------------------------------------------- 🧭 приложение
def test_all_tabs_open_in_full_mode_and_puzzle_mode_hides_economy():
    """Владелец 27.10, вечер: во «🌐 Всей экосистеме» вкладки открыты сразу, поэтапно — только рецепты и технологии."""
    assert "TAB_DAY" not in HTML and 'me.app_mode === "puzzle" && !PUZZLE_TABS.includes(t)' in HTML
    puzzle = re.findall(r'"(\w+)"', re.search(r"const PUZZLE_TABS = \[([^\]]*)\]", HTML).group(1))
    assert "games" in puzzle and "farm" not in puzzle and "market" not in puzzle and "raids" not in puzzle


def test_new_app_texts_are_in_ru_and_en():
    used = set(re.findall(r"\bL\.((?:md|lk|di|ac|tf|sq|cs)_\w+)", HTML))
    assert len(used) > 60
    for key in used:
        assert len(re.findall(r"[\s,{]" + key + r':\s*"', HTML)) >= 2, key   # ru и en (паки — test_app_wave)


def test_generated_i18n_packs_are_valid_json_and_up_to_date():
    """12 переводов — отдельные файлы static/webapp/i18n/<код>.json (31.10: index.html без них в 2,7 раза легче).
    «\n» в переводах (cs_shareText) раньше превращался генератором в настоящий перевод строки — и приложение не грузилось.
    Файлы совпадают с паками: забыли `python -m scripts.gen_miniapp_i18n` после правки MINIAPP — тест красный."""
    import json
    from shared.locales import MINIAPP_PACKS
    folder = ROOT / "static" / "webapp" / "i18n"
    codes = sorted(c for c, p in MINIAPP_PACKS.items() if p)
    assert len(codes) == 12 and f"const I18N_PACKS = {json.dumps(codes)};" in HTML and "const I18N_VER = " in HTML
    for code in codes:
        assert json.loads((folder / f"{code}.json").read_text(encoding="utf-8")) == MINIAPP_PACKS[code], code
    assert "\n" in json.loads((folder / "de.json").read_text(encoding="utf-8"))["cs_shareText"]
    assert "const I18N_EXTRA = " not in HTML and len(HTML.encode()) < 700_000


def test_pages_are_gzipped_once_and_revalidated_with_etag():
    """Страница жмётся один раз и отдаётся 304 при повторном открытии; перевод — только существующий язык."""
    import gzip
    from types import SimpleNamespace
    from bots.main_bot import webapp
    req = SimpleNamespace(headers={"Accept-Encoding": "gzip, br"}, query={})
    first = webapp._page("index.html", req)
    assert first.headers["Content-Encoding"] == "gzip" and gzip.decompress(first.body) == (ROOT / "static/webapp/index.html").read_bytes()
    again = webapp._page("index.html", SimpleNamespace(headers={"If-None-Match": first.headers["ETag"]}, query={}))
    assert again.status == 304 and not again.body
    plain = webapp._cached_file(SimpleNamespace(headers={}, query={}), "i18n/de.json", "application/json")
    assert "Content-Encoding" not in plain.headers and json_ok(plain.body)


def json_ok(raw: bytes) -> bool:
    import json
    return bool(json.loads(raw))


def test_hindi_shows_a_goat_instead_of_a_cow():
    """Владелец 28.10: в хинди корова священна — ресурс «корова» показывается козой; механика та же."""
    from shared.locales import localize_icons, t
    from shared.resources import format_bundle
    assert localize_icons("hi", "🐄 1 + 🔥 2 → 🥩 3") == "🐐 1 + 🔥 2 → 🥩 3"
    assert localize_icons("bn", "🐄") == "🐄" and localize_icons("ru", "🐄") == "🐄"
    assert "🐄" not in t("hi", "games.resource_gain", icon="🐄", qty=1, name="x", total=5) and "🐐" in t("hi", "games.resource_gain", icon="🐄", qty=1, name="x", total=5)
    assert "गाय" not in format_bundle("hi", {"cow": 1})
    assert 'const ICON_SWAPS = { hi: [["🐄", "🐐"]] };' in HTML and "const raw = swapIcons(await res.text()" in HTML


def test_tabs_render_from_memory_and_revalidate():
    """⚡ 31.10: повторный вход во вкладку — из памяти, свежее фоном; POST стирает память; игры — всегда живые."""
    assert "const GET_CACHE = new Map()" in HTML and 'const NO_CACHE_TABS = ["games"]' in HTML
    assert "if (!isGet) { GET_CACHE.clear(); cacheGen++; }" in HTML and "gen === cacheGen" in HTML
    assert "prefetchMain()" in HTML and "b.onpointerdown = () => { prefetchTab(b.dataset.tab); };" in HTML
    assert "revalidate(tab, nav, Array.from(vc.used))" in HTML and "go(tab, { quiet: true })" in HTML
    assert "loadPack(guess);" in HTML and "await loadPack(me.lang);" in HTML


def test_every_suit_has_its_own_drawing_and_level_tiers():
    """Владелец 31.10: у каждого из 6 костюмов свой рисунок всех 5 деталей, и он богатеет с уровнем 1 → 3."""
    for s in ("el", "mn", "ml", "st", "sc", "en"):
        assert f"\n                        {s}: {{" in HTML or f"const SUIT_DECO = {{ {s}:" in HTML, s
    for name in ("mnHead", "mlBody", "stHead", "enBody", "mlFeet", "stLegs", "enHands"):
        assert f"const {name} = () =>" in HTML, name
    assert "const TIER = {" in HTML and 'id="psCamo"' in HTML and "t(lv(slot))" in HTML


def test_gender_switch_is_instant_without_reloading_the_tab():
    """31.10: М/Ж меняет аватар на месте, сохранение — фоном (откат при ошибке); вкладка не перерисовывается."""
    assert 'post("/api/gear/gender", { gender: g })' in HTML and 'ava.outerHTML = avatarSvg(to' in HTML
    assert 'act(b, "/api/gear/gender"' not in HTML


def test_app_has_no_control_characters():
    """31.10: в регулярку попал невидимый \x08 вместо \b — замена id молча не работала. Управляющих символов в коде нет."""
    import re
    bad = [(i, hex(ord(c))) for i, c in enumerate(HTML) if ord(c) < 32 and c not in "\n\r\t"]
    assert not bad, bad[:5]
    assert "Holo)" + chr(92) + "b/g" in HTML
