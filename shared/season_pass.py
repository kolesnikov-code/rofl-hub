"""
🎟 Пропуск сезона (решение владельца 30.10: «да» — бесплатная и платная дорожка, эксклюзивный костюм сезона).

Сезон = календарный месяц UTC (как ТОП). Опыт пропуска копится за события игры (shared/trophies.record → add_xp):
победы, дуэли, налёты, походы, изделия, открытия, квесты, сундук. PASS_LEVELS уровней по PASS_XP_PER_LEVEL опыта.
Бесплатная дорожка — монеты и немного ресурсов; платная (PASS_STARS ★, покупка «seasonpass_<ГГГГММ>») — больше монет,
котлеты и ЭКСКЛЮЗИВНЫЕ скины сезона (рамка, титул, маркер, костюм на 30-м уровне), которые никогда не продаются:
кончился месяц — такой скин больше не получить. Купить пропуск можно и посреди сезона: открываются все уже пройденные
уровни платной дорожки. Награды забираются кнопкой; выдача — shared/prizes.grant (ключ PASS<сезон>_<дорожка><уровень>).
"""
from __future__ import annotations

from datetime import datetime, timedelta

from shared.economy import season_bounds, season_key, utcnow

PASS_LEVELS = 30
PASS_XP_PER_LEVEL = 100
PASS_STARS = 299
PASS_FIRST = "2026-11"         # первый сезон с эксклюзивными скинами: более ранние пропуска не продаются
PASS_EARLY_DAYS = 7            # за неделю до сезона пропуск следующего месяца уже можно купить
PASS_XP = {"game_win": 5, "duel": 5, "duel_win": 10, "raid": 8, "raid_win": 12, "raid_def": 4, "expedition": 30,
           "craft": 10, "tech": 40, "quest": 40, "chest": 30}
# Опыт за победы в играх — не больше PASS_GAME_XP_DAILY в сутки UTC (владелец 30.10: «больше вовлечённости»): одними играми
# 30-й уровень — за 20 дней; с купленным безлимитом на 30 дней — PASS_GAME_XP_DAILY_MONTHLY (за 10 дней). Суточный безлимит
# лимит опыта не поднимает (решение владельца). Остальные события не ограничены.
PASS_GAME_XP_DAILY = 150
PASS_GAME_XP_DAILY_MONTHLY = 300
PASS_MONTHLY_SKU = "unlimit_30d"
PASS_DAILY_CAPPED = ("game_win",)

# Темы сезонов по месяцам: название, цвета и эффект эксклюзивных скинов пропуска (никогда не продаются)
PASS_THEMES = {
    1: ("Ледяной патруль", "Ice Patrol", "#bfe9ff", "#3a7bd5", "shimmer", "❄️"),
    2: ("Алая вьюга", "Crimson Blizzard", "#ff6b6b", "#ffd1dc", "aurora", "🌹"),
    3: ("Первая оттепель", "First Thaw", "#9cff8a", "#2bb5a0", "pulse", "🌱"),
    4: ("Звёздный рейс", "Star Run", "#ffe27a", "#5a2bff", "shimmer", "🛰"),
    5: ("Майский гром", "May Thunder", "#7df9ff", "#7b2ff7", "flame", "⚡"),
    6: ("Пустынный ветер", "Desert Wind", "#ffcf7a", "#c2571a", "aurora", "🏜"),
    7: ("Глубина", "The Deep", "#38f9d7", "#1e3c72", "pulse", "🐙"),
    8: ("Неоновая ночь", "Neon Night", "#ff4d8d", "#00ffe1", "aurora", "🌃"),
    9: ("Кибер-урожай", "Cyber Harvest", "#ffb43a", "#6b8e23", "shimmer", "🌾"),
    10: ("Тыквенный сбой", "Pumpkin Glitch", "#ff8a00", "#3d0066", "flame", "🎃"),
    11: ("Полярная вахта", "Polar Watch", "#e8f7ff", "#2bffb1", "aurora", "🧊"),
    12: ("Гирлянда", "Garland", "#ff3d6e", "#ffd23f", "pulse", "🎄"),
}


def _theme(season: str):
    return PASS_THEMES[int(season[5:7])]


def pass_skin_ids(season: str) -> dict[str, str]:
    """Эксклюзивные скины пропуска сезона: {"frame": id, "title": id, "marker": id, "suit": id}."""
    code = season.replace("-", "")
    return {t: f"ps{code}_{t}" for t in ("frame", "title", "marker", "suit")}


