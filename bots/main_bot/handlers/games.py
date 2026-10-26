"""
Соло-игры против бота: КНБ, Больше/Меньше, Викторина, Сейф
(Орёл/Решка и Кубики удалены 22.10 — чистая случайность без решений игрока).

Единый движок execute_solo_game_payout(): лимиты побед по UTC-дате, учёт купленного
безлимита (users.unlimit_until), все движения монет — через ledger.

Викторина: таймер QUIZ_ANSWER_SECONDS (вотчдог-задача; не успел(а) — проигрыш)
и прогрессивные уровни — уровень N закрывается за N×10 верных ответов и даёт N×100 монет.
Вопрос — лаконичный (дизайн владельца), техника и правила — в итоге раунда.
Все тексты — через shared/locales (14 языков).
"""
from __future__ import annotations

import asyncio
import logging
import random

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bots.main_bot.guards import feature_enabled
from bots.main_bot.utils.questions_loader import get_question_by_id, get_random_question, pick_unseen
from shared.analytics import notify_referrer_qualified, qualify_referral_if_due, track
from shared.database import db
from shared.economy import (
    DAILY_WIN_LIMITS,
    DEFAULT_DAILY_WIN_LIMIT,
    INTERN_LEVEL_STEP,
    LOSE_PENALTY,
    QUIZ_ANSWER_SECONDS,
    SAFE_CODES_COUNT,
    SAFE_WIN_REWARD,
    WIN_REWARD,
    is_active,
    permanent_expiry,
    quiz_answers_required,
    quiz_level_reward,
    utcnow,
    win_reward_for,
)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import resolve_lang, t
from shared.economy import ENERGY_WIN_CHANCE_PERCENT
from shared.resources import RESOURCE_ICONS, change_resource, game_resource_gain, resource_capacity

router = Router()
logger = logging.getLogger(__name__)

