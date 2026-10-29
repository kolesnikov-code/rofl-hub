"""
Квесты: интерактивные истории с выборами (сценарии — JSON в data/quests).

Поток: /quests → список → карточка квеста → сцены с кнопками-выборами. Кнопки — по одной в ряд.
Механика (прогресс, награда за первую победу, платные подсказки) — общая с приложением: shared/quest_engine.py.
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from bots.main_bot.utils.quest_loader import get_quest, visible_choices
from bots.main_bot.webapp_links import app_url
from shared import quest_engine as qe
from shared.database import db
from shared.economy import QUEST_DAILY_NEW, quest_stones
from shared.locales import t

router = Router()
logger = logging.getLogger(__name__)


def _list_kb(completed: set[str], lang: str, quests: list[dict]) -> types.InlineKeyboardMarkup:
    rows = [[types.InlineKeyboardButton(
        text=f"{'✅ ' if q['id'] in completed else ''}{q['title']} · {q['minutes']} мин",
        callback_data=f"quest_info:{q['id']}")]
        for q in quests]
    rows.append([types.InlineKeyboardButton(text=t(lang, "common.btn_menu"),
                                            callback_data="refresh_main_menu")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _quest_accessible(quest_id: str, user_id: int) -> bool:
    async with db.pool.acquire() as conn:
        return await qe.quest_accessible(conn, quest_id, user_id)


def _scene_kb(quest: dict, scene_key: str, flags: set[str], lang: str) -> types.InlineKeyboardMarkup:
    scene = quest["scenes"][scene_key]
    if scene.get("end"):
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=t(lang, "quest.btn_replay"),
                                        callback_data=f"quest_start:{quest['id']}")],
            [types.InlineKeyboardButton(text=t(lang, "quest.btn_list"), callback_data="quest_list")],
        ])
    rows = [[types.InlineKeyboardButton(text=ch["label"],
                                        callback_data=f"qst:{quest['id']}:{scene_key}:{i}")]
            for i, ch in visible_choices(scene, flags)]
    if scene.get("input") and (url := app_url("games")):
        # 🔐 ответ (код, шифр) набирается в приложении — там же идёт таймер сцены
        rows.insert(0, [types.InlineKeyboardButton(text=t(lang, "quest.btn_answer_app"), web_app=types.WebAppInfo(url=url))])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


# ============================================================================
# Список и карточка квеста
# ============================================================================
async def _completed_ids(user_id: int) -> set[str]:
    async with db.pool.acquire() as conn:
        return await qe.completed_ids(conn, user_id)


async def _visible(user_id: int) -> list[dict]:
    async with db.pool.acquire() as conn:
        return await qe.visible_for(conn, user_id)


@router.message(Command("quests"))
async def cmd_quests(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "quests", user_lang):
        return
    completed = await _completed_ids(message.from_user.id)
    await message.answer(t(user_lang, "quest.list_header"),
                         reply_markup=_list_kb(completed, user_lang, await _visible(message.from_user.id)),
                         parse_mode="HTML")


@router.callback_query(F.data == "quest_list")
async def quest_list_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "quests", user_lang):
        return
    await callback.answer()
    completed = await _completed_ids(callback.from_user.id)
    await _safe_edit(callback.message, t(user_lang, "quest.list_header"),
                     _list_kb(completed, user_lang, await _visible(callback.from_user.id)))


@router.callback_query(F.data.startswith("quest_info:"))
async def quest_info(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    quest = get_quest(callback.data.split(":", 1)[1])
    if not quest or not await _quest_accessible(quest["id"], callback.from_user.id):
        await callback.answer(t(user_lang, "quest.not_found"), show_alert=True)
        return

    async with db.pool.acquire() as conn:
        prog = await qe.progress(conn, callback.from_user.id, quest["id"])
    st = qe.status_of(quest, prog)
    in_progress = bool(prog and not qe.is_finished(quest, prog["scene"]))
    status = t(user_lang, {"done": "quest.card_done", "progress": "quest.card_progress", "new": "quest.card_new"}[st])

    rows = []
    if in_progress:
        rows.append([types.InlineKeyboardButton(text=t(user_lang, "quest.btn_resume"),
                                                callback_data=f"quest_resume:{quest['id']}")])
    start_label = t(user_lang, "quest.btn_restart" if prog else "quest.btn_start")
    rows.append([types.InlineKeyboardButton(text=start_label,
                                            callback_data=f"quest_start:{quest['id']}")])
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "quest.btn_list"),
                                            callback_data="quest_list")])

    await _safe_edit(
        callback.message,
        t(user_lang, "quest.card", title=f"<b>{quest['title']}</b>", genre=quest["genre"],
          minutes=quest["minutes"], reward=quest["reward_coins"],
          teaser=quest["teaser"], status=status),
        types.InlineKeyboardMarkup(inline_keyboard=rows))


# ============================================================================
# Старт / продолжение
# ============================================================================
@router.callback_query(F.data.startswith("quest_start:"))
async def quest_start(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    quest = get_quest(callback.data.split(":", 1)[1])
    if not quest or not await _quest_accessible(quest["id"], callback.from_user.id):
        return
    async with db.pool.acquire() as conn:
        await qe.start(conn, callback.from_user.id, quest)
    scene = quest["scenes"][quest["start"]]
    await _safe_edit(callback.message, scene["text"],
                     _scene_kb(quest, quest["start"], set(), user_lang))


@router.callback_query(F.data.startswith("quest_resume:"))
async def quest_resume(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    quest = get_quest(callback.data.split(":", 1)[1])
    if not quest:
        return
    async with db.pool.acquire() as conn:
        prog = await qe.progress(conn, callback.from_user.id, quest["id"])
    scene_key, flags = qe.resume_point(quest, prog)
    await _safe_edit(callback.message, quest["scenes"][scene_key]["text"],
                     _scene_kb(quest, scene_key, flags, user_lang))


# ============================================================================
# Выбор в сцене — сердце движка
# ============================================================================
@router.callback_query(F.data.startswith("qst:"))
async def quest_choice(callback: types.CallbackQuery, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 4 or not parts[3].isdigit():
        await callback.answer()
        return
    qid, scene_key, idx = parts[1], parts[2], int(parts[3])
    quest = get_quest(qid)
    if not quest or scene_key not in quest["scenes"]:
        await callback.answer(t(user_lang, "quest.not_found"), show_alert=True)
        return
    user_id = callback.from_user.id
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                res = await qe.choose(conn, user_id, quest, scene_key, idx)
    except qe.QuestStale as stale:
        # Клик по устаревшей сцене (старое сообщение) — мягко возвращаем в актуальную
        await callback.answer(t(user_lang, "quest.stale"))
        if stale.current != scene_key:
            await _safe_edit(callback.message, quest["scenes"][stale.current]["text"],
                             _scene_kb(quest, stale.current, stale.flags, user_lang))
        return
    except qe.QuestNoCoins as e:
        await callback.answer(t(user_lang, "quest.no_coins", cost=e.cost), show_alert=True)
        return
    except qe.QuestLocked as e:
        await callback.answer(t(user_lang, "quest.epic_locked") if e.reason == "epic"
                              else t(user_lang, "quest.locked", n=QUEST_DAILY_NEW), show_alert=True)
        return
    if res is None:
        await callback.answer()
        return
    footer = {
        "win_first": t(user_lang, "quest.win_first", coins=quest["reward_coins"])
        + t(user_lang, "quest.win_resources", qty=quest_stones(quest["reward_coins"], bool(quest.get("epic")))),
        "win_repeat": t(user_lang, "quest.win_repeat"),
        "fail": t(user_lang, "quest.fail_footer"),
    }.get(res["outcome"], "")
    await callback.answer()
    await _safe_edit(callback.message, quest["scenes"][res["scene"]]["text"] + footer,
                     _scene_kb(quest, res["scene"], res["flags"], user_lang))