def pass_skins(season: str) -> dict[str, dict]:
    """Описания скинов пропуска для каталога shared/skins.SKINS (генерируются по теме месяца)."""
    ru, en, c1, c2, fx, emoji = _theme(season)
    ids = pass_skin_ids(season)
    mark = f" · {season[5:7]}.{season[:4]}"
    base = {"set": "pass_" + season, "stars": None, "edition": None, "pass": season}
    return {
        ids["frame"]: {**base, "target": "frame", "rarity": "epic", "look": {"c1": c1, "c2": c2, "fx": fx},
                       "name": f"Рамка «{ru}»{mark}", "name_en": f"{en} frame{mark}"},
        ids["title"]: {**base, "target": "title", "rarity": "epic", "look": {"c1": c1, "c2": c2, "fx": "shimmer"},
                       "name": f"Титул «{ru}»{mark}", "name_en": f"{en} title{mark}", "text": ru, "text_en": en},
        ids["marker"]: {**base, "target": "marker", "rarity": "rare", "look": {"c1": c1, "c2": c2, "fx": "pulse", "emoji": emoji},
                        "name": f"Маркер «{ru}»{mark}", "name_en": f"{en} marker{mark}"},
        ids["suit"]: {**base, "target": "suit", "rarity": "legendary", "look": {"c1": c1, "c2": c2, "fx": fx},
                      "name": f"Костюм «{ru}»{mark}", "name_en": f"{en} suit{mark}"},
    }


def rewards(season: str, track: str, level: int) -> list[dict]:
    """Награда уровня на дорожке (free / paid) — в формате shared/prizes."""
    ids = pass_skin_ids(season)
    if track == "free":
        out = [{"kind": "coins", "amount": 20 + level * 4}]
        if level % 5 == 0:
            out.append({"kind": "resource", "res": "battery", "qty": 1})
        if level == PASS_LEVELS:
            out.append({"kind": "cutlets", "qty": 2})
        return out
    out = [{"kind": "coins", "amount": 40 + level * 8}]
    special = {5: {"kind": "skin", "skin": ids["marker"]}, 10: {"kind": "skin", "skin": ids["frame"]},
               20: {"kind": "skin", "skin": ids["title"]}, PASS_LEVELS: {"kind": "skin", "skin": ids["suit"]}}
    if level in special:
        out.append(special[level])
    elif level % 3 == 0:
        out.append({"kind": "cutlets", "qty": 1})
    if level in (15, 25):
        out.append({"kind": "resource", "res": "battery", "qty": 3})
    return out


