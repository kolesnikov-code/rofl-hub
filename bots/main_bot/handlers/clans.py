from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# Импортируем наши боевые офисы состояний и базы данных
from bots.main_bot.utils.states import TeamCreationStates
from shared.db_clans import check_user_can_create_team, create_new_team_in_db

router = Router()


# ----------------------------------------------------------------
# 🛑 СТАРТ АНКЕТЫ: КОМАНДА /make_team
# ----------------------------------------------------------------
@router.message(Command("make_team"))
async def cmd_make_team(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # 1. Проверяем в бэкенде Railway, имеет ли право юзер создать команду (баланс, лимиты)
    status = await check_user_can_create_team(user_id)

    if status != "OK":
        await message.answer(status)  # Выводим ошибку ("Недостаточно Рофлов" или "Уже в команде")
        return

    # 2. Если всё супер — включаем первый шаг FSM
    await message.answer(
        "👥 <b>СОЗДАНИЕ НОВОЙ КОМАНДЫ</b>\n"
        "..................................................\n"
        "Создание команды спишет с твоего счета <b>100 000 рофлов</b>.\n\n"
        "👇 <b>ШАГ №1: Введи название для своей команды.</b>\n\n"
        "<i><b>Пример:</b> 7-Б класс 110 школы, Акулы Ташкента, Манчестер на минималках и т.д. "
        "Чем оригинальнее название - тем круче!</i>\n\n"
        "⚠️ Длина названия: от 3 до 30 символов. Без мата.",
        parse_mode="HTML"
    )
    await state.set_state(TeamCreationStates.name)


# ----------------------------------------------------------------
# 📝 ШАГ №2: ПЕРЕХВАТ НАЗВАНИЯ КОМАНДЫ
# ----------------------------------------------------------------
@router.message(TeamCreationStates.name)
async def process_team_name(message: types.Message, state: FSMContext):
    name = message.text.strip()

    if len(name) < 3 or len(name) > 30:
        await message.answer("❌ Длина должна быть строго от 3 до 30 букв. Попробуй еще раз:")
        return

    # Сохраняем имя в оперативную память FSM
    await state.update_data(team_name=name)

    await message.answer(
        "📍 <b>ШАГ №2: Введи свой город привязки.</b>\n\n"
        "<i>Это нужно, чтобы тимейты из твоего класса или города могли найти команду через поиск!</i>\n\n"
        "<i><b>Пример:</b> Москва, Ташкент, Минск, Владивосток, Ереван, Киев, Новосибирск, Астана и т.д.</i>",
        parse_mode="HTML"
    )
    await state.set_state(TeamCreationStates.city)


# ----------------------------------------------------------------
# 📍 ШАГ №3: ПЕРЕХВАТ ГОРОДА
# ----------------------------------------------------------------
@router.message(TeamCreationStates.city)
async def process_team_city(message: types.Message, state: FSMContext):
    city = message.text.strip()

    if len(city) < 2 or len(city) > 30:
        await message.answer("❌ Строго 2 до 30 символов! Попробуй еще раз:")
        return

    await state.update_data(city=city)

    await message.answer(
        "🏫 <b>ФИНАЛЬНЫЙ ШАГ №3: Введи номер или название школы.</b>\n\n"
        "<i><b>Пример:</b> Школа 110, Лицей №5, Гимназия 12. "
        "Если играешь не от школы, напиши что угодно, например 'Одиночка' или 'Табуретка'. "
        "Но лучше выбрать максимально оригинальное название.</i>",
        parse_mode="HTML"
    )
    await state.set_state(TeamCreationStates.school)


# ----------------------------------------------------------------
# 🚀 ФИНАЛ: ЗАПИСЬ В ОБЛАКО RAILWAY
# ----------------------------------------------------------------
@router.message(TeamCreationStates.school)
async def process_team_school(message: types.Message, state: FSMContext):
    school = message.text.strip()
    captain_id = message.from_user.id

    if len(school) < 1 or len(school) > 30:
        await message.answer("❌ Слишком длинно или пусто. Введи номер школы:")
        return

    # Достаем все накопленные шаги из памяти FSM
    user_data = await state.get_data()
    team_name = user_data["team_name"]
    city = user_data["city"]

    await message.answer("⚡ <i>Выполняю запрос... \n\nСвязываюсь с хабом. \n\nСписываю 100 000 Рофлов...</i>",
                         parse_mode="HTML")

    # Стучимся в наш бэкенд-офис БД, созданный прошлым шагом
    success = await create_new_team_in_db(
        captain_id=captain_id,
        team_name=team_name,
        city=city,
        school=school
    )

    if success:
        success_text = (
            f"👑 <b>ПОЗДРАВЛЯЕМ, КАПИТАН!</b>\n"
            f"..................................................\n"
            f"👥 Команда <b>«{team_name}»</b> официально зарегистрирована в облаке хостинга!\n\n"
            f"📍 Город: <code>{city}</code>\n"
            f"🏫 Школа: <code>{school}</code>\n"
            f"🚷 Состав: <code>1 / 50</code> игроков (жесткий лимит!)\n"
            f"..................................................\n"
            f"📢 <b>Что делать дальше:</b> Твой лимит расширен до 50 человек. "
            f"Бери свою реферальную ссылку /referral_link, кидай одноклассникам и забивай команду до отказа! "
            f"Готовь банду к командным битвам за призовые фонды и кибер-котлеты!"
        )
        await message.answer(success_text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ <b>База данных отклонила запрос!</b> Возможно, команда с таким названием уже кем-то создана. Придумай уникальное имя через /make_team.")

    # Полностью очищаем состояния FSM, возвращая юзера в обычный режим бота
    await state.clear()
