"""
Удаление аккаунта по желанию игрока (решение владельца 26.10).

Жизненный цикл:
1. request_deletion() — игрок дважды подтвердил в /profile: users.deletion_requested_at = now,
   открытые ордера и обмены на бирже снимаются (эскроу возвращается), аккаунт ЗАМОРОЖЕН —
   middleware не пускает в игру, игрок пропадает из ТОПа и целей налётов.
2. cancel_deletion() — передумал в течение ACCOUNT_DELETE_GRACE_DAYS: всё как было.
3. purge_account() — после отсрочки (жнец account_reaper_loop): строка users ОБЕЗЛИЧИВАЕТСЯ
   на месте (username/имя/баланс/склад/роботы/прогресс/команда/VIP ID), users.deleted_at = now.
   Сохраняются только user_id, created_at, referred_by, qualified_at, bonus_claims, is_blocked:
   платежи Stars (star_payments) и ledger нужны для возвратов и споров, а «след» защищает
   от абуза «удалил → зашёл заново»: повторная регистрация (restore_account) НЕ даёт
   стартового бонуса, защиты новичка от налётов и повторной награды пригласившему.

Покупки за Stars (бусты, Безлимит, роботы) сгорают вместе с аккаунтом — игрок предупреждён.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from shared.economy import ACCOUNT_DELETE_GRACE_DAYS, RESOURCE_KINDS
from shared.ledger import change_balance

logger = logging.getLogger(__name__)


def deletion_due_at(requested_at: datetime) -> datetime:
    """Когда заявка на удаление будет исполнена."""
    return requested_at + timedelta(days=ACCOUNT_DELETE_GRACE_DAYS)


async def request_deletion(conn, user_id: int, now: datetime) -> datetime | None:
    """
    Ставит аккаунт в очередь на удаление (внутри транзакции вызывающего).
    Возвращает дату исполнения или None, если профиля нет / он уже удалён.
    Повторный запрос не сдвигает срок.
    """
    row = await conn.fetchrow(
        "SELECT deletion_requested_at, deleted_at FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not row or row["deleted_at"] is not None:
        return None
    requested = row["deletion_requested_at"]
    if requested is None:
        requested = now
        await conn.execute("UPDATE users SET deletion_requested_at = $2 WHERE user_id = $1", user_id, now)
        await _close_market(conn, user_id)
        logger.info("[ACCOUNT_DELETE] user=%s поставлен в очередь", user_id)
    return deletion_due_at(requested)


async def cancel_deletion(conn, user_id: int) -> bool:
    """Отменяет заявку. True — заявка была и снята."""
    result = await conn.execute(
        "UPDATE users SET deletion_requested_at = NULL "
        "WHERE user_id = $1 AND deletion_requested_at IS NOT NULL AND deleted_at IS NULL", user_id)
    return result.endswith(" 1")


async def _close_market(conn, user_id: int) -> None:
    """Снимает открытые ордера и обмены игрока, эскроу возвращается ему же."""
    from shared.market import cancel_order, cancel_swap
    for r in await conn.fetch(
            "SELECT id FROM market_orders WHERE seller_id = $1 AND status = 'open'", user_id):
        await cancel_order(conn, user_id, r["id"])
    for r in await conn.fetch(
            "SELECT id FROM resource_swaps WHERE maker_id = $1 AND status = 'open'", user_id):
        await cancel_swap(conn, user_id, r["id"])


async def purge_blocker(conn, user_id: int) -> str | None:
    """Что мешает удалить прямо сейчас (тогда жнец попробует позже)."""
    if await conn.fetchval(
            "SELECT 1 FROM auctions WHERE status = 'open' AND highest_bidder_id = $1 LIMIT 1", user_id):
        return "auction_leader"     # ставка-эскроу лидера: ждём закрытия аукциона
    if await conn.fetchval(
            "SELECT 1 FROM duels WHERE status IN ('waiting', 'active') AND $1 IN (player1, player2) LIMIT 1",
            user_id):
        return "duel"               # жнец дуэлей доиграет или вернёт ставку
    return None


async def due_for_purge(conn, now: datetime, limit: int = 100) -> list[int]:
    rows = await conn.fetch(
        """SELECT user_id FROM users
           WHERE deleted_at IS NULL AND deletion_requested_at IS NOT NULL
             AND deletion_requested_at <= $1::timestamptz - make_interval(days => $2::int)
           ORDER BY deletion_requested_at LIMIT $3""",
        now, ACCOUNT_DELETE_GRACE_DAYS, limit)
    return [r["user_id"] for r in rows]


async def purge_account(conn, user_id: int, now: datetime) -> bool:
    """
    Обезличивает аккаунт (внутри транзакции вызывающего). True — удалён сейчас.
    False — ещё не срок, заявку отменили, уже удалён или мешает аукцион/дуэль.
    """
    from shared.db_clans import leave_team
    from shared.resources import change_resource, get_resources

    row = await conn.fetchrow(
        "SELECT balance, deletion_requested_at, deleted_at FROM users WHERE user_id = $1 FOR UPDATE",
        user_id)
    if (not row or row["deleted_at"] is not None or row["deletion_requested_at"] is None
            or deletion_due_at(row["deletion_requested_at"]) > now):
        return False
    blocker = await purge_blocker(conn, user_id)
    if blocker:
        logger.info("[ACCOUNT_DELETE] user=%s отложен: %s", user_id, blocker)
        return False

    await _close_market(conn, user_id)        # на случай ордеров, открытых до заморозки
    await leave_team(conn, user_id)           # капитанство — старейшему участнику
    if row["balance"]:
        await change_balance(conn, user_id, -row["balance"], "account_deleted")
    for kind, qty in (await get_resources(conn, user_id)).items():
        if qty > 0 and kind in RESOURCE_KINDS:
            await change_resource(conn, user_id, kind, -qty, "account_deleted")
    await conn.execute("DELETE FROM miners WHERE user_id = $1", user_id)
    await conn.execute("DELETE FROM user_items WHERE user_id = $1", user_id)
    await conn.execute("DELETE FROM vip_aliases WHERE user_id = $1", user_id)
    await conn.execute("DELETE FROM game_stats WHERE user_id = $1", user_id)
    await conn.execute("DELETE FROM quest_progress WHERE user_id = $1", user_id)
    await conn.execute(
        """
        UPDATE users SET
            username = NULL, display_name = NULL,
            fridge_capacity = 1, fridge_cutlets = 0, inv_cutlets = 0, boost_level = 0,
            boost_nuclear_until = NULL, boost_nitrogen_until = NULL, drone_until = NULL,
            unlimit_until = NULL, mining_acc = 0,
            raid_shield_until = NULL, raid_stance = NULL, last_raid_at = NULL,
            has_shuttle = FALSE, farm_armor_level = 0, armor_until = NULL,
            goal_streak = 0, goal_last_claim = NULL, res_capacity = DEFAULT,
            intern_claimed = FALSE, interns_pending = 0,
            interns_backfilled = TRUE, interns_rebalanced = TRUE,
            team_id = NULL, team_joined_at = NULL,
            deletion_requested_at = NULL, deleted_at = $2
        WHERE user_id = $1
        """, user_id, now)
    logger.info("[ACCOUNT_DELETE] user=%s обезличен", user_id)
    return True


async def restore_account(conn, user_id: int, username: str | None, display_name: str | None,
                          lang: str | None = None) -> bool:
    """
    Игрок вернулся после удаления (/start): профиль оживает С НУЛЯ — без стартового
    бонуса, со старой датой регистрации (защита новичка не повторяется) и прежним
    referred_by/qualified_at (награда пригласившему не повторяется). True — восстановлен.
    """
    result = await conn.execute(
        "UPDATE users SET deleted_at = NULL, username = $2, display_name = $3, "
        "lang = COALESCE($4, lang), last_seen_at = NOW() "
        "WHERE user_id = $1 AND deleted_at IS NOT NULL",
        user_id, username, (display_name or "")[:128] or None, lang)
    if not result.endswith(" 1"):
        return False
    await conn.execute("INSERT INTO game_stats (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
    logger.info("[ACCOUNT_DELETE] user=%s вернулся", user_id)
    return True
