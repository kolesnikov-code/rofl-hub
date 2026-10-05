import os
import asyncpg
from dotenv import load_dotenv

# Принудительно находим корень проекта и жестко привязываем файл .env для локальных тестов на компе
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Считываем ссылку из .env. На сервере Railway эта переменная подставится автоматически!
DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    # Защитный буфер: если переменные на хостинге или локально лежат раздельно
    PGHOST = os.getenv("PGHOST", "localhost")
    PGPORT = os.getenv("PGPORT", "5432")
    PGUSER = os.getenv("PGUSER", "postgres")
    PGPASSWORD = os.getenv("PGPASSWORD", "postgres")
    PGDATABASE = os.getenv("PGDATABASE", "rofl_db")
    DB_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Открывает асинхронный пул соединений к БД"""
        try:
            print(f"DEBUG: Наш текущий URL базы: {DB_URL}")
            self.pool = await asyncpg.create_pool(dsn=DB_URL)
            print("[DB] Пул соединений с PostgreSQL успешно открыт!")
        except Exception as e:
            print(f"[DB] Ошибка подключения к БД: {e}")

    async def disconnect(self):
        """Закрывает каналы связи при перезапуске бота"""
        if self.pool:
            await self.pool.close()
            print("[DB] Пул соединений с PostgreSQL закрыт")

    async def create_tables(self):
        """Создание БД """
        if not self.pool:
            return

        # 1. ТАБЛИЦА ЮЗЕРА, СТАРТОВОГО БАЛАНСА И ВНУТРЕННЕГО ID ЭКОСИСТЕМЫ

        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(100),
                    rofl_hub_id VARCHAR(50) DEFAULT NULL,
                    balance INT DEFAULT 1000,
                    inv_cutlets INT DEFAULT 1,
                    referred_by BIGINT,
                    is_subscribed INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. ТАБЛИЦА МАЙНЕРОВ И ХОЛОДИЛЬНИКА

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS miners (
                    user_id BIGINT PRIMARY KEY,
                    miner_type VARCHAR(50) DEFAULT 'none',
                    miner_coins_packed INT DEFAULT 0,
                    fridge_slots INT DEFAULT 1,
                    cutlets_inside INT DEFAULT 0,
                    miner_charge INT DEFAULT 100,
                    contract_expires TIMESTAMP,
                    last_claim_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # 3. ТАБЛИЦА ИГРОВОЙ АНАЛИТИКИ И АНТИФРОДА

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS game_stats (
                    user_id BIGINT PRIMARY KEY,
                    games_played INT DEFAULT 0,
                    games_won INT DEFAULT 0,
                    today_games_count INT DEFAULT 0,
                    last_game_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # 4. ТАБЛИЦА ПОКУПКИ ПОСТОВ

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS pending_posts (
                    post_id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    photo_file_id VARCHAR(255) NOT NULL,
                    post_text TEXT NOT NULL,
                    target_url VARCHAR(255) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # 5. ТАБЛИЦА

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS site_ads (
                    ad_id SERIAL PRIMARY KEY,
                    photo_file_id VARCHAR(255) NOT NULL,
                    post_text TEXT NOT NULL,
                    target_url VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            #

            #

            print("[DB] Все таблицы империи успешно созданы")


db = Database()
