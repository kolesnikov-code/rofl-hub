"""
Соло-игры против бота: КНБ, Больше/Меньше, Викторина.

Единый движок execute_solo_game_payout(): лимиты побед по UTC-дате, учёт купленного
безлимита (users.unlimit_until), все движения монет — через ledger.
"""
from __future__ import annotations

import logging
import random

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bots.main_bot.utils.questions_loader import get_question_by_id, get_random_question
from shared.database import db
from shared.economy import DAILY_WIN_LIMITS, DEFAULT_DAILY_WIN_LIMIT, LOSE_PENALTY, WIN_REWARD, is_active, utcnow
from shared.ledger import InsufficientFunds, change_balance

router = Router()
logger = logging.getLogger(__name__)

GAME_TITLES = {"rps": "Камень-Ножницы-Бумага", "hl": "Больше/Меньше", "quiz": "Викторина"}
WIN_COLUMNS = {"rps": "daily_wins_rps", "hl": "daily_wins_hl", "quiz": "daily_wins_quiz"}


class SoloGameStates(StatesGroup):
    waiting_for_quiz = State()


def limit_for(game_type: str) -> int:
    return DAILY_WIN_LIMITS.get(game_type, DEFAULT_DAILY_WIN_LIMIT)


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

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow(
                "SELECT balance, unlimit_until FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return False, "⚠️ Профиль не найден. Нажми /start", 0

            stats = await conn.fetchrow(
                "SELECT daily_wins_rps, daily_wins_hl, daily_wins_quiz, last_game_date "
                "FROM game_stats WHERE user_id = $1 FOR UPDATE", user_id)

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
                new_balance = await change_balance(conn, user_id, WIN_REWARD, f"game_win:{game_type}")
                status = f"🎉 ПОБЕДА! Начислено: <b>+{WIN_REWARD} рофла</b>."
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
                await conn.execute(
                    f"""
                    INSERT INTO game_stats (user_id, games_played, games_won, {column}, last_game_date)
                    VALUES ($1, 1, $2, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE SET
                        games_played = game_stats.games_played + 1,
                        games_won = game_stats.games_won + $2,
                        daily_wins_rps = 0, daily_wins_hl = 0, daily_wins_quiz = 0,
                        {column} = $2,
                        last_game_date = $3
                    """,
                    user_id, 1 if is_win else 0, today)

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


RPS_BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
RPS_NAMES = {"rock": "🪨 Камень", "scissors": "✂️ Ножницы", "paper": "🧻 Бумага"}


@router.callback_query(F.data.startswith("rps_play:"))
async def process_rps_choice(callback: types.CallbackQuery):
    await callback.answer()
    user_choice = callback.data.split(":", 1)[1]
    if user_choice not in RPS_BEATS:
        return
    bot_choice = random.choice(list(RPS_BEATS))

    if user_choice == bot_choice:
        ok, text, balance = await execute_solo_game_payout(callback.from_user.id, False, "rps", is_draw=True)
        headline = f"🤝 <b>Ничья!</b> Оба выбрали {RPS_NAMES[bot_choice]}."
    elif RPS_BEATS[user_choice] == bot_choice:
        ok, text, balance = await execute_solo_game_payout(callback.from_user.id, True, "rps")
        headline = f"🏆 <b>Победа!</b> {RPS_NAMES[user_choice]} бьёт {RPS_NAMES[bot_choice]}."
    else:
        ok, text, balance = await execute_solo_game_payout(callback.from_user.id, False, "rps")
        headline = f"💀 <b>Бот победил.</b> {RPS_NAMES[bot_choice]} бьёт {RPS_NAMES[user_choice]}."

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
    is_win = (direction == "up" and secret > base) or (direction == "down" and secret < base)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "hl")
    body = text if not ok else (f"🎲 <b>ИТОГ РАУНДА</b>\n\nЧисло бота: <b>{base}</b> · Скрытое: <b>{secret}</b>\n\n"
                                f"{text}\n💰 Баланс: <b>{balance} рофлов</b>")
    await _safe_edit(callback.message, body, _retry_kb("hl"))


# ============================================================================
# Игра 3: Викторина (вопросы из data/questions.csv)
# ============================================================================
def _quiz_round(question: dict) -> tuple[str, types.InlineKeyboardMarkup, int]:
    """Возвращает текст, клавиатуру и индекс правильного ответа в перемешанном порядке."""
    options = list(question["options"])
    random.shuffle(options)
    correct_idx = options.index(question["correct"])
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=opt, callback_data=f"quiz_check:{question['id']}:{i}")]
        for i, opt in enumerate(options)
    ])
    text = (f"🧠 <b>ВИКТОРИНА · {question['category']}</b>\n\n❓ {question['q']}\n\n"
            f"<i>Верно: <b>+{WIN_REWARD}</b> · Ошибка: <b>-{LOSE_PENALTY}</b> · Лимит: <b>{limit_for('quiz')}</b> побед</i>")
    return text, kb, correct_idx


async def _start_quiz(target: types.Message, state: FSMContext, edit: bool) -> None:
    question = get_random_question()
    if question is None:
        await target.answer("⚠️ База вопросов пуста. Сообщи администратору.")
        return
    text, kb, correct_idx = _quiz_round(question)
    await state.set_state(SoloGameStates.waiting_for_quiz)
    await state.update_data(quiz_qid=question["id"], quiz_correct=correct_idx)
    if edit:
        await _safe_edit(target, text, kb)
    else:
        await target.answer(text, reply_markup=kb, parse_mode="HTML")


@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext):
    await _start_quiz(message, state, edit=False)


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
        await _safe_edit(callback.message, "⏳ Этот вопрос уже не активен. Запусти новый!", _retry_kb("quiz", "🧠 Новый вопрос"))
        return

    is_win = chosen == data.get("quiz_correct")
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "quiz")
    if not ok:
        await _safe_edit(callback.message, text, _retry_kb("quiz", "🧠 Новый вопрос"))
        return

    question = get_question_by_id(qid)
    verdict = "✅ <b>Верно!</b>" if is_win else f"❌ <b>Ошибка.</b> Правильный ответ: <code>{question['correct'] if question else '—'}</code>"
    await _safe_edit(callback.message, f"📊 <b>ИТОГ</b>\n\n{verdict}\n\n{text}\n💰 Баланс: <b>{balance} рофлов</b>",
                     _retry_kb("quiz", "🧠 Новый вопрос"))


@router.callback_query(F.data.startswith("quiz_check:"))
async def process_quiz_answer_stale(callback: types.CallbackQuery):
    """Клик по старому вопросу вне состояния — без начислений."""
    await callback.answer("Этот вопрос уже не активен. Запусти новый!", show_alert=True)


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
        await _start_quiz(callback.message, state, edit=True)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")
