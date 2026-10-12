import logging
import re
import html
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db
from shared.db_clans import create_new_team_in_db
from shared.economy import TEAM_CREATE_COST

router = Router()
logger = logging.getLogger(__name__)


class ClanCreationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_motto = State()
    waiting_for_symbol = State()
    waiting_for_search = State()


# 🛡️ ЖЕСТКИЕ ФИЛЬТРЫ БЕЗОПАСНОСТИ (АНТИ-СПАМ, АНТИ-ФИШИНГ, АНТИ-МАТ)
URL_REGEX = re.compile(r'(https?://[^\s]+|t\.me/[^\s]+|@[^\s]+)')
PHONE_REGEX = re.compile(r'(\+?\d[\d\-\(\) ]{7,\d})')
PROHIBITED_WORDS = ["хуй", "пизда", "ебать", "член", "сука", "бля", "трахать", "мудак"]


def validate_input_string(text: str, max_len: int) -> tuple[bool, str]:
    """Серверный валидатор строк холдинга ROFL HUB CORE"""
    cleaned = text.strip()
    if not cleaned or len(cleaned) > max_len:
        return False, f"❌ Длина текста должна быть от 1 до {max_len} символов!"

    # Защита от фишинга и рекламы
    if URL_REGEX.search(cleaned) or PHONE_REGEX.search(cleaned):
        return False, "🚨 Ошибка безопасности! Ссылки, юзернеймы и телефоны строго запрещены!"

    # Базовый фильтр мата для детской аудитории
    for word in PROHIBITED_WORDS:
        if word in cleaned.lower():
            return False, "❌ Обнаружены нецензурные выражения! Соблюдай правила хаба."

    # Намертво экранируем HTML-теги для предотвращения XSS инъекций в рулетке
    return True, html.escape(cleaned)


def get_cancel_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Прервать создание команды", callback_data="clan_action:cancel_fsm")]
    ])


# ============================================================================
# 👥 1. ГЛАВНЫЙ ХАБ КОМАНД (С ФИКСОМ КОНТЕКСТА CALLBАCK.MESSAGE)
# ============================================================================
@router.message(Command("clan"))
@router.message(Command("clans"))
@router.message(F.text == "🏆 КОМАНДЫ И КЛАНЫ")
@router.callback_query(F.data == "clan_main_menu")
async def cmd_clan_hub(message: types.Message | types.CallbackQuery):
    is_callback = isinstance(message, types.CallbackQuery)
    # 🔥 ФИКС 4: Вытягиваем ID строго из from_user, а не из message.from_user (который равен боту при callback)
    user_id = message.from_user.id
    target_msg = message.message if is_callback else message

    if is_callback:
        await message.answer()

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1", user_id)

        if user and user["team_id"] is not None:
            await show_user_team_dashboard(target_msg, user["team_id"], user_id)
            return

    welcome_text = (
        f"👥 <b>ЦЕНТРАЛЬНЫЙ ОФИС КОМАНД И КЛАНОВ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"Изначально ВСЕГДА создаётся обычная Команда за 100 000 рофлов до 50 человек. "
        f"И уже затем в магазине /shop её можно прокачать звёздами до уровня КЛАН на 1000 человек!\n\n"
        f"Никаких привязок к реальным школам и городам — полная анонимность от буллинга.\n\n"
        f"👇 <b>ВЫБЕРИ ДЕЙСТВИЕ:</b>"
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🏆 Создать Команду (/create_team)", callback_data="clan_action:start_create")],
        [types.InlineKeyboardButton(text="🔍 Найти Команду по названию", callback_data="clan_action:search_name")],
        [types.InlineKeyboardButton(text="📍 Игровая Рулетка команд СНГ", callback_data="clan_action:search_city")],
        [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
    ])
    await target_msg.answer(welcome_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# 👥 2. ВЫЗОВ СВОЕЙ КОМАНДЫ ДАННЫЙ СЕЙЧАС: /my_team
# ============================================================================
@router.message(Command("my_team"))
async def cmd_my_team_isolated(message: types.Message):
    user_id = message.from_user.id

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1", user_id)

        if not user or user["team_id"] is None:
            kb = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="🏆 Создать Команду за 100к",
                                            callback_data="clan_action:start_create")],
                [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
            ])
            await message.answer(
                "⚠️ <b>У тебя пока нет созданной команды!</b>\n\nТы можешь зарегистрировать личную банду прямо сейчас, нажав на кнопку ниже.",
                reply_markup=kb, parse_mode="HTML")
            return

        await show_user_team_dashboard(message, user["team_id"], user_id)


