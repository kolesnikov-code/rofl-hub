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
        """Открывает асинхронный пул соединений к БД без утечки паролей в логи"""
        try:
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
        """Создание СУБД империи ROFL HUB CORE под ленивый расчёт,Stars-транзакции и аукционы"""
        if not self.pool:
            return

        async with self.pool.acquire() as conn:
            # ----------------------------------------------------------------
            # 👑 1. ГЛАВНАЯ ТАБЛИЦА ПРОФИЛЯ ЮЗЕРА, ФЕРМ И ТОПЛИВНОГО ХАБА
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(100),
                    rofl_hub_id VARCHAR(50) DEFAULT NULL,
                    balance BIGINT DEFAULT 1000,                  -- BIGINT защита от миллиардных переполнений Китов
                    referred_by BIGINT,
                    is_subscribed INT DEFAULT 0,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    team_id INT DEFAULT NULL,
                    boost_level INT DEFAULT 0,                    -- Уровень Боевого Буста дуэлей (макс 3)

                    -- 📦 ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ (НОВАЯ ЛOГИКА АНАТOЛИЯ АЛЕКСЕЕВИЧА)
                    fridge_capacity INT DEFAULT 1,                -- Вместимость хаба (1, 5, 10, 50, 100 котлет)
                    fridge_cutlets INT DEFAULT 1,                 -- Сколько платных котлет лежит на складе сейчас
                    inv_cutlets INT DEFAULT 0,                    -- Котлеты в кармане (не заправленные в хаб)

                    -- 🤖 СЧЁТЧИКИ ОБОPУДОВАНИЯ (Поддерживают неограниченный закуп доната!)
                    miner_junior_count INT DEFAULT 0,             -- Сколько у юзера Младших Майнеров (★49 Stars)
                    miner_premium_count INT DEFAULT 0,            -- Сколько у юзера Кибер-Бурильщиков (★99 Stars)

                    -- ⏳ ТИТАНОВЫЙ ПРЕДOХРАНИТЕЛЬ СЕРВЕРА Railway (Lazy Evaluation)
                    last_update_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # ----------------------------------------------------------------
            # 📊 2. ТАБЛИЦА ИГРОВОЙ АНАЛИТИКИ И АНТИФРОДА
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS game_stats (
                    user_id BIGINT PRIMARY KEY,
                    games_played INT DEFAULT 0,
                    games_won INT DEFAULT 0,
                    today_games_count INT DEFAULT 0,
                    last_game_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # ----------------------------------------------------------------
            # 💎 3. ТАБЛИЦА АУДИТА И ФИНАНСОВОЙ ВАЛИДАЦИИ STARS (Защита от дублей)
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS star_payments (
                    payment_id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    telegram_charge_id VARCHAR(255) UNIQUE NOT NULL,
                    item_payload VARCHAR(100) NOT NULL,
                    stars_amount INT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # ----------------------------------------------------------------
            # 👑 4. ТАБЛИЦА ДИНAМИЧЕСКИХ ТOРГOВ И VIP-AУКЦИOНOВ
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS active_auction (
                    auction_id SERIAL PRIMARY KEY,
                    vip_id_target VARCHAR(50) NOT NULL,
                    current_leader_id BIGINT DEFAULT NULL,
                    current_max_bid BIGINT DEFAULT 10000,
                    expires_at TIMESTAMPTZ NOT NULL,
                    is_active INT DEFAULT 1,
                    FOREIGN KEY (current_leader_id) REFERENCES users(user_id) ON DELETE SET NULL
                );
            """)

            # ----------------------------------------------------------------
            # 📸 5. ТАБЛИЦА ПОКУПКИ ПОСТОВ (Спринты и Инста-Лифт)
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS pending_posts (
                    post_id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    photo_file_id VARCHAR(255) NOT NULL,
                    post_text TEXT NOT NULL,
                    target_url VARCHAR(255) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            # ----------------------------------------------------------------
            # 🌐 6. ТАБЛИЦА РЕКЛАМЫ НА БУДУЩЕМ САЙТЕ
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS site_ads (
                    ad_id SERIAL PRIMARY KEY,
                    photo_file_id VARCHAR(255) NOT NULL,
                    post_text TEXT NOT NULL,
                    target_url VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # ----------------------------------------------------------------
            # 👥 7. ТАБЛИЦА КОМАНД (ЖЕСТКИЙ ЛИМИТ 50 ИГРOКОВ АНАТOЛИЯ АЛЕКСЕЕВИЧА)
            # ----------------------------------------------------------------
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    team_id SERIAL PRIMARY KEY,
                    team_name VARCHAR(100) UNIQUE NOT NULL,
                    captain_id BIGINT UNIQUE NOT NULL,
                    city VARCHAR(100) DEFAULT 'Не указан',
                    school_num VARCHAR(50) DEFAULT 'Не указана',
                    members_count INT DEFAULT 1,
                    max_members INT DEFAULT 50,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (captain_id) REFERENCES users(user_id) ON DELETE CASCADE
                );
            """)

            print("[DB] Все таблицы империи успешно созданы по новой токеномике!")


db = Database()
