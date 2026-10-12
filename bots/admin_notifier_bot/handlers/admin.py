import logging
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)

# Жесткий фикс безопасности: пульт доступен ТОЛЬКО твоему Telegram ID
ADMIN_TESTER_ID = 227653457


class AuctionCreationStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_desc = State()
    waiting_for_price = State()
    waiting_for_step = State()


# Фильтр для проверки прав администратора
def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_TESTER_ID


# ============================================================================
# 👑 1. ТОЧКА СТАРТА СОЗДАНИЯ ЛОТА: /new_auction
# ============================================================================
@router.message(Command("new_auction"))
async def cmd_new_auction(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(AuctionCreationStates.waiting_for_title)
    await message.answer(
        "🎁 <b>ЗАПУСК КОНВЕЙЕРА АУКЦИОНА: ШАГ 1 ИЗ 4</b>\n\n"
        "Введи краткое и сочное название лота (например: <i>Telegram Premium 1 год</i>):",
        parse_mode="HTML"
    )


@router.message(AuctionCreationStates.waiting_for_title)
async def process_auc_title(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    title = message.text.strip()

    await state.update_data(auc_title=title)
    await state.set_state(AuctionCreationStates.waiting_for_desc)
    await message.answer("📝 <b>ШАГ 2 ИЗ 4: ОПИСАНИЕ ЛОТА</b>\n\nНапиши подробное описание приза для детей:")


@router.message(AuctionCreationStates.waiting_for_desc)
async def process_auc_desc(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    desc = message.text.strip()

    await state.update_data(auc_desc=desc)
    await state.set_state(AuctionCreationStates.waiting_for_price)
    await message.answer("💰 <b>ШАГ 3 ИЗ 4: СТАРТОВАЯ ЦЕНА</b>\n\nВведи начальную цену лота в рофлах (число без букв):")


@router.message(AuctionCreationStates.waiting_for_price)
async def process_auc_price(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    try:
        price = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Ошибка! Введи корректное целое число:")
        return

    await state.update_data(auc_price=price)
    await state.set_state(AuctionCreationStates.waiting_for_step)
    await message.answer(
        "🚀 <b>ШАГ 4 ИЗ 4: МИНИМАЛЬНЫЙ ШАГ</b>\n\nВведи минимальный шаг повышения ставки в рофлах (например: 500):")


@router.message(AuctionCreationStates.waiting_for_step)
async def process_auc_step_finalize(message: types.Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id): return
    try:
        step = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Ошибка! Введи корректное целое число:")
        return

    data = await state.get_data()
    await state.clear()

    # Атомарно записываем новый лот в СУБД Railway с заморозкой статуса
    async with db.pool.acquire() as conn:
        auction_id = await conn.fetchval(
            """
            INSERT INTO auctions (item_title, item_desc, current_price, min_step, status)
            VALUES ($1, $2, $3, $4, 'open') RETURNING auction_id
            """,
            data.get("auc_title"), data.get("auc_desc"), data.get("auc_price"), step
        )

    # Вытягиваем username нашего бота для генерации красивой диплинк-ссылки
    bot_info = await bot.get_me()
    bot_username = bot_info.username

    # 🔥 ГЕНЕРАЦИЯ КРАСИВОЙ DEEP-LINK ССЫЛКИ ДЛЯ ТЕЛЕГРАМ-КАНАЛА
    deep_link = f"https://t.me{bot_username}?start=auction_{auction_id}"

    success_text = (
        f"👑 <b>ЛОТ АУКЦИОНА УСПЕШНО СФОРМИРОВАН!</b>\n"
        f"..................................................\n\n"
        f"🆔 ID Лота в базе: <code>{auction_id}</code>\n"
        f"🎁 Название: <b>{data.get('auc_title')}</b>\n"
        f"💰 Стартовая цена: <b>{data.get('auc_price')} рофлов</b>\n"
        f"🚀 Минимальный шаг: <b>{step} рофлов</b>\n\n"
        f"..................................................\n\n"
        f"🔗 <b>ТВОЯ БOЕВАЯ DEEP-LINK ССЫЛКА ДЛЯ КAНAЛA:</b>\n"
        f"<code>{deep_link}</code>\n\n"
        f"<i>Скопируй эту ссылку (кликни по ней) и вшивай её в кнопку поста под Reels! При клике на неё ребенок будет сразу лететь на карточку ставки!</i>"
    )
    await message.answer(success_text, parse_mode="HTML")


# ============================================================================
# 🛑 2. ЭКСТРЕННОЕ ЗAКРЫТИЕ ИГРЫ И ВЫДАЧА ПРИЗА: /close_auction
# ============================================================================
@router.message(Command("close_auction"))
async def cmd_close_auction(message: types.Message):
    if not is_admin(message.from_user.id): return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("⚠️ Введи команду вместе с ID лота. Пример: <code>/close_auction 1</code>",
                             parse_mode="HTML")
        return

    try:
        auction_id = int(parts[1])
    except ValueError:
        await message.answer("❌ Неверный формат ID лота.")
        return

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
            if not auction:
                await message.answer("❌ Лот с таким ID не найден в Railway.")
                return
            if auction["status"] != "open":
                await message.answer("⚠️ Этот аукцион уже закрыт.")
                return

            # Намертво закрываем торги
            await conn.execute("UPDATE auctions SET status = 'closed' WHERE auction_id = $1", auction_id)

    await message.answer(
        f"🏁 <b>АУКЦИОН №{auction_id} ОФИЦИАЛЬНО ЗАКРЫТ АДМИНИСТРАЦИЕЙ!</b>\n\n"
        f"🎁 Лот: <b>{auction['item_title']}</b>\n"
        f"👑 Победитель раунда: ID <code>{auction['highest_bidder_id'] if auction['highest_bidder_id'] else 'Ставок не было'}</code>\n"
        f"💵 Финальная цена: <b>{auction['current_price']} рофлов</b>.\n\n"
        f"<i>Все невозвратные ставки соперников сожжены. Баланс СУБД очищен от лишних монет! Свяжись с победителем для выдачи физического приза.</i>",
        parse_mode="HTML"
    )
