import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from pathlib import Path
from dotenv import load_dotenv

# Жестко привязываем чтение .env к корню проекта для безопасности токенов
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Считываем токен секретного админ-бота из файла .env
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

if not ADMIN_BOT_TOKEN:
    raise RuntimeError(
        "🚨 КРИТИЧЕСКИЙ КРАШ АДМИНКИ: Переменная ADMIN_BOT_TOKEN отсутствует в системе или файле .env! Запуск заблокирован."
    )

# Импортируем монолитный роутер управления админ-панелью
from bots.admin_notifier_bot.handlers.admin_panel import router as admin_panel_router
from shared.database import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Главная точка входа в асинхронный контур административного бота.
    Отвечает за модерацию заявок Инста-Лифта и запуск VIP-аукционов.
    """
    bot = Bot(token=ADMIN_BOT_TOKEN)
    dp = Dispatcher()

    try:
        # Подключаемся к общему пулу PostgreSQL на Railway (если еще не открыт основным ботом)
        if not db.pool:
            await db.connect()
            await db.create_tables()

        # Подключаем наш единственный монолитный роутер админки
        dp.include_router(admin_panel_router)

        logger.info("🟢 БОТ АДМИНИСТРАТИВНОЙ ПАНЕЛИ УСПЕШНО ЗАПУЩЕН И СЛУШАЕТ КОМАНДЫ!")

        # Запускаем шлюз прослушивания обновлений админ-панели
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"🚨 Фатальная ошибка во время работы админ-бота: {e}")

    finally:
        logger.info("⏳ Безопасное закрытие сессий административного бота...")
        await bot.session.close()
        # Пул базы данных закрываем только если основной бот юзеров его не использует,
        # но для изоляции админки при перезапуске просто гасим ее сессию.
        logger.info("🔒 Сессия административного бота успешно изолирована.")


if __name__ == "__main__":
    asyncio.run(main())
