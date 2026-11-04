"""
Админ-операции над базой: блокировка, подарки монет, суточный отчёт,
бэкап всех таблиц в JSON и учёт возвратов Stars.

Без Telegram — только asyncpg-соединение/пул. Используется админ-ботом.
"""
from __future__ import annotations

import json
import logging
from datetime import date, datetime

from shared.economy import utcnow
from shared.ledger import change_balance

logger = logging.getLogger(__name__)

# Полный список таблиц проекта для бэкапа (порядок = порядок в файле)
BACKUP_TABLES = ("users", "teams", "miners", "game_stats", "star_payments", "auctions", "ledger")


async def set_user_blocked(conn, user_id: int, blocked: bool) -> bool:
    """Ставит/снимает блокировку. False — игрок не найден."""
    result = await conn.execute("UPDATE users SET is_blocked = $2 WHERE user_id = $1", user_id, blocked)
    changed = result.endswith("1")
    if changed:
        logger.info("[ADMIN_BLOCK] user=%s blocked=%s", user_id, blocked)
    return changed


async def admin_gift_coins(conn, user_id: int, amount: int, admin_id: int) -> int:
    """Дарит (или списывает при amount<0) монеты от имени администрации. Возвращает новый баланс."""
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
            (SELECT COUNT(*) FROM users WHERE deletion_requested_at IS NOT NULL)                AS deletion_pending,
            (SELECT COUNT(*) FROM users WHERE deleted_at >= NOW() - INTERVAL '24 hours')        AS deleted_24h,
            (SELECT COALESCE(SUM(balance), 0) FROM users)                                       AS coins_mass,
            (SELECT COUNT(*) FROM teams)                                                        AS teams_count,
            (SELECT COUNT(*) FROM miners WHERE expires_at > NOW())                              AS active_miners,
            (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments)                          AS stars_total,
            (SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments
              WHERE created_at >= NOW() - INTERVAL '24 hours')                                  AS stars_24h,
            (SELECT COUNT(*) FROM star_payments
              WHERE created_at >= NOW() - INTERVAL '24 hours' AND stars_amount > 0)             AS payments_24h,
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


def _jsonable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


async def dump_database(conn) -> dict:
    """Снимок всех таблиц проекта: {'generated_at': ..., 'tables': {имя: [строки]}}."""
    dump: dict = {"generated_at": utcnow().isoformat(), "tables": {}}
    for table in BACKUP_TABLES:
        rows = await conn.fetch(f"SELECT * FROM {table}")
        dump["tables"][table] = [{k: _jsonable(v) for k, v in dict(r).items()} for r in rows]
    logger.info("[BACKUP] снято таблиц: %s, строк: %s",
                len(BACKUP_TABLES), sum(len(v) for v in dump["tables"].values()))
    return dump


def backup_to_json_bytes(dump: dict) -> bytes:
    """JSON-файл бэкапа (utf-8, читаемый человеком)."""
    return json.dumps(dump, ensure_ascii=False, indent=1).encode("utf-8")


async def find_payment(conn, charge_id: str):
    return await conn.fetchrow(
        "SELECT * FROM star_payments WHERE telegram_charge_id = $1", charge_id)


async def mark_refunded(conn, charge_id: str) -> bool:
    """Помечает платёж возвращённым. False — платёж не найден или уже возвращён."""
    result = await conn.execute(
        "UPDATE star_payments SET refunded_at = NOW() "
        "WHERE telegram_charge_id = $1 AND refunded_at IS NULL", charge_id)
    return result.endswith("1")


def format_daily_report(r: dict) -> str:
    """HTML-текст отчёта для Тайной Комнаты админа."""
    return (
        "👑 <b>СУТОЧНЫЙ ОТЧЁТ ХОЛДИНГА BOT BARONS</b>\n"
        "..................................................\n"
        f"👥 Игроков всего: <b>{r['total_users']}</b> (заблокировано: {r['blocked_users']})\n"
        f"🔥 DAU (актив за 24ч): <b>{r['dau']}</b>\n"
        f"🆕 Новых регистраций за 24ч: <b>{r['new_users_24h']}</b>\n"
        f"🗑 Удалили аккаунт за 24ч: <b>{r.get('deleted_24h', 0)}</b> (в очереди: {r.get('deletion_pending', 0)})\n"
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
        f"🪙 Масса монет в обороте: <code>{r['coins_mass']}</code>\n"
        "..................................................\n"
        "<i>⚙️ Отчёт собран по живым данным СУБД на момент запроса.</i>"
    )
