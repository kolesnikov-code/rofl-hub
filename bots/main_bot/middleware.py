"""
Middleware главного бота (Блок 4):
- заблокированные игроки (users.is_blocked) не получают ответов бота;
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

from shared.database import db

logger = logging.getLogger(__name__)

LAST_SEEN_WRITE_INTERVAL = 300   # секунд между записями last_seen_at одного игрока
BLOCK_NOTICE_INTERVAL = 300      # как часто напоминать заблокированному о блокировке


class ActivityMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._last_seen_written: dict[int, float] = {}
        self._block_notified: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None or not db.is_connected:
            return await handler(event, data)

        now = time.monotonic()
        try:
            is_blocked = await db.pool.fetchval(
                "SELECT is_blocked FROM users WHERE user_id = $1", user.id)

            if is_blocked:
                await self._notify_blocked(event, user.id, now)
                return None  # апдейт не доходит до обработчиков

            if now - self._last_seen_written.get(user.id, 0.0) >= LAST_SEEN_WRITE_INTERVAL:
                self._last_seen_written[user.id] = now
                await db.pool.execute(
                    "UPDATE users SET last_seen_at = NOW() WHERE user_id = $1", user.id)
        except Exception:
            logger.exception("[ACTIVITY_MW] сбой middleware, апдейт пропущен дальше")

        return await handler(event, data)

    async def _notify_blocked(self, event: TelegramObject, user_id: int, now: float) -> None:
        if now - self._block_notified.get(user_id, 0.0) < BLOCK_NOTICE_INTERVAL:
            return
        self._block_notified[user_id] = now
        try:
            update = event  # на dp.update событие — Update
            if isinstance(getattr(update, "callback_query", None), CallbackQuery):
                await update.callback_query.answer(
                    "🚫 Твой аккаунт заблокирован администрацией.", show_alert=True)
            elif isinstance(getattr(update, "message", None), Message):
                await update.message.answer("🚫 Твой аккаунт заблокирован администрацией ROFL HUB.")
        except Exception:
            pass
