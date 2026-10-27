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


def test_generated_i18n_block_is_valid_json():
    """«\n» в переводах (cs_shareText) раньше превращался генератором в настоящий перевод строки — и приложение не грузилось."""
    import json
    start = HTML.index("const I18N_EXTRA = ") + len("const I18N_EXTRA = ")
    end = HTML.index("// I18N_EXTRA_END")
    packs = json.loads(HTML[start:end].rstrip().rstrip(";"))
    assert len(packs) == 12 and "\n" in packs["de"]["cs_shareText"]
