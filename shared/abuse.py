"""
🕵️ Проверка на абуз (решение владельца 30.10): алгоритм сам ищет, кого стоит проверить, и раскладывает
доказательства по полочкам. Только игровые данные за ABUSE_WINDOW_DAYS дней — журналы, которые игра и так ведёт
(ledger, resource_ledger, team_help, market_trades, resource_swaps, raids, duels, star_payments, events).

Сигналы (баллы складываются, у каждого — объяснение по-русски для пульта):
  • воронка ресурсов / монет — один аккаунт получает от многих (фарм на твинках и слив в «главный»);
  • кормушка — аккаунт отдаёт почти всё одному игроку;
  • свои рефералы кормят пригласившего — самый жёсткий признак фермы твинков;
  • биржа: одни и те же пары и сделки в разы дороже рынка (перевод монет под видом торговли);
  • налёты в одну цель раз за разом (цель «подставляется»), дуэли одной пары с одним победителем (слив ставок);
  • друзья, пропавшие сразу после квалификации (накрутка награды за рефералов), пачки регистраций за сутки;
  • «круглосуточная» активность (18+ разных часов в сутки — похоже на бота), возвраты Stars, связи с забаненными.

Ничего не блокирует само: решение принимает владелец (кнопки «Проверен» и «Заблокировать» в пульте).
Отметка «Проверен» опускает игрока вниз ленты, пока его баллы не вырастут выше отмеченных.
"""
from __future__ import annotations

import time
from collections import defaultdict
from datetime import datetime, timedelta
from statistics import median

ABUSE_WINDOW_DAYS = 30
ABUSE_FEED_LIMIT = 300          # карточек в ленте (подозрительные + самые активные «чистые» в хвосте)
ABUSE_CACHE_SECONDS = 60
DETAIL_ROWS = 400               # строк журнала в одной категории карточки

# Пороги и баллы сигналов
FUNNEL_MIN_GIVERS = 2           # воронка — от 2 разных дарителей…
FUNNEL_MIN_QTY = 200            # …или от 200 ресурсов суммарно
COIN_FUNNEL_MIN = 2000          # монет переводами
FEEDER_SHARE = 0.8              # доля отданного одному получателю
FEEDER_MIN_QTY = 100
FEEDER_MIN_COINS = 1000
THIN_AGE_DAYS = 14              # «тонкий» аккаунт — моложе двух недель или интеллект ≤ 3
THIN_QUIZ_LEVEL = 3
PAIR_MIN_TRADES = 3
OVERPAY_RATIO = 3               # цена ≥ 3× медианы актива
OVERPAY_MIN_COINS = 1000
RAID_FARM_MIN = 3               # побед одного налётчика над одной целью
DUEL_PAIR_MIN = 4
DUEL_ONE_SIDED = 0.8
REF_BURST_DAY = 5
BOT_HOURS = 18
LEVELS = ((60, "red"), (30, "orange"), (10, "yellow"), (0, "green"))


def level_of(score: int) -> str:
    return next(name for edge, name in LEVELS if score >= edge)


def asset_label(asset: str) -> str:
    """Подпись товара биржи: ресурс — с иконкой, котлета — 🥩, остальное (детали, скины) — кодом."""
    from shared.resources import RESOURCE_ICONS
    return "🥩 котлеты" if asset == "cutlet" else f"{RESOURCE_ICONS[asset]} {asset}" if asset in RESOURCE_ICONS else asset


def _sig(code: str, points: float, text: str, cap: int, links=()) -> dict:
    return {"code": code, "points": int(min(cap, round(points))), "text": text, "links": sorted(set(links))}


