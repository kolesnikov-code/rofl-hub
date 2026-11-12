"""
Метрики Cyber Barons: чистые формулы + SQL-сборщики + форматтеры отчётов.

Деньги считаются ТОЛЬКО из ledger и star_payments (источники правды, возвраты
и TEST-чеки исключены). События (events) — для поведения, daily_activity — для
DAU/WAU/MAU и retention. Везде UTC. В отчётах — только агрегаты, без username
и ID игроков; единственное исключение — коды промоутеров.
"""
from __future__ import annotations

import html
import json
from datetime import date, datetime, timedelta, timezone

from shared.economy import (
    ACTIVATION_WINDOW_HOURS,
    LIMIT_TO_UNLIMIT_WINDOW_HOURS,
    RETENTION_COHORT_DAYS,
    TOP_RICH_PERCENT,
    VIRAL_WINDOW_DAYS,
    utcnow,
)

TG_MESSAGE_LIMIT = 4096

# Выручка: что исключаем из star_payments
_REVENUE_FILTER = "refunded_at IS NULL AND telegram_charge_id NOT LIKE 'TEST_%'"


# ============================================================================
# Чистые формулы (юнит-тестируются без БД)
# ============================================================================
def ratio(num: float, den: float) -> float:
    """Безопасное деление: 0.0 при нулевом/отрицательном знаменателе."""
    return num / den if den else 0.0


def pct(num: float, den: float) -> float:
    return 100.0 * ratio(num, den)


def k_factor(invited: int, cohort_size: int) -> float:
    return ratio(invited, cohort_size)


def stickiness(dau: int, mau: int) -> float:
    return pct(dau, mau)


def arpu(revenue: int, audience: int) -> float:
    return ratio(revenue, audience)


def arppu(revenue: int, payers: int) -> float:
    return ratio(revenue, payers)


def net_inflation(emission: int, burn: int) -> int:
    """Чистая инфляция монет: эмиссия минус сжигание (burn — положительное число)."""
    return emission - burn


def report_kind_for_hour(hour: int) -> str | None:
    """Расписание демона: только 00:00 UTC → полный суточный (владелец 12.11: экспрессы 06/12/18
    убраны — хватает суточного и /metrics по запросу)."""
    return "daily" if hour == 0 else None


def split_message(text: str, limit: int = TG_MESSAGE_LIMIT) -> list[str]:
    """Режет длинный отчёт по строкам так, чтобы каждая часть влезла в Telegram."""
    if len(text) <= limit:
        return [text]
    parts, current = [], ""
    for line in text.split("\n"):
        while len(line) > limit:          # сверхдлинная строка — жёсткая нарезка
            parts.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) + 1 > limit:
            parts.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        parts.append(current)
    return parts


def delta_str(cur: float | int | None, prev: float | int | None, suffix: str = "") -> str:
    """«(+3)» к прошлому срезу; «(н/д)», если прошлого среза нет."""
    if prev is None or cur is None:
        return ""
    diff = cur - prev
    if isinstance(diff, float):
        diff = round(diff, 2)
    sign = "+" if diff > 0 else ""
    return f" ({sign}{diff}{suffix})" if diff else " (=)"


