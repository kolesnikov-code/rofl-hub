"""
🗺 Квесты в приложении (шаг 3 плана 27.10: «чат — дверь и почтальон, игра — в приложении»).
Механика общая с чатом — shared/quest_engine.py; тексты сцен — из data/quests (пока на русском).

API: GET /api/quests · POST /api/quest/open {id, restart} · POST /api/quest/choose {id, scene, i} ·
POST /api/quest/answer {id, scene, text} (ввод ответа) · POST /api/quest/timeout {id, scene} (время сцены вышло).
"""
from __future__ import annotations

from aiohttp import web

from bots.main_bot.utils.quest_loader import annoyed_line, get_quest, visible_choices
from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared import quest_engine as qe
from shared.database import db
from shared.economy import QUEST_DAILY_NEW, quest_stones
from shared.locales import t


def scene_mood(quest: dict, scene_key: str) -> list[str]:
    """✨ Атмосфера сцены (static/webapp/fx.js): метка сцены, иначе общая метка квеста; до двух эффектов."""
    mood = quest["scenes"][scene_key].get("mood", quest.get("mood"))
    if not mood:
        return []
    return ([mood] if isinstance(mood, str) else list(mood))[:2]


def scene_payload(quest: dict, scene_key: str, flags: set[str], state=None) -> dict:
    """
    Сцена для приложения: текст (HTML из сценария), видимые выборы с исходными индексами и ценой подсказки;
    state — строка прогресса или итог хода (scene_at, tries, visits): таймер, попытки ввода, «раздражение» персонажа.
    """
    scene = quest["scenes"][scene_key]
    state = state or {}
    annoyed = annoyed_line(quest, scene_key, qe.visits_of(state.get("visits")))
    text = ('<i>' + annoyed + '</i>\n\n' + scene["text"]) if annoyed else scene["text"]
    extra = {}
    if (inp := scene.get("input")) and not scene.get("end"):
        extra["input"] = {"hint": inp.get("hint") or "", "tries_left": qe.tries_left(scene, state or None) if state else inp.get("tries", 3),
                          "tries": inp.get("tries", 3)}
    if (timer := scene.get("timer")) and not scene.get("end"):
        left = qe.timer_left(scene, state) if state.get("scene_at") is not None else timer["seconds"]
        extra["timer"] = {"seconds": timer["seconds"], "left": left}
    return {**extra, "id": quest["id"], "title": quest["title"], "scene": scene_key, "text": text,
            "end": scene.get("end"), "mood": scene_mood(quest, scene_key), "fx_text": scene.get("fx_text") or "",
            "fx_draw": scene.get("fx_draw") or "", "fx_lock": scene.get("fx_lock") or "",
            "choices": [] if scene.get("end") else
            [{"i": i, "label": ch["label"], "cost": ch.get("cost") or 0} for i, ch in visible_choices(scene, flags)]}


async def _guard(request):
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("quests", ctx.lang)) is not None:
        return off
    return ctx


def _locked_text(lang: str, reason: str) -> str:
    return t(lang, "quest.epic_locked") if reason == "epic" else t(lang, "quest.locked", n=QUEST_DAILY_NEW)


async def handle_quests(request: web.Request) -> web.Response:
    ctx = await _guard(request)
    if isinstance(ctx, web.Response):
        return ctx
    quests = await qe.visible_quests()
    async with db.pool.acquire() as conn:
        progs = {r["quest_id"]: r for r in await conn.fetch(
            "SELECT quest_id, scene, flags, completed_at FROM quest_progress WHERE user_id = $1", ctx.user_id)}
        daily = await qe.daily_state(conn, ctx.user_id)
    return web.json_response({"ok": True, "ru_only": ctx.lang != "ru", "total": qe.total_count(), "daily": daily,
                              "quests": [
        {"id": q["id"], "title": q["title"], "genre": q["genre"], "minutes": q["minutes"], "reward": q["reward_coins"],
         "teaser": q["teaser"], "status": qe.status_of(q, progs.get(q["id"])), "epic": qe.is_epic(q),
         "notes": bool(q.get("notes") or qe.is_epic(q)),
         "notes": bool(q.get("notes") or qe.is_epic(q)),
         "locked": qe.lock_reason(q, progs.get(q["id"]), daily)} for q in quests]})


