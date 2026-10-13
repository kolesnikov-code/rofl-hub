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
from shared.locales import resolve_lang, t

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

    lang = resolve_lang(user["lang"])
    await state.clear()
    if auction_id:
        await trigger_inline_auction_window(message, auction_id)
        return
    await message.answer(
        t(lang, "start.welcome_back", username=username),
        reply_markup=get_reply_main_keyboard(lang), parse_mode="HTML")


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

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(lang, "start.btn_continue"),
                                    callback_data=f"intro_step_2:{auc_part}")]])
    await callback.message.edit_text(t(lang, "start.intro1"), reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_2"))
async def cmd_start_step_2(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "start.btn_cutlet"),
                                    callback_data=f"intro_step_3:{auc_part}")]])
    await callback.message.edit_text(
        t(user_lang, "start.intro2", balance=START_BALANCE, cutlets=START_CUTLETS_INVENTORY),
        reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_3"))
async def cmd_start_step_3(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "start.btn_fight"),
                                    callback_data=f"intro_step_4:{auc_part}")]])
    await callback.message.edit_text(t(user_lang, "start.intro3"), reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("intro_step_4"))
async def cmd_start_step_4(callback: types.CallbackQuery, state: FSMContext, user_lang: str = "ru"):
    await callback.answer()
    auc_part = callback.data.split(":")[1] if ":" in callback.data else "none"
    auction_id = _auction_id_from(auc_part)

    await callback.message.edit_text(t(user_lang, "start.intro4"), parse_mode="HTML")
    await callback.message.answer(
        t(user_lang, "start.console"),
        reply_markup=get_reply_main_keyboard(user_lang), parse_mode="HTML")

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
