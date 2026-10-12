"""
Каталог магазина ROFL HUB: 18 позиций, две категории (ферма / игровые).

Это ДАННЫЕ, а не код: витрина, инвойс и доставка читают один и тот же словарь.
Ключ словаря = SKU = callback_data кнопки без префикса «buy_».
"""
from __future__ import annotations

from shared.economy import (
    BOOST_DAYS,
    DRONE_DAYS,
    MEGA_CLAN_MAX_MEMBERS,
    UNLIMIT_DAY_HOURS,
    UNLIMIT_MONTH_DAYS,
)

CATEGORY_FARM = "farm"
CATEGORY_GAMES = "games"

# type → как доставлять (см. shared/delivery.py)
CATALOG: dict[str, dict] = {
    # --- Роботы (лицензия 30 дней) ---
    "miner_junior": {"type": "miner", "kind": "junior", "stars": 49, "category": CATEGORY_FARM,
                     "title": "🤖 Младший Майнер (30 дней)", "button": "🤖 Младший Майнер | 49 ★"},
    "miner_premium": {"type": "miner", "kind": "premium", "stars": 99, "category": CATEGORY_FARM,
                      "title": "⚡ Кибер-Бурильщик (30 дней)", "button": "⚡ Кибер-Бурильщик | 99 ★"},
    # --- Котлеты на склад ---
    "cutlet_10": {"type": "cutlets", "qty": 10, "stars": 49, "category": CATEGORY_FARM,
                  "title": "🥩 Пак котлет: 10 шт.", "button": "🥩 Пак котлет (10) | 49 ★"},
    "cutlet_50": {"type": "cutlets", "qty": 50, "stars": 239, "category": CATEGORY_FARM,
                  "title": "🥩 Запас котлет: 50 шт.", "button": "🥩 Запас котлет (50) | 239 ★"},
    "cutlet_100": {"type": "cutlets", "qty": 100, "stars": 449, "category": CATEGORY_FARM,
                   "title": "🥩 Пром. пак котлет: 100 шт.", "button": "🥩 Пром. пак (100) | 449 ★"},
    # --- Холодильник ---
    "fridge_10": {"type": "fridge_upgrade", "capacity": 10, "stars": 99, "category": CATEGORY_FARM,
                  "title": "📦 Холодильник на 10 котлет", "button": "📦 Холодильник 10 | 99 ★"},
    "fridge_50": {"type": "fridge_upgrade", "capacity": 50, "stars": 499, "category": CATEGORY_FARM,
                  "title": "📦 Холодильник на 50 котлет", "button": "📦 Холодильник 50 | 499 ★"},
    "fridge_100": {"type": "fridge_upgrade", "capacity": 100, "stars": 999, "category": CATEGORY_FARM,
                   "title": "📦 Холодильник на 100 котлет", "button": "📦 Холодильник 100 | 999 ★"},
    # --- Бусты фермы (30 дней) ---
    "boost_nuclear_30": {"type": "farm_boost", "kind": "nuclear", "days": BOOST_DAYS, "stars": 199,
                         "category": CATEGORY_FARM,
                         "title": "🔋 Ядерный Разгон x5 (30 дней)", "button": "🔋 Ядерный Разгон x5 | 199 ★"},
    "boost_nitrogen_30": {"type": "farm_boost", "kind": "nitrogen", "days": BOOST_DAYS, "stars": 299,
                          "category": CATEGORY_FARM,
                          "title": "❄️ Азотное Охлаждение +40% (30 дней)",
                          "button": "❄️ Азотное Охлаждение +40% | 299 ★"},
    # --- Мастер-дрон ---
    "repair_drone_365": {"type": "vip_character", "kind": "drone", "days": DRONE_DAYS, "stars": 999,
                         "category": CATEGORY_FARM,
                         "title": "🛸 Мастер-дрон: авторемонт на 1 год", "button": "🛸 Мастер-дрон (1 год) | 999 ★"},
    # --- Игровой безлимит ---
    "unlimit_24h": {"type": "game_unlimit", "hours": UNLIMIT_DAY_HOURS, "stars": 5, "category": CATEGORY_GAMES,
                    "title": "⚡ Снятие лимитов на 24 часа", "button": "⚡ Безлимит 24 ч | 5 ★"},
    "unlimit_30d": {"type": "game_unlimit", "hours": UNLIMIT_MONTH_DAYS * 24, "stars": 99,
                    "category": CATEGORY_GAMES,
                    "title": "🚀 Безлимитный гейминг на 30 дней", "button": "🚀 Безлимит 30 дней | 99 ★"},
    # --- Казна рофлов ---
    "coins_5k": {"type": "coins", "coins_amount": 5_000, "stars": 149, "category": CATEGORY_GAMES,
                 "title": "💰 Пак «Сержант»: 5 000 рофлов", "button": "💰 5 000 рофлов | 149 ★"},
    "coins_10k": {"type": "coins", "coins_amount": 10_000, "stars": 299, "category": CATEGORY_GAMES,
                  "title": "💰 Пак «Ветеран»: 10 000 рофлов", "button": "💰 10 000 рофлов | 299 ★"},
    "coins_50k": {"type": "coins", "coins_amount": 50_000, "stars": 1299, "category": CATEGORY_GAMES,
                  "title": "👑 Пак «Генерал»: 50 000 рофлов", "button": "👑 50 000 рофлов | 1299 ★"},
    "coins_100k": {"type": "coins", "coins_amount": 100_000, "stars": 2499, "category": CATEGORY_GAMES,
                   "title": "👑 Пак «Легенда»: 100 000 рофлов", "button": "👑 100 000 рофлов | 2499 ★"},
    # --- Мега-клан ---
    "clan_upgrade": {"type": "clan_upgrade", "max_members": MEGA_CLAN_MAX_MEMBERS, "stars": 2499,
                     "category": CATEGORY_GAMES,
                     "title": "🏆 Лицензия Мега-Клана (до 1000 мест)", "button": "🏆 Мега-Клан (1000 мест) | 2499 ★"},
}

