import os
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Подтягиваем наш титановый бэкенд регистрации команд
from shared.db_clans import create_new_team_in_db

router = Router()


# ----------------------------------------------------------------
# 🎭 КЛАСС FSM СОСТОЯНИЙ (Сценарный капкан Анатолия Алексеевича)
# ----------------------------------------------------------------
class CreateTeamStates(StatesGroup):
    waiting_for_name = State()  # Ждём название банды (напр. "7-Б класс")
    waiting_for_city = State()  # Ждём город привязки (напр. "Ташкент")
    waiting_for_school = State()  # Ждём номер школы / лицея (напр. "110 школа")


# ----------------------------------------------------------------
# 👥 КОМАНДА СТАРТА: /create_team
# ----------------------------------------------------------------
@router.message(Command("create_team"))
@router.message(Command("make_team"))
async def cmd_create_team_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Сбрасываем любые старые зависшие состояния ребенка, если они были
    await state.clear()

    welcome_text = (
        "👥 <b>РЕГИСТРАЦИЯ НОВОЙ КОМАНДЫ В ROFL HUB</b>\n"
        "..................................................\n\n"
        "🏆 Создание собственной банды позволит тебе собирать до 50 игроков, "
        "биться в межшкольных дуэлях и выжигать глобальный топ СНГ!\n\n"
        "💳 Стоимость открытия официального штаба: <b>100 000 рофлов</b>.\n"
        "<i>(Списание произойдет автоматически только в случае успешного финала)</i>\n\n"
        "..................................................\n"
        "👇 <b>ШАГ №1:</b> Напиши крутое и блатное <b>название</b> для своей команды.\n"
        "<i>(Пример: 7-Б класс, Бешеные Акулы, Мажоры 110-й)</i>"
    )

    # Включаем FSM-капкан на перехват текстовых сообщений названия
    await state.set_state(CreateTeamStates.waiting_for_name)
    await message.answer(welcome_text, parse_mode="HTML")


# ----------------------------------------------------------------
# ✏️ ПЕРЕХВАТ ШАГА №1: НАЗВАНИЕ КОМАНДЫ
# ----------------------------------------------------------------
@router.message(CreateTeamStates.waiting_for_name, F.text)
async def process_team_name(message: types.Message, state: FSMContext):
    team_name = message.text.strip()

    # Защита от дурака: жесткая валидация длины строки
    if len(team_name) < 3 or len(team_name) > 30:
        await message.answer("⚠️ Название должно быть от 3 до 30 символов! Напиши нормальное название:")
        return

    # Сохраняем название во временный кэш оперативной памяти FSM
    await state.update_data(team_name=team_name)

    next_step_text = (
        f"📝 Название <b>«{team_name}»</b> зафиксировано!\n"
        f"..................................................\n\n"
        f"👇 <b>ШАГ №2:</b> Напиши <b>город</b>, в котором находится твоя банда.\n"
        f"<i>(Пример: Ташкент, Москва, Самарканд, Новосибирск)</i>"
    )
    await state.set_state(CreateTeamStates.waiting_for_city)
    await message.answer(next_step_text, parse_mode="HTML")


# ----------------------------------------------------------------
# ✏️ ПЕРЕХВАТ ШАГА №2: ГОРОД
# ----------------------------------------------------------------
@router.message(CreateTeamStates.waiting_for_city, F.text)
async def process_team_city(message: types.Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2 or len(city) > 30:
        await message.answer("⚠️ Название города должно быть от 2 до 30 символов! Повтори ввод:")
        return

    await state.update_data(city=city)

    next_step_text = (
        f"📍 Город <b>«{city}»</b> зафиксирован!\n"
        f"..................................................\n\n"
        f"👇 <b>ШАГ №3 (ФИНАЛ):</b> Напиши <b>номер школы или название учебного заведения</b>.\n"
        f"<i>(Пример: Школа №110, Лицей Интерхаус, Гимназия 4)</i>"
    )
    await state.set_state(CreateTeamStates.waiting_for_school)
    await message.answer(next_step_text, parse_mode="HTML")


# ----------------------------------------------------------------
# ✏️ ПЕРЕХВАТ ШАГА №3: ШКОЛА + АТОМАРНЫЙ ВОРВ С БАЗОЙ
# ----------------------------------------------------------------
@router.message(CreateTeamStates.waiting_for_school, F.text)
async def process_team_school_and_finalize(message: types.Message, state: FSMContext):
    school = message.text.strip()

    if len(school) < 2 or len(school) > 50:
        await message.answer("⚠️ Описание школы должно быть от 2 to 50 символов! Повтори ввод:")
        return

    # Вытаскиваем все накопленные шаги из кэша FSM памяти
    user_data = await state.get_data()
    team_name = user_data['team_name']
    city = user_data['city']

    # Полностью закрываем и вычищаем FSM сессию для юзера
    await state.clear()

    # Оповещаем, что шлюз Railway открыт
    await message.answer("🔒 <i>Шлюз асинхронных транзакций запущен. Сверяю баланс и создаю банду...</i>",
                         parse_mode="HTML")

    # 🚀 ЕДИНЫЙ ТИТАНОВЫЙ ВОРВ В БАЗУ ДАННЫХ (Защита от Race Condition)
    success, result_message = await create_new_team_in_db(
        captain_id=message.from_user.id,
        team_name=team_name,
        city=city,
        school=school
    )

    if not success:
        # Если проверка на FOR UPDATE не прошла, выкатываем точную причину отказа из базы
        await message.answer(result_message, parse_mode="HTML")
        return

    # Финальный победный аккорд
    success_text = (
        f"🎉 <b>БАНДА УСПЕШНО ЗАРЕГИСТРИРОВАНА В СНГ!</b>\n"
        f"..................................................\n\n"
        f"👑 Название: <b>{team_name}</b>\n"
        f"📍 Локация: <b>{city}, {school}</b>\n"
        f"💳 Списание: <b>-100 000 рофлов</b> с твоего кошелька.\n\n"
        f"..................................................\n\n"
        f"👥 <i>Ты официально стал Капитаном! Твой лимит — до 50 игроков. "
        f"Качай реферальную ссылку, собирай одноклассников и готовься выжигать рудники!</i>"
    )
    await message.answer(success_text, parse_mode="HTML")


# ----------------------------------------------------------------
# ❌ СБРОС СОСТОЯНИЙ (Если ребенок передумал в процессе)
# ----------------------------------------------------------------
@router.message(Command("cancel"))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("❌ Регистрация команды отменена. Твои 100 000 рофлов остались в целости и сохранности!")
