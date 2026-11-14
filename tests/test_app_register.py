"""
Вход сразу в приложение (кнопка «Открыть» в списке чатов, t.me/<бот>?startapp=…): новичок регистрируется так же,
как по /start — бонус, язык из Telegram, пригласивший и источник из start_param. Фейковый пул, без БД.
"""
import asyncio
import os
import time

import pytest

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

import bots.main_bot.handlers.start as start
from bots.main_bot.webapp import register_from_app
from shared.webapp_auth import sign_init_data

TOKEN = "123456:TEST"


class _Req:
    def __init__(self, uid, start_param=None, lang="pt-br", username="neo"):
        pairs = {"auth_date": str(int(time.time())),
                 "user": {"id": uid, "first_name": "Neo", "last_name": "A", "language_code": lang, "username": username}}
        if start_param is not None:
            pairs["start_param"] = start_param
        self.headers = {"X-Telegram-Init-Data": sign_init_data(pairs, TOKEN)}
        self.app = {"bot_token": TOKEN}


class _Conn:
    def __init__(self, existing=()):
        self.existing, self.calls = set(existing), []

    async def fetchval(self, sql, *args):
        return 1 if args[0] in self.existing else None

    async def execute(self, sql, *args):
        self.calls.append((sql, args))

    def transaction(self):
        class _T:
            async def __aenter__(self):
                return None

            async def __aexit__(self, *a):
                return False
        return _T()


class _Pool:
    def __init__(self, conn):
        self.conn = conn

    def acquire(self):
        conn = self.conn

        class _A:
            async def __aenter__(self):
                return conn

            async def __aexit__(self, *a):
                return False
        return _A()


@pytest.fixture
def env(monkeypatch):
    conn = _Conn(existing={777})
    from shared.database import db
    monkeypatch.setattr(db, "_pool", _Pool(conn))
    made, events = [], []

    async def fake_register(c, uid, username, lang, referrer, display_name=None, source="organic"):
        made.append(dict(uid=uid, username=username, lang=lang, referrer=referrer, name=display_name, source=source))
        return True

    async def fake_track(uid, event, **props):
        events.append((uid, event, props))

    async def fake_invite(c, code):
        return {"player1": 777} if code == "v6uc3f4r" else None
    monkeypatch.setattr(start, "register_user", fake_register)
    monkeypatch.setattr("bots.main_bot.webapp.track", fake_track)
    monkeypatch.setattr("shared.duels.invite_info", fake_invite)
    return conn, made, events


def test_newcomer_from_the_open_button_is_registered_with_telegram_language(env):
    conn, made, events = env
    assert asyncio.run(register_from_app(_Req(42))) is True
    assert made == [dict(uid=42, username="neo", lang="pt", referrer=None, name="Neo A", source="organic")]
    assert events == [(42, "registered", {"source": "organic", "lang": "pt", "via": "app"})]


@pytest.mark.parametrize("sp, referrer, source", [
    ("777", 777, "referral"),            # ссылка друга ?startapp=<ID>
    ("42", None, "organic"),             # свой ID — не реферал
    ("p_blogger", None, "p_blogger"),    # промоутер
    ("duel_v6uc3f4r", 777, "referral"),    # вызов на дуэль — вызвавший становится пригласившим
])
def test_start_param_sets_referrer_and_source(env, sp, referrer, source):
    conn, made, _ = env
    asyncio.run(register_from_app(_Req(42, sp)))
    assert (made[0]["referrer"], made[0]["source"]) == (referrer, source)
    if sp.startswith("duel_"):
        assert conn.calls and conn.calls[-1][1] == (42, "v6uc3f4r")       # окно «Принять вызов» в приложении


def test_existing_player_and_bad_signature_are_not_registered(env):
    _, made, _ = env
    assert asyncio.run(register_from_app(_Req(777))) is False                # уже есть (в т.ч. удалённый — только /start)
    bad = _Req(43)
    bad.headers["X-Telegram-Init-Data"] += "x"
    assert asyncio.run(register_from_app(bad)) is False
    assert made == []


# ---------------------------------------------------------------- 14.11: язык в приложении и первое приветствие в чате
class _LangConn(_Conn):
    def __init__(self, rows=1, due=None):
        super().__init__()
        self.rows, self.due = rows, due

    async def execute(self, sql, *args):
        self.calls.append((sql, args))
        return f"UPDATE {self.rows}"

    async def fetchval(self, sql, *args):
        return self.due


def test_app_language_switch_saves_only_known_languages(monkeypatch):
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.database import db
    conn = _LangConn()
    monkeypatch.setattr(db, "_pool", _Pool(conn))

    async def go():
        c = TestClient(TestServer(create_webapp(TOKEN)))
        await c.start_server()
        try:
            h = _Req(42).headers
            assert (await c.post("/api/lang", json={"lang": "uz"})).status == 401
            assert (await c.post("/api/lang", json={"lang": "xx"}, headers=h)).status == 400
            r = await c.post("/api/lang", json={"lang": "uz"}, headers=h)
            assert r.status == 200 and (await r.json()) == {"lang": "uz"}
            assert conn.calls[-1][1] == (42, "uz")
            conn.rows = 0
            assert (await c.post("/api/lang", json={"lang": "en"}, headers=h)).status == 404
        finally:
            await c.close()
    asyncio.run(go())


def test_app_language_options_match_chat_buttons():
    from bots.main_bot.webapp import _lang_options
    assert [c for c, _ in _lang_options("ru")] == ["en", "uz", "ru"]
    assert _lang_options("pt")[-1] == ["pt", "🇧🇷 Português"]          # подобранный автоматически — тоже в списке


def test_first_start_after_app_registration_gets_the_full_welcome_once(monkeypatch):
    from shared.database import db
    conn = _LangConn(due=True)
    monkeypatch.setattr(db, "_pool", _Pool(conn))
    assert asyncio.run(start._take_chat_welcome(42)) is True
    conn.due = None                                                       # флаг снят атомарно — второй раз нет
    assert asyncio.run(start._take_chat_welcome(42)) is False


def test_app_has_language_chip():
    from pathlib import Path
    html = (Path(__file__).resolve().parents[1] / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert 'id="langChip"' in html and "function chooseLang" in html and '"/api/lang"' in html
