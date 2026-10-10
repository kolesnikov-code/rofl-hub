import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


# ============================================================================
# ШАГ 1: ПЕРВОЕ ПРИВЕТСТВИЕ ПО КОМАНДЕ /START
# ============================================================================
@router.message(Command("start"))
@router.message(F.text == "Первое приветствие")
async def cmd_start(message: types.Message):
    # Парсим реферальный ID из команды, если он передан (например, /start 8476232024)
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].isdigit():
        possible_referrer = int(args[1])
        if possible_referrer != message.from_user.id:
            referrer_id = possible_referrer

    start_text = (
        "👋 <b>Привет! Я — ROFL HUB BOT, главный бот игровой экосистемы ROFL HUB. </b>"
        "<b>Это развлекательный хаб нового поколения!</b>\n\n"
        "<b>Здесь ты можешь:</b>\n"
        "🎮 Сыграть более чем в 20 чат-бот-игр против друга или бота\n"
        "💸 Заработать «рофлы» - игровые монеты экосистемы\n"
        "⚙️ Запустить ферму и круглосуточно майнить валюту <b>ROFL HUB</b>\n"
        "🤼 Создать команду и залететь в ТОП рейтинга своего города\n"
        "🏆 Создать свой клан и залететь в ТОП международного рейтинга\n"
        "💰 Вместе со своей бандой сорвать куш в миллион монет\n"
        "💬 Купить публикацию (за игровые монеты) на главной странице в соцсетях или на сайте, чтобы продвинуть себя или свой блог\n\n"
        "<b>Этот чат-бот умеет:</b>\n"
        "🎮 Показывать список всех игр, каналов и сайтов экосистемы\n"
        "⚡ Начислять рофлы в играх, за достижения и активность\n"
        "🔄 Переводить игровые монеты другому пользователю хаба\n"
        "💎 Продавать публикации на сайте и занимать <b>VIP-места</b> для персон и блогеров\n"
        "🚀 Продавать ускорители, звания, статусы и многое другое...\n\n"
        "<i>Жми кнопку \"ПРОДОЛЖИТЬ\", расскажу подробнее 👇👇👇</i>"
    )

    # Передаем ID реферера в callback_data, чтобы сохранить его на следующем шаге
    cb_data = f"intro_step_2:{referrer_id}" if referrer_id else "intro_step_2:none"

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🛸 ПРОДОЛЖИТЬ", callback_data=cb_data)]
    ])
    await message.answer(start_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# ШАГ 2: РЕГИСТРАЦИЯ И ВЫДАЧА НАГРАД
# ============================================================================
@router.callback_query(F.data.startswith("intro_step_2"))
async def cmd_start_step_2(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    username = callback.from_user.username or f"user_{user_id}"

    # Извлекаем реферальный ID из callback_data
    parts = callback.data.split(":")
    referrer_id = None
    if len(parts) > 1 and parts[1] != "none":
        referrer_id = int(parts[1])

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            try:
                # Проверяем наличие пользователя в базе данных
                user_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)

                if not user_exists:
                    # Создаем запись: 1000 рофлов, 1 котлета в холодильнике, вместимость 1
                    await conn.execute(
                        """
                        INSERT INTO users (user_id, username, balance, referred_by,
                                           fridge_capacity, fridge_cutlets, inv_cutlets)
                        VALUES ($1, $2, 1000, $3, 1, 1, 0)
                        """,
                        user_id, username, referrer_id
                    )

                    # Создаем пустую строку статистики в game_stats
                    await conn.execute(
                        """
                        INSERT INTO game_stats (user_id, games_played, games_won)
                        VALUES ($1, 0, 0)
                        """,
                    user_id
                    )
                    logger.info(f"[REGISTRATION] Новый пользователь зарегистрирован: ID {user_id}")
            except Exception as e:
                logger.error(f"[START_HANDLER] Ошибка регистрации: {e}")

    bonus_text = (
        "🎁 <b>ДЕРЖИ СВОИ ПЕРВЫЕ НАГРАДЫ ЗА РЕГИСТРАЦИЮ!</b>\n"
        "..................................................\n"
        "💸 Тебе начислено: <b>1000 рофлов</b>\n"
        "🥩 Тебе начислено: <b>1 кибер-котлета</b>\n"
        "..................................................\n"
        "Это твой стартовый бонус за вступление в клуб ROFL HUB.\n\n"
        "🔒 <i>Бонус выдаётся только один раз при первой регистрации.</i>\n\n"
        "Монеты можно потратить разными способами, они — основа экономики хаба. Береги их...\n\n"
        "⁉️ <b>Но у тебя наверняка возник вопрос:</b> Что за котлета? Кого ей кормить?"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="What is кибер-котлета?🥩🤔", callback_data="intro_step_3")]
    ])
    await callback.message.edit_text(bonus_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# ШАГ 3: ОБЪЯСНЕНИЕ КИБЕР-КОТЛЕТ И РОБОТОВ
# ============================================================================
@router.callback_query(F.data == "intro_step_3")
async def cmd_start_step_3(callback: types.CallbackQuery):
    await callback.answer()
    miner_text = (
        "<b>СНАЧАЛА НУЖНО ПОНЯТЬ, ПОЧЕМУ ТАК ВАЖНЫ ИГРОВЫЕ МОНЕТЫ \"РОФЛЫ\"?</b>\n\n"
        "Рофлы - это основа всей торговли, состязаний и покупок in <b>ROFL HUB</b>. "
        "Это почти единственная игровая валюта в мире, которую можно добывать бесплатно!\n"
        "..................................................\n"
        "<b>Сделать это можно разными способами:</b>\n\n"
        "- Приглашать друзей по реферальной ссылке\n"
        "- Побеждать в играх против бота\n"
        "- Рубиться в дуэли с другими игроками\n"
        "- Участвовать в командных и клановых битвах\n"
        "- Получать бонус за ежедневный вход и задания\n"
        "- Завести бота для круглосуточной добычи монет (робот-майнер / кибер-бурильщик)\n"
        "..................................................\n"
        "<b>Если ты завёл робота второго уровня (кибер-бурильщик) - его нужно кормить каждый день. </b>"
        "<b>Вот как раз здесь и пригодится кибер-котлета - это топливо для автоматической добычи игровой валюты, "
        "которое выдаётся бесплатно! Нужно лишь зайти и покормить робота.</b>\n\n"
        "Если не покормить вовремя - бот разряжается и добыча валюты останавливается.\n\n"
        "Майнер первого уровня не требует топлива - он вкалывает без дозаправки:) "
        "Важно! Раз в месяц бот любого уровня требует ремонта, т.к. работает круглосуточно... "
        "Думаю, ты разберёшься с этим самостоятельно:) Не будем отвлекаться.\n\n"
        "Хочу рассказать тебе об играх и дуэлях <b>ROFL HUB</b>, чтобы тебе было понятно, как здесь всё устроено.\n\n"
        "🛑 <b>Это будет последнее сообщение нашего знакомства. Дальше только в бой:)</b>"
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Расскажи скорее и в БОЙ!", callback_data="intro_step_4")]
    ])
    await callback.message.edit_text(miner_text, reply_markup=keyboard, parse_mode="HTML")


