"""
Пул PostgreSQL и схема. Миграции идемпотентны: каждая строка безопасна для повторного запуска.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger(__name__)


class DatabaseNotConnected(RuntimeError):
    pass


class Database:
    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None
        self.DATABASE_URL = os.getenv("DATABASE_URL")

    @property
    def pool(self) -> asyncpg.Pool:
        """Никогда не возвращает None: без соединения — явная ошибка, а не AttributeError в обработчике."""
        if self._pool is None:
            raise DatabaseNotConnected("База данных не подключена: вызови await db.connect() при старте.")
        return self._pool

    @property
    def is_connected(self) -> bool:
        return self._pool is not None

    async def connect(self, dsn: str | None = None) -> None:
        dsn = dsn or self.DATABASE_URL
        if not dsn:
            logger.critical("DATABASE_URL не задан в переменных окружения.")
            raise RuntimeError("Переменная DATABASE_URL отсутствует.")
        try:
            self._pool = await asyncpg.create_pool(dsn, min_size=2, max_size=10, command_timeout=60)
        except Exception:
            logger.exception("Не удалось создать пул PostgreSQL")
            raise
        logger.info("Пул PostgreSQL инициализирован.")

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def create_tables(self) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for statement in SCHEMA_STATEMENTS:
                    await conn.execute(statement)
        logger.info("Схема PostgreSQL синхронизирована.")


SCHEMA_STATEMENTS: list[str] = [
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        username VARCHAR(255),
        balance BIGINT NOT NULL DEFAULT 0,
        fridge_capacity INT NOT NULL DEFAULT 1,
        fridge_cutlets INT NOT NULL DEFAULT 0,
        inv_cutlets INT NOT NULL DEFAULT 0,
        miner_junior_count INT NOT NULL DEFAULT 0,
        miner_premium_count INT NOT NULL DEFAULT 0,
        boost_level INT NOT NULL DEFAULT 0,
        team_id INT DEFAULT NULL,
        referred_by BIGINT DEFAULT NULL,
        lang VARCHAR(5) NOT NULL DEFAULT 'ru',
        last_update_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS teams (
        team_id SERIAL PRIMARY KEY,
        team_name VARCHAR(32) UNIQUE NOT NULL,
        captain_id BIGINT NOT NULL,
        city VARCHAR(100),
        school_num VARCHAR(20),
        members_count INT NOT NULL DEFAULT 1,
        max_members INT NOT NULL DEFAULT 50,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS star_payments (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        telegram_charge_id VARCHAR(255) UNIQUE NOT NULL,
        item_payload VARCHAR(255) NOT NULL,
        stars_amount INT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS game_stats (
        user_id BIGINT PRIMARY KEY,
        games_played INT NOT NULL DEFAULT 0,
        games_won INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS auctions (
        auction_id SERIAL PRIMARY KEY,
        item_title VARCHAR(100) NOT NULL,
        item_desc TEXT,
        current_price BIGINT NOT NULL DEFAULT 0,
        highest_bidder_id BIGINT DEFAULT NULL,
        previous_bidder_id BIGINT DEFAULT NULL,
        min_step INT NOT NULL DEFAULT 100,
        status VARCHAR(20) NOT NULL DEFAULT 'open',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # --- Журнал движения рофлов ---
    """
    CREATE TABLE IF NOT EXISTS ledger (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        delta BIGINT NOT NULL,
        reason VARCHAR(64) NOT NULL,
        ref VARCHAR(128),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS ledger_user_created_idx ON ledger (user_id, created_at);",
    "CREATE INDEX IF NOT EXISTS ledger_reason_created_idx ON ledger (reason, created_at);",
    # --- Миграции: суточные лимиты ---
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_rps INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_hl INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_quiz INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS last_game_date DATE DEFAULT CURRENT_DATE;",
    # --- Миграции: срочные лицензии (бусты, дрон, безлимит) ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS boost_nuclear_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS boost_nitrogen_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS drone_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS unlimit_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN NOT NULL DEFAULT FALSE;",
    # --- Защита денег на уровне БД: баланс не может быть отрицательным ---
    """
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_balance_nonnegative') THEN
            ALTER TABLE users ADD CONSTRAINT users_balance_nonnegative CHECK (balance >= 0);
        END IF;
    END $$;
    """,
    "CREATE INDEX IF NOT EXISTS users_referred_by_idx ON users (referred_by);",
    "CREATE INDEX IF NOT EXISTS users_team_id_idx ON users (team_id);",
]


db = Database()
