import os
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile  # ТИТАНОВЫЙ ИМПОРТ ДЛЯ ХРАНИЛИЩА RAILWAY
from shared.database import db         # Импортируем твой официальный экземпляр класса базы данных
from shared.strings import get_plural_cutlets

router = Router()


# ----------------------------------------------------------------
# 💰 КОМАНДА: /balance
# ----------------------------------------------------------------
@router.message(Command("balance"))
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id

    # Прямой снайперский запрос баланса из пула
    async with db.pool.acquire() as conn:
        data = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1", user_id)

    if not data:
        await message.answer("⚠️ Ты еще не зарегистрирован в системе! Нажми /start")
        return

    await message.answer(
        f"💰 <b>ТВОЙ КОШЕЛЁК ROFL HUB:</b>\n..................................................\n\n"
        f"🪙 На твоем счету: <code>{data['balance']}</code> рофлов",
        parse_mode="HTML"
    )


# ----------------------------------------------------------------
# 📊 КОМАНДА: /my_stats (МOНОЛИТНЫЙ ВАPИАНТ С ГPАФИКОЙ ИЗ static)
# ----------------------------------------------------------------
@router.message(Command("my_stats"))
async def cmd_my_stats(message: types.Message):
    user_id = message.from_user.id

    # 🎯 Прямой хирургический запрос в PostgreSQL без посредников
    async with db.pool.acquire() as conn:
        data = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

    if not data:
        await message.answer("⚠️ Ты еще не зарегистрирован в системе! Нажми /start")
        return

    # Забираем вместимость холодильника (если поля нет в записи — ставим дефолт 1)
    capacity = data.get("fridge_capacity", 1)

    # 🎰 Динамический подбор неоновой картинки под уровень прокачки из папки static
    if capacity == 1:
        photo_path = "static/fridge_1.jpg"
    elif capacity == 5:
        photo_path = "static/fridge_5.jpg"
    elif capacity == 10:
        photo_path = "static/fridge_10.jpg"
    elif capacity == 50:
        photo_path = "static/fridge_50.jpg"
    else:
        photo_path = "static/fridge_100.jpg" # При значении 100 включится этот международный арт!

    # Обертываем путь в объект локального файла для жесткого диска
    fridge_photo = FSInputFile(photo_path)

    # Красивое формирование кастомного или системного ID Паспорта
    display_id = f"👑 <b>VIP ID:</b> <code>{data['rofl_hub_id']}</code>" if data.get('rofl_hub_id') else f"📎 <b>ID Паспорта:</b> <code>{user_id}</code>"

    # Считываем актуальный запас котлет внутри центрального хаба (где у тебя вбито 42)
    actual_cutlets = data.get("fridge_cutlets", 0)
    all_cutlets = data.get("inv_cutlets", 0)
    cutlets_text = get_plural_cutlets(actual_cutlets)

    # Собираем монолитный пацанский текст профиля
    profile_text = (
        f"🛸 <b>ЛИЧНЫЙ ПРОФИЛЬ ИГРОКА @{message.from_user.username or 'NoName'}</b>\n"
        f"..................................................\n"
        f"{display_id}\n"
        f"💰 <b>Баланс на счету:</b> <code>{data['balance']}</code> рофлов\n"
        f"👥 <b>Твоя банда:</b> <code>{data.get('ref_count', 0)}</code> рефералов\n"
        f"..................................................\n"
        f"📦 <b>РАЗМЕР ХОЛОДИЛЬНИКА: {capacity}</b>\n"
        f"🥩 <b>В холодильнике:</b> {cutlets_text}\n"
        f"🥩 <b>Кибер-котлет всего:</b> {all_cutlets} шт.\n"        
        f"..................................................\n"
        f"📊 <b>БОЕВАЯ СТАТИСТИКА ДУЭЛЕЙ:</b>\n"
        f"• Сыграно раундов: <code>{data.get('games_played', 0)}</code>\n"
        f"• Успешных побед: <code>{data.get('games_won', 0)}</code>"
    )

    # 🚀 СНАЙПЕРСКИЙ ВЫСТРЕЛ: Картинка из папки static + текст под ней на одном экране!
    await message.answer_photo(
        photo=fridge_photo,
        caption=profile_text,
        parse_mode="HTML"
    )


