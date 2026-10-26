"""
🕹 Игры в приложении (решение владельца 26.10: «больше Mini App, меньше чат-бота»): КНБ, Больше-Меньше,
Кибер-Сейф и Викторина на тех же движках, что и в чате (execute_solo_game_payout — лимиты, монеты, ресурсы,
уровни интеллекта). Загаданное (число, код, правильный ответ) хранится только на сервере (game_rounds) и
отдаётся игроку уже ПОСЛЕ ответа; таймер викторины считает сервер.

API: GET /api/games · POST /api/games/rps · /api/games/hl/new · /api/games/hl/play · /api/games/safe ·
/api/quiz/next · /api/quiz/hint · /api/quiz/answer · (27.10) /api/math/next|answer · /api/flags/next|answer ·
/api/code/new · /api/code/guess · /api/memory/new · /api/memory/flip.
"""
from __future__ import annotations

import html
import json
import random
from datetime import timedelta

from aiohttp import web

from bots.main_bot.handlers.games import (GAME_TYPES, RPS_BEATS, WIN_COLUMNS, _next_question,
                                          execute_solo_game_payout, hl_outcome, limit_for, rps_outcome,
                                          safe_outcome)
from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail, plain
from shared.database import db
from shared.economy import (CODE_DIGITS, CODE_MAX_ATTEMPTS, FLAGS_ANSWER_SECONDS, GAME_ANSWER_GRACE_SECONDS,
                            GAME_MILESTONES, GAME_RESOURCE, LOSE_PENALTY, MATH_ANSWER_SECONDS, MEMORY_MAX_MOVES,
                            MEMORY_PAIRS, QUIZ_ANSWER_SECONDS, QUIZ_HINT_COST, QUIZ_ROUND_SIZE, RESOURCE_PER_WIN,
                            SAFE_CODES_COUNT, is_active, quiz_answers_required, quiz_level_reward, utcnow,
                            win_reward_for)
from shared.minigames import (bulls_cows, code_secret, flags_round_state, math_round_state, memory_deck, memory_flip,
                              valid_code_guess)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t

HL_BASE_RANGE = (10, 90)     # то же, что в чате: «следующее число от 1 до 100 больше или меньше base?»
HL_SECRET_RANGE = (1, 100)


def _bad() -> web.Response:
    return web.json_response({"ok": False, "message": "bad request"}, status=400)


