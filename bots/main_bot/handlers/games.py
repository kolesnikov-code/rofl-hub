import random
import logging
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from shared.database import db  # Твой официальный экземпляр класса БД

router = Router()
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------
# 🎭 FSM СОСТОЯНИЯ ДЛЯ СОЛО-ВИКТОРИНЫ С 4 ВАРИАНТАМИ
# ----------------------------------------------------------------
class QuizStates(StatesGroup):
    waiting_for_answer = State()


# ================================================================
# ⚙️ ТИТАНОВЫЙ ИГРОВОЙ ДВИЖЕК (CORE ENGINE)
# ================================================================
class BaseGameEngine:
    @staticmethod
    async def execute_solo_round(user_id: int, win_reward: int, lose_penalty: int, is_win: bool) -> tuple[
        bool, str, int]:
        """
        Универсальный асинхронный движок для соло-игр против бота.
        Выполняет ленивый расчёт баланса, начисляет выигрыш или списывает жесткий штраф.
        Возвращает: (Успех_транзакции: bool, Сообщение: str, Текущий_баланс: int)
        """
        async with db.pool.acquire() as conn:
            # Открываем изолированную транзакцию asyncpg (Race Condition = 0%)
            async with conn.transaction():
                # Блокируем строку юзера для предотвращения параллельных кликов
                user = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1 FOR UPDATE", user_id)
                if not user:
                    return False, "⚠️ Профиль не найден. Нажми /start", 0

                current_balance = user["balance"]

                # Если это проигрыш, проверяем, есть ли у ребенка монеты на оплату штрафа
                if not is_win and current_balance < lose_penalty:
                    return False, f"❌ У тебя недостаточно Рофлов для оплаты штрафа! Нужно минимум {lose_penalty} монет.", current_balance

                # Рассчитываем дефляционный итог
                if is_win:
                    new_balance = current_balance + win_reward
                    status_text = f"🎉 ПОБЕДА! Начислено: <b>+{win_reward} рофлов</b>."
                else:
                    new_balance = current_balance - lose_penalty
                    status_text = f"💀 ПРОИГРЫШ! Списан штраф: <b>-{lose_penalty} рофлов</b>."

                # Фиксируем изменения в PostgreSQL на Railway
                await conn.execute("UPDATE users SET balance = $1 WHERE user_id = $2", new_balance, user_id)

                # Записываем раунд в общую статистику
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


# ================================================================
# 🕹️ ИГРА №1: БЫСТРАЯ ДУЭЛЬ 50/50 (Твоё матожидание +2 / -3)
# ================================================================
@router.message(Command("duel_bot"))
async def cmd_duel_bot(message: types.Message):
    user_id = message.from_user.id

    # Хладнокровный рандом 50/50
    is_win = random.choice([True, False])

    # Вызываем наш движок с твоей жесткой математикой против авто-кликеров
    success, result_text, new_balance = await BaseGameEngine.execute_solo_round(
        user_id=user_id,
        win_reward=2,  # Награда за успех
        lose_penalty=3,  # Жесткий штраф за проигрыш
        is_win=is_win
    )

    if not success:
        await message.answer(result_text)
        return

    response = (
        f"🎲 <b>БЫСТРАЯ КИБЕР-ДУЭЛЬ С БОТОМ</b>\n"
        f"..................................................\n\n"
        f"Бот выбросил силовое поле... Твой удар...\n\n"
        f"{result_text}\n"
        f"💰 Твой новый баланс: <b>{new_balance} рофлов</b>\n\n"
        f"..................................................\n"
        f"🔥 <i>На дистанции бот всегда заберёт своё. Прокачивай ферму в /shop, чтобы не рисковать балансом!</i>"
    )
    await message.answer(response, parse_mode="HTML")


# ================================================================
# 🧠 ИГРА №2: ИНТЕЛЛЕКТУАЛЬНАЯ ВИКТОРИНА (4 варианта, штраф -5)
# ================================================================
@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext):
    # Пул жестких вопросов для проверки интеллекта подростков
    quizzes = [
        {"q": "Какая функция в Python используется для вывода текста в консоль?", "a": "print",
         "o": ["input", "print", "output", "len"]},
        {"q": "Что такое Railway в нашей экосистеме?", "a": "Хостинг",
         "o": ["База данных", "Хостинг", "Язык кода", "Бот"]},
        {"q": "Какая базовая валюта зашита в шлюз /shop?", "a": "Stars", "o": ["Рофлы", "Рубли", "Stars", "Доллары"]},
    ]

    quiz = random.choice(quizzes)

    # Генерируем инлайн-кнопки с 4 вариантами ответа
    buttons = []
    for option in quiz["o"]:
        buttons.append([types.InlineKeyboardButton(text=option, callback_data=f"quiz_ans:{option}")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    # Запираем данные вопроса в кэш FSM сессии ребенка
    await state.update_data(correct_answer=quiz["a"])
    await state.set_state(QuizStates.waiting_for_answer)

    await message.answer(
        f"🧠 <b>ИНТЕЛЛЕКТУАЛЬНЫЙ СПРИНТ-ТЕСТ</b>\n"
        f"..................................................\n\n"
        f"❓ <b>Вопрос:</b> {quiz['q']}\n\n"
        f"⚠️ <i>ВНИМАНИЕ! У тебя 4 варианта ответа. Вероятность ошибки 75%. "
        f"Успех принесет <b>+2 рофла</b>, малейший просчет спишет жесткий штраф <b>-5 рофлов</b>!</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(QuizStates.waiting_for_answer, F.data.startswith("quiz_ans:"))
async def process_quiz_answer(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    selected_answer = callback.data.split(":")[1]

    # Достаем правильный ответ из кэша памяти
    user_data = await state.get_data()
    correct_answer = user_data.get("correct_answer")

    # Сбрасываем FSM состояние
    await state.clear()
    await callback.answer()

    is_win = (selected_answer == correct_answer)

    # Вызываем асинхронный движок с капканом мясорубки (+2 / -5)
    success, result_text, new_balance = await BaseGameEngine.execute_solo_round(
        user_id=user_id,
        win_reward=2,
        lose_penalty=5,
        is_win=is_win
    )

    if not success:
        await callback.message.answer(result_text)
        return

    if is_win:
        final_reply = f"✅ <b>Абсолютно верно!</b> Ты выбрал: <code>{selected_answer}</code>.\n\n{result_text}"
    else:
        final_reply = f"❌ <b>Грубейшая ошибка!</b> Правильный ответ был: <b>{correct_answer}</b>.\n\n{result_text}"

    response = (
        f"📊 <b>ИТОГ ИНТЕЛЛЕКТУАЛЬНОГО РАУНДА</b>\n"
        f"..................................................\n\n"
        f"{final_reply}\n"
        f"💰 Твой текущий кошелек: <b>{new_balance} рофлов</b>\n"
        f"..................................................\n"
        f"🤖 <i>Тыкать наугад — банкротство. Включай мозги или заправляй Бурильщиков!</i>"
    )

    # Красиво меняем текст вопроса на результат раунда на экране смартфона
    await callback.message.edit_text(response, parse_mode="HTML")
