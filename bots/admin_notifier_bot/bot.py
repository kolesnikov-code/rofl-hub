import asyncio
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Намертво привязываем чтение .env к корню проекта для безопасности холдинга
# Принудительно и правильно находим корень всего проекта ROFL-HUB
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

# 🔥 МУЛЬТИ-АККАУНТНЫЙ ПЕРЕХВАТ ИЗ ENV (Парсим список через запятую БЕЗ СИНТАКСИЧЕСКИХ ДЫР)
ADMIN_IDS = []
raw_admin_ids = os.getenv("ADMIN_ID", "")
if raw_admin_ids:
    try:
        ADMIN_IDS = [int(uid.strip()) for uid in raw_admin_ids.split(",") if uid.strip().isdigit()]
    except Exception:
        ADMIN_IDS = []

try:
    USERS_CHANNEL_ID = int(os.getenv("USERS_CHANNEL_ID", "0"))
    ADMIN_SECRET_CHANNEL_ID = int(os.getenv("ADMIN_SECRET_CHANNEL_ID", "0"))
except (ValueError, TypeError):
    USERS_CHANNEL_ID = 0
    ADMIN_SECRET_CHANNEL_ID = 0

if not ADMIN_BOT_TOKEN:
    raise RuntimeError("🚨 КРИТИЧЕСКИЙ КРАШ: Переменная ADMIN_BOT_TOKEN отсутствует в .env!")
if not ADMIN_IDS or USERS_CHANNEL_ID == 0 or ADMIN_SECRET_CHANNEL_ID == 0:
    raise RuntimeError("🚨 ОШИБКА БЕЗОПАСНОСТИ: Ключи лимитов или список ADMIN_IDS не заданы в .env!")

from shared.database import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())

# Юзернейм главного бота для моментальной генерации диплинков
MAIN_BOT_USERNAME = os.getenv("MAIN_BOT_USERNAME", "RoflHubGame_Bot").lstrip("@")

MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")


async def notify_user_via_main_bot(user_id: int, text: str) -> bool:
    """Отправляет игроку сообщение от имени главного бота. Ошибки не роняют админ-бот."""
    if not MAIN_BOT_TOKEN:
        logger.warning("[NOTIFY] MAIN_BOT_TOKEN не задан — уведомление игроку %s не отправлено", user_id)
        return False
    main_bot = Bot(token=MAIN_BOT_TOKEN)
    try:
        await main_bot.send_message(user_id, text, parse_mode="HTML")
        return True
    except Exception as e:
        logger.warning("[NOTIFY] не удалось уведомить игрока %s: %s", user_id, e)
        return False
    finally:
        await main_bot.session.close()


class AuctionCreationStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_desc = State()
    waiting_for_price = State()
    waiting_for_step = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@dp.message(Command("start"))
async def cmd_admin_start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ заблокирован. Этот бот — закрытый пульт управления.")
        return
    await message.answer(
        "🛠️ <b>ШТАБ-КВАРТИРА МОДЕРАЦИИ ROFL HUB</b>\n..................................................\n\n"
        "🟢 <b>ДОСТУПНЫЕ КОМАНДЫ ПУЛЬТА:</b>\n"
        "• /new_auction — Запустить лот и вывесить автоматический анонс в канал юзеров\n"
        "• /close_auction [ID] — Принудительно закрыть торги\n"
        "• /report — Суточный отчёт: DAU, продажи, когорты за 30 дней\n"
        "• /gift [ID] [сумма] — Подарить рофлы игроку (отрицательная сумма — штраф)\n"
        "• /block [ID] — Заблокировать игрока · /unblock [ID] — Разблокировать\n"
        "• /find [ID или @username] — Досье игрока\n",
        parse_mode="HTML"
    )