def score_user(f: dict, name) -> list[dict]:
    """Чистая оценка: факты игрока → сигналы с баллами (по убыванию). name(uid) — подпись другого игрока."""
    out = []
    thin = f.get("thin", False)
    # 🎁 воронка ресурсов
    givers = f.get("help_in", {})
    q_in = sum(givers.values())
    if len(givers) >= FUNNEL_MIN_GIVERS or q_in >= FUNNEL_MIN_QTY:
        top = sorted(givers.items(), key=lambda x: -x[1])[:5]
        out.append(_sig("funnel", 4 * len(givers) + q_in / 50, f"Получил(а) {q_in} ресурсов в команде от {len(givers)} игроков: "
                        + ", ".join(f"{name(u)} — {q}" for u, q in top), 50, givers))
    # 💸 воронка монет
    senders = f.get("tr_in", {})
    c_in = sum(senders.values())
    if len(senders) >= FUNNEL_MIN_GIVERS or c_in >= COIN_FUNNEL_MIN:
        top = sorted(senders.items(), key=lambda x: -x[1])[:5]
        out.append(_sig("coin_funnel", 4 * len(senders) + c_in / 500, f"Получил(а) переводами {c_in} 🪙 от {len(senders)} игроков: "
                        + ", ".join(f"{name(u)} — {c}" for u, c in top), 50, senders))
    # 🍼 кормушка: почти всё — одному
    for key, minimum, unit in (("help_out", FEEDER_MIN_QTY, "ресурсов"), ("tr_out", FEEDER_MIN_COINS, "🪙")):
        dest = f.get(key, {})
        total = sum(dest.values())
        if total >= minimum:
            uid, top = max(dest.items(), key=lambda x: x[1])
            if top / total >= FEEDER_SHARE:
                base = 15 + total / (100 if unit != "🪙" else 1000) + (10 if thin else 0)
                out.append(_sig("feeder", base, f"Отдаёт почти всё одному игроку: {name(uid)} — {top} {unit} из {total}"
                                + (" (молодой/слабый аккаунт — похоже на твинка)" if thin else ""), 35, [uid]))
    # 👥 свои рефералы кормят пригласившего
    feeders = f.get("own_ref_feeders", [])
    if feeders:
        out.append(_sig("ref_feeders", 15 * len(feeders), f"Его/её же рефералы ({len(feeders)}) отдают ему/ей ресурсы и монеты: "
                        + ", ".join(name(u) for u in feeders[:8]), 60, feeders))
    if f.get("feeds_referrer"):
        out.append(_sig("feeds_referrer", 15, f"Кормит того, кто пригласил: {name(f['feeds_referrer'])}", 15, [f["feeds_referrer"]]))
    # 📈 биржа: одна пара раз за разом и переплата
    for cp, n in f.get("market_pairs", {}).items():
        if n >= PAIR_MIN_TRADES:
            out.append(_sig("market_pair", 5 * n, f"Сделок на бирже с одним и тем же игроком: {n} — {name(cp)}", 30, [cp]))
    over = f.get("overpay", [])
    if over:
        coins = sum(o["coins"] for o in over)
        groups: dict[tuple, int] = {}
        for o in over:
            k = (o["role"], o["qty"], o["asset"], o["price"], o["median"], o["cp"])
            groups[k] = groups.get(k, 0) + 1
        sample = "; ".join(f"{role} {qty} {asset_label(asset)} по {price} 🪙 (рынок ~{med})" + (f" ×{n}" if n > 1 else "")
                           + f" — {name(cp)}" for (role, qty, asset, price, med, cp), n in list(groups.items())[:4])
        out.append(_sig("overpay", 20 + coins / 1000, f"Сделки в {OVERPAY_RATIO}+ раз дороже рынка (перевод монет под видом торговли), "
                        f"{coins} 🪙: {sample}", 45, [o["cp"] for o in over]))
    # ⚔️ налёты в одну цель
    for cp, n in f.get("raid_wins_vs", {}).items():
        if n >= RAID_FARM_MIN:
            out.append(_sig("raid_farm", 8 * n, f"Удачных налётов на одного и того же игрока: {n} — {name(cp)}", 40, [cp]))
    for cp, n in f.get("raid_losses_to", {}).items():
        if n >= RAID_FARM_MIN:
            out.append(_sig("raid_victim", 5 * n, f"Раз за разом проигрывает налёты одному игроку ({n}): {name(cp)} — "
                            "возможна подставная цель", 25, [cp]))
    # 🥊 дуэли одной пары с одним победителем
    for cp, (total, mine) in f.get("duel_pairs", {}).items():
        if total >= DUEL_PAIR_MIN:
            share = mine / total
            if share >= DUEL_ONE_SIDED:
                out.append(_sig("duel_dump_win", 6 * total, f"Побед в дуэлях с одним соперником: {mine} из {total} — {name(cp)}; "
                                "похоже на слив ставок", 40, [cp]))
            elif share <= 1 - DUEL_ONE_SIDED:
                out.append(_sig("duel_dump_lose", 4 * total, f"Поражений в дуэлях одному сопернику: {total - mine} из {total} — "
                                f"{name(cp)}; возможно, сливает ставки", 30, [cp]))
    for cp, n in f.get("swap_pairs", {}).items():
        if n >= PAIR_MIN_TRADES:
            out.append(_sig("swap_pair", 5 * n, f"Обменов ресурсами с одним игроком: {n} — {name(cp)}", 20, [cp]))
    # 🤝 рефералы
    ab, q = f.get("refs_abandoned", 0), f.get("refs_qualified", 0)
    if ab >= 2:
        out.append(_sig("ref_abandoned", 10 * ab, f"Активных друзей, пропавших сразу после того, как принесли награду: {ab} из {q} — "
                        "накрутка рефералов", 50, f.get("abandoned_ids", [])))
    if f.get("refs_day_max", 0) >= REF_BURST_DAY:
        out.append(_sig("ref_burst", 15, f"Регистраций по ссылке за одни сутки: {f['refs_day_max']}", 15))
    if f.get("bot_days", 0):
        out.append(_sig("bot_hours", 10 * f["bot_days"], f"Дней с активностью в {BOT_HOURS}+ разных часах суток: {f['bot_days']} — "
                        "похоже на бота или общий аккаунт", 40))
    if f.get("refunds", 0):
        out.append(_sig("refunds", 10 * f["refunds"], f"Возвратов Stars: {f['refunds']}", 30))
    banned = f.get("banned_links", [])
    if banned:
        out.append(_sig("banned_links", 15 * len(banned), "Связан(а) с заблокированными: " + ", ".join(name(u) for u in banned[:6]),
                        45, banned))
    return sorted((s for s in out if s["points"] > 0), key=lambda s: -s["points"])