def hl_new_round(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or random
    base = rng.randint(*HL_BASE_RANGE)
    secret = rng.randint(*HL_SECRET_RANGE)
    return base, secret + 1 if secret == base else secret


def quiz_round_state(question: dict, rng: random.Random | None = None) -> dict:
    """Перемешанные варианты (текст без HTML-экранирования загрузчика) и индекс верного — только на сервере."""
    rng = rng or random
    options = [html.unescape(o) for o in question["options"]]
    rng.shuffle(options)
    return {"key": question["key"], "q": html.unescape(question["q"]),
            "category": html.unescape(str(question["category"])),
            "options": options, "correct": options.index(html.unescape(question["correct"])), "hint": []}


def hint_removal(state: dict, rng: random.Random | None = None) -> list[int]:
    """50/50: два случайных НЕВЕРНЫХ варианта."""
    rng = rng or random
    wrong = [i for i in range(len(state["options"])) if i != state["correct"]]
    return sorted(rng.sample(wrong, 2))


# Игры «вопрос — 4 варианта — таймер»: секунды на ответ по игре
TIMED_SECONDS = {"quiz": QUIZ_ANSWER_SECONDS, "math": MATH_ANSWER_SECONDS, "flags": FLAGS_ANSWER_SECONDS}


def answered_in_time(created_at, now, seconds: int = QUIZ_ANSWER_SECONDS) -> bool:
    return now <= created_at + timedelta(seconds=seconds + GAME_ANSWER_GRACE_SECONDS)


async def _wins_today(conn, user_id: int) -> tuple[dict, bool]:
    """(побед сегодня по играм, безлимит включён)."""
    now = utcnow()
    stats = await conn.fetchrow("SELECT * FROM game_stats WHERE user_id = $1", user_id)
    same_day = bool(stats and stats["last_game_date"] == now.date())
    wins = {g: (stats[WIN_COLUMNS[g]] if same_day else 0) for g in GAME_TYPES}
    unlimit = await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = $1", user_id)
    return wins, is_active(unlimit, now)


async def _limit_reached(ctx, game: str) -> web.Response | None:
    """Лимит побед на сегодня исчерпан — игру не начинаем (иначе проигрыш списал бы монету, а победа не засчиталась)."""
    async with db.pool.acquire() as conn:
        wins, unlimited = await _wins_today(conn, ctx.user_id)
    if unlimited or wins[game] < limit_for(game):
        return None
    return web.json_response({"ok": False, "limit": True, "message": plain(t(
        ctx.lang, "games.limit", game=t(ctx.lang, f"games.name.{game}"), limit=limit_for(game)))})


async def _payout(request, ctx, is_win: bool, game: str, is_draw: bool = False) -> dict:
    info: dict = {}
    ok, text, balance = await execute_solo_game_payout(ctx.user_id, is_win, game, is_draw=is_draw, lang=ctx.lang,
                                                       bot=request.app.get("bot"), info=info)
    out = {"ok": ok, "balance": balance, "info": info}
    if not ok:
        out["message"] = plain(text)
    return out


async def _guard(request, game: str):
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("games", ctx.lang)) is not None:
        return off
    if (limited := await _limit_reached(ctx, game)) is not None:
        return limited
    return ctx


# ============================================================================
# Хаб
# ============================================================================
async def handle_games(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("games", ctx.lang)) is not None:
        return off
    async with db.pool.acquire() as conn:
        wins, unlimited = await _wins_today(conn, ctx.user_id)
        quiz = await conn.fetchrow("SELECT quiz_level, quiz_level_progress FROM game_stats WHERE user_id = $1",
                                   ctx.user_id)
        balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id) or 0
    level, progress = (quiz["quiz_level"], quiz["quiz_level_progress"]) if quiz else (0, 0)
    return web.json_response({
        "games": [{"id": g, "wins": wins[g], "limit": limit_for(g), "reward": win_reward_for(g),
                   "res": GAME_RESOURCE.get(g), "res_qty": RESOURCE_PER_WIN.get(g, 1),
                   "every": list(GAME_MILESTONES[g]) if g in GAME_MILESTONES else None} for g in GAME_TYPES],
        "seconds": TIMED_SECONDS, "code": {"digits": CODE_DIGITS, "max": CODE_MAX_ATTEMPTS},
        "memory": {"pairs": MEMORY_PAIRS, "max": MEMORY_MAX_MOVES},
        "unlimited": unlimited, "penalty": LOSE_PENALTY, "balance": balance,
        "quiz": {"level": level, "progress": progress, "required": quiz_answers_required(level + 1),
                 "next_reward": quiz_level_reward(level + 1), "seconds": QUIZ_ANSWER_SECONDS,
                 "round": QUIZ_ROUND_SIZE, "hint_cost": QUIZ_HINT_COST},
        "safe_codes": SAFE_CODES_COUNT,
    })


# ============================================================================
# КНБ, Сейф, Больше-Меньше
# ============================================================================
async def handle_rps(request: web.Request) -> web.Response:
    ctx = await _guard(request, "rps")
    if isinstance(ctx, web.Response):
        return ctx
    move = (await _json(request)).get("move")
    if move not in RPS_BEATS:
        return _bad()
    bot_move = random.choice(list(RPS_BEATS))
    is_win, is_draw = rps_outcome(move, bot_move)
    out = await _payout(request, ctx, is_win, "rps", is_draw)
    out.update(bot=bot_move, result="draw" if is_draw else ("win" if is_win else "lose"))
    return web.json_response(out)


