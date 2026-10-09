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
        """Создание БД империи ROFL HUB CORE под ленивый расчёт и генератор Pillow"""
        if not self.pool:
            return

        async with self.pool.acquire() as conn:
            # ----------------------------------------------------------------
            # 👑 1. ГЛАВНАЯ ТАБЛИЦА ПРОФИЛЯ ЮЗЕРА, ФЕРМ И ТОПЛИВНОГО ХАБА
            # ----------------------------------------------------------------
            # Сюда вшита вся экономика, подписки на ремонт и счетчики роботов!
            await conn.execute(
                """
                               CREATE TABLE IF NOT EXISTS users
                               (
                                   user_id BIGINT PRIMARY KEY,
                                   username VARCHAR
                               (
                                   100
                               ),
                                   rofl_hub_id VARCHAR
                               (
                                   50
                               ) DEFAULT NULL,
                                   balance BIGINT DEFAULT 1000, -- BIGINT защита от миллиардных переполнений Китов
                                   referred_by BIGINT,
                                   is_subscribed INT DEFAULT 0,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   team_id INT DEFAULT NULL,

                                   -- 📦 ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ (НОВАЯ ЛOГИКА АНАТOЛИЯ АЛЕКСЕЕВИЧА)
                                   fridge_capacity INT DEFAULT 1, -- Вместимость хаба (1, 5, 10, 50, 100 котлет)
                                   fridge_cutlets INT DEFAULT 1, -- Сколько платных котлет лежит на складе сейчас
                                   inv_cutlets INT DEFAULT 0, -- Котлеты в кармане (не заправленные в хаб)

                               -- 🤖 СЧЁТЧИКИ ОБОPУДОВАНИЯ (Поддерживают неограниченный закуп доната!)
                                   miner_junior_count INT DEFAULT 0, -- Сколько у юзера Младших Майнеров (★49 Stars)
                                   miner_premium_count INT DEFAULT 0, -- Сколько у юзера Кибер-Бурильщиков (★99 Stars)

                               -- ⏳ ТИТАНОВЫЙ ПРЕДOХРАНИТЕЛЬ СЕРВЕРА Railway (Lazy Evaluation)
                                   last_update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Время последнего ленивого расчета баланса
                                   );
                               """)

            # ----------------------------------------------------------------
            # 📊 2. ТАБЛИЦА ИГРОВОЙ АНАЛИТИКИ И АНТИФРОДА
            # ----------------------------------------------------------------
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS game_stats
                               (
                                   user_id
                                   BIGINT
                                   PRIMARY
                                   KEY,
                                   games_played
                                   INT
                                   DEFAULT
                                   0,
                                   games_won
                                   INT
                                   DEFAULT
                                   0,
                                   today_games_count
                                   INT
                                   DEFAULT
                                   0,
                                   last_game_time
                                   TIMESTAMP
                                   DEFAULT
                                   CURRENT_TIMESTAMP,
                                   FOREIGN
                                   KEY
                               (
                                   user_id
                               ) REFERENCES users
                               (
                                   user_id
                               ) ON DELETE CASCADE
                                   );
                               """)

            # ----------------------------------------------------------------
            # 📸 3. ТАБЛИЦА ПОКУПКИ ПОСТОВ (Спринты и Инста-Лифт)
            # ----------------------------------------------------------------
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS pending_posts
                               (
                                   post_id
                                   SERIAL
                                   PRIMARY
                                   KEY,
                                   user_id
                                   BIGINT
                                   NOT
                                   NULL,
                                   photo_file_id
                                   VARCHAR
                               (
                                   255
                               ) NOT NULL,
                                   post_text TEXT NOT NULL,
                                   target_url VARCHAR
                               (
                                   255
                               ) NOT NULL,
                                   status VARCHAR
                               (
                                   20
                               ) DEFAULT 'pending',
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   FOREIGN KEY
                               (
                                   user_id
                               ) REFERENCES users
                               (
                                   user_id
                               ) ON DELETE CASCADE
                                   );
                               """)

            # ----------------------------------------------------------------
            # 🌐 4. ТАБЛИЦА РЕКЛАМЫ НА БУДУЩЕМ САЙТЕ
            # ----------------------------------------------------------------
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS site_ads
                               (
                                   ad_id
                                   SERIAL
                                   PRIMARY
                                   KEY,
                                   photo_file_id
                                   VARCHAR
                               (
                                   255
                               ) NOT NULL,
                                   post_text TEXT NOT NULL,
                                   target_url VARCHAR
                               (
                                   255
                               ) NOT NULL,
                                   expires_at TIMESTAMP NOT NULL,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                   );
                               """)

            # ----------------------------------------------------------------
            # 👥 5. ТАБЛИЦА КОМАНД (ЖЕСТКИЙ ЛИМИТ 50 ИГРOКОВ)
            # ----------------------------------------------------------------
            await conn.execute("""
                               CREATE TABLE IF NOT EXISTS teams
                               (
                                   team_id
                                   SERIAL
                                   PRIMARY
                                   KEY,
                                   team_name
                                   VARCHAR
                               (
                                   100
                               ) UNIQUE NOT NULL,
                                   captain_id BIGINT UNIQUE NOT NULL,
                                   city VARCHAR
                               (
                                   100
                               ) DEFAULT 'Не указан',
                                   school_num VARCHAR
                               (
                                   50
                               ) DEFAULT 'Не указана',
                                   members_count INT DEFAULT 1,
                                   max_members INT DEFAULT 50,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   FOREIGN KEY
                               (
                                   captain_id
                               ) REFERENCES users
                               (
                                   user_id
                               ) ON DELETE CASCADE
                                   );
                               """)

            print("[DB] Все таблицы империи успешно созданы по новой токеномике!")


db = Database()