# ============================================================================
# SQL-сборщики. Каждый принимает conn и границы периода [since, until).
# ============================================================================
async def fetch_acquisition(conn, since: datetime, until: datetime) -> dict:
    new_total = await conn.fetchval(
        "SELECT COUNT(*) FROM users WHERE created_at >= $1 AND created_at < $2", since, until)
    by_source = await conn.fetch(
        """SELECT source, COUNT(*) AS n FROM users
           WHERE created_at >= $1 AND created_at < $2
           GROUP BY source ORDER BY n DESC LIMIT 10""", since, until)
    by_lang = await conn.fetch(
        """SELECT lang, COUNT(*) AS n FROM users
           WHERE created_at >= $1 AND created_at < $2
           GROUP BY lang ORDER BY n DESC LIMIT 14""", since, until)
    top_channels = await conn.fetch(
        """SELECT source,
                  COUNT(*) AS regs,
                  COUNT(*) FILTER (WHERE qualified_at IS NOT NULL) AS qualified
           FROM users
           WHERE created_at >= $1 AND created_at < $2
             AND (source LIKE 'p\\_%' OR source LIKE 'c\\_%' OR source = 'tg_affiliate')
           GROUP BY source ORDER BY qualified DESC, regs DESC LIMIT 10""", since, until)
    return {
        "new_total": int(new_total or 0),
        "by_source": [{"source": r["source"], "n": int(r["n"])} for r in by_source],
        "by_lang": [{"lang": r["lang"], "n": int(r["n"])} for r in by_lang],
        "top_channels": [{"source": r["source"], "regs": int(r["regs"]),
                          "qualified": int(r["qualified"])} for r in top_channels],
    }


async def fetch_activation_funnel(conn, since: datetime, until: datetime) -> dict:
    """Воронка новичка за ACTIVATION_WINDOW_HOURS от регистрации."""
    row = await conn.fetchrow(
        f"""
        SELECT COUNT(*) AS registered,
               COUNT(*) FILTER (WHERE EXISTS (
                   SELECT 1 FROM events e WHERE e.user_id = u.user_id
                     AND e.event = 'onboarding_done'
                     AND e.created_at <= u.created_at + make_interval(hours => $3))) AS onboarded,
               COUNT(*) FILTER (WHERE EXISTS (
                   SELECT 1 FROM events e WHERE e.user_id = u.user_id
                     AND e.event = 'game_round'
                     AND e.created_at <= u.created_at + make_interval(hours => $3))) AS played,
               COUNT(*) FILTER (WHERE EXISTS (
                   SELECT 1 FROM star_payments p WHERE p.user_id = u.user_id
                     AND {_REVENUE_FILTER}
                     AND p.created_at <= u.created_at + make_interval(hours => $3))) AS paid
        FROM users u
        WHERE u.created_at >= $1 AND u.created_at < $2
        """,
        since, until, ACTIVATION_WINDOW_HOURS)
    return {k: int(row[k] or 0) for k in ("registered", "onboarded", "played", "paid")}


async def fetch_activity(conn, day: date) -> dict:
    dau = await conn.fetchval("SELECT COUNT(*) FROM daily_activity WHERE day = $1", day)
    wau = await conn.fetchval(
        "SELECT COUNT(DISTINCT user_id) FROM daily_activity "
        "WHERE day > $1::date - 7 AND day <= $1::date", day)
    mau = await conn.fetchval(
        "SELECT COUNT(DISTINCT user_id) FROM daily_activity "
        "WHERE day > $1::date - 30 AND day <= $1::date", day)
    dau, wau, mau = int(dau or 0), int(wau or 0), int(mau or 0)
    return {"dau": dau, "wau": wau, "mau": mau, "stickiness_pct": round(stickiness(dau, mau), 1)}


async def fetch_retention_cohorts(conn, last_n: int = 7) -> list[dict]:
    """Retention D1/D3/D7/D30 по когортам дня регистрации (NULL = день ещё не наступил)."""
    today = utcnow().date()
    selects = ", ".join(
        f"""COUNT(*) FILTER (WHERE EXISTS (
            SELECT 1 FROM daily_activity a
            WHERE a.user_id = u.user_id AND a.day = u.created_at::date + {d})) AS d{d}"""
        for d in RETENTION_COHORT_DAYS)
    rows = await conn.fetch(
        f"""SELECT u.created_at::date AS cohort, COUNT(*) AS size, {selects}
            FROM users u GROUP BY cohort ORDER BY cohort DESC LIMIT $1""", last_n)
    out = []
    for r in rows:
        item = {"cohort": r["cohort"].isoformat(), "size": int(r["size"])}
        for d in RETENTION_COHORT_DAYS:
            matured = r["cohort"] + timedelta(days=d) <= today
            item[f"d{d}_pct"] = round(pct(int(r[f"d{d}"]), int(r["size"])), 1) if matured else None
        out.append(item)
    return out


