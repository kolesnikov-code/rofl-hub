"""
Соло-игры против бота: КНБ, Больше/Меньше, Викторина, Орёл/Решка, Кубики, Сейф.

Единый движок execute_solo_game_payout(): лимиты побед по UTC-дате, учёт купленного
безлимита (users.unlimit_until), все движения монет — через ledger.

Викторина (Блок 3): таймер 10 секунд на ответ (вотчдог-задача; не успел — проигрыш)
и уровни — каждые 30 верных ответов дают +500 рофлов.
"""
from __future__ import annotations

import asyncio
import logging
import random

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bots.main_bot.utils.questions_loader import get_question_by_id, get_random_question
from shared.database import db
from shared.economy import (
    DAILY_WIN_LIMITS,
    DEFAULT_DAILY_WIN_LIMIT,
    LOSE_PENALTY,
    QUIZ_ANSWER_SECONDS,
    QUIZ_ANSWERS_PER_LEVEL,
    QUIZ_LEVEL_UP_BONUS,
    SAFE_CODES_COUNT,
    SAFE_WIN_REWARD,
    WIN_REWARD,
    is_active,
    quiz_answers_to_next_level,
    quiz_level_for,
    utcnow,
    win_reward_for,
)
from shared.ledger import InsufficientFunds, change_balance

router = Router()
logger = logging.getLogger(__name__)

GAME_TITLES = {
    "rps": "Камень-Ножницы-Бумага",
    "hl": "Больше/Меньше",
    "quiz": "Викторина",
    "coin": "Орёл/Решка",
    "dice": "Кубики",
    "safe": "Сейф",
}
WIN_COLUMNS = {
    "rps": "daily_wins_rps",
    "hl": "daily_wins_hl",
    "quiz": "daily_wins_quiz",
    "coin": "daily_wins_coin",
    "dice": "daily_wins_dice",
    "safe": "daily_wins_safe",
}
_ALL_WIN_COLUMNS = tuple(WIN_COLUMNS.values())


class SoloGameStates(StatesGroup):
    waiting_for_quiz = State()


def limit_for(game_type: str) -> int:
    return DAILY_WIN_LIMITS.get(game_type, DEFAULT_DAILY_WIN_LIMIT)


# ============================================================================
# Чистые правила раундов (без БД и Telegram — на них юнит-тесты)
# ============================================================================
RPS_BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
RPS_NAMES = {"rock": "🪨 Камень", "scissors": "✂️ Ножницы", "paper": "🧻 Бумага"}
COIN_NAMES = {"heads": "🦅 Орёл", "tails": "🪙 Решка"}


def rps_outcome(user_choice: str, bot_choice: str) -> tuple[bool, bool]:
    """(победа, ничья) для КНБ."""
    if user_choice == bot_choice:
        return False, True
    return RPS_BEATS[user_choice] == bot_choice, False


def hl_outcome(direction: str, base: int, secret: int) -> bool:
    return (direction == "up" and secret > base) or (direction == "down" and secret < base)


def coin_outcome(choice: str, result: str) -> bool:
    return choice == result


def dice_outcome(player: int, bot: int) -> tuple[bool, bool]:
    """(победа, ничья) для Кубиков: больше очков — победа."""
    return player > bot, player == bot


def safe_outcome(guess: int, code: int) -> bool:
    return guess == code


