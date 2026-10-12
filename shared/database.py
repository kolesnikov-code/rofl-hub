import logging
import os
import asyncpg
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.pool = None
        self.DATABASE_URL = os.getenv("DATABASE_URL")

    async def connect(self):
        """Устанавливает соединение с асинхронным пулом PostgreSQL на Railway"""
        if not self.DATABASE_URL:
            logger.critical("🚨 DATABASE_URL не найден в переменных окружения .env!")
            raise RuntimeError("Переменная DATABASE_URL отсутствует.")

        try:
            self.pool = await asyncpg.create_pool(
                self.DATABASE_URL,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("🟢 Асинхронный пул базы данных PostgreSQL успешно инициализирован!")
        except Exception as e:
            logger.error(f"🚨 Ошибка подключения к базе данных на Railway: {e}")
            raise e

    async def create_tables(self):
        """Инициализирует базовую схему и автоматически накатывает миграции"""
        if not self.pool:
            raise RuntimeError("База данных не подключена.")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 1. Базовая таблица пользователей (Вшита колонка lang!)
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username VARCHAR(255),
                        balance BIGINT DEFAULT 0,
                        fridge_capacity INT DEFAULT 1,
                        fridge_cutlets INT DEFAULT 0,
                        inv_cutlets INT DEFAULT 0,
                        miner_junior_count INT DEFAULT 0,
                        miner_premium_count INT DEFAULT 0,
                        boost_level INT DEFAULT 0,
                        team_id INT DEFAULT NULL,
                        referred_by BIGINT DEFAULT NULL,
                        lang VARCHAR(5) DEFAULT 'ru',
                        last_update_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 2. Базовая таблица команд и кланов
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS teams (
                        team_id SERIAL PRIMARY KEY,
                        team_name VARCHAR(32) UNIQUE NOT NULL,
                        captain_id BIGINT NOT NULL,
                        city VARCHAR(100),
                        school_num VARCHAR(20),
                        members_count INT DEFAULT 1,
                        max_members INT DEFAULT 50,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 3. Базовая таблица финансовой отчетности Stars
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS star_payments (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        telegram_charge_id VARCHAR(255) UNIQUE NOT NULL,
                        item_payload VARCHAR(255) NOT NULL,
                        stars_amount INT NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 4. Базовая таблица игровой статистики
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS game_stats (
                        user_id BIGINT PRIMARY KEY,
                        games_played INT DEFAULT 0,
                        games_won INT DEFAULT 0,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # 5. Таблица невозвратных/возвратных аукционов холдинга (Добавлен previous_bidder_id)
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS auctions (
                        auction_id SERIAL PRIMARY KEY,
                        item_title VARCHAR(100) NOT NULL,
                        item_desc TEXT,
                        current_price BIGINT DEFAULT 0,
                        highest_bidder_id BIGINT DEFAULT NULL,
                        previous_bidder_id BIGINT DEFAULT NULL,
                        min_step INT DEFAULT 100,
                        status VARCHAR(20) DEFAULT 'open',
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # ============================================================================
                # 🔄 МОДУЛЬ НАКАТЫВАНИЯ РАЗДЕЛЬНЫХ СУТОЧНЫХ ЛИМИТОВ (ФИКС ДЛЯ ИГР)
                # ============================================================================
                logger.info("⏳ Синхронизация трех раздельных колонок лимитов побед...")

                await conn.execute("ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_rps INT DEFAULT 0;")
                await conn.execute("ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_hl INT DEFAULT 0;")
                await conn.execute("ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_quiz INT DEFAULT 0;")
                await conn.execute("ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS last_game_date DATE DEFAULT CURRENT_DATE;")

                logger.info("📊 СХЕМА ДАННЫХ POSTGRESQL ПОЛНОСТЬЮ СИНХРОНИЗИРОВАНА С КОНСОЛЬЮ RAILWAY!")

db = Database()
