"""🌐 02.11: сменить язык можно в любой момент — кнопкой нижней панели или /language (выбрали не тот, дети пошутили)."""
import asyncio
import os
from pathlib import Path

import pytest

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from bots.main_bot import config, webapp_links
from bots.main_bot.handlers import menu, start
from shared.locales import SUPPORTED_LANGS, btn, btn_variants, t


@pytest.fixture
def with_app(monkeypatch):
    monkeypatch.setattr(config, "WEBAPP_URL", "https://app.example")
    monkeypatch.setattr(webapp_links, "WEBAPP_URL", "https://app.example")


def test_language_button_is_recognizable_in_every_language():
    labels = {lang: btn(lang, "language") for lang in SUPPORTED_LANGS}
    assert all(lbl.startswith("🌐") and "LANGUAGE" in lbl for lbl in labels.values())
    assert set(labels.values()) == btn_variants("language")
    for lang in SUPPORTED_LANGS:
        assert "/language" in t(lang, "lang.kb_hint"), lang
        assert t(lang, "lang.changed") != t("en", "lang.changed") or lang == "en", lang


def test_with_the_app_bottom_panel_is_only_the_language_button(with_app):
    for lang in SUPPORTED_LANGS:
        kb = menu.get_reply_keyboard(lang)
        assert [[b.text for b in row] for row in kb.keyboard] == [[btn(lang, "language")]], lang


def test_without_the_app_language_button_ends_the_old_grid(monkeypatch):
    monkeypatch.setattr(config, "WEBAPP_URL", None)
    kb = menu.get_reply_keyboard("ru")
    assert kb.keyboard[-1][0].text == btn("ru", "language") and len(kb.keyboard) == 4


def test_change_grid_offers_all_14_languages_in_owner_order():
    rows = start.get_language_change_keyboard().inline_keyboard
    codes = [b.callback_data.split(":")[1] for row in rows for b in row]
    assert codes == [c for c, _ in start.LANGUAGES] and all(len(r) == 2 for r in rows)


def test_language_command_is_in_the_blue_menu_of_every_language(with_app, monkeypatch):
    from bots.main_bot import bot as main_bot
    monkeypatch.setattr(main_bot, "WEBAPP_URL", "https://app.example")
    assert "language" in main_bot.menu_commands()


class _Conn:
    def __init__(self, rows):
        self.rows, self.calls = rows, []

    async def execute(self, sql, *args):
        self.calls.append(args)
        return f"UPDATE {self.rows}"


class _Pool:
    def __init__(self, conn):
        self.conn = conn

    def acquire(self):
        conn = self.conn

        class _Ctx:
            async def __aenter__(self):
                return conn

            async def __aexit__(self, *a):
                return False
        return _Ctx()


class _Msg:
    def __init__(self):
        self.sent, self.edited = [], []

    async def answer(self, text, **kw):
        self.sent.append((text, kw.get("reply_markup")))

    async def edit_text(self, text, **kw):
        self.edited.append(text)


class _Cb:
    def __init__(self, data):
        self.data, self.message, self.alerts = data, _Msg(), []
        self.from_user = type("U", (), {"id": 42})()

    async def answer(self, text=None, show_alert=False):
        self.alerts.append(text)


def _run_change(monkeypatch, data, rows=1):
    conn = _Conn(rows)
    monkeypatch.setattr(start.db, "_pool", _Pool(conn))
    cb = _Cb(data)
    asyncio.run(start.process_language_change(cb))
    return cb, conn


def test_change_saves_language_and_answers_in_the_new_one(with_app, monkeypatch):
    cb, conn = _run_change(monkeypatch, "chg_lang:de")
    assert conn.calls == [(42, "de")]
    text, kb = cb.message.sent[0]
    assert text == t("de", "lang.changed")
    assert kb.keyboard[-1][0].text == btn("de", "language")


def test_change_ignores_unknown_codes_and_unregistered_players(with_app, monkeypatch):
    cb, conn = _run_change(monkeypatch, "chg_lang:xx")
    assert conn.calls == [] and cb.message.sent == []
    cb, conn = _run_change(monkeypatch, "chg_lang:fr", rows=0)
    assert cb.message.sent == [] and cb.alerts == ["/start"]


class _Sent:
    def __init__(self, log):
        self.log, self.chat = log, type("C", (), {"id": 42})()
        log_ = log

        class _Bot:
            async def unpin_all_chat_messages(self, chat_id):
                log_.append(("unpin_all", chat_id))
        self.bot = _Bot()

    async def pin(self, disable_notification=False):
        self.log.append(("pin", disable_notification))


class _PinMsg:
    def __init__(self):
        self.sent, self.log = [], []

    async def answer(self, text, **kw):
        self.sent.append((text, kw.get("reply_markup")))
        return _Sent(self.log)


def test_open_app_is_not_in_the_bottom_panel_but_pinned_in_the_chat(with_app):
    """04.11: reply-кнопка приложения — лишнее нажатие; вместо неё закреплённое «Открыть приложение» с web_app-кнопкой."""
    for lang in SUPPORTED_LANGS:
        texts = [b.text for row in menu.get_reply_keyboard(lang).keyboard for b in row]
        assert btn(lang, "open_app") not in texts, lang
    msg = _PinMsg()
    asyncio.run(start.send_pinned_app(msg, "de"))
    text, kb = msg.sent[0]
    assert text == t("de", "app.btn") and kb.inline_keyboard[0][0].web_app is not None
    assert msg.log == [("unpin_all", 42), ("pin", True)]     # наверху один закреп, без звука


def test_pin_failure_does_not_break_the_message(with_app):
    msg = _PinMsg()

    async def boom(*a, **kw):
        raise RuntimeError("no rights")
    sent_cls = _Sent
    orig = sent_cls.pin
    sent_cls.pin = boom
    try:
        asyncio.run(start.send_pinned_app(msg, "ru"))
    finally:
        sent_cls.pin = orig
    assert len(msg.sent) == 1


def test_onboarding_end_start_and_language_change_send_the_pinned_app():
    src = Path(start.__file__).read_text(encoding="utf-8")
    for fn in ("async def cmd_start(", "async def cmd_start_step_4(", "async def process_language_change("):
        body = src[src.index(fn):]
        end = body.find("@router", 1)
        body = body if end < 0 else body[:end]
        assert "send_pinned_app(" in body, fn