# ============================================================================
# Единый движок результата раунда
# ============================================================================
async def execute_solo_game_payout(user_id: int, is_win: bool, game_type: str,
                                   is_draw: bool = False) -> tuple[bool, str, int]:
    """
    Возвращает (успех, текст, новый баланс). Успех=False означает: раунд не засчитан
    (лимит, нет монет, нет профиля) — текст объясняет почему.
    """
    now = utcnow()
    today = now.date()
    column = WIN_COLUMNS.get(game_type, "daily_wins_rps")
    max_limit = limit_for(game_type)
    reward = win_reward_for(game_type)

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow(
                "SELECT balance, unlimit_until FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return False, "⚠️ Профиль не найден. Нажми /start", 0

            stats = await conn.fetchrow(
                "SELECT * FROM game_stats WHERE user_id = $1 FOR UPDATE", user_id)

            same_day = bool(stats and stats["last_game_date"] == today)
            wins_today = stats[column] if same_day else 0
            unlimited = is_active(user["unlimit_until"], now)

            if is_win and not unlimited and wins_today >= max_limit:
                return False, (
                    f"🛑 <b>Суточный лимит достигнут!</b>\n\n"
                    f"В игре {GAME_TITLES.get(game_type, game_type)} ты уже забрал {max_limit} побед на сегодня. "
                    f"Лимит обновится в 00:00 UTC.\n\n"
                    f"⚡ Снять лимит на 24 часа — 5 ★, на 30 дней — 99 ★ (раздел «Игровые» в /shop)."
                ), user["balance"]

            if is_win:
                new_balance = await change_balance(conn, user_id, reward, f"game_win:{game_type}")
                status = f"🎉 ПОБЕДА! Начислено: <b>+{reward} рофл.</b>"
            else:
                try:
                    new_balance = await change_balance(conn, user_id, -LOSE_PENALTY, f"game_loss:{game_type}")
                except InsufficientFunds:
                    return False, "❌ У тебя 0 рофлов — нечем оплатить сбор раунда. Забери доход с фермы в /farm!", \
                        user["balance"]
                status = (f"🤝 НИЧЬЯ! Сбор раунда: <b>-{LOSE_PENALTY} рофл</b>." if is_draw
                          else f"💀 ПРОИГРЫШ! Сбор раунда: <b>-{LOSE_PENALTY} рофл</b>.")

            # Счётчики: при смене дня все суточные колонки обнуляются
            if same_day:
                await conn.execute(
                    f"""
                    INSERT INTO game_stats (user_id, games_played, games_won, {column}, last_game_date)
                    VALUES ($1, 1, $2, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE SET
                        games_played = game_stats.games_played + 1,
                        games_won = game_stats.games_won + $2,
                        {column} = game_stats.{column} + $2,
                        last_game_date = $3
                    """,
                    user_id, 1 if is_win else 0, today)
            else:
                zero_all = ", ".join(f"{c} = 0" for c in _ALL_WIN_COLUMNS if c != column)
                await conn.execute(
                    f"""
                    INSERT INTO game_stats (user_id, games_played, games_won, {column}, last_game_date)
                    VALUES ($1, 1, $2, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE SET
                        games_played = game_stats.games_played + 1,
                        games_won = game_stats.games_won + $2,
                        {zero_all},
                        {column} = $2,
                        last_game_date = $3
                    """,
                    user_id, 1 if is_win else 0, today)

            # Уровни викторины: каждые 30 верных ответов — +500 рофлов
            if is_win and game_type == "quiz":
                total = await conn.fetchval(
                    "UPDATE game_stats SET quiz_correct_total = quiz_correct_total + 1 "
                    "WHERE user_id = $1 RETURNING quiz_correct_total", user_id)
                if total % QUIZ_ANSWERS_PER_LEVEL == 0:
                    level = quiz_level_for(total)
                    await conn.execute("UPDATE game_stats SET quiz_level = $2 WHERE user_id = $1",
                                       user_id, level)
                    new_balance = await change_balance(conn, user_id, QUIZ_LEVEL_UP_BONUS,
                                                       "quiz_level_up", str(level))
                    status += (f"\n\n🏅 <b>НОВЫЙ УРОВЕНЬ ВИКТОРИНЫ: {level}!</b> "
                               f"Бонус: <b>+{QUIZ_LEVEL_UP_BONUS} рофлов</b>!")
                else:
                    status += f"\n📚 До следующего уровня: <b>{quiz_answers_to_next_level(total)}</b> верных ответов."

            return True, status, new_balance


def _retry_kb(game_type: str, label: str = "🎮 Сыграть ещё раз!") -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=label, callback_data=f"game_retry:{game_type}")],
        [types.InlineKeyboardButton(text="🕹️ Игровая зона", callback_data="games_hub")],
    ])


# ============================================================================
# Игра 1: Камень-Ножницы-Бумага
# ============================================================================
def get_rps_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="🪨 Камень", callback_data="rps_play:rock"),
        types.InlineKeyboardButton(text="✂️ Ножницы", callback_data="rps_play:scissors"),
        types.InlineKeyboardButton(text="🧻 Бумага", callback_data="rps_play:paper"),
    ]])


def rps_intro_text() -> str:
    return (f"🪨✂️🧻 <b>КАМЕНЬ-НОЖНИЦЫ-БУМАГА</b>\n\n"
            f"Победа: <b>+{WIN_REWARD}</b> · Проигрыш/ничья: <b>-{LOSE_PENALTY}</b>\n"
            f"Лимит побед в сутки: <b>{limit_for('rps')}</b>")