GAME_TYPES = ("rps", "hl", "quiz", "safe")
GAME_TITLES = {g: f"games.name.{g}" for g in GAME_TYPES}  # ключи локалей
WIN_COLUMNS = {
    "rps": "daily_wins_rps",
    "hl": "daily_wins_hl",
    "quiz": "daily_wins_quiz",
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


def rps_name(lang: str, choice: str) -> str:
    return t(lang, f"rps.{choice}")


def rps_outcome(user_choice: str, bot_choice: str) -> tuple[bool, bool]:
    """(победа, ничья) для КНБ."""
    if user_choice == bot_choice:
        return False, True
    return RPS_BEATS[user_choice] == bot_choice, False


def hl_outcome(direction: str, base: int, secret: int) -> bool:
    return (direction == "up" and secret > base) or (direction == "down" and secret < base)


def safe_outcome(guess: int, code: int) -> bool:
    return guess == code


# ============================================================================
# Единый движок результата раунда
# ============================================================================
async def execute_solo_game_payout(user_id: int, is_win: bool, game_type: str,
                                   is_draw: bool = False, lang: str = "ru",
                                   bot: Bot | None = None) -> tuple[bool, str, int]:
    """
    Возвращает (успех, текст, новый баланс). Успех=False означает: раунд не засчитан
    (лимит, нет монет, нет профиля) — текст объясняет почему.

    Аналитика (events) пишется ПОСЛЕ транзакции — сбой записи события не может
    откатить монеты. Квалификация реферала (новый уровень интеллекта мог сделать друга
    «активным» → +500 рефереру) — ВНУТРИ транзакции: бонус начисляется строго один раз.
    """
    events: list[tuple[str, dict]] = []
    ok, text, balance, qualified_referrer = await _payout_in_tx(
        user_id, is_win, game_type, is_draw, lang, events)
    for name, props in events:
        await track(user_id, name, **props)
    await notify_referrer_qualified(bot, qualified_referrer)
    return ok, text, balance


async def _payout_in_tx(user_id: int, is_win: bool, game_type: str, is_draw: bool, lang: str,
                        events: list[tuple[str, dict]]) -> tuple[bool, str, int, int | None]:
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
                return False, t(lang, "common.no_profile"), 0, None

            stats = await conn.fetchrow(
                "SELECT * FROM game_stats WHERE user_id = $1 FOR UPDATE", user_id)

            same_day = bool(stats and stats["last_game_date"] == today)
            wins_today = stats[column] if same_day else 0
            unlimited = is_active(user["unlimit_until"], now)

            if is_win and not unlimited and wins_today >= max_limit:
                events.append(("daily_limit_hit", {"game": game_type}))
                return False, t(lang, "games.limit",
                                game=t(lang, GAME_TITLES.get(game_type, "games.name.rps")),
                                limit=max_limit), user["balance"], None

            if is_win:
                new_balance = await change_balance(conn, user_id, reward, f"game_win:{game_type}")
                status = t(lang, "games.win", reward=reward)
                # Ресурс игры за победу (волна 22.10): КНБ → металл, Б/М → водород,
                # викторина → кристаллы, сейф → детали
                gain = game_resource_gain(game_type)
                if gain is not None:
                    kind, qty = gain
                    cap = await resource_capacity(conn, user_id)
                    stock = await change_resource(conn, user_id, kind, qty, f"game_win:{game_type}", cap=cap)
                    status += "\n" + t(lang, "games.resource_gain", icon=RESOURCE_ICONS[kind],
                                        qty=qty, name=t(lang, f"res.{kind}"), total=stock)
                    if stock >= cap:
                        status += "\n" + t(lang, "games.resource_full", icon=RESOURCE_ICONS[kind], cap=cap)
                # ⚡ Электричество иногда «выпадает» в любой победе (27.10)
                if random.randrange(100) < ENERGY_WIN_CHANCE_PERCENT:
                    await change_resource(conn, user_id, "energy", 1, f"game_win:{game_type}",
                                          cap=await resource_capacity(conn, user_id))
                    status += "\n" + t(lang, "games.energy_gain")
            else:
                try:
                    new_balance = await change_balance(conn, user_id, -LOSE_PENALTY, f"game_loss:{game_type}")
                except InsufficientFunds:
                    return False, t(lang, "games.no_coins"), user["balance"], None
                status = t(lang, "games.draw" if is_draw else "games.lose", penalty=LOSE_PENALTY)

            # Счётчики: при смене дня все суточные колонки обнуляются
            if same_day:
                games_played = await conn.fetchval(
                    f"""
                    INSERT INTO game_stats (user_id, games_played, games_won, {column}, last_game_date)
                    VALUES ($1, 1, $2, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE SET
                        games_played = game_stats.games_played + 1,
                        games_won = game_stats.games_won + $2,
                        {column} = game_stats.{column} + $2,
                        last_game_date = $3
                    RETURNING games_played
                    """,
                    user_id, 1 if is_win else 0, today)
            else:
                zero_all = ", ".join(f"{c} = 0" for c in _ALL_WIN_COLUMNS if c != column)
                games_played = await conn.fetchval(
                    f"""
                    INSERT INTO game_stats (user_id, games_played, games_won, {column}, last_game_date)
                    VALUES ($1, 1, $2, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE SET
                        games_played = game_stats.games_played + 1,
                        games_won = game_stats.games_won + $2,
                        {zero_all},
                        {column} = $2,
                        last_game_date = $3
                    RETURNING games_played
                    """,
                    user_id, 1 if is_win else 0, today)

            qualified_referrer = None
            events.append(("game_round", {
                "game": game_type,
                "result": "win" if is_win else ("draw" if is_draw else "lose"),
            }))

            # Прогрессивные уровни викторины: уровень N = N*10 верных ответов → N*100 монет
            if is_win and game_type == "quiz":
                row = await conn.fetchrow(
                    "UPDATE game_stats SET quiz_correct_total = quiz_correct_total + 1, "
                    "quiz_level_progress = quiz_level_progress + 1 "
                    "WHERE user_id = $1 RETURNING quiz_level, quiz_level_progress", user_id)
                next_level = row["quiz_level"] + 1
                required = quiz_answers_required(next_level)
                if row["quiz_level_progress"] >= required:
                    bonus = quiz_level_reward(next_level)
                    await conn.execute(
                        "UPDATE game_stats SET quiz_level = $2, quiz_level_progress = 0 "
                        "WHERE user_id = $1", user_id, next_level)
                    new_balance = await change_balance(conn, user_id, bonus,
                                                       "quiz_level_up", str(next_level))
                    status += "\n\n" + t(lang, "games.level_up", level=next_level, bonus=bonus,
                                         next_required=quiz_answers_required(next_level + 1),
                                         next_reward=quiz_level_reward(next_level + 1))
                    if next_level % INTERN_LEVEL_STEP == 0:
                        # Уровень, кратный 10, — ещё один Робот-Стажёр ждёт на ферме:
                        # игрок забирает его кнопкой (видит награду, а не получает молча)
                        await conn.execute(
                            "UPDATE users SET interns_pending = interns_pending + 1 WHERE user_id = $1", user_id)
                        status += "\n" + t(lang, "games.intern_ready")
                    # Новый уровень мог сделать игрока «активным другом» → +500 рефереру (один раз)
                    qualified_referrer = await qualify_referral_if_due(conn, user_id)

            return True, status, new_balance, qualified_referrer


def _retry_kb(lang: str, game_type: str, label: str | None = None) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=label or t(lang, "games.btn_retry"),
                                    callback_data=f"game_retry:{game_type}")],
        [types.InlineKeyboardButton(text=t(lang, "games.btn_hub"), callback_data="games_hub")],
    ])