async def fetch_virality(conn, since: datetime, until: datetime) -> dict:
    """K-factor когорты регистраций [since, until): приглашения в окне VIRAL_WINDOW_DAYS."""
    row = await conn.fetchrow(
        """
        SELECT COUNT(*) AS cohort_size,
               COALESCE(SUM(inv.raw), 0) AS invited_raw,
               COALESCE(SUM(inv.qual), 0) AS invited_qualified,
               COUNT(*) FILTER (WHERE inv.raw > 0) AS inviters
        FROM users u
        LEFT JOIN LATERAL (
            SELECT COUNT(*) AS raw,
                   COUNT(*) FILTER (WHERE r.qualified_at IS NOT NULL) AS qual
            FROM users r
            WHERE r.referred_by = u.user_id
              AND r.created_at >= u.created_at
              AND r.created_at < u.created_at + make_interval(days => $3)
        ) inv ON TRUE
        WHERE u.created_at >= $1 AND u.created_at < $2
        """,
        since, until, VIRAL_WINDOW_DAYS)
    median_cycle_h = await conn.fetchval(
        """
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY first_invite)
        FROM (
            SELECT EXTRACT(EPOCH FROM MIN(r.created_at) - u.created_at) / 3600.0 AS first_invite
            FROM users u JOIN users r ON r.referred_by = u.user_id
            WHERE u.created_at >= $1 AND u.created_at < $2
            GROUP BY u.user_id, u.created_at
        ) t
        """,
        since, until)
    size = int(row["cohort_size"] or 0)
    raw = int(row["invited_raw"] or 0)
    qual = int(row["invited_qualified"] or 0)
    return {
        "cohort_size": size,
        "k_raw": round(k_factor(raw, size), 3),
        "k_qualified": round(k_factor(qual, size), 3),
        "inviter_share_pct": round(pct(int(row["inviters"] or 0), size), 1),
        "median_cycle_hours": round(float(median_cycle_h), 1) if median_cycle_h is not None else None,
    }


