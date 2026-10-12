import logging
from datetime import datetime, timezone
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from shared.database import db
from bots.main_bot.handlers.menu import get_reply_main_keyboard

router = Router()
logger = logging.getLogger(__name__)


# ============================================================================
# 🌍 МЕЖДУНАРОДНЫЙ СЕЛЕКТОР: СЕТКА ИЗ 13 УТВЕРЖДЕННЫХ ЯЗЫКОВ МИРА
# ============================================================================
def get_language_selection_keyboard(ref_part: str, auc_part: str) -> types.InlineKeyboardMarkup:
    """Генерирует компактную инлайн-сетку флагов мира с пробросом аргументов"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"set_lang:ru:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇺🇸 English", callback_data=f"set_lang:en:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇨🇳 中文", callback_data=f"set_lang:zh:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data=f"set_lang:hi:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇪🇸 Español", callback_data=f"set_lang:es:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇦🇪 العربية", callback_data=f"set_lang:ar:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇫🇷 Français", callback_data=f"set_lang:fr:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇧🇩 বাংলা", callback_data=f"set_lang:bn:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇧🇷 Português", callback_data=f"set_lang:pt:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data=f"set_lang:id:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data=f"set_lang:de:{ref_part}:{auc_part}"),
            types.InlineKeyboardButton(text="🇮🇹 Italiano", callback_data=f"set_lang:it:{ref_part}:{auc_part}")
        ],
        [
            types.InlineKeyboardButton(text="🇵🇱 Polski", callback_data=f"set_lang:pl:{ref_part}:{auc_part}")
        ]
    ])


# ============================================================================
# 🏁 ТОЧКА ВХОДА: ВЫЗОВ ВЫБОРА ЯЗЫКА ПРИ ПЕРВОМ КАСАНИИ /START
# ============================================================================
@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    # Безопасный разбор deep-link аргументов
    start_args = None
    try:
        if hasattr(message, "text") and len(message.text.split()) > 1:
            start_args = message.text.split()[-1].strip()
    except Exception as e:
        logger.error(f"[START_ARGS_ERROR] Сбой парсинга аргументов: {e}")

    auction_id = None
    referrer_id = None

    if start_args:
        if start_args.startswith("auction_"):
            try:
                auction_id = int(start_args.split("_")[-1])
            except ValueError:
                pass
        elif start_args.isdigit():
            possible_referrer = int(start_args)
            if possible_referrer != user_id:
                referrer_id = possible_referrer

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT lang FROM users WHERE user_id = $1", user_id)

    # Запечатываем параметры для сквозного прохода по инлайн-кнопкам
    ref_part = str(referrer_id) if referrer_id else "none"
    auc_part = f"auc_{auction_id}" if auction_id else "none"

    if not user:
        # 🔥 ПЕРВЫЙ ЗАПУСК: Никакого текста, строго инлайн-кнопки выбора языка!
        await message.answer(
            "🌐 <b>Select your language / Выберите язык экосистемы:</b>",
            reply_markup=get_language_selection_keyboard(ref_part, auc_part),
            parse_mode="HTML"
        )
    else:
        # Если юзер уже есть и у него намертво приклеен язык — шлём в окно аукциона или меню
        if auction_id:
            await state.clear()
            await trigger_inline_auction_window(message, auction_id)
            return

        await message.answer(
            f"👋 <b>С возвращением, @{username}!</b>\n"
            f"Все твои данные и прогресс в полной безопасности. Используй нижнюю панель для навигации!",
            reply_markup=get_reply_main_keyboard(),
            parse_mode="HTML"
        )


# ============================================================================
# 💾 АТОМАРНАЯ ФИКСАЦИЯ ЯЗЫКА В СУБД И ВЫДАЧА ШАГА №1 (ТВОЙ ОРИГИНАЛ)
# ============================================================================
@router.callback_query(F.data.startswith("set_lang:"))
async def process_language_binding(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    username = callback.from_user.username or f"user_{user_id}"

    # Парсим параметры: set_lang:код_языка:реферер:аукцион
    _, selected_lang, ref_part, auc_part = callback.data.split(":")

    referrer_id = int(ref_part) if ref_part != "none" else None
    auction_id = int(auc_part.split("_")[-1]) if auc_part != "none" else None

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)
            if not user_exists:
                # Намертво приклеиваем выбранный язык при первичной регистрации кита!
                await conn.execute(
                    """
                    INSERT INTO users (user_id, username, balance, referred_by,
                                       fridge_capacity, fridge_cutlets, inv_cutlets, lang)
                    VALUES ($1, $2, 1000, $3, 1, 1, 0, $4)
                    """,
                    user_id, username, referrer_id, selected_lang
                )
                await conn.execute("INSERT INTO game_stats (user_id, games_played, games_won) VALUES ($1, 0, 0);",
                                   user_id)
                logger.info(f"[REGISTRATION] Юзер {user_id} зарегистрирован с языком: {selected_lang}")

    # 🔥 ТВОЙ СВЯЩЕННЫЙ ОРИГИНАЛЬНЫЙ ТЕКСТ ШАГА №1 (ВЫЛЕТАЕТ СТРОГО ПОСЛЕ ВЫБОРА ЯЗЫКА)
    start_text = (
        "👋 <b>Привет! Я — ROFL HUB BOT, главный бот игровой экосистемы ROFL HUB. </b>"
        "<b>Это познавательно-развлекательный хаб нового поколения!</b>\n\n"
        "<b>Здесь ты можешь:</b>\n"
        "🎮 Сыграть более чем в 20 чат-бот игр против друга или бота\n"
        "💸 Получить игровую валюту за победы in чат-бот играх или запустить ферму и круглосуточно добывать\n"
        "🤼 Создать команду и залететь в ТОП рейтинга своего города\n"
        "🏆 Создать свой клан и залететь в ТОП международного рейтинга\n"
        "💰 Вместе со своей бандой сорвать куш в миллион монет\n"
        "👑 Купить публикацию (за игровые монеты) на главной странице в соцсетях или на сайте, чтобы продвинуть себя или свой блог на весь мир\n\n"
        "<b>Этот чат-бот умеет:</b>\n"
        "🎮 Показывать список всех игр, каналов и сайтов ROFL HUB\n"
        "⚡ Начислять монеты в играх, битвах среди команд и кланов, а также за достижения, активность, и рефералов\n"
        "🔄 Переводить игровые монеты другому пользователю ROFL HUB\n"
        "💎 Продавать публикации на сайте и занимать <b>VIP-места</b> для персон и блогеров\n"
        "🚀 Продавать ускорители, звания, статусы и многое другое...\n\n"
        f"<i>Жми кнопку \"ПРОДОЛЖИТЬ\", и я расскажу подробнее 👇👇👇</i>"
    )

    next_cb = f"intro_step_2:{auc_part}" if auction_id else "intro_step_2:none"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🛸 ПРОДОЛЖИТЬ", callback_data=next_cb)]
    ])

    # Стираем окно выбора языка и бесшовно выводим Шаг №1
    await callback.message.edit_text(start_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# 🎁 ШАГ 2: ВЫДАЧА НАГРАД (ТВОЙ ОРИГИНАЛЬНЫЙ ТЕКСТ БЕЗ ИЗМЕНЕНИЙ)
# ============================================================================
@router.callback_query(F.data.startswith("intro_step_2"))
async def cmd_start_step_2(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    parts = callback.data.split(":")
    auction_id = None
    if len(parts) > 1 and parts[1] != "none":
        auction_id = int(parts[1].split("_")[-1])

    # 🔥 ТВОЙ ОРИГИНАЛЬНЫЙ ТЕКСТ ШАГА №2
    bonus_text = (
        "🎁 <b>ДЕРЖИ СВОИ ПЕРВЫЕ НАГРАДЫ ЗА REГИСТРAЦИЮ!</b>\n"
        "..................................................\n"
        "💸 Тебе начислено: <b>1000 монет</b>\n"
        "🥩 Тебе начислено: <b>1 кибер-котлета</b>\n"
        "..................................................\n"
        "Это твой стартовый бонус за вступление в клуб ROFL HUB.\n\n"
        "🔒 <i>Бонус выдаётся только один раз в момент регистрации.</i>\n\n"
        "Монеты можно потратить разными способами, они — основа экономики хаба. Береги их...\n\n"
        "⁉️ <b>Но у тебя наверняка возник вопрос:</b> Что за котлета? Кого ей кормить?"
    )

    next_cb = f"intro_step_3:auc_{auction_id}" if auction_id else "intro_step_3:none"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Что за кибер-котлета?🥩🤔", callback_data=next_cb)]
    ])
    await callback.message.edit_text(bonus_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# 🥩 ШАГ 3: ОБЪЯСНЕНИЕ КИБЕР-КОТЛЕТ И РОБОТОВ (ТВОЙ ОРИГИНАЛЬНЫЙ ТЕКСТ)
# ============================================================================
@router.callback_query(F.data.startswith("intro_step_3"))
async def cmd_start_step_3(callback: types.CallbackQuery):
    await callback.answer()

    # Извлекаем ID аукциона из callback_data
    parts = callback.data.split(":")
    auction_id = None
    if len(parts) > 1 and parts[1] != "none":
        auction_id = int(parts[1].split("_")[-1])

    # 🔥 ТВОЙ СВЯЩЕННЫЙ ОРИГИНАЛЬНЫЙ ТЕКСТ ШАГА №3
    miner_text = (
        "<b>СНАЧАЛА НУЖНО ПОНЯТЬ, ПОЧЕМУ ТАК ВАЖНЫ ИГРОВЫЕ МОНЕТЫ?</b>\n\n"
        "Монеты - это основа всей торговли, состязаний и покупок в <b>ROFL HUB</b>. "
        "Это почти единственная игровая валюта in мире, которую можно добывать бесплатно!\n"
        "..................................................\n"
        "<b>Сделать это можно разными способами:</b>\n"
        "- Приглашать друзей по реферальной ссылке\n"
        "- Побеждать in играх против бота\n"
        "- Побеждать in дуэлях с другими игроками\n"
        "- Участвовать in командных и клановых битвах\n"
        "- Получать бонус за ежедневный вход и задания\n"
        "- Завести робота для круглосуточной добычи монет (робот-майнер / кибер-бурильщик)\n"
        "..................................................\n"
        "<b>Если ты завёл робота второго уровня (кибер-бурильщик) - его нужно кормить каждый день. </b>"
        "<b>Вот как раз здесь и пригодится кибер-котлета - это топливо для автоматической добычи игровой валюты, "
        "которое выдаётся бесплатно каждый день! Твоя задача очень простая - зайти и покормить робота.</b>\n\n"
        "Если не покормить вовремя - робот разряжается и добыча валюты останавливается.\n\n"
        "Робот-майнер (первый уроовень) не требует топлива - он добывает без дозаправки, ему не нужны кибер-котлеты:) "
        "Важно! Раз в месяц бот любого уровня требует ремонта, т.к. работает круглосуточно... "
        "Я думаю, ты разберёшься с этим самостоятельно:) Не будем отвлекаться.\n\n"
        "Хочу рассказать тебе ещё немного о <b>ROFL HUB</b>, чтобы тебе было понятно, как здесь всё устроено.\n\n"
        "🛑 <b>Это будет последнее сообщение нашего знакомства. Дальше только in бой:)</b>"
    )

    next_cb = f"intro_step_4:auc_{auction_id}" if auction_id else "intro_step_4:none"

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Расскажи скорее и in БОЙ!", callback_data=next_cb)]
    ])
    await callback.message.edit_text(miner_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# 🏁 ШАГ 4: ФИНАЛЬНЫЙ СРЕЗ ЗНАКОМСТВА ИЛИ ДИПЛИНК ПЕРЕЛЕТ
# ============================================================================
@router.callback_query(F.data.startswith("intro_step_4"))
async def cmd_start_step_4(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id

    parts = callback.data.split(":")
    auction_id = None
    if len(parts) > 1 and parts[1] != "none":
        auction_id = int(parts[1].split("_")[-1])

    # 🔥 ТВОЙ ОРИГИНАЛЬНЫЙ ТЕКСТ ШАГА №4
    finish_text = (
        "<b>РАССКАЗЫВАЮ ОЧЕНЬ КРАТКО. ROFL HUB - это:</b>\n"
        "- 23 чат-бот-игры на любой вкус\n"
        "- Возможность создать команду (до 50 человек)\n"
        "- Возможность создать клан (до 1000 человек)\n"
        "- Командные и клановые битвы за огромные призы\n"
        "- Познавательно-развлекательный канал ROFL HUB CHANNEL\n"
        "- Страница in Instagram - rofl_hub_global"
        "- Сайт rofl-hub.com для общения и продвижения без регистрации\n"
        "- Тысячи других игроков по всему миру, среди которых могут быть твои новые друзья!\n"
        "..................................................\n"
        "<b>Как и обещал, это было завершающее сообщение нашего знакомства. Дальше только in бой! Ниже ты видишь несколько ссылок:</b>\n\n"
        "/start - начать диалог заново (если что-то было непонятно)\n"
        "/games - список всех игр клуба ROFL HUB\n"
        "/menu - быстрое управление функциями ROFL HUB\n"
        "/faq - почитать часто-задаваемые вопросы\n"
        "/rules - пользовательское соглашение\n"
    )

    # Принудительно выкатываем нижнюю Reply-клавиатуру 2х3, чтобы она закрепилась намертво!
    await callback.message.answer(
        "🚀 <b>Консоль управления успешно активирована! Используй кнопки внизу экрана.</b>",
        reply_markup=get_reply_main_keyboard(),
        parse_mode="HTML"
    )
    await callback.message.edit_text(finish_text, parse_mode="HTML")

    # Бесшовный перелёт на карточку аукциона
    if auction_id:
        await state.clear()
        await trigger_inline_auction_window(callback.message, auction_id)


# ============================================================================
# 🔮 5. МОДЕРНИЗИРОВАННЫЙ КОНТУР АБСОЛЮТНО ВОЗВРАТНЫХ АУКЦИОНОВ
# ============================================================================
async def trigger_inline_auction_window(message: types.Message, auction_id: int):
    async with db.pool.acquire() as conn:
        auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1", auction_id)

    if not auction:
        await message.answer("⚠️ <b>Упс! Срок действия лота истёк!</b>", parse_mode="HTML")
        return

    if auction["status"] != "open":
        await message.answer(
            f"📦 <b>Лот «{auction['item_title']}» уже ЗАКРЫТ!</b>\n\n"
            f"Победитель раунда: ID <code>{auction['highest_bidder_id']}</code>\n"
            f"Финальная цена: <b>{auction['current_price']} рофлов</b>.\n\n"
            f"🎯 <i>Твоя ставка не победила! Включай ферму, копи монеты и жди следующий лот!</i>",
            parse_mode="HTML"
        )
        return

    auction_text = (
        f"🔥 <b>VIP-АУКЦИОН ИЗ КАНАЛА! (СТАВКИ ВОЗВРАТНЫЕ)</b>\n"
        f"..................................................\n\n"
        f"🎁 Лот: <b>{auction['item_title']}</b>\n"
        f"📝 Описание: <i>{auction['item_desc']}</i>\n\n"
        f"💰 Текущая ставка: <b>{auction['current_price']} рофлов</b>\n"
        f"👑 Лидер раунда: ID <code>{auction['highest_bidder_id'] if auction['highest_bidder_id'] else 'Ставок пока нет'}</code>\n\n"
        f"..................................................\n"
        f"⚠️ <b>ОБЩИЕ ПРАВИЛА АУКЦИОНА:</b>\n"
        f"<i>Принимаются только ВОЗВРАТНЫЕ ставки! Если твою ставку перебьет другой игрок, "
        f"твои рофлы МГНОВЕННО и в полном объеме вернутся обратно к тебе на баланс СУБД Railway! "
        f"Монеты спишутся окончательно только у победителя в момент закрытия лота. "
        f"Минимальный шаг повышения: <b>+{auction['min_step']} рофлов</b>.</i>"
    )

    step = auction["min_step"]
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=f"💥 Поднять на +{step} рофлов",
                                       callback_data=f"auc_bid:{auction_id}:{step}"),
            types.InlineKeyboardButton(text=f"🚀 Поднять на +{step * 5} рофлов",
                                       callback_data=f"auc_bid:{auction_id}:{step * 5}")
        ],
        [
            types.InlineKeyboardButton(text="🔄 Обновить статус лота", callback_data=f"auc_refresh:{auction_id}"),
            types.InlineKeyboardButton(text="📱 Главное Меню", callback_data="refresh_main_menu")
        ]
    ])

    await message.answer(auction_text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("auc_bid:"))
async def process_auction_bid_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    auction_id = int(parts[1])
    bid_step = int(parts[2])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1 FOR UPDATE", auction_id)
            user = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1 FOR UPDATE", user_id)

            if not auction or auction["status"] != "open":
                await callback.answer("🚨 Лот закрыт или не существует!", show_alert=True)
                return
            if not user or user["balance"] < bid_step:
                await callback.answer("❌ Недостаточно монет на балансе для этой ставки!", show_alert=True)
                return

            # 🔥 ГЕHИАЛЬНЫЙ ФИНТEХ-ВOЗВРAТ: Возвращаем монеты прошлому лидеру, если он был!
            prev_leader_id = auction["highest_bidder_id"]
            if prev_leader_id and prev_leader_id != user_id:
                await conn.execute(
                    "UPDATE users SET balance = balance + $1 WHERE user_id = $2",
                    auction["current_price"], prev_leader_id
                )
                try:
                    # Уведомляем прошлого лидера в личку (опционально, не ломает поток)
                    await callback.bot.send_message(
                        chat_id=prev_leader_id,
                        text=f"⚠️ <b>Твою ставку в аукционе на лот «{auction['item_title']}» перебили!</b>\n"
                             f"💰 <code>{auction['current_price']} рофлов</code> успешно возвращены на твой баланс профиля!"
                    )
                except Exception:
                    pass

            # Фиксируем новые данные
            new_price = auction["current_price"] + bid_step
            new_balance = user["balance"] - bid_step

            await conn.execute("UPDATE users SET balance = $1 WHERE user_id = $2", new_balance, user_id)
            await conn.execute(
                """
                UPDATE auctions
                SET current_price      = $1,
                    highest_bidder_id  = $2,
                    previous_bidder_id = $3
                WHERE auction_id = $4
                """,
                new_price, user_id, prev_leader_id, auction_id
            )

    await callback.answer(f"💥 Твоя ставка принята! Текущая цена лота: {new_price} рофлов!", show_alert=True)
    await update_auction_view_text(callback, auction_id)


@router.callback_query(F.data.startswith("auc_refresh:"))
async def process_auction_refresh_click(callback: types.CallbackQuery):
    auction_id = int(callback.data.split(":")[1])
    await callback.answer("🔄 Данные лота синхронизированы!")
    await update_auction_view_text(callback, auction_id)


async def update_auction_view_text(callback: types.CallbackQuery, auction_id: int):
    async with db.pool.acquire() as conn:
        auction = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1", auction_id)
    if not auction:
        return

    step = auction["min_step"]
    updated_text = (
        f"🔥 <b>VIP-АУКЦИОН ИЗ КАНАЛА! (СТАВКИ ВОЗВРАТНЫЕ)</b>\n"
        f"..................................................\n\n"
        f"🎁 Лот: <b>{auction['item_title']}</b>\n"
        f"📝 Описание: <i>{auction['item_desc']}</i>\n\n"
        f"💰 Текущая ставка: <b>{auction['current_price']} рофлов</b>\n"
        f"👑 Лидер раунда: ID <code>{auction['highest_bidder_id'] if auction['highest_bidder_id'] else 'Ставок пока нет'}</code>\n\n"
        f"..................................................\n"
        f"⚠️ <b>ОБЩИЕ ПРАВИЛА АУКЦИОНА:</b>\n"
        f"<i>Принимаются только ВОЗВРАТНЫЕ ставки! Если твою ставку перебьет другой игрок, "
        f"твои рофлы МГНОВЕННО и в полном объеме вернутся обратно к тебе на баланс СУБД Railway! "
        f"Монеты спишутся окончательно только у победителя в момент закрытия лота. "
        f"Минимальный шаг повышения: <b>+{step} рофлов</b>.</i>"
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=f"💥 Поднять на +{step} рофлов",
                                       callback_data=f"auc_bid:{auction_id}:{step}"),
            types.InlineKeyboardButton(text=f"🚀 Поднять на +{step * 5} рофлов",
                                       callback_data=f"auc_bid:{auction_id}:{step * 5}")
        ],
        [
            types.InlineKeyboardButton(text="🔄 Обновить статус лота", callback_data=f"auc_refresh:{auction_id}"),
            types.InlineKeyboardButton(text="📱 Главное Меню", callback_data="refresh_main_menu")
        ]
    ])

    try:
        await callback.message.edit_text(updated_text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