# ============================================================================
# Игра 1: Камень-Ножницы-Бумага
# ============================================================================
def get_rps_keyboard(lang: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=t(lang, "rps.rock"), callback_data="rps_play:rock"),
        types.InlineKeyboardButton(text=t(lang, "rps.scissors"), callback_data="rps_play:scissors"),
        types.InlineKeyboardButton(text=t(lang, "rps.paper"), callback_data="rps_play:paper"),
    ]])


def rps_intro_text(lang: str) -> str:
    return t(lang, "rps.intro", reward=WIN_REWARD, penalty=LOSE_PENALTY, limit=limit_for("rps"))


@router.message(Command("rps"))
async def cmd_rps_start(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "games", user_lang):
        return
    await message.answer(rps_intro_text(user_lang), reply_markup=get_rps_keyboard(user_lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("rps_play:"))
async def process_rps_choice(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    user_choice = callback.data.split(":", 1)[1]
    if user_choice not in RPS_BEATS:
        return
    bot_choice = random.choice(list(RPS_BEATS))
    is_win, is_draw = rps_outcome(user_choice, bot_choice)

    user_name = rps_name(user_lang, user_choice)
    bot_name = rps_name(user_lang, bot_choice)
    if is_draw:
        headline = t(user_lang, "rps.draw", bot=bot_name)
    elif is_win:
        headline = t(user_lang, "rps.win", user=user_name, bot=bot_name)
    else:
        headline = t(user_lang, "rps.lose", user=user_name, bot=bot_name)

    ok, text, balance = await execute_solo_game_payout(
        callback.from_user.id, is_win, "rps", is_draw=is_draw, lang=user_lang, bot=callback.bot)
    body = text if not ok else (f"{headline}\n\n{text}\n"
                                + t(user_lang, "games.balance", balance=balance))
    await _safe_edit(callback.message, body, _retry_kb(user_lang, "rps"))


# ============================================================================
# Игра 2: Больше / Меньше
# ============================================================================
def _hl_round(lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    base = random.randint(10, 90)
    secret = random.randint(1, 100)
    if secret == base:
        secret += 1
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=t(lang, "hl.btn_up"), callback_data=f"hl_play:up:{base}:{secret}"),
        types.InlineKeyboardButton(text=t(lang, "hl.btn_down"), callback_data=f"hl_play:down:{base}:{secret}"),
    ]])
    text = t(lang, "hl.intro", base=base, reward=WIN_REWARD, penalty=LOSE_PENALTY, limit=limit_for("hl"))
    return text, kb


@router.message(Command("high_low"))
async def cmd_high_low(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "games", user_lang):
        return
    text, kb = _hl_round(user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("hl_play:"))
async def process_high_low_choice(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    parts = callback.data.split(":")
    if len(parts) != 4 or not (parts[2].isdigit() and parts[3].isdigit()):
        return
    direction, base, secret = parts[1], int(parts[2]), int(parts[3])
    is_win = hl_outcome(direction, base, secret)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "hl",
                                                       lang=user_lang, bot=callback.bot)
    body = text if not ok else (t(user_lang, "hl.result", base=base, secret=secret)
                                + f"\n\n{text}\n" + t(user_lang, "games.balance", balance=balance))
    await _safe_edit(callback.message, body, _retry_kb(user_lang, "hl"))


# ============================================================================
# Игра 3: Викторина — таймер QUIZ_ANSWER_SECONDS и прогрессивные уровни
# ============================================================================
# Разделитель блоков в итоге раунда — дизайн владельца (13.10)
QUIZ_DOTS = "." * 40


def _quiz_round(question: dict, lang: str) -> tuple[str, types.InlineKeyboardMarkup, int]:
    """Возвращает текст, клавиатуру и индекс правильного ответа в перемешанном порядке."""
    options = list(question["options"])
    random.shuffle(options)
    correct_idx = options.index(question["correct"])
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=opt, callback_data=f"quiz_check:{question['id']}:{i}")]
        for i, opt in enumerate(options)
    ])
    text = t(lang, "quiz.round",
             category=str(question["category"]).upper(), question=question["q"])
    return text, kb, correct_idx