async def fetch_monetization(conn, since: datetime, until: datetime) -> dict:
    pay = await conn.fetchrow(
        f"""SELECT COALESCE(SUM(stars_amount), 0) AS revenue,
                   COUNT(DISTINCT user_id) AS payers, COUNT(*) AS purchases
            FROM star_payments
            WHERE created_at >= $1 AND created_at < $2 AND {_REVENUE_FILTER}""", since, until)
    by_sku = await conn.fetch(
        f"""SELECT item_payload AS sku, COUNT(*) AS n, SUM(stars_amount) AS stars
            FROM star_payments
            WHERE created_at >= $1 AND created_at < $2 AND {_REVENUE_FILTER}
            GROUP BY sku ORDER BY stars DESC LIMIT 10""", since, until)
    by_lang = await conn.fetch(
        f"""SELECT u.lang, SUM(p.stars_amount) AS stars
            FROM star_payments p JOIN users u ON u.user_id = p.user_id
            WHERE p.created_at >= $1 AND p.created_at < $2 AND {_REVENUE_FILTER}
            GROUP BY u.lang ORDER BY stars DESC LIMIT 14""", since, until)
    by_source = await conn.fetch(
        f"""SELECT u.source, SUM(p.stars_amount) AS stars
            FROM star_payments p JOIN users u ON u.user_id = p.user_id
            WHERE p.created_at >= $1 AND p.created_at < $2 AND {_REVENUE_FILTER}
            GROUP BY u.source ORDER BY stars DESC LIMIT 10""", since, until)
    first_sku = await conn.fetch(
        f"""SELECT sku, COUNT(*) AS n FROM (
                SELECT DISTINCT ON (user_id) user_id, item_payload AS sku
                FROM star_payments WHERE {_REVENUE_FILTER}
                ORDER BY user_id, created_at
            ) f GROUP BY sku ORDER BY n DESC LIMIT 5""")
    median_first_h = await conn.fetchval(
        f"""SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY hours) FROM (
                SELECT EXTRACT(EPOCH FROM MIN(p.created_at) - u.created_at) / 3600.0 AS hours
                FROM star_payments p JOIN users u ON u.user_id = p.user_id
                WHERE {_REVENUE_FILTER} GROUP BY u.user_id, u.created_at
            ) t""")
    repeat = await conn.fetchrow(
        f"""SELECT COUNT(*) AS payers,
                   COUNT(*) FILTER (WHERE n >= 2) AS repeaters
            FROM (SELECT user_id, COUNT(*) AS n FROM star_payments
                  WHERE {_REVENUE_FILTER} GROUP BY user_id) t""")
    limit_conv = await conn.fetchrow(
        f"""
        SELECT COUNT(DISTINCT e.user_id) AS hit_users,
               COUNT(DISTINCT e.user_id) FILTER (WHERE EXISTS (
                   SELECT 1 FROM star_payments p
                   WHERE p.user_id = e.user_id AND {_REVENUE_FILTER}
                     AND p.item_payload IN ('unlimit_24h', 'unlimit_30d')
                     AND p.created_at >= e.created_at
                     AND p.created_at <= e.created_at + make_interval(hours => $3)
               )) AS converted
        FROM events e
        WHERE e.event = 'daily_limit_hit' AND e.created_at >= $1 AND e.created_at < $2
        """,
        since, until, LIMIT_TO_UNLIMIT_WINDOW_HOURS)
    total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
    mau = await conn.fetchval(
        "SELECT COUNT(DISTINCT user_id) FROM daily_activity WHERE day > $1::date - 30", until.date())
    revenue, payers = int(pay["revenue"]), int(pay["payers"])
    payers_total, repeaters = int(repeat["payers"] or 0), int(repeat["repeaters"] or 0)
    return {
        "revenue_stars": revenue,
        "payers": payers,
        "purchases": int(pay["purchases"]),
        "cr_mau_pct": round(pct(payers, int(mau or 0)), 2),
        "cr_base_pct": round(pct(payers, int(total_users or 0)), 2),
        "arpu_stars": round(arpu(revenue, int(mau or 0)), 2),
        "arppu_stars": round(arppu(revenue, payers), 2),
        "by_sku": [{"sku": r["sku"], "n": int(r["n"]), "stars": int(r["stars"])} for r in by_sku],
        "by_lang": [{"lang": r["lang"], "stars": int(r["stars"])} for r in by_lang],
        "by_source": [{"source": r["source"], "stars": int(r["stars"])} for r in by_source],
        "first_purchase_sku": [{"sku": r["sku"], "n": int(r["n"])} for r in first_sku],
        "median_hours_to_first_purchase":
            round(float(median_first_h), 1) if median_first_h is not None else None,
        "repeat_buyers_pct": round(pct(repeaters, payers_total), 1),
        "limit_hit_users": int(limit_conv["hit_users"] or 0),
        "limit_to_unlimit_pct": round(
            pct(int(limit_conv["converted"] or 0), int(limit_conv["hit_users"] or 0)), 1),
    }


