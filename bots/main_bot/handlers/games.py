import random
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


class SoloGameStates(StatesGroup):
    waiting_for_quiz = State()  # Состояние для удержания викторины в FSM


# ============================================================================
# ⚙️ ЦЕНТРАЛЬНЫЙ ИГРOВOЙ ДВИЖEК (AТOMAPНЫЕ ТРАНЗАКЦИИ С FOR UPDATE)
# ============================================================================
async def execute_solo_game_payout(user_id: int, win_reward: int, lose_penalty: int, is_win: bool) -> tuple[
    bool, str, int]:
    """
    Титановый движок расчета соло-игр холдинга ROFL HUB CORE.
    Автоматически считывает boost_level и добавляет +1, +2 или +3 монеты прямо к выигрышу!
    """
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Вытягиваем баланс и уровень буста вожака
            user = await conn.fetchrow("SELECT balance, boost_level FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return False, "⚠️ Профиль не найден. Нажми /start", 0

            current_balance = user["balance"]
            boost_level = user["boost_level"] or 0

            if not is_win and current_balance < lose_penalty:
                return False, f"❌ У тебя недостаточно Рофлов для оплаты штрафа! Нужно минимум {lose_penalty} монет.", current_balance

            if is_win:
                # 🔥 ИГРОВАЯ МАТЕМАТИКА АНАТОЛИЯ АЛЕКСЕЕВИЧА: Награда + Бонус уровня буста!
                final_reward = win_reward + boost_level
                new_balance = current_balance + final_reward

                if boost_level > 0:
                    status_text = f"🎉 ПОБЕДА! Начислено: <b>+{win_reward} рофлов</b> (и плюс эксклюзивный бонус буста: <b>+{boost_level} рофлов</b>)!"
                else:
                    status_text = f"🎉 ПОБЕДА! Начислено: <b>+{win_reward} рофлов</b>."
            else:
                new_balance = current_balance - lose_penalty
                status_text = f"💀 ПРОИГРЫШ! Списан штраф: <b>-{lose_penalty} рофлов</b>."

            await conn.execute("UPDATE users SET balance = $1 WHERE user_id = $2", new_balance, user_id)

            await conn.execute(
                """
                INSERT INTO game_stats (user_id, games_played, games_won)
                VALUES ($1, 1, $2) ON CONFLICT (user_id) DO
                UPDATE SET
                    games_played = game_stats.games_played + 1,
                    games_won = game_stats.games_won + $2
                """,
                user_id, 1 if is_win else 0
            )
            return True, status_text, new_balance


# ============================================================================
# 🕹️ ИГРА №1: КАМЕНЬ-НОЖНИЦЫ-БУМАГА (КНБ против Бота)
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
        "Выбирай свое оружие. Победа принесет <b>+2 рофла</b>, проигрыш спишет <b>-3 рофла</b>!",
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

    # 🔥 ФИКС: Вшиваем инлайн-кнопку реванша под итогом раунда
    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Сыграть еще раз!", callback_data="game_retry:rps")]
    ])

    if user_choice == bot_choice:
        success, result_text, new_balance = await execute_solo_game_payout(user_id, 0, 1, False)
        final_text = (
            f"🤝 <b>Абсолютная Ничья!</b> Оба выбрали {choices_ru[bot_choice]}.\n"
            f"Списан сбор за раунд: -1 рофл.\n"
            f"💰 Твой баланс: <b>{new_balance} рофлов</b>"
        )
    elif (user_choice == "rock" and bot_choice == "scissors") or \
            (user_choice == "scissors" and bot_choice == "paper") or \
            (user_choice == "paper" and bot_choice == "rock"):
        success, result_text, new_balance = await execute_solo_game_payout(user_id, 2, 3, True)
        final_text = (
            f"🏆 <b>Красивая Победа!</b> Твой {choices_ru[user_choice]} сокрушил {choices_ru[bot_choice]}.\n"
            f"{result_text}\n"
            f"💰 Твой баланс: <b>{new_balance} рофлов</b>"
        )
    else:
        success, result_text, new_balance = await execute_solo_game_payout(user_id, 2, 3, False)
        final_text = (
            f"💀 <b>Бот тебя уделал!</b> Его {choices_ru[bot_choice]} победил твой {choices_ru[user_choice]}.\n"
            f"{result_text}\n"
            f"💰 Твой баланс: <b>{new_balance} рофлов</b>"
        )

    await callback.message.edit_text(final_text, reply_markup=retry_kb, parse_mode="HTML")


