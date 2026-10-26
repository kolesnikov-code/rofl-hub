"""
Middleware главного бота (Блок 4):
- заблокированные игроки (users.is_blocked) не получают ответов бота;
- аккаунт в очереди на удаление ЗАМОРОЖЕН: на любой апдейт — напоминание и кнопка отмены;
  удалённый (обезличенный) — только /start, он заводит профиль заново без бонусов;
- last_seen_at обновляется на ЛЮБОЕ действие (для честного DAU в админ-отчёте),
  с троттлингом записи раз в 5 минут на игрока, чтобы не грузить базу.

Отказоустойчивость: любой сбой БД внутри middleware не роняет обработку апдейта.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from shared.analytics import mark_daily_activity
from shared.database import db
from shared.feature_flags import get_flag
from shared.locales import resolve_lang, t

logger = logging.getLogger(__name__)

LAST_SEEN_WRITE_INTERVAL = 300   # секунд между записями last_seen_at одного игрока
BLOCK_NOTICE_INTERVAL = 300      # как часто напоминать заблокированному о блокировке


def _is_callback(event: TelegramObject, data: str) -> bool:
    callback = getattr(event, "callback_query", None)
    return isinstance(callback, CallbackQuery) and callback.data == data


def _is_start(event: TelegramObject) -> bool:
    message = getattr(event, "message", None)
    return isinstance(message, Message) and (message.text or "").startswith("/start")


def _is_paid(event: TelegramObject) -> bool:
    """Оплата уже прошла (Stars списаны) — такой апдейт нельзя глушить ни техработами, ни блокировкой:
    доставка или авто-возврат обязаны сработать. pre_checkout по-прежнему глушится — там деньги ещё не взяты."""
    message = getattr(event, "message", None)
    return isinstance(message, Message) and message.successful_payment is not None


class ActivityMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._last_seen_written: dict[int, float] = {}
        self._block_notified: dict[int, float] = {}
        self._maintenance_notified: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None or not db.is_connected:
            if user is not None:
                data["user_lang"] = resolve_lang(getattr(user, "language_code", None))
            return await handler(event, data)

        now = time.monotonic()
        # Язык по умолчанию — из клиента Telegram (до регистрации), после — из профиля
        data["user_lang"] = resolve_lang(getattr(user, "language_code", None))

        if _is_paid(event):
            try:
                row = await db.pool.fetchrow("SELECT lang FROM users WHERE user_id = $1", user.id)
                if row:
                    data["user_lang"] = resolve_lang(row["lang"])
            except Exception:
                logger.exception("[ACTIVITY_MW] язык для оплаты не прочитан — доставка всё равно идёт")
            return await handler(event, data)

        # 🛠 Режим техработ (тумблер владельца в админ-боте): бот отвечает заглушкой
        try:
            if await get_flag("maintenance"):
                if now - self._maintenance_notified.get(user.id, 0.0) >= 60:
                    self._maintenance_notified[user.id] = now
                    await self._reply_to_event(event, t(data["user_lang"], "common.maintenance"))
                return None
        except Exception:
            logger.exception("[ACTIVITY_MW] сбой проверки maintenance — пускаю апдейт")

        try:
            row = await db.pool.fetchrow(
                "SELECT is_blocked, lang, deletion_requested_at, deleted_at FROM users WHERE user_id = $1",
                user.id)
            if row:
                data["user_lang"] = resolve_lang(row["lang"])

            if row and row["is_blocked"]:
                await self._notify_blocked(event, user.id, now, data["user_lang"])
                return None  # апдейт не доходит до обработчиков

            if row and row["deletion_requested_at"] is not None and not _is_callback(event, "acct_undo"):
                await self._notify_pending_deletion(event, data["user_lang"], row["deletion_requested_at"])
                return None
            if row and row["deleted_at"] is not None and not _is_start(event):
                await self._reply_to_event(event, t(data["user_lang"], "acct.deleted_notice"))
                return None

            if row and now - self._last_seen_written.get(user.id, 0.0) >= LAST_SEEN_WRITE_INTERVAL:
                self._last_seen_written[user.id] = now
                await db.pool.execute(
                    "UPDATE users SET last_seen_at = NOW() WHERE user_id = $1", user.id)
            if row:
                # База DAU/WAU/MAU/retention; сама глотает ошибки и кэширует «уже отмечен»
                await mark_daily_activity(user.id)
        except Exception:
            logger.exception("[ACTIVITY_MW] сбой middleware, апдейт пропущен дальше")

        return await handler(event, data)

    @staticmethod
    async def _reply_to_event(event: TelegramObject, text: str) -> None:
        """Отвечает на апдейт (message или callback) переданным текстом. Сбои глотает."""
        try:
            update = event  # на dp.update событие — Update
            if isinstance(getattr(update, "callback_query", None), CallbackQuery):
                await update.callback_query.answer(text, show_alert=True)
            elif isinstance(getattr(update, "message", None), Message):
                await update.message.answer(text)
        except Exception:
            pass

    @staticmethod
    async def _notify_pending_deletion(event: TelegramObject, lang: str, requested_at) -> None:
        """Напоминание о заморозке с кнопкой «Отменить удаление». Сбои глотает."""
        from bots.main_bot.handlers.account import pending_notice, undo_keyboard
        try:
            text = await pending_notice(lang, requested_at)
            callback = getattr(event, "callback_query", None)
            message = getattr(event, "message", None)
            if isinstance(callback, CallbackQuery):
                await callback.answer()
                if callback.message:
                    await callback.message.answer(text, reply_markup=undo_keyboard(lang), parse_mode="HTML")
            elif isinstance(message, Message):
                await message.answer(text, reply_markup=undo_keyboard(lang), parse_mode="HTML")
        except Exception:
            pass

    async def _notify_blocked(self, event: TelegramObject, user_id: int, now: float,
                              lang: str = "ru") -> None:
        if now - self._block_notified.get(user_id, 0.0) < BLOCK_NOTICE_INTERVAL:
            return
        self._block_notified[user_id] = now
        await self._reply_to_event(event, t(lang, "common.blocked"))