async def handle_safe(request: web.Request) -> web.Response:
    ctx = await _guard(request, "safe")
    if isinstance(ctx, web.Response):
        return ctx
    guess = _int((await _json(request)).get("guess"))
    if not 1 <= guess <= SAFE_CODES_COUNT:
        return _bad()
    code = random.randint(1, SAFE_CODES_COUNT)     # код загадывается в момент попытки — подсмотреть нечего
    is_win = safe_outcome(guess, code)
    out = await _payout(request, ctx, is_win, "safe")
    out.update(code=code, result="win" if is_win else "lose")
    return web.json_response(out)


async def handle_hl_new(request: web.Request) -> web.Response:
    ctx = await _guard(request, "hl")
    if isinstance(ctx, web.Response):
        return ctx
    base, secret = hl_new_round()
    async with db.pool.acquire() as conn:
        round_id = await conn.fetchval("INSERT INTO game_rounds (user_id, game, state) VALUES ($1, 'hl', $2::jsonb) "
                                       "RETURNING id", ctx.user_id, json.dumps({"base": base, "secret": secret}))
    return web.json_response({"ok": True, "round_id": round_id, "base": base})


async def _close_round(ctx, round_id: int, game: str):
    """Раунд закрывается ровно один раз (повторный ответ — «устарел»). (state, created_at) или None."""
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("UPDATE game_rounds SET done = TRUE WHERE id = $1 AND user_id = $2 AND game = $3 "
                                  "AND NOT done RETURNING state, created_at", round_id, ctx.user_id, game)
    if row is None:
        return None
    state = json.loads(row["state"]) if isinstance(row["state"], str) else row["state"]
    return state, row["created_at"]


