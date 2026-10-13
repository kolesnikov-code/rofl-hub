"""
Блок 4.2: локализация ru/en.

Главные гарантии:
- у КАЖДОГО ключа есть перевод в обоих языках (ничего не выпадает в ru у англичан);
- наборы {плейсхолдеров} совпадают между языками (иначе .format() упадёт в проде);
- у каждой reply-кнопки два языковых варианта и обработчики ловят оба;
- у каждого товара каталога есть английские title/button.
"""
import string

import pytest

from shared.locales import BUTTONS, EN, RU, btn, btn_variants, resolve_lang, t


def _placeholders(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


# ---------------------------------------------------------------- resolve_lang
@pytest.mark.parametrize("lang,expected", [
    ("ru", "ru"), ("en", "en"), ("zh", "en"), ("hi", "en"), ("es", "en"),
    ("de", "en"), ("uk", "en"), ("xx", "en"), (None, "ru"),
])
def test_resolve_lang(lang, expected):
    assert resolve_lang(lang) == expected


# ---------------------------------------------------------------- полнота словарей
def test_every_ru_key_has_en_translation():
    missing = set(RU) - set(EN)
    assert not missing, f"Нет английского перевода: {sorted(missing)}"


def test_no_orphan_en_keys():
    orphans = set(EN) - set(RU)
    assert not orphans, f"Английские ключи без русского эталона: {sorted(orphans)}"


def test_placeholders_match_between_languages():
    broken = []
    for key, ru_text in RU.items():
        if _placeholders(ru_text) != _placeholders(EN[key]):
            broken.append(key)
    assert not broken, f"Разные плейсхолдеры ru/en: {broken}"


def test_translations_are_not_empty_or_identical_dicts():
    assert len(RU) == len(EN) >= 100
    differing = sum(1 for k in RU if RU[k] != EN[k])
    assert differing > len(RU) * 0.9  # en — реальный перевод, а не копия ru


# ---------------------------------------------------------------- t()
def test_t_formats_kwargs():
    assert "5" in t("ru", "games.win", reward=5)
    assert "coins" in t("en", "games.win", reward=5)


def test_t_falls_back_to_russian_for_unknown_lang():
    assert t("zh", "games.btn_hub") == EN["games.btn_hub"]
    assert t(None, "games.btn_hub") == RU["games.btn_hub"]


def test_t_raises_on_unknown_key():
    with pytest.raises(KeyError):
        t("ru", "no.such.key")


# ---------------------------------------------------------------- кнопки
def test_every_button_has_both_languages():
    for key, variants in BUTTONS.items():
        assert set(variants) == {"ru", "en"}, key
        assert variants["ru"] != variants["en"], key


def test_btn_variants_cover_both_languages():
    assert btn_variants("farm") == {"🚜 МОЯ ФЕРМА", "🚜 MY FARM"}
    assert btn("en", "shop") == "🏪 SHOP"
    assert btn("ru", "shop") == "🏪 МАГАЗИН"


# ---------------------------------------------------------------- каталог
def test_every_catalog_item_has_english_title_and_button():
    from bots.main_bot.catalog import CATALOG, item_button, item_title
    for sku, item in CATALOG.items():
        assert item.get("title_en"), f"{sku}: нет title_en"
        assert item.get("button_en"), f"{sku}: нет button_en"
        assert item_title(item, "en") == item["title_en"]
        assert item_title(item, "ru") == item["title"]
        assert item_button(item, "en") == item["button_en"]
        # цена в звёздах должна совпадать в обеих версиях кнопки
        assert str(item["stars"]) in item["button_en"], sku


def test_reply_keyboards_built_per_language():
    pytest.importorskip("aiogram")
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    from bots.main_bot.handlers.menu import get_reply_main_keyboard

    ru_texts = [b.text for row in get_reply_main_keyboard("ru").keyboard for b in row]
    en_texts = [b.text for row in get_reply_main_keyboard("en").keyboard for b in row]
    assert "🚜 МОЯ ФЕРМА" in ru_texts and "🚜 MY FARM" in en_texts
    assert len(ru_texts) == len(en_texts) == 6
