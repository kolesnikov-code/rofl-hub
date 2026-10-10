import logging
import random
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db
from shared.db_clans import create_new_team_in_db

router = Router()
logger = logging.getLogger(__name__)


class ClanCreationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_motto = State()  # 🔥 Вместо города — Девиз команды!
    waiting_for_symbol = State()  # 🔥 Вместо школы — Эмодзи-символ с клавиатуры!
    waiting_for_search = State()


def get_cancel_keyboard() -> types.InlineKeyboardMarkup:
    """Кнопка экстренной отмены FSM-процесса на любом шаге опроса"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Прервать создание команды", callback_data="clan_action:cancel_fsm")]
    ])


# ============================================================================
# 👥 1. ЦЕНТРАЛЬНЫЙ ДАШБОРД КОМАНД И КЛАНОВ: /my_team И /all_teams
# ============================================================================
@router.message(Command("clan"))
@router.message(Command("clans"))
@router.message(Command("my_team"))
@router.message(Command("all_teams"))
@router.callback_query(F.data == "clan_main_menu")
async def cmd_clan_hub(message: types.Message or types.CallbackQuery):
    is_callback = isinstance(message, types.CallbackQuery)
    user_id = message.from_user.id if is_callback else message.chat.id
    target_msg = message.message if is_callback else message

    if is_callback:
        # 🔥 ИСПРАВЛЕНО: Чистый, эталонный синтаксис aiogram без лишних переменных!
        await message.answer()

    # Проверяем, ввёл ли пользователь текстовую команду поиска команд напрямую
    is_search_cmd = False
    if not is_callback and message.text.startswith("/all_teams"):
        is_search_cmd = True

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1", user_id)

        if user and user["team_id"] is not None and not is_search_cmd:
            # ЮЗЕР УЖЕ В КЛАНЕ — ВЫВОДИМ ЕГО СТЕРИЛЬНЫЙ ДАШБОРД БЕЗ СЛЕДКИ ЗА ШКОЛАМИ
            team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1", user["team_id"])

            # Показываем юзернейм капитана только членам этой же банды (Анти-буллинг защита!)
            captain_row = await conn.fetchrow("SELECT username FROM users WHERE user_id = $1", team["captain_id"])
            captain_name = f"@{captain_row['username']}" if captain_row else f"ID {team['captain_id']}"

            status_clan = "👑 СТАТУС: КЛАН ИМПЕРИИ" if team["max_members"] >= 1000 else "👥 СТАТУС: ОБЫЧНАЯ КОМАНДА"

            clan_text = (
                f"🏆 <b>ИНФОРМАЦИОННЫЙ ДАШБОРД ТВОЕЙ КОМАНДЫ</b>\n"
                f"..................................................\n\n"
                f"📌 Название: <b>{team['team_name']}</b>\n"
                f"⚡ {status_clan}\n"
                f"👤 Капитан банды: <b>{captain_name}</b>\n"
                f"💬 Девиз: <i>«{team['city']}»</i>\n"
                f"🔮 Символ эмблемы: {team['school_num']}\n\n"
                f"👥 Состав участников: <b>{team['members_count']} / {team['max_members']} чел.</b>\n"
                f"..................................................\n\n"
                f"👇 <b>НАВИГАЦИЯ:</b>"
            )
            kb = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
            ])
            await target_msg.answer(clan_text, reply_markup=kb, parse_mode="HTML")
            return

    # ЮЗЕР БЕЗ КЛАНА (ИЛИ КЛИКНУЛ НА КOМАНДУ ПОИСКА)
    welcome_text = (
        f"👥 <b>ЦЕНТРАЛЬНЫЙ ОФИС КОМАНД И КЛАНОВ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"Изначально ВСЕГДА создаётся обычная Команда за 100 000 рофлов до 50 человек. "
        f"И уже затем в магазине /shop её можно прокачать звёздами до уровня КЛАН на 1000 человек!\n\n"
        f"Никаких привязок к реальным школам и городам — полная анонимность от буллинга и преследований соперников.\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🏆 Создать Команду (/create_team)", callback_data="clan_action:start_create")],
        [types.InlineKeyboardButton(text="🔍 Найти Команду по названию", callback_data="clan_action:search_name")],
        [types.InlineKeyboardButton(text="📍 Посмотреть последние команды СНГ",
                                    callback_data="clan_action:search_city")],
        [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
    ])

    await target_msg.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")


# Вторая часть FSM конвейера и отмены (из предыдущего сообщения) идет далее без изменений...


# ============================================================================
# 👥 2. ПОШАГОВЫЙ БЕЗОПАСНЫЙ КОНВЕЙЕР СОЗДАНИЯ (C КНОПКОЙ ОТМЕНЫ)
# ============================================================================
@router.message(Command("create_team"))
@router.callback_query(F.data == "clan_action:start_create")
async def trigger_clan_creation_fsm(message: types.Message or types.CallbackQuery, state: FSMContext):
    is_cb = isinstance(message, types.CallbackQuery)
    user_id = message.from_user.id if is_cb else message.from_user.id
    target = message.message if is_cb else message

    if is_cb: await message.answer()

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT balance, team_id FROM users WHERE user_id = $1", user_id)

    if user and user["team_id"] is not None:
        await target.answer("⚠️ Ошибка! Ты уже состоишь в команде. Чтобы создать свою, сначала выйди из старой!")
        return
    if not user or user["balance"] < 100000:
        await target.answer(
            f"❌ Недостаточно монет! Создание стоит 100 000 рофлов. Твой баланс: {user['balance'] if user else 0}")
        return

    await state.set_state(ClanCreationStates.waiting_for_name)
    await target.answer(
        "🏆 <b>ШАГ 1 ИЗ 3: НАЗВАНИЕ КОМАНДЫ</b>\n\n"
        "Придумай и введи уникальное имя для своей банды (до 32 знаков):",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(ClanCreationStates.waiting_for_name)
async def process_fsm_clan_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2 or len(name) > 32:
        await message.answer("❌ Название должно быть от 2 до 32 символов! Введи еще раз:",
                             reply_markup=get_cancel_keyboard())
        return
    await state.update_data(clan_name=name)
    await state.set_state(ClanCreationStates.waiting_for_motto)
    await message.answer(
        "💬 <b>ШАГ 2 ИЗ 3: ДЕВИЗ КОМАНДЫ</b>\n\n"
        "Напиши боевой девиз твоей банды (до 100 символов):",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(ClanCreationStates.waiting_for_motto)
async def process_fsm_clan_motto(message: types.Message, state: FSMContext):
    motto = message.text.strip()
    if len(motto) < 1 or len(motto) > 100:
        await message.answer("❌ Девиз слишком короткий или длинный! Введи еще раз:", reply_markup=get_cancel_keyboard())
        return
    await state.update_data(clan_motto=motto)
    await state.set_state(ClanCreationStates.waiting_for_symbol)
    await message.answer(
        "🔮 <b>ШАГ 3 ИЗ 3: СИМВОЛ КОМАНДЫ</b>\n\n"
        "Отправь один или несколько смайликов/эмодзи с клавиатуры смартфона, которые станут визуальным знаком твоей банды:",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(ClanCreationStates.waiting_for_symbol)
async def process_fsm_clan_symbol_finalize(message: types.Message, state: FSMContext):
    symbol = message.text.strip()
    if len(symbol) < 1 or len(symbol) > 20:
        await message.answer("❌ Отправь корректные эмодзи с клавиатуры:", reply_markup=get_cancel_keyboard())
        return

    data = await state.get_data()
    await state.clear()

    # Переиспользуем ячейки city под девиз, а school_num под эмодзи-символ! СУБД Railway в безопасности!
    success, status = await create_new_team_in_db(
        captain_id=message.from_user.id,
        team_name=data.get("clan_name"),
        city=data.get("clan_motto"),
        school=symbol
    )
    if not success:
        await message.answer(f"❌ {status}")
        return

    await message.answer(
        f"👑 <b>КОМАНДА УСПЕШНО ЗАРЕГИСТРИРОВАНА!</b>\n"
        f"..................................................\n\n"
        f"🏆 Название: <b>{data.get('clan_name')}</b>\n"
        f"💬 Девиз: <i>«{data.get('clan_motto')}»</i>\n"
        f"🔮 Твой символ: {symbol}\n\n"
        f"..................................................\n"
        f"💳 С баланса списано: <b>100 000 рофлов</b> за покупку лицензии.\n\n"
        f"👥 <i>Твоя команда создана с лимитом до 50 игроков. Прокачать её до уровня КЛАН на 1000 мест можно в магазине /shop за Stars! Друзья могут найти тебя через поиск по названию!</i>",
        parse_mode="HTML"
    )


# ============================================================================
# ❌ ЭКСТРЕННАЯ КНОПКА ОТМЕНЫ ОПРОСА И СБРОСА ДАННЫХ
# ============================================================================
@router.callback_query(F.data == "clan_action:cancel_fsm")
async def process_cancel_fsm_logic(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Создание команды прервано!")
    await state.clear()  # Намертво стираем буфер FSM
    try:
        await callback.message.delete()
    except Exception:
        pass
    # Выводим чистое текстовое оповещение и кнопку возврата на главную базу
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💿 Открыть Главное Меню /menu", callback_data="refresh_main_menu")]
    ])
    await callback.message.answer("❌ <b>Процедура создания отменена. Все временные данные удалены.</b>",
                                  reply_markup=kb, parse_mode="HTML")


# ============================================================================
# 🔍 3. МОДУЛЬ АНОНИМНОГО ГЛОБАЛЬНОГО ПОИСКА (АНТИ-БУЛЛИНГ СИСТЕМА)
# ============================================================================
@router.callback_query(F.data == "clan_action:search_name")
async def trigger_search_by_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ClanCreationStates.waiting_for_search)
    await callback.message.answer("🔍 Введи название команды или ключевое слово для поиска:")


@router.message(ClanCreationStates.waiting_for_search)
async def process_clan_search_by_name(message: types.Message, state: FSMContext):
    search_query = message.text.strip()
    await state.clear()

    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM teams WHERE team_name ILIKE $1 LIMIT 5", f"%{search_query}%")

    if not rows:
        await message.answer("❌ Команды с таким названием не найдены.")
        return

    await message.answer("🔍 <b>РЕЗУЛЬТАТЫ ГЛОБАЛЬНОГО ПОИСКА:</b>", parse_mode="HTML")

    for team in rows:
        status_clan = "Мега-Клан" if team["max_members"] >= 1000 else "Команда"
        # Скрываем юзернеймы! Показываем только сухие игровые параметры
        text = (
            f"🏆 <b>{team['team_name']}</b> ({status_clan})\n"
            f"💬 Девиз: <i>«{team['city']}»</i>\n"
            f"🔮 Эмблема: {team['school_num']}\n"
            f"👥 Участники: <b>{team['members_count']} / {team['max_members']} чел.</b>"
        )
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="💥 Подать заявку и войти", callback_data=f"clan_join:{team['team_id']}")]
        ])
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "clan_action:search_city")
async def process_search_by_user_city(callback: types.CallbackQuery):
    await callback.answer()

    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM teams ORDER BY created_at DESC LIMIT 5")

    if not rows:
        await callback.message.answer("⚠️ В базе данных пока нет ни одной созданной команды.")
        return

    await callback.message.answer("📍 <b>ПОСЛЕДНИЕ СОЗДАННЫЕ КОМАНДЫ В СНГ:</b>", parse_mode="HTML")

    for team in rows:
        status_clan = "Мега-Клан" if team["max_members"] >= 1000 else "Команда"
        text = (
            f"🏆 Команда: <b>{team['team_name']}</b> ({status_clan})\n"
            f"💬 Девиз: <i>«{team['city']}»</i>\n"
            f"🔮 Эмблема: {team['school_num']}\n"
            f"👥 Состав: {team['members_count']} / {team['max_members']} чел."
        )
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="💥 Вступить в эту команду", callback_data=f"clan_join:{team['team_id']}")]
        ])
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")


# ============================================================================
# 💥 4. АТОМАРНЫЙ ВХОД ИГРОКА В КЛАН (БЕЗОПАСНАЯ СИНХРОНИЗАЦИЯ С FOR UPDATE)
# ============================================================================
@router.callback_query(F.data.startswith("clan_join:"))
async def process_clan_join_request(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    team_id = int(callback.data.split(":"))

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", team_id)
            user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)

            if not team:
                await callback.message.answer("❌ Ошибка! Эта команда больше не существует.")
                return
            if user and user["team_id"] is not None:
                await callback.message.answer("⚠️ Ты уже состоишь в какой-то команде! Сначала выйди из неё.")
                return
            if team["members_count"] >= team["max_members"]:
                await callback.message.answer("📦 В этой команде закончились свободные места!")
                return

            await conn.execute("UPDATE teams SET members_count = members_count + 1 WHERE team_id = $1", team_id)
            await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = $2", team_id, user_id)

            await callback.message.edit_text(
                f"🎉 <b>ПОЗДРАВЛЯЕМ, ТЫ В ИГРЕ!</b>\n\n"
                f"Ты успешно вступил в команду <b>{team['team_name']}</b>!\n"
                f"📍 Твой дашборд обновлен. Пиши команду /my_team, чтобы проверить состав!",
                parse_mode="HTML"
            )
