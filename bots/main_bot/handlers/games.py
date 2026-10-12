import random
import logging
from datetime import datetime, timezone
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


class SoloGameStates(StatesGroup):
    waiting_for_quiz = State()


# 🎰 РАЗДЕЛЬНЫЙ ПЛАТИНОВЫЙ БАЛАНС АНАТОЛИЯ АЛЕКСЕЕВИЧА (АНТИИНФЛЯЦИЯ)
WIN_REWARD = 2
LOSE_PENALTY = 1

# Суточные лимиты чистых побед по типам игровых сессий
LIMITS = {
    "rps": 10,  # Камень-Ножницы-Бумага
    "hl": 10,  # Больше/Меньше
    "quiz": 20  # Интеллектуальная викторина
}


# ============================================================================
# ⚙️ ЦЕНТРАЛЬНЫЙ ДВИЖОК С СЕГМЕНТИРОВАННЫМИ СУТОЧНЫМИ ЛИМИТАМИ
# ============================================================================
async def execute_solo_game_payout(user_id: int, is_win: bool, game_type: str, is_draw: bool = False) -> tuple[
    bool, str, int]:
    """
    Универсальный игровой движок с раздельными лимитами побед для каждой игры.
    Защищает экономику от инфляции и исключает краши NameError: callback.
    """
    current_time = datetime.now(timezone.utc)
    today_date = current_time.date()
    max_limit = LIMITS.get(game_type, 10)

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Блокируем баланс от параллельных тапов через FOR UPDATE
            user = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return False, "⚠️ Профиль не найден. Нажми /start", 0

            current_balance = user["balance"]

            # Вытягиваем расширенную статистику суточных лимитов трех игр
            stats = await conn.fetchrow(
                """
                SELECT daily_wins_rps, daily_wins_hl, daily_wins_quiz, last_game_date
                FROM game_stats
                WHERE user_id = $1 FOR UPDATE
                """,
                user_id
            )

            wins_rps = 0
            wins_hl = 0
            wins_quiz = 0

            if stats and stats["last_game_date"] == today_date:
                wins_rps = stats["daily_wins_rps"]
                wins_hl = stats["daily_wins_hl"]
                wins_quiz = stats["daily_wins_quiz"]

            # Определяем текущий счетчик для проверяемой игры
            current_game_wins = wins_rps if game_type == "rps" else (wins_hl if game_type == "hl" else wins_quiz)

            # 🔥 ФИКС: Вместо edit_text здесь мы просто возвращаем статус лимита!
            if is_win and current_game_wins >= max_limit:
                game_title = "Камень-Ножницы-Бумага" if game_type == "rps" else (
                    "Больше/Меньше" if game_type == "hl" else "Викторина")
                return False, f"🛑 <b>Суточный лимит достигнут!</b>\n\nВ игре {game_title} ты уже забрал свои {max_limit} побед на сегодня. Но другие разделы и безлимитные дуэли еще открыты! Рискуй! 🔥", current_balance

            if not is_win and current_balance < LOSE_PENALTY:
                return False, "❌ У тебя 0 рофлов! Нечем оплатить мягкий сбор раунда. Забери кэш с фермы в /profile!", current_balance

            # Начисление монет и инкремент лимитов
            if is_win:
                new_balance = current_balance + WIN_REWARD
                if game_type == "rps":
                    wins_rps += 1
                elif game_type == "hl":
                    wins_hl += 1
                elif game_type == "quiz":
                    wins_quiz += 1
                status_text = f"🎉 ПОБЕДА! Начислено: <b>+{WIN_REWARD} рофлов</b>."
            elif is_draw:
                new_balance = current_balance - LOSE_PENALTY
                status_text = f"🤝 НИЧЬЯ! Списан технический сбор раунда: <b>-{LOSE_PENALTY} рофл</b>."
            else:
                new_balance = current_balance - LOSE_PENALTY
                status_text = f"💀 ПРОИГРЫШ! Списан мягкий экономический сбор: <b>-{LOSE_PENALTY} рофл</b>."

            await conn.execute("UPDATE users SET balance = $1 WHERE user_id = $2", new_balance, user_id)

            # Сохраняем расширенные лимиты трех игр в PostgreSQL на Railway
            await conn.execute(
                """
                INSERT INTO game_stats (user_id, games_played, games_won, daily_wins_rps, daily_wins_hl,
                                        daily_wins_quiz, last_game_date)
                VALUES ($1, 1, $2, $3, $4, $5, $6) ON CONFLICT (user_id) DO
                UPDATE SET
                    games_played = game_stats.games_played + 1,
                    games_won = game_stats.games_won + $2,
                    daily_wins_rps = $3,
                    daily_wins_hl = $4,
                    daily_wins_quiz = $5,
                    last_game_date = $6
                """,
                user_id, 1 if is_win else 0, wins_rps, wins_hl, wins_quiz, today_date
            )
            return True, status_text, new_balance