# ----------------------------------------------------------------
# 👥 КОМАНДА: /referral_link
# ----------------------------------------------------------------
@router.message(Command("referral_link"))
async def cmd_referral_link(message: types.Message):
    ref_link = f"https://t.me{message.from_user.id}"
    ref_text = (
        f"👥 <b>ТВОЯ РЕФЕРАЛЬНАЯ ССЫЛКА:</b>\n"
        f"..................................................\n"
        f"<code>{ref_link}</code>\n"
        f"..................................................\n"
        f"🎁 Скопируй ссылку и кидай друзьям! За каждого, кто придёт по твоему приглашению, "
        f"ты МГНОВЕННО получишь <b>+1 000 рофлов</b> на счет!"
    )
    await message.answer(ref_text, parse_mode="HTML")


# ----------------------------------------------------------------
# 🚜 КОМАНДА: /farm (ОБНОВЛЕННАЯ: С ИНЛАЙН-УПРАВЛЕНИЕМ ХАБА)
# ----------------------------------------------------------------
@router.message(Command("my_farm"))
@router.message(Command("farm"))
async def cmd_farm(message: types.Message):
    user_id = message.from_user.id

    # Вытягиваем актуальные данные фермы напрямую из базы Railway
    async with db.pool.acquire() as conn:
        data = await conn.fetchrow(
            """
            SELECT fridge_cutlets, inv_cutlets, miner_junior_count, miner_premium_count
            FROM users
            WHERE user_id = $1
            """,
            user_id
        )

    if not data:
        await message.answer("⚠️ Профиль не найден. Нажми /start")
        return

    total_miners = data.get("miner_junior_count", 0) + data.get("miner_premium_count", 0)

    # 🕹️ СОЗДАЕМ СОЧНУЮ ИНЛАЙН-КЛАВИАТУРУ УПРАВЛЕНИЯ
    # callback_data привязываем напрямую к нашим обработчикам из farm.py!
    farm_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🔋 Заправить 1 котлету", callback_data="farm_action:load_1"),
            types.InlineKeyboardButton(text="⚡ Запустить Завод на 24ч", callback_data="farm_action:run")
        ],
        [
            types.InlineKeyboardButton(text="🏪 Зайти в Магазин /shop", callback_data="open_shop_from_farm")
        ]
    ])

    my_farm_text = (
        f"🚜 <b>КИБЕР-ФЕРМА АВТОДОБЫЧИ МОНЕТ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🤖 Активных роботов на заводе: <b>{total_miners} шт.</b>\n"
        f"• Младшие Майнеры: <code>{data.get('miner_junior_count', 0)} шт.</code>\n"
        f"• Кибер-Бурильщики: <code>{data.get('miner_premium_count', 0)} шт.</code>\n\n"
        f"..................................................\n\n"
        f"📦 <b>СОСТОЯНИЕ ТОПЛИВНОГО ХАБА:</b>\n"
        f"🥩 Запас в Холодильнике: <b>{data.get('fridge_cutlets', 0)} шт.</b>\n"
        f"💼 Котлеты в кармане инвентаря: <code>{data.get('inv_cutlets', 0)} шт.</code>\n\n"
        f"..................................................\n\n"
        f"💿 <b>ИНСТРУКЦИЯ ВОЖАКА:</b>\n"
        f"1. Нажми <b>[Заправить 1 котлету]</b>, чтобы переложить топливо на склад.\n"
        f"2. Нажми <b>[Запустить Завод]</b>, чтобы Бурильщики ушли работать на сутки!"
    )

    await message.answer(my_farm_text, reply_markup=farm_keyboard, parse_mode="HTML")
