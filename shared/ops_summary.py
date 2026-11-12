"""
Сводка для пульта холдинга владельца: GET /ops/summary (контракт v1, см. репозиторий pult).

Запрос пульта подписан HMAC секретом OPS_SECRET (shared/ops_sign.py — копия из пульта).
Без OPS_SECRET адрес не существует (404). Только агрегаты — никаких ID, имён и username.
Деньги — из star_payments без возвратов и TEST-чеков (как в shared/metrics.py).

details — полная аналитика (бывший полночный отчёт в Тайную Комнату, теперь — в пульте): разделы
«подпись → значение» из shared/metrics. Считается не чаще раза в DETAILS_TTL секунд; сбой
аналитики не роняет сводку — она уходит без details.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta, timezone

from aiohttp import web

from shared import metrics
from shared.database import db
from shared.ops_sign import HEADER_SIG, HEADER_TS, MIN_SECRET_LEN, verify

logger = logging.getLogger(__name__)

PATH = "/ops/summary"
DETAILS_TTL = 60
_details_cache: dict = {"at": 0.0, "data": None}
COHORT_NAMES = {"f2p": "F2P", "light": "до 100★", "normal": "100–500★", "whale": "500+★"}

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


def _top(items: list[dict], key: str, val: str, fmt: str = "{}", n: int = 5) -> str:
    return ", ".join(f"{x[key]}: {fmt.format(x[val])}" for x in items[:n]) or "—"


def _hours(value) -> str:
    return f"{value} ч" if value is not None else "—"


def build_details(snap: dict, retention: list[dict], spend: list[dict]) -> list[dict]:
    """Полная аналитика за сутки разделами для пульта (только агрегаты; источники — коды промоутеров)."""
    acq, f, a = snap["acquisition"], snap["funnel"], snap["activity"]
    m, eco, gf, v = snap["monetization"], snap["economy"], snap["games_farm"], snap["virality_7d"]
    ret_rows = [[f"{c['cohort']} ({c['size']} чел.)",
                 " · ".join(f"D{d} {c[f'd{d}_pct']}%" if c[f"d{d}_pct"] is not None else f"D{d} —"
                            for d in metrics.RETENTION_COHORT_DAYS)] for c in retention]
    return [
        {"title": "🆕 Привлечение за сутки", "rows": [
            ["Новых игроков", acq["new_total"]],
            ["Источники", _top(acq["by_source"], "source", "n")],
            ["Языки", _top(acq["by_lang"], "lang", "n")],
            ["Каналы (квал. из рег.)", ", ".join(f"{c['source']}: {c['qualified']}/{c['regs']}"
                                                 for c in acq["top_channels"][:5]) or "—"],
        ]},
        {"title": "🚀 Воронка новичка (24 ч)", "rows": [
            ["Регистрация", f["registered"]], ["Онбординг", f["onboarded"]],
            ["Первая игра", f["played"]], ["Первая покупка", f["paid"]],
        ]},
        {"title": "👥 Активность", "rows": [
            ["DAU / WAU / MAU", f"{a['dau']} / {a['wau']} / {a['mau']}"],
            ["Липкость DAU/MAU", f"{a['stickiness_pct']}%"],
        ]},
        {"title": "📈 Retention последних когорт", "rows": ret_rows or [["Когорт пока нет", "—"]]},
        {"title": "🧲 Вирусность (7 дней)", "rows": [
            ["K-raw / K-qualified", f"{v['k_raw']} / {v['k_qualified']}"],
            ["Приглашают", f"{v['inviter_share_pct']}%"],
            ["Медиана до 1-го приглашения", _hours(v["median_cycle_hours"])],
        ]},
        {"title": "💵 Монетизация за сутки", "rows": [
            ["Выручка", f"★ {m['revenue_stars']}, покупок: {m['purchases']}"],
            ["Платящих", m["payers"]],
            ["CR от MAU / от базы", f"{m['cr_mau_pct']}% / {m['cr_base_pct']}%"],
            ["ARPU / ARPPU", f"★ {m['arpu_stars']} / ★ {m['arppu_stars']}"],
            ["Повторные покупатели", f"{m['repeat_buyers_pct']}%"],
            ["Медиана до 1-й покупки", _hours(m["median_hours_to_first_purchase"])],
            ["Лимит → безлимит за 24 ч", f"{m['limit_to_unlimit_pct']}% из {m['limit_hit_users']}"],
            ["Товары суток", _top(m["by_sku"], "sku", "stars", "★ {}")],
            ["Первая покупка (всё время)", _top(m["first_purchase_sku"], "sku", "n", "×{}")],
        ]},
        {"title": "🪙 Экономика монет за сутки", "rows": [
            ["Эмиссия / сжигание", f"+{eco['emission']} / −{eco['burn']}"],
            ["Инфляция", f"{eco['net_inflation']:+}"],
            ["Масса монет", eco["coin_supply"]],
            [f"Доля топ-{metrics.TOP_RICH_PERCENT}%", f"{eco['top1pct_share_pct']}%"],
            ["Принтеры", _top(eco["emission_by_reason"], "reason", "coins", "+{}")],
            ["Печки", _top(eco["burn_by_reason"], "reason", "coins", "−{}")],
        ]},
        {"title": "🎮 Игры и ферма за сутки", "rows": [
            *[[g["game"], f"{g['rounds']} раундов, winrate {g['winrate_pct']}%"] for g in gf["games"][:8]],
            ["Упёрлись в лимит", _top(gf["limit_hits"], "game", "n")],
            ["Роботов активно / сгорело", f"{gf['miners_active']} / {gf['miners_burned']}"],
            ["Бурильщики без котлет", f"{gf['hungry_drill_owners_pct']}%"],
        ]},
        {"title": "💳 Когорты трат (30 дней)", "rows": [
            [COHORT_NAMES.get(c["cohort"], c["cohort"]),
             f"{c['size']} чел., активны {c['active_7d_pct']}%, K {c['k_qualified_30d']}, "
             f"игра: {c['favorite_game'] or '—'}"] for c in spend] or [["Данных нет", "—"]]},
    ]


async def _details(conn) -> list[dict] | None:
    if _details_cache["data"] is not None and time.monotonic() - _details_cache["at"] < DETAILS_TTL:
        return _details_cache["data"]
    try:
        now = datetime.now(timezone.utc)
        snap = await metrics.collect_snapshot(conn, now - timedelta(days=1), now)
        retention = await metrics.fetch_retention_cohorts(conn, last_n=7)
        spend = await metrics.fetch_spend_cohorts(conn)
        data = build_details(snap, retention, spend)
    except Exception:
        logger.exception("ops: аналитика для пульта не собралась")
        return None
    _details_cache.update(at=time.monotonic(), data=data)
    return data


async def handle_ops_summary(request: web.Request) -> web.Response:
    secret = ops_secret()
    if len(secret) < MIN_SECRET_LEN or not verify(secret, request.method, PATH,
                                                  request.headers.get(HEADER_TS), request.headers.get(HEADER_SIG)):
        raise web.HTTPNotFound()   # снаружи адрес выглядит несуществующим
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(SUMMARY_SQL)
        details = await _details(conn)
    payload = build_payload(row)
    if details:
        payload["details"] = details
    return web.json_response(payload, headers={"Cache-Control": "no-store"})


def register_ops_routes(app: web.Application) -> None:
    app.router.add_get(PATH, handle_ops_summary)