# ============================================================================
# Сбор фактов (один проход SQL на всю базу; на текущих масштабах — доли секунды)
# ============================================================================
def _cut(now: datetime) -> datetime:
    return now - timedelta(days=ABUSE_WINDOW_DAYS)


async def collect(conn, now: datetime) -> tuple[dict, dict]:
    """Возвращает (facts по игрокам, users-справочник)."""
    since = _cut(now)
    users = {r["user_id"]: dict(r) for r in await conn.fetch(
        """SELECT u.user_id, u.username, u.display_name, u.created_at, u.last_seen_at, u.is_blocked, u.referred_by,
                  u.qualified_at, u.team_id, u.balance, u.bonus_claims, COALESCE(g.quiz_level, 0) AS quiz_level
           FROM users u LEFT JOIN game_stats g ON g.user_id = u.user_id WHERE u.deleted_at IS NULL""")}
    F: dict[int, dict] = defaultdict(lambda: defaultdict(dict))

    def add(uid, key, cp, v):
        d = F[uid].setdefault(key, {})
        d[cp] = d.get(cp, 0) + v

    for r in await conn.fetch(
            """SELECT g.user_id AS giver, h.user_id AS receiver, SUM(-g.delta)::bigint AS qty
               FROM resource_ledger g JOIN team_help h ON g.ref ~ '^[0-9]+$' AND h.id = g.ref::bigint
               WHERE g.reason = 'team_help_give' AND g.created_at >= $1 GROUP BY 1, 2""", since):
        add(r["receiver"], "help_in", r["giver"], int(r["qty"]))
        add(r["giver"], "help_out", r["receiver"], int(r["qty"]))
    for r in await conn.fetch(
            """SELECT user_id AS sender, ref::bigint AS recipient, SUM(-delta)::bigint AS coins FROM ledger
               WHERE reason = 'transfer_out' AND created_at >= $1 AND ref ~ '^[0-9]+$' GROUP BY 1, 2""", since):
        add(r["recipient"], "tr_in", r["sender"], int(r["coins"]))
        add(r["sender"], "tr_out", r["recipient"], int(r["coins"]))
    trades = await conn.fetch("SELECT buyer_id, seller_id, asset, qty, price FROM market_trades WHERE created_at >= $1 "
                              "ORDER BY id DESC LIMIT 50000", since)
    med = {a: median(p) for a, p in _group(trades, "asset", "price").items()}
    for r in trades:
        b, s = r["buyer_id"], r["seller_id"]
        add(b, "market_pairs", s, 1)
        add(s, "market_pairs", b, 1)
        m = med.get(r["asset"]) or 0
        coins = r["qty"] * r["price"]
        if m and r["price"] >= OVERPAY_RATIO * m and coins >= OVERPAY_MIN_COINS:
            base = {"asset": r["asset"], "qty": r["qty"], "price": r["price"], "median": int(m), "coins": coins}
            F[b].setdefault("overpay", []).append({**base, "cp": s, "role": "купил(а)"})
            F[s].setdefault("overpay", []).append({**base, "cp": b, "role": "продал(а)"})
    for r in await conn.fetch("""SELECT attacker_id, defender_id, COUNT(*) FILTER (WHERE result = 'win') AS wins
                                 FROM raids WHERE created_at >= $1 GROUP BY 1, 2""", since):
        if r["wins"]:
            add(r["attacker_id"], "raid_wins_vs", r["defender_id"], int(r["wins"]))
            add(r["defender_id"], "raid_losses_to", r["attacker_id"], int(r["wins"]))
    for r in await conn.fetch("""SELECT player1, player2, winner_id FROM duels WHERE status = 'finished'
                                 AND player2 IS NOT NULL AND finished_at >= $1""", since):
        for me, cp in ((r["player1"], r["player2"]), (r["player2"], r["player1"])):
            t, w = F[me].setdefault("duel_pairs", {}).get(cp, (0, 0))
            F[me]["duel_pairs"][cp] = (t + 1, w + (r["winner_id"] == me))
    for r in await conn.fetch("""SELECT maker_id, taker_id, COUNT(*) AS n FROM resource_swaps WHERE status = 'done'
                                 AND taker_id IS NOT NULL AND created_at >= $1 GROUP BY 1, 2""", since):
        add(r["maker_id"], "swap_pairs", r["taker_id"], int(r["n"]))
        add(r["taker_id"], "swap_pairs", r["maker_id"], int(r["n"]))
    # 👥 рефералы: брошенные после квалификации и пачки регистраций
    last_day = {r["user_id"]: r["d"] for r in await conn.fetch(
        "SELECT user_id, MAX(day) AS d FROM daily_activity GROUP BY 1")}
    per_day: dict[tuple, int] = defaultdict(int)
    for u in users.values():
        ref = u["referred_by"]
        if not ref or ref not in users:
            continue
        if u["created_at"] >= since:
            per_day[(ref, u["created_at"].date())] += 1
        q = u["qualified_at"]
        if q and q >= since:
            F[ref]["refs_qualified"] = F[ref].get("refs_qualified", 0) + 1
            ld = last_day.get(u["user_id"])
            if now - q > timedelta(days=3) and (ld is None or ld <= q.date() + timedelta(days=1)):
                F[ref]["refs_abandoned"] = F[ref].get("refs_abandoned", 0) + 1
                F[ref].setdefault("abandoned_ids", []).append(u["user_id"])
    for (ref, _), n in per_day.items():
        F[ref]["refs_day_max"] = max(F[ref].get("refs_day_max", 0), n)
    # кто кормит своего пригласившего
    for uid, f in list(F.items()):
        for cp in set(f.get("help_out", {})) | set(f.get("tr_out", {})):
            if users.get(uid, {}).get("referred_by") == cp:
                F[uid]["feeds_referrer"] = cp
                F[cp].setdefault("own_ref_feeders", []).append(uid)
    for r in await conn.fetch(
            """SELECT user_id, COUNT(*) AS days FROM (
                 SELECT user_id, created_at::date AS d FROM (
                   SELECT user_id, created_at FROM events WHERE created_at >= $1
                   UNION ALL SELECT user_id, created_at FROM game_rounds WHERE created_at >= $1) x
                 GROUP BY 1, 2 HAVING COUNT(DISTINCT EXTRACT(HOUR FROM created_at)) >= $2) y GROUP BY 1""", since, BOT_HOURS):
        F[r["user_id"]]["bot_days"] = int(r["days"])
    for r in await conn.fetch("SELECT user_id, COUNT(*) AS n FROM star_payments WHERE refunded_at >= $1 GROUP BY 1", since):
        F[r["user_id"]]["refunds"] = int(r["n"])
    # связи с забаненными и «тонкость»
    for uid, f in F.items():
        u = users.get(uid)
        if not u:
            continue
        f["thin"] = (now - u["created_at"]).days < THIN_AGE_DAYS or u["quiz_level"] <= THIN_QUIZ_LEVEL
        linked = set()
        for key in ("help_in", "help_out", "tr_in", "tr_out", "market_pairs", "swap_pairs"):
            linked |= set(f.get(key, {}))
        f["banned_links"] = sorted(c for c in linked if users.get(c, {}).get("is_blocked") and c != uid)
    return F, users