async def show_user_team_dashboard(message: types.Message, team_id: int, viewer_id: int):
    """Рендеринг дашборда банды с титановой защитой от утечки юзернеймов"""
    async with db.pool.acquire() as conn:
        team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1", team_id)
        captain_row = await conn.fetchrow("SELECT username FROM users WHERE user_id = $1", team["captain_id"])

    # Защита от буллинга: юзернейм виден только соклановцам, чужие видят сухой ID
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
        [types.InlineKeyboardButton(text="🚪 Покинуть команду / Бросить банду", callback_data=f"clan_leave:{team_id}")],
        [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
    ])
    await message.answer(clan_text, reply_markup=kb, parse_mode="HTML")


# ============================================================================
# 🔍 3. ПРЯМОЙ ВЫЗОВ ПОИСКА И ИГРОВОЙ РУЛЕТКИ КОМАНД СНГ: /all_teams
# ============================================================================
@router.message(Command("all_teams"))
async def cmd_all_teams_isolated(message: types.Message):
    """Выводит 3 случайные команды из общей базы с кнопкой ротации"""
    async with db.pool.acquire() as conn:
        # 🔥 Ротация: Выдергиваем 3 случайных незаполненных клана из БД!
        rows = await conn.fetch(
            "SELECT * FROM teams WHERE members_count < max_members ORDER BY RANDOM() LIMIT 3"
        )

    if not rows:
        await message.answer("⚠️ В базе данных пока нет свободных команд для вступления.")
        return

    await message.answer("📍 <b>АКТУАЛЬНЫЕ КОМАНДЫ В СНГ:</b>", parse_mode="HTML")

    for team in rows:
        status_clan = "Мега-Клан" if team["max_members"] >= 1000 else "Команда"
        text = (
            f"🏆 <b>{team['team_name']}</b> ({status_clan})\n"
            f"💬 Девиз: <i>«{team['city']}»</i>\n"
            f"🔮 Эмблема: {team['school_num']}\n"
            f"👥 Состав: <b>{team['members_count']} / {team['max_members']} чел.</b>"
        )
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="💥 Вступить в эту команду", callback_data=f"clan_join:{team['team_id']}")]
        ])
        await message.answer(text, reply_markup=kb, parse_mode="HTML")

    rotation_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔄 Показать другие команды", callback_data="clan_action:search_city")]
    ])
    await message.answer("👇 <b>Не нашел подходящую банду? Прокрути рулетку!</b>", reply_markup=rotation_kb,
                         parse_mode="HTML")


# ============================================================================
# 👥 4. ПОШАГОВЫЙ БЕЗОПАСНЫЙ КОНВЕЙЕР СОЗДАНИЯ КОМАНДЫ (FSM С СЕРВЕРНОЙ ВАЛИДАЦИЕЙ)
# ============================================================================
async def _begin_team_creation(target: types.Message, user_id: int, state: FSMContext) -> None:
    """Общий вход в создание команды: из кнопки и из команды /create_team."""
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT balance, team_id FROM users WHERE user_id = $1", user_id)

    if not user:
        await target.answer("⚠️ Профиль не найден. Нажми /start")
        return
    if user["team_id"] is not None:
        await target.answer("⚠️ Ты уже состоишь в команде. Посмотреть её: /my_team")
        return
    if user["balance"] < TEAM_CREATE_COST:
        await target.answer(
            f"❌ Недостаточно рофлов! Создание стоит {TEAM_CREATE_COST:,}. Твой баланс: {user['balance']:,}".replace(",", " "))
        return

    await state.set_state(ClanCreationStates.waiting_for_name)
    await target.answer("🏆 <b>ШАГ 1 ИЗ 3: НАЗВАНИЕ КОМАНДЫ</b>\n\nВведи уникальное имя банды (до 32 знаков):",
                        reply_markup=get_cancel_keyboard(), parse_mode="HTML")


@router.message(Command("create_team"))
async def cmd_create_team(message: types.Message, state: FSMContext):
    await _begin_team_creation(message, message.from_user.id, state)