async def fetch_coin_economy(conn, since: datetime, until: datetime) -> dict:
    flows = await conn.fetch(
        """SELECT reason, SUM(delta) FILTER (WHERE delta > 0) AS plus,
                  SUM(-delta) FILTER (WHERE delta < 0) AS minus
           FROM ledger WHERE created_at >= $1 AND created_at < $2
           GROUP BY reason""", since, until)
    emission_by = sorted(({"reason": r["reason"], "coins": int(r["plus"])}
                          for r in flows if r["plus"]), key=lambda x: -x["coins"])[:10]
    burn_by = sorted(({"reason": r["reason"], "coins": int(r["minus"])}
                      for r in flows if r["minus"]), key=lambda x: -x["coins"])[:10]
    emission = sum(x["coins"] for x in emission_by)
    burn = sum(x["coins"] for x in burn_by)
    supply = int(await conn.fetchval("SELECT COALESCE(SUM(balance), 0) FROM users") or 0)
    top_row = await conn.fetchrow(
        """
        WITH ranked AS (SELECT balance, NTILE(100) OVER (ORDER BY balance DESC) AS tile FROM users)
        SELECT COALESCE(SUM(balance) FILTER (WHERE tile <= $1), 0) AS top_coins FROM ranked
        """, TOP_RICH_PERCENT)
    return {
        "emission": emission, "burn": burn, "net_inflation": net_inflation(emission, burn),
        "emission_by_reason": emission_by, "burn_by_reason": burn_by,
        "coin_supply": supply,
        "top1pct_share_pct": round(pct(int(top_row["top_coins"]), supply), 1),
    }


async def fetch_games_farm(conn, since: datetime, until: datetime) -> dict:
    games = await conn.fetch(
        """SELECT props->>'game' AS game, COUNT(*) AS rounds,
                  COUNT(*) FILTER (WHERE props->>'result' = 'win') AS wins
           FROM events WHERE event = 'game_round' AND created_at >= $1 AND created_at < $2
           GROUP BY game ORDER BY rounds DESC""", since, until)
    limit_hits = await conn.fetch(
        """SELECT props->>'game' AS game, COUNT(*) AS n
           FROM events WHERE event = 'daily_limit_hit' AND created_at >= $1 AND created_at < $2
           GROUP BY game ORDER BY n DESC""", since, until)
    miners = await conn.fetchrow(
        """SELECT COUNT(*) FILTER (WHERE expires_at > NOW()) AS active,
                  COUNT(*) FILTER (WHERE expires_at >= $1 AND expires_at < $2) AS burned
           FROM miners""", since, until)
    hungry = await conn.fetchrow(
        """
        SELECT COUNT(DISTINCT m.user_id) AS drill_owners,
               COUNT(DISTINCT m.user_id) FILTER (WHERE u.fridge_cutlets = 0) AS hungry
        FROM miners m JOIN users u ON u.user_id = m.user_id
        WHERE m.kind = 'premium' AND m.expires_at > NOW()
        """)
    return {
        "games": [{"game": r["game"] or "?", "rounds": int(r["rounds"]),
                   "winrate_pct": round(pct(int(r["wins"]), int(r["rounds"])), 1)} for r in games],
        "limit_hits": [{"game": r["game"] or "?", "n": int(r["n"])} for r in limit_hits],
        "miners_active": int(miners["active"] or 0),
        "miners_burned": int(miners["burned"] or 0),
        "drill_owners": int(hungry["drill_owners"] or 0),
        "hungry_drill_owners_pct": round(
            pct(int(hungry["hungry"] or 0), int(hungry["drill_owners"] or 0)), 1),
    }


