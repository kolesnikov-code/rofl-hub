"""
Квесты: интерактивные истории с выборами (сценарии — JSON в data/quests).

Поток: /quests → список → карточка квеста → сцены с кнопками-выборами.
Прогресс в quest_progress (сцена + флаги), переживает рестарты бота.
Награда — только за ПЕРВУЮ победу (ledger reason='quest_reward');
платные подсказки — reason='quest_hint'. Кнопки — по одной в ряд.
"""
from __future__ import annotations

import json
import logging

from aiogram import F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from bots.main_bot.utils.quest_loader import all_quests, get_quest, visible_choices
from shared.database import db
from shared.feature_flags import get_flag
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t

router = Router()
logger = logging.getLogger(__name__)


def _flags_of(row) -> set[str]:
    raw = row["flags"] if row else "[]"
    return set(json.loads(raw) if isinstance(raw, str) else raw)


def _is_finished(quest: dict, scene_key: str) -> bool:
    scene = quest["scenes"].get(scene_key)
    return bool(scene and scene.get("end"))


async def _visible_quests() -> list[dict]:
    """Квесты, включённые владельцем с пульта (тумблеры quest:<id> в админ-боте)."""
    return [q for q in all_quests() if await get_flag(f"quest:{q['id']}")]


def _list_kb(completed: set[str], lang: str, quests: list[dict]) -> types.InlineKeyboardMarkup:
    rows = [[types.InlineKeyboardButton(
        text=f"{'✅ ' if q['id'] in completed else ''}{q['title']} · {q['minutes']} мин",
        callback_data=f"quest_info:{q['id']}")]
        for q in quests]
    rows.append([types.InlineKeyboardButton(text=t(lang, "common.btn_menu"),
                                            callback_data="refresh_main_menu")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _quest_accessible(quest_id: str, user_id: int) -> bool:
    """Скрытый квест доступен лишь тем, кто его уже начал (доигрывание в ротации)."""
    if await get_flag(f"quest:{quest_id}"):
        return True
    async with db.pool.acquire() as conn:
        started = await conn.fetchval(
            "SELECT 1 FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
            user_id, quest_id)
    return bool(started)


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
        rows = await conn.fetch(
            "SELECT quest_id FROM quest_progress WHERE user_id = $1 AND completed_at IS NOT NULL",
            user_id)
    return {r["quest_id"] for r in rows}


@router.message(Command("quests"))
async def cmd_quests(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "quests", user_lang):
        return
    completed = await _completed_ids(message.from_user.id)
    await message.answer(t(user_lang, "quest.list_header"),
                         reply_markup=_list_kb(completed, user_lang, await _visible_quests()),
                         parse_mode="HTML")


@router.callback_query(F.data == "quest_list")
async def quest_list_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "quests", user_lang):
        return
    await callback.answer()
    completed = await _completed_ids(callback.from_user.id)
    await _safe_edit(callback.message, t(user_lang, "quest.list_header"),
                     _list_kb(completed, user_lang, await _visible_quests()))


@router.callback_query(F.data.startswith("quest_info:"))
async def quest_info(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    quest = get_quest(callback.data.split(":", 1)[1])
    if not quest or not await _quest_accessible(quest["id"], callback.from_user.id):
        await callback.answer(t(user_lang, "quest.not_found"), show_alert=True)
        return

    async with db.pool.acquire() as conn:
        prog = await conn.fetchrow(
            "SELECT scene, completed_at FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
            callback.from_user.id, quest["id"])

    in_progress = bool(prog and not _is_finished(quest, prog["scene"]))
    if prog and prog["completed_at"]:
        status = t(user_lang, "quest.card_done")
    elif in_progress:
        status = t(user_lang, "quest.card_progress")
    else:
        status = t(user_lang, "quest.card_new")

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
        await conn.execute(
            """
            INSERT INTO quest_progress (user_id, quest_id, scene, flags, updated_at)
            VALUES ($1, $2, $3, '[]'::jsonb, NOW())
            ON CONFLICT (user_id, quest_id)
            DO UPDATE SET scene = $3, flags = '[]'::jsonb, updated_at = NOW()
            """,
            callback.from_user.id, quest["id"], quest["start"])
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
        prog = await conn.fetchrow(
            "SELECT scene, flags FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
            callback.from_user.id, quest["id"])
    scene_key = prog["scene"] if prog and prog["scene"] in quest["scenes"] else quest["start"]
    flags = _flags_of(prog)
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

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            prog = await conn.fetchrow(
                "SELECT * FROM quest_progress WHERE user_id = $1 AND quest_id = $2 FOR UPDATE",
                user_id, qid)
            if not prog:
                await callback.answer()
                return

            flags = _flags_of(prog)
            # Клик по устаревшей сцене (старое сообщение) — мягко возвращаем в актуальную
            if prog["scene"] != scene_key:
                await callback.answer(t(user_lang, "quest.stale"))
                current = prog["scene"] if prog["scene"] in quest["scenes"] else quest["start"]
                await _safe_edit(callback.message, quest["scenes"][current]["text"],
                                 _scene_kb(quest, current, flags, user_lang))
                return

            scene = quest["scenes"][scene_key]
            choices = scene.get("choices") or []
            if idx >= len(choices):
                await callback.answer()
                return
            choice = choices[idx]
            # Перепроверяем доступность выбора по текущим флагам
            if (idx, choice) not in visible_choices(scene, flags):
                await callback.answer(t(user_lang, "quest.stale"))
                return

            cost = choice.get("cost") or 0
            if cost:
                try:
                    await change_balance(conn, user_id, -cost, "quest_hint", f"{qid}:{scene_key}")
                except InsufficientFunds:
                    await callback.answer(t(user_lang, "quest.no_coins", cost=cost), show_alert=True)
                    return

            new_flags = sorted(flags | set(choice.get("set", [])))
            target_key = choice["goto"]
            target = quest["scenes"][target_key]

            footer = ""
            completed_at = prog["completed_at"]
            if target.get("end") == "win":
                if completed_at is None:
                    await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
                    await change_balance(conn, user_id, quest["reward_coins"], "quest_reward", qid)
                    footer = t(user_lang, "quest.win_first", coins=quest["reward_coins"])
                    await conn.execute(
                        "UPDATE quest_progress SET completed_at = NOW() "
                        "WHERE user_id = $1 AND quest_id = $2", user_id, qid)
                else:
                    footer = t(user_lang, "quest.win_repeat")
            elif target.get("end") == "fail":
                footer = t(user_lang, "quest.fail_footer")

            await conn.execute(
                "UPDATE quest_progress SET scene = $3, flags = $4::jsonb, updated_at = NOW() "
                "WHERE user_id = $1 AND quest_id = $2",
                user_id, qid, target_key, json.dumps(new_flags))

    await callback.answer()
    await _safe_edit(callback.message, target["text"] + footer,
                     _scene_kb(quest, target_key, set(new_flags), user_lang))