@router.message(Command("rps"))
async def cmd_rps_start(message: types.Message):
    await message.answer(rps_intro_text(), reply_markup=get_rps_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.startswith("rps_play:"))
async def process_rps_choice(callback: types.CallbackQuery):
    await callback.answer()
    user_choice = callback.data.split(":", 1)[1]
    if user_choice not in RPS_BEATS:
        return
    bot_choice = random.choice(list(RPS_BEATS))
    is_win, is_draw = rps_outcome(user_choice, bot_choice)

    if is_draw:
        headline = f"🤝 <b>Ничья!</b> Оба выбрали {RPS_NAMES[bot_choice]}."
    elif is_win:
        headline = f"🏆 <b>Победа!</b> {RPS_NAMES[user_choice]} бьёт {RPS_NAMES[bot_choice]}."
    else:
        headline = f"💀 <b>Бот победил.</b> {RPS_NAMES[bot_choice]} бьёт {RPS_NAMES[user_choice]}."

    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "rps", is_draw=is_draw)
    body = text if not ok else f"{headline}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>"
    await _safe_edit(callback.message, body, _retry_kb("rps"))


# ============================================================================
# Игра 2: Больше / Меньше
# ============================================================================
def _hl_round() -> tuple[str, types.InlineKeyboardMarkup]:
    base = random.randint(10, 90)
    secret = random.randint(1, 100)
    if secret == base:
        secret += 1
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="📈 Больше", callback_data=f"hl_play:up:{base}:{secret}"),
        types.InlineKeyboardButton(text="📉 Меньше", callback_data=f"hl_play:down:{base}:{secret}"),
    ]])
    text = (f"🎲 <b>БОЛЬШЕ ИЛИ МЕНЬШЕ</b>\n\nБот выставил число: <b>{base}</b>.\n"
            f"Скрытое число будет больше или меньше?\n"
            f"Победа: <b>+{WIN_REWARD}</b> · Проигрыш: <b>-{LOSE_PENALTY}</b> · Лимит: <b>{limit_for('hl')}</b> побед")
    return text, kb


@router.message(Command("high_low"))
async def cmd_high_low(message: types.Message):
    text, kb = _hl_round()
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("hl_play:"))
async def process_high_low_choice(callback: types.CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    if len(parts) != 4 or not (parts[2].isdigit() and parts[3].isdigit()):
        return
    direction, base, secret = parts[1], int(parts[2]), int(parts[3])
    is_win = hl_outcome(direction, base, secret)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "hl")
    body = text if not ok else (f"🎲 <b>ИТОГ РАУНДА</b>\n\nЧисло бота: <b>{base}</b> · Скрытое: <b>{secret}</b>\n\n"
                                f"{text}\n💰 Баланс: <b>{balance} рофлов</b>")
    await _safe_edit(callback.message, body, _retry_kb("hl"))


# ============================================================================
# Игра 3: Викторина — таймер 10 секунд и уровни по 30 верных ответов
# ============================================================================
def _quiz_round(question: dict, level: int, correct_total: int) -> tuple[str, types.InlineKeyboardMarkup, int]:
    """Возвращает текст, клавиатуру и индекс правильного ответа в перемешанном порядке."""
    options = list(question["options"])
    random.shuffle(options)
    correct_idx = options.index(question["correct"])
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=opt, callback_data=f"quiz_check:{question['id']}:{i}")]
        for i, opt in enumerate(options)
    ])
    text = (f"🧠 <b>ВИКТОРИНА · {question['category']}</b>\n"
            f"🏅 Уровень: <b>{level}</b> · До следующего: <b>{quiz_answers_to_next_level(correct_total)}</b> верных\n\n"
            f"❓ {question['q']}\n\n"
            f"⏱ <b>На ответ — {QUIZ_ANSWER_SECONDS} секунд!</b> Не успел — проигрыш.\n"
            f"<i>Верно: <b>+{WIN_REWARD}</b> · Ошибка: <b>-{LOSE_PENALTY}</b> · Лимит: <b>{limit_for('quiz')}</b> побед</i>")
    return text, kb, correct_idx