# ============================================================================
# 🕹️ ИГРА №2: БOЛЬШЕ / МEНЬШE (Угадай скрытый шаг)
# ============================================================================
@router.message(Command("high_low"))
async def cmd_high_low(message: types.Message):
    base_num = random.randint(10, 90)
    secret_num = random.randint(1, 100)
    if secret_num == base_num:
        secret_num += 1

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
        f"Победа: <b>+2 рофла</b> | Штраф: <b>-3 рофла</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("hl_play:"))
async def process_high_low_choice(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    _, direction, base_num, secret_num = callback.data.split(":")

    base_num, secret_num = int(base_num), int(secret_num)

    is_win = (direction == "up" and secret_num > base_num) or (direction == "down" and secret_num < base_num)
    success, result_text, new_balance = await execute_solo_game_payout(user_id, 2, 3, is_win)

    if not success:
        await callback.message.answer(result_text)
        return

    # 🔥 ФИКС: Кнопка быстрого перезапуска раунда Больше/Меньше
    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Сыграть еще раз!", callback_data="game_retry:hl")]
    ])

    final_text = (
        f"🎲 <b>ИТОГ РАУНДА БOЛЬШE/МEНЬШE</b>\n"
        f"..................................................\n\n"
        f"Базовое число бота: <b>{base_num}</b>\n"
        f"Скрытое число оказалось: <b>{secret_num}</b>\n\n"
        f"{result_text}\n"
        f"💰 Твой баланс: <b>{new_balance} рофлов</b>"
    )
    await callback.message.edit_text(final_text, reply_markup=retry_kb, parse_mode="HTML")


# ============================================================================
# 🕹️ ИГРА №3: ИНТЕЛЛЕКТУАЛЬНЫЙ СПРИНТ-ТЕСТ (Викторина)
# ============================================================================
@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext):
    # Наш выверенный пакет вопросов от ассистентов
    quizzes = [
        {"q": "Какой робот-майнер в /shop стоит ровно ★ 99 Stars?", "a": "⚡ Робот «Кибер Бурильщик»",
         "o": ["🤖 Робот «Младший Майнер»", "⚡ Робот «Кибер Бурильщик»", "🥩 10 кибер-котлет", "👑 Бандл «VIP-Старт»"]},
        {"q": "Какая база данных хранит профили нашей империи на Railway?", "a": "PostgreSQL",
         "o": ["MongoDB", "MySQL", "PostgreSQL", "Redis"]},
        {"q": "Какая максимальная вместимость Центрального Холодильника в игре?", "a": "100 шт.",
         "o": ["10 шт.", "50 шт.", "100 шт.", "Бесконечно"]},
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
        f"🧠 <b>ШКОЛЬНЫЙ ИНТЕЛЛЕКТУАЛЬНЫЙ ТЕСТ</b>\n"
        f"..................................................\n\n"
        f"❓ <b>Вопрос:</b> {quiz['q']}\n\n"
        f"⚠️ <i>ВНИМАНИЕ! Малейшая ошибка активирует капкан списания <b>-5 рофлов</b>, "
        f"верный ответ принесет всего <b>+2 рофла</b>!</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(SoloGameStates.waiting_for_quiz, F.data.startswith("quiz_check:"))
async def process_quiz_answer(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    selected = callback.data.split(":", 1)[1]  # Исправлено извлечение строки ответа

    user_data = await state.get_data()
    correct = user_data.get("correct_answer")

    await state.clear()
    await callback.answer()

    is_win = (selected == correct)
    success, result_text, new_balance = await execute_solo_game_payout(user_id, 2, 5, is_win)

    if not success:
        await callback.message.answer(result_text)
        return

    # Кнопка быстрого перезапуска раунда Викторины
    retry_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Ответить на другой вопрос!", callback_data="game_retry:quiz")]
    ])

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
# 🎯 ЦЕНТРАЛЬНЫЙ ПЕРЕХВАТ КЛИКOВ С КНОПОК РЕВАНША (БЫСТРЫЙ RESTART)
# ============================================================================
@router.callback_query(F.data.startswith("game_retry:"))
async def process_game_retry_inline(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    game_type = callback.data.split(":")[1]

    # Стираем старый итог раунда, чтобы чат оставался чистым и неоновым
    await callback.message.delete()

    if game_type == "rps":
        await cmd_rps_start(callback.message)
    elif game_type == "hl":
        await cmd_high_low(callback.message)
    elif game_type == "quiz":
        await cmd_quiz_start(callback.message, state)