# ============================================================================
# ШАГ 4: ФИНАЛЬНЫЙ СРЕЗ И ССЫЛКИ НА КОМАНДЫ
# ============================================================================
@router.callback_query(F.data == "intro_step_4")
async def cmd_start_step_4(callback: types.CallbackQuery):
    await callback.answer()
    finish_text = (
        "<b>РАССКАЗЫВАЮ ОЧЕНЬ КРАТКО. ROFL HUB - это:</b>\n\n"
        "- 23 чат-бот-игры на любой вкус\n"
        "- Возможность создать команду (до 50 человек)\n"
        "- Возможность создать клан (до 1000 человек)\n"
        "- Командные и клановые битвы за огромные призы\n"
        "- Познавательно-развлекательный канал ROFL HUB CHANNEL\n"
        "- Сайт rofl-hub.com для общения и продвижения без регистрации\n"
        "- Тысячи других игроков по всему миру, среди которых могут быть твои новые друзья!\n"
        "..................................................\n"
        "<b>Как и обещал, это было финальное сообщение знакомства. Дальше только в бой! Ниже ты видишь несколько ссылок:</b>\n\n"
        "/start - начать диалог заново (если что-то было непонятно)\n"
        "/games - список всех игр клуба ROFL HUB\n"
        "/menu - здесь собраны все команды этого чат-бота\n"
        "/faq - почитать часто-задаваемые вопросы\n"
    )
    await callback.message.edit_text(finish_text, parse_mode="HTML")
