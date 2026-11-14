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


# --- 27.10: ПОЛНЫЙ СБРОС ЭКОСИСТЕМЫ (решение владельца: в базе только тестовые аккаунты и фейки).
# Все стартуют «как будто зарегистрировались сегодня»: монеты, интеллект, роботы, ресурсы, команды,
# рецепты по одному в сутки — с нуля (вход через /start). Перед удалением всё копируется в схему
# reset_backup_20261027 (откат возможен вручную). Остаются: платежи Stars (история и возвраты),
# тумблеры владельца, промоутеры. Разово (флаг migr:full_reset_20261027), под advisory-локом —
# два бота, стартующие одновременно, не выполнят сброс дважды.
RESET_TABLES = (
    "users", "teams", "game_stats", "auctions", "ledger", "miners", "duels", "battles", "quest_progress",
    "vip_aliases", "events", "daily_activity", "metrics_snapshots", "market_orders", "user_resources",
    "resource_ledger", "raids", "daily_goal_claims", "team_stations", "team_donations", "market_trades",
    "resource_swaps", "team_help", "user_items", "team_banners", "user_tech", "user_badges",
    "season_results", "weekly_crafts",
)
# Таблицы, созданные позже сброса, в него не входят (сброс разовый и уже выполнен).
RESET_ALL_STATEMENT = """
DO $$
DECLARE t TEXT;
BEGIN
  PERFORM pg_advisory_xact_lock(20261027);
  IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:full_reset_20261027') THEN
    CREATE SCHEMA IF NOT EXISTS reset_backup_20261027;
    FOREACH t IN ARRAY ARRAY[%s] LOOP
      EXECUTE format('CREATE TABLE IF NOT EXISTS reset_backup_20261027.%%I AS TABLE public.%%I', t, t);
      EXECUTE format('TRUNCATE public.%%I RESTART IDENTITY', t);
    END LOOP;
    UPDATE mines SET team_id = NULL, battle_id = NULL, captured_at = NULL, captured_until = NULL,
                     last_paid_at = NULL, cores_paid = 0;
    INSERT INTO feature_flags (key, enabled) VALUES ('migr:full_reset_20261027', TRUE);
  END IF;
END $$;
""" % ", ".join(f"'{t}'" for t in RESET_TABLES)


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
    # --- Пульт владельца: фиче-тумблеры без деплоя ---
    """
    CREATE TABLE IF NOT EXISTS feature_flags (
        key VARCHAR(64) PRIMARY KEY,
        enabled BOOLEAN NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # --- Биржа котлет (22.10): ордера на продажу, котлеты в эскроу ---
    """
    CREATE TABLE IF NOT EXISTS market_orders (
        id BIGSERIAL PRIMARY KEY,
        seller_id BIGINT NOT NULL,
        qty INT NOT NULL CHECK (qty >= 0),
        price INT NOT NULL CHECK (price > 0),
        status VARCHAR(12) NOT NULL DEFAULT 'open',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS market_open_idx ON market_orders (status, price, created_at);",
    "CREATE INDEX IF NOT EXISTS market_seller_idx ON market_orders (seller_id, status);",
    # Квесты №4–10 приезжают СКРЫТЫМИ (запас под ротацию); владелец включает их
    # в /quests_admin. ON CONFLICT DO NOTHING: повторный деплой не перетирает решение.
    """
    INSERT INTO feature_flags (key, enabled) VALUES
        ('quest:night_drone', FALSE), ('quest:cutlet_exchange', FALSE),
        ('quest:robot_chef', FALSE), ('quest:ice_expedition', FALSE),
        ('quest:space_signal', FALSE), ('quest:blackout', FALSE),
        ('quest:metro_veteran', FALSE)
    ON CONFLICT (key) DO NOTHING;
    """,
    # 27.10 ротация v2: новые квесты по умолчанию скрыты — первые три (были видны «по умолчанию») фиксируем включёнными
    """
    INSERT INTO feature_flags (key, enabled) VALUES
        ('quest:golden_cutlet', TRUE), ('quest:miner_career', TRUE), ('quest:locked_safe', TRUE)
    ON CONFLICT (key) DO NOTHING;
    """,
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS source VARCHAR(32) NOT NULL DEFAULT 'organic';",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS qualified_at TIMESTAMP WITH TIME ZONE;",
    # Робот-Стажёр активирован (бесплатный вечный робот, один на игрока при старте)
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS intern_claimed BOOLEAN NOT NULL DEFAULT FALSE;",
    "CREATE INDEX IF NOT EXISTS users_created_idx ON users (created_at);",
    # --- Волна 22.10 (вечер): ресурсы, мастерская, налёты, цели, станция команды ---
    """
    CREATE TABLE IF NOT EXISTS user_resources (
        user_id BIGINT NOT NULL,
        kind VARCHAR(16) NOT NULL,
        qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0),
        PRIMARY KEY (user_id, kind)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS resource_ledger (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        kind VARCHAR(16) NOT NULL,
        delta INT NOT NULL,
        reason VARCHAR(64) NOT NULL,
        ref VARCHAR(128),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS resource_ledger_user_idx ON resource_ledger (user_id, created_at);",
    "CREATE INDEX IF NOT EXISTS resource_ledger_reason_idx ON resource_ledger (reason, created_at);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_shield_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_stance VARCHAR(10);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_raid_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS has_shuttle BOOLEAN NOT NULL DEFAULT FALSE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS farm_armor_level INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS goal_streak INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS goal_last_claim DATE;",
    """
    CREATE TABLE IF NOT EXISTS raids (
        id BIGSERIAL PRIMARY KEY,
        attacker_id BIGINT NOT NULL,
        defender_id BIGINT NOT NULL,
        attack_move VARCHAR(10) NOT NULL,
        stance VARCHAR(10) NOT NULL,
        result VARCHAR(8) NOT NULL,
        loot JSONB NOT NULL DEFAULT '{}'::jsonb,
        is_revenge BOOLEAN NOT NULL DEFAULT FALSE,
        revenged BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS raids_defender_idx ON raids (defender_id, created_at);",
    "CREATE INDEX IF NOT EXISTS raids_attacker_idx ON raids (attacker_id, created_at);",
    """
    CREATE TABLE IF NOT EXISTS daily_goal_claims (
        user_id BIGINT NOT NULL,
        day DATE NOT NULL,
        PRIMARY KEY (user_id, day)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS team_stations (
        team_id INT PRIMARY KEY,
        level INT NOT NULL DEFAULT 0,
        metal INT NOT NULL DEFAULT 0,
        hydrogen INT NOT NULL DEFAULT 0,
        crystal INT NOT NULL DEFAULT 0,
        parts INT NOT NULL DEFAULT 0,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS team_donations (
        id BIGSERIAL PRIMARY KEY,
        team_id INT NOT NULL,
        user_id BIGINT NOT NULL,
        kind VARCHAR(16) NOT NULL,
        qty INT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS team_donations_team_idx ON team_donations (team_id, created_at);",
    # --- 24.10: биржа v2 (ресурсы, заявки на покупку, история), броня на 30 дней ---
    "ALTER TABLE market_orders ADD COLUMN IF NOT EXISTS asset VARCHAR(16) NOT NULL DEFAULT 'cutlet';",
    "ALTER TABLE market_orders ADD COLUMN IF NOT EXISTS side VARCHAR(4) NOT NULL DEFAULT 'sell';",
    "CREATE INDEX IF NOT EXISTS market_book_idx ON market_orders (asset, side, status, price);",
    """
    CREATE TABLE IF NOT EXISTS market_trades (
        id BIGSERIAL PRIMARY KEY,
        asset VARCHAR(16) NOT NULL,
        qty INT NOT NULL,
        price INT NOT NULL,
        buyer_id BIGINT NOT NULL,
        seller_id BIGINT NOT NULL,
        order_id BIGINT,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS market_trades_asset_idx ON market_trades (asset, created_at);",
    "CREATE INDEX IF NOT EXISTS market_trades_buyer_idx ON market_trades (buyer_id, created_at);",
    "CREATE INDEX IF NOT EXISTS market_trades_seller_idx ON market_trades (seller_id, created_at);",
    """
    CREATE TABLE IF NOT EXISTS resource_swaps (
        id BIGSERIAL PRIMARY KEY,
        maker_id BIGINT NOT NULL,
        give_kind VARCHAR(16) NOT NULL,
        give_qty INT NOT NULL CHECK (give_qty > 0),
        want_kind VARCHAR(16) NOT NULL,
        want_qty INT NOT NULL CHECK (want_qty > 0),
        status VARCHAR(12) NOT NULL DEFAULT 'open',
        taker_id BIGINT,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS resource_swaps_open_idx ON resource_swaps (status, created_at);",
    # --- 26.10: биржа команды (лоты только для тиммейтов, комиссия ниже) и взаимопомощь ---
    "ALTER TABLE market_orders ADD COLUMN IF NOT EXISTS team_id INT;",
    "ALTER TABLE resource_swaps ADD COLUMN IF NOT EXISTS team_id INT;",
    "CREATE INDEX IF NOT EXISTS market_orders_team_idx ON market_orders (team_id, status) WHERE team_id IS NOT NULL;",
    """
    CREATE TABLE IF NOT EXISTS team_help (
        id BIGSERIAL PRIMARY KEY,
        team_id INT NOT NULL,
        user_id BIGINT NOT NULL,
        kind VARCHAR(16) NOT NULL,
        qty INT NOT NULL CHECK (qty > 0),
        filled INT NOT NULL DEFAULT 0 CHECK (filled >= 0),
        status VARCHAR(12) NOT NULL DEFAULT 'open',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS team_help_open_idx ON team_help (team_id, status);",
    # --- 26.10: склад изделий мастерской (активируются игроком, когда удобно) ---
    """
    CREATE TABLE IF NOT EXISTS user_items (
        user_id BIGINT NOT NULL,
        effect VARCHAR(16) NOT NULL,
        hours INT NOT NULL CHECK (hours > 0),
        qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0),
        PRIMARY KEY (user_id, effect, hours)
    );
    """,
    # --- 26.10 (вечер): новые изделия, рудники, поэтапные рецепты ---
    "ALTER TABLE user_items DROP CONSTRAINT IF EXISTS user_items_hours_check;",   # разовые изделия: hours = 0
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_camo_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_trap_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_drill_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS thermos_from TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS thermos_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS forsage_used_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_free_fuel INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS raid_cargo INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS market_free_sales INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS station_boost INT NOT NULL DEFAULT 0;",
    "ALTER TABLE teams ADD COLUMN IF NOT EXISTS dome_until TIMESTAMP WITH TIME ZONE;",
    """
    CREATE TABLE IF NOT EXISTS team_banners (
        id BIGSERIAL PRIMARY KEY,
        team_id INT NOT NULL,
        starts_at TIMESTAMP WITH TIME ZONE NOT NULL,
        ends_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """,
    "CREATE INDEX IF NOT EXISTS team_banners_team_idx ON team_banners (team_id, ends_at);",
    """
    CREATE TABLE IF NOT EXISTS mines (
        id INT PRIMARY KEY,
        kind VARCHAR(16) NOT NULL,
        team_id INT,
        battle_id INT,
        captured_at TIMESTAMP WITH TIME ZONE,
        captured_until TIMESTAMP WITH TIME ZONE,
        last_paid_at TIMESTAMP WITH TIME ZONE
    );
    """,
    # 30 рудников (economy.MINES_COUNT), 6 ресурсов поровну по кругу (economy.MINE_KINDS); существующие не трогаются
    "INSERT INTO mines (id, kind) SELECT g, (ARRAY['metal', 'hydrogen', 'crystal', 'parts', 'stone', 'wood'])"
    "[1 + (g - 1) % 6] FROM generate_series(1, 30) g ON CONFLICT (id) DO NOTHING;",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS mine_id INT;",
    # --- 27.10: новые ресурсы, Лаборатория, лошади, сезоны ---
    """
    CREATE TABLE IF NOT EXISTS user_tech (
        user_id BIGINT NOT NULL,
        tech VARCHAR(16) NOT NULL,
        level INT NOT NULL DEFAULT 0 CHECK (level >= 0),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, tech)
    );
    """,
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS horses INT NOT NULL DEFAULT 0;",
    # 31.10, решение владельца: бонус костюма закрепляется В МОМЕНТ действия — снял костюм, выгода остаётся
    "ALTER TABLE user_tech ADD COLUMN IF NOT EXISTS cd_cut SMALLINT NOT NULL DEFAULT 0;",   # 🔬 перерыв короче на N%
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS carts INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS meds_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS shuttle_until TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE mines ADD COLUMN IF NOT EXISTS cores_paid INT NOT NULL DEFAULT 0;",
    """
    CREATE TABLE IF NOT EXISTS user_badges (
        user_id BIGINT NOT NULL,
        season VARCHAR(7) NOT NULL,
        place INT NOT NULL,
        PRIMARY KEY (user_id, season)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS season_results (
        season VARCHAR(7) PRIMARY KEY,
        processed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        payload JSONB
    );
    """,
    # Разовые миграции 27.10 (флаги в feature_flags — повторно не выполняются):
    # — Ремдрон станции убран: изделия и заряды снимаются;
    # — рудники получают 7 видов ресурса (свободные перекрашиваются);
    # — старожилам (до обновления) — 📡/🔭/⚔️ 1 уровня, чтобы налёты не встали; Шаттлу — заряд на 30 дней.
    """
    DO $$ BEGIN
      IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:resources_v3') THEN
        DELETE FROM user_items WHERE effect = 'station_drone';
        UPDATE users SET station_boost = 0 WHERE station_boost <> 0;
        UPDATE mines SET kind = (ARRAY['metal', 'hydrogen', 'crystal', 'parts', 'stone', 'wood', 'energy'])[1 + (id - 1) % 7]
          WHERE team_id IS NULL;
        INSERT INTO user_tech (user_id, tech, level)
          SELECT u.user_id, x.tech, 1 FROM users u CROSS JOIN (VALUES ('comm'), ('scout'), ('attack')) AS x(tech)
          ON CONFLICT DO NOTHING;
        UPDATE users SET shuttle_until = NOW() + INTERVAL '30 days' WHERE has_shuttle AND shuttle_until IS NULL;
        INSERT INTO feature_flags (key, enabled) VALUES ('migr:resources_v3', TRUE);
      END IF;
    END $$;
    """,
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS armor_until TIMESTAMP WITH TIME ZONE;",
    # --- 25.10: склад ресурсов с лимитом, рецепты недели ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS res_capacity INT NOT NULL DEFAULT 500;",
    # --- 26.10: Стажёр за каждый уровень интеллекта, забирается кнопкой ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS interns_pending INT NOT NULL DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS interns_backfilled BOOLEAN NOT NULL DEFAULT FALSE;",
    # Разовый пересчёт по новому правилу: положено = уровень интеллекта, уже выдано за уровни =
    # Стажёры на ферме минус стартовый. Разница ждёт игрока на ферме (идемпотентно по флагу).
    """
    UPDATE users u SET
        interns_pending = GREATEST(0,
            COALESCE((SELECT g.quiz_level FROM game_stats g WHERE g.user_id = u.user_id), 0)
            - GREATEST(0, (SELECT COUNT(*) FROM miners m WHERE m.user_id = u.user_id AND m.kind = 'intern')
                          - CASE WHEN u.intern_claimed THEN 1 ELSE 0 END)),
        interns_backfilled = TRUE
    WHERE NOT u.interns_backfilled;
    """,
    # --- 26.10 (вечер): Стажёр только за уровни, кратные 10; рефералка «активный друг» ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS interns_rebalanced BOOLEAN NOT NULL DEFAULT FALSE;",
    # Разовый откат правила «Стажёр за каждый уровень»: оставляем стартового + по одному за
    # каждые 10 уровней, лишних (самых новых) снимаем, ожидающие пересчитываем. Идемпотентно по флагу.
    """
    DELETE FROM miners WHERE miner_id IN (
        SELECT m.miner_id
        FROM (SELECT miner_id, user_id,
                     ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY purchased_at, miner_id) AS rn
              FROM miners WHERE kind = 'intern') m
        JOIN users u ON u.user_id = m.user_id
        LEFT JOIN game_stats g ON g.user_id = u.user_id
        WHERE NOT u.interns_rebalanced
          AND m.rn > (CASE WHEN u.intern_claimed THEN 1 ELSE 0 END) + COALESCE(g.quiz_level, 0) / 10);
    """,
    """
    UPDATE users u SET
        interns_pending = GREATEST(0,
            COALESCE((SELECT g.quiz_level FROM game_stats g WHERE g.user_id = u.user_id), 0) / 10
            - GREATEST(0, (SELECT COUNT(*) FROM miners m WHERE m.user_id = u.user_id AND m.kind = 'intern')
                          - CASE WHEN u.intern_claimed THEN 1 ELSE 0 END)),
        interns_rebalanced = TRUE
    WHERE NOT u.interns_rebalanced;
    """,
    # Сколько ежедневных котлет забрал игрок — условие «активного друга» в рефералке
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS bonus_claims INT NOT NULL DEFAULT 0;",
    # Счётчик котлет появился 26.10 — разово досчитываем старые получения из событий
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS bonus_claims_backfilled BOOLEAN NOT NULL DEFAULT FALSE;",
    """
    UPDATE users u SET
        bonus_claims = GREATEST(u.bonus_claims,
            (SELECT COUNT(*) FROM events e WHERE e.user_id = u.user_id AND e.event = 'bonus_claimed')),
        bonus_claims_backfilled = TRUE
    WHERE NOT u.bonus_claims_backfilled;
    """,
    # --- 26.10: удаление аккаунта (заморозка 7 дней → обезличивание строки) ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS deletion_requested_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE;",
    "CREATE INDEX IF NOT EXISTS users_deletion_idx ON users (deletion_requested_at) "
    "WHERE deletion_requested_at IS NOT NULL;",
    """
    CREATE TABLE IF NOT EXISTS weekly_crafts (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        recipe_id VARCHAR(32) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS weekly_crafts_user_idx ON weekly_crafts (user_id, recipe_id, created_at);",
    # Броня, собранная до 24.10 «навсегда», получает честные 30 дней с момента выкатки
    "UPDATE users SET armor_until = NOW() + INTERVAL '30 days' WHERE farm_armor_level > 0 AND armor_until IS NULL;",
    "CREATE INDEX IF NOT EXISTS users_referred_idx ON users (referred_by) WHERE referred_by IS NOT NULL;",
    "CREATE INDEX IF NOT EXISTS star_payments_created_idx ON star_payments (created_at);",
    RESET_ALL_STATEMENT,
    # --- 14.11: зарегистрировался в приложении, минуя чат → на первом /start полное приветствие ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS chat_welcome_due BOOLEAN NOT NULL DEFAULT FALSE;",
    # --- 14.11: 🔐 ПИН пульта владельца (shared/admin_pin.py) — одна строка, только хэш ---
    """
    CREATE TABLE IF NOT EXISTS admin_pin (
        id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
        pin_hash TEXT,
        pin_ver VARCHAR(32),
        fails INT NOT NULL DEFAULT 0,
        locked_until TIMESTAMP WITH TIME ZONE
    );
    """,
    # --- 27.10: битвы и акции v2 (пульт владельца): зачёт, места, рудники по местам, ручные итоги ---
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS scope VARCHAR(8) NOT NULL DEFAULT 'teams';",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS places INT NOT NULL DEFAULT 10;",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS mine_ids INT[] NOT NULL DEFAULT '{}';",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS manual_results JSONB;",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS announced BOOLEAN NOT NULL DEFAULT TRUE;",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS results_posted BOOLEAN NOT NULL DEFAULT TRUE;",
    "UPDATE battles SET mine_ids = ARRAY[mine_id] WHERE mine_id IS NOT NULL AND mine_ids = '{}';",
    """
    CREATE TABLE IF NOT EXISTS battle_entries (
        battle_id BIGINT NOT NULL,
        team_id BIGINT NOT NULL,
        batteries INT NOT NULL DEFAULT 0 CHECK (batteries >= 0),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (battle_id, team_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS battle_entry_log (
        id BIGSERIAL PRIMARY KEY,
        battle_id BIGINT NOT NULL,
        team_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # --- 27.10: VIP-аукционы из пульта: лот привязан к VIP ID, закрывается сам по ends_at ---
    "ALTER TABLE auctions ADD COLUMN IF NOT EXISTS vip_alias VARCHAR(32);",
    "ALTER TABLE auctions ADD COLUMN IF NOT EXISTS ends_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE auctions ADD COLUMN IF NOT EXISTS announced BOOLEAN NOT NULL DEFAULT TRUE;",
    """
    CREATE TABLE IF NOT EXISTS reward_grants (
        ref VARCHAR(128) PRIMARY KEY,
        user_id BIGINT NOT NULL,
        payload JSONB NOT NULL DEFAULT '[]'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # --- 28.10: 🤖 боевые дроны (личные спутники в налётах и экспедициях) ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS drones_guard INT NOT NULL DEFAULT 0 CHECK (drones_guard >= 0);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS drones_attack INT NOT NULL DEFAULT 0 CHECK (drones_attack >= 0);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS drones_spy INT NOT NULL DEFAULT 0 CHECK (drones_spy >= 0);",
    # --- 28.10: 🗺 экспедиции: цели на карте мира, отряды, развилки с голосованием ---
    """
    CREATE TABLE IF NOT EXISTS expedition_targets (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        descr TEXT NOT NULL DEFAULT '',
        icon VARCHAR(16) NOT NULL DEFAULT '🎯',
        x REAL NOT NULL,
        y REAL NOT NULL,
        scope VARCHAR(8) NOT NULL,
        forks INT NOT NULL DEFAULT 3,
        resolve_at TIMESTAMP WITH TIME ZONE NOT NULL,
        places INT NOT NULL DEFAULT 3,
        prizes JSONB NOT NULL DEFAULT '{}'::jsonb,
        reward_all JSONB NOT NULL DEFAULT '[]'::jsonb,
        status VARCHAR(12) NOT NULL DEFAULT 'open',
        announced BOOLEAN NOT NULL DEFAULT FALSE,
        results JSONB,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS expeditions (
        id BIGSERIAL PRIMARY KEY,
        target_id INT NOT NULL,
        mode VARCHAR(8) NOT NULL,
        user_id BIGINT,
        team_id BIGINT,
        status VARCHAR(12) NOT NULL DEFAULT 'gathering',
        batteries INT NOT NULL DEFAULT 0,
        cutlets INT NOT NULL DEFAULT 0,
        ox REAL NOT NULL,
        oy REAL NOT NULL,
        departed_at TIMESTAMP WITH TIME ZONE,
        planned_minutes INT,
        arrive_at TIMESTAMP WITH TIME ZONE,
        cargo INT NOT NULL DEFAULT 100,
        forks_done INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS expeditions_solo_uq ON expeditions (target_id, user_id) WHERE mode = 'solo';",
    "CREATE UNIQUE INDEX IF NOT EXISTS expeditions_team_uq ON expeditions (target_id, team_id) WHERE mode <> 'solo';",
    "CREATE INDEX IF NOT EXISTS expeditions_target_idx ON expeditions (target_id, status);",
    "ALTER TABLE expeditions ADD COLUMN IF NOT EXISTS suit_pct SMALLINT NOT NULL DEFAULT 0;",   # 🪖 бонус военного при выходе (31.10)
    """
    CREATE TABLE IF NOT EXISTS expedition_members (
        expedition_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        batteries INT NOT NULL DEFAULT 0,
        cutlets INT NOT NULL DEFAULT 0,
        PRIMARY KEY (expedition_id, user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS expedition_votes (
        expedition_id BIGINT NOT NULL,
        fork_no INT NOT NULL,
        user_id BIGINT NOT NULL,
        option INT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (expedition_id, fork_no, user_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS expedition_log (
        expedition_id BIGINT NOT NULL,
        fork_no INT NOT NULL,
        event_id VARCHAR(32) NOT NULL,
        option INT NOT NULL,
        votes INT NOT NULL DEFAULT 0,
        cargo_delta INT NOT NULL DEFAULT 0,
        delay_min INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (expedition_id, fork_no)
    );
    """,
    # 🔎 разведанные развилки: последствия видны отряду до решения (min шпионов и разведки лидера)
    """
    CREATE TABLE IF NOT EXISTS expedition_peeks (
        expedition_id BIGINT NOT NULL,
        fork_no INT NOT NULL,
        user_id BIGINT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (expedition_id, fork_no)
    );
    """,
    # 28.10 ночью: рудников 30, по 5 каждого из 6 ресурсов, без Ядра; у битв — награда «за участие»
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS reward_all JSONB NOT NULL DEFAULT '[]'::jsonb;",
    """
    DO $$ BEGIN
      IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:mines_30') THEN
        PERFORM pg_advisory_xact_lock(20261028);
        IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:mines_30') THEN
          UPDATE battles SET mine_ids = ARRAY(SELECT x FROM unnest(mine_ids) x WHERE x <= 30)
            WHERE status = 'active' AND EXISTS (SELECT 1 FROM unnest(mine_ids) x WHERE x > 30);
          DELETE FROM mines WHERE id > 30;
          UPDATE mines SET kind = (ARRAY['metal', 'hydrogen', 'crystal', 'parts', 'stone', 'wood'])[1 + (id - 1) % 6]
            WHERE team_id IS NULL;
          INSERT INTO feature_flags (key, enabled) VALUES ('migr:mines_30', TRUE) ON CONFLICT (key) DO NOTHING;
        END IF;
      END IF;
    END $$;
    """,
    # 🏷 26.10: название-заготовка {"a", "n", "num"} — игрок видит его на своём языке (shared/titles.py)
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS title_tpl JSONB;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS title_tpl JSONB;",
    # 📜 26.10: история игрока — выборки по игроку за 30 дней
    "CREATE INDEX IF NOT EXISTS reward_grants_user_idx ON reward_grants (user_id, created_at);",
    "CREATE INDEX IF NOT EXISTS market_trades_seller_idx ON market_trades (seller_id, created_at);",
    # --- 26.10 (аудит 1.1/1.3): итоги переживают рестарт — статус 'finishing' с отметкой времени, повтор безопасен;
    # «Итоги сейчас» в экспедиции помнит плановый час итогов (отряды в пути не становятся опоздавшими) ---
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS finishing_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS finishing_at TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS planned_resolve_at TIMESTAMP WITH TIME ZONE;",
    # --- 26.10: игры в приложении — загаданное (число, правильный ответ) хранится только на сервере ---
    """
    CREATE TABLE IF NOT EXISTS game_rounds (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        game VARCHAR(16) NOT NULL,
        state JSONB NOT NULL,
        done BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS game_rounds_user_idx ON game_rounds (user_id, created_at);",
    # 27.10: предзагрузка — таймер вопроса стартует при показе (не позже created_at + PREFETCH_SLACK_SECONDS)
    "ALTER TABLE game_rounds ADD COLUMN IF NOT EXISTS started_at TIMESTAMPTZ;",
    # --- 27.10: новые игры приложения — суточные победы и общие счётчики побед (ресурс за каждые N) ---
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_math INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_flags INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_code INT NOT NULL DEFAULT 0;",
    "ALTER TABLE game_stats ADD COLUMN IF NOT EXISTS daily_wins_memory INT NOT NULL DEFAULT 0;",
    """
    CREATE TABLE IF NOT EXISTS game_counters (
        user_id BIGINT NOT NULL,
        game VARCHAR(16) NOT NULL,
        wins_total INT NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, game)
    );
    """,
    # --- 26.10: викторина без повторов — какие вопросы игрок уже видел (ключ = хэш текста вопроса) ---
    """
    CREATE TABLE IF NOT EXISTS quiz_seen (
        user_id BIGINT NOT NULL,
        qkey VARCHAR(16) NOT NULL,
        seen_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, qkey)
    );
    """,
    # --- 27.10: жалобы игроков на вопросы викторины (одна жалоба игрока на вопрос; владелец разбирает /quiz_reports) ---
    """
    CREATE TABLE IF NOT EXISTS quiz_reports (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        qkey VARCHAR(16) NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        reason VARCHAR(16) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP WITH TIME ZONE,
        UNIQUE (user_id, qkey)
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_quiz_reports_open ON quiz_reports (qkey) WHERE resolved_at IS NULL;",
    # --- 27.10 волна «после оценки 9 агентов»: режим приложения, вызов друга на дуэль, дело дня ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS app_mode VARCHAR(10);",          # puzzle | full | NULL — не выбран
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS pending_duel VARCHAR(16);",      # код вызова, пришедший по ссылке
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS app_seen_at TIMESTAMPTZ;",       # прошлый /api/me — окно «Пока тебя не было»
    "ALTER TABLE duels ADD COLUMN IF NOT EXISTS invite_code VARCHAR(16);",      # приватная дуэль «вызов друга»
    "CREATE UNIQUE INDEX IF NOT EXISTS duels_invite_code_idx ON duels (invite_code) WHERE invite_code IS NOT NULL;",
    # --- 27.10, вечер: ввод ответа и таймер в сценах квестов (момент входа в сцену и неверные попытки) ---
    "ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS scene_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP;",
    "ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS tries INT NOT NULL DEFAULT 0;",
    # сколько раз игрок заходил к персонажу (scene.who): с третьего раза тот «раздражается» (владелец 27.10)
    "ALTER TABLE quest_progress ADD COLUMN IF NOT EXISTS visits JSONB NOT NULL DEFAULT '{}'::jsonb;",
    """
    CREATE TABLE IF NOT EXISTS daily_case_runs (
        user_id BIGINT NOT NULL,
        day DATE NOT NULL,
        case_id VARCHAR(32) NOT NULL,
        clues INT NOT NULL DEFAULT 1,
        accused INT,
        solved BOOLEAN,
        reward INT NOT NULL DEFAULT 0,
        started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMP WITH TIME ZONE,
        PRIMARY KEY (user_id, day)
    );
    """,
    "CREATE INDEX IF NOT EXISTS daily_case_runs_day_idx ON daily_case_runs (day);",
    # 30.10 ротация квестов v3: весь банк обычных квестов — в ротации дня (10 случайных на всех); разово возвращаем
    # в банк квесты, скрытые по старым правилам; дальше тумблер quest:<id> = «исключить из ротации»
    """
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:quest_pool_20261030') THEN
        PERFORM pg_advisory_xact_lock(20261030);
        IF NOT EXISTS (SELECT 1 FROM feature_flags WHERE key = 'migr:quest_pool_20261030') THEN
          UPDATE feature_flags SET enabled = TRUE WHERE key LIKE 'quest:%';
          INSERT INTO feature_flags (key, enabled) VALUES ('migr:quest_pool_20261030', TRUE) ON CONFLICT (key) DO NOTHING;
        END IF;
      END IF;
    END $$;
    """,
    # --- 30.10 🧍 персонаж и костюмы (shared/gear.py) ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(1);",              # m | f | NULL — не выбран
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS suit VARCHAR(3);",                # действующий полный комплект
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS suit_level SMALLINT;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS suit_since TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS miner_bonus_day DATE;",          # бонус шахтёра выплачен за сутки
    """
    CREATE TABLE IF NOT EXISTS user_gear (
        user_id BIGINT NOT NULL,
        suit VARCHAR(3) NOT NULL,
        slot VARCHAR(5) NOT NULL,
        level SMALLINT NOT NULL DEFAULT 1,
        qty INT NOT NULL DEFAULT 0 CHECK (qty >= 0),
        PRIMARY KEY (user_id, suit, slot, level)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_equip (
        user_id BIGINT NOT NULL,
        slot VARCHAR(5) NOT NULL,
        suit VARCHAR(3) NOT NULL,
        level SMALLINT NOT NULL DEFAULT 1,
        PRIMARY KEY (user_id, slot)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS gear_ledger (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        suit VARCHAR(3) NOT NULL,
        slot VARCHAR(5) NOT NULL,
        level SMALLINT NOT NULL,
        delta INT NOT NULL,
        reason VARCHAR(32) NOT NULL,
        ref VARCHAR(64),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS gear_ledger_user_idx ON gear_ledger (user_id, reason, created_at);",
    # --- 30.10 (вечер): артефакты на поясе, досрочные итоги «по N», детали/артефакты за соло-походы, подарки ---
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS art_bonus JSONB NOT NULL DEFAULT '{}'::jsonb;",
    "ALTER TABLE battles ADD COLUMN IF NOT EXISTS finish_count INT;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS finish_count INT;",
    "ALTER TABLE auctions ADD COLUMN IF NOT EXISTS finish_count INT;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS give_gear BOOLEAN NOT NULL DEFAULT FALSE;",
    "ALTER TABLE expedition_targets ADD COLUMN IF NOT EXISTS give_artifact BOOLEAN NOT NULL DEFAULT FALSE;",
    """
    CREATE TABLE IF NOT EXISTS gift_campaigns (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL DEFAULT '',
        rewards JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        cancelled BOOLEAN NOT NULL DEFAULT FALSE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS gift_claims (
        campaign_id INT NOT NULL,
        user_id BIGINT NOT NULL,
        claimed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (campaign_id, user_id)
    );
    """,
    # --- 30.10 ✨ скины (shared/skins.py): экземпляр с номером тиража, закалка, история; user_id = 0 — эскроу биржи ---
    """
    CREATE TABLE IF NOT EXISTS user_skins (
        id BIGSERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        skin_id VARCHAR(32) NOT NULL,
        target VARCHAR(8) NOT NULL,
        serial INT NOT NULL,
        xp INT NOT NULL DEFAULT 0,
        merged INT NOT NULL DEFAULT 0,
        equipped BOOLEAN NOT NULL DEFAULT FALSE,
        stats JSONB NOT NULL DEFAULT '{}'::jsonb,
        source VARCHAR(32) NOT NULL DEFAULT '',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (skin_id, serial)
    );
    """,
    "CREATE INDEX IF NOT EXISTS user_skins_user_idx ON user_skins (user_id);",
    "CREATE UNIQUE INDEX IF NOT EXISTS user_skins_equipped_uq ON user_skins (user_id, target) WHERE equipped;",
    # 🏆 трофейная история деталей костюма (shared/trophies.py) и 🎟 пропуск сезона (shared/season_pass.py)
    """
    CREATE TABLE IF NOT EXISTS gear_stats (
        user_id BIGINT NOT NULL,
        suit VARCHAR(3) NOT NULL,
        slot VARCHAR(5) NOT NULL,
        level SMALLINT NOT NULL,
        stats JSONB NOT NULL DEFAULT '{}'::jsonb,
        PRIMARY KEY (user_id, suit, slot, level)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS season_pass (
        user_id BIGINT NOT NULL,
        season VARCHAR(7) NOT NULL,
        xp INT NOT NULL DEFAULT 0,
        premium BOOLEAN NOT NULL DEFAULT FALSE,
        claimed_free INT[] NOT NULL DEFAULT '{}',
        claimed_paid INT[] NOT NULL DEFAULT '{}',
        PRIMARY KEY (user_id, season)
    );
    """,
    # 🕵️ Проверка на абуз (shared/abuse.py): отметка владельца «проверен» с баллами на момент проверки
    """
    CREATE TABLE IF NOT EXISTS abuse_reviews (
        user_id BIGINT PRIMARY KEY,
        score INT NOT NULL DEFAULT 0,
        note VARCHAR(300) NOT NULL DEFAULT '',
        reviewed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # 🤝 Костюм за 10 активных друзей (один раз, на выбор): какой костюм забран
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS ref_suit VARCHAR(3)",
    # 🎟 подарок владельца /unlimit на 30+ дней — до этого срока лимит опыта пропуска как у месячного безлимита
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS pass_boost_until TIMESTAMP WITH TIME ZONE",
    "ALTER TABLE season_pass ADD COLUMN IF NOT EXISTS game_day DATE",
    "ALTER TABLE season_pass ADD COLUMN IF NOT EXISTS game_xp INT NOT NULL DEFAULT 0",
    # 🎟 Опыт, набранный до первого пропуска (2026-10), — в первый пропуск 2026-11, который и виден на экране.
    # Идемпотентно: после переноса октябрьских строк нет, а add_xp туда больше не пишет (active_season).
    """
    WITH moved AS (DELETE FROM season_pass WHERE season < '2026-11' RETURNING user_id, xp)
    INSERT INTO season_pass (user_id, season, xp)
    SELECT user_id, '2026-11', SUM(xp) FROM moved GROUP BY user_id
    ON CONFLICT (user_id, season) DO UPDATE SET xp = season_pass.xp + EXCLUDED.xp;
    """,
    # --- 04.11: переименование ROFL HUB → Cyber Barons (сначала было Bot Barons): VIP ID ROFL-HUB-777 → BARON-777 (идемпотентно) ---
    "UPDATE vip_aliases SET alias = 'BARON-' || substr(alias, 10) WHERE alias LIKE 'ROFL-HUB-%';",
    "UPDATE auctions SET vip_alias = 'BARON-' || substr(vip_alias, 10) WHERE vip_alias LIKE 'ROFL-HUB-%';",
    "UPDATE auctions SET item_title = replace(replace(replace(item_title, 'ROFL-HUB-', 'BARON-'), 'ROFL HUB', 'Cyber Barons'), "
    "'Bot Barons', 'Cyber Barons') "
    "WHERE item_title LIKE '%ROFL%' OR item_title LIKE '%Bot Barons%';",
]


db = Database()