# ============================================================================
# 🕹️ ИГРА №1: КАМЕНЬ-НОЖНИЦЫ-БУМАГА (КНБ С ЛИМИТОМ 10 ПОБЕД)
# ============================================================================
def get_rps_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🪨 Камень", callback_data="rps_play:rock"),
            types.InlineKeyboardButton(text="✂️ Ножницы", callback_data="rps_play:scissors"),
            types.InlineKeyboardButton(text="🧻 Бумага", callback_data="rps_play:paper")
        ]
    ])


@router.message(Command("rps"))
async def cmd_rps_start(message: types.Message):
    await message.answer(
        "🪨✂️🧻 <b>КАМЕНЬ-НОЖНИЦЫ-БУМАГА С БOТOM</b>\n\n"
        f"Выбирай оружие! Победа: <b>+{WIN_REWARD} рофлов</b>. Проигрыш/Ничья: <b>-{LOSE_PENALTY} рофл</b>.\n"
        f"Суточный лимит этой игры: <b>{LIMITS['rps']} побед</b>.",
        reply_markup=get_rps_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("rps_play:"))
async def process_rps_choice(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    user_choice = callback.data.split(":")[1]

    bot_choice = random.choice(["rock", "scissors", "paper"])
    choices_ru = {"rock": "🪨 Камень", "scissors": "✂️ Ножницы", "paper": "🧻 Бумага"}

    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Сыграть еще раз!", callback_data="game_retry:rps")]
    ])

    if user_choice == bot_choice:
        success, result_text, new_balance = await execute_solo_game_payout(user_id, is_win=False, game_type="rps",
                                                                           is_draw=True)
        if not success:
            await callback.message.edit_text(result_text, reply_markup=retry_kb, parse_mode="HTML")
            return
        final_text = f"🤝 <b>Абсолютная Ничья!</b> Оба выбрали {choices_ru[bot_choice]}.\n\n{result_text}\n💰 Твой баланс: <b>{new_balance} рофлов</b>"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
            (user_choice == "scissors" and bot_choice == "paper") or \
            (user_choice == "paper" and bot_choice == "rock"):
        success, result_text, new_balance = await execute_solo_game_payout(user_id, is_win=True, game_type="rps")
        if not success:
            await callback.message.edit_text(result_text, reply_markup=retry_kb, parse_mode="HTML")
            return
        final_text = f"🏆 <b>Красивая Победа!</b> Твой {choices_ru[user_choice]} сокрушил {choices_ru[bot_choice]}.\n\n{result_text}\n💰 Твой баланс: <b>{new_balance} рофлов</b>"
    else:
        success, result_text, new_balance = await execute_solo_game_payout(user_id, is_win=False, game_type="rps")
        if not success:
            await callback.message.edit_text(result_text, reply_markup=retry_kb, parse_mode="HTML")
            return
        final_text = f"💀 <b>Бот тебя уделал!</b> Его {choices_ru[bot_choice]} победил твой {choices_ru[user_choice]}.\n\n{result_text}\n💰 Твой баланс: <b>{new_balance} рофлов</b>"

    await callback.message.edit_text(final_text, reply_markup=retry_kb, parse_mode="HTML")