async def _quiz_result_tail(user_id: int, lang: str, balance: int,
                            lost_line: bool = False) -> str:
    """
    Хвост итога раунда по дизайну владельца: [списание] / баланс / уровень / правила,
    блоки разделены строкой точек. Уровень читается из БД после начисления.
    """
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT quiz_level, quiz_level_progress FROM game_stats WHERE user_id = $1", user_id)
    level = row["quiz_level"] if row else 0
    progress = row["quiz_level_progress"] if row else 0
    next_level = level + 1
    left = max(quiz_answers_required(next_level) - progress, 0)

    money_block = t(lang, "games.balance", balance=balance)
    if lost_line:
        money_block = t(lang, "quiz.lost_line", penalty=LOSE_PENALTY) + "\n" + money_block
    return (
        f"{QUIZ_DOTS}\n{money_block}\n"
        f"{QUIZ_DOTS}\n"
        + t(lang, "quiz.level_line", level=level, next_level=next_level, left=left) + "\n"
        f"{QUIZ_DOTS}\n"
        + t(lang, "quiz.rules", seconds=QUIZ_ANSWER_SECONDS, win=WIN_REWARD,
            penalty=LOSE_PENALTY, limit=limit_for("quiz"))
    )


async def _quiz_timeout_watchdog(message: types.Message, state: FSMContext, token: int,
                                 user_id: int, lang: str, correct_answer: str) -> None:
    """По истечении таймера закрывает неотвеченный вопрос как проигрыш."""
    await asyncio.sleep(QUIZ_ANSWER_SECONDS)
    try:
        if await state.get_state() != SoloGameStates.waiting_for_quiz.state:
            return
        data = await state.get_data()
        if data.get("quiz_token") != token:
            return  # уже другой вопрос
        await state.clear()
        ok, text, balance = await execute_solo_game_payout(user_id, False, "quiz", lang=lang,
                                                           bot=message.bot)
        body = t(lang, "quiz.timeout", correct=correct_answer)
        if ok:
            body += "\n" + await _quiz_result_tail(user_id, lang, balance, lost_line=True)
        else:
            body += f"\n\n{text}"
        await _safe_edit(message, body, _retry_kb(lang, "quiz", t(lang, "quiz.btn_new")))
    except Exception:
        logger.exception("[QUIZ_TIMER] сбой вотчдога user=%s", user_id)


async def _next_question(user_id: int) -> dict | None:
    """Сначала вопросы, которых игрок ещё не видел; прошёл всю базу — новый круг. Сбой БД — просто случайный."""
    try:
        async with db.pool.acquire() as conn:
            seen = {r["qkey"] for r in await conn.fetch("SELECT qkey FROM quiz_seen WHERE user_id = $1", user_id)}
            question, lap_done = pick_unseen(seen)
            if question is None:
                return None
            if lap_done:
                await conn.execute("DELETE FROM quiz_seen WHERE user_id = $1", user_id)
            await conn.execute("INSERT INTO quiz_seen (user_id, qkey) VALUES ($1, $2) ON CONFLICT DO NOTHING",
                               user_id, question["key"])
            return question
    except Exception:
        logger.exception("[QUIZ] не удалось учесть просмотренные вопросы user=%s", user_id)
        return get_random_question()


async def _start_quiz(target: types.Message, state: FSMContext, user_id: int, edit: bool,
                      lang: str = "ru") -> None:
    question = await _next_question(user_id)
    if question is None:
        await target.answer(t(lang, "quiz.empty"))
        return

    text, kb, correct_idx = _quiz_round(question, lang)
    token = random.getrandbits(62)
    await state.set_state(SoloGameStates.waiting_for_quiz)
    await state.update_data(quiz_qid=question["id"], quiz_correct=correct_idx, quiz_token=token)
    if edit:
        sent = await _safe_edit(target, text, kb)
    else:
        sent = await target.answer(text, reply_markup=kb, parse_mode="HTML")
    asyncio.create_task(_quiz_timeout_watchdog(sent or target, state, token, user_id, lang,
                                               question["correct"]))


@router.message(Command("quiz"))
async def cmd_quiz_start(message: types.Message, state: FSMContext, user_lang: str = "ru"):
    if not await feature_enabled(message, "games", user_lang):
        return
    await _start_quiz(message, state, message.from_user.id, edit=False, lang=user_lang)


