"""
Локализация: 14 языков (решение владельца 13.10.2026).

Главные гарантии:
- каждый язык содержит ВСЕ ключи RU-эталона, лишних нет;
- наборы {плейсхолдеров} совпадают с эталоном (иначе .format() упадёт в проде);
- у каждой reply-кнопки есть вариант на всех языках, обработчики ловят все;
- у каждого пака полные MINIAPP и COMMANDS;
- выбор языка при /start — все 14, раскладка владельца.
"""
import string

import pytest

from shared.locales import (
    BUTTONS,
    COMMAND_PACKS,
    EN,
    MINIAPP_PACKS,
    PACK_CODES,
    RU,
    STRINGS,
    SUPPORTED_LANGS,
    btn,
    btn_variants,
    resolve_lang,
    t,
)

ALL_LANGS = ("ru", "en") + tuple(PACK_CODES)


def _placeholders(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


# ---------------------------------------------------------------- подключение паков
def test_all_14_languages_loaded():
    assert set(SUPPORTED_LANGS) == set(ALL_LANGS)
    assert len(SUPPORTED_LANGS) == 14


# ---------------------------------------------------------------- resolve_lang
@pytest.mark.parametrize("lang", ALL_LANGS)
def test_resolve_supported_lang_returns_itself(lang):
    assert resolve_lang(lang) == lang


def test_resolve_unknown_and_none():
    assert resolve_lang(None) == "ru"      # аудитория СНГ по умолчанию
    assert resolve_lang("xx") == "en"      # незнакомый код → английский
    assert resolve_lang("uk") == "en"


# ---------------------------------------------------------------- полнота словарей
@pytest.mark.parametrize("lang", ALL_LANGS)
def test_language_has_every_ru_key_and_no_orphans(lang):
    missing = set(RU) - set(STRINGS[lang])
    orphans = set(STRINGS[lang]) - set(RU)
    assert not missing, f"{lang}: нет перевода ключей {sorted(missing)[:8]}"
    assert not orphans, f"{lang}: лишние ключи {sorted(orphans)[:8]}"


@pytest.mark.parametrize("lang", ALL_LANGS)
def test_placeholders_match_reference(lang):
    broken = [k for k in RU if _placeholders(RU[k]) != _placeholders(STRINGS[lang][k])]
    assert not broken, f"{lang}: разные плейсхолдеры с эталоном: {broken[:8]}"


@pytest.mark.parametrize("lang", [l for l in ALL_LANGS if l != "ru"])
def test_translation_is_not_a_copy_of_russian(lang):
    differing = sum(1 for k in RU if RU[k] != STRINGS[lang][k])
    assert differing > len(RU) * 0.9, f"{lang}: похоже на копию русского"


def test_dictionaries_are_substantial():
    assert len(RU) == len(EN) >= 100


# ---------------------------------------------------------------- t()
def test_t_formats_kwargs_in_every_language():
    for lang in ALL_LANGS:
        text = t(lang, "games.win", reward=5)
        assert "5" in text, lang


def test_t_falls_back_to_english_for_unknown_lang():
    assert t("xx", "games.btn_hub") == EN["games.btn_hub"]
    assert t(None, "games.btn_hub") == RU["games.btn_hub"]


def test_t_raises_on_unknown_key():
    with pytest.raises(KeyError):
        t("ru", "no.such.key")


# ---------------------------------------------------------------- кнопки
def test_every_button_has_all_languages():
    for key, variants in BUTTONS.items():
        missing = set(ALL_LANGS) - set(variants)
        assert not missing, f"кнопка {key}: нет языков {sorted(missing)}"
        assert all(v.strip() for v in variants.values()), key


def test_btn_variants_cover_all_languages():
    assert "🚜 МОЯ ФЕРМА" in btn_variants("farm")
    assert "🚜 MY FARM" in btn_variants("farm")
    assert len(btn_variants("farm")) >= 10  # 14 языков минус возможные совпадения
    assert btn("ru", "shop") == "🏪 МАГАЗИН"


# ---------------------------------------------------------------- Mini App и команды
def test_every_pack_has_full_miniapp_dictionary():
    key_sets = {code: set(MINIAPP_PACKS[code]) for code in PACK_CODES}
    reference = key_sets[PACK_CODES[0]]
    assert len(reference) >= 35
    for code, keys in key_sets.items():
        assert keys == reference, f"{code}: MINIAPP ключи отличаются: {keys ^ reference}"
        assert all(str(v).strip() for v in MINIAPP_PACKS[code].values()), code


def test_every_pack_has_full_command_descriptions():
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    pytest.importorskip("aiogram")
    from bots.main_bot.bot import BOT_COMMANDS
    for code in PACK_CODES:
        pack = COMMAND_PACKS[code]
        missing = set(BOT_COMMANDS) - set(pack)
        assert not missing, f"{code}: нет описаний команд {sorted(missing)}"
        for cmd in BOT_COMMANDS:
            assert 1 <= len(str(pack[cmd])) <= 256, f"{code}/{cmd}"


# ---------------------------------------------------------------- выбор языка и клавиатуры
def test_start_language_grid_is_owner_layout():
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.start import LANGUAGES

    codes = [code for code, _ in LANGUAGES]
    assert len(codes) == 14 and len(set(codes)) == 14
    assert set(codes) == set(ALL_LANGS)
    # Раскладка владельца: первые три ряда (по 2 кнопки)
    assert codes[:6] == ["en", "es", "uz", "fr", "ru", "pt"]


def test_reply_keyboards_built_per_language():
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.menu import get_reply_main_keyboard

    for lang in ALL_LANGS:
        texts = [b.text for row in get_reply_main_keyboard(lang).keyboard for b in row]
        assert len(texts) == 6 and all(t.strip() for t in texts), lang
    assert "🚜 MY FARM" in [b.text for row in get_reply_main_keyboard("en").keyboard for b in row]


# ---------------------------------------------------------------- каталог (ru/en)
def test_every_catalog_item_has_english_title_and_button():
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    pytest.importorskip("aiogram")
    from bots.main_bot.catalog import CATALOG, item_button, item_title
    for sku, item in CATALOG.items():
        assert item.get("title_en") and item.get("button_en"), sku
        assert item_title(item, "en") == item["title_en"]
        assert item_title(item, "ru") == item["title"]
        assert item_button(item, "de") == item["button_en"]  # не-ru языки видят en-витрину
        assert str(item["stars"]) in item["button_en"], sku