async def handle_quest_open(request: web.Request) -> web.Response:
    """Продолжить с места остановки или (restart / нет прогресса / концовка) — начать заново."""
    ctx = await _guard(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    quest = get_quest(str(data.get("id") or ""))
    async with db.pool.acquire() as conn:
        if not quest or not await qe.quest_accessible(conn, quest["id"], ctx.user_id):
            return fail(t(ctx.lang, "quest.not_found"))
        prog = await qe.progress(conn, ctx.user_id, quest["id"])
        if (reason := qe.lock_reason(quest, prog, await qe.daily_state(conn, ctx.user_id))) is not None:
            return fail(_locked_text(ctx.lang, reason))
        if data.get("restart") or prog is None or qe.is_finished(quest, prog["scene"]):
            await qe.start(conn, ctx.user_id, quest)
            prog = await qe.progress(conn, ctx.user_id, quest["id"])
        scene_key, flags = qe.resume_point(quest, prog)
        if quest["scenes"][scene_key].get("timer") and qe.timer_left(quest["scenes"][scene_key], prog) == 0:
            async with conn.transaction():       # вернулся(лась), а время сцены давно вышло — сразу её исход
                res = await qe.timeout(conn, ctx.user_id, quest, scene_key)
            if res is not None:
                return web.json_response({"ok": True, **_result(quest, res, None)})
    return web.json_response({"ok": True, **scene_payload(quest, scene_key, flags, prog)})


async def handle_quest_choose(request: web.Request) -> web.Response:
    ctx = await _ctx(request)        # начатый квест доигрывается и при выключенном тумблере (как в чате)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    quest = get_quest(str(data.get("id") or ""))
    scene_key = str(data.get("scene") or "")
    if not quest or scene_key not in quest["scenes"]:
        return fail(t(ctx.lang, "quest.not_found"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await qe.choose(conn, ctx.user_id, quest, scene_key, _int(data.get("i"), -1))
            balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
    except qe.QuestStale as stale:   # вторая вкладка / старый экран — показываем актуальную сцену
        return web.json_response({"ok": True, "stale": True, **scene_payload(quest, stale.current, stale.flags)})
    except qe.QuestNoCoins as e:
        return fail(t(ctx.lang, "quest.no_coins", cost=e.cost))
    except qe.QuestLocked as e:
        return fail(_locked_text(ctx.lang, e.reason))
    if res is None:
        return fail(t(ctx.lang, "quest.stale"))
    return web.json_response({"ok": True, **_result(quest, res, balance)})


def _result(quest: dict, res: dict, balance) -> dict:
    out = {"outcome": res["outcome"], "balance": balance, "wrong": bool(res.get("wrong")), "timeout": bool(res.get("timeout")),
           **scene_payload(quest, res["scene"], res["flags"], res)}
    if res["outcome"] == "win_first":
        out["reward"] = {"coins": quest["reward_coins"], "res_each": quest_stones(quest["reward_coins"], qe.is_epic(quest))}
    return out


async def _step(request: web.Request, action) -> web.Response:
    """Общий каркас хода в сцене (ответ, таймер): та же логика ошибок, что у выбора."""
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    data = await _json(request)
    quest = get_quest(str(data.get("id") or ""))
    scene_key = str(data.get("scene") or "")
    if not quest or scene_key not in quest["scenes"]:
        return fail(t(ctx.lang, "quest.not_found"))
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await action(conn, ctx.user_id, quest, scene_key, data)
            balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", ctx.user_id)
            if res is None:            # рано (таймер ещё идёт) или в сцене нет ввода — показываем её как есть
                prog = await qe.progress(conn, ctx.user_id, quest["id"])
                return web.json_response({"ok": True, "outcome": None, "wait": True,
                                          **scene_payload(quest, scene_key, qe.flags_of(prog), prog)})
    except qe.QuestStale as stale:
        return web.json_response({"ok": True, "stale": True, **scene_payload(quest, stale.current, stale.flags)})
    except qe.QuestLocked as e:
        return fail(_locked_text(ctx.lang, e.reason))
    return web.json_response({"ok": True, **_result(quest, res, balance)})


async def handle_quest_answer(request: web.Request) -> web.Response:
    """🔐 Ответ на ребус/шифр/код: сверка на сервере, неверные попытки сгорают."""
    return await _step(request, lambda conn, uid, q, key, data: qe.answer(conn, uid, q, key, str(data.get("text") or "")[:64]))


async def handle_quest_timeout(request: web.Request) -> web.Response:
    """⏱ Приложение сообщает «время вышло» — сервер сам проверяет, что оно действительно вышло."""
    return await _step(request, lambda conn, uid, q, key, data: qe.timeout(conn, uid, q, key))


def register_quest_routes(app: web.Application) -> None:
    app.router.add_get("/api/quests", handle_quests)
    app.router.add_post("/api/quest/open", handle_quest_open)
    app.router.add_post("/api/quest/choose", handle_quest_choose)
    app.router.add_post("/api/quest/answer", handle_quest_answer)
    app.router.add_post("/api/quest/timeout", handle_quest_timeout)
