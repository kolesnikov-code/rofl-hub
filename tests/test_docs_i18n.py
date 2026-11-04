"""
Справочник (/faq) и «Как играть» (/guide) на 14 языках: сервер отдаёт перевод по ?lang=, а каждый перевод
повторяет разметку русского оригинала (те же разделы с теми же id — на них ведут ссылки ?s=), без русского текста.
"""
import re
from collections import Counter
from pathlib import Path

import pytest
from aiohttp.test_utils import make_mocked_request

from bots.main_bot import webapp
from shared.locales import PACK_CODES

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "static" / "webapp"
DOCS = ("faq", "guide")
LANGS = ("en",) + tuple(PACK_CODES)
TAG = re.compile(r"<(/?[a-zA-Z0-9]+)")
ID = re.compile(r'\bid="([^"]+)"')


def _body(base, lang):
    resp = webapp._doc_page(base, make_mocked_request("GET", f"/{base}?lang={lang}" if lang is not None else f"/{base}"))
    return resp.body.decode("utf-8")


@pytest.mark.parametrize("base", DOCS)
def test_doc_page_serves_the_player_language(base):
    ru = (WEB / f"{base}.html").read_text(encoding="utf-8")
    assert _body(base, None) == ru
    assert _body(base, "ru") == ru
    for lang in LANGS:
        assert _body(base, lang) == (WEB / "docs" / f"{base}.{lang}.html").read_text(encoding="utf-8"), lang
    # Неизвестный язык — английский, мусор в параметре — оригинал (путь из запроса не собирается)
    assert _body(base, "xx") == (WEB / "docs" / f"{base}.en.html").read_text(encoding="utf-8")
    assert _body(base, "../faq") == ru


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("base", DOCS)
def test_translated_doc_keeps_the_original_layout(base, lang):
    src = (WEB / f"{base}.html").read_text(encoding="utf-8")
    dst = (WEB / "docs" / f"{base}.{lang}.html").read_text(encoding="utf-8")
    assert Counter(TAG.findall(dst)) == Counter(TAG.findall(src))
    assert ID.findall(dst) == ID.findall(src)
    assert dst.split("<script>")[-1] == src.split("<script>")[-1]
    assert f'<html lang="{lang}"' in dst
    for handle in ("@BotBaronsBot", "@mister_telebot", "https://t.me/mister_telebot"):
        assert src.count(handle) == dst.count(handle), handle   # имена ботов и ссылки — не переводятся
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", dst, flags=re.S)
    assert not re.search(r"[А-Яа-яЁё]", text), "в переводе остался русский текст"
    assert "rofl" not in re.sub(r"BOT BARONS|ROFL-HUB|rofl-hub|RoflHub|\bROFL\b", "", text).lower()


def test_app_and_chat_open_docs_in_the_player_language():
    app = (WEB / "index.html").read_text(encoding="utf-8")
    assert '"?lang=" + encodeURIComponent(me.lang' in app
    assert "/faq?lang={user_lang}" in (ROOT / "bots" / "main_bot" / "handlers" / "faq.py").read_text(encoding="utf-8")
    assert "&lang={lang}" in (ROOT / "bots" / "main_bot" / "handlers" / "shop.py").read_text(encoding="utf-8")
