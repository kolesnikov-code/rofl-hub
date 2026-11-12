"""
Сводка для пульта холдинга владельца: GET /ops/summary (контракт v1, см. репозиторий pult).

Запрос пульта подписан HMAC секретом OPS_SECRET (shared/ops_sign.py — копия из пульта).
Без OPS_SECRET адрес не существует (404). Только агрегаты — никаких ID, имён и username.
Деньги — из star_payments без возвратов и TEST-чеков (как в shared/metrics.py).
"""
from __future__ import annotations

import logging
import os

from aiohttp import web

from shared.database import db
from shared.ops_sign import HEADER_SIG, HEADER_TS, MIN_SECRET_LEN, verify

logger = logging.getLogger(__name__)

PATH = "/ops/summary"

SUMMARY_SQL = """
SELECT
  (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL) AS total,
  (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL AND created_at > now() - interval '24 hours') AS new_24h,
  (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL AND last_seen_at > now() - interval '24 hours') AS active_24h,
  (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL AND last_seen_at > now() - interval '7 days') AS active_7d,
  (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments WHERE refunded_at IS NULL
     AND telegram_charge_id NOT LIKE 'TEST_%' AND created_at > now() - interval '24 hours') AS stars_24h,
  (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments WHERE refunded_at IS NULL
     AND telegram_charge_id NOT LIKE 'TEST_%' AND created_at > now() - interval '30 days') AS stars_30d,
  (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments WHERE refunded_at IS NULL
     AND telegram_charge_id NOT LIKE 'TEST_%') AS stars_total,
  (SELECT COUNT(*) FROM teams) AS teams,
  (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL AND qualified_at IS NOT NULL) AS qualified,
  (SELECT COUNT(*) FROM market_trades WHERE created_at > now() - interval '24 hours') AS trades_24h,
  (SELECT COUNT(*) FROM battles WHERE status = 'active') AS battles_active
"""


def ops_secret() -> str:
    return os.getenv("OPS_SECRET", "").strip()


def build_payload(row) -> dict:
    r = dict(row)
    return {
        "v": 1,
        "users": {k: int(r[k]) for k in ("total", "new_24h", "active_24h", "active_7d")},
        "money": {k: int(r[k]) for k in ("stars_24h", "stars_30d", "stars_total")},
        "kpis": [
            {"key": "teams", "label": "Команд и отрядов", "value": int(r["teams"])},
            {"key": "qualified", "label": "Активных (3 ур. + 3 котлеты)", "value": int(r["qualified"])},
            {"key": "trades_24h", "label": "Сделок на бирже за сутки", "value": int(r["trades_24h"])},
            {"key": "battles_active", "label": "Идущих битв и акций", "value": int(r["battles_active"])},
        ],
        "alerts": [],
    }


async def handle_ops_summary(request: web.Request) -> web.Response:
    secret = ops_secret()
    if len(secret) < MIN_SECRET_LEN or not verify(secret, request.method, PATH,
                                                  request.headers.get(HEADER_TS), request.headers.get(HEADER_SIG)):
        raise web.HTTPNotFound()   # снаружи адрес выглядит несуществующим
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(SUMMARY_SQL)
    return web.json_response(build_payload(row), headers={"Cache-Control": "no-store"})


def register_ops_routes(app: web.Application) -> None:
    app.router.add_get(PATH, handle_ops_summary)
