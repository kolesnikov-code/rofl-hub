from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


# ----------------------------------------------------------------
# 🏪 ГЛАВНАЯ ВИТРИНА МАГАЗИНА
# ----------------------------------------------------------------
@router.message(Command("shop"))
@router.message(Command("buy_miner"))
@router.message(Command("buy_coins"))
async def cmd_shop_catalog(message: types.Message):
    shop_text = (
        "🏪 <b>МАРКЕТПЛЕЙС ИГРОВЫХ ТОВАРОВ ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 <b>Прокачай свой аккаунт и запусти пассивный доход!</b>\n"
        "Покупки совершаются моментально через официальные звёзды Telegram Stars.\n"
        "..................................................\n"
        "👇 <b>ВЫБЕРИ ТОВАР ДЛЯ ПОКУПКИ:</b>"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🤖 Робот «Младший Майнер» | ★ 49 Stars", callback_data="buy_miner_junior")],
        [types.InlineKeyboardButton(text="⚡ Робот «Кибер Бурильщик» | ★ 99 Stars", callback_data="buy_miner_premium")],        # "/buy_post - купить публикацию на сайте\n"
        # "/buy_vip - купить VIP-место на сайте\n"
        # "/buy_top_id - купить красивый ID ROFL HUB\n"
        [types.InlineKeyboardButton(text="🥩 1 кибер-котлета | ★ 7 Stars", callback_data="buy_cutlet_1")],
        [types.InlineKeyboardButton(text="🥩 5 кибер-котлет | ★ 29 Stars", callback_data="buy_cutlets_3")],
        [types.InlineKeyboardButton(text="🥩 10 кибер-котлет | ★ 49 Stars", callback_data="buy_cutlets_10")],
        [types.InlineKeyboardButton(text="🥩 50 кибер-котлет | ★ 239 Stars", callback_data="buy_cutlets_50")],
        [types.InlineKeyboardButton(text="🥩 100 кибер-котлет | ★ 449 Stars", callback_data="buy_cutlets_100")],
        [types.InlineKeyboardButton(text="📦 Холодильник на 5 котлет | ★ 49 Stars", callback_data="buy_slot_5")],
        [types.InlineKeyboardButton(text="📦 Холодильник на 10 котлет | ★ 99 Stars", callback_data="buy_slot_10")],
        [types.InlineKeyboardButton(text="📦 Холодильник на 50 котлет | ★ 499 Stars", callback_data="buy_slot_50")],
        [types.InlineKeyboardButton(text="📦 Холодильник на 100 котлет | ★ 999 Stars", callback_data="buy_slot_100")],
        [types.InlineKeyboardButton(text="💰 \"Солдат\": 1 000 монет | ★ 49 Stars", callback_data="buy_coins_1k")],
        [types.InlineKeyboardButton(text="💰 \"Капитан\": 3 000 монет | ★ 99 Stars", callback_data="buy_coins_3k")],
        [types.InlineKeyboardButton(text="💰 \"Ветеран\": 10 000 монет | ★ 299 Stars", callback_data="buy_coins_10k")],
        [types.InlineKeyboardButton(text="👑 \"Легенда\": 50 000 монет | ★ 1299 Stars", callback_data="buy_coins_50k")],
        [types.InlineKeyboardButton(text="👑 \"Генерал армии\": 100 000 монет | ★ 2499 Stars", callback_data="buy_coins_100k")],
        [types.InlineKeyboardButton(text="👑 \"Властелин империи\": 1 000 000 монет | ★ 19999 Stars", callback_data="buy_coins_1_million")],
        [types.InlineKeyboardButton(text="🚀 Boost +1 монета за победу (навсегда) | ★ 199 Stars", callback_data="buy_boost_win")],
    ])
    await message.answer(shop_text, reply_markup=keyboard, parse_mode="HTML")