# ============================================================================
# 🕹️ ИГРА №2: БОЛЬШЕ / МЕНЬШЕ (УГАДАЙ СКРЫТЫЙ ШАГ С ЛИМИТОМ 10 ПОБЕД)
# ============================================================================
@router.message(Command("high_low"))
async def cmd_high_low(message: types.Message):
    """Первичный запуск игры Больше/Меньше через текстовую команду"""
    base_num = random.randint(10, 90)
    secret_num = random.randint(1, 100)
    if secret_num == base_num:
        secret_num += 1

    # В payload зашиваем вектор направления и скрытое число для защиты от накруток
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="📈 Больше", callback_data=f"hl_play:up:{base_num}:{secret_num}"),
            types.InlineKeyboardButton(text="📉 Меньше", callback_data=f"hl_play:down:{base_num}:{secret_num}")
        ]
    ])
    await message.answer(
        f"🎲 <b>ИГРА «БОЛЬШЕ ИЛИ МЕНЬШЕ»</b>\n\n"
        f"Бот выставил число: <b>{base_num}</b>.\n\n"
        f"Загаданное скрытое число будет БОЛЬШЕ или МЕНЬШЕ этого значения?\n"
        f"Победа: <b>+{WIN_REWARD} рофлов</b> | Сбор за проигрыш: <b>-{LOSE_PENALTY} рофл</b>\n"
        f"Суточный лимит игры: <b>{LIMITS['hl']} побед</b>.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("hl_play:"))
async def process_high_low_choice(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id

    parts = callback.data.split(":")
    if len(parts) < 4:
        return
    _, direction, base_num, secret_num = parts
    base_num, secret_num = int(base_num), int(secret_num)

    is_win = (direction == "up" and secret_num > base_num) or (direction == "down" and secret_num < base_num)
    success, result_text, new_balance = await execute_solo_game_payout(user_id, is_win=is_win, game_type="hl")

    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Сыграть еще раз!", callback_data="game_retry:hl")]
    ])

    if not success:
        # Выводим красивое информационное сообщение об исчерпании лимита без крашей контекста!
        await callback.message.edit_text(result_text, reply_markup=retry_kb, parse_mode="HTML")
        return

    final_text = (
        f"🎲 <b>ИТОГ РАУНДА БОЛЬШЕ/МЕНЬШЕ</b>\n"
        f"..................................................\n\n"
        f"Базовое число бота: <b>{base_num}</b>\n"
        f"Скрытое число оказалось: <b>{secret_num}</b>\n\n"
        f"{result_text}\n"
        f"💰 Твой баланс: <b>{new_balance} рофлов</b>"
    )
    await callback.message.edit_text(final_text, reply_markup=retry_kb, parse_mode="HTML")


