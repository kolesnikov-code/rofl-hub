"""
🔐 ПИН пульта владельца (shared/admin_pin.py + admin_pin_middleware): хэш, блокировка, сессии и сам вход —
на фейковом пуле (одна строка admin_pin в памяти), без настоящей БД.
"""
import time
from datetime import timedelta

import pytest
from aiohttp.test_utils import TestClient, TestServer

from shared import admin_pin
from shared.economy import utcnow
from shared.webapp_auth import sign_init_data

TOKEN = "123456:TEST"


def _init(uid):
    return sign_init_data({"auth_date": str(int(time.time())), "user": {"id": uid, "first_name": "A"}}, TOKEN)


# ---------------------------------------------------------------- чистая логика
def test_pin_hash_is_salted_and_checkable():
    h1, h2 = admin_pin.hash_pin("2468"), admin_pin.hash_pin("2468")
    assert h1 != h2 and "2468" not in h1                                     # соль разная, ПИН не хранится
    assert admin_pin.check_pin("2468", h1) and not admin_pin.check_pin("2469", h1)
    assert not admin_pin.check_pin("2468", None) and not admin_pin.check_pin("2468", "мусор")


@pytest.mark.parametrize("pin, ok", [("1234", True), ("12345678", True), ("123", False), ("123456789", False),
                                     ("12a4", False), ("", False), (1234, False)])
def test_valid_pin(pin, ok):
    assert admin_pin.valid_pin(pin) is ok


def test_lock_after_five_fails_doubles_and_caps_at_a_day():
    assert [admin_pin.lock_seconds(n) for n in range(5)] == [0] * 5
    assert admin_pin.lock_seconds(5) == 900 and admin_pin.lock_seconds(6) == 1800
    assert admin_pin.lock_seconds(50) == 24 * 3600


def test_session_is_bound_to_user_pin_version_and_time():
    sec = admin_pin.session_secret(TOKEN)
    tok = admin_pin.issue_session(sec, 111, "v1", now=1000)
    assert admin_pin.verify_session(tok, sec, 111, "v1", now=1001)
    assert not admin_pin.verify_session(tok, sec, 222, "v1", now=1001)          # чужой ID
    assert not admin_pin.verify_session(tok, sec, 111, "v2", now=1001)          # ПИН сменили/сбросили
    assert not admin_pin.verify_session(tok, sec, 111, "v1", now=1000 + 13 * 3600)   # срок вышел
    assert not admin_pin.verify_session(tok, admin_pin.session_secret("9:OTHER"), 111, "v1", now=1001)
    assert not admin_pin.verify_session(None, sec, 111, "v1") and not admin_pin.verify_session("a.b", sec, 111, "v1")


# ---------------------------------------------------------------- вход через API на фейковом пуле
class _Conn:
    def __init__(self, store):
        self.s = store

    def transaction(self):
        conn = self

        class _T:
            async def __aenter__(self):
                return conn

            async def __aexit__(self, *a):
                return False
        return _T()

    async def execute(self, sql, *args):
        if sql.startswith("DELETE"):
            self.s.clear()
        elif sql.startswith("INSERT"):
            self.s.setdefault("row", {"pin_hash": None, "pin_ver": None, "fails": 0, "locked_until": None})
        elif "pin_hash = $1" in sql:
            self.s["row"].update(pin_hash=args[0], pin_ver=args[1], fails=0, locked_until=None)
        elif "fails = $1" in sql:
            self.s["row"].update(fails=args[0], locked_until=args[1])
        elif "fails = 0" in sql:
            self.s["row"].update(fails=0, locked_until=None)

    async def fetchrow(self, sql, *args):
        return dict(self.s["row"]) if "row" in self.s else None


class _Pool:
    def __init__(self):
        self.store = {}

    def acquire(self):
        conn = _Conn(self.store)

        class _A:
            async def __aenter__(self):
                return conn

            async def __aexit__(self, *a):
                return False
        return _A()


@pytest.fixture
def pool(monkeypatch):
    from shared.database import db
    import bots.main_bot.webapp_admin as wa
    p = _Pool()
    monkeypatch.setattr(db, "_pool", p)
    monkeypatch.setattr(wa, "_reset_done", False)
    monkeypatch.setenv("ADMIN_ID", "111")
    monkeypatch.delenv("ADMIN_RESET_PIN", raising=False)
    return p