async def fetch_spend_cohorts(conn) -> list[dict]:
    """Когорты трат за 30 дней: F2P / до 100★ / 100–500★ / 500+★ + поведение каждой."""
    rows = await conn.fetch(
        f"""
        WITH spend AS (
            SELECT u.user_id,
                   COALESCE((SELECT SUM(p.stars_amount) FROM star_payments p
                             WHERE p.user_id = u.user_id AND {_REVENUE_FILTER}
                               AND p.created_at > NOW() - INTERVAL '30 days'), 0) AS stars
            FROM users u
        ),
        tagged AS (
            SELECT user_id, CASE WHEN stars = 0 THEN 'f2p'
                                 WHEN stars < 100 THEN 'light'
                                 WHEN stars < 500 THEN 'normal'
                                 ELSE 'whale' END AS cohort
            FROM spend
        )
        SELECT cohort, COUNT(*) AS size,
               COUNT(*) FILTER (WHERE EXISTS (
                   SELECT 1 FROM daily_activity a
                   WHERE a.user_id = tagged.user_id AND a.day > CURRENT_DATE - 7)) AS active_7d,
               COALESCE(SUM((SELECT COUNT(*) FROM users r
                             WHERE r.referred_by = tagged.user_id
                               AND r.qualified_at IS NOT NULL
                               AND r.created_at > NOW() - INTERVAL '30 days')), 0) AS k_invited
        FROM tagged GROUP BY cohort
        """)
    fav = await conn.fetch(
        f"""
        WITH spend AS (
            SELECT u.user_id,
                   COALESCE((SELECT SUM(p.stars_amount) FROM star_payments p
                             WHERE p.user_id = u.user_id AND {_REVENUE_FILTER}
                               AND p.created_at > NOW() - INTERVAL '30 days'), 0) AS stars
            FROM users u
        ),
        tagged AS (
            SELECT user_id, CASE WHEN stars = 0 THEN 'f2p'
                                 WHEN stars < 100 THEN 'light'
                                 WHEN stars < 500 THEN 'normal'
                                 ELSE 'whale' END AS cohort
            FROM spend
        ),
        plays AS (
            SELECT t.cohort, e.props->>'game' AS game, COUNT(*) AS n
            FROM events e JOIN tagged t ON t.user_id = e.user_id
            WHERE e.event = 'game_round' AND e.created_at > NOW() - INTERVAL '30 days'
            GROUP BY t.cohort, game
        )
        SELECT DISTINCT ON (cohort) cohort, game FROM plays ORDER BY cohort, n DESC
        """)
    fav_map = {r["cohort"]: r["game"] for r in fav}
    order = {"f2p": 0, "light": 1, "normal": 2, "whale": 3}
    out = []
    for r in sorted(rows, key=lambda x: order.get(x["cohort"], 9)):
        size = int(r["size"])
        out.append({
            "cohort": r["cohort"], "size": size,
            "active_7d_pct": round(pct(int(r["active_7d"]), size), 1),
            "favorite_game": fav_map.get(r["cohort"]),
            "k_qualified_30d": round(k_factor(int(r["k_invited"]), size), 3),
        })
    return out


# ============================================================================
# Снапшот целиком (демон и /metrics)
# ============================================================================
async def collect_snapshot(conn, since: datetime, until: datetime) -> dict:
    day = (until - timedelta(seconds=1)).date()
    return {
        "period": {"since": since.isoformat(), "until": until.isoformat()},
        "acquisition": await fetch_acquisition(conn, since, until),
        "funnel": await fetch_activation_funnel(conn, since, until),
        "activity": await fetch_activity(conn, day),
        "virality_7d": await fetch_virality(conn, until - timedelta(days=7), until),
        "monetization": await fetch_monetization(conn, since, until),
        "economy": await fetch_coin_economy(conn, since, until),
        "games_farm": await fetch_games_farm(conn, since, until),
    }


# ============================================================================
# Форматтеры отчётов (HTML, только агрегаты)
# ============================================================================
def _esc(value) -> str:
    return html.escape(str(value), quote=False)


