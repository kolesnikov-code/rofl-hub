"""
Админ-операции над базой (Блок 4): блокировка, подарки монет, суточный отчёт.

Без Telegram — только asyncpg-соединение/пул. Используется админ-ботом.
"""
from __future__ import annotations

import logging

from shared.ledger import change_balance

logger = logging.getLogger(__name__)


async def set_user_blocked(conn, user_id: int, blocked: bool) -> bool:
    """Ставит/снимает блокировку. False — игрок не найден."""
    result = await conn.execute("UPDATE users SET is_blocked = $2 WHERE user_id = $1", user_id, blocked)
    changed = result.endswith("1")
    if changed:
        logger.info("[ADMIN_BLOCK] user=%s blocked=%s", user_id, blocked)
    return changed


async def admin_gift_coins(conn, user_id: int, amount: int, admin_id: int) -> int:
    """Дарит (или списывает при amount<0) рофлы от имени администрации. Возвращает новый баланс."""
    if amount == 0:
        raise ValueError("amount must be non-zero")
    return await change_balance(conn, user_id, amount, "admin_gift", str(admin_id))


async def collect_daily_report(conn) -> dict:
    """Суточный отчёт: DAU, регистрации, продажи и когорты трат за 30 дней."""
    base = await conn.fetchrow(
        """
        SELECT
            (SELECT COUNT(*) FROM users)                                                        AS total_users,
            (SELECT COUNT(*) FROM users WHERE last_seen_at >= NOW() - INTERVAL '24 hours')      AS dau,
            (SELECT COUNT(*) FROM users WHERE created_at   >= NOW() - INTERVAL '24 hours')      AS new_users_24h,
            (SELECT COUNT(*) FROM users WHERE is_blocked)                                       AS blocked_users,
            (SELECT COALESCE(SUM(balance), 0) FROM users)                                       AS coins_mass,
            (SELECT COUNT(*) FROM teams)                                                        AS teams_count,
            (SELECT COUNT(*) FROM miners WHERE expires_at > NOW())                              AS active_miners,
            (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments)                          AS stars_total,
            (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments
              WHERE created_at >= NOW() - INTERVAL '24 hours')                                  AS stars_24h,
            (SELECT COUNT(*) FROM star_payments
              WHERE created_at >= NOW() - INTERVAL '24 hours')                                  AS payments_24h,
            (SELECT COALESCE(SUM(games_played), 0) FROM game_stats)                             AS games_played,
            (SELECT COALESCE(SUM(games_won), 0) FROM game_stats)                                AS games_won
        """
    )
    cohorts = await conn.fetchrow(
        """
        WITH spend_30d AS (
            SELECT user_id, SUM(stars_amount) AS spent
            FROM star_payments
            WHERE created_at >= NOW() - INTERVAL '30 days'
            GROUP BY user_id
        )
        SELECT
            COUNT(*) FILTER (WHERE spent > 0   AND spent <= 100) AS light,
            COUNT(*) FILTER (WHERE spent > 100 AND spent <= 500) AS normal,
            COUNT(*) FILTER (WHERE spent > 500)                  AS whale
        FROM spend_30d
        """
    )
    report = dict(base)
    report["cohort_light"] = cohorts["light"] or 0
    report["cohort_normal"] = cohorts["normal"] or 0
    report["cohort_whale"] = cohorts["whale"] or 0
    report["cohort_f2p"] = max(
        0, report["total_users"] - report["cohort_light"] - report["cohort_normal"] - report["cohort_whale"])
    return report


def format_daily_report(r: dict) -> str:
    """HTML-текст отчёта для Тайной Комнаты админа."""
    return (
        "👑 <b>СУТОЧНЫЙ ОТЧЁТ ХОЛДИНГА ROFL HUB</b>\n"
        "..................................................\n\n"
        f"👥 Игроков всего: <b>{r['total_users']}</b> (заблокировано: {r['blocked_users']})\n"
        f"🔥 DAU (актив за 24ч): <b>{r['dau']}</b>\n"
        f"🆕 Новых регистраций за 24ч: <b>{r['new_users_24h']}</b>\n"
        f"🏆 Команд и кланов: <b>{r['teams_count']}</b>\n"
        f"🤖 Живых роботов на фермах: <b>{r['active_miners']}</b>\n\n"
        f"💵 <b>ПРОДАЖИ:</b>\n"
        f"• За 24ч: <b>★ {r['stars_24h']}</b> ({r['payments_24h']} платежей)\n"
        f"• За всё время: <b>★ {r['stars_total']}</b>\n\n"
        f"📊 <b>КОГОРТЫ ТРАТ ЗА 30 ДНЕЙ:</b>\n"
        f"🛑 F2P (0 ★): <code>{r['cohort_f2p']}</code>\n"
        f"🪵 Микро (1–100 ★): <b>{r['cohort_light']}</b>\n"
        f"⚡ Нормы (101–500 ★): <b>{r['cohort_normal']}</b>\n"
        f"👑 Киты (500+ ★): <u>{r['cohort_whale']}</u>\n\n"
        f"🎮 Раундов сыграно: <code>{r['games_played']}</code> · побед: <code>{r['games_won']}</code>\n"
        f"🪙 Масса рофлов в обороте: <code>{r['coins_mass']}</code>\n"
        "..................................................\n"
        "<i>⚙️ Отчёт собран по живым данным СУБД на момент запроса.</i>"
    )