@router.callback_query(SoloGameStates.waiting_for_quiz, F.data.startswith("quiz_check:"))
async def process_quiz_answer(callback: types.CallbackQuery, state: FSMContext, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    qid, chosen = int(parts[1]), int(parts[2])

    data = await state.get_data()
    await state.clear()
    await callback.answer()

    if data.get("quiz_qid") != qid:
        await _safe_edit(callback.message, t(user_lang, "quiz.stale"),
                         _retry_kb(user_lang, "quiz", t(user_lang, "quiz.btn_new")))
        return

    is_win = chosen == data.get("quiz_correct")
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "quiz",
                                                       lang=user_lang, bot=callback.bot)
    if not ok:
        await _safe_edit(callback.message, text, _retry_kb(user_lang, "quiz", t(user_lang, "quiz.btn_new")))
        return

    question = get_question_by_id(qid)
    if is_win:
        # text = games.win (+ games.level_up при повышении уровня)
        head = text
    else:
        head = t(user_lang, "quiz.wrong", correct=question["correct"] if question else "—")
    tail = await _quiz_result_tail(callback.from_user.id, user_lang, balance,
                                   lost_line=not is_win)
    kb = _retry_kb(user_lang, "quiz", t(user_lang, "quiz.btn_new"))
    pending = await _interns_pending(callback.from_user.id) if is_win else 0
    if pending:
        kb.inline_keyboard.insert(0, [types.InlineKeyboardButton(
            text=t(user_lang, "farm.btn_claim_intern", n=pending), callback_data="farm_action:claim_intern")])
    await _safe_edit(callback.message, f"{head}\n{tail}", kb)


async def _interns_pending(user_id: int) -> int:
    try:
        async with db.pool.acquire() as conn:
            return await conn.fetchval("SELECT interns_pending FROM users WHERE user_id = $1", user_id) or 0
    except Exception:
        return 0


@router.callback_query(F.data.startswith("quiz_check:"))
async def process_quiz_answer_stale(callback: types.CallbackQuery, user_lang: str = "ru"):
    """Клик по старому вопросу вне состояния — без начислений."""
    await callback.answer(t(user_lang, "quiz.stale_alert"), show_alert=True)


# ============================================================================
# Игра 6: Сейф — подбери код из 4 вариантов, куш больше
# ============================================================================
def _safe_round(lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    code = random.randint(1, SAFE_CODES_COUNT)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=f"🔢 {i}", callback_data=f"safe_play:{i}:{code}")
        for i in range(1, SAFE_CODES_COUNT + 1)
    ]])
    text = t(lang, "safe.intro", jackpot=SAFE_WIN_REWARD, codes=SAFE_CODES_COUNT,
             penalty=LOSE_PENALTY, limit=limit_for("safe"))
    return text, kb


@router.message(Command("safe"))
async def cmd_safe_start(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "games", user_lang):
        return
    text, kb = _safe_round(user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("safe_play:"))
async def process_safe_guess(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        return
    guess, code = int(parts[1]), int(parts[2])
    is_win = safe_outcome(guess, code)
    ok, text, balance = await execute_solo_game_payout(callback.from_user.id, is_win, "safe",
                                                       lang=user_lang, bot=callback.bot)
    headline = t(user_lang, "safe.win", code=code) if is_win else \
        t(user_lang, "safe.lose", guess=guess, code=code)
    body = text if not ok else (f"{headline}\n\n{text}\n"
                                + t(user_lang, "games.balance", balance=balance))
    await _safe_edit(callback.message, body, _retry_kb(user_lang, "safe", t(user_lang, "safe.btn_retry")))


# ============================================================================
# Реванш
# ============================================================================
@router.callback_query(F.data.startswith("game_retry:"))
async def process_game_retry_inline(callback: types.CallbackQuery, state: FSMContext,
                                    user_lang: str = "ru"):
    if not await feature_enabled(callback, "games", user_lang):
        return
    await callback.answer()
    game_type = callback.data.split(":", 1)[1]
    if game_type == "rps":
        await _safe_edit(callback.message, rps_intro_text(user_lang), get_rps_keyboard(user_lang))
    elif game_type == "hl":
        text, kb = _hl_round(user_lang)
        await _safe_edit(callback.message, text, kb)
    elif game_type == "quiz":
        await _start_quiz(callback.message, state, callback.from_user.id, edit=True, lang=user_lang)
    elif game_type == "safe":
        text, kb = _safe_round(user_lang)
        await _safe_edit(callback.message, text, kb)


async def _safe_edit(message: types.Message, text: str,
                     kb: types.InlineKeyboardMarkup) -> types.Message | None:
    try:
        result = await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        return result if isinstance(result, types.Message) else message
    except Exception:
        return await message.answer(text, reply_markup=kb, parse_mode="HTML")