def pass_level(xp: int) -> int:
    return min(PASS_LEVELS, xp // PASS_XP_PER_LEVEL)


def current_season(now: datetime) -> str:
    return season_key(now)


def active_season(now: datetime) -> str:
    """Сезон пропуска в приложении: текущий, но не раньше PASS_FIRST (до старта — показываем первый)."""
    return max(current_season(now), PASS_FIRST)


def season_end(season: str) -> datetime:
    """Конец сезона «ГГГГ-ММ» (UTC)."""
    from datetime import timezone
    return season_bounds(datetime(int(season[:4]), int(season[5:7]), 2, tzinfo=timezone.utc))[1]


def sale_season(now: datetime) -> str:
    """Какой пропуск продаётся: текущего месяца, а в последние PASS_EARLY_DAYS дней — уже следующего."""
    _, end = season_bounds(now)
    sale = season_key(end + timedelta(hours=1)) if end - now <= timedelta(days=PASS_EARLY_DAYS) else season_key(now)
    return max(sale, PASS_FIRST)


def pass_sku(season: str) -> str:
    return "seasonpass_" + season.replace("-", "")


def season_of_sku(sku: str) -> str | None:
    code = sku[len("seasonpass_"):] if sku.startswith("seasonpass_") else ""
    return f"{code[:4]}-{code[4:6]}" if len(code) == 6 and code.isdigit() and 1 <= int(code[4:6]) <= 12 else None


def can_buy(season: str, now: datetime) -> bool:
    return season >= PASS_FIRST and season in (season_key(now), sale_season(now))


async def add_xp(conn, user_id: int, event: str, n: int = 1) -> None:
    gain = PASS_XP.get(event, 0) * n
    if gain <= 0:
        return
    now = utcnow()
    season = active_season(now)   # до PASS_FIRST опыт копится в первый пропуск — тот, что виден на экране
    if event not in PASS_DAILY_CAPPED:
        await conn.execute(
            "INSERT INTO season_pass (user_id, season, xp) VALUES ($1, $2, $3) "
            "ON CONFLICT (user_id, season) DO UPDATE SET xp = season_pass.xp + EXCLUDED.xp", user_id, season, gain)
        return
    today = now.date()
    await conn.execute("INSERT INTO season_pass (user_id, season) VALUES ($1, $2) ON CONFLICT DO NOTHING", user_id, season)
    row = await conn.fetchrow("SELECT game_day, game_xp FROM season_pass WHERE user_id = $1 AND season = $2 FOR UPDATE",
                              user_id, season)
    used = game_xp_today(row, now)
    gain = min(gain, await game_xp_cap(conn, user_id, now) - used)
    if gain <= 0:
        return
    await conn.execute("UPDATE season_pass SET xp = xp + $3, game_day = $4, game_xp = $5 WHERE user_id = $1 AND season = $2",
                       user_id, season, gain, today, used + gain)


async def has_monthly_unlimit(conn, user_id: int, now: datetime) -> bool:
    """Безлимит действует и куплен месячным тарифом за ★ в последние 30 дней (без возвратов и тест-чеков)."""
    until = await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = $1", user_id)
    if not until or until <= now:
        return False
    return bool(await conn.fetchval(
        "SELECT 1 FROM star_payments WHERE user_id = $1 AND item_payload = $2 AND stars_amount > 0 AND refunded_at IS NULL "
        "AND telegram_charge_id NOT LIKE 'TEST%' AND created_at >= $3 LIMIT 1",
        user_id, PASS_MONTHLY_SKU, now - timedelta(days=30)))


async def game_xp_cap(conn, user_id: int, now: datetime) -> int:
    return PASS_GAME_XP_DAILY_MONTHLY if await has_monthly_unlimit(conn, user_id, now) else PASS_GAME_XP_DAILY


def game_xp_today(row, now: datetime) -> int:
    """Сколько опыта за победы в играх уже набрано сегодня (UTC)."""
    return row["game_xp"] if row and row["game_day"] == now.date() else 0


async def state(conn, user_id: int, season: str) -> dict:
    row = await conn.fetchrow("SELECT xp, premium, claimed_free, claimed_paid, game_day, game_xp FROM season_pass "
                              "WHERE user_id = $1 AND season = $2", user_id, season)
    xp = row["xp"] if row else 0
    return {"season": season, "xp": xp, "level": pass_level(xp), "premium": bool(row and row["premium"]),
            "game_xp_today": game_xp_today(row, utcnow()), "game_xp_cap": await game_xp_cap(conn, user_id, utcnow()),
            "game_xp_cap_monthly": PASS_GAME_XP_DAILY_MONTHLY,
            "claimed_free": list(row["claimed_free"]) if row else [], "claimed_paid": list(row["claimed_paid"]) if row else []}


class PassError(Exception):
    def __init__(self, key: str):
        self.key = key
        super().__init__(key)


async def claim(conn, user_id: int, season: str, now: datetime) -> list[dict]:
    """Забрать все открытые награды сезона (обе дорожки). Возвращает выданное."""
    from shared.prizes import grant
    st = await state(conn, user_id, season)
    got = []
    for track, claimed in (("free", st["claimed_free"]), ("paid", st["claimed_paid"])):
        if track == "paid" and not st["premium"]:
            continue
        for level in range(1, st["level"] + 1):
            if level in claimed:
                continue
            items = rewards(season, track, level)
            await grant(conn, user_id, items, f"PASS{season}_{track[0].upper()}{level}", now)
            column = "claimed_free" if track == "free" else "claimed_paid"
            await conn.execute(f"UPDATE season_pass SET {column} = array_append({column}, $3) "
                               "WHERE user_id = $1 AND season = $2", user_id, season, level)
            got += items
    if not got:
        raise PassError("pass.err_nothing")
    return got


async def activate_premium(conn, user_id: int, season: str) -> None:
    """Доставка оплаченного пропуска (shared/delivery)."""
    if await conn.fetchval("SELECT premium FROM season_pass WHERE user_id = $1 AND season = $2", user_id, season):
        raise PassError("pass.err_owned")
    await conn.execute("INSERT INTO season_pass (user_id, season, premium) VALUES ($1, $2, TRUE) "
                       "ON CONFLICT (user_id, season) DO UPDATE SET premium = TRUE", user_id, season)
