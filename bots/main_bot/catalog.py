import logging

logger = logging.getLogger(__name__)


def calculate_stars_order(payload: str, current_capacity: int, current_boost: int) -> dict:
    """
    Единый бэкенд-каталог цен и тарифов холдинга ROFL HUB CORE.
    Очищен от розничного мусора, мелких паков и сложных бустов.
    """
    cleaned_payload = payload.replace("buy_", "")

    # 1. Линейка роботов-майнеров (Жесткий лимит жизни на 30 дней)
    if cleaned_payload == "miner_junior":
        return {"type": "miner", "kind": "junior", "stars": 49, "title": "🤖 Робот: Младший Майнер (Срок: 30 дней)"}
    elif cleaned_payload == "miner_premium":
        return {"type": "miner", "kind": "premium", "stars": 99, "title": "⚡ Робот: Кибер Бурильщик (Срок: 30 дней)"}

    # 2. Ресурсы: Крупные оптовые паки кибер-котлет на склад инвентаря
    elif cleaned_payload == "cutlet_10":
        return {"type": "cutlets", "qty": 10, "stars": 49, "title": "🥩 10 котлет на склад"}
    elif cleaned_payload == "cutlet_50":
        return {"type": "cutlets", "qty": 50, "stars": 239, "title": "🥩 50 котлет на склад"}
    elif cleaned_payload == "cutlet_100":
        return {"type": "cutlets", "qty": 100, "stars": 449, "title": "🥩 100 котлет на склад"}

    # 3. Прогрессивные улучшения Холодильника (Синхронизировано с паками котлет)
    elif cleaned_payload.startswith("fridge_"):
        target_capacity = int(cleaned_payload.split("_")[-1])
        if target_capacity <= current_capacity:
            raise ValueError("У тебя уже активирован холодильник равного или большего объема!")

        prices = {10: 99, 50: 499, 100: 999}
        stars_cost = prices.get(target_capacity, 999)
        return {"type": "fridge_upgrade", "capacity": target_capacity, "stars": stars_cost,
                "title": f"📦 Апгрейд Холодильника до уровня {target_capacity}"}

    # 4. Высокодоходные математические бусты фермы (Сгораемые, на 30 дней)
    elif cleaned_payload == "boost_nitrogen_30":
        return {"type": "farm_boost", "kind": "nitrogen", "stars": 299,
                "title": "❄️ Азотное охлаждение роботов: +40% к добыче всей фермы (На 30 дней)"}
    elif cleaned_payload == "boost_nuclear_30":
        return {"type": "farm_boost", "kind": "nuclear", "stars": 199,
                "title": "🔋 +500% к скорости добычи Кибер Бурильщика (На 30 дней)"}

    # 5. Снятие суточных лимитов на гейминг и викторины (15/15/30 побед)
    elif cleaned_payload == "unlimit_24h":
        return {"type": "game_unlimit", "kind": "day", "stars": 5, "title": "⚡ Безлимитный гейминг: 24 часа"}
    elif cleaned_payload == "unlimit_30d":
        return {"type": "game_unlimit", "kind": "month", "stars": 99, "title": "🚀 Безлимитный гейминг: 30 дней"}

    # 6. Специальный VIP-персонаж: Дрон-Ремонтник (Авторемонт всех роботов на 1 год)
    elif cleaned_payload == "repair_drone_365":
        return {"type": "vip_character", "kind": "drone", "stars": 999,
                "title": "🤖 VIP Дрон-Ремонтник (Лицензия: 1 год)"}

    # 7. Оптовая казна монет (Крупные паки рофлов для входа в дуэли и кланы)
    elif cleaned_payload == "coins_5k":
        return {"type": "coins", "coins_amount": 5000, "stars": 149, "title": "💰 Пак «Сержант»: +5 000 рофлов"}
    elif cleaned_payload == "coins_10k":
        return {"type": "coins", "coins_amount": 10000, "stars": 299, "title": "💰 Пак «Ветеран»: +10 000 рофлов"}
    elif cleaned_payload == "coins_50k":
        return {"type": "coins", "coins_amount": 50000, "stars": 1299, "title": "👑 Пак «Генерал»: +50 000 рофлов"}
    elif cleaned_payload == "coins_100k":
        return {"type": "coins", "coins_amount": 100000, "stars": 2499, "title": "👑 Пак «Легенда»: +100 000 рофлов"}

    # 8. Специальные ультимативные предложения холдинга
    elif cleaned_payload == "clan_upgrade":
        return {"type": "clan_upgrade", "stars": 2499, "title": "🏆 Лицензия Мега-Клана (до 1000 мест)"}

    else:
        raise ValueError(f"Неизвестный тип товара в каталоге: {payload}")
