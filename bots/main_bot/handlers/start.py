"""
/start: регистрация сразу (язык — из Telegram) → онбординг 4 шага → reply-панель.
Кнопками языка предлагаются только OFFERED_LANGS (владелец 13.11); остальные языки — автоматически.
Deep-link: /start <referrer_id> или /start auction_<id>.
Плюс контур возвратного аукциона (ставки/обновление).
"""
from __future__ import annotations

import html
import logging

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bots.main_bot.guards import feature_enabled
from bots.main_bot.handlers.app_first import app_markup, app_ready
from bots.main_bot.handlers.menu import get_reply_keyboard, get_reply_main_keyboard
from shared import analytics
from shared.analytics import track
from shared.account_deletion import restore_account
from shared.database import db
from bots.main_bot.webapp_links import app_url
from shared.duels import invite_info, valid_invite_code
from shared.economy import DUEL_INVITE_TTL_HOURS, START_BALANCE, START_CUTLETS_INVENTORY, duel_payout
from shared.locales import btn_variants, resolve_lang, t

router = Router()
logger = logging.getLogger(__name__)

# 14 языков. Порядок задаёт сетку кнопок (по 2 в ряд) — раскладка владельца:
# English–Español / O'zbekcha–Français / Русский–Português / далее произвольно.
LANGUAGES = [
    ("en", "🇺🇸 English"), ("es", "🇪🇸 Español"),
    ("uz", "🇺🇿 O'zbekcha"), ("fr", "🇫🇷 Français"),
    ("ru", "🇷🇺 Русский"), ("pt", "🇧🇷 Português"),
    ("de", "🇩🇪 Deutsch"), ("it", "🇮🇹 Italiano"),
    ("pl", "🇵🇱 Polski"), ("id", "🇮🇩 Indonesia"),
    ("zh", "🇨🇳 中文"), ("hi", "🇮🇳 हिन्दी"),
    ("ar", "🇦🇪 العربية"), ("bn", "🇧🇩 বাংলা"),
]
LANGUAGE_CODES = {code for code, _ in LANGUAGES}
# 13.11 (владелец): на выбор кнопками — только эти языки; остальные 11 включаются сами по языку Telegram.
# Реклама на новый рынок (Бразилия, Индия…) = добавить его код сюда — кнопка появится везде.
OFFERED_LANGS = ("en", "uz", "ru")   # порядок кнопок — владелец
# Языки интерфейса Telegram не из наших 14, чьи носители почти всегда читают по-русски
RU_READERS = {"uk", "be", "kk", "ky", "tg"}
LANG_SHORT = {code: label.split(" ", 1)[0] + " " + code.upper() for code, label in LANGUAGES}   # «🇷🇺 RU»


def lang_from_telegram(code: str | None) -> str:
    """Язык игры по языку интерфейса Telegram: «pt-br» → pt, «uk» → ru, незнакомый или пустой → en."""
    base = (code or "").lower().replace("_", "-").split("-")[0]
    if base in LANGUAGE_CODES:
        return base
    return "ru" if base in RU_READERS else "en"


def offered_langs(current: str | None = None) -> list[str]:
    """Кнопки выбора: предлагаемые языки + текущий, если игроку его подобрали автоматически (чтобы мог вернуться)."""
    codes = list(OFFERED_LANGS)
    if current in LANGUAGE_CODES and current not in codes:
        codes.append(current)
    return codes


LANGUAGE_PROMPT = "🌐 <b>Select your language / Выберите язык:</b>"


def get_language_change_keyboard(current: str | None = None) -> types.InlineKeyboardMarkup:
    """Смена языка зарегистрированным игроком: только предлагаемые языки (+ его текущий), по 2 в ряд."""
    labels = dict(LANGUAGES)
    buttons = [types.InlineKeyboardButton(text=("✅ " if code == current else "") + labels[code],
                                          callback_data=f"chg_lang:{code}") for code in offered_langs(current)]
    return types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])


def intro1_keyboard(lang: str, auc_part: str) -> types.InlineKeyboardMarkup:
    """Первый экран онбординга: «Продолжить» + один ряд коротких кнопок языка (текущий — с ✅)."""
    langs = [types.InlineKeyboardButton(text=("✅ " if code == lang else "") + LANG_SHORT[code],
                                        callback_data=f"ob_lang:{code}:{auc_part}") for code in offered_langs(lang)]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(lang, "start.btn_continue"), callback_data=f"intro_step_2:{auc_part}")],
        langs,
    ])


async def send_lang_hint(target: types.Message, lang: str) -> None:
    """С приложением нижняя панель — одна кнопка «🌐 язык»: показываем её короткой подсказкой."""
    if app_ready():
        await target.answer(t(lang, "lang.kb_hint"), reply_markup=get_reply_keyboard(lang), parse_mode="HTML")


