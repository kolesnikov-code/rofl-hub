"""🎛 Сводка для пульта холдинга: без подписи OPS_SECRET адреса «нет», формат v1, только агрегаты."""
import asyncio

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from shared import ops_summary
from shared.ops_sign import sign_headers

SECRET = "o" * 40


def _client_status(monkeypatch, secret_env: str, headers: dict) -> int:
    monkeypatch.setenv("OPS_SECRET", secret_env)

    async def go():
        app = web.Application()
        ops_summary.register_ops_routes(app)
        client = TestClient(TestServer(app))
        await client.start_server()
        try:
            return (await client.get(ops_summary.PATH, headers=headers)).status
        finally:
            await client.close()
    return asyncio.run(go())


def test_unsigned_or_wrong_secret_looks_like_missing_page(monkeypatch):
    good = sign_headers(SECRET, "GET", ops_summary.PATH)
    assert _client_status(monkeypatch, SECRET, {}) == 404
    assert _client_status(monkeypatch, SECRET, sign_headers("w" * 40, "GET", ops_summary.PATH)) == 404
    assert _client_status(monkeypatch, "", good) == 404            # без OPS_SECRET адрес выключен
    assert _client_status(monkeypatch, "short", sign_headers("short", "GET", ops_summary.PATH)) == 404


def test_payload_is_contract_v1_with_aggregates_only():
    row = {"total": 10, "new_24h": 2, "active_24h": 4, "active_7d": 7, "stars_24h": 15, "stars_30d": 264,
           "stars_total": 300, "teams": 3, "qualified": 1, "trades_24h": 5, "battles_active": 0}
    p = ops_summary.build_payload(row)
    assert p["v"] == 1 and p["users"] == {"total": 10, "new_24h": 2, "active_24h": 4, "active_7d": 7}
    assert p["money"] == {"stars_24h": 15, "stars_30d": 264, "stars_total": 300}
    assert [k["key"] for k in p["kpis"]] == ["teams", "qualified", "trades_24h", "battles_active"]
    assert set(p) == {"v", "users", "money", "kpis", "alerts"}


def test_details_carry_the_former_daily_report_as_sections():
    from tests.test_metrics import _fake_snapshot
    retention = [{"cohort": "2026-11-12", "size": 5, "d1_pct": 40.0, "d3_pct": None, "d7_pct": None,
                  "d30_pct": None}]
    spend = [{"cohort": "f2p", "size": 10, "active_7d_pct": 30.0, "favorite_game": None,
              "k_qualified_30d": 0.1}]
    sections = ops_summary.build_details(_fake_snapshot(), retention, spend)
    titles = " ".join(s["title"] for s in sections)
    for marker in ("Привлечение", "Воронка", "Активность", "Retention", "Вирусность", "Монетизация",
                   "Экономика", "Игры", "Когорты трат"):
        assert marker in titles
    rows = {r[0]: r[1] for s in sections for r in s["rows"]}
    assert rows["DAU / WAU / MAU"] == "10 / 20 / 40" and rows["Выручка"] == "★ 150, покупок: 3"
    assert rows["2026-11-12 (5 чел.)"].startswith("D1 40.0% · D3 —")
    assert rows["F2P"].endswith("игра: —")


def test_signing_file_is_the_pult_contract():
    from shared import ops_sign
    assert ops_sign.HEADER_TS == "X-Ops-Ts" and ops_sign.HEADER_SIG == "X-Ops-Sig" and ops_sign.MAX_SKEW == 300
