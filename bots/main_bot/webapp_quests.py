"""
🗺 Квесты в приложении (шаг 3 плана 27.10: «чат — дверь и почтальон, игра — в приложении»).
Механика общая с чатом — shared/quest_engine.py; тексты сцен — из data/quests (пока на русском).

API: GET /api/quests · POST /api/quest/open {id, restart} · POST /api/quest/choose {id, scene, i}.
"""
from __future__ import annotations

from aiohttp import web

from bots.main_bot.utils.quest_loader import get_quest, visible_choices
from bots.main_bot.webapp_game import _ctx, _feature_off, _int, _json, fail
from shared import quest_engine as qe
from shared.database import db
from shared.economy import QUEST_DAILY_NEW, QUEST_RESOURCE_BUNDLE
from shared.locales import t


def scene_mood(quest: dict, scene_key: str) -> list[str]:
    """✨ Атмосфера сцены (static/webapp/fx.js): метка сцены, иначе общая метка квеста; до двух эффектов."""
    mood = quest["scenes"][scene_key].get("mood", quest.get("mood"))
    if not mood:
        return []
    return ([mood] if isinstance(mood, str) else list(mood))[:2]


def scene_payload(quest: dict, scene_key: str, flags: set[str]) -> dict:
    """Сцена для приложения: текст (HTML из сценария), видимые выборы с исходными индексами и ценой подсказки."""
    scene = quest["scenes"][scene_key]
    return {"id": quest["id"], "title": quest["title"], "scene": scene_key, "text": scene["text"],
            "end": scene.get("end"), "mood": scene_mood(quest, scene_key),
            "choices": [] if scene.get("end") else
            [{"i": i, "label": ch["label"], "cost": ch.get("cost") or 0} for i, ch in visible_choices(scene, flags)]}


async def _guard(request):
    ctx = await _ctx(request)
    if isinstance(ctx, web.Response):
        return ctx
    if (off := await _feature_off("quests", ctx.lang)) is not None:
        return off
    return ctx


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
         "locked": qe.locked_for(q, progs.get(q["id"]), daily)} for q in quests]})


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
        if qe.locked_for(quest, prog, await qe.daily_state(conn, ctx.user_id)):
            return fail(t(ctx.lang, "quest.locked", n=QUEST_DAILY_NEW))
        if data.get("restart") or prog is None or qe.is_finished(quest, prog["scene"]):
            await qe.start(conn, ctx.user_id, quest)
            scene_key, flags = quest["start"], set()
        else:
            scene_key, flags = qe.resume_point(quest, prog)
    return web.json_response({"ok": True, **scene_payload(quest, scene_key, flags)})


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
    except qe.QuestLocked:
        return fail(t(ctx.lang, "quest.locked", n=QUEST_DAILY_NEW))
    if res is None:
        return fail(t(ctx.lang, "quest.stale"))
    out = {"ok": True, "outcome": res["outcome"], "balance": balance, **scene_payload(quest, res["scene"], res["flags"])}
    if res["outcome"] == "win_first":
        out["reward"] = {"coins": quest["reward_coins"], "res_each": QUEST_RESOURCE_BUNDLE}
    return web.json_response(out)


def register_quest_routes(app: web.Application) -> None:
    app.router.add_get("/api/quests", handle_quests)
    app.router.add_post("/api/quest/open", handle_quest_open)
    app.router.add_post("/api/quest/choose", handle_quest_choose)