def parse_start_args(text: str | None, user_id: int) -> tuple[int | None, int | None, str | None]:
    """Возвращает (referrer_id, auction_id, raw_arg) из текста команды /start."""
    if not text:
        return None, None, None
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return None, None, None
    arg = parts[1].strip()
    if arg.startswith("auction_") and arg[8:].isdigit():
        return None, int(arg[8:]), arg
    if arg.isdigit() and int(arg) != user_id:
        return int(arg), None, arg
    return None, None, arg


def _source_from_cb(tag: str, referrer_id: int | None) -> str:
    if referrer_id is not None:
        return analytics.SOURCE_REFERRAL
    if tag == "tgr":
        return analytics.SOURCE_TG_AFFILIATE
    if tag.startswith(("p_", "c_")):
        return tag
    return analytics.SOURCE_ORGANIC


def _duel_code_from(cb_part: str | None) -> str | None:
    """«duel_<код>» из аргумента /start или из callback (вызов друга на дуэль по ссылке, 27.10)."""
    if cb_part and cb_part.startswith("duel_") and valid_invite_code(cb_part[5:].lower()):
        return cb_part[5:].lower()
    return None


async def send_duel_invite(target: types.Message, lang: str, code: str) -> None:
    """Сообщение «тебя вызвали на дуэль» с кнопкой в приложение (или подсказкой, если вызов протух)."""
    async with db.pool.acquire() as conn:
        inv = await invite_info(conn, code)
    if inv is None:
        await target.answer(t(lang, "duel.invite_gone"), parse_mode="HTML")
        return
    name = ("@" + inv["username"]) if inv["username"] else html.escape(inv["display_name"] or "?")
    url = app_url("games")
    markup = None
    if url:
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
            text=t(lang, "duel.invite_btn"), web_app=types.WebAppInfo(url=f"{url}&duel={code}"))]])
    await target.answer(t(lang, "duel.invite_msg", name=name, stake=inv["stake"], payout=duel_payout(inv["stake"])[0],
                          hours=DUEL_INVITE_TTL_HOURS), reply_markup=markup, parse_mode="HTML")


def _auction_id_from(cb_part: str) -> int | None:
    if cb_part.startswith("auc_") and cb_part[4:].isdigit():
        return int(cb_part[4:])
    return None


