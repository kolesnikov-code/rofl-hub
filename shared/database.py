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

    async def connect(self, dsn: str | None = None, retries: int = 5, delay: float = 3.0) -> None:
        """
        Создаёт пул с ретраями: при рестарте хостинга база может подняться
        на несколько секунд позже бота — не падаем, а ждём и пробуем снова.
        """
        dsn = dsn or self.DATABASE_URL
        if not dsn:
            logger.critical("DATABASE_URL не задан в переменных окружения.")
            raise RuntimeError("Переменная DATABASE_URL отсутствует.")
        last_error: Exception | None = None
        for attempt in range(1, retries + 1):
            try:
                self._pool = await asyncpg.create_pool(dsn, min_size=2, max_size=10, command_timeout=60)
                logger.info("Пул PostgreSQL инициализирован (попытка %s).", attempt)
                return
            except Exception as e:
                last_error = e
                logger.warning("Попытка %s/%s подключения к PostgreSQL не удалась: %s",
                               attempt, retries, e)
                if attempt < retries:
                    import asyncio
                    await asyncio.sleep(delay * attempt)
        logger.critical("Не удалось создать пул PostgreSQL после %s попыток", retries)
        raise last_error

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
    # --- Журнал движения монет ---
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
    # --- Блок 3: новые соло-игры и уровни викторины ---
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_coin INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_dice INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_safe INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS quiz_correct_total INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS quiz_level INT NOT NULL DEFAULT 0;",
    # Прогресс текущей итерации уровня (обнуляется при переходе на новый уровень)
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS quiz_level_progress INT NOT NULL DEFAULT 0;",
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
    # --- Блок 2: ферма. Каждый робот — строка со своей датой сгорания ---
    """
    CREATE TABLE IF NOT EXISTS miners (
        miner_id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        kind VARCHAR(16) NOT NULL,
        purchased_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        fuel_until TIMESTAMP WITH TIME ZONE
    );
    """,
    "CREATE INDEX IF NOT EXISTS miners_user_idx ON miners (user_id);",
    # Остаток точного начисления (монето-микросекунды, см. shared/farm_logic.py)
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS mining_acc BIGINT NOT NULL DEFAULT 0;",
    # Ежедневная бесплатная котлета: время последнего нажатия «ЗАБРАТЬ БОНУС»
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_bonus_claim_at TIMESTAMP WITH TIME ZONE;",
    # --- Блок 5: отметка возврата Stars по платежу ---
    "ALTER TABLE star_payments ADD COLUMN IF NOT EXISTS refunded_at TIMESTAMP WITH TIME ZONE;",
    # --- Дуэли: КНБ 1-на-1 со ставками-эскроу и сжиганием 20% банка ---
    """
    CREATE TABLE IF NOT EXISTS duels (
        duel_id BIGSERIAL PRIMARY KEY,
        stake INT NOT NULL,
        player1 BIGINT NOT NULL,
        player2 BIGINT,
        move1 VARCHAR(10),
        move2 VARCHAR(10),
        rounds INT NOT NULL DEFAULT 1,
        status VARCHAR(16) NOT NULL DEFAULT 'waiting',
        winner_id BIGINT,
        round_started_at TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMP WITH TIME ZONE
    );
    """,
    "CREATE INDEX IF NOT EXISTS duels_matchmaking_idx ON duels (status, stake);",
    "CREATE INDEX IF NOT EXISTS duels_players_idx ON duels (player1, player2);",
    # --- Битвы команд и кланов: событийные состязания, запускаемые владельцем ---
    """
    CREATE TABLE IF NOT EXISTS battles (
        battle_id BIGSERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        nomination_key VARCHAR(32) NOT NULL,
        nomination_text VARCHAR(200) NOT NULL,
        starts_at TIMESTAMP WITH TIME ZONE NOT NULL,
        ends_at TIMESTAMP WITH TIME ZONE NOT NULL,
        prizes JSONB NOT NULL DEFAULT '{}'::jsonb,
        status VARCHAR(16) NOT NULL DEFAULT 'active',
        results JSONB,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS battles_status_idx ON battles (status, ends_at);",
    # --- Квесты: прогресс игрока по сценариям (сценарии — JSON в data/quests) ---
    """
    CREATE TABLE IF NOT EXISTS quest_progress (
        user_id BIGINT NOT NULL,
        quest_id VARCHAR(64) NOT NULL,
        scene VARCHAR(64) NOT NULL,
        flags JSONB NOT NULL DEFAULT '[]'::jsonb,
        completed_at TIMESTAMP WITH TIME ZONE,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, quest_id)
    );
    """,
    # --- VIP ID с аукционов: равноправный алиас игрока для переводов и понта ---
    """
    CREATE TABLE IF NOT EXISTS vip_aliases (
        alias VARCHAR(32) PRIMARY KEY,
        user_id BIGINT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS vip_aliases_user_idx ON vip_aliases (user_id);",
    # --- Блок 4: тиммейты, капитанство по старшинству, имена без username ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS team_joined_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(128);",
    # Старожилам без даты вступления — консервативная отметка «сейчас» (один раз)
    "UPDATE users SET team_joined_at = CURRENT_TIMESTAMP WHERE team_id IS NOT NULL AND team_joined_at IS NULL;",
    "CREATE INDEX IF NOT EXISTS users_team_joined_idx ON users (team_id, team_joined_at);",
    # Разовый перенос старых счётчиков роботов в таблицу miners (30 дней жизни).
    # Идемпотентно: после переноса счётчики обнуляются и блок больше не срабатывает.
    """
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM users WHERE miner_junior_count > 0 OR miner_premium_count > 0) THEN
            INSERT INTO miners (user_id, kind, purchased_at, expires_at)
            SELECT u.user_id, 'junior', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '30 days'
            FROM users u CROSS JOIN LATERAL generate_series(1, u.miner_junior_count)
            WHERE u.miner_junior_count > 0;
            INSERT INTO miners (user_id, kind, purchased_at, expires_at)
            SELECT u.user_id, 'premium', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '30 days'
            FROM users u CROSS JOIN LATERAL generate_series(1, u.miner_premium_count)
            WHERE u.miner_premium_count > 0;
            UPDATE users SET miner_junior_count = 0, miner_premium_count = 0
            WHERE miner_junior_count > 0 OR miner_premium_count > 0;
        END IF;
    END $$;
    """,
    # --- Продуктовая аналитика (13.10 вечер): события, активность, трафик, снапшоты ---
    """
    CREATE TABLE IF NOT EXISTS events (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        event VARCHAR(64) NOT NULL,
        props JSONB NOT NULL DEFAULT '{}',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS events_event_created_idx ON events (event, created_at);",
    "CREATE INDEX IF NOT EXISTS events_user_created_idx ON events (user_id, created_at);",
    """
    CREATE TABLE IF NOT EXISTS daily_activity (
        user_id BIGINT NOT NULL,
        day DATE NOT NULL,
        PRIMARY KEY (user_id, day)
    );
    """,
    "CREATE INDEX IF NOT EXISTS daily_activity_day_idx ON daily_activity (day);",
    """
    CREATE TABLE IF NOT EXISTS promoters (
        code VARCHAR(32) PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS metrics_snapshots (
        id BIGSERIAL PRIMARY KEY,
        taken_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        kind VARCHAR(16) NOT NULL,
        data JSONB NOT NULL DEFAULT '{}'
    );
    """,
    "CREATE INDEX IF NOT EXISTS metrics_snapshots_kind_idx ON metrics_snapshots (kind, taken_at);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS source VARCHAR(32) NOT NULL DEFAULT 'organic';",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS qualified_at TIMESTAMP WITH TIME ZONE;",
    "CREATE INDEX IF NOT EXISTS users_created_idx ON users (created_at);",
    "CREATE INDEX IF NOT EXISTS users_referred_idx ON users (referred_by) WHERE referred_by IS NOT NULL;",
    "CREATE INDEX IF NOT EXISTS star_payments_created_idx ON star_payments (created_at);",
]


db = Database()