def _g(snap: dict | None, *path):
    cur = snap
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def build_express_report(snap: dict, prev: dict | None, hour: int) -> str:
    a, m, v = snap["activity"], snap["monetization"], snap["virality_7d"]
    top3 = snap["acquisition"]["by_source"][:3]
    top_str = ", ".join(f"{_esc(s['source'])}: {s['n']}" for s in top3) or "—"
    return (
        f"⏱️ <b>ЭКСПРЕСС-АНАЛИТИКА ({hour:02d}:00 UTC, за сутки)</b>\n"
        f"{'.' * 50}\n\n"
        f"🆕 Новые игроки: <b>{snap['acquisition']['new_total']}</b>"
        f"{delta_str(snap['acquisition']['new_total'], _g(prev, 'acquisition', 'new_total'))}\n"
        f"👥 DAU: <b>{a['dau']}</b>{delta_str(a['dau'], _g(prev, 'activity', 'dau'))}"
        f" · WAU: {a['wau']} · MAU: {a['mau']}"
        f" · липкость: {a['stickiness_pct']}%\n"
        f"💵 Выручка за сутки: <b>★ {m['revenue_stars']}</b>"
        f"{delta_str(m['revenue_stars'], _g(prev, 'monetization', 'revenue_stars'))}"
        f" · платящих: {m['payers']}\n"
        f"🧲 K-qualified (7 дней): <b>{v['k_qualified']}</b>"
        f"{delta_str(v['k_qualified'], _g(prev, 'virality_7d', 'k_qualified'))}"
        f" · K-raw: {v['k_raw']}\n"
        f"📣 Топ-3 источника суток: {top_str}\n"
        f"{'.' * 50}\n"
        f"<i>⚙️ Дельты — к предыдущему срезу. Полный разбор — в полночном отчёте.</i>"
    )


def _format_retention_table(cohorts: list[dict]) -> str:
    lines = []
    for c in cohorts:
        cells = " · ".join(
            f"D{d}: {c[f'd{d}_pct']}%" if c[f"d{d}_pct"] is not None else f"D{d}: —"
            for d in RETENTION_COHORT_DAYS)
        lines.append(f"{c['cohort']} ({c['size']} чел.) → {cells}")
    return "\n".join(lines) or "—"


