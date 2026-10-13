"""
Точка входа главного бота ROFL HUB. Запуск: python -m bots.main_bot.bot
"""
from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, ErrorEvent, MenuButtonWebApp, WebAppInfo

from bots.main_bot.config import BOT_TOKEN, SHOP_TEST_MODE, SHOP_TEST_USER_IDS, WEBAPP_PORT, WEBAPP_URL
from bots.main_bot.webapp import start_webapp_server
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.duels import duel_reaper_loop, router as duels_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.farm import router as farm_router
from bots.main_bot.handlers.games import router as games_router
from bots.main_bot.handlers.menu import router as menu_router
from bots.main_bot.handlers.payments import router as payments_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.quests import router as quests_router
from bots.main_bot.handlers.referral_link import router as referral_router
from bots.main_bot.handlers.rofl_hub_all import router as rofl_hub_all_router
from bots.main_bot.handlers.rules import router as rules_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.transfer import router as transfer_router
from bots.main_bot.middleware import ActivityMiddleware
from bots.main_bot.utils.quest_loader import load_quests
from bots.main_bot.utils.questions_loader import load_questions_from_csv
from shared.database import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())
# Блокировка игроков + учёт активности (DAU) — на каждый апдейт
dp.update.outer_middleware(ActivityMiddleware())
# Порядок важен: start (регистрация) и payments (деньги) — первыми
for r in (start_router, payments_router, shop_router, games_router, duels_router, quests_router,
          farm_router, profile_router, clans_router, transfer_router, referral_router, menu_router,
          faq_router, rules_router, rofl_hub_all_router):
    dp.include_router(r)


# Синее меню команд Telegram (кнопка «/»). Ключ — команда, значения — описания ru/en.
BOT_COMMANDS: dict[str, tuple[str, str]] = {
    "app": ("🎮 Открыть Mini App", "🎮 Open the Mini App"),
    "menu": ("📱 Главное меню", "📱 Main menu"),
    "profile": ("👤 Мой профиль и паспорт", "👤 My profile & passport"),
    "farm": ("🚜 Кибер-ферма и заправка", "🚜 Cyber-farm & refueling"),
    "shop": ("🏪 Магазин за Telegram Stars", "🏪 Shop (Telegram Stars)"),
    "games": ("🕹️ Все игры против бота", "🕹️ All games vs the bot"),
    "quiz": ("🧠 Викторина: 10 секунд на ответ", "🧠 Quiz: 10 seconds to answer"),
    "duel": ("⚔️ Дуэль 1-на-1 на ставку", "⚔️ 1-on-1 duel for a stake"),
    "quests": ("🗺️ Квесты: истории с выборами", "🗺️ Quests: stories with choices"),
    "my_team": ("🏆 Моя команда и тиммейты", "🏆 My team & teammates"),
    "invite": ("🤝 Реферальная ссылка: +1000 за друга", "🤝 Referral link: +1000 per friend"),
    "transfer": ("🔄 Перевести монеты игроку", "🔄 Send coins to a player"),
    "my_stats": ("📊 Моя статистика", "📊 My stats"),
    "faq": ("📚 Частые вопросы", "📚 FAQ"),
    "rules": ("📜 Пользовательское соглашение", "📜 User agreement"),
    "paysupport": ("🛟 Поддержка по платежам", "🛟 Payment support"),
}


async def register_bot_commands(bot: Bot) -> None:
    """Регистрирует синее меню команд: русский — для ru-клиентов, английский — для всех прочих."""
    ru = [BotCommand(command=c, description=d[0]) for c, d in BOT_COMMANDS.items()]
    en = [BotCommand(command=c, description=d[1]) for c, d in BOT_COMMANDS.items()]
    await bot.set_my_commands(en)  # дефолт для всех языков клиента
    await bot.set_my_commands(ru, language_code="ru")


@dp.error()
async def on_error(event: ErrorEvent) -> None:
    """Любое необработанное исключение — в лог целиком, игроку — короткий ответ, бот живёт дальше."""
    logger.exception("Необработанная ошибка в обработчике: %s", event.exception)
    update = event.update
    try:
        if update.callback_query:
            await update.callback_query.answer("⚠️ Что-то пошло не так. Попробуй ещё раз.", show_alert=True)
        elif update.message:
            await update.message.answer("⚠️ Что-то пошло не так. Попробуй ещё раз через минуту.")
    except Exception:
        pass


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await db.connect()
    await db.create_tables()
    load_questions_from_csv()
    load_quests()

    if SHOP_TEST_MODE:
        logger.warning("SHOP_TEST_MODE=1: бесплатные покупки для %s. На проде выключить!", sorted(SHOP_TEST_USER_IDS))

    try:
        await register_bot_commands(bot)
    except Exception:
        logger.exception("Не удалось зарегистрировать меню команд — бот работает дальше.")

    # Жнец дуэлей: доигрывает зависшие раунды и возвращает ставки протухших очередей
    asyncio.create_task(duel_reaper_loop(bot))

    # Mini App: веб-сервер (статика + API + Stars-инвойсы) и кнопка меню чата
    try:
        await start_webapp_server(BOT_TOKEN, WEBAPP_PORT, bot=bot)
    except OSError as e:
        logger.warning("Mini App сервер не стартовал (порт %s занят?): %s — бот работает дальше.",
                       WEBAPP_PORT, e)
    if WEBAPP_URL:
        try:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="🎮 ROFL HUB", web_app=WebAppInfo(url=WEBAPP_URL)))
            logger.info("Кнопка Mini App установлена: %s", WEBAPP_URL)
        except Exception:
            logger.exception("Не удалось установить кнопку Mini App — бот работает дальше.")

    me = await bot.get_me()
    logger.info("Главный бот @%s запущен.", me.username)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