# Порядок кнопок на витрине (ряды по 1–2 кнопки)
SHOP_LAYOUT: dict[str, list[list[str]]] = {
    CATEGORY_FARM: [
        ["miner_junior", "miner_premium"],
        ["cutlet_10"],
        ["cutlet_50", "cutlet_100"],
        ["fridge_10"],
        ["fridge_50", "fridge_100"],
        ["boost_nuclear_30", "boost_nitrogen_30"],
        ["repair_drone_365"],
    ],
    CATEGORY_GAMES: [
        ["unlimit_24h", "unlimit_30d"],
        ["coins_5k", "coins_10k"],
        ["coins_50k", "coins_100k"],
        ["clan_upgrade"],
    ],
}


class CatalogError(ValueError):
    """Ошибка валидации заказа (неизвестный товар, недопустимая покупка)."""


def normalize_sku(payload: str) -> str:
    """'buy_cutlet_10' → 'cutlet_10'; 'cutlet_10:49' → 'cutlet_10'."""
    sku = payload.split(":", 1)[0]
    if sku.startswith("buy_"):
        sku = sku[4:]
    return sku


def get_item(sku: str) -> dict:
    item = CATALOG.get(sku)
    if item is None:
        raise CatalogError(f"Неизвестный товар: {sku}")
    return {"sku": sku, **item}


def build_order(payload: str, *, current_capacity: int = 1) -> dict:
    """
    Валидирует покупку и возвращает заказ для инвойса и доставки.
    Единственное правило, зависящее от состояния игрока: нельзя купить
    холодильник не больше текущего.
    """
    sku = normalize_sku(payload)
    item = get_item(sku)
    if item["type"] == "fridge_upgrade" and item["capacity"] <= current_capacity:
        raise CatalogError("У тебя уже холодильник такого или большего объёма!")
    return item


# Обратная совместимость со старым именем
def calculate_stars_order(payload: str, current_capacity: int, current_boost: int = 0) -> dict:
    return build_order(payload, current_capacity=current_capacity)