async def _quiz_timeout_watchdog(message: types.Message, state: FSMContext, token: int, user_id: int) -> None:
    """Через 10 секунд закрывает неотвеченный вопрос как проигрыш."""
    await asyncio.sleep(QUIZ_ANSWER_SECONDS)
    try:
        if await state.get_state() != SoloGameStates.waiting_for_quiz.state:
            return
        data = await state.get_data()
        if data.get("quiz_token") != token:
            return  # уже другой вопрос
        await state.clear()
        ok, text, balance = await execute_solo_game_payout(user_id, False, "quiz")
        body = f"⏰ <b>ВРЕМЯ ВЫШЛО!</b> На ответ даётся {QUIZ_ANSWER_SECONDS} секунд.\n\n{text}"
        if ok:
            body += f"\n💰 Баланс: <b>{balance} рофлов</b>"
        await _safe_edit(message, body, _retry_kb("quiz", "🧠 Новый вопрос"))
    except Exception:
        logger.exception("[QUIZ_TIMER] сбой вотчдога user=%s", user_id)


async def _start_quiz(target: types.Message, state: FSMContext, user_id: int, edit: bool) -> None:
    question = get_random_question()
    if question is None:
        await target.answer("⚠️ База вопросов пуста. Сообщи администратору.")
        return

    async with db.pool.acquire() as conn:
        total = await conn.fetchval(
            "SELECT quiz_correct_total FROM game_stats WHERE user_id = $1", user_id) or 0

    text, kb, correct_idx = _quiz_round(question, quiz_level_for(total), total)
    token = random.getrandbits(62)
    await state.set_state(SoloGameStates.waiting_for_quiz)
    await state.update_data(quiz_qid=question["id"], quiz_correct=correct_idx, quiz_token=token)
    if edit:
        sent = await _safe_edit(target, text, kb)
    else:
        sent = await target.answer(text, reply_markup=kb, parse_mode="HTML")
    asyncio.create_task(_quiz_timeout_watchdog(sent or target, state, token, user_id))


@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext):
    await _start_quiz(message, state, message.from_user.id, edit=False)


@router.callback_query(SoloGameStates.waiting_for_quiz, F.data.startswith("quiz_check:"))
async def process_quiz_answer(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    qid, chosen = int(parts[1]), int(parts[2])

    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if data.get("quiz_qid") != qid:
        await _safe_edit(callback.message, "⏳ Этот вопрос уже не активен. Запусти новый!",
                         _retry_kb("quiz", "🧠 Новый вопрос"))
        return

    is_win = chosen == data.get("quiz_correct")
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "quiz")
    if not ok:
        await _safe_edit(callback.message, text, _retry_kb("quiz", "🧠 Новый вопрос"))
        return

    question = get_question_by_id(qid)
    verdict = "✅ <b>Верно!</b>" if is_win else \
        f"❌ <b>Ошибка.</b> Правильный ответ: <code>{question['correct'] if question else '—'}</code>"
    await _safe_edit(callback.message, f"📊 <b>ИТОГ</b>\n\n{verdict}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>",
                     _retry_kb("quiz", "🧠 Новый вопрос"))


@router.callback_query(F.data.startswith("quiz_check:"))
async def process_quiz_answer_stale(callback: types.CallbackQuery):
    """Клик по старому вопросу вне состояния — без начислений."""
    await callback.answer("Этот вопрос уже не активен. Запусти новый!", show_alert=True)


# ============================================================================
# Игра 4: Орёл / Решка
# ============================================================================
def get_coin_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="🦅 Орёл", callback_data="coin_play:heads"),
        types.InlineKeyboardButton(text="🪙 Решка", callback_data="coin_play:tails"),
    ]])


def coin_intro_text() -> str:
    return (f"🪙 <b>ОРЁЛ ИЛИ РЕШКА</b>\n\n"
            f"Бот подбрасывает кибер-монету. Угадай, какой стороной она упадёт!\n"
            f"Победа: <b>+{WIN_REWARD}</b> · Проигрыш: <b>-{LOSE_PENALTY}</b> · Лимит: <b>{limit_for('coin')}</b> побед")


@router.message(Command("coin"))
async def cmd_coin_start(message: types.Message):
    await message.answer(coin_intro_text(), reply_markup=get_coin_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.startswith("coin_play:"))
async def process_coin_choice(callback: types.CallbackQuery):
    await callback.answer()
    choice = callback.data.split(":", 1)[1]
    if choice not in COIN_NAMES:
        return
    result = random.choice(("heads", "tails"))
    is_win = coin_outcome(choice, result)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "coin")
    headline = (f"🪙 Монета крутится... выпал <b>{COIN_NAMES[result]}</b>! "
                f"Твоя ставка: {COIN_NAMES[choice]}.")
    body = text if not ok else f"{headline}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>"
    await _safe_edit(callback.message, body, _retry_kb("coin"))


