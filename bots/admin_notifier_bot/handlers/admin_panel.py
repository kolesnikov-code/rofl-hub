import logging
from datetime import datetime, timedelta, timezone
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)

# 🔥 ЖЕСТКИЙ СПИСОК АДМИНИСТРАТOPOВ (Вставь сюда свой Telegram ID)
ADMIN_IDS = [8895172416]  # Твой верифицированный ID Паспорта


class AuctionStates(StatesGroup):
    waiting_for_lot = State()
    waiting_for_price = State()


def is_admin_filter(user_id: int) -> bool:
    """Проверка на права Главного Администратора империи"""
    return user_id in ADMIN_IDS


# ============================================================================
# 👑 1. ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА: /admin
# ============================================================================
@router.message(Command("admin"))
async def cmd_admin_main(message: types.Message):
    if not is_admin_filter(message.from_user.id):
        await message.answer("❌ Доступ заблокирован. У тебя нет прав Администратора.")
        return

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔥 Запустить VIP-Аукцион", callback_data="admin_action:start_auction")],
        [types.InlineKeyboardButton(text="📊 Сводная Аналитика БД", callback_data="admin_action:get_db_stats")]
    ])

    await message.answer(
        "🛠️ <b>ПАНЕЛЬ УПРАВЛЕНИЯ ЭКОСИСТЕМОЙ ROFL HUB</b>\n"
        "..................................................\n\n"
        "Вожак, приветствуем в штабе модерации. Отсюда ты можешь принудительно "
        "запускать аукционы элитарных ID и просматривать финансовые отчеты Railway.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# ============================================================================
# 🎰 2. ФУНКЦИОНАЛ VIP-АУКЦИОНОВ (DEEP LINK КОНТУР ДЛЯ КАНАЛА)
# ============================================================================
@router.callback_query(F.data == "admin_action:start_auction")
async def admin_trigger_auction_state(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin_filter(callback.from_user.id):
        await callback.answer("Отказ в доступе", show_alert=True)
        return

    await callback.answer()
    await state.set_state(AuctionStates.waiting_for_lot)
    await callback.message.answer("⌨️ Введи блатное имя лота для торгов (например: 777 или 666):")


@router.message(AuctionStates.waiting_for_lot)
async def process_auction_lot_name(message: types.Message, state: FSMContext):
    lot_name = message.text.strip()
    await state.update_data(auction_lot=lot_name)
    await state.set_state(AuctionStates.waiting_for_price)
    await message.answer(f"💰 Лот <b>{lot_name}</b> принят. Укажи стартовую цену в монетах (например: 10000):",
                         parse_mode="HTML")


@router.message(AuctionStates.waiting_for_price)
async def process_auction_price_and_finalize(message: types.Message, state: FSMContext):
    price_text = message.text.strip()
    if not price_text.isdigit():
        await message.answer("❌ Цена должна быть целым числом! Введи заново:")
        return

    start_price = int(price_text)
    data = await state.get_data()
    lot_name = data.get("auction_lot")
    await state.clear()

    # Устанавливаем время жизни аукциона — ровно 24 часа с текущей секунды UTC
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    async with db.pool.acquire() as conn:
        # Гасим прошлые активные торги на всякий случай
        await conn.execute("UPDATE active_auction SET is_active = 0 WHERE is_active = 1")
        # Создаем новую запись торгов
        await conn.execute(
            """
            INSERT INTO active_auction (vip_id_target, current_max_bid, expires_at, is_active)
            VALUES ($1, $2, $3, 1)
            """,
            lot_name, start_price, expires_at
        )

    # Формируем бесшовную deep-link ссылку-перелет в юзер-бота, как ты и задумал!
    deep_link_url = f"https://t.me_{lot_name}"

    success_text = (
        f"🚀 <b>ТОРГИ ЗАПУЩЕНЫ И СИНХРОНИЗИРОВАНЫ В БД!</b>\n"
        f"..................................................\n\n"
        f"👑 Лот: <b>VIP ID {lot_name}</b>\n"
        f"💵 Стартовая цена: <b>{start_price} рофлов</b>\n"
        f"⏳ Закрытие: через 24 часа (строго по UTC Railway)\n\n"
        f"..................................................\n\n"
        f"📢 <b>Скопируй этот текст и отправь в официальный Канал:</b>\n\n"
        f"🔥 <b>БИТВА ОЛИГАРХОВ ЗА ВЕЧНЫЙ ПОНТ!</b>\n"
        f"Объявляются торги за элитарный паспорт империи — 👑 <b>VIP ID {lot_name}</b>!\n"
        f"Перебивай ставки соперников и забери высший статус на свой аккаунт!\n\n"
        f"👇 <b>КЛИКАЙ ПО ССЫЛКЕ ДЛЯ ПЕРЕЛЕТА В БОТ И СТАВКИ:</b>\n"
        f"{deep_link_url}"
    )
    await message.answer(success_text, parse_mode="HTML")


# ============================================================================
# 📸 3. МОДУЛЬ МОДЕРАЦИИ «ИНСТА-ЛИФТ» (РЕАКЦИЯ НА КЛИКИ АДМИНА)
# ============================================================================
@router.callback_query(F.data.startswith("insta_mod:"))
async def process_insta_lift_moderation(callback: types.CallbackQuery):
    if not is_admin_filter(callback.from_user.id):
        await callback.answer("Отказ в доступе", show_alert=True)
        return

    await callback.answer()
    _, action, post_id = callback.data.split(":")
    post_id = int(post_id)

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Забираем заявку из таблицы pending_posts
            post = await conn.fetchrow("SELECT user_id, status FROM pending_posts WHERE post_id = $1 FOR UPDATE",
                                       post_id)

            if not post:
                await callback.message.edit_text("⚠️ Заявка не найдена в базе данных.")
                return

            if post["status"] != "pending":
                await callback.message.edit_text(f"⚠️ Эта заявка уже была обработана ранее. Статус: {post['status']}")
                return

            target_user_id = post["user_id"]

            if action == "approve":
                # Одобрение: меняем статус на approved и атомарно начисляем 100 монет юзеру
                await conn.execute("UPDATE pending_posts SET status = 'approved' WHERE post_id = $1", post_id)
                await conn.execute("UPDATE users SET balance = balance + 100 WHERE user_id = $1", target_user_id)

                await callback.message.edit_text(
                    "✅ <b>Заявка одобрена! +100 монет успешно отправлены на Railway юзеру.</b>", parse_mode="HTML")

                # Здесь можно прописать отправку уведомления в личку юзеру через Bot(token=...) при желании
                print(f"📸 [INSTA_LIFT] Заявка {post_id} одобрена админом. Юзер {target_user_id} получил бонус.")

            elif action == "reject":
                # Отклонение: просто меняем статус на rejected
                await conn.execute("UPDATE pending_posts SET status = 'rejected' WHERE post_id = $1", post_id)
                await callback.message.edit_text("❌ <b>Заявка отклонена. Бонус аннулирован.</b>", parse_mode="HTML")


# ============================================================================
# 📊 4. СВОДНАЯ СИСТЕМНАЯ АНАЛИТИКА ЭКОСИСТЕМЫ
# ============================================================================
@router.callback_query(F.data == "admin_action:get_db_stats")
async def admin_get_database_stats(callback: types.CallbackQuery):
    if not is_admin_filter(callback.from_user.id):
        await callback.answer("Отказ в доступе", show_alert=True)
        return

    await callback.answer()

    async with db.pool.acquire() as conn:
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
        total_clans = await conn.fetchval("SELECT COUNT(*) FROM teams")
        total_stars_revenue = await conn.fetchval("SELECT SUM(stars_amount) FROM star_payments")
        total_coins = await conn.fetchval("SELECT SUM(balance) FROM users")

    stars_revenue = total_stars_revenue or 0
    coins_in_circulation = total_coins or 0

    stats_text = (
        f"📊 <b>СВОДНАЯ СТАТИСТИКА ИМПЕРИИ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"👥 Зарегистрировано вожаков в БД: <b>{total_users} чел.</b>\n"
        f"🏆 Создано школьных банд/кланов: <b>{total_clans} шт.</b>\n\n"
        f"💎 <b>ФИНАНСОВЫЙ КОНТУРStars (Фрагмент):</b>\n"
        f"• Общий валовый оборот: <b>{stars_revenue} ★ Stars</b>\n"
        f"• Монет в обороте у детей: <code>{coins_in_circulation} рофлов</code>\n"
        f"..................................................\n"
        f"<i>Серверный таймер Railway функционирует в штатном режиме 24/7.</i>"
    )
    await callback.message.answer(stats_text, parse_mode="HTML")