# ============================================================================
# 🛡️ МОДЕРАЦИЯ И ЭКОНОМИКА (Блок 4): блокировки, подарки, отчёт по запросу
# ============================================================================
from shared.db_admin import admin_gift_coins, collect_daily_report, format_daily_report, set_user_blocked  # noqa: E402
from shared.ledger import UserNotFound  # noqa: E402


@dp.message(Command("report"))
async def admin_daily_report(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    async with db.pool.acquire() as conn:
        report = await collect_daily_report(conn)
    await message.answer(format_daily_report(report), parse_mode="HTML")


def _parse_id_arg(text: str) -> int | None:
    parts = text.split()
    return int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else None


@dp.message(Command("block"))
async def admin_block_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    user_id = _parse_id_arg(message.text)
    if user_id is None:
        await message.answer("⚠️ Пример: <code>/block 123456789</code>", parse_mode="HTML")
        return
    async with db.pool.acquire() as conn:
        found = await set_user_blocked(conn, user_id, True)
    if not found:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    await notify_user_via_main_bot(user_id, "🚫 <b>Твой аккаунт заблокирован администрацией ROFL HUB.</b>")
    await message.answer(f"🚫 Игрок <code>{user_id}</code> заблокирован: бот перестал отвечать на его действия.",
                         parse_mode="HTML")


@dp.message(Command("unblock"))
async def admin_unblock_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    user_id = _parse_id_arg(message.text)
    if user_id is None:
        await message.answer("⚠️ Пример: <code>/unblock 123456789</code>", parse_mode="HTML")
        return
    async with db.pool.acquire() as conn:
        found = await set_user_blocked(conn, user_id, False)
    if not found:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    await notify_user_via_main_bot(user_id, "✅ <b>Твой аккаунт разблокирован. С возвращением в ROFL HUB!</b>")
    await message.answer(f"✅ Игрок <code>{user_id}</code> разблокирован.", parse_mode="HTML")


@dp.message(Command("gift"))
async def admin_gift(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].lstrip("-").isdigit() or int(parts[2]) == 0:
        await message.answer("⚠️ Пример: <code>/gift 123456789 5000</code> (отрицательная сумма — штраф)",
                             parse_mode="HTML")
        return
    user_id, amount = int(parts[1]), int(parts[2])

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
                new_balance = await admin_gift_coins(conn, user_id, amount, message.from_user.id)
    except UserNotFound:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    except Exception as e:
        await message.answer(f"❌ Операция отклонена: {e}")
        return

    if amount > 0:
        await notify_user_via_main_bot(
            user_id, f"🎁 <b>Администрация ROFL HUB подарила тебе {amount} рофлов!</b> Проверь /profile")
    await message.answer(
        f"💰 Готово! Игроку <code>{user_id}</code> {'начислено' if amount > 0 else 'списано'} "
        f"<b>{abs(amount)} рофлов</b>. Новый баланс: <b>{new_balance}</b>.", parse_mode="HTML")


@dp.message(Command("find"))
async def admin_find_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("⚠️ Пример: <code>/find 123456789</code> или <code>/find @username</code>",
                             parse_mode="HTML")
        return
    arg = parts[1]

    async with db.pool.acquire() as conn:
        if arg.startswith("@"):
            user = await conn.fetchrow("SELECT * FROM users WHERE LOWER(username) = LOWER($1)", arg[1:])
        elif arg.isdigit():
            user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", int(arg))
        else:
            user = None
        if not user:
            await message.answer("❌ Игрок не найден.")
            return
        stars = await conn.fetchval(
            "SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments WHERE user_id = $1", user["user_id"])
        quiz = await conn.fetchrow(
            "SELECT quiz_level, quiz_correct_total FROM game_stats WHERE user_id = $1", user["user_id"])

    await message.answer(
        f"🕵️ <b>ДОСЬЕ ИГРОКА</b>\n"
        f"🆔 <code>{user['user_id']}</code> · @{user['username'] or '—'} · {user['display_name'] or '—'}\n"
        f"💰 Баланс: <b>{user['balance']}</b> · 🧠 Уровень: {quiz['quiz_level'] if quiz else 0}\n"
        f"💵 Потрачено Stars: <b>★ {stars}</b>\n"
        f"🏆 Команда: {user['team_id'] or 'нет'} · 🌐 Язык: {user['lang']}\n"
        f"📅 Регистрация: {user['created_at']:%d.%m.%Y} · Был в сети: {user['last_seen_at']:%d.%m.%Y %H:%M}\n"
        f"🚫 Блокировка: <b>{'ДА' if user['is_blocked'] else 'нет'}</b>",
        parse_mode="HTML")

@dp.message(Command("new_auction"))
async def admin_new_auction(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.set_state(AuctionCreationStates.waiting_for_title)
    await message.answer("🎁 <b>ШАГ 1 ИЗ 4: НАЗВАНИЕ ЛОТА</b>\n\nВведи название: <i>VIP ID или пост в Instagram</i>):", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_title)
async def process_auc_title(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.update_data(auc_title=message.text.strip())
    await state.set_state(AuctionCreationStates.waiting_for_desc)
    await message.answer("📝 <b>ШАГ 2 ИЗ 4: ОПИСАНИЕ ЛОТА</b>\n\nНапиши условия аукциона для выжигания монет:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_desc)
async def process_auc_desc(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.update_data(auc_desc=message.text.strip())
    await state.set_state(AuctionCreationStates.waiting_for_price)
    await message.answer("💰 <b>ШАГ 3 ИЗ 4: СТАРТОВАЯ ЦЕНА</b>\n\nУкажи начальную цену в рофлах:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_price)
async def process_auc_price(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    if not message.text.strip().isdigit():
        await message.answer("❌ Цена должна быть числом! Введи заново:")
        return
    await state.update_data(auc_price=int(message.text.strip()))
    await state.set_state(AuctionCreationStates.waiting_for_step)
    await message.answer("🚀 <b>ШАГ 4 ИЗ 4: МИНИМАЛЬНЫЙ ШАГ</b>\n\nВведи минимальный шаг повышения цены:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_step)
async def process_auc_finalize(message: types.Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id): return
    if not message.text.strip().isdigit():
        await message.answer("❌ Шаг должен быть числом! Введи заново:")
        return

    step = int(message.text.strip())
    data = await state.get_data()
    await state.clear()

    async with db.pool.acquire() as conn:
        auction_id = await conn.fetchval(
            """
            INSERT INTO auctions (item_title, item_desc, current_price, min_step, status)
            VALUES ($1, $2, $3, $4, 'open') RETURNING auction_id
            """,
            data.get("auc_title"), data.get("auc_desc"), data.get("auc_price"), step
        )

    # 🔥 БЕЗУПРЕЧНЫЙ ФИКС СЛЭШЕЙ: Ссылка собирается строго с разделителем /
    deep_link = f"https://t.me/{MAIN_BOT_USERNAME}?start=auction_{auction_id}"

    channel_post_text = (
        f"🔥 <b>БИТВА ВОЖАКОВ ЗА ВЕЧНЫЙ ПОНТ И VIP-ПРИЗЫ!</b>\n"
        f"..................................................\n\n"
        f"Объявляются официальные торги холдинга экосистемы!\n\n"
        f"🎁 Лот раунда: <b>{data.get('auc_title')}</b>\n"
        f"📝 Детали: <i>{data.get('auc_desc')}</i>\n\n"
        f"💰 Стартовая цена: <b>{data.get('auc_price')} рофлов</b>\n"
        f"🚀 Шаг повышения: <b>+{step} рофлов</b>\n\n"
        f"..................................................\n"
        f"⚠️ <i>Ставки возвратные: если тебя перебили, монеты вернутся на баланс. Платит только победитель!</i>\n\n"
        f"👇 <b>КЛИКАЙ ПО ССЫЛКЕ НИЖЕ ДЛЯ ВХОДА И СТАВКИ:</b>\n"
        f"{deep_link}"
    )

    try:
        await bot.send_message(chat_id=USERS_CHANNEL_ID, text=channel_post_text, parse_mode="HTML")
        channel_status = "🟢 <b>Анонс лота успешно опубликован в USERS_CHANNEL_ID!</b>"
    except Exception as e:
        logger.error(f"[CHANNEL_POST_ERROR] Не удалось отправить пост в канал юзеров: {e}")
        channel_status = f"❌ <b>Ошибка публикации в USERS_CHANNEL_ID:</b> {e}"

    success_text = (
        f"👑 <b>ЛОТ АУКЦИОНА УСПЕШНО СФОРМИРОВАН!</b>\n"
        f"..................................................\n\n"
        f"🆔 ID Лота в базе Railway: <code>{auction_id}</code>\n"
        f"🎁 Название: <b>{data.get('auc_title')}</b>\n"
        f"💰 Стартовая цена: <b>{data.get('auc_price')} рофлов</b>\n\n"
        f"..................................................\n\n"
        f"{channel_status}\n\n"
        f"🔗 Ссылка: <code>{deep_link}</code>"
    )
    await message.answer(success_text, parse_mode="HTML")

@dp.message(Command("close_auction"))
async def admin_close_auction(message: types.Message, bot: Bot):
    if not is_admin(message.from_user.id): return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("⚠️ Пример: <code>/close_auction 1</code>", parse_mode="HTML")
        return
    if not parts[1].isdigit():
        await message.answer("❌ ID лота должен быть числом.")
        return
    auction_id = int(parts[1])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
            if not auction or auction["status"] != "open":
                await message.answer("❌ Лот не существует или уже закрыт.")
                return
            await conn.execute("UPDATE auctions SET status = 'closed' WHERE auction_id = $1", auction_id)

    winner_id = auction["highest_bidder_id"]
    if winner_id:
        # Игрок общается с ГЛАВНЫМ ботом: админ-бот не может писать ему первым (chat not found)
        await notify_user_via_main_bot(
                winner_id,
                f"🏆 <b>Ты победил в аукционе за лот «{auction['item_title']}»!</b>\n"
                f"Финальная цена: <b>{auction['current_price']} рофлов</b>. Администрация свяжется с тобой для выдачи приза.",
        )
        try:
            await bot.send_message(
                USERS_CHANNEL_ID,
                f"🏁 <b>Аукцион за лот «{auction['item_title']}» завершён!</b>\n"
                f"👑 Победитель: ID <code>{winner_id}</code> · 💰 {auction['current_price']} рофлов",
                parse_mode="HTML")
        except Exception as e:
            logger.warning("[AUCTION_CLOSE] не удалось опубликовать итог в канал: %s", e)

    await message.answer(
        f"🏁 <b>АУКЦИОН №{auction_id} ЗАКРЫТ ИЗ ШТАБА!</b>\n\n"
        f"🎁 Лот: <b>{auction['item_title']}</b>\n"
        f"👑 Победитель: ID <code>{auction['highest_bidder_id'] if auction['highest_bidder_id'] else 'Ставок нет'}</code>\n"
        f"💵 Финальная цена: <b>{auction['current_price']} рофлов</b>.",
        parse_mode="HTML"
    )


# ============================================================================
# 📊 2. АВТОНОМНЫЙ ДЕМОН СКВОЗНОЙ АНАЛИТИКИ ПО ЧАСАМ UTC (00, 06, 12, 18)
# ============================================================================
async def dynamic_analytics_daemon(bot: Bot):
    """
    Фоновый демон сбора метрик холдинга ROFL HUB CORE.
    Срабатывает строго в 06:00, 12:00, 18:00 UTC (экспресс-срез)
    и в 00:00 UTC (глубокий суточный когортный анализ).
    """
    logger.info("⏳ Астрономический аналитический демон успешно запущен по UTC!")

    # Флаг-предохранитель, чтобы бот не отправлял отчет каждую секунду внутри одной минуты
    last_triggered_hour = -1

    while True:
        try:
            await asyncio.sleep(20)

            now_utc = datetime.now(timezone.utc)
            current_hour = now_utc.hour
            current_minute = now_utc.minute
            current_date = now_utc.date()

            # Проверяем, наступила ли целевая минута (00 минут) нужного часа
            if current_hour in [0, 6, 12, 18] and current_minute == 0:
                # Если в этот час триггер уже срабатывал — пропускаем тик
                if current_hour == last_triggered_hour:
                    continue

                last_triggered_hour = current_hour
                logger.info(f"📊 Наступила контрольная точка времени: {current_hour}:00 UTC. Сбор данных...")

                async with db.pool.acquire() as conn:
                    # Сбор базовых агрегатных метрик со всей базы Railway
                    total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
                    total_clans = await conn.fetchval("SELECT COUNT(*) FROM teams")
                    total_stars_revenue = await conn.fetchval("SELECT SUM(stars_amount) FROM star_payments")
                    total_coins_mass = await conn.fetchval("SELECT SUM(balance) FROM users")

                    total_played = await conn.fetchval("SELECT SUM(games_played) FROM game_stats")
                    total_won = await conn.fetchval("SELECT SUM(games_won) FROM game_stats")
                    total_wins_rps = await conn.fetchval("SELECT SUM(daily_wins_rps) FROM game_stats")
                    total_wins_hl = await conn.fetchval("SELECT SUM(daily_wins_hl) FROM game_stats")
                    total_wins_quiz = await conn.fetchval("SELECT SUM(daily_wins_quiz) FROM game_stats")

                stars_total = total_stars_revenue if total_stars_revenue else 0
                coins_total = total_coins_mass if total_coins_mass else 0
                games_played_all = total_played if total_played else 0
                games_won_all = total_won if total_won else 0

                # ====================================================================
                # 📢 ВЫДАЧА ЭКСПРЕСС-ОТЧЕТОВ (В 06:00, 12:00, 18:00 UTC)
                # ====================================================================
                if current_hour in (0, 6, 12, 18) and current_minute == 0:
                    express_text = (
                        f"⏱️ <b>ЭКСПРЕСС-АНАЛИТИКА ЭКОСИСТЕМЫ ({current_hour}:00 UTC)</b>\n"
                        f"..................................................\n\n"
                        f"👥 Всего игроков в СУБД: <b>{total_users} чел.</b>\n"
                        f"🏆 Активных Кланов/Команд: <b>{total_clans} банд</b>\n\n"
                        f"🎮 Проведено раундов: <b>{games_played_all} игр</b>\n"
                        f"👑 Одержано побед юзерами: <code>{games_won_all} раз</code>\n\n"
                        f"💵 Валовый кэш Stars: <b>★ {stars_total} XTR</b>\n"
                        f"🪙 Масса фантиков в СУБД: <code>{coins_total} рофлов</code>\n"
                        f"..................................................\n"
                        f"<i>⚙️ Следующий системный срез произойдет строго по графику UTC.</i>"
                    )
                    await bot.send_message(chat_id=ADMIN_SECRET_CHANNEL_ID, text=express_text, parse_mode="HTML")
                    logger.info(f"🟢 Экспресс-отчет {current_hour}:00 UTC отправлен в Тайную Комнату.")

                # ====================================================================
                # 👑 ПОЛНОЧНЫЙ ИТОГОВЫЙ СРЕЗ И КОГОРТНЫЙ АНАЛИЗ (СТРОГО В 00:00 UTC)
                # ====================================================================
                if current_hour == 0:
                    async with db.pool.acquire() as conn:
                        cohort_data = await conn.fetchrow("""
                                                          WITH user_spend
                                                                   AS (SELECT user_id, COALESCE(SUM(stars_amount), 0) as total_spend
                                                                       FROM star_payments
                                                                       GROUP BY user_id)
                                                          SELECT COUNT(CASE WHEN total_spend = 0 THEN 1 END)                          as f2p_count,
                                                                 COUNT(CASE WHEN total_spend > 0 AND total_spend <= 100 THEN 1 END)   as light_count,
                                                                 COUNT(CASE WHEN total_spend > 100 AND total_spend <= 500 THEN 1 END) as normal_count,
                                                                 COUNT(CASE WHEN total_spend > 500 THEN 1 END)                        as whale_count
                                                          FROM user_spend;
                                                          """)

                    f2p = cohort_data["f2p_count"] if cohort_data else 0
                    light = cohort_data["light_count"] if cohort_data else 0
                    normal = cohort_data["normal_count"] if cohort_data else 0
                    whale = cohort_data["whale_count"] if cohort_data else 0
                    non_paying_total = max(0, total_users - (light + normal + whale))

                    daily_text = (
                        f"👑 <b>ИТОГОВЫЙ СУТОЧНЫЙ ОТЧЕТ ХОЛДИНГА (00:00 UTC)</b>\n"
                        f"..................................................\n\n"
                        f"📊 <b>КОГОРТНЫЙ АНАЛИЗ ПСИХОЛОГИИ И ТРАТ (LTV):</b>\n"
                        f"🛑 <b>F2P Халявщики (0 ★):</b> <code>{non_paying_total} чел.</code>\n"
                        f"🪵 <b>Микро-донатеры (до 100 ★):</b> <b>{light} чел.</b>\n"
                        f"⚡ <b>Нормы (100-500 ★):</b> <b>{normal} чел.</b>\n"
                        f"👑 <b>КИТЫ ЭКОСИСТЕМЫ (500+ ★):</b> <u>{whale} чел.</u>\n\n"
                        f"🎯 <b>АКТИВНОСТЬ ПО ТИПАМ ИГР ЗА ВСЕ ВРЕМЯ:</b>\n"
                        f"• Раундов в КНБ: <code>{total_wins_rps if total_wins_rps else 0} раундов</code>\n"
                        f"• Раундов в Больше/Меньше: <code>{total_wins_hl if total_wins_hl else 0} раундов</code>\n"
                        f"• Пройдено тестов Викторины: <code>{total_wins_quiz if total_wins_quiz else 0} вопросов</code>\n\n"
                        f"..................................................\n"
                        f"<i>📈 Суточный срез зафиксирован под елочкой в канале навсегда. Данные СУБД синхронизированы.</i>"
                    )
                    await bot.send_message(chat_id=ADMIN_SECRET_CHANNEL_ID, text=daily_text, parse_mode="HTML")
                    logger.info("👑 Суточный глубокий когортный отчет успешно опубликован в 00:00 UTC!")

            # Сброс триггера блокировки часов, когда целевая минута прошла
            if current_minute != 0:
                last_triggered_hour = -1

        except Exception as e:
            logger.error(f"[ANALYTICS_DAEMON_CRASH] Критический сбой демона: {e}")


# ============================================================================
# 🏎️ ИНИЦИАЛИЗАЦИЯ И СТАРТ СЕКРЕТНОГО АДМИН-БОТА
# ============================================================================
async def main():
    bot = Bot(token=ADMIN_BOT_TOKEN)
    await db.connect()
    await db.create_tables()

    # Запускаем аналитического демона в асинхронном фоне Event Loop!
    asyncio.create_task(dynamic_analytics_daemon(bot))

    logger.info("🟢 СЕКРЕТНЫЙ АДМИН-БОТ С АНАЛИТИЧЕСКИМ ШЛЮЗОМ ЗАПУЩЕН!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
