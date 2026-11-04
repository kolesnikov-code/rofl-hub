"""📱 27.10: «чат — дверь и почтальон» — команды разделов ведут в приложение, в синем меню только чатовое."""
import asyncio

import pytest

from bots.main_bot import bot as main_bot
from bots.main_bot import config, webapp_links
from bots.main_bot.handlers import app_first
from shared.locales import SUPPORTED_LANGS, t


class _Msg:
    def __init__(self, text):
        self.text, self.sent = text, []

    async def answer(self, text, **kw):
        self.sent.append((text, kw.get("reply_markup")))


@pytest.fixture
def with_app(monkeypatch):
    monkeypatch.setattr(config, "WEBAPP_URL", "https://app.example")
    monkeypatch.setattr(webapp_links, "WEBAPP_URL", "https://app.example")
    monkeypatch.setattr(main_bot, "WEBAPP_URL", "https://app.example")


def test_every_section_command_points_to_a_real_tab():
    for cmd, tab in app_first.SECTION_TABS.items():
        assert tab in webapp_links.APP_TABS, cmd
    for tab in app_first.REPLY_TABS.values():
        assert tab is None or tab in webapp_links.APP_TABS


def test_section_command_answers_with_a_button_into_its_tab(with_app):
    msg = _Msg("/farm@rofl_bot")
    asyncio.run(app_first.section_moved(msg, user_lang="de"))
    text, markup = msg.sent[0]
    assert text == t("de", "app.moved")
    assert markup.inline_keyboard[0][0].web_app.url == "https://app.example?tab=farm"


def test_old_reply_keyboard_is_replaced_by_language_button_and_tab_opened(with_app):
    from shared.locales import btn
    msg = _Msg(btn("es", "games_zone"))
    asyncio.run(app_first.old_keyboard_pressed(msg, user_lang="es"))
    assert [[b.text for b in row] for row in msg.sent[0][1].keyboard] == [[btn("es", "open_app")], [btn("es", "language")]]
    assert msg.sent[1][1].inline_keyboard[0][0].web_app.url.endswith("tab=games")


def test_filter_lets_old_chat_handlers_work_without_the_app(monkeypatch):
    monkeypatch.setattr(config, "WEBAPP_URL", None)
    assert not app_first.app_ready()


def test_blue_menu_shows_only_chat_commands_when_app_is_on(with_app):
    shown = main_bot.menu_commands()
    assert set(shown) <= set(main_bot.APP_MODE_COMMANDS) and {"app", "invite", "paysupport"} <= set(shown)
    assert not set(shown) & set(app_first.SECTION_TABS)


def test_new_chat_texts_exist_in_all_languages():
    assert len(SUPPORTED_LANGS) == 14
    for lang in SUPPORTED_LANGS:
        for key in ("app.moved", "app.keyboard_gone", "start.console_app", "menu.app"):
            assert t(lang, key) and t(lang, key) != key, (lang, key)
        assert "{username}" not in t(lang, "start.welcome_back_app", username="x"), lang
        assert "/delete_account" in t(lang, "menu.app") and "/paysupport" in t(lang, "menu.app")


def test_app_first_router_comes_before_game_routers():
    src = (main_bot.__file__ and open(main_bot.__file__, encoding="utf-8").read())
    order = src[src.index("for r in (start_router"):]
    assert order.index("app_first_router") < order.index("games_router") < order.index("menu_router")


def _tg_message(text):
    from datetime import datetime
    from aiogram.types import Message
    return Message.model_validate({"message_id": 1, "date": datetime(2026, 10, 27), "text": text,
                                   "chat": {"id": 7, "type": "private"}, "from": {"id": 7, "is_bot": False, "first_name": "A"}})


async def _first_match(text):
    from aiogram import Bot
    bot = Bot("123456:TEST")
    for handler in app_first.router.message.handlers:
        ok, _ = await handler.check(_tg_message(text), bot=bot)
        if ok:
            return handler.callback.__name__
    return None


def test_aiogram_routes_section_commands_only_when_the_app_is_on(with_app, monkeypatch):
    assert asyncio.run(_first_match("/farm")) == "section_moved"
    assert asyncio.run(_first_match("/menu")) == "app_menu"
    assert asyncio.run(_first_match("/invite")) is None          # чатовые команды — дальше, к своим обработчикам
    monkeypatch.setattr(config, "WEBAPP_URL", None)
    assert asyncio.run(_first_match("/farm")) is None             # без приложения — прежняя чатовая ферма
