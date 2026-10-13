import asyncio
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Намертво привязываем чтение .env к корню проекта для безопасности холдинга
# Принудительно и правильно находим корень всего проекта ROFL-HUB
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

# 🔥 МУЛЬТИ-АККАУНТНЫЙ ПЕРЕХВАТ ИЗ ENV (Парсим список через запятую БЕЗ СИНТАКСИЧЕСКИХ ДЫР)
ADMIN_IDS = []
raw_admin_ids = os.getenv("ADMIN_ID", "")
if raw_admin_ids:
    try:
        ADMIN_IDS = [int(uid.strip()) for uid in raw_admin_ids.split(",") if uid.strip().isdigit()]
    except Exception:
        ADMIN_IDS = []

try:
    USERS_CHANNEL_ID = int(os.getenv("USERS_CHANNEL_ID", "0"))
    ADMIN_SECRET_CHANNEL_ID = int(os.getenv("ADMIN_SECRET_CHANNEL_ID", "0"))
except (ValueError, TypeError):
    USERS_CHANNEL_ID = 0
    ADMIN_SECRET_CHANNEL_ID = 0

if not ADMIN_BOT_TOKEN:
    raise RuntimeError("🚨 КРИТИЧЕСКИЙ КРАШ: Переменная ADMIN_BOT_TOKEN отсутствует в .env!")
if not ADMIN_IDS or USERS_CHANNEL_ID == 0 or ADMIN_SECRET_CHANNEL_ID == 0:
    raise RuntimeError("🚨 ОШИБКА БЕЗОПАСНОСТИ: Ключи лимитов или список ADMIN_IDS не заданы в .env!")

from shared.database import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())

# Юзернейм главного бота для моментальной генерации диплинков
MAIN_BOT_USERNAME = os.getenv("MAIN_BOT_USERNAME", "RoflHubGame_Bot").lstrip("@")

MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")


async def notify_user_via_main_bot(user_id: int, text: str) -> bool:
    """Отправляет игроку сообщение от имени главного бота. Ошибки не роняют админ-бот."""
    if not MAIN_BOT_TOKEN:
        logger.warning("[NOTIFY] MAIN_BOT_TOKEN не задан — уведомление игроку %s не отправлено", user_id)
        return False
    main_bot = Bot(token=MAIN_BOT_TOKEN)
    try:
        await main_bot.send_message(user_id, text, parse_mode="HTML")
        return True
    except Exception as e:
        logger.warning("[NOTIFY] не удалось уведомить игрока %s: %s", user_id, e)
        return False
    finally:
        await main_bot.session.close()


class AuctionCreationStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_desc = State()
    waiting_for_price = State()
    waiting_for_step = State()


class BattleCreationStates(StatesGroup):
    waiting_title = State()
    waiting_starts = State()
    waiting_ends = State()
    waiting_nom_manual = State()
    waiting_prize_manual = State()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@dp.message(Command("start"))
async def cmd_admin_start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ заблокирован. Этот бот — закрытый пульт управления.")
        return
    await message.answer(
        "🛠️ <b>ШТАБ-КВАРТИРА МОДЕРАЦИИ ROFL HUB</b>\n..................................................\n\n"
        "🟢 <b>ДОСТУПНЫЕ КОМАНДЫ ПУЛЬТА:</b>\n"
        "• /new_auction — Запустить лот и вывесить автоматический анонс в канал юзеров\n"
        "• /close_auction [ID] — Принудительно закрыть торги\n"
        "• /report — Суточный отчёт: DAU, продажи, когорты за 30 дней\n"
        "• /gift [ID] [сумма] — Подарить монеты игроку (отрицательная сумма — штраф)\n"
        "• /block [ID] — Заблокировать игрока · /unblock [ID] — Разблокировать\n"
        "• /find [ID или @username] — Досье игрока\n"
        "• /refund [номер_платежа] — Вернуть Stars игроку по чеку\n"
        "• /backup — Снимок всех таблиц базы JSON-файлом прямо в этот чат\n"
        "• /new_battle — Запустить БИТВУ команд и кланов (событие!) · /battles — список\n"
        "• /finish_battle [ID] — Принудительно подвести итоги битвы\n"
        "• /assign_vip [ID] [АЛИАС] — Выдать VIP ID победителю аукциона · /revoke_vip [АЛИАС]\n",
        parse_mode="HTML"
    )


