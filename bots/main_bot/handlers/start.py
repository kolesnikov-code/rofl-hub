"""
/start: выбор языка → регистрация → онбординг 4 шага → reply-панель.
Deep-link: /start <referrer_id> или /start auction_<id>.
Плюс контур возвратного аукциона (ставки/обновление).
"""
from __future__ import annotations

import html
import logging

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bots.main_bot.handlers.menu import get_reply_main_keyboard
from shared.auction_logic import compute_bid
from shared.database import db
from shared.economy import REFERRAL_SIGNUP_BONUS, START_BALANCE, START_CUTLETS_INVENTORY
from shared.ledger import change_balance

router = Router()
logger = logging.getLogger(__name__)

LANGUAGES = [
    ("ru", "🇷🇺 Русский"), ("en", "🇺🇸 English"), ("zh", "🇨🇳 中文"), ("hi", "🇮🇳 हिन्दी"),
    ("es", "🇪🇸 Español"), ("ar", "🇦🇪 العربية"), ("fr", "🇫🇷 Français"), ("bn", "🇧🇩 বাংলা"),
    ("pt", "🇧🇷 Português"), ("id", "🇮🇩 Indonesia"), ("de", "🇩🇪 Deutsch"), ("it", "🇮🇹 Italiano"),
    ("pl", "🇵🇱 Polski"),
]
LANGUAGE_CODES = {code for code, _ in LANGUAGES}


def get_language_selection_keyboard(ref_part: str, auc_part: str) -> types.InlineKeyboardMarkup:
    buttons = [types.InlineKeyboardButton(text=label, callback_data=f"set_lang:{code}:{ref_part}:{auc_part}")
               for code, label in LANGUAGES]
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def parse_start_args(text: str | None, user_id: int) -> tuple[int | None, int | None]:
    """Возвращает (referrer_id, auction_id) из текста команды /start."""
    if not text:
        return None, None
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return None, None
    arg = parts[1].strip()
    if arg.startswith("auction_") and arg[8:].isdigit():
        return None, int(arg[8:])
    if arg.isdigit() and int(arg) != user_id:
        return int(arg), None
    return None, None


def _auction_id_from(cb_part: str) -> int | None:
    if cb_part.startswith("auc_") and cb_part[4:].isdigit():
        return int(cb_part[4:])
    return None