async def _client():
    from bots.main_bot.webapp import create_webapp
    c = TestClient(TestServer(create_webapp(TOKEN)))
    await c.start_server()
    return c


async def test_admin_api_needs_pin_session_after_telegram_signature(pool):
    c = await _client()
    h = {"X-Telegram-Init-Data": _init(111)}
    try:
        assert (await c.get("/api/admin/meta")).status == 401                      # без подписи
        assert (await c.get("/api/admin/meta", headers={"X-Telegram-Init-Data": _init(222)})).status == 403
        r = await c.get("/api/admin/meta", headers=h)
        assert r.status == 401 and (await r.json())["error"] == "pin"               # владелец, но без ПИНа
        st = await (await c.get("/api/admin/auth/state", headers=h)).json()
        assert st == {"pin_set": False, "locked_for": 0}
        r = await c.post("/api/admin/auth", json={"pin": "2468"}, headers=h)
        assert r.status == 409                                                     # ПИНа нет — только setup
        r = await c.post("/api/admin/auth", json={"pin": "2468", "setup": True}, headers=h)
        sess = (await r.json())["session"]
        assert "2468" not in str(pool.store)
        r = await c.post("/api/admin/auth", json={"pin": "1111", "setup": True}, headers=h)
        assert r.status == 403                                                     # setup не перезаписывает ПИН
        r = await c.get("/api/admin/auth/state", headers={"X-Telegram-Init-Data": _init(222)})
        assert r.status == 403                                                     # чужому — даже состояние
        # с сессией защита ПИНом пройдена (дальше — обработчик; без БД он может упасть, но не 401 pin)
        r = await c.get("/api/admin/meta", headers={**h, admin_pin.SESSION_HEADER: sess})
        assert not (r.status == 401 and (await r.json(content_type=None) or {}).get("error") == "pin")
        r = await c.get("/api/admin/meta", headers={**h, admin_pin.SESSION_HEADER: sess + "0"})
        assert r.status == 401
    finally:
        await c.close()


async def test_five_wrong_pins_lock_the_door_and_reset_env_clears_it(pool, monkeypatch):
    c = await _client()
    h = {"X-Telegram-Init-Data": _init(111)}
    try:
        await c.post("/api/admin/auth", json={"pin": "2468", "setup": True}, headers=h)
        lefts = []
        for _ in range(4):
            r = await c.post("/api/admin/auth", json={"pin": "0000"}, headers=h)
            assert r.status == 403
            lefts.append((await r.json())["left"])
        assert lefts == [4, 3, 2, 1]
        r = await c.post("/api/admin/auth", json={"pin": "0000"}, headers=h)
        assert r.status == 429 and (await r.json())["locked_for"] == 900
        r = await c.post("/api/admin/auth", json={"pin": "2468"}, headers=h)
        assert r.status == 429                                                     # даже верный ПИН — ждать
        pool.store["row"]["locked_until"] = utcnow() - timedelta(seconds=1)        # срок вышел — пускает
        r = await c.post("/api/admin/auth", json={"pin": "2468"}, headers=h)
        assert r.status == 200 and pool.store["row"]["fails"] == 0
        monkeypatch.setenv("ADMIN_RESET_PIN", "1")                                 # забыл ПИН
        st = await (await c.get("/api/admin/auth/state", headers=h)).json()
        assert st["pin_set"] is False
        r = await c.post("/api/admin/auth", json={"pin": "1357", "setup": True}, headers=h)
        assert r.status == 200
        st = await (await c.get("/api/admin/auth/state", headers=h)).json()
        assert st["pin_set"] is True                                               # сброс — один раз за запуск
    finally:
        await c.close()


def test_admin_html_asks_pin_before_the_panel():
    from pathlib import Path
    html = (Path(__file__).resolve().parents[1] / "static" / "webapp" / "admin.html").read_text(encoding="utf-8")
    assert "X-Admin-Session" in html and "/api/admin/auth" in html and "pinScreen()" in html
    assert "localStorage" not in html.split("pinScreen")[0][-2000:]                # сессия — только sessionStorage