# ----------------------------------------------------------------
# 💳 ПЕРЕХВАТЧИКИ КЛИКОВ (CALLBACK QUERIES)
# ----------------------------------------------------------------
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase(callback: types.CallbackQuery):
    product_type = callback.data
    invoice_text = ""  # Инициализируем пустую строку, чтобы не было NameError

    # Психологический триггер для Казны Властелин империи за ★ 19999 Stars!
    if product_type == "buy_coins_1k":
        invoice_text = (
            "💎 <b>ПАКЕТ \"СОЛДАТ\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>1000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 49 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Хороший капитал для уверенного старта в ROFL HUB и неделю дуэлей!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_coins_3k":
        invoice_text = (
            "💎 <b>ПАКЕТ \"КАПИТАН\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>3000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 99 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Пачка валюты на классные донаты в ферму и примерно один месяц дуэлей!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_coins_10k":
        invoice_text = (
            "💎 <b>ПАКЕТ \"ВЕТЕРАН\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>10 000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 299 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Большое количество монет на мощные донаты в ферму и пару месяцев дуэлей!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_coins_50k":
        invoice_text = (
            "💎 <b>ПАКЕТ \"ЛЕГЕНДА\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>50 000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 1299 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Внушительное количество монет на несколько топовых аукционов или целый год дуэлей!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_coins_100k":
        invoice_text = (
            "💎 <b>ПАКЕТ \"ГЕНЕРАЛ АРМИИ\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>100 000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 2499 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Такого огромного количества валюты тебе хватит "
            "на создание команды на 50 игроков в ROFL HUB и на другие донаты VIP-уровня! "
            "Количество команд будет ограниченное количество, постарайся собрать !</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_coins_1_million":
        invoice_text = (
            "💎 <b>ПАКЕТ \"ВЛАСТЕЛИН ИМПЕРИИ\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>1 000 000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 19999 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Этого богатства хватит на создание собственного клана на 1000 игроков в ROFL HUB! "
            "Кланов будет около 100 штук на весь мир, не упусти возможность стать знаменитостью!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )

    elif product_type == "buy_miner_junior":
        invoice_text = (
            "⚡ <b>ПОКУПКА БОТА \"МЛАДШИЙ МАЙНЕР\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>робот-майнер 1-го поколения</b>\n"
            "⚡ Скорость добычи - 2 монеты в час\n"
            "⚡ Автономность: работает без кибер-котлет 30 дней подряд!\n"
            "Срок лицензии майнера - 30 дней. Далее робот ломается из-за круглосуточной работы и отправляется на металл, "
            "но после покупки его можно починить, восстановить работоспособность "
            "и продлевать ещё на 30 дней в 2 раза дешевле от стоимости покупки всего за 19 Stars!\n"
            "💳 Стоимость покупки сейчас: <b>★ 49 Stars</b>\n"
            "..................................................\n"
            "🤖 <i>Станок начнет качать тебе монеты круглосуточно без перерыва на подзарядку!</i>"
        )

    # Психологический триггер для Премиум Бурильщика за ★ 99 Stars!
    elif product_type == "buy_miner_premium":
        invoice_text = (
            "⚡ <b>ПОКУПКА БОТА \"КИБЕР-БУРИЛЬЩИК\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>робот-майнер 2-го поколения</b>\n"
            "⚡ Скорость добычи - 5 монет в час\n"
            "⚡ Добывает больше, нужно кормить кибер-котлетой. Одна кибер-котлета выдаётся каждый день бесплатно!\n"
            "Срок лицензии майнера - 30 дней. Далее робот ломается из-за ысокой нагрузки и отправляется на металл, "
            "но после покупки его можно починить, восстановить работоспособность "
            "и продлевать ещё на 30 дней в 2 раза дешевле от стоимости покупки всего за 39 Stars!\n"
            "💳 Стоимость покупки сейчас: <b>★ 99 Stars</b>\n"
            "..................................................\n"
            "🤖 <i>Станок начнет бешенно выкачивать монеты из рудника в твой кошелёк! "
            "Не забывай кормить его кибер-котлетой, чтобы робот работал non-stop 24/7!</i>"
        )

    # Добавляем текстовые заготовки для упаковок котлет (чтобы генератор чеков не ломался)
    elif product_type == "buy_cutlet_1":
        invoice_text = "🥩 <b>1 КИБЕР-КОТЛЕТА</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_cutlets_5":
        invoice_text = "🥩 <b>ПАКЕТ \"ДАЙ ПЯТЬ\" (5 котлет)</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_cutlets_10":
        invoice_text = "🥩 <b>ПАКЕТ \"В ДЕСЯТКУ\" (10 котлет)</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_cutlets_50":
        invoice_text = "🥩 <b>ПАКЕТ \"ОЛИГАРХ МАЙНИНГА\" (50 котлет)</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_cutlets_100":
        invoice_text = "🥩 <b>СУПЕР-ПАК \"ВЛАСТЕЛИН МАЙНИНГА\" (100 котлет)</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_fridge_5":
        invoice_text = "📦 <b>ХОЛОДИЛЬНИК НА 5 КОТЛЕТ</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_fridge_10":
        invoice_text = "📦 <b>ХОЛОДИЛЬНИК НА 10 КОТЛЕТ</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_fridge_50":
        invoice_text = "📦 <b>ХОЛОДИЛЬНИК НА 50 КОТЛЕТ</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_fridge_100":
        invoice_text = "📦 <b>ХОЛОДИЛЬНИК НА 100 КОТЛЕТ</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_slot_3":
        invoice_text = "🔒 <b>ХОЛОДИЛЬНИК НА 3 КОТЛЕТЫ</b>\n\nПодготовка инвойса..."
    elif product_type == "buy_boost_win":
        invoice_text = "🚀 <b>БУСТ (+1 МОНЕТА ЗА ПОБЕДУ)</b>\n\nПодготовка инвойса..."

    # ----------------------------------------------------------------
    # 💰 ВОТ СЮДА ОН И ВСТАЛ! АВТОМАТИЧЕСКИЙ РАСЧЕТ И ОТПРАВКА ИНВОЙСА
    # ----------------------------------------------------------------
    # Словарь, где ключ — твой callback_data, а значение — реальная цена в Stars (XTR)
    stars_prices = {
        "buy_coins_1k": 49,
        "buy_coins_3k": 99,
        "buy_coins_10k": 299,
        "buy_coins_50k": 1299,
        "buy_coins_100k": 2499,
        "buy_coins_1_million": 19999,
        "buy_miner_junior": 49,
        "buy_miner_premium": 99,
        "buy_cutlet_1": 7,
        "buy_cutlets_5": 29,
        "buy_cutlets_10": 49,
        "buy_cutlets_50": 239,
        "buy_cutlets_100": 449,
        "buy_fridge_5": 49,
        "buy_fridge_10": 99,
        "buy_fridge_50": 499,
        "buy_fridge_100": 999,
        "buy_boost_win": 199
    }

    # Обязательно гасим системные часики на кнопке телефона ребенка
    await callback.answer()

    # Если товар есть в нашей тарифной сетке — выставляем официальный счет
    if product_type in stars_prices:
        price_in_stars = stars_prices[product_type]

        # Очищаем название лота от лишних префиксов для красивого отображения в чеке
        clean_title = invoice_text.split("<b>")[1].split("</b>")[0] if "<b>" in invoice_text else "Товар ROFL HUB"

        # 🚀 СНАЙПЕРСКИЙ ДЕСАНТ ИНВОЙСА В ЧАТ ЮЗЕРА
        await callback.message.answer_invoice(
            title=clean_title,
            description="Безопасная покупка через шлюз Telegram Stars. Товар будет мгновенно зачислен на твой ID в облаке Railway.",
            payload=product_type,  # Этот скрытый маркер прилетит в pre_checkout_query после оплаты
            provider_token="",  # Для Telegram Stars (XTR) токен провайдера ВСЕГДА оставляется ПУСТЫМ!
            currency="XTR",  # Жесткая международная валюта Звезд
            prices=[types.LabeledPrice(label=clean_title, amount=price_in_stars)],
            start_parameter="rofl_hub_shop"
        )
    else:
        # Резервный технический текст, если что-то пошло не так
        if not invoice_text:
            invoice_text = f"⚙️ Модуль оплаты товара [{product_type}] вызван успешно!\nШлюз готовится к приему транзакции."
        await callback.message.answer(invoice_text, parse_mode="HTML")