async def handle_hl_play(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    direction = data.get("dir")
    if direction not in ("up", "down"):
        return _bad()
    closed = await _close_round(ctx, _int(data.get("round_id")), "hl")
    if closed is None:
        return fail(t(ctx.lang, "quiz.stale"))
    state, _ = closed
    is_win = hl_outcome(direction, state["base"], state["secret"])
    out = await _payout(request, ctx, is_win, "hl")
    out.update(secret=state["secret"], base=state["base"], result="win" if is_win else "lose")
    return web.json_response(out)


# ============================================================================
# Викторина: 30 секунд, подсказка 50/50, раунды по 10 вопросов (счёт раунда — в приложении)
# ============================================================================
async def handle_quiz_next(request: web.Request) -> web.Response:
    ctx = await _guard(request, "quiz")
    if isinstance(ctx, web.Response):
        return ctx
    question = await _next_question(ctx.user_id)
    if question is None:
        return fail(t(ctx.lang, "quiz.empty"))
    state = quiz_round_state(question)
    async with db.pool.acquire() as conn:
        round_id = await conn.fetchval("INSERT INTO game_rounds (user_id, game, state) VALUES ($1, 'quiz', $2::jsonb) "
                                       "RETURNING id", ctx.user_id, json.dumps(state, ensure_ascii=False))
    return web.json_response({"ok": True, "round_id": round_id, "category": state["category"], "q": state["q"],
                              "options": state["options"], "seconds": QUIZ_ANSWER_SECONDS,
                              "hint_cost": QUIZ_HINT_COST})


async def handle_quiz_hint(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    round_id = _int((await _json(request)).get("round_id"))
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("SELECT state FROM game_rounds WHERE id = $1 AND user_id = $2 AND game = 'quiz' "
                                      "AND NOT done FOR UPDATE", round_id, ctx.user_id)
            if row is None:
                return fail(t(ctx.lang, "quiz.stale"))
            state = json.loads(row["state"]) if isinstance(row["state"], str) else row["state"]
            if state.get("hint"):
                return web.json_response({"ok": True, "removed": state["hint"], "balance": None})
            try:
                balance = await change_balance(conn, ctx.user_id, -QUIZ_HINT_COST, "quiz_hint", str(round_id))
            except InsufficientFunds:
                return fail(t(ctx.lang, "games.no_coins"))
            state["hint"] = hint_removal(state)
            await conn.execute("UPDATE game_rounds SET state = $2::jsonb WHERE id = $1",
                               round_id, json.dumps(state, ensure_ascii=False))
    return web.json_response({"ok": True, "removed": state["hint"], "balance": balance})


async def _timed_answer(request: web.Request, game: str) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    option = _int(data.get("option"), -1)          # −1 — время вышло (приложение само шлёт по таймеру)
    closed = await _close_round(ctx, _int(data.get("round_id")), game)
    if closed is None:
        return fail(t(ctx.lang, "quiz.stale"))
    state, created_at = closed
    in_time = answered_in_time(created_at, utcnow(), TIMED_SECONDS[game])
    is_win = in_time and option == state["correct"]
    out = await _payout(request, ctx, is_win, game)
    out.update(correct=state["correct"], correct_text=state["options"][state["correct"]],
               result="win" if is_win else ("timeout" if not in_time or option < 0 else "lose"))
    return web.json_response(out)


async def handle_quiz_answer(request: web.Request) -> web.Response:
    return await _timed_answer(request, "quiz")


async def _new_round(ctx, game: str, state: dict) -> int:
    async with db.pool.acquire() as conn:
        return await conn.fetchval("INSERT INTO game_rounds (user_id, game, state) VALUES ($1, $2, $3::jsonb) RETURNING id",
                                   ctx.user_id, game, json.dumps(state, ensure_ascii=False))


# ============================================================================
# ➗ Математика и 🏳️ Флаги — «вопрос, 4 варианта, таймер», раунды по 10 (как викторина)
# ============================================================================
async def handle_math_next(request: web.Request) -> web.Response:
    ctx = await _guard(request, "math")
    if isinstance(ctx, web.Response):
        return ctx
    state = math_round_state()
    round_id = await _new_round(ctx, "math", state)
    return web.json_response({"ok": True, "round_id": round_id, "q": state["q"], "options": state["options"],
                              "seconds": MATH_ANSWER_SECONDS})


async def handle_flags_next(request: web.Request) -> web.Response:
    ctx = await _guard(request, "flags")
    if isinstance(ctx, web.Response):
        return ctx
    state = flags_round_state(ctx.lang)
    round_id = await _new_round(ctx, "flags", state)
    public = {k: v for k, v in state.items() if k not in ("correct", "iso")}   # верный ответ остаётся на сервере
    if state["mode"] == "capital":
        public.pop("flag", None)                     # по флагу столицу угадать проще — показываем только страну
    return web.json_response({"ok": True, "round_id": round_id, "seconds": FLAGS_ANSWER_SECONDS, **public})


async def handle_math_answer(request: web.Request) -> web.Response:
    return await _timed_answer(request, "math")


async def handle_flags_answer(request: web.Request) -> web.Response:
    return await _timed_answer(request, "flags")


async def _locked_round(conn, ctx, round_id: int, game: str) -> dict | None:
    row = await conn.fetchrow("SELECT state FROM game_rounds WHERE id = $1 AND user_id = $2 AND game = $3 AND NOT done "
                              "FOR UPDATE", round_id, ctx.user_id, game)
    if row is None:
        return None
    return json.loads(row["state"]) if isinstance(row["state"], str) else row["state"]


# ============================================================================
# 💻 Взлом кода: 4 разные цифры, 🐂/🐄 после каждой попытки, не больше CODE_MAX_ATTEMPTS
# ============================================================================
async def handle_code_new(request: web.Request) -> web.Response:
    ctx = await _guard(request, "code")
    if isinstance(ctx, web.Response):
        return ctx
    round_id = await _new_round(ctx, "code", {"secret": code_secret(), "tries": []})
    return web.json_response({"ok": True, "round_id": round_id, "digits": CODE_DIGITS, "max": CODE_MAX_ATTEMPTS})


async def handle_code_guess(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    guess = str(data.get("guess") or "")
    if not valid_code_guess(guess):
        return _bad()
    round_id = _int(data.get("round_id"))
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            state = await _locked_round(conn, ctx, round_id, "code")
            if state is None:
                return fail(t(ctx.lang, "quiz.stale"))
            bulls, cows = bulls_cows(state["secret"], guess)
            state["tries"].append([guess, bulls, cows])
            solved, over = bulls == CODE_DIGITS, len(state["tries"]) >= CODE_MAX_ATTEMPTS
            await conn.execute("UPDATE game_rounds SET state = $2::jsonb, done = $3 WHERE id = $1",
                               round_id, json.dumps(state), solved or over)
    out = {"ok": True, "bulls": bulls, "cows": cows, "left": CODE_MAX_ATTEMPTS - len(state["tries"]), "result": None}
    if solved or over:
        out.update(await _payout(request, ctx, solved, "code"))
        out.update(result="win" if solved else "lose", secret=state["secret"])
    return web.json_response(out)


# ============================================================================
# 🃏 Мемори: 6 пар; найти все за ≤ MEMORY_MAX_MOVES ходов — победа (карточки открывает сервер)
# ============================================================================
async def handle_memory_new(request: web.Request) -> web.Response:
    ctx = await _guard(request, "memory")
    if isinstance(ctx, web.Response):
        return ctx
    round_id = await _new_round(ctx, "memory", {"deck": memory_deck(), "matched": [], "pending": None, "moves": 0})
    return web.json_response({"ok": True, "round_id": round_id, "cards": MEMORY_PAIRS * 2, "max": MEMORY_MAX_MOVES})


async def handle_memory_flip(request: web.Request) -> web.Response:
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    round_id, idx = _int(data.get("round_id")), _int(data.get("idx"), -1)
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            state = await _locked_round(conn, ctx, round_id, "memory")
            if state is None:
                return fail(t(ctx.lang, "quiz.stale"))
            try:
                flip = memory_flip(state, idx)
            except ValueError:
                return _bad()
            lost = not flip["done"] and state["moves"] >= MEMORY_MAX_MOVES and flip["pair"] is not None
            await conn.execute("UPDATE game_rounds SET state = $2::jsonb, done = $3 WHERE id = $1",
                               round_id, json.dumps(state, ensure_ascii=False), flip["done"] or lost)
    out = {"ok": True, **flip, "moves": state["moves"], "max": MEMORY_MAX_MOVES, "result": None}
    if flip["done"] or lost:
        win = flip["done"] and state["moves"] <= MEMORY_MAX_MOVES
        out.update(await _payout(request, ctx, win, "memory"))
        out.update(result="win" if win else "lose", deck=state["deck"])
    return web.json_response(out)


def register_games_routes(app: web.Application) -> None:
    app.router.add_get("/api/games", handle_games)
    app.router.add_post("/api/games/rps", handle_rps)
    app.router.add_post("/api/games/safe", handle_safe)
    app.router.add_post("/api/games/hl/new", handle_hl_new)
    app.router.add_post("/api/games/hl/play", handle_hl_play)
    app.router.add_post("/api/quiz/next", handle_quiz_next)
    app.router.add_post("/api/quiz/hint", handle_quiz_hint)
    app.router.add_post("/api/quiz/answer", handle_quiz_answer)
    app.router.add_post("/api/math/next", handle_math_next)
    app.router.add_post("/api/math/answer", handle_math_answer)
    app.router.add_post("/api/flags/next", handle_flags_next)
    app.router.add_post("/api/flags/answer", handle_flags_answer)
    app.router.add_post("/api/code/new", handle_code_new)
    app.router.add_post("/api/code/guess", handle_code_guess)
    app.router.add_post("/api/memory/new", handle_memory_new)
    app.router.add_post("/api/memory/flip", handle_memory_flip)