# ============================================================================
# Игра 5: Кубики (анимированные 🎲 Telegram)
# ============================================================================
DICE_ANIMATION_SECONDS = 3.2  # длительность анимации 🎲 в клиентах Telegram


def dice_intro_text() -> str:
    return (f"🎲 <b>КУБИКИ</b>\n\n"
            f"Ты и бот бросаете по кубику. У кого больше очков — тот забирает раунд!\n"
            f"Победа: <b>+{WIN_REWARD}</b> · Проигрыш/ничья: <b>-{LOSE_PENALTY}</b> · "
            f"Лимит: <b>{limit_for('dice')}</b> побед")


def get_dice_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="🎲 БРОСИТЬ КУБИКИ", callback_data="dice_play"),
    ]])


@router.message(Command("dice"))
async def cmd_dice_start(message: types.Message):
    await message.answer(dice_intro_text(), reply_markup=get_dice_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "dice_play")
async def process_dice_roll(callback: types.CallbackQuery):
    await callback.answer("Кубики брошены!")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)  # защита от даблклика
    except Exception:
        pass

    player_msg = await callback.message.answer_dice(emoji="🎲")
    bot_msg = await callback.message.answer_dice(emoji="🎲")
    await asyncio.sleep(DICE_ANIMATION_SECONDS)

    player, bot_roll = player_msg.dice.value, bot_msg.dice.value
    is_win, is_draw = dice_outcome(player, bot_roll)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "dice", is_draw=is_draw)
    headline = f"🎲 Твой кубик (первый): <b>{player}</b> · Кубик бота: <b>{bot_roll}</b>"
    body = text if not ok else f"{headline}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>"
    await callback.message.answer(body, reply_markup=_retry_kb("dice"), parse_mode="HTML")


# ============================================================================
# Игра 6: Сейф — подбери код из 4 вариантов, куш больше
# ============================================================================
def _safe_round() -> tuple[str, types.InlineKeyboardMarkup]:
    code = random.randint(1, SAFE_CODES_COUNT)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=f"🔢 {i}", callback_data=f"safe_play:{i}:{code}")
        for i in range(1, SAFE_CODES_COUNT + 1)
    ]])
    text = (f"🔐 <b>КИБЕР-СЕЙФ</b>\n\n"
            f"Внутри — куш <b>{SAFE_WIN_REWARD} рофлов</b>! Дверца заперта кодом "
            f"от 1 до {SAFE_CODES_COUNT}. У тебя одна попытка.\n"
            f"Вскрыл: <b>+{SAFE_WIN_REWARD}</b> · Сигнализация: <b>-{LOSE_PENALTY}</b> · "
            f"Лимит: <b>{limit_for('safe')}</b> побед")
    return text, kb


@router.message(Command("safe"))
async def cmd_safe_start(message: types.Message):
    text, kb = _safe_round()
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("safe_play:"))
async def process_safe_guess(callback: types.CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        return
    guess, code = int(parts[1]), int(parts[2])
    is_win = safe_outcome(guess, code)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "safe")
    headline = (f"🔓 <b>Сейф вскрыт!</b> Код был: <b>{code}</b>." if is_win
                else f"🚨 <b>Сработала сигнализация!</b> Ты набрал {guess}, а код был: <b>{code}</b>.")
    body = text if not ok else f"{headline}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>"
    await _safe_edit(callback.message, body, _retry_kb("safe", "🔐 Взломать ещё раз!"))


# ============================================================================
# Реванш
# ============================================================================
@router.callback_query(F.data.startswith("game_retry:"))
async def process_game_retry_inline(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    game_type = callback.data.split(":", 1)[1]
    if game_type == "rps":
        await _safe_edit(callback.message, rps_intro_text(), get_rps_keyboard())
    elif game_type == "hl":
        text, kb = _hl_round()
        await _safe_edit(callback.message, text, kb)
    elif game_type == "quiz":
        await _start_quiz(callback.message, state, callback.from_user.id, edit=True)
    elif game_type == "coin":
        await _safe_edit(callback.message, coin_intro_text(), get_coin_keyboard())
    elif game_type == "dice":
        await _safe_edit(callback.message, dice_intro_text(), get_dice_keyboard())
    elif game_type == "safe":
        text, kb = _safe_round()
        await _safe_edit(callback.message, text, kb)


async def _safe_edit(message: types.Message, text: str,
                     kb: types.InlineKeyboardMarkup) -> types.Message | None:
    try:
        result = await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        return result if isinstance(result, types.Message) else message
    except Exception:
        return await message.answer(text, reply_markup=kb, parse_mode="HTML")