def _group(rows, key, val) -> dict:
    out = defaultdict(list)
    for r in rows:
        out[r[key]].append(r[val])
    return out


def label(u: dict | None, uid: int) -> str:
    if not u:
        return f"#{uid}"
    nm = ("@" + u["username"]) if u.get("username") else (u.get("display_name") or "")
    return f"{nm} ({uid})" if nm else f"#{uid}"


_cache: dict = {}


async def feed(conn, now: datetime, use_cache: bool = True) -> list[dict]:
    """Лента карточек: самые подозрительные сверху, проверенные (без роста баллов) — ниже, чистые активные — в хвосте."""
    if use_cache and _cache.get("at", 0) > time.monotonic() - ABUSE_CACHE_SECONDS:
        return _cache["feed"]
    F, users = await collect(conn, now)
    reviews = {r["user_id"]: dict(r) for r in await conn.fetch("SELECT user_id, score, note, reviewed_at FROM abuse_reviews")}
    active = {r["user_id"] for r in await conn.fetch("SELECT DISTINCT user_id FROM daily_activity WHERE day >= $1",
                                                     _cut(now).date())}
    name = lambda u: label(users.get(u), u)  # noqa: E731
    cards = []
    for uid in set(F) | active:
        u = users.get(uid)
        if not u:
            continue
        sigs = score_user(F.get(uid, {}), name)
        score = sum(s["points"] for s in sigs)
        rv = reviews.get(uid)
        cleared = bool(rv) and score <= rv["score"]
        cards.append({"id": uid, "name": label(u, uid), "score": score, "level": level_of(score), "blocked": u["is_blocked"],
                      "reasons": [s["text"] for s in sigs[:3]], "signals": len(sigs),
                      "links": len({c for s in sigs for c in s["links"]}),
                      "reviewed": rv and {"score": rv["score"], "at": rv["reviewed_at"].isoformat(), "note": rv["note"]},
                      "cleared": cleared, "age_days": (now - u["created_at"]).days, "quiz": u["quiz_level"]})
    cards.sort(key=lambda c: (c["blocked"], c["cleared"], -c["score"], -c["signals"], c["id"]))
    cards = cards[:ABUSE_FEED_LIMIT]
    _cache.update(at=time.monotonic(), feed=cards)
    return cards