# ============================================================================
# 💎 VIP ID: выдача победителям аукционов (равноправный айдишник для переводов)
# ============================================================================
@dp.message(Command("assign_vip"))
async def admin_assign_vip(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit():
        await message.answer("⚠️ Пример: <code>/assign_vip 123456789 ROFL-HUB-777</code>",
                             parse_mode="HTML")
        return
    user_id, alias = int(parts[1]), parts[2].strip().upper()[:32]
    if alias.isdigit() or alias.startswith("@"):
        await message.answer("❌ Алиас не может быть числом или начинаться с @ — "
                             "иначе он столкнётся с обычными ID и юзернеймами.")
        return

    async with db.pool.acquire() as conn:
        exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", user_id)
        if not exists:
            await message.answer("❌ Игрок с таким ID не найден.")
            return
        taken = await conn.fetchval("SELECT user_id FROM vip_aliases WHERE alias = $1", alias)
        if taken:
            await message.answer(f"❌ Алиас уже занят игроком <code>{taken}</code>. "
                                 f"Сначала /revoke_vip {alias}", parse_mode="HTML")
            return
        await conn.execute("INSERT INTO vip_aliases (alias, user_id) VALUES ($1, $2)", alias, user_id)

    await notify_user_via_main_bot(
        user_id,
        f"💎 <b>Тебе присвоен VIP ID: {alias}!</b>\n"
        f"Теперь это твой равноправный айдишник в экосистеме: другие игроки могут переводить "
        f"тебе монеты командой <code>/transfer {alias} сумма</code>, а сам VIP ID красуется в твоём /profile.")
    await message.answer(f"💎 VIP ID <b>{alias}</b> присвоен игроку <code>{user_id}</code>.",
                         parse_mode="HTML")


@dp.message(Command("revoke_vip"))
async def admin_revoke_vip(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("⚠️ Пример: <code>/revoke_vip ROFL-HUB-777</code>", parse_mode="HTML")
        return
    alias = parts[1].strip().upper()
    async with db.pool.acquire() as conn:
        result = await conn.execute("DELETE FROM vip_aliases WHERE alias = $1", alias)
    if result.endswith("1"):
        await message.answer(f"🗑 VIP ID <b>{alias}</b> отозван.", parse_mode="HTML")
    else:
        await message.answer("❌ Такого VIP ID нет.")


# ============================================================================
# 🛡️ МОДЕРАЦИЯ И ЭКОНОМИКА (Блок 4): блокировки, подарки, отчёт по запросу
# ============================================================================
from shared.db_admin import (  # noqa: E402
    admin_gift_coins,
    backup_to_json_bytes,
    collect_daily_report,
    dump_database,
    find_payment,
    format_daily_report,
    mark_refunded,
    set_user_blocked,
)
from shared.ledger import UserNotFound  # noqa: E402


@dp.message(Command("report"))
async def admin_daily_report(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    async with db.pool.acquire() as conn:
        report = await collect_daily_report(conn)
    await message.answer(format_daily_report(report), parse_mode="HTML")


def _parse_id_arg(text: str) -> int | None:
    parts = text.split()
    return int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else None


@dp.message(Command("block"))
async def admin_block_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    user_id = _parse_id_arg(message.text)
    if user_id is None:
        await message.answer("⚠️ Пример: <code>/block 123456789</code>", parse_mode="HTML")
        return
    async with db.pool.acquire() as conn:
        found = await set_user_blocked(conn, user_id, True)
    if not found:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    await notify_user_via_main_bot(user_id, "🚫 <b>Твой аккаунт заблокирован администрацией ROFL HUB.</b>")
    await message.answer(f"🚫 Игрок <code>{user_id}</code> заблокирован: бот перестал отвечать на его действия.",
                         parse_mode="HTML")


@dp.message(Command("unblock"))
async def admin_unblock_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    user_id = _parse_id_arg(message.text)
    if user_id is None:
        await message.answer("⚠️ Пример: <code>/unblock 123456789</code>", parse_mode="HTML")
        return
    async with db.pool.acquire() as conn:
        found = await set_user_blocked(conn, user_id, False)
    if not found:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    await notify_user_via_main_bot(user_id, "✅ <b>Твой аккаунт разблокирован. С возвращением в ROFL HUB!</b>")
    await message.answer(f"✅ Игрок <code>{user_id}</code> разблокирован.", parse_mode="HTML")


@dp.message(Command("gift"))
async def admin_gift(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].lstrip("-").isdigit() or int(parts[2]) == 0:
        await message.answer("⚠️ Пример: <code>/gift 123456789 5000</code> (отрицательная сумма — штраф)",
                             parse_mode="HTML")
        return
    user_id, amount = int(parts[1]), int(parts[2])

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
                new_balance = await admin_gift_coins(conn, user_id, amount, message.from_user.id)
    except UserNotFound:
        await message.answer("❌ Игрок с таким ID не найден в базе.")
        return
    except Exception as e:
        await message.answer(f"❌ Операция отклонена: {e}")
        return

    if amount > 0:
        await notify_user_via_main_bot(
            user_id, f"🎁 <b>Администрация ROFL HUB подарила тебе {amount} монет!</b> Проверь /profile")
    await message.answer(
        f"💰 Готово! Игроку <code>{user_id}</code> {'начислено' if amount > 0 else 'списано'} "
        f"<b>{abs(amount)} монет</b>. Новый баланс: <b>{new_balance}</b>.", parse_mode="HTML")


# ============================================================================
# ⚔️ БИТВЫ КОМАНД И КЛАНОВ: событийный конструктор владельца
# ============================================================================
import json as _json  # noqa: E402

from bots.main_bot.catalog import CATALOG, get_item  # noqa: E402
from shared.battles import (  # noqa: E402
    BATTLE_NOMINATIONS,
    MAX_PRIZE_PLACES,
    award_sku_to_team,
    battle_team_scores,
    build_announce_post,
    build_results_post,
    parse_battle_moment,
    prizes_from_row,
    prizes_to_json,
)


def _prize_mode_kb(place: int) -> types.InlineKeyboardMarkup:
    rows = [[
        types.InlineKeyboardButton(text="📋 Товар из магазина", callback_data="battle_przmode:sku"),
        types.InlineKeyboardButton(text="✍️ Указать вручную", callback_data="battle_przmode:manual"),
    ]]
    if place > 1:
        rows.append([types.InlineKeyboardButton(text="⏹ Призов больше нет — завершить",
                                                callback_data="battle_przmode:stop")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def _sku_list_kb() -> types.InlineKeyboardMarkup:
    # По одной кнопке в ряд — цены не обрезаются на телефоне
    rows = [[types.InlineKeyboardButton(text=item["button"], callback_data=f"battle_sku:{sku}")]
            for sku, item in CATALOG.items()]
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _ask_prize_for_place(message: types.Message, state: FSMContext, place: int) -> None:
    await state.update_data(b_place=place)
    label = "🥇 ПРИЗ ЗА 1 МЕСТО (получит КАЖДЫЙ боец команды-победителя)" if place == 1 \
        else f"🎁 Приз за {place} место (каждому бойцу команды)"
    await message.answer(f"<b>{label}</b>\n\nКак определим приз?",
                         reply_markup=_prize_mode_kb(place), parse_mode="HTML")


@dp.message(Command("new_battle"))
async def admin_new_battle(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(BattleCreationStates.waiting_title)
    await message.answer(
        "⚔️ <b>СОЗДАНИЕ БИТВЫ КОМАНД И КЛАНОВ</b>\n\n"
        "ШАГ 1. Введи НАЗВАНИЕ битвы (до 100 символов), например:\n"
        "<i>Осенний Кубок Ферм · Неделя Интеллекта · ROFL Champions League</i>",
        parse_mode="HTML")


@dp.message(BattleCreationStates.waiting_title)
async def battle_title(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    title = (message.text or "").strip()[:100]
    if not title:
        await message.answer("❌ Название пустое. Введи ещё раз:")
        return
    await state.update_data(b_title=title)
    await state.set_state(BattleCreationStates.waiting_starts)
    await message.answer(
        "ШАГ 2. МОМЕНТ СТАРТА зачёта (UTC):\n"
        "• <code>0</code> — начать прямо сейчас\n"
        "• число — через столько ЧАСОВ от текущего момента\n"
        "• или дата: <code>ДД.ММ.ГГГГ ЧЧ:ММ</code>",
        parse_mode="HTML")


@dp.message(BattleCreationStates.waiting_starts)
async def battle_starts(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    starts = parse_battle_moment(message.text or "", base=datetime.now(timezone.utc))
    if starts is None:
        await message.answer("❌ Не понял момент. Формат: <code>0</code>, часы или "
                             "<code>ДД.ММ.ГГГГ ЧЧ:ММ</code>", parse_mode="HTML")
        return
    await state.update_data(b_starts=starts.isoformat())
    await state.set_state(BattleCreationStates.waiting_ends)
    await message.answer(
        f"Старт: <b>{starts:%d.%m.%Y %H:%M} UTC</b>\n\n"
        "ШАГ 3. ОКОНЧАНИЕ битвы (счётчики остановятся и итоги подведутся автоматически):\n"
        "• число — длительность в ЧАСАХ от старта (например <code>168</code> = неделя)\n"
        "• или дата: <code>ДД.ММ.ГГГГ ЧЧ:ММ</code> (UTC)",
        parse_mode="HTML")


@dp.message(BattleCreationStates.waiting_ends)
async def battle_ends(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    data = await state.get_data()
    starts = datetime.fromisoformat(data["b_starts"])
    ends = parse_battle_moment(message.text or "", base=starts)
    if ends is None or ends <= starts:
        await message.answer("❌ Финиш должен быть ПОЗЖЕ старта. Часы от старта или дата:")
        return
    await state.update_data(b_ends=ends.isoformat())
    await state.set_state(None)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="📋 Выбрать из списка", callback_data="battle_nommode:list"),
        types.InlineKeyboardButton(text="✍️ Указать вручную", callback_data="battle_nommode:manual"),
    ]])
    await message.answer(
        f"Финиш: <b>{ends:%d.%m.%Y %H:%M} UTC</b>\n\n"
        "ШАГ 4. НОМИНАЦИЯ битвы — что меряем?",
        reply_markup=kb, parse_mode="HTML")


@dp.callback_query(F.data.startswith("battle_nommode:"))
async def battle_nom_mode(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    mode = callback.data.split(":")[1]
    if mode == "manual":
        await state.set_state(BattleCreationStates.waiting_nom_manual)
        await callback.message.answer(
            "✍️ Введи текст номинации (итоги по ней ты подведёшь вручную, "
            "бот их автоматически НЕ считает):")
        return
    rows = [[types.InlineKeyboardButton(text=nom["title"], callback_data=f"battle_nom:{key}")]
            for key, nom in BATTLE_NOMINATIONS.items()]
    await callback.message.answer("📋 Выбери номинацию:",
                                  reply_markup=types.InlineKeyboardMarkup(inline_keyboard=rows))


@dp.message(BattleCreationStates.waiting_nom_manual)
async def battle_nom_manual(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    text = (message.text or "").strip()[:200]
    if not text:
        await message.answer("❌ Пустая номинация. Введи ещё раз:")
        return
    await state.update_data(b_nom_key="manual", b_nom_text=text, b_prizes={})
    await state.set_state(None)
    await _ask_prize_for_place(message, state, 1)


@dp.callback_query(F.data.startswith("battle_nom:"))
async def battle_nom_pick(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    key = callback.data.split(":", 1)[1]
    if key not in BATTLE_NOMINATIONS:
        return
    await state.update_data(b_nom_key=key, b_nom_text=BATTLE_NOMINATIONS[key]["title"], b_prizes={})
    await callback.message.answer(f"Номинация: <b>{BATTLE_NOMINATIONS[key]['title']}</b>",
                                  parse_mode="HTML")
    await _ask_prize_for_place(callback.message, state, 1)


@dp.callback_query(F.data.startswith("battle_przmode:"))
async def battle_prize_mode(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    mode = callback.data.split(":")[1]
    data = await state.get_data()
    place = data.get("b_place", 1)
    if mode == "stop":
        await _battle_confirm(callback.message, state)
        return
    if mode == "manual":
        await state.set_state(BattleCreationStates.waiting_prize_manual)
        await callback.message.answer(
            f"✍️ Опиши приз за {place} место (вручишь его сам, бот только опубликует описание):")
        return
    await callback.message.answer(f"📋 Выбери товар-приз за {place} место "
                                  f"(получит каждый боец команды):",
                                  reply_markup=_sku_list_kb())


@dp.message(BattleCreationStates.waiting_prize_manual)
async def battle_prize_manual(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    text = (message.text or "").strip()[:200]
    if not text:
        await message.answer("❌ Пустое описание. Введи ещё раз:")
        return
    await state.set_state(None)
    await _save_prize_and_next(message, state, {"mode": "manual", "value": text})


@dp.callback_query(F.data.startswith("battle_sku:"))
async def battle_prize_sku(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    sku = callback.data.split(":", 1)[1]
    if sku not in CATALOG:
        return
    await _save_prize_and_next(callback.message, state, {"mode": "sku", "value": sku})


async def _save_prize_and_next(message: types.Message, state: FSMContext, prize: dict) -> None:
    data = await state.get_data()
    place = data.get("b_place", 1)
    prizes = dict(data.get("b_prizes") or {})
    prizes[place] = prize
    await state.update_data(b_prizes=prizes)
    label = CATALOG[prize["value"]]["title"] if prize["mode"] == "sku" else prize["value"]
    await message.answer(f"✅ Приз за {place} место: <b>{label}</b>", parse_mode="HTML")
    if place >= MAX_PRIZE_PLACES:
        await _battle_confirm(message, state)
        return
    await _ask_prize_for_place(message, state, place + 1)


async def _battle_confirm(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    starts = datetime.fromisoformat(data["b_starts"])
    ends = datetime.fromisoformat(data["b_ends"])
    prizes = {int(k): v for k, v in (data.get("b_prizes") or {}).items()}
    prize_lines = []
    for place in sorted(prizes):
        p = prizes[place]
        label = CATALOG[p["value"]]["title"] if p["mode"] == "sku" else p["value"]
        prize_lines.append(f"{place} место: {label}")
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="🚀 ЗАПУСТИТЬ БИТВУ И АНОНСИРОВАТЬ", callback_data="battle_go:launch"),
        types.InlineKeyboardButton(text="❌ Отмена", callback_data="battle_go:cancel"),
    ]])
    await message.answer(
        "⚔️ <b>ПРОВЕРЬ БИТВУ ПЕРЕД ЗАПУСКОМ:</b>\n\n"
        f"📌 Название: <b>{data['b_title']}</b>\n"
        f"🏅 Номинация: {data['b_nom_text']}"
        + (" <i>(итоги вручную)</i>" if data["b_nom_key"] == "manual" else "") + "\n"
        f"🕐 Старт: <b>{starts:%d.%m.%Y %H:%M} UTC</b>\n"
        f"🏁 Финиш: <b>{ends:%d.%m.%Y %H:%M} UTC</b>\n\n"
        "🎁 <b>Призы:</b>\n" + ("\n".join(prize_lines) or "— не заданы —"),
        reply_markup=kb, parse_mode="HTML")


@dp.callback_query(F.data.startswith("battle_go:"))
async def battle_launch(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if not is_admin(callback.from_user.id):
        return
    await callback.answer()
    action = callback.data.split(":")[1]
    data = await state.get_data()
    await state.clear()
    if action == "cancel" or not data.get("b_title"):
        await callback.message.answer("❌ Создание битвы отменено.")
        return

    prizes = {int(k): v for k, v in (data.get("b_prizes") or {}).items()}
    async with db.pool.acquire() as conn:
        battle_id = await conn.fetchval(
            """
            INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, prizes)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb) RETURNING battle_id
            """,
            data["b_title"], data["b_nom_key"], data["b_nom_text"],
            datetime.fromisoformat(data["b_starts"]), datetime.fromisoformat(data["b_ends"]),
            prizes_to_json(prizes))
        battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", battle_id)

    try:
        await bot.send_message(USERS_CHANNEL_ID, build_announce_post(battle), parse_mode="HTML")
        channel_note = "🟢 Анонс опубликован в канале игроков."
    except Exception as e:
        logger.error("[BATTLE_ANNOUNCE] не удалось опубликовать анонс: %s", e)
        channel_note = f"❌ Анонс в канал не ушёл: {e}"

    await callback.message.answer(
        f"⚔️ <b>БИТВА №{battle_id} ЗАПУЩЕНА!</b>\n{channel_note}\n\n"
        f"Итоги подведутся автоматически в {battle['ends_at']:%d.%m.%Y %H:%M} UTC.\n"
        f"Принудительно: <code>/finish_battle {battle_id}</code> · Список: /battles",
        parse_mode="HTML")


@dp.message(Command("battles"))
async def admin_battles_list(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM battles ORDER BY battle_id DESC LIMIT 10")
    if not rows:
        await message.answer("Битв ещё не было. Создай первую: /new_battle")
        return
    lines = ["⚔️ <b>ПОСЛЕДНИЕ БИТВЫ:</b>\n"]
    for b in rows:
        status = {"active": "🟢 активна", "finished": "🏁 завершена"}.get(b["status"], b["status"])
        lines.append(f"№{b['battle_id']} «{b['title']}» — {status}\n"
                     f"   {b['starts_at']:%d.%m %H:%M} → {b['ends_at']:%d.%m %H:%M} UTC · {b['nomination_text']}")
    await message.answer("\n".join(lines), parse_mode="HTML")


@dp.message(Command("finish_battle"))
async def admin_finish_battle(message: types.Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("⚠️ Пример: <code>/finish_battle 1</code>", parse_mode="HTML")
        return
    async with db.pool.acquire() as conn:
        battle = await conn.fetchrow(
            "SELECT * FROM battles WHERE battle_id = $1 AND status = 'active'", int(parts[1]))
    if not battle:
        await message.answer("❌ Активная битва с таким номером не найдена.")
        return
    await _finish_battle(bot, battle)
    await message.answer(f"🏁 Битва №{battle['battle_id']} закрыта, итоги опубликованы.")


async def _finish_battle(bot: Bot, battle) -> None:
    """Подводит итоги: считает топ, раздаёт авто-призы, публикует пост в канал."""
    battle_id = battle["battle_id"]
    async with db.pool.acquire() as conn:
        await conn.execute("UPDATE battles SET status = 'finished' WHERE battle_id = $1", battle_id)

        if battle["nomination_key"] == "manual":
            await bot.send_message(
                ADMIN_SECRET_CHANNEL_ID,
                f"🖐 <b>Битва №{battle_id} «{battle['title']}» завершена.</b>\n"
                f"Номинация ручная («{battle['nomination_text']}») — подведи итоги и "
                f"опубликуй пост в канал сам.", parse_mode="HTML")
            return

        scores = await battle_team_scores(
            conn, battle["nomination_key"], battle["starts_at"], battle["ends_at"])
        prizes = prizes_from_row(battle["prizes"])

        prize_notes: dict[int, str] = {}
        for place, prize in sorted(prizes.items()):
            if place > len(scores):
                continue
            team = scores[place - 1]
            if prize["mode"] == "sku":
                # Призы не считаются продажами: нулевая цена в star_payments
                order = {**get_item(prize["value"]), "stars": 0}
                delivered, skipped = await award_sku_to_team(
                    conn, team["team_id"], prize["value"], order, battle_id, place)
                note = f"каждому бойцу — {order['title']} (выдано: {delivered}"
                note += f", пропущено: {skipped})" if skipped else ")"
                prize_notes[place] = note
            else:
                prize_notes[place] = prize["value"]

        await conn.execute(
            "UPDATE battles SET results = $2::jsonb WHERE battle_id = $1",
            battle_id, _json.dumps({"scores": scores, "prize_notes":
                                    {str(k): v for k, v in prize_notes.items()}}, ensure_ascii=False))

    post = build_results_post(battle, scores, prize_notes)
    try:
        await bot.send_message(USERS_CHANNEL_ID, post, parse_mode="HTML")
    except Exception as e:
        logger.error("[BATTLE_RESULTS] пост в канал не ушёл: %s", e)
    try:
        await bot.send_message(ADMIN_SECRET_CHANNEL_ID,
                               f"🏁 Битва №{battle_id} закрыта автоматически.\n\n{post}",
                               parse_mode="HTML")
    except Exception:
        pass


async def check_finished_battles(bot: Bot) -> None:
    """Вызывается демоном: закрывает битвы, чьё время вышло."""
    async with db.pool.acquire() as conn:
        due = await conn.fetch(
            "SELECT * FROM battles WHERE status = 'active' AND ends_at <= NOW()")
    for battle in due:
        try:
            await _finish_battle(bot, battle)
        except Exception:
            logger.exception("[BATTLE_FINISH] сбой закрытия битвы %s", battle["battle_id"])


@dp.message(Command("backup"))
async def admin_backup(message: types.Message):
    """Снимок всех таблиц базы JSON-файлом в чат админа (Блок 5: бэкап в один клик)."""
    if not is_admin(message.from_user.id):
        return
    await message.answer("⏳ Собираю снимок базы...")
    async with db.pool.acquire() as conn:
        dump = await dump_database(conn)
    payload = backup_to_json_bytes(dump)
    rows_total = sum(len(v) for v in dump["tables"].values())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    document = types.BufferedInputFile(payload, filename=f"rofl_hub_backup_{stamp}.json")
    await message.answer_document(
        document,
        caption=(f"💾 <b>Бэкап базы готов.</b>\n"
                 f"Таблиц: {len(dump['tables'])} · Строк: {rows_total} · "
                 f"Размер: {len(payload) // 1024} КБ\n"
                 f"<i>Храни файл в надёжном месте — это полный снимок экономики.</i>"),
        parse_mode="HTML")


@dp.message(Command("refund"))
async def admin_refund(message: types.Message):
    """Возврат Stars по номеру платежа. Делается ГЛАВНЫМ ботом (он принимал оплату)."""
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("⚠️ Пример: <code>/refund tg_charge_id_из_чека</code>", parse_mode="HTML")
        return
    charge_id = parts[1].strip()

    async with db.pool.acquire() as conn:
        payment = await find_payment(conn, charge_id)
    if not payment:
        await message.answer("❌ Платёж с таким номером не найден в базе.")
        return
    if payment["refunded_at"]:
        await message.answer(f"⚠️ Этот платёж уже был возвращён {payment['refunded_at']:%d.%m.%Y %H:%M} UTC.")
        return
    if charge_id.startswith("TEST_"):
        await message.answer("🧪 Это платёж тест-режима — настоящих Stars за ним нет, возвращать нечего.")
        return

    if not MAIN_BOT_TOKEN:
        await message.answer("❌ MAIN_BOT_TOKEN не задан — возврат невозможен.")
        return
    main_bot = Bot(token=MAIN_BOT_TOKEN)
    try:
        refunded = await main_bot.refund_star_payment(
            user_id=payment["user_id"], telegram_payment_charge_id=charge_id)
    except Exception as e:
        await message.answer(f"❌ Telegram отклонил возврат: {e}")
        return
    finally:
        await main_bot.session.close()

    if not refunded:
        await message.answer("❌ Telegram не подтвердил возврат. Попробуй позже.")
        return

    async with db.pool.acquire() as conn:
        await mark_refunded(conn, charge_id)
    await notify_user_via_main_bot(
        payment["user_id"],
        f"💫 <b>Тебе возвращены {payment['stars_amount']} ★</b> по платежу <code>{charge_id}</code>. "
        f"Stars уже на твоём счету Telegram.")
    await message.answer(
        f"✅ Возврат выполнен: <b>★ {payment['stars_amount']}</b> игроку <code>{payment['user_id']}</code> "
        f"(товар: {payment['item_payload']}).\n"
        f"<i>Если товар нужно отобрать — используй /gift с отрицательной суммой или правь вручную.</i>",
        parse_mode="HTML")


@dp.message(Command("find"))
async def admin_find_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("⚠️ Пример: <code>/find 123456789</code> или <code>/find @username</code>",
                             parse_mode="HTML")
        return
    arg = parts[1]

    async with db.pool.acquire() as conn:
        if arg.startswith("@"):
            user = await conn.fetchrow("SELECT * FROM users WHERE LOWER(username) = LOWER($1)", arg[1:])
        elif arg.isdigit():
            user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", int(arg))
        else:
            user = None
        if not user:
            await message.answer("❌ Игрок не найден.")
            return
        stars = await conn.fetchval(
            "SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments WHERE user_id = $1", user["user_id"])
        quiz = await conn.fetchrow(
            "SELECT quiz_level, quiz_correct_total FROM game_stats WHERE user_id = $1", user["user_id"])

    await message.answer(
        f"🕵️ <b>ДОСЬЕ ИГРОКА</b>\n"
        f"🆔 <code>{user['user_id']}</code> · @{user['username'] or '—'} · {user['display_name'] or '—'}\n"
        f"💰 Баланс: <b>{user['balance']}</b> · 🧠 Уровень: {quiz['quiz_level'] if quiz else 0}\n"
        f"💵 Потрачено Stars: <b>★ {stars}</b>\n"
        f"🏆 Команда: {user['team_id'] or 'нет'} · 🌐 Язык: {user['lang']}\n"
        f"📅 Регистрация: {user['created_at']:%d.%m.%Y} · Был в сети: {user['last_seen_at']:%d.%m.%Y %H:%M}\n"
        f"🚫 Блокировка: <b>{'ДА' if user['is_blocked'] else 'нет'}</b>",
        parse_mode="HTML")

@dp.message(Command("new_auction"))
async def admin_new_auction(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.set_state(AuctionCreationStates.waiting_for_title)
    await message.answer("🎁 <b>ШАГ 1 ИЗ 4: НАЗВАНИЕ ЛОТА</b>\n\nВведи название: <i>VIP ID или пост в Instagram</i>):", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_title)
async def process_auc_title(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.update_data(auc_title=message.text.strip())
    await state.set_state(AuctionCreationStates.waiting_for_desc)
    await message.answer("📝 <b>ШАГ 2 ИЗ 4: ОПИСАНИЕ ЛОТА</b>\n\nНапиши условия аукциона для выжигания монет:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_desc)
async def process_auc_desc(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    await state.update_data(auc_desc=message.text.strip())
    await state.set_state(AuctionCreationStates.waiting_for_price)
    await message.answer("💰 <b>ШАГ 3 ИЗ 4: СТАРТОВАЯ ЦЕНА</b>\n\nУкажи начальную цену в монетах:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_price)
async def process_auc_price(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    if not message.text.strip().isdigit():
        await message.answer("❌ Цена должна быть числом! Введи заново:")
        return
    await state.update_data(auc_price=int(message.text.strip()))
    await state.set_state(AuctionCreationStates.waiting_for_step)
    await message.answer("🚀 <b>ШАГ 4 ИЗ 4: МИНИМАЛЬНЫЙ ШАГ</b>\n\nВведи минимальный шаг повышения цены:", parse_mode="HTML")

@dp.message(AuctionCreationStates.waiting_for_step)
async def process_auc_finalize(message: types.Message, state: FSMContext, bot: Bot):
    if not is_admin(message.from_user.id): return
    if not message.text.strip().isdigit():
        await message.answer("❌ Шаг должен быть числом! Введи заново:")
        return

    step = int(message.text.strip())
    data = await state.get_data()
    await state.clear()

    async with db.pool.acquire() as conn:
        auction_id = await conn.fetchval(
            """
            INSERT INTO auctions (item_title, item_desc, current_price, min_step, status)
            VALUES ($1, $2, $3, $4, 'open') RETURNING auction_id
            """,
            data.get("auc_title"), data.get("auc_desc"), data.get("auc_price"), step
        )

    # 🔥 БЕЗУПРЕЧНЫЙ ФИКС СЛЭШЕЙ: Ссылка собирается строго с разделителем /
    deep_link = f"https://t.me/{MAIN_BOT_USERNAME}?start=auction_{auction_id}"

    channel_post_text = (
        f"🔥 <b>БИТВА ВОЖАКОВ ЗА ВЕЧНЫЙ ПОНТ И VIP-ПРИЗЫ!</b>\n"
        f"..................................................\n\n"
        f"Объявляются официальные торги холдинга экосистемы!\n\n"
        f"🎁 Лот раунда: <b>{data.get('auc_title')}</b>\n"
        f"📝 Детали: <i>{data.get('auc_desc')}</i>\n\n"
        f"💰 Стартовая цена: <b>{data.get('auc_price')} монет</b>\n"
        f"🚀 Шаг повышения: <b>+{step} монет</b>\n\n"
        f"..................................................\n"
        f"⚠️ <i>Ставки возвратные: если тебя перебили, монеты вернутся на баланс. Платит только победитель!</i>\n\n"
        f"👇 <b>КЛИКАЙ ПО ССЫЛКЕ НИЖЕ ДЛЯ ВХОДА И СТАВКИ:</b>\n"
        f"{deep_link}"
    )

    try:
        await bot.send_message(chat_id=USERS_CHANNEL_ID, text=channel_post_text, parse_mode="HTML")
        channel_status = "🟢 <b>Анонс лота успешно опубликован в USERS_CHANNEL_ID!</b>"
    except Exception as e:
        logger.error(f"[CHANNEL_POST_ERROR] Не удалось отправить пост в канал юзеров: {e}")
        channel_status = f"❌ <b>Ошибка публикации в USERS_CHANNEL_ID:</b> {e}"

    success_text = (
        f"👑 <b>ЛОТ АУКЦИОНА УСПЕШНО СФОРМИРОВАН!</b>\n"
        f"..................................................\n\n"
        f"🆔 ID Лота в базе Railway: <code>{auction_id}</code>\n"
        f"🎁 Название: <b>{data.get('auc_title')}</b>\n"
        f"💰 Стартовая цена: <b>{data.get('auc_price')} монет</b>\n\n"
        f"..................................................\n\n"
        f"{channel_status}\n\n"
        f"🔗 Ссылка: <code>{deep_link}</code>"
    )
    await message.answer(success_text, parse_mode="HTML")

@dp.message(Command("close_auction"))
async def admin_close_auction(message: types.Message, bot: Bot):
    if not is_admin(message.from_user.id): return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("⚠️ Пример: <code>/close_auction 1</code>", parse_mode="HTML")
        return
    if not parts[1].isdigit():
        await message.answer("❌ ID лота должен быть числом.")
        return
    auction_id = int(parts[1])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
            if not auction or auction["status"] != "open":
                await message.answer("❌ Лот не существует или уже закрыт.")
                return
            await conn.execute("UPDATE auctions SET status = 'closed' WHERE auction_id = $1", auction_id)

    winner_id = auction["highest_bidder_id"]
    if winner_id:
        # Игрок общается с ГЛАВНЫМ ботом: админ-бот не может писать ему первым (chat not found)
        await notify_user_via_main_bot(
                winner_id,
                f"🏆 <b>Ты победил(а) в аукционе за лот «{auction['item_title']}»!</b>\n"
                f"Финальная цена: <b>{auction['current_price']} монет</b>. Администрация свяжется с тобой для выдачи приза.",
        )
        try:
            await bot.send_message(
                USERS_CHANNEL_ID,
                f"🏁 <b>Аукцион за лот «{auction['item_title']}» завершён!</b>\n"
                f"👑 Победитель: ID <code>{winner_id}</code> · 💰 {auction['current_price']} монет",
                parse_mode="HTML")
        except Exception as e:
            logger.warning("[AUCTION_CLOSE] не удалось опубликовать итог в канал: %s", e)

    await message.answer(
        f"🏁 <b>АУКЦИОН №{auction_id} ЗАКРЫТ ИЗ ШТАБА!</b>\n\n"
        f"🎁 Лот: <b>{auction['item_title']}</b>\n"
        f"👑 Победитель: ID <code>{auction['highest_bidder_id'] if auction['highest_bidder_id'] else 'Ставок нет'}</code>\n"
        f"💵 Финальная цена: <b>{auction['current_price']} монет</b>.",
        parse_mode="HTML"
    )


# ============================================================================
# 📊 2. АВТОНОМНЫЙ ДЕМОН СКВОЗНОЙ АНАЛИТИКИ ПО ЧАСАМ UTC (00, 06, 12, 18)
# ============================================================================
async def dynamic_analytics_daemon(bot: Bot):
    """
    Фоновый демон сбора метрик холдинга ROFL HUB CORE.
    Срабатывает строго в 06:00, 12:00, 18:00 UTC (экспресс-срез)
    и в 00:00 UTC (глубокий суточный когортный анализ).
    """
    logger.info("⏳ Астрономический аналитический демон успешно запущен по UTC!")

    # Флаг-предохранитель, чтобы бот не отправлял отчет каждую секунду внутри одной минуты
    last_triggered_hour = -1

    while True:
        try:
            await asyncio.sleep(20)

            # Авто-закрытие битв, чьё время вышло (итоги + призы + пост в канал)
            try:
                await check_finished_battles(bot)
            except Exception:
                logger.exception("[BATTLE_DAEMON] сбой проверки битв")

            now_utc = datetime.now(timezone.utc)
            current_hour = now_utc.hour
            current_minute = now_utc.minute
            current_date = now_utc.date()

            # Проверяем, наступила ли целевая минута (00 минут) нужного часа
            if current_hour in [0, 6, 12, 18] and current_minute == 0:
                # Если в этот час триггер уже срабатывал — пропускаем тик
                if current_hour == last_triggered_hour:
                    continue

                last_triggered_hour = current_hour
                logger.info(f"📊 Наступила контрольная точка времени: {current_hour}:00 UTC. Сбор данных...")

                async with db.pool.acquire() as conn:
                    # Сбор базовых агрегатных метрик со всей базы Railway
                    total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
                    total_clans = await conn.fetchval("SELECT COUNT(*) FROM teams")
                    total_stars_revenue = await conn.fetchval("SELECT SUM(stars_amount) FROM star_payments")
                    total_coins_mass = await conn.fetchval("SELECT SUM(balance) FROM users")

                    total_played = await conn.fetchval("SELECT SUM(games_played) FROM game_stats")
                    total_won = await conn.fetchval("SELECT SUM(games_won) FROM game_stats")
                    total_wins_rps = await conn.fetchval("SELECT SUM(daily_wins_rps) FROM game_stats")
                    total_wins_hl = await conn.fetchval("SELECT SUM(daily_wins_hl) FROM game_stats")
                    total_wins_quiz = await conn.fetchval("SELECT SUM(daily_wins_quiz) FROM game_stats")

                stars_total = total_stars_revenue if total_stars_revenue else 0
                coins_total = total_coins_mass if total_coins_mass else 0
                games_played_all = total_played if total_played else 0
                games_won_all = total_won if total_won else 0

                # ====================================================================
                # 📢 ВЫДАЧА ЭКСПРЕСС-ОТЧЕТОВ (В 06:00, 12:00, 18:00 UTC)
                # ====================================================================
                if current_hour in (0, 6, 12, 18) and current_minute == 0:
                    express_text = (
                        f"⏱️ <b>ЭКСПРЕСС-АНАЛИТИКА ЭКОСИСТЕМЫ ({current_hour}:00 UTC)</b>\n"
                        f"..................................................\n\n"
                        f"👥 Всего игроков в СУБД: <b>{total_users} чел.</b>\n"
                        f"🏆 Активных Кланов/Команд: <b>{total_clans} банд</b>\n\n"
                        f"🎮 Проведено раундов: <b>{games_played_all} игр</b>\n"
                        f"👑 Одержано побед юзерами: <code>{games_won_all} раз</code>\n\n"
                        f"💵 Валовый кэш Stars: <b>★ {stars_total} XTR</b>\n"
                        f"🪙 Масса фантиков в СУБД: <code>{coins_total} монет</code>\n"
                        f"..................................................\n"
                        f"<i>⚙️ Следующий системный срез произойдет строго по графику UTC.</i>"
                    )
                    await bot.send_message(chat_id=ADMIN_SECRET_CHANNEL_ID, text=express_text, parse_mode="HTML")
                    logger.info(f"🟢 Экспресс-отчет {current_hour}:00 UTC отправлен в Тайную Комнату.")

                # ====================================================================
                # 👑 ПОЛНОЧНЫЙ ИТОГОВЫЙ СРЕЗ И КОГОРТНЫЙ АНАЛИЗ (СТРОГО В 00:00 UTC)
                # ====================================================================
                if current_hour == 0:
                    async with db.pool.acquire() as conn:
                        cohort_data = await conn.fetchrow("""
                                                          WITH user_spend
                                                                   AS (SELECT user_id, COALESCE(SUM(stars_amount), 0) as total_spend
                                                                       FROM star_payments
                                                                       GROUP BY user_id)
                                                          SELECT COUNT(CASE WHEN total_spend = 0 THEN 1 END)                          as f2p_count,
                                                                 COUNT(CASE WHEN total_spend > 0 AND total_spend <= 100 THEN 1 END)   as light_count,
                                                                 COUNT(CASE WHEN total_spend > 100 AND total_spend <= 500 THEN 1 END) as normal_count,
                                                                 COUNT(CASE WHEN total_spend > 500 THEN 1 END)                        as whale_count
                                                          FROM user_spend;
                                                          """)

                    f2p = cohort_data["f2p_count"] if cohort_data else 0
                    light = cohort_data["light_count"] if cohort_data else 0
                    normal = cohort_data["normal_count"] if cohort_data else 0
                    whale = cohort_data["whale_count"] if cohort_data else 0
                    non_paying_total = max(0, total_users - (light + normal + whale))

                    daily_text = (
                        f"👑 <b>ИТОГОВЫЙ СУТОЧНЫЙ ОТЧЕТ ХОЛДИНГА (00:00 UTC)</b>\n"
                        f"..................................................\n\n"
                        f"📊 <b>КОГОРТНЫЙ АНАЛИЗ ПСИХОЛОГИИ И ТРАТ (LTV):</b>\n"
                        f"🛑 <b>F2P Халявщики (0 ★):</b> <code>{non_paying_total} чел.</code>\n"
                        f"🪵 <b>Микро-донатеры (до 100 ★):</b> <b>{light} чел.</b>\n"
                        f"⚡ <b>Нормы (100-500 ★):</b> <b>{normal} чел.</b>\n"
                        f"👑 <b>КИТЫ ЭКОСИСТЕМЫ (500+ ★):</b> <u>{whale} чел.</u>\n\n"
                        f"🎯 <b>АКТИВНОСТЬ ПО ТИПАМ ИГР ЗА ВСЕ ВРЕМЯ:</b>\n"
                        f"• Раундов в КНБ: <code>{total_wins_rps if total_wins_rps else 0} раундов</code>\n"
                        f"• Раундов в Больше/Меньше: <code>{total_wins_hl if total_wins_hl else 0} раундов</code>\n"
                        f"• Пройдено тестов Викторины: <code>{total_wins_quiz if total_wins_quiz else 0} вопросов</code>\n\n"
                        f"..................................................\n"
                        f"<i>📈 Суточный срез зафиксирован под елочкой в канале навсегда. Данные СУБД синхронизированы.</i>"
                    )
                    await bot.send_message(chat_id=ADMIN_SECRET_CHANNEL_ID, text=daily_text, parse_mode="HTML")
                    logger.info("👑 Суточный глубокий когортный отчет успешно опубликован в 00:00 UTC!")

            # Сброс триггера блокировки часов, когда целевая минута прошла
            if current_minute != 0:
                last_triggered_hour = -1

        except Exception as e:
            logger.error(f"[ANALYTICS_DAEMON_CRASH] Критический сбой демона: {e}")


# ============================================================================
# 🏎️ ИНИЦИАЛИЗАЦИЯ И СТАРТ СЕКРЕТНОГО АДМИН-БОТА
# ============================================================================
async def main():
    bot = Bot(token=ADMIN_BOT_TOKEN)
    await db.connect()
    await db.create_tables()

    # Запускаем аналитического демона в асинхронном фоне Event Loop!
    asyncio.create_task(dynamic_analytics_daemon(bot))

    logger.info("🟢 СЕКРЕТНЫЙ АДМИН-БОТ С АНАЛИТИЧЕСКИМ ШЛЮЗОМ ЗАПУЩЕН!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
