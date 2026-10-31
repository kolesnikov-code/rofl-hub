"""
Каталог магазина ROFL HUB: 19 позиций, две категории (ферма / игровые).

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
# title/button — русская витрина, title_en/button_en — английская (locales ru/en)
CATALOG: dict[str, dict] = {
    # --- Роботы (лицензия 30 дней) ---
    "miner_junior": {"type": "miner", "kind": "junior", "stars": 49, "category": CATEGORY_FARM,
                     "title": "🤖 Младший Майнер (30 дней)", "button": "🤖 Младший Майнер | 49 ★",
                     "title_en": "🤖 Miner Bot (30 days)", "button_en": "🤖 Miner Bot | 49 ★"},
    "miner_premium": {"type": "miner", "kind": "premium", "stars": 99, "category": CATEGORY_FARM,
                      "title": "⚡ Кибер-Бурильщик (30 дней)", "button": "⚡ Кибер-Бурильщик | 99 ★",
                      "title_en": "⚡ Cyber-Driller (30 days)", "button_en": "⚡ Cyber-Driller | 99 ★"},
    # --- Котлеты на склад ---
    "cutlet_10": {"type": "cutlets", "qty": 10, "stars": 49, "category": CATEGORY_FARM,
                  "title": "🥩 Пак котлет: 10 шт.", "button": "🥩 Пак котлет (10) | 49 ★",
                  "title_en": "🥩 Cutlet pack: 10 pcs", "button_en": "🥩 Cutlet pack (10) | 49 ★"},
    "cutlet_50": {"type": "cutlets", "qty": 50, "stars": 239, "category": CATEGORY_FARM,
                  "title": "🥩 Запас котлет: 50 шт.", "button": "🥩 Запас котлет (50) | 239 ★",
                  "title_en": "🥩 Cutlet stock: 50 pcs", "button_en": "🥩 Cutlet stock (50) | 239 ★"},
    "cutlet_100": {"type": "cutlets", "qty": 100, "stars": 449, "category": CATEGORY_FARM,
                   "title": "🥩 Пром. пак котлет: 100 шт.", "button": "🥩 Пром. пак (100) | 449 ★",
                   "title_en": "🥩 Industrial pack: 100 pcs", "button_en": "🥩 Industrial pack (100) | 449 ★"},
    # --- Холодильник ---
    "fridge_10": {"type": "fridge_upgrade", "capacity": 10, "stars": 99, "category": CATEGORY_FARM,
                  "title": "📦 Холодильник на 10 котлет", "button": "📦 Холодильник 10 | 99 ★",
                  "title_en": "📦 Fridge for 10 cutlets", "button_en": "📦 Fridge 10 | 99 ★"},
    "fridge_50": {"type": "fridge_upgrade", "capacity": 50, "stars": 499, "category": CATEGORY_FARM,
                  "title": "📦 Холодильник на 50 котлет", "button": "📦 Холодильник 50 | 499 ★",
                  "title_en": "📦 Fridge for 50 cutlets", "button_en": "📦 Fridge 50 | 499 ★"},
    "fridge_100": {"type": "fridge_upgrade", "capacity": 100, "stars": 999, "category": CATEGORY_FARM,
                   "title": "📦 Холодильник на 100 котлет", "button": "📦 Холодильник 100 | 999 ★",
                   "title_en": "📦 Fridge for 100 cutlets", "button_en": "📦 Fridge 100 | 999 ★"},
    # --- Бусты фермы (30 дней) ---
    "boost_nuclear_30": {"type": "farm_boost", "kind": "nuclear", "days": BOOST_DAYS, "stars": 199,
                         "category": CATEGORY_FARM,
                         "title": "🔋 Ядерный Разгон x5 (30 дней)", "button": "🔋 Ядерный Разгон x5 | 199 ★",
                         "title_en": "🔋 Nuclear Boost x5 (30 days)", "button_en": "🔋 Nuclear Boost x5 | 199 ★"},
    "boost_nitrogen_30": {"type": "farm_boost", "kind": "nitrogen", "days": BOOST_DAYS, "stars": 299,
                          "category": CATEGORY_FARM,
                          "title": "❄️ Азотное Охлаждение +40% (30 дней)",
                          "button": "❄️ Азотное Охлаждение +40% | 299 ★",
                          "title_en": "❄️ Nitrogen Cooling +40% (30 days)",
                          "button_en": "❄️ Nitrogen Cooling +40% | 299 ★"},
    # --- Апгрейд Робота-Стажёра до ВЕЧНОГО Младшего Майнера (условие: 3 квалифицированных друга) ---
    "intern_upgrade": {"type": "intern_upgrade", "stars": 999, "category": CATEGORY_FARM,
                       "title": "♾ Вечный Майнер: апгрейд Робота-Стажёра", "button": "♾ Вечный Майнер | 999 ★",
                       "title_en": "♾ Eternal Miner: upgrade your Intern Bot",
                       "button_en": "♾ Eternal Miner | 999 ★"},
    # --- Мастер-дрон ---
    "repair_drone_365": {"type": "vip_character", "kind": "drone", "days": DRONE_DAYS, "stars": 999,
                         "category": CATEGORY_FARM,
                         "title": "🛸 Мастер-дрон: авторемонт на 1 год", "button": "🛸 Мастер-дрон (1 год) | 999 ★",
                         "title_en": "🛸 Master Drone: auto-repair for 1 year",
                         "button_en": "🛸 Master Drone (1 year) | 999 ★"},
    # --- Игровой безлимит ---
    "unlimit_24h": {"type": "game_unlimit", "hours": UNLIMIT_DAY_HOURS, "stars": 15, "category": CATEGORY_GAMES,
                    "title": "⚡ Безлимит на 24 часа", "button": "⚡ Безлимит 24 ч | 15 ★",
                    "title_en": "⚡ Remove limits for 24 hours", "button_en": "⚡ Unlimited 24h | 15 ★"},
    "unlimit_30d": {"type": "game_unlimit", "hours": UNLIMIT_MONTH_DAYS * 24, "stars": 249,
                    "category": CATEGORY_GAMES,
                    "title": "🚀 Безлимит на 30 дней", "button": "🚀 Безлимит 30 дней | 249 ★",
                    "title_en": "🚀 Unlimited gaming for 30 days", "button_en": "🚀 Unlimited 30 days | 249 ★"},
    # --- Казна монет ---
    "coins_5k": {"type": "coins", "coins_amount": 5_000, "stars": 149, "category": CATEGORY_GAMES,
                 "title": "💰 Пак «Сержант»: 5 000 🪙", "button": "💰 5 000 🪙 | 149 ★",
                 "title_en": "💰 “Sergeant” pack: 5,000 coins", "button_en": "💰 5,000 🪙 | 149 ★"},
    "coins_10k": {"type": "coins", "coins_amount": 10_000, "stars": 299, "category": CATEGORY_GAMES,
                  "title": "💰 Пак «Ветеран»: 10 000 🪙", "button": "💰 10 000 🪙 | 299 ★",
                  "title_en": "💰 “Veteran” pack: 10,000 coins", "button_en": "💰 10,000 🪙 | 299 ★"},
    "coins_50k": {"type": "coins", "coins_amount": 50_000, "stars": 1299, "category": CATEGORY_GAMES,
                  "title": "👑 Пак «Генерал»: 50 000 🪙", "button": "👑 50 000 🪙 | 1299 ★",
                  "title_en": "👑 “General” pack: 50,000 coins", "button_en": "👑 50,000 🪙 | 1299 ★"},
    "coins_100k": {"type": "coins", "coins_amount": 100_000, "stars": 2499, "category": CATEGORY_GAMES,
                   "title": "👑 Пак «Легенда»: 100 000 🪙", "button": "👑 100 000 🪙 | 2499 ★",
                   "title_en": "👑 “Legend” pack: 100,000 coins", "button_en": "👑 100,000 🪙 | 2499 ★"},
    # --- Мега-клан ---
    "clan_upgrade": {"type": "clan_upgrade", "max_members": MEGA_CLAN_MAX_MEMBERS, "stars": 2499,
                     "category": CATEGORY_GAMES,
                     "title": "🏆 Лицензия Мега-Клана (до 1000 мест)", "button": "🏆 Мега-Клан (1000 мест) | 2499 ★",
                     "title_en": "🏆 Mega-Clan license (up to 1000 seats)",
                     "button_en": "🏆 Mega-Clan (1000 seats) | 2499 ★"},
}


def item_title(item: dict, lang: str = "ru") -> str:
    """Каталог локализован ru/en: все не-русские языки видят английскую витрину."""
    return item["title_en"] if lang != "ru" and item.get("title_en") else item["title"]


def item_button(item: dict, lang: str = "ru") -> str:
    return item["button_en"] if lang != "ru" and item.get("button_en") else item["button"]

# Порядок кнопок на витрине. СТРОГО по одной кнопке в ряд (решение владельца 13.10:
# две кнопки в ряду обрезают текст с ценой на телефонах — игроки боятся нажимать).
SHOP_LAYOUT: dict[str, list[list[str]]] = {
    CATEGORY_FARM: [
        ["miner_junior"],
        ["miner_premium"],
        ["cutlet_10"],
        ["cutlet_50"],
        ["cutlet_100"],
        ["fridge_10"],
        ["fridge_50"],
        ["fridge_100"],
        ["boost_nuclear_30"],
        ["boost_nitrogen_30"],
        ["repair_drone_365"],
        ["intern_upgrade"],
    ],
    CATEGORY_GAMES: [
        ["unlimit_24h"],
        ["unlimit_30d"],
        ["coins_5k"],
        ["coins_10k"],
        ["coins_50k"],
        ["coins_100k"],
        ["clan_upgrade"],
    ],
}


# «Что даёт каждый товар» — карточка рядом с витриной в приложении (те же тексты, что в FAQ).
# Как и весь каталог, ru/en: остальные языки видят английский вариант.
SHOP_INFO: list[dict[str, str]] = [
    {"cat": "farm", "title": "🤖 Младший Майнер · 49 ★ · 30 дней",
     "text": "Добывает 5 🪙 в час без топлива — около 3 600 🪙 за месяц. Для тех, кто не хочет следить за заправкой.",
     "title_en": "🤖 Miner Bot · 49 ★ · 30 days",
     "text_en": "Mines 5 🪙 per hour with no fuel — about 3,600 🪙 a month. For those who don't want to refuel."},
    {"cat": "farm", "title": "⚡ Кибер-Бурильщик · 99 ★ · 30 дней",
     "text": "10 🪙 в час — вдвое мощнее Майнера, но съедает 1 котлету в сутки. С бустами — до 70 🪙 в час.",
     "title_en": "⚡ Cyber-Driller · 99 ★ · 30 days",
     "text_en": "10 🪙 per hour — twice the Miner, but eats 1 cutlet a day. With boosts — up to 70 🪙 per hour."},
    {"cat": "farm", "title": "🥩 Паки котлет · 10 / 50 / 100 шт.",
     "text": "Топливо Бурильщиков: 1 котлета = сутки работы одного робота. Чем больше пак, тем дешевле котлета.",
     "title_en": "🥩 Cutlet packs · 10 / 50 / 100 pcs",
     "text_en": "Driller fuel: 1 cutlet = one robot working for a day. The bigger the pack, the cheaper each cutlet."},
    {"cat": "farm", "title": "📦 Холодильник · на 10 / 50 / 100 котлет",
     "text": "Бак, из которого Бурильщики заправляются сами: загрузил котлеты — и ферма работает без тебя.",
     "title_en": "📦 Fridge · for 10 / 50 / 100 cutlets",
     "text_en": "A tank the Drillers refuel from on their own: load cutlets and the farm runs without you."},
    {"cat": "farm", "title": "🔋 Ядерный Разгон x5 · 199 ★ · 30 дней",
     "text": "Добыча всех роботов ×5, но Бурильщики едят в 3 раза больше котлет. Самый быстрый путь к большим суммам.",
     "title_en": "🔋 Nuclear Boost x5 · 199 ★ · 30 days",
     "text_en": "All robots mine ×5, but Drillers eat 3× more cutlets. The fastest way to big numbers."},
    {"cat": "farm", "title": "❄️ Азотное Охлаждение +40% · 299 ★ · 30 дней",
     "text": "+40% к добыче всех роботов без лишнего топлива. Складывается с Ядерным Разгоном.",
     "title_en": "❄️ Nitrogen Cooling +40% · 299 ★ · 30 days",
     "text_en": "+40% to every robot's output with no extra fuel. Stacks with the Nuclear Boost."},
    {"cat": "farm", "title": "🛸 Мастер-дрон · 999 ★ · 1 год",
     "text": "Пока дрон активен, роботы не стареют: их 30-дневная лицензия замирает.",
     "title_en": "🛸 Master Drone · 999 ★ · 1 year",
     "text_en": "While the drone is active, robots don't age: their 30-day license is frozen."},
    {"cat": "farm", "title": "♾ Вечный Майнер · 999 ★",
     "text": "Превращает бесплатного Робота-Стажёра в вечного Младшего Майнера: 5 🪙 в час навсегда. Нужно 3 активных друга.",
     "title_en": "♾ Eternal Miner · 999 ★",
     "text_en": "Turns your free Intern Bot into an eternal Miner Bot: 5 🪙 per hour forever. Needs 3 active friends."},
    {"cat": "games", "title": "⚡ Безлимит · 24 ч за 15 ★ / 30 дней за 249 ★",
     "text": "Снимает суточный лимит побед: каждая победа приносит монеты и ресурс игры без ограничений. "
             "Безлимит на 30 дней ещё и удваивает опыт пропуска сезона за игры: до 300 в сутки вместо 150.",
     "title_en": "⚡ Unlimited · 24h for 15 ★ / 30 days for 249 ★",
     "text_en": "Removes the daily win limit: every win brings coins and the game's resource without caps. "
                "The 30-day pass also doubles season-pass XP from games: up to 300 a day instead of 150."},
    {"cat": "games", "title": "💰 Паки монет · 5 000 – 100 000 🪙",
     "text": "Монеты сразу на баланс: дуэли с большими ставками, биржа, своя команда, Шаттл. Чем больше пак, тем выгоднее курс.",
     "title_en": "💰 Coin packs · 5,000 – 100,000 🪙",
     "text_en": "Coins straight to your balance: high-stake duels, the market, your own team, the Shuttle. Bigger pack — better rate."},
    {"cat": "games", "title": "🏆 Мега-Клан · 2499 ★",
     "text": "Расширяет команду до 1000 мест: больше бойцов в битвах и быстрее растёт станция команды. Покупает капитан команды (отряд сначала расширяется до команды за монеты).",
     "title_en": "🏆 Mega-Clan · 2499 ★",
     "text_en": "Expands your team to 1000 seats: more fighters in battles and a faster-growing team station. Bought by the team captain (a squad first expands into a team for coins)."},
]


def shop_info(lang: str = "ru") -> list[dict[str, str]]:
    en = lang != "ru"
    return [{"cat": i["cat"], "title": i["title_en"] if en else i["title"], "text": i["text_en"] if en else i["text"]}
            for i in SHOP_INFO]


class CatalogError(ValueError):
    """Ошибка валидации заказа (неизвестный товар, недопустимая покупка)."""


def normalize_sku(payload: str) -> str:
    """'buy_cutlet_10' → 'cutlet_10'; 'cutlet_10:49' → 'cutlet_10'."""
    sku = payload.split(":", 1)[0]
    if sku.startswith("buy_"):
        sku = sku[4:]
    return sku


def skin_item(sku: str) -> dict | None:
    """✨ Скины продаются вне витрины CATALOG (Магазин → «✨ Скины»): skin_<id> → заказ, пока скин в продаже."""
    from shared.economy import utcnow
    from shared.skins import SKINS, for_sale, skin_name
    sid = sku[5:] if sku.startswith("skin_") else None
    if sid not in SKINS:
        return None
    if not for_sale(sid, utcnow()):
        raise CatalogError("Этот скин больше не продаётся.")
    s = SKINS[sid]
    return {"sku": sku, "type": "skin", "skin": sid, "stars": s["stars"], "category": CATEGORY_GAMES,
            "title": "✨ " + skin_name(sid, "ru"), "title_en": "✨ " + skin_name(sid, "en"),
            "button": f"✨ {skin_name(sid, 'ru')} | {s['stars']} ★", "button_en": f"✨ {skin_name(sid, 'en')} | {s['stars']} ★"}


def pass_item(sku: str) -> dict | None:
    """🎟 Пропуск сезона: seasonpass_ГГГГММ — текущего месяца или (в последнюю неделю) следующего."""
    from shared.economy import utcnow
    from shared.season_pass import PASS_STARS, can_buy, season_of_sku
    season = season_of_sku(sku)
    if season is None:
        return None
    if not can_buy(season, utcnow()):
        raise CatalogError("Этот пропуск сейчас не продаётся.")
    label = f"{season[5:7]}.{season[:4]}"
    return {"sku": sku, "type": "season_pass", "season": season, "stars": PASS_STARS, "category": CATEGORY_GAMES,
            "title": f"🎟 Пропуск сезона {label}", "title_en": f"🎟 Season pass {label}",
            "button": f"🎟 Пропуск сезона | {PASS_STARS} ★", "button_en": f"🎟 Season pass | {PASS_STARS} ★"}


def get_item(sku: str) -> dict:
    item = CATALOG.get(sku)
    if item is None:
        skin = skin_item(sku) or pass_item(sku)
        if skin is not None:
            return skin
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
