import logging

logger = logging.getLogger(__name__)

# ============================================================================
# 🎰 ГЛOБАЛЬНЫЙ РЕЕСТР ЦЕН И КОНТЕНТА ТОВАРОВ STARS (XTR) — ROFL HUB CORE
# ============================================================================
# Цены и метаданные жестко заперты на сервере. Подделать payload из кнопок нереально!

# 1. ТOПЛИВНЫЕ РЕСУРСЫ: Котлеты (Строго по кнопкам со скрина)
CUTLET_PACKS = {
    "buy_cutlet_1": {"stars": 7, "qty": 1, "title": "🥩 1 кибер-котлета"},
    "buy_cutlet_5": {"stars": 29, "qty": 5, "title": "🥩 5 кибер-котлет"},
    "buy_cutlet_10": {"stars": 49, "qty": 10, "title": "🥩 10 кибер-котлет"},
    "buy_cutlet_50": {"stars": 239, "qty": 50, "title": "🥩 50 кибер-котлет"},
    "buy_cutlet_100": {"stars": 449, "qty": 100, "title": "🥩 100 кибер-котлет"},
}

# 2. АПГРЕЙДЫ ЦЕНТРАЛЬНОГО ХОЛОДИЛЬНИКА (Только вверх)
FRIDGE_UPGRADES = {
    "buy_fridge_5": {"stars": 49, "capacity": 5, "title": "📦 Холодильник на 5 котлет"},
    "buy_fridge_10": {"stars": 99, "capacity": 10, "title": "📦 Холодильник на 10 котлет"},
    "buy_fridge_50": {"stars": 499, "capacity": 50, "title": "📦 Холодильник на 50 котлет"},
    "buy_fridge_100": {"stars": 999, "capacity": 100, "title": "👑 Холодильник на 100 котлет"},
}

# 3. АВТОМАТИЗАЦИЯ И ФЕРМА: Роботы-майнеры
MINER_EQUIPMENT = {
    "buy_miner_junior": {"stars": 49, "kind": "junior", "title": "🤖 Робот «Младший Майнер»"},
    "buy_miner_premium": {"stars": 99, "kind": "premium", "title": "⚡ Робот «Кибер Бурильщик»"},
}

# 4. РОЗНИЧНАЯ КАЗНА: Пакеты игровых монет (Формируют Floor Price для рынка)
COIN_PACKS = {
    "buy_coins_1k": {"stars": 49, "coins": 1000, "title": "💰 «Солдат»: 1 000 монет"},
    "buy_coins_3k": {"stars": 99, "coins": 3000, "title": "💰 «Капитан»: 3 000 монет"},
    "buy_coins_10k": {"stars": 299, "coins": 10000, "title": "💰 «Ветеран»: 10 000 монет"},
    "buy_coins_50k": {"stars": 1299, "coins": 50000, "title": "👑 «Легенда»: 50 000 монет"},
    "buy_coins_100k": {"stars": 2499, "coins": 100000, "title": "👑 «Генерал армии»: 100 000 монет"},
    "buy_coins_1m": {"stars": 19999, "coins": 1000000, "title": "👑 «Властелин империи»: 1 000 000 монет"},
}


# ============================================================================
# ⚙️ ЕДИНЫЙ ЦЕНТРАЛЬНЫЙ ВAЛИДАТOР И КAЛЬКУЛЯТOР ЗАКАЗOВ
# ============================================================================
def calculate_stars_order(payload: str, current_fridge_capacity: int, current_boost_level: int) -> dict:
    """
    Принимает payload клика, текущую вместимость хаба и уровень буста игрока из PostgreSQL.
    Возвращает полный срез параметров товара для инвойса Stars.
    Выбрасывает ValueError при любых попытках обхода ограничений (чит-запросы).
    """
    # 1. Обработка паков котлет
    if payload in CUTLET_PACKS:
        item = CUTLET_PACKS[payload]
        return {"stars": item["stars"], "title": item["title"], "type": "cutlets", "qty": item["qty"]}

    # 2. Обработка закупки роботов-майнеров
    if payload in MINER_EQUIPMENT:
        item = MINER_EQUIPMENT[payload]
        return {"stars": item["stars"], "title": item["title"], "type": "miner", "kind": item["kind"]}

    # 3. Обработка улучшения холодильника (С защитой «Только вверх!»)
    if payload in FRIDGE_UPGRADES:
        item = FRIDGE_UPGRADES[payload]
        target_capacity = item["capacity"]

        if target_capacity <= current_fridge_capacity:
            raise ValueError(
                f"🚨 Читерский запрос! Попытка даунгрейда хаба с {current_fridge_capacity} до {target_capacity}."
            )
        return {"stars": item["stars"], "title": item["title"], "type": "fridge_upgrade", "capacity": target_capacity}

    # 4. Обработка пакетов розничной монетарной казны
    if payload in COIN_PACKS:
        item = COIN_PACKS[payload]
        return {"stars": item["stars"], "title": item["title"], "type": "coins", "coins_amount": item["coins"]}

    # 5. 🔥 БОЕВОЙ БУСТ ПОБЕДЫ: ТРИ УРОВНЯ НА ОДНИ РУКИ НАВСЕГДА!
    if payload == "buy_boost_upgrade":
        if current_boost_level >= 3:
            raise ValueError("🚨 Лимит достигнут! У игрока уже активирован максимальный уровень буста.")

        next_level = current_boost_level + 1

        # Динамическая прогрессивная тарифная сетка Анатолия Алексеевича
        if next_level == 1:
            stars_price = 99
            title = "🚀 Боевой Буст +1 монета за победу"
        elif next_level == 2:
            stars_price = 199
            title = "🚀🚀 Боевой Буст +2 монеты за победу"
        else:
            stars_price = 299
            title = "👑👑👑 Ультимативный Буст +3 монеты за победу"

        return {"stars": stars_price, "title": title, "type": "boost_upgrade", "next_level": next_level}

    # 6. КОМБО-БАНДЛ «VIP-СТАРТ» (Робот в подарок при покупке 30 котлет)
    if payload == "buy_vip_start_bundle":
        return {"stars": 149, "title": "👑 Элитарный Бандл «VIP-Старт»", "type": "vip_bundle"}

    raise ValueError(f"🚨 Ошибка каталога: Товар с payload '{payload}' не зарегистрирован в системе.")