def invalidate() -> None:
    _cache.clear()


async def review(conn, user_id: int, note: str, now: datetime) -> int:
    """«Проверен»: запоминаем баллы на сейчас — игрок уходит вниз, пока не наберёт больше."""
    F, users = await collect(conn, now)
    if user_id not in users:
        raise KeyError(user_id)
    score = sum(s["points"] for s in score_user(F.get(user_id, {}), lambda u: label(users.get(u), u)))
    await conn.execute(
        "INSERT INTO abuse_reviews (user_id, score, note, reviewed_at) VALUES ($1, $2, $3, $4) "
        "ON CONFLICT (user_id) DO UPDATE SET score = EXCLUDED.score, note = EXCLUDED.note, reviewed_at = EXCLUDED.reviewed_at",
        user_id, score, note[:300], now)
    invalidate()
    return score


# ============================================================================
# Полная карточка игрока — категории, как разделы магазина
# ============================================================================
async def detail(conn, user_id: int, now: datetime) -> dict | None:
    F, users = await collect(conn, now)
    u = users.get(user_id)
    if not u:
        return None
    since = _cut(now)
    f = F.get(user_id, {})
    name = lambda x: label(users.get(x), x)  # noqa: E731
    sigs = score_user(f, name)
    team = await conn.fetchval("SELECT team_name FROM teams WHERE team_id = $1", u["team_id"]) if u["team_id"] else None
    rv = await conn.fetchrow("SELECT score, note, reviewed_at FROM abuse_reviews WHERE user_id = $1", user_id)
    iso = lambda v: v.isoformat() if v else None  # noqa: E731
    lim = DETAIL_ROWS

    # 🔗 связи: со всеми, с кем были обмены ценностями, — в обе стороны
    links: dict[int, dict] = defaultdict(lambda: defaultdict(int))
    for key, field in (("help_in", "res_in"), ("help_out", "res_out"), ("tr_in", "coins_in"), ("tr_out", "coins_out"),
                       ("market_pairs", "trades"), ("swap_pairs", "swaps"), ("raid_wins_vs", "raids_won"),
                       ("raid_losses_to", "raids_lost")):
        for cp, v in f.get(key, {}).items():
            links[cp][field] += v
    for cp, (t, w) in f.get("duel_pairs", {}).items():
        links[cp]["duels"] += t
        links[cp]["duel_wins"] += w
    link_rows = []
    for cp, d in links.items():
        cu = users.get(cp)
        weight = d["res_in"] + d["res_out"] + (d["coins_in"] + d["coins_out"]) / 10 + 30 * (d["trades"] + d["swaps"] + d["duels"]
                                                                                         + d["raids_won"] + d["raids_lost"])
        link_rows.append({"id": cp, "name": name(cp), "blocked": bool(cu and cu["is_blocked"]),
                          "referral": bool(cu and cu["referred_by"] == user_id), "referrer": u["referred_by"] == cp,
                          "same_team": bool(cu and cu["team_id"] and cu["team_id"] == u["team_id"]), **d, "weight": int(weight)})
    link_rows.sort(key=lambda r: -r["weight"])

    async def rows(sql, *args):
        return [dict(r) for r in await conn.fetch(sql, *args)]

    coins = await rows("SELECT created_at, delta, reason, ref FROM ledger WHERE user_id = $1 AND created_at >= $2 "
                       "ORDER BY id DESC LIMIT $3", user_id, since, lim)
    coin_sum = await rows("SELECT reason, SUM(delta)::bigint AS total, COUNT(*) AS n FROM ledger WHERE user_id = $1 "
                          "AND created_at >= $2 GROUP BY 1 ORDER BY ABS(SUM(delta)) DESC", user_id, since)
    res = await rows("SELECT created_at, kind, delta, reason, ref FROM resource_ledger WHERE user_id = $1 AND created_at >= $2 "
                     "ORDER BY id DESC LIMIT $3", user_id, since, lim)
    res_sum = await rows("SELECT kind, reason, SUM(delta)::bigint AS total, COUNT(*) AS n FROM resource_ledger WHERE user_id = $1 "
                         "AND created_at >= $2 GROUP BY 1, 2 ORDER BY ABS(SUM(delta)) DESC", user_id, since)
    gifts = await rows(
        """SELECT g.created_at, g.kind, -g.delta AS qty, 'out' AS dir, h.user_id AS cp FROM resource_ledger g
             JOIN team_help h ON g.ref ~ '^[0-9]+$' AND h.id = g.ref::bigint
           WHERE g.user_id = $1 AND g.reason = 'team_help_give' AND g.created_at >= $2
           UNION ALL
           SELECT g.created_at, g.kind, -g.delta AS qty, 'in' AS dir, g.user_id AS cp FROM resource_ledger g
             JOIN team_help h ON g.ref ~ '^[0-9]+$' AND h.id = g.ref::bigint
           WHERE h.user_id = $1 AND g.reason = 'team_help_give' AND g.created_at >= $2
           ORDER BY created_at DESC LIMIT $3""", user_id, since, lim)
    transfers = await rows("SELECT created_at, delta, reason, ref FROM ledger WHERE user_id = $1 AND created_at >= $2 "
                           "AND reason IN ('transfer_in', 'transfer_out') ORDER BY id DESC LIMIT $3", user_id, since, lim)
    market = await rows("SELECT created_at, asset, qty, price, buyer_id, seller_id FROM market_trades WHERE created_at >= $2 "
                        "AND (buyer_id = $1 OR seller_id = $1) ORDER BY id DESC LIMIT $3", user_id, since, lim)
    swaps = await rows("SELECT created_at, maker_id, taker_id, give_kind, give_qty, want_kind, want_qty, status FROM resource_swaps "
                       "WHERE created_at >= $2 AND (maker_id = $1 OR taker_id = $1) ORDER BY id DESC LIMIT $3", user_id, since, lim)
    raids = await rows("SELECT created_at, attacker_id, defender_id, result, loot::text AS loot, is_revenge FROM raids "
                       "WHERE created_at >= $2 AND (attacker_id = $1 OR defender_id = $1) ORDER BY id DESC LIMIT $3",
                       user_id, since, lim)
    duels = await rows("SELECT finished_at AS created_at, stake, player1, player2, winner_id, status FROM duels "
                       "WHERE COALESCE(finished_at, created_at) >= $2 AND (player1 = $1 OR player2 = $1) "
                       "ORDER BY duel_id DESC LIMIT $3", user_id, since, lim)
    games = await rows(
        """SELECT created_at::date AS day, SPLIT_PART(reason, ':', 2) AS game, COUNT(*) AS wins, SUM(delta)::bigint AS coins
           FROM ledger WHERE user_id = $1 AND reason LIKE 'game_win:%' AND created_at >= $2 GROUP BY 1, 2 ORDER BY 1 DESC, 2""",
        user_id, since)
    rounds = await rows("SELECT created_at::date AS day, game, COUNT(*) AS n FROM game_rounds WHERE user_id = $1 "
                        "AND created_at >= $2 GROUP BY 1, 2 ORDER BY 1 DESC, 2", user_id, since)
    hours = await rows(
        """SELECT d AS day, COUNT(DISTINCT h) AS hours FROM (
             SELECT created_at::date AS d, EXTRACT(HOUR FROM created_at) AS h FROM events WHERE user_id = $1 AND created_at >= $2
             UNION ALL SELECT created_at::date, EXTRACT(HOUR FROM created_at) FROM game_rounds WHERE user_id = $1 AND created_at >= $2
           ) x GROUP BY 1 ORDER BY 1 DESC""", user_id, since)
    exps = await rows(
        """SELECT e.created_at, e.status, e.mode, e.cargo, e.departed_at, e.arrive_at, t.title FROM expedition_members m
             JOIN expeditions e ON e.id = m.expedition_id LEFT JOIN expedition_targets t ON t.id = e.target_id
           WHERE m.user_id = $1 AND e.created_at >= $2
           UNION
           SELECT e.created_at, e.status, e.mode, e.cargo, e.departed_at, e.arrive_at, t.title FROM expeditions e
             LEFT JOIN expedition_targets t ON t.id = e.target_id WHERE e.user_id = $1 AND e.created_at >= $2
           ORDER BY created_at DESC LIMIT $3""", user_id, since, lim)
    pays = await rows("SELECT created_at, item_payload, stars_amount, refunded_at FROM star_payments WHERE user_id = $1 "
                      "ORDER BY id DESC LIMIT $2", user_id, lim)
    refs = [{"id": x["user_id"], "name": label(x, x["user_id"]), "created_at": x["created_at"], "qualified_at": x["qualified_at"],
             "last_seen_at": x["last_seen_at"], "blocked": x["is_blocked"], "quiz": x["quiz_level"],
             "feeds": x["user_id"] in f.get("own_ref_feeders", []), "abandoned": x["user_id"] in f.get("abandoned_ids", [])}
            for x in users.values() if x["referred_by"] == user_id]
    refs.sort(key=lambda r: r["created_at"], reverse=True)
    gear = await rows("SELECT created_at, suit, slot, level, delta, reason, ref FROM gear_ledger WHERE user_id = $1 "
                      "AND created_at >= $2 ORDER BY id DESC LIMIT $3", user_id, since, lim)
    grants = await rows("SELECT created_at, ref, payload::text AS payload FROM reward_grants WHERE user_id = $1 "
                        "AND created_at >= $2 ORDER BY created_at DESC LIMIT $3", user_id, since, lim)

    cp_ids = set()
    for r in gifts:
        cp_ids.add(r["cp"])
    for r in market:
        cp_ids |= {r["buyer_id"], r["seller_id"]}
    for r in swaps:
        cp_ids |= {r["maker_id"], r["taker_id"]}
    for r in raids:
        cp_ids |= {r["attacker_id"], r["defender_id"]}
    for r in duels:
        cp_ids |= {r["player1"], r["player2"]}
    for r in transfers:
        if (r["ref"] or "").isdigit():
            cp_ids.add(int(r["ref"]))
    cp_ids |= {r["id"] for r in link_rows} | {x for sg in sigs for x in sg["links"]} | {r["id"] for r in refs}
    cp_ids.add(u["referred_by"])
    names = {str(c): name(c) for c in cp_ids if c}

    def ser(rs):
        return [{k: (iso(v) if isinstance(v, datetime) else v.isoformat() if hasattr(v, "isoformat") else v) for k, v in r.items()}
                for r in rs]

    score = sum(s["points"] for s in sigs)
    return {
        "id": user_id, "name": label(u, user_id), "score": score, "level": level_of(score), "signals": sigs,
        "profile": {"created_at": iso(u["created_at"]), "last_seen_at": iso(u["last_seen_at"]), "blocked": u["is_blocked"],
                    "team": team, "balance": u["balance"], "quiz": u["quiz_level"], "bonus_claims": u["bonus_claims"],
                    "qualified_at": iso(u["qualified_at"]), "referrer": u["referred_by"] and name(u["referred_by"]),
                    "referrer_id": u["referred_by"], "thin": f.get("thin", False)},
        "reviewed": rv and {"score": rv["score"], "note": rv["note"], "at": iso(rv["reviewed_at"])},
        "window_days": ABUSE_WINDOW_DAYS, "names": names,
        "links": link_rows[:100],
        "coins": ser(coins), "coin_sum": ser(coin_sum), "resources": ser(res), "res_sum": ser(res_sum), "gifts": ser(gifts),
        "transfers": ser(transfers), "market": ser(market), "swaps": ser(swaps), "raids": ser(raids), "duels": ser(duels),
        "games": ser(games), "rounds": ser(rounds), "hours": ser(hours), "expeditions": ser(exps), "payments": ser(pays),
        "referrals": ser(refs), "gear": ser(gear), "grants": ser(grants),
    }