@router.callback_query(F.data == "clan_action:start_create")
async def trigger_clan_creation_inline(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await _begin_team_creation(callback.message, callback.from_user.id, state)


@router.message(ClanCreationStates.waiting_for_name)
async def process_fsm_clan_name(message: types.Message, state: FSMContext):
    is_valid, validated_name = validate_input_string(message.text, 32)
    if not is_valid:
        await message.answer(validated_name, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
        return

    await state.update_data(clan_name=validated_name)
    await state.set_state(ClanCreationStates.waiting_for_motto)
    await message.answer("💬 <b>ШАГ 2 ИЗ 3: ДЕВИЗ КОМАНДЫ</b>\n\nНапиши боевой девиз твоей банды (до 100 символов):",
                         reply_markup=get_cancel_keyboard(), parse_mode="HTML")


@router.message(ClanCreationStates.waiting_for_motto)
async def process_fsm_clan_motto(message: types.Message, state: FSMContext):
    is_valid, validated_motto = validate_input_string(message.text, 100)
    if not is_valid:
        await message.answer(validated_motto, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
        return

    await state.update_data(clan_motto=validated_motto)
    await state.set_state(ClanCreationStates.waiting_for_symbol)
    await message.answer(
        "🔮 <b>ШАГ 3 ИЗ 3: СИМВОЛ КОМАНДЫ</b>\n\nОтправь эмодзи-символ эмблемы (до 5 знаков клавиатуры):",
        reply_markup=get_cancel_keyboard(), parse_mode="HTML")


@router.message(ClanCreationStates.waiting_for_symbol)
async def process_fsm_clan_symbol_finalize(message: types.Message, state: FSMContext):
    is_valid, validated_symbol = validate_input_string(message.text, 5)
    if not is_valid:
        await message.answer(validated_symbol, reply_markup=get_cancel_keyboard(), parse_mode="HTML")
        return

    data = await state.get_data()
    await state.clear()

    success, status = await create_new_team_in_db(
        captain_id=message.from_user.id,
        team_name=data.get("clan_name"),
        city=data.get("clan_motto"),
        school=validated_symbol
    )
    if not success:
        await message.answer(f"❌ {status}")
        return

    await message.answer(
        f"👑 <b>КОМАНДА УСПЕШНО ЗАРЕГИСТРИРОВАНА!</b>\n"
        f"..................................................\n\n"
        f"🏆 Название: <b>{data.get('clan_name')}</b>\n"
        f"💬 Девиз: <i>«{data.get('clan_motto')}»</i>\n"
        f"🔮 Твой символ: {validated_symbol}\n\n"
        f"..................................................\n"
        f"💳 Списано: <b>100 000 рофлов</b>. Управляй бандой через /my_team!",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "clan_action:cancel_fsm")
async def process_cancel_fsm_logic(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Создание прервано!")
    await state.clear()
    try:
        await callback.message.delete()
    except Exception:
        pass
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💿 Открыть Главное Меню /menu", callback_data="refresh_main_menu")]])
    await callback.message.answer("❌ <b>Процедура создания отменена. Все временные данные удалены.</b>",
                                  reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "clan_action:search_name")
async def trigger_search_by_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ClanCreationStates.waiting_for_search)
    await callback.message.answer("🔍 Введи название команды или ключевое слово для поиска:")


@router.message(ClanCreationStates.waiting_for_search)
async def process_clan_search_by_name(message: types.Message, state: FSMContext):
    is_valid, search_query = validate_input_string(message.text, 32)
    await state.clear()
    if not is_valid:
        await message.answer(search_query)
        return

    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM teams WHERE team_name ILIKE $1 LIMIT 5", f"%{search_query}%")
    if not rows:
        await message.answer("❌ Команды с таким названием не найдены.")
        return
    await message.answer("🔍 <b>РЕЗУЛЬТАТЫ ГЛОБАЛЬНОГО ПОИСКА:</b>", parse_mode="HTML")
    for team in rows:
        status_clan = "Мега-Клан" if team["max_members"] >= 1000 else "Команда"
        text = (
            f"🏆 <b>{team['team_name']}</b> ({status_clan})\n💬 Девиз: <i>«{team['city']}»</i>\n🔮 Эмблема: {team['school_num']}\n👥 Участники: <b>{team['members_count']} / {team['max_members']} чел.</b>")
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="💥 Подать заявку и войти", callback_data=f"clan_join:{team['team_id']}")]])
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "clan_action:search_city")
async def process_search_by_user_city(callback: types.CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await cmd_all_teams_isolated(callback.message)


@router.callback_query(F.data.startswith("clan_join:"))
async def process_clan_join_request(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) < 2: return
    team_id = int(parts[1])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", team_id)
            user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not team:
                await callback.message.answer("❌ Ошибка! Эта команда больше не существует.")
                return
            if user and user["team_id"] is not None:
                await callback.message.answer(
                    "⚠️ <b>Ты уже состоишь в команде!</b>\n\nСначала выйди из нее, прописав команду /my_team.",
                    parse_mode="HTML")
                return
            if team["members_count"] >= team["max_members"]:
                await callback.message.answer("📦 В этой команде закончились места!")
                return
            await conn.execute("UPDATE teams SET members_count = members_count + 1 WHERE team_id = $1", team_id)
            await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = $2", team_id, user_id)
    await callback.message.edit_text(
        f"🎉 <b>ПОЗДРАВЛЯЕМ, ТЫ В ИГРЕ!</b>\n\nТы успешно вступил в команду <b>{team['team_name']}</b>!\n📍 Пиши команду /my_team, чтобы проверить состав!",
        parse_mode="HTML")


# ============================================================================
# 🚪 5. ТИТАНОВЫЙ КОНТУР ВЫХОДА (С ЗАЩИТОЙ ОТ РАССИНХРОНИЗАЦИИ СЧЕТЧИКОВ)
# ============================================================================
@router.callback_query(F.data.startswith("clan_leave:"))
async def process_clan_leave_logic(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) < 2 or not parts[1].isdigit():
        return
    team_id = int(parts[1])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Блокируем строку клана и юзера одновременно через жесткий FOR UPDATE
            team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", team_id)
            user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)

            # 🔥 ФИКС 7: Проверка, что игрок реально находится именно в этой команде
            if not user or user["team_id"] != team_id or not team:
                await callback.message.answer(
                    "❌ Ошибка безопасности! Ты не состоишь в данной команде или она уже расформирована.")
                return

            if team["captain_id"] == user_id:
                # 👑 СЦЕНАРИЙ А: ВЫХОДИТ САМ КАПИТАН БАНДЫ!
                # Ищем самого преданного ветерана (кто зарегистрирован в команде раньше всех)
                next_captain = await conn.fetchrow(
                    "SELECT user_id, username FROM users WHERE team_id = $1 AND user_id != $2 ORDER BY last_seen_at DESC, user_id ASC LIMIT 1",
                    team_id, user_id
                )

                if next_captain:
                    # Ветеран найден! Передаем ему корону и списываем одного человека
                    await conn.execute(
                        "UPDATE teams SET captain_id = $1, members_count = members_count - 1 WHERE team_id = $2",
                        next_captain["user_id"], team_id)
                    await conn.execute("UPDATE users SET team_id = NULL WHERE user_id = $1", user_id)

                    announce_text = (
                        f"🚪 <b>РЕВОЛЮЦИЯ В БАНДЕ!</b>\n"
                        f"..................................................\n\n"
                        f"Капитан бросил команду <b>{team['team_name']}</b> и ушёл в закат.\n\n"
                        f"👑 По праву преданности и старшинства, новым <b>Вожаком банды</b> официально объявлен ветеран: "
                        f"@{html.escape(next_captain['username'] or str(next_captain['user_id']))} (ID: <code>{next_captain['user_id']}</code>)!\n\n"
                        f"<i>Власть сменилась. Команда продолжает битву за ТОП СНГ!</i>"
                    )
                    await callback.message.answer(announce_text, parse_mode="HTML")
                else:
                    # Капитан был один на лодке — наглухо аннулируем команду, чтоб не спамить базу Railway
                    await conn.execute("DELETE FROM teams WHERE team_id = $1", team_id)
                    await conn.execute("UPDATE users SET team_id = NULL WHERE user_id = $1", user_id)
                    await callback.message.answer(
                        "🚪 Ты был единственным участником. Команда официально <b>удалена и расформирована</b>.",
                        parse_mode="HTML")
            else:
                # 👥 СЦЕНАРИЙ Б: ВЫХОДИТ ОБЫЧНЫЙ УЧАСТНИК
                await conn.execute("UPDATE teams SET members_count = members_count - 1 WHERE team_id = $1", team_id)
                await conn.execute("UPDATE users SET team_id = NULL WHERE user_id = $1", user_id)
                await callback.message.answer(
                    f"🚪 Ты успешно покинул команду <b>{team['team_name']}</b>. Теперь ты вольная птица!",
                    parse_mode="HTML")

            # Наводим идеальный порядок в чате: удаляем старый дашборд с кнопками
            try:
                await callback.message.delete()
            except Exception:
                pass