async def register_user(conn, user_id: int, username: str, lang: str, referrer_id: int | None,
                        display_name: str | None = None, source: str = "organic") -> bool:
    """Создаёт профиль, если его нет (реферер только запоминается: бонус — за АКТИВНОГО друга,
    см. analytics.qualify_referral_if_due). Возвращает True, если создан."""
    exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", user_id)
    if exists:
        return False
    if referrer_id is not None:
        referrer_exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", referrer_id)
        if not referrer_exists:
            referrer_id = None
            if source == analytics.SOURCE_REFERRAL:
                source = analytics.SOURCE_ORGANIC

    await conn.execute(
        """
        INSERT INTO users (user_id, username, balance, referred_by, fridge_capacity, fridge_cutlets,
                           inv_cutlets, lang, display_name, source)
        VALUES ($1, $2, $3, $4, 1, 0, $5, $6, $7, $8)
        """,
        user_id, username, START_BALANCE, referrer_id, START_CUTLETS_INVENTORY, lang,
        (display_name or "")[:128] or None, source[:32],
    )
    await conn.execute("INSERT INTO ledger (user_id, delta, reason) VALUES ($1, $2, 'signup_bonus')",
                       user_id, START_BALANCE)
    await conn.execute("INSERT INTO game_stats (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)

    logger.info("[REGISTRATION] user=%s lang=%s referrer=%s", user_id, lang, referrer_id)
    return True


# ============================================================================
# /start
# ============================================================================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = html.escape(message.from_user.username or f"user_{user_id}")
    referrer_id, auction_id, raw_arg = parse_start_args(message.text, user_id)
    duel_code = _duel_code_from(raw_arg)
    if duel_code and referrer_id is None:
        # Пришёл по вызову на дуэль: новичок становится рефералом того, кто позвал (бонус — только за активного друга)
        async with db.pool.acquire() as conn:
            inv = await invite_info(conn, duel_code)
        if inv is not None and inv["player1"] != user_id:
            referrer_id = inv["player1"]
    source = analytics.parse_source(raw_arg, referrer_id)

    returned = False
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT lang, deleted_at FROM users WHERE user_id = $1", user_id)
        if user and user["deleted_at"] is not None:
            # Вернулся после удаления: старт с нуля, бонусы новичка не повторяются
            async with conn.transaction():
                returned = await restore_account(conn, user_id, message.from_user.username or f"user_{user_id}",
                                                 message.from_user.full_name)
        elif user:
            await conn.execute(
                "UPDATE users SET last_seen_at = NOW(), username = $2, display_name = $3 WHERE user_id = $1",
                user_id, message.from_user.username or f"user_{user_id}",
                (message.from_user.full_name or "")[:128] or None)

    ref_part = str(referrer_id) if referrer_id else "none"
    auc_part = f"auc_{auction_id}" if auction_id else (f"duel_{duel_code}" if duel_code else "none")

    if not user:
        # 13.11: без сетки языков — регистрируем сразу, язык из Telegram; сменить — кнопками под первым экраном
        lang = lang_from_telegram(message.from_user.language_code)
        await register_and_greet(message, user_id, message.from_user.username or f"user_{user_id}",
                                 message.from_user.full_name, lang, referrer_id, auc_part, source)
        return

    lang = resolve_lang(user["lang"])
    await state.clear()
    await send_lang_hint(message, lang)
    if returned:
        await message.answer(t(lang, "acct.welcome_back"),
                             reply_markup=_main_markup(lang), parse_mode="HTML")
        return
    if auction_id:
        await trigger_inline_auction_window(message, auction_id)
        return
    if duel_code:
        async with db.pool.acquire() as conn:
            await conn.execute("UPDATE users SET pending_duel = $2 WHERE user_id = $1", user_id, duel_code)
        await send_duel_invite(message, lang, duel_code)
        return
    if app_ready():
        await message.answer(t(lang, "start.welcome_back_app", username=username), parse_mode="HTML")
        await send_pinned_app(message, lang)
        return
    await message.answer(t(lang, "start.welcome_back", username=username),
                         reply_markup=_main_markup(lang), parse_mode="HTML")


async def send_pinned_app(target: types.Message, lang: str) -> None:
    """📌 «Открыть приложение» с инлайн-кнопкой — закреплено вверху чата (владелец 04.11): после онбординга, на /start
    и после смены языка. Прошлые закрепы бота снимаются, чтобы наверху был один, на языке игрока; сбой закрепа не мешает."""
    markup = app_markup(lang)
    if markup is None:
        return
    sent = await target.answer(t(lang, "app.btn"), reply_markup=markup)
    if sent is None:
        return
    try:
        await sent.bot.unpin_all_chat_messages(sent.chat.id)
        await sent.pin(disable_notification=True)
    except Exception:
        logger.warning("pin app message failed", exc_info=True)


def _main_markup(lang: str):
    """Вся игра в приложении (27.10) — одна кнопка «открыть»; без WEBAPP_URL — прежняя нижняя клавиатура."""
    return app_markup(lang) if app_ready() else get_reply_main_keyboard(lang)


# ============================================================================
# Выбор языка → регистрация → шаг 1
# ============================================================================
@router.callback_query(F.data.startswith("set_lang:"))
async def process_language_binding(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    username = callback.from_user.username or f"user_{user_id}"

    parts = callback.data.split(":")
    if len(parts) not in (4, 5):   # 4 — старые кнопки, выданные до появления source
        return
    _, lang, ref_part, auc_part = parts[:4]
    src_part = parts[4] if len(parts) == 5 else "none"
    if lang not in LANGUAGE_CODES:
        lang = "ru"
    referrer_id = int(ref_part) if ref_part.isdigit() and int(ref_part) != user_id else None
    source = _source_from_cb(src_part, referrer_id)
    # Старая сетка 14 языков (сообщения, отправленные до 13.11): та же регистрация, что теперь сразу по /start
    await register_and_greet(callback.message, user_id, username, callback.from_user.full_name, lang,
                             referrer_id, auc_part, source, edit=True)


async def register_and_greet(target: types.Message, user_id: int, username: str, full_name: str | None, lang: str,
                             referrer_id: int | None, auc_part: str, source: str, edit: bool = False) -> None:
    """Регистрация + первый экран онбординга (с кнопками языка). edit=True — правит сообщение со старой сеткой."""
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            created = await register_user(conn, user_id, username, lang, referrer_id,
                                          display_name=full_name, source=source)
            if (code := _duel_code_from(auc_part)) is not None:
                await conn.execute("UPDATE users SET pending_duel = $2 WHERE user_id = $1", user_id, code)
            if not created:   # уже был (повторный /start, гонка двух нажатий) — первый экран на его языке
                lang = resolve_lang(await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", user_id))
    if created:
        await track(user_id, "registered", source=source, lang=lang)
    send = target.edit_text if edit else target.answer
    await send(t(lang, "start.intro1"), reply_markup=intro1_keyboard(lang, auc_part), parse_mode="HTML")


@router.callback_query(F.data.startswith("ob_lang:"))
async def process_onboarding_language(callback: types.CallbackQuery):
    """Кнопка языка под первым экраном: язык профиля меняется, экран перерисовывается на нём."""
    parts = callback.data.split(":", 2)
    lang = parts[1] if len(parts) == 3 else ""
    if lang not in LANGUAGE_CODES:
        await callback.answer()
        return
    async with db.pool.acquire() as conn:
        await conn.execute("UPDATE users SET lang = $2 WHERE user_id = $1", callback.from_user.id, lang)
    await callback.answer()
    try:
        await callback.message.edit_text(t(lang, "start.intro1"), reply_markup=intro1_keyboard(lang, parts[2]),
                                         parse_mode="HTML")
    except Exception:   # нажали тот же язык — текст не изменился
        pass


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
    await send_lang_hint(callback.message, user_lang)
    if app_ready():
        await callback.message.answer(t(user_lang, "start.console_app"), parse_mode="HTML")
        await send_pinned_app(callback.message, user_lang)
    else:
        await callback.message.answer(t(user_lang, "start.console"),
                                      reply_markup=_main_markup(user_lang), parse_mode="HTML")
    await track(callback.from_user.id, "onboarding_done")

    if auction_id:
        await state.clear()
        await trigger_inline_auction_window(callback.message, auction_id)
    if (code := _duel_code_from(auc_part)) is not None:
        await send_duel_invite(callback.message, user_lang, code)


# ============================================================================
# 🌐 Смена языка (02.11): кнопка нижней панели или /language — на случай, если выбрали не тот язык
# ============================================================================
@router.message(Command("language", "lang"))
@router.message(F.text.in_(btn_variants("language")))
async def cmd_change_language(message: types.Message, user_lang: str = "ru"):
    await message.answer(LANGUAGE_PROMPT, reply_markup=get_language_change_keyboard(user_lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("chg_lang:"))
async def process_language_change(callback: types.CallbackQuery):
    lang = callback.data.split(":", 1)[1]
    if lang not in LANGUAGE_CODES:
        await callback.answer()
        return
    async with db.pool.acquire() as conn:
        status = await conn.execute("UPDATE users SET lang = $2 WHERE user_id = $1", callback.from_user.id, lang)
    if status.endswith(" 0"):   # ещё не зарегистрирован — язык выбирается в /start
        await callback.answer("/start", show_alert=True)
        return
    await callback.answer()
    label = dict(LANGUAGES)[lang]
    try:
        await callback.message.edit_text(f"🌐 ✅ {label}")
    except Exception:
        pass
    await callback.message.answer(t(lang, "lang.changed"), reply_markup=get_reply_keyboard(lang), parse_mode="HTML")
    if app_ready():
        await send_pinned_app(callback.message, lang)   # закреп — на новом языке


# ============================================================================
# Возвратный аукцион
# ============================================================================
def _auction_text(auction) -> str:
    leader = f"ID <code>{auction['highest_bidder_id']}</code>" if auction["highest_bidder_id"] else "ставок пока нет"
    return (
        "🔥 <b>VIP-АУКЦИОН (СТАВКИ ВОЗВРАТНЫЕ)</b>\n"
        "..................................................\n"
        f"🎁 Лот: <b>{html.escape(auction['item_title'])}</b>\n"
        f"📝 Описание: <i>{html.escape(auction['item_desc'] or '')}</i>\n\n"
        f"💰 Текущая цена: <b>{auction['current_price']} монет</b>\n"
        f"👑 Лидер: {leader}\n"
        "..................................................\n"
        "⚠️ <b>ПРАВИЛА:</b> <i>Ставка списывается сразу. Если тебя перебили — вся сумма мгновенно "
        "возвращается на баланс. Монеты окончательно списываются только у победителя при закрытии лота. "
        f"Минимальный шаг: <b>+{auction['min_step']} монет</b>.</i>"
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
            f"Финальная цена: <b>{auction['current_price']} монет</b>.", parse_mode="HTML")
        return
    await message.answer(_auction_text(auction), reply_markup=_auction_kb(auction), parse_mode="HTML")


@router.callback_query(F.data.startswith("auc_bid:"))
async def process_auction_bid_click(callback: types.CallbackQuery, user_lang: str = "ru"):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    auction_id, bid_step = int(parts[1]), int(parts[2])
    if not await feature_enabled(callback, "auctions", user_lang):   # тумблер аукционов — и для чата
        return

    from shared.auctions import AuctionError, notify_outbid, place_bid
    lang = user_lang
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await place_bid(conn, user_id, auction_id, bid_step)
    except AuctionError as e:
        await callback.answer(html.unescape(e.localized(lang)), show_alert=True)
        return

    await track(user_id, "auction_bid", auction_id=auction_id, amount=result["charge"])
    await notify_outbid(callback.bot, result)
    await callback.answer(t(lang, "auc.bid_ok", price=result["price"]), show_alert=True)
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