# ============================================================================
# 🕹️ ИГРА №3: ИНТЕЛЛЕКТУАЛЬНЫЙ СПРИНТ-ТЕСТ (ВИКТOРИНA С ЛИМИТOМ 20 ПОБЕД)
# ============================================================================
@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext):
    quizzes = [
        {"q": "Какую скорость добычи дает Кибер-Бурильщик в магазине /shop?", "a": "5 рофлов в час",
         "o": ["2 рофла в час", "5 рофлов в час", "10 рофлов в час", "100 рофлов в час"]},
        {"q": "Какое максимальное количество человек может вместить вечный Мега-Клан?", "a": "1000 человек",
         "o": ["50 человек", "100 человек", "500 человек", "1000 человек"]},
        {"q": "Какая максимальная вместимость автоматического Холодильника в игре?", "a": "100 шт.",
         "o": ["10 шт.", "50 шт.", "100 шт.", "500 шт."]},
    ]
    quiz = random.choice(quizzes)
    options = list(quiz["o"])
    random.shuffle(options)

    buttons = []
    for option in options:
        buttons.append([types.InlineKeyboardButton(text=option, callback_data=f"quiz_check:{option}")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await state.update_data(correct_answer=quiz["a"])
    await state.set_state(SoloGameStates.waiting_for_quiz)

    await message.answer(
        f"🧠 <b>ИГРОВОЙ ИНТЕЛЛЕКТУАЛЬНЫЙ ТЕСТ</b>\n"
        f"..................................................\n\n"
        f"❓ <b>Вопрос:</b> {quiz['q']}\n\n"
        f"⚠️ <i>ВНИМАНИЕ! Малейшая ошибка спишет мягкий сбор <b>-{LOSE_PENALTY} рофл</b>, "
        f"верный ответ принесет <b>+{WIN_REWARD} рофла</b>!\n"
        f"Суточный лимит викторины: <b>{LIMITS['quiz']} побед</b>.</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(SoloGameStates.waiting_for_quiz, F.data.startswith("quiz_check:"))
async def process_quiz_answer(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    parts = callback.data.split(":", 1)
    if len(parts) < 2:
        await callback.answer()
        return
    selected = parts[1]

    user_data = await state.get_data()
    correct = user_data.get("correct_answer")

    await state.clear()
    await callback.answer()

    is_win = (selected == correct)
    success, result_text, new_balance = await execute_solo_game_payout(user_id, is_win=is_win, game_type="quiz")

    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Ответить на другой вопрос!", callback_data="game_retry:quiz")]
    ])

    if not success:
        await callback.message.edit_text(result_text, reply_markup=retry_kb, parse_mode="HTML")
        return

    if is_win:
        reply = f"✅ <b>Абсолютно верно!</b>\n\n{result_text}"
    else:
        reply = f"❌ <b>Грубейшая ошибка!</b> Правильный ответ был:\n<code>{correct}</code>\n\n{result_text}"

    await callback.message.edit_text(
        f"📊 <b>ИТОГ ВИКТОРИНЫ:</b>\n"
        f"..................................................\n\n"
        f"{reply}\n"
        f"💰 Твой кошелек: <b>{new_balance} рофлов</b>",
        reply_markup=retry_kb,
        parse_mode="HTML"
    )


# ============================================================================
# 🎯 ЦЕНТРАЛЬНЫЙ ПЕРЕХВАТ КЛИКOВ С КНОПОК РЕВАНША (БЕСШОВНОЕ РЕДАКТИРОВАНИЕ)
# ============================================================================
@router.callback_query(F.data.startswith("game_retry:"))
async def process_game_retry_inline(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    game_type = callback.data.split(":")[1]

    if game_type == "rps":
        await callback.message.edit_text(
            f"🪨✂️🧻 <b>КАМЕНЬ-НОЖНИЦЫ-БУМАГА С БOТOM</b>\n\nВыбирай оружие! Победа: <b>+{WIN_REWARD} рофлов</b>. Проигрыш или Ничья: <b>-{LOSE_PENALTY} рофл</b>.\nСуточный лимит: <b>{LIMITS['rps']} побед</b>.",
            reply_markup=get_rps_keyboard(),
            parse_mode="HTML"
        )
    elif game_type == "hl":
        base_num = random.randint(10, 90)
        secret_num = random.randint(1, 100)
        if secret_num == base_num: secret_num += 1

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="📈 Больше", callback_data=f"hl_play:up:{base_num}:{secret_num}"),
                types.InlineKeyboardButton(text="📉 Меньше", callback_data=f"hl_play:down:{base_num}:{secret_num}")
            ]
        ])
        await callback.message.edit_text(
            f"🎲 <b>ИГРА «БОЛЬШЕ ИЛИ МЕНЬШЕ»</b>\n\nБот выставил число: <b>{base_num}</b>.\n\nЗагаданное скрытое число будет БОЛЬШЕ или МЕНЬШЕ этого значения?\nПобеда: <b>+{WIN_REWARD} рофлов</b> | Сбор за проигрыш: <b>-{LOSE_PENALTY} рофл</b>\nСуточный лимит: <b>{LIMITS['hl']} побед</b>.",
            keyboard_markup=None,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    elif game_type == "quiz":
        quizzes = [
            {"q": "Какую скорость добычи дает Кибер-Бурильщик в магазине /shop?", "a": "5 рофлов в час",
             "o": ["2 рофла в час", "5 рофлов в час", "10 рофлов в час", "100 рофлов в час"]},
            {"q": "Какое максимальное количество человек может вместить вечный Мега-Клан?", "a": "1000 человек",
             "o": ["50 человек", "100 человек", "500 человек", "1000 человек"]},
            {"q": "Какая максимальная вместимость автоматического Холодильника в игре?", "a": "100 шт.",
             "o": ["10 шт.", "50 шт.", "100 шт.", "500 шт."]},
        ]
        quiz = random.choice(quizzes)
        options = list(quiz["o"])
        random.shuffle(options)

        buttons = []
        for option in options:
            buttons.append([types.InlineKeyboardButton(text=option, callback_data=f"quiz_check:{option}")])

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await state.update_data(correct_answer=quiz["a"])
        await state.set_state(SoloGameStates.waiting_for_quiz)

        await callback.message.edit_text(
            f"🧠 <b>ИГРОВОЙ ИНТЕЛЛЕКТУАЛЬНЫЙ ТЕСТ</b>\n\n❓ <b>Вопрос:</b> {quiz['q']}\n\n⚠️ <i>ВНИМАНИЕ! Малейшая ошибка спишет мягкий сбор <b>-{LOSE_PENALTY} рофл</b>, верный ответ принесет <b>+{WIN_REWARD} рофла</b>!\nСуточный лимит: <b>{LIMITS['quiz']} побед</b>.</i>",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