def build_daily_report(snap: dict, prev: dict | None, retention: list[dict],
                       spend_cohorts: list[dict]) -> str:
    acq, f, a = snap["acquisition"], snap["funnel"], snap["activity"]
    m, eco, gf, v = snap["monetization"], snap["economy"], snap["games_farm"], snap["virality_7d"]
    src_lines = "\n".join(f"  • {_esc(s['source'])}: {s['n']}" for s in acq["by_source"]) or "  • —"
    lang_lines = ", ".join(f"{_esc(x['lang'])}: {x['n']}" for x in acq["by_lang"]) or "—"
    chan_lines = "\n".join(
        f"  • {_esc(c['source'])}: {c['qualified']} квал. из {c['regs']}"
        for c in acq["top_channels"]) or "  • —"
    sku_lines = "\n".join(
        f"  • {_esc(s['sku'])}: ★ {s['stars']} ({s['n']} шт.)" for s in m["by_sku"]) or "  • —"
    first_sku = ", ".join(f"{_esc(s['sku'])} ×{s['n']}" for s in m["first_purchase_sku"]) or "—"
    emi_lines = ", ".join(f"{_esc(x['reason'])}: +{x['coins']}"
                          for x in eco["emission_by_reason"][:5]) or "—"
    burn_lines = ", ".join(f"{_esc(x['reason'])}: −{x['coins']}"
                           for x in eco["burn_by_reason"][:5]) or "—"
    game_lines = "\n".join(
        f"  • {_esc(g['game'])}: {g['rounds']} раундов, winrate {g['winrate_pct']}%"
        for g in gf["games"]) or "  • —"
    hit_lines = ", ".join(f"{_esc(h['game'])}: {h['n']}" for h in gf["limit_hits"]) or "—"
    cohort_names = {"f2p": "F2P", "light": "до 100★", "normal": "100–500★", "whale": "500+★"}
    spend_lines = "\n".join(
        f"  • {cohort_names.get(c['cohort'], c['cohort'])}: {c['size']} чел., "
        f"активны 7д: {c['active_7d_pct']}%, любимая игра: {_esc(c['favorite_game'] or '—')}, "
        f"K-qual: {c['k_qualified_30d']}"
        for c in spend_cohorts) or "  • —"
    median_first = (f"{m['median_hours_to_first_purchase']} ч"
                    if m["median_hours_to_first_purchase"] is not None else "—")
    median_cycle = (f"{v['median_cycle_hours']} ч"
                    if v["median_cycle_hours"] is not None else "—")
    return (
        f"👑 <b>ПОЛНЫЙ СУТОЧНЫЙ СРЕЗ (00:00 UTC)</b>\n"
        f"{'.' * 50}\n\n"
        f"🆕 <b>ПРИВЛЕЧЕНИЕ</b>: {acq['new_total']} новых"
        f"{delta_str(acq['new_total'], _g(prev, 'acquisition', 'new_total'))}\n"
        f"{src_lines}\n"
        f"  Языки: {lang_lines}\n"
        f"  Каналы/промоутеры (квалифицированные):\n{chan_lines}\n\n"
        f"🚀 <b>ВОРОНКА 24 Ч</b>: регистрация {f['registered']} → онбординг {f['onboarded']} → "
        f"первая игра {f['played']} → первая покупка {f['paid']}\n\n"
        f"👥 <b>АКТИВНОСТЬ</b>: DAU {a['dau']}{delta_str(a['dau'], _g(prev, 'activity', 'dau'))} · "
        f"WAU {a['wau']} · MAU {a['mau']} · липкость {a['stickiness_pct']}%\n\n"
        f"📈 <b>RETENTION ПОСЛЕДНИХ КОГОРТ</b>:\n{_format_retention_table(retention)}\n\n"
        f"🧲 <b>ВИРУСНОСТЬ (7 дней)</b>: K-raw {v['k_raw']} · K-qualified {v['k_qualified']} · "
        f"приглашают {v['inviter_share_pct']}% · медиана цикла {median_cycle}\n\n"
        f"💵 <b>МОНЕТИЗАЦИЯ (сутки)</b>: ★ {m['revenue_stars']}"
        f"{delta_str(m['revenue_stars'], _g(prev, 'monetization', 'revenue_stars'))} · "
        f"платящих {m['payers']} · CR от MAU {m['cr_mau_pct']}% · от базы {m['cr_base_pct']}%\n"
        f"  ARPU ★ {m['arpu_stars']} · ARPPU ★ {m['arppu_stars']} · "
        f"повторные {m['repeat_buyers_pct']}% · медиана до 1-й покупки {median_first}\n"
        f"  SKU суток:\n{sku_lines}\n"
        f"  Первая покупка (все время): {first_sku}\n"
        f"  Лимит → безлимит за 24 ч: {m['limit_to_unlimit_pct']}% "
        f"из {m['limit_hit_users']} упёршихся\n\n"
        f"🪙 <b>ЭКОНОМИКА МОНЕТ (сутки)</b>: эмиссия +{eco['emission']} · сжигание −{eco['burn']} · "
        f"инфляция {eco['net_inflation']:+}\n"
        f"  Масса: {eco['coin_supply']} · у топ-{TOP_RICH_PERCENT}%: {eco['top1pct_share_pct']}%\n"
        f"  Принтеры: {emi_lines}\n  Печки: {burn_lines}\n\n"
        f"🎮 <b>ИГРЫ (сутки)</b>:\n{game_lines}\n"
        f"  Упёрлись в лимит: {hit_lines}\n"
        f"  Роботы: активных {gf['miners_active']} · сгорело за сутки {gf['miners_burned']} · "
        f"Бурильщики с пустым Холодильником: {gf['hungry_drill_owners_pct']}%\n\n"
        f"💳 <b>КОГОРТЫ ТРАТ (30 дней)</b>:\n{spend_lines}\n"
        f"{'.' * 50}\n"
        f"<i>📈 Срез сохранён в metrics_snapshots. Дельты — к предыдущему суточному срезу.</i>"
    )


def snapshot_to_json(snap: dict) -> str:
    return json.dumps(snap, ensure_ascii=False, default=str)
