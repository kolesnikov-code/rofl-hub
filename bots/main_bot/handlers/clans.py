import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db
from shared.db_clans import create_new_team_in_db

router = Router()
logger = logging.getLogger(__name__)


# Определение цепочки состояний FSM для создания банды
class ClanCreationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_city = State()
    waiting_for_school = State()


# ============================================================================
# 👥 1. СТАРТ ЦЕПОЧКИ: КОМАНДА /create_clan ИЛИ /create_team
# ============================================================================
@router.message(Command("create_clan"))
@router.message(Command("create_team"))
async def cmd_create_clan_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Первичная проверка лимитов и баланса перед запуском опроса
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT balance, team_id FROM users WHERE user_id = $1", user_id)

    if not user:
        await message.answer("⚠️ Профиль не найден. Прожми /start")
        return

    if user["team_id"] is not None:
        await message.answer("⚠️ Ты уже состоишь в команде или клане!")
        return

    if user["balance"] < 100000:
        await message.answer(
            f"❌ Недостаточно рофлов для регистрации клана!\n"
            f"Стоимость создания банды: <b>100 000 рофлов</b>.\n"
            f"Твой текущий баланс: <code>{user['balance']} рофлов</code>."
        )
        return

    # Переводим юзера на первый шаг опроса FSM
    await state.set_state(ClanCreationStates.waiting_for_name)
    await message.answer(
        "🏆 <b>РЕГИСТРАЦИЯ НОВОЙ ШКОЛЬНОЙ БАНДЫ</b>\n"
        "..................................................\n\n"
        "Введи название для своей команды (до 32 символов).\n"
        "Название должно быть уникальным!",
        parse_mode="HTML"
    )


# ============================================================================
# 👥 2. ШАГ FSM: ПЕРЕХВАТ НАЗВАНИЯ КЛАНА
# ============================================================================
@router.message(ClanCreationStates.waiting_for_name)
async def process_clan_name(message: types.Message, state: FSMContext):
    team_name = message.text.strip()

    if len(team_name) < 2 or len(team_name) > 32:
        await message.answer("❌ Длина названия должна быть от 2 до 32 символов. Попробуй ещё раз:")
        return

    # Сохраняем имя в буфер FSM и переводим на следующий шаг
    await state.update_data(clan_name=team_name)
    await state.set_state(ClanCreationStates.waiting_for_city)
    await message.answer(
        "📍 Отлично! Теперь укажи город, в котором находится твоя школа (например, Ташкент, Москва, Самарканд):")


# ============================================================================
# 👥 3. ШАГ FSM: ПЕРЕХВАТ ГОРОДА ТОРГОВЛИ
# ============================================================================
@router.message(ClanCreationStates.waiting_for_city)
async def process_clan_city(message: types.Message, state: FSMContext):
    city_name = message.text.strip()

    if len(city_name) < 2 or len(city_name) > 50:
        await message.answer("❌ Название города слишком короткое или длинное. Попробуй ещё раз:")
        return

    await state.update_data(clan_city=city_name)
    await state.set_state(ClanCreationStates.waiting_for_school)
    await message.answer(
        "🏫 И финальный шаг: введи номер или название твоей школы (например, Школа №50, Лицей Интерхаус):")


# ============================================================================
# 👥 4. ШАГ FSM: ФИНАЛЬНАЯ ТОЧКА И ВОРВ В БАЗУ ДАННЫХ
# ============================================================================
@router.message(ClanCreationStates.waiting_for_school)
async def process_clan_school_and_finalize(message: types.Message, state: FSMContext):
    school_name = message.text.strip()

    if len(school_name) < 1 or len(school_name) > 50:
        await message.answer("❌ Описание школы некорректно. Введи номер школы заново:")
        return

    # Извлекаем все накопленные данные из буфера FSM
    user_data = await state.get_data()
    clan_name = user_data.get("clan_name")
    clan_city = user_data.get("clan_city")

    # Мгновенно очищаем состояние FSM, защищая контур от повторного ввода данных
    await state.clear()

    captain_id = message.from_user.id

    # Вызываем наш титановый транзакционный блок из shared/db_clans.py
    success, result_status = await create_new_team_in_db(
        captain_id=captain_id,
        team_name=clan_name,
        city=clan_city,
        school=school_name
    )

    if not success:
        # Если транзакция вернула ошибку, выводим её на экран (деньги не списаны!)
        await message.answer(f"{result_status}")
        return

    # Выдаем лаконичный, чистый победный чек создания клана
    success_text = (
        f"👑 <b>БАНДА УСПЕШНО ЗАРЕГИСТРИРОВАНА!</b>\n"
        f"..................................................\n\n"
        f"🏆 Название клана: <b>{clan_name}</b>\n"
        f"📍 Локация: <code>{clan_city}, {school_name}</code>\n"
        f"👤 Капитан банды: <code>{captain_id}</code>\n\n"
        f"..................................................\n"
        f"💳 С баланса списано: <b>100 000 рофлов</b> за покупку лицензии.\n\n"
        f"👥 <i>Команда создана с лимитом до 50 игроков. Твои одноклассники теперь могут "
        f"вступить в твой клан по твоему ID Паспорта! Собирай армию!</i>"
    )
    await message.answer(success_text, parse_mode="HTML")
