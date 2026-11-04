"""
🎛 Пульт владельца (Mini App): доступ только ADMIN_ID, проверка формы битвы, VIP-кандидаты, маршруты.
Чистые тесты без БД; выдача призов, итоги и аукционы — в test_db_integration.py.
"""
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from aiohttp.test_utils import TestClient, TestServer

from bots.main_bot.webapp_admin import VIP_POOL, VIP_PREFIX, admin_ids, validate_battle_form, vip_candidates
from shared.webapp_auth import sign_init_data

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)
TOKEN = "123456:TEST"


def _form(**kw):
    base = {"title": "Кубок", "scope": "teams", "nomination": "farm_mined", "starts_at": "now", "hours": 72,
            "places": 3, "prizes": {"1": [{"kind": "coins", "amount": 500}], "2": [{"kind": "bogus"}], "9": [{"kind": "coins", "amount": 5}]},
            "mine_ids": [4, 9]}
    base.update(kw)
    return base


def test_validate_battle_form_happy_path():
    form, err = validate_battle_form(_form(), {4, 9, 12}, NOW)
    assert err is None
    assert form["starts_at"] == NOW and form["ends_at"] == NOW + timedelta(hours=72)
    assert form["prizes"] == {"1": [{"kind": "coins", "amount": 500}]}          # мусор и места за пределами — отброшены
    assert form["mine_ids"] == [4, 9] and form["places"] == 3
    assert form["nomination_text"].startswith("⛏️")


@pytest.mark.parametrize("patch, needle", [
    ({"title": ""}, "Название"), ({"title": "x" * 101}, "Название"),
    ({"scope": "galaxy"}, "зачёт"), ({"nomination": "nope"}, "номинацию"),
    ({"nomination": "custom", "custom": "ab"}, "Своя"),
    ({"nomination": "tiktok", "scope": "teams", "mine_ids": []}, "Соцсети"),
    ({"hours": 0}, "Длительность"), ({"hours": 24 * 366}, "Длительность"),
    ({"places": 101}, "мест"), ({"places": -1}, "мест"),
    ({"scope": "solo", "nomination": "farm_mined"}, "Рудники"),
    ({"mine_ids": [4, 13]}, "свободные"),
    ({"places": 1}, "Рудников не больше"),
    ({"starts_at": "2020-01-01T00:00:00+00:00"}, "прошлом"), ({"starts_at": "вчера"}, "дата"),
])
def test_validate_battle_form_rejects(patch, needle):
    form, err = validate_battle_form(_form(**patch), {4, 9, 12}, NOW)
    assert form is None and needle in err, err


def test_validate_battle_form_custom_solo_and_mines_raise_places():
    form, err = validate_battle_form(_form(nomination="custom", custom="Лучший мем", scope="solo", mine_ids=[]), set(), NOW)
    assert err is None and form["nomination_text"] == "Лучший мем" and form["mine_ids"] == []
    form, err = validate_battle_form(_form(places=0, mine_ids=[4, 9, 12]), {4, 9, 12}, NOW)
    assert err is None and form["places"] == 3                                  # 3 рудника — 3 призовых места
    form, err = validate_battle_form(_form(starts_at="2026-10-28T18:00:00"), {4, 9}, NOW)
    assert err is None and form["starts_at"] == datetime(2026, 10, 28, 18, 0, tzinfo=timezone.utc)
    form, err = validate_battle_form(_form(mine_ids=[4, 4, "x", 9]), {4, 9}, NOW)
    assert err is None and form["mine_ids"] == [4, 9]


def test_vip_candidates_skip_taken_and_rotate():
    taken = {VIP_PREFIX + "777", VIP_PREFIX + "SHARK"}
    first = vip_candidates(taken, 10, 0)
    assert len(first) == 10 and not set(first) & taken and all(a.startswith(VIP_PREFIX) for a in first)
    assert vip_candidates(taken, 10, 10) != first
    assert vip_candidates({VIP_PREFIX + x for x in VIP_POOL}) == []
    assert all(len(VIP_PREFIX + x) <= 32 and not (VIP_PREFIX + x).isdigit() for x in VIP_POOL)


def test_admin_ids_from_env(monkeypatch):
    monkeypatch.setenv("ADMIN_ID", "111, 222,abc,")
    assert admin_ids() == {111, 222}
    monkeypatch.setenv("ADMIN_ID", "")
    assert admin_ids() == set()


def test_admin_panel_url_and_hidden_command():
    from bots.main_bot.bot import BOT_COMMANDS
    from bots.main_bot.handlers.admin_panel import admin_panel_url
    assert admin_panel_url("https://x.app") == "https://x.app/admin"
    assert admin_panel_url("https://x.app/?tab=farm") == "https://x.app/admin"
    assert admin_panel_url("") is None
    assert "admin" not in BOT_COMMANDS                                          # не светится в синем меню


def _init(uid: int) -> str:
    return sign_init_data({"auth_date": str(int(time.time())), "user": {"id": uid, "first_name": "A"}}, TOKEN)


async def test_admin_api_requires_owner(monkeypatch):
    from bots.main_bot.webapp import create_webapp
    monkeypatch.setenv("ADMIN_ID", "111")
    client = TestClient(TestServer(create_webapp(TOKEN)))
    await client.start_server()
    try:
        for method, path in (("GET", "/api/admin/meta"), ("GET", "/api/admin/battles"), ("POST", "/api/admin/battle"),
                             ("POST", "/api/admin/battle/close"), ("POST", "/api/admin/battle/manual"),
                             ("POST", "/api/admin/reward"), ("GET", "/api/admin/vip"), ("POST", "/api/admin/vip/auction"),
                             ("POST", "/api/admin/flag")):
            r = await client.request(method, path)
            assert r.status == 401, path                                         # без подписи Telegram
            r = await client.request(method, path, headers={"X-Telegram-Init-Data": _init(222)})
            assert r.status == 403, path                                         # чужой ID
        page = await client.get("/admin")
        assert page.status == 200 and "ПУЛЬТ CYBER BARONS" in await page.text()
    finally:
        await client.close()


def test_admin_html_has_every_section_and_reward_kind():
    html = (ROOT / "static" / "webapp" / "admin.html").read_text(encoding="utf-8")
    for needle in ("/api/admin/meta", "/api/admin/battle", "/api/admin/battle/close", "/api/admin/battle/manual",
                   "/api/admin/reward", "/api/admin/vip/auction", "/api/admin/flag", "season_prev",
                   "rewardBuilder", "X-Telegram-Init-Data"):
        assert needle in html, needle
    from shared.prizes import REWARD_KINDS
    for kind in REWARD_KINDS:
        assert f'["{kind}",' in html, kind
    assert "railway" not in html.lower()


def test_events_and_battery_routes_for_players():
    from bots.main_bot.webapp import create_webapp
    app = create_webapp(TOKEN)
    paths = {r.resource.canonical for r in app.router.routes() if r.resource is not None}
    for p in ("/api/events", "/api/battle/battery", "/admin", "/api/admin/meta"):
        assert p in paths, p


def test_player_ui_events_tab_and_battle_entry():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert '["season", "events", "rich"]' in html and "function viewEvents" in html and "/api/events" in html
    assert "/api/battle/battery" in html and "L.bt_entry" in html and "L.bt_info" in html
