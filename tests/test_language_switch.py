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


def test_change_grid_offers_only_owner_languages_plus_the_current_one():
    """13.11 (владелец): на выбор — английский, узбекский, русский; остальные языки — только автоматически."""
    codes = lambda kb: [b.callback_data.split(":")[1] for row in kb.inline_keyboard for b in row]
    assert start.OFFERED_LANGS == ("en", "uz", "ru")
    assert codes(start.get_language_change_keyboard("ru")) == ["en", "uz", "ru"]
    kb = start.get_language_change_keyboard("pt")            # язык подобран по Telegram — вернуться к нему можно
    assert codes(kb) == ["en", "uz", "ru", "pt"] and all(len(r) <= 2 for r in kb.inline_keyboard)
    assert kb.inline_keyboard[-1][-1].text.startswith("✅")


def test_language_comes_from_telegram_with_sane_fallbacks():
    f = start.lang_from_telegram
    assert f("ru") == "ru" and f("pt-br") == "pt" and f("zh-hans") == "zh" and f("UZ") == "uz"
    assert f("uk") == "ru" and f("kk") == "ru" and f("be") == "ru"   # почти всегда читают по-русски
    assert f("tr") == "en" and f(None) == "en" and f("") == "en"


def test_first_screen_has_continue_and_one_short_language_row():
    kb = start.intro1_keyboard("uz", "none").inline_keyboard
    assert kb[0][0].callback_data == "intro_step_2:none" and kb[0][0].text == t("uz", "start.btn_continue")
    assert [b.text for b in kb[1]] == ["🇺🇸 EN", "✅ 🇺🇿 UZ", "🇷🇺 RU"]
    assert all(len(b.callback_data.encode()) <= 64 for b in kb[1])
    assert [b.text for b in start.intro1_keyboard("hi", "duel_abcd1234").inline_keyboard[1]][-1] == "✅ 🇮🇳 HI"


def test_new_player_is_registered_on_start_without_the_language_grid(monkeypatch):
    calls = {}

    async def fake_register(target, user_id, username, full_name, lang, referrer_id, auc_part, source, edit=False):
        calls.update(user=user_id, lang=lang, auc=auc_part, edit=edit)

    class _NoUserConn:
        async def fetchrow(self, *a):
            return None
    monkeypatch.setattr(start.db, "_pool", _Pool(_NoUserConn()))
    monkeypatch.setattr(start, "register_and_greet", fake_register)
    msg = _Msg()
    msg.text = "/start"
    msg.from_user = type("U", (), {"id": 7, "username": "neo", "full_name": "Neo", "language_code": "pt-br"})()

    class _State:
        async def clear(self):
            pass
    asyncio.run(start.cmd_start(msg, _State()))
    assert calls == {"user": 7, "lang": "pt", "auc": "none", "edit": False} and msg.sent == []


def test_language_command_is_in_the_blue_menu_of_every_language(with_app, monkeypatch):
    from bots.main_bot import bot as main_bot
    monkeypatch.setattr(main_bot, "WEBAPP_URL", "https://app.example")
    assert "language" in main_bot.menu_commands()


class _Conn:
    """rows=0 — игрок не найден; fresh — зарегистрирован меньше суток назад."""
    def __init__(self, rows, fresh=False):
        self.rows, self.fresh, self.calls = rows, fresh, []

    async def execute(self, sql, *args):
        self.calls.append(args)
        return f"UPDATE {self.rows}"

    async def fetchval(self, sql, *args):
        self.calls.append(args[:2])
        return self.fresh if self.rows else None


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


def _run_change(monkeypatch, data, rows=1, fresh=False):
    conn = _Conn(rows, fresh)
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


# ---------------------------------------------------------------- 14.11: одно приветствие вместо 4 шагов
def test_welcome_is_approved_text_with_gift_and_play_button_in_every_language():
    from shared.economy import START_BALANCE
    for lang in SUPPORTED_LANGS:
        text = t(lang, "start.welcome", coins=START_BALANCE)
        assert "Cyber Barons" in text and f"{START_BALANCE} 🪙" in text, lang
        assert text.count("<b>") == text.count("</b>") >= 6, lang          # разметка как в утверждённом ru
        assert [ln[:1] for ln in text.split("\n") if ln][:3] == ["👋", "🎮", "🛠"], lang
        assert t(lang, "start.btn_play").startswith("🎮"), lang
        assert "/" not in t(lang, "start.btn_play"), lang                   # без слэш-команд на кнопке
    assert "викторине, дуэлях и квестах" in t("ru", "start.welcome", coins=500)


class _WMsg:
    def __init__(self):
        self.sent, self.deleted, self.pinned = [], [], []
        self.chat = type("C", (), {"id": 42})()
        outer = self

        class _Bot:
            async def unpin_all_chat_messages(self, chat_id):
                outer.pinned.append("unpin")
        self.bot = _Bot()

    async def answer(self, text, **kw):
        outer = self

        class _Sent:
            chat, bot = outer.chat, outer.bot

            async def delete(self):
                outer.deleted.append(text)

            async def pin(self, disable_notification=False):
                outer.pinned.append(text)
        self.sent.append((text, kw.get("reply_markup")))
        return _Sent()


def test_welcome_flow_is_one_visible_message_with_play_and_language_panel(with_app):
    msg = _WMsg()

    async def go():
        await start.set_lang_panel(msg, "ru")
        await start.send_welcome(msg, "ru")
    asyncio.run(go())
    (hint, panel), (welcome, kb) = msg.sent
    assert msg.deleted == [hint]                                            # служебное сообщение убрано
    assert panel.keyboard[-1][0].text == btn("ru", "language")              # а кнопка языка осталась
    assert welcome == t("ru", "start.welcome", coins=500) and msg.pinned == ["unpin", welcome]
    assert kb.inline_keyboard[0][0].text == t("ru", "start.btn_play") and kb.inline_keyboard[0][0].web_app


def test_new_player_changing_language_gets_the_welcome_again(with_app, monkeypatch):
    sent = []

    async def fake_panel(target, lang):
        sent.append(("panel", lang))

    async def fake_welcome(target, lang):
        sent.append(("welcome", lang))
    monkeypatch.setattr(start, "set_lang_panel", fake_panel)
    monkeypatch.setattr(start, "send_welcome", fake_welcome)
    cb, _ = _run_change(monkeypatch, "chg_lang:uz", fresh=True)
    assert sent == [("panel", "uz"), ("welcome", "uz")] and cb.message.sent == []