async def register_user(conn, user_id: int, username: str, lang: str, referrer_id: int | None,
                        display_name: str | None = None) -> bool:
    """Создаёт профиль, если его нет. Начисляет бонус рефереру. Возвращает True, если создан."""
    exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", user_id)
    if exists:
        return False
    if referrer_id is not None:
        referrer_exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", referrer_id)
        if not referrer_exists:
            referrer_id = None

    await conn.execute(
        """
        INSERT INTO users (user_id, username, balance, referred_by, fridge_capacity, fridge_cutlets,
                           inv_cutlets, lang, display_name)
        VALUES ($1, $2, $3, $4, 1, 0, $5, $6, $7)
        """,
        user_id, username, START_BALANCE, referrer_id, START_CUTLETS_INVENTORY, lang,
        (display_name or "")[:128] or None,
    )
    await conn.execute("INSERT INTO ledger (user_id, delta, reason) VALUES ($1, $2, 'signup_bonus')",
                       user_id, START_BALANCE)
    await conn.execute("INSERT INTO game_stats (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)

    if referrer_id is not None:
        await change_balance(conn, referrer_id, REFERRAL_SIGNUP_BONUS, "referral_signup", str(user_id))
    logger.info("[REGISTRATION] user=%s lang=%s referrer=%s", user_id, lang, referrer_id)
    return True


# ============================================================================
# /start
# ============================================================================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = html.escape(message.from_user.username or f"user_{user_id}")
    referrer_id, auction_id = parse_start_args(message.text, user_id)

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT lang FROM users WHERE user_id = $1", user_id)
        if user:
            await conn.execute(
                "UPDATE users SET last_seen_at = NOW(), username = $2, display_name = $3 WHERE user_id = $1",
                user_id, message.from_user.username or f"user_{user_id}",
                (message.from_user.full_name or "")[:128] or None)

    ref_part = str(referrer_id) if referrer_id else "none"
    auc_part = f"auc_{auction_id}" if auction_id else "none"

    if not user:
        await message.answer(
            "🌐 <b>Select your language / Выберите язык:</b>",
            reply_markup=get_language_selection_keyboard(ref_part, auc_part), parse_mode="HTML")
        return

    await state.clear()
    if auction_id:
        await trigger_inline_auction_window(message, auction_id)
        return
    await message.answer(
        f"👋 <b>С возвращением, @{username}!</b>\nТвой прогресс на месте. Панель навигации — внизу экрана.",
        reply_markup=get_reply_main_keyboard(), parse_mode="HTML")


# ============================================================================
# Выбор языка → регистрация → шаг 1
# ============================================================================
@router.callback_query(F.data.startswith("set_lang:"))
async def process_language_binding(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    username = callback.from_user.username or f"user_{user_id}"

    parts = callback.data.split(":")
    if len(parts) != 4:
        return
    _, lang, ref_part, auc_part = parts
    if lang not in LANGUAGE_CODES:
        lang = "ru"
    referrer_id = int(ref_part) if ref_part.isdigit() and int(ref_part) != user_id else None
    auction_id = _auction_id_from(auc_part)

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await register_user(conn, user_id, username, lang, referrer_id,
                                display_name=callback.from_user.full_name)

    start_text = (
        "👋 <b>Привет! Я — ROFL HUB BOT, главный бот игровой экосистемы ROFL HUB. "
        "Это познавательно-развлекательный хаб нового поколения!</b>\n\n"
        "<b>Здесь ты можешь:</b>\n"
        "🎮 Сыграть в чат-бот игры против бота и других игроков\n"
        "💸 Получить игровую валюту за победы или запустить ферму и добывать её круглосуточно\n"
        "🤼 Создать команду и залететь в ТОП рейтинга\n"
        "🏆 Прокачать команду до клана и бороться в международном рейтинге\n"
        "💰 Вместе со своей бандой сорвать куш в миллион монет\n"
        "👑 Купить публикацию на главной странице в соцсетях или на сайте, чтобы продвинуть себя или свой блог\n\n"
        "<b>Этот чат-бот умеет:</b>\n"
        "🎮 Показывать список всех игр, каналов и сайтов ROFL HUB\n"
        "⚡ Начислять монеты в играх, битвах команд и кланов, за достижения, активность и рефералов\n"
        "🔄 Переводить игровые монеты другому игроку ROFL HUB\n"
        "💎 Продавать публикации на сайте и VIP-места для персон и блогеров\n"
        "🚀 Продавать ускорители, звания, статусы и многое другое...\n\n"
        "<i>Жми «ПРОДОЛЖИТЬ», и я расскажу подробнее 👇</i>"
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🛸 ПРОДОЛЖИТЬ", callback_data=f"intro_step_2:{auc_part}")]])
    await callback.message.edit_text(start_text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_2"))
async def cmd_start_step_2(callback: types.CallbackQuery):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    bonus_text = (
        "🎁 <b>ДЕРЖИ СВОИ ПЕРВЫЕ НАГРАДЫ ЗА РЕГИСТРАЦИЮ!</b>\n"
        "..................................................\n"
        f"💸 Тебе начислено: <b>{START_BALANCE} монет</b>\n"
        f"🥩 Тебе начислено: <b>{START_CUTLETS_INVENTORY} кибер-котлета</b>\n"
        "..................................................\n"
        "Это твой стартовый бонус за вступление в клуб ROFL HUB.\n\n"
        "🔒 <i>Бонус выдаётся только один раз в момент регистрации.</i>\n\n"
        "Монеты можно потратить разными способами, они — основа экономики хаба. Береги их...\n\n"
        "⁉️ <b>Но у тебя наверняка возник вопрос:</b> Что за котлета? Кого ей кормить?"
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Что за кибер-котлета?🥩🤔", callback_data=f"intro_step_3:{auc_part}")]])
    await callback.message.edit_text(bonus_text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_3"))
async def cmd_start_step_3(callback: types.CallbackQuery):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    miner_text = (
        "<b>СНАЧАЛА НУЖНО ПОНЯТЬ, ПОЧЕМУ ТАК ВАЖНЫ ИГРОВЫЕ МОНЕТЫ?</b>\n\n"
        "Монеты — это основа всей торговли, состязаний и покупок в <b>ROFL HUB</b>. "
        "Это почти единственная игровая валюта в мире, которую можно добывать бесплатно!\n"
        "..................................................\n"
        "<b>Сделать это можно разными способами:</b>\n"
        "- Приглашать друзей по реферальной ссылке\n"
        "- Побеждать в играх против бота\n"
        "- Побеждать в дуэлях с другими игроками\n"
        "- Участвовать в командных и клановых битвах\n"
        "- Получать бонус за ежедневный вход и задания\n"
        "- Завести робота для круглосуточной добычи монет (робот-майнер / кибер-бурильщик)\n"
        "..................................................\n"
        "<b>Если ты завёл робота второго уровня (кибер-бурильщик) — его нужно кормить каждый день. "
        "Вот здесь и пригодится кибер-котлета — топливо для автоматической добычи, "
        "которое выдаётся бесплатно каждый день! Твоя задача простая — зайти и покормить робота.</b>\n\n"
        "Если не покормить вовремя — робот разряжается и добыча останавливается.\n\n"
        "Робот-майнер (первый уровень) топлива не требует. "
        "Важно! Любой робот покупается на 30 дней — потом его нужно купить заново или завести Мастер-дрона. "
        "Разберёшься по ходу:) Не будем отвлекаться.\n\n"
        "Хочу рассказать ещё немного о <b>ROFL HUB</b>, чтобы было понятно, как здесь всё устроено.\n\n"
        "🛑 <b>Это последнее сообщение нашего знакомства. Дальше только в бой:)</b>"
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Расскажи скорее и в БОЙ!", callback_data=f"intro_step_4:{auc_part}")]])
    await callback.message.edit_text(miner_text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_4"))
async def cmd_start_step_4(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    auction_id = _auction_id_from(auc_part)

    finish_text = (
        "<b>РАССКАЗЫВАЮ ОЧЕНЬ КРАТКО. ROFL HUB — это:</b>\n"
        "- Чат-бот-игры на любой вкус\n"
        "- Возможность создать команду (до 50 человек)\n"
        "- Возможность прокачать её до клана (до 1000 человек)\n"
        "- Командные и клановые битвы за призы\n"
        "- Познавательно-развлекательный канал ROFL HUB CHANNEL\n"
        "- Страница в Instagram — rofl_hub_global\n"
        "- Сайт rofl-hub.com для общения и продвижения без регистрации\n"
        "- Тысячи игроков по всему миру, среди которых могут быть твои новые друзья!\n"
        "..................................................\n"
        "<b>Как и обещал, это завершающее сообщение. Дальше только в бой! Полезные команды:</b>\n\n"
        "/menu — быстрое управление функциями\n"
        "/games — список всех игр\n"
        "/faq — часто задаваемые вопросы\n"
        "/rules — пользовательское соглашение\n"
    )
    await callback.message.edit_text(finish_text, parse_mode="HTML")
    await callback.message.answer(
        "🚀 <b>Консоль управления активирована! Используй кнопки внизу экрана.</b>",
        reply_markup=get_reply_main_keyboard(), parse_mode="HTML")

    if auction_id:
        await state.clear()
        await trigger_inline_auction_window(callback.message, auction_id)


# ============================================================================
# Возвратный аукцион
# ============================================================================
def _auction_text(auction) -> str:
    leader = f"ID <code>{auction['highest_bidder_id']}</code>" if auction["highest_bidder_id"] else "ставок пока нет"
    return (
        "🔥 <b>VIP-АУКЦИОН (СТАВКИ ВОЗВРАТНЫЕ)</b>\n"
        "..................................................\n\n"
        f"🎁 Лот: <b>{html.escape(auction['item_title'])}</b>\n"
        f"📝 Описание: <i>{html.escape(auction['item_desc'] or '')}</i>\n\n"
        f"💰 Текущая цена: <b>{auction['current_price']} рофлов</b>\n"
        f"👑 Лидер: {leader}\n\n"
        "..................................................\n"
        "⚠️ <b>ПРАВИЛА:</b> <i>Ставка списывается сразу. Если тебя перебили — вся сумма мгновенно "
        "возвращается на баланс. Монеты окончательно списываются только у победителя при закрытии лота. "
        f"Минимальный шаг: <b>+{auction['min_step']} рофлов</b>.</i>"
    )


def _auction_kb(auction) -> types.InlineKeyboardMarkup:
    step, aid = auction["min_step"], auction["auction_id"]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=f"💥 +{step}", callback_data=f"auc_bid:{aid}:{step}"),
         types.InlineKeyboardButton(text=f"🚀 +{step * 5}", callback_data=f"auc_bid:{aid}:{step * 5}")],
        [types.InlineKeyboardButton(text="🔄 Обновить", callback_data=f"auc_refresh:{aid}"),
         types.InlineKeyboardButton(text="📱 Главное меню", callback_data="refresh_main_menu")],
    ])


async def trigger_inline_auction_window(message: types.Message, auction_id: int) -> None:
    async with db.pool.acquire() as conn:
        auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1", auction_id)
    if not auction:
        await message.answer("⚠️ <b>Лот не найден или срок его действия истёк.</b>", parse_mode="HTML")
        return
    if auction["status"] != "open":
        await message.answer(
            f"📦 <b>Лот «{html.escape(auction['item_title'])}» закрыт.</b>\n"
            f"Победитель: ID <code>{auction['highest_bidder_id'] or '—'}</code> · "
            f"Финальная цена: <b>{auction['current_price']} рофлов</b>.", parse_mode="HTML")
        return
    await message.answer(_auction_text(auction), reply_markup=_auction_kb(auction), parse_mode="HTML")


@router.callback_query(F.data.startswith("auc_bid:"))
async def process_auction_bid_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    auction_id, bid_step = int(parts[1]), int(parts[2])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
            if not auction:
                await callback.answer("🚨 Лот не существует!", show_alert=True)
                return
            user = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                await callback.answer("Нажми /start для регистрации.", show_alert=True)
                return

            result = compute_bid(
                current_price=auction["current_price"], min_step=auction["min_step"], bid_step=bid_step,
                bidder_id=user_id, bidder_balance=user["balance"],
                highest_bidder_id=auction["highest_bidder_id"], status=auction["status"],
            )
            if not result.ok:
                messages = {
                    "closed": "🚨 Лот уже закрыт!",
                    "insufficient_funds": f"❌ Нужно {result.bidder_charge} рофлов, у тебя {user['balance']}.",
                }
                await callback.answer(messages.get(result.reason, "❌ Ставка отклонена."), show_alert=True)
                return

            await change_balance(conn, user_id, -result.bidder_charge, "auction_bid", str(auction_id))
            if result.refund_to_previous and result.previous_bidder_id:
                await change_balance(conn, result.previous_bidder_id, result.refund_to_previous,
                                     "auction_refund", str(auction_id))
            await conn.execute(
                "UPDATE auctions SET current_price = $1, highest_bidder_id = $2, previous_bidder_id = $3 "
                "WHERE auction_id = $4",
                result.new_price, user_id, result.previous_bidder_id, auction_id)

    if result.previous_bidder_id:
        try:
            await callback.bot.send_message(
                result.previous_bidder_id,
                f"⚠️ Твою ставку на лот «{html.escape(auction['item_title'])}» перебили!\n"
                f"💰 {result.refund_to_previous} рофлов возвращены на баланс.", parse_mode="HTML")
        except Exception:
            pass

    await callback.answer(f"💥 Ставка принята! Цена лота: {result.new_price} рофлов.", show_alert=True)
    await update_auction_view_text(callback, auction_id)


@router.callback_query(F.data.startswith("auc_refresh:"))
async def process_auction_refresh_click(callback: types.CallbackQuery):
    aid = callback.data.split(":")[1]
    await callback.answer("🔄 Обновлено")
    if aid.isdigit():
        await update_auction_view_text(callback, int(aid))


async def update_auction_view_text(callback: types.CallbackQuery, auction_id: int) -> None:
    async with db.pool.acquire() as conn:
        auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1", auction_id)
    if not auction:
        return
    try:
        await callback.message.edit_text(_auction_text(auction), reply_markup=_auction_kb(auction), parse_mode="HTML")
    except Exception:
        pass
