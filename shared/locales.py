"""
Локализация ROFL HUB: ru + en на старте (решение владельца 13.10.2026).

Правила:
- t(lang, key, **kwargs) — единственная точка получения текста; ru — эталон,
  отсутствующий en-ключ тихо падает обратно на ru (тест следит, чтобы такого не было);
- resolve_lang(): 'ru' → ru, всё остальное (en/zh/hi/... и незнакомые коды) → en,
  None (нет профиля и кода клиента) → ru — аудитория запуска СНГ;
- reply-кнопки матчатся по тексту, поэтому у каждой кнопки есть btn_variants() —
  обработчики ловят оба языка.
"""
from __future__ import annotations

SUPPORTED_LANGS = ("ru", "en")


def resolve_lang(lang: str | None) -> str:
    if lang is None:
        return "ru"
    return "ru" if lang == "ru" else "en"


# ==========================================================================
# Кнопки нижних reply-панелей (матчинг по тексту!)
# ==========================================================================
BUTTONS: dict[str, dict[str, str]] = {
    "main_menu": {"ru": "📱 ГЛАВНОЕ МЕНЮ", "en": "📱 MAIN MENU"},
    "profile": {"ru": "👤 МОЙ ПРОФИЛЬ", "en": "👤 MY PROFILE"},
    "farm": {"ru": "🚜 МОЯ ФЕРМА", "en": "🚜 MY FARM"},
    "games_zone": {"ru": "🕹️ ИГРОВАЯ ЗОНА", "en": "🕹️ GAME ZONE"},
    "teams": {"ru": "🏆 КОМАНДЫ И КЛАНЫ", "en": "🏆 TEAMS & CLANS"},
    "shop": {"ru": "🏪 МАГАЗИН", "en": "🏪 SHOP"},
    "shop_cat_farm": {"ru": "🚜 ДЛЯ ФЕРМЫ", "en": "🚜 FOR THE FARM"},
    "shop_cat_games": {"ru": "🕹️ ИГРОВЫЕ", "en": "🕹️ GAMING"},
}


def btn(lang: str, key: str) -> str:
    return BUTTONS[key][resolve_lang(lang)]


def btn_variants(key: str) -> set[str]:
    """Все языковые варианты кнопки — для F.text.in_(...) в обработчиках."""
    return set(BUTTONS[key].values())


# ==========================================================================
# Тексты. Эталон — ru. Плейсхолдеры {name} должны совпадать в обоих языках.
# ==========================================================================
RU: dict[str, str] = {
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ Профиль не найден. Нажми /start для регистрации.",
    "common.btn_menu": "💿 Главное Меню /menu",
    "common.blocked": "🚫 Твой аккаунт заблокирован администрацией ROFL HUB.",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>С возвращением, @{username}!</b>\nТвой прогресс на месте. Панель навигации — внизу экрана.",
    "start.btn_continue": "🛸 ПРОДОЛЖИТЬ",
    "start.btn_cutlet": "Что за кибер-котлета?🥩🤔",
    "start.btn_fight": "Расскажи скорее и в БОЙ!",
    "start.console": "🚀 <b>Консоль управления активирована! Используй кнопки внизу экрана.</b>",
    "start.intro1": (
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
    ),
    "start.intro2": (
        "🎁 <b>ДЕРЖИ СВОИ ПЕРВЫЕ НАГРАДЫ ЗА РЕГИСТРАЦИЮ!</b>\n"
        "..................................................\n"
        "💸 Тебе начислено: <b>{balance} монет</b>\n"
        "🥩 Тебе начислено: <b>{cutlets} кибер-котлета</b>\n"
        "..................................................\n"
        "Это твой стартовый бонус за вступление в клуб ROFL HUB.\n\n"
        "🔒 <i>Бонус выдаётся только один раз в момент регистрации.</i>\n\n"
        "Монеты можно потратить разными способами, они — основа экономики хаба. Береги их...\n\n"
        "⁉️ <b>Но у тебя наверняка возник вопрос:</b> Что за котлета? Кого ей кормить?"
    ),
    "start.intro3": (
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
    ),
    "start.intro4": (
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
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>ГЛАВНОЕ МЕНЮ ЭКОСИСТЕМЫ ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>ЛИЧНЫЙ ПРОФИЛЬ И ПАСПОРТ:</b>\n"
        "• /start — Начать знакомство и зарегистрировать аккаунт\n"
        "• /profile — Твой паспорт, баланс и команда в реальном времени\n"
        "• /my_stats — Твоя историческая статистика за последние 30 дней\n\n"
        "🚜 <b>КИБЕР-ФЕРМА И АВТОМАТИЗАЦИЯ:</b>\n"
        "• /farm — Топливный хаб: заправка и скорость выработки роботов\n"
        "• /shop — Маркетплейс: закупка майнеров, котлет и улучшений хаба\n\n"
        "🕹️ <b>ИГРОВАЯ КОМНАТА:</b>\n"
        "• /games — Инлайн-хаб всех игр против бота\n"
        "• /quiz — Викторина на скорость: 10 секунд на ответ, уровни и бонусы\n"
        "• /duel — ДУЭЛИ 1-на-1 с живыми игроками: столы 10/100/1000\n"
        "• /rps, /high_low, /coin, /dice, /safe — Быстрые игры на рофлы\n\n"
        "👥 <b>УПРАВЛЕНИЕ БАНДАМИ:</b>\n"
        "• /create_team — Зарегистрировать свою команду за 100 000 рофлов\n"
        "• /my_team — Дашборд банды и СПИСОК ТИММЕЙТОВ с уровнями 🧠\n"
        "• /all_teams — Игровая рулетка случайных команд СНГ\n\n"
        "💸 <b>ДЕНЬГИ И ДРУЗЬЯ:</b>\n"
        "• /invite — Твоя реферальная ссылка: +1000 рофлов за друга\n"
        "• /transfer — Перевести рофлы другому игроку\n\n"
        "📚 <b>ЮРИДИЧЕСКИЙ БЛОК:</b>\n"
        "• /faq — Часто задаваемые вопросы и ответы\n"
        "• /rules — Пользовательское соглашение и юридический бронежилет\n"
        "..................................................\n"
        "<i>⚙️ Используй вечную двухколонную гейм-панель внизу экрана для мгновенной навигации по разделам!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>ДОБРО ПОЖАЛОВАТЬ В ИГРОВУЮ ЗОНУ ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Здесь ты можешь сразиться с ботом в быстрых дуэлях или пройти "
        "интеллектуальный спринт-тест, чтобы сорвать куш или слить баланс!\n\n"
        "💸 Победа приносит: <b>+2 рофла</b> (Кибер-Сейф: <b>+5</b>)\n"
        "💀 Проигрыш или ничья списывает: <b>-1 рофл</b>\n"
        "🧠 В Викторине — таймер 10 секунд и уровни интеллекта: 1-й уровень — 10 верных ответов и <b>+100 рофлов</b>, "
        "дальше каждый уровень на 10 ответов длиннее, но и награда растёт на 100!\n\n"
        "..................................................\n"
        "👇 <b>КЛИКАЙ ПО КНОПКЕ НИЖЕ ДЛЯ НЕМЕДЛЕННОГО СТАРТА РAУНДA:</b>"
    ),
    "menu.btn_quiz": "🧠 Викторина (/quiz)",
    "menu.btn_rps": "🪨 КНБ (/rps)",
    "menu.btn_hl": "📈 Больше/Меньше (/high_low)",
    "menu.btn_coin": "🪙 Орёл/Решка (/coin)",
    "menu.btn_dice": "🎲 Кубики (/dice)",
    "menu.btn_safe": "🔐 Кибер-Сейф (/safe)",
    "menu.btn_duel": "⚔️ ДУЭЛИ 1-на-1 (/duel)",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 ЗАБРАТЬ БОНУС (котлета раз в 24 ч)",
    "farm.btn_load1": "🥩 Заправить 1 шт.",
    "farm.btn_loadall": "⚡ Заправить ВСЕ",
    "farm.btn_shop": "🏪 Зайти в Магазин /shop",
    "farm.status_all_fueled": "🟢 Все Кибер-Бурильщики заправлены и добывают монеты!",
    "farm.status_partial": "🟡 Заправлено {fueled} из {total} Кибер-Бурильщиков. Остальные ждут котлет в холодильнике!",
    "farm.status_no_fuel": "🔴 Кибер-Бурильщики остановились! В холодильнике не хватает топлива.",
    "farm.status_no_drills": "💡 Заведи Кибер-Бурильщиков в /shop для увеличения дохода.",
    "farm.boost_nuclear": "🔋 Ядерный Разгон x5 до {until} UTC (расход котлет ×3)",
    "farm.boost_nitrogen": "❄️ Азотное Охлаждение +40% до {until} UTC",
    "farm.boost_drone": "🛸 Мастер-дрон продлевает жизнь роботов до {until} UTC",
    "farm.no_boosts": "Нет активных усилений — загляни в /shop.",
    "farm.burnout": "🔥 Ближайшее сгорание робота: <b>{until} UTC</b>\n",
    "farm.dashboard": (
        "🚜 <b>ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Активных роботов на заводе: <b>{total} шт.</b>\n"
        "• Младшие Майнеры ({junior_rate} рофлов/ч): <code>{junior} шт.</code>\n"
        "• Кибер-Бурильщики ({premium_rate} рофлов/ч): <code>{premium} шт.</code>\n"
        "{burnout}\n"
        "📊 <b>АКТУАЛЬНАЯ СКОРОСТЬ ТВОЕЙ ФЕРМЫ:</b>\n"
        "• Выработка в час: <b>+{speed_hour} рофлов</b>\n"
        "• Выработка в сутки: <b>+{speed_day} рофлов</b>\n\n"
        "⚡ <b>УСИЛЕНИЯ:</b>\n{boosts}\n\n"
        "📋 <b>СТАТУС ИГРОВОГО ЗАВОДА:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>СОСТОЯНИЕ АВТОМАТИЧЕСКОГО ХОЛОДИЛЬНИКА:</b>\n"
        "🥩 Запас топлива: <b>{fridge} / {capacity} шт.</b>\n"
        "💼 Котлеты на складе инвентаря: <code>{inv} шт.</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Важно: роботы живут 30 дней (Мастер-дрон приостанавливает износ). "
        "Кибер-Бурильщик списывает целую котлету из холодильника на каждые 24 часа работы. "
        "Следи за заправкой!</i>"
    ),
    "farm.bonus_ok": "🎁 Кибер-котлета зачислена на склад! Возвращайся через 24 часа.",
    "farm.bonus_wait": "⏳ Бонус уже забран! Следующая котлета через {hours} ч {minutes} мин.",
    "farm.no_inv_cutlets": "❌ У тебя в инвентаре нет кибер-котлет! Купи их в /shop",
    "farm.fridge_full": "📦 Твой Холодильник уже полностью забит!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>ЛИЧНЫЙ КАБИНЕТ ИГРОКА ROFL HUB</b>\n"
        "..................................................\n\n"
        "🆔 Твой ID Паспорта: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Монеты сейчас: <b>{balance} рофлов</b>\n"
        "🏆 Твой статус: <b>{team}</b>\n"
        "🧠 Уровень интеллекта: <b>{level}</b> · до уровня {next_level}: "
        "<b>{left}</b> верных ответов в /quiz (награда: +{reward} рофлов)\n\n"
        "..................................................\n"
        "<i>Здесь показано то, что есть у тебя прямо сейчас. Используй кнопки для перелёта в другие разделы!</i>"
    ),
    "profile.no_team": "Нет команды",
    "profile.team_label": "Команда",
    "profile.clan_label": "Клан",
    "profile.btn_farm": "🚜 Моя Кибер-Ферма",
    "profile.btn_shop": "🏪 Магазин /shop",
    "profile.stats": (
        "📊 <b>ИГРОВАЯ СТАТИСТИКА ДОСТИЖЕНИЙ (30 ДНЕЙ)</b>\n"
        "..................................................\n\n"
        "🧠 Уровень игрового интеллекта: <b>{level}</b> (всего верных ответов: {total})\n"
        "🎮 Проведено раундов в дуэлях: <b>{played} игр</b>\n"
        "🏆 Одержано побед над соперниками: <code>{won} раз</code>\n"
        "👥 Приглашено активных друзей: <b>{refs} чел.</b>\n\n"
        "..................................................\n"
        "<i>Статистика хранит твои исторические заслуги и прошлые достижения, даже если выигранные монеты уже были потрачены в маркете!</i>"
    ),
    "img.passport": "ID ПАСПОРТА: {user_id}",
    "img.owner": "ВОЖАК: @{username}",
    "img.balance": "Баланс: {balance} рофлов",
    "img.fridge": "В холодильнике: {fridge} / {capacity} шт.",
    "img.inv": "Котлеты на складе: {inv} шт.",
    "img.junior": "Младшие Майнеры: {count} шт.",
    "img.premium": "Кибер-Бурильщики: {count} шт.",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 ПОБЕДА! Начислено: <b>+{reward} рофл.</b>",
    "games.lose": "💀 ПРОИГРЫШ! Сбор раунда: <b>-{penalty} рофл</b>.",
    "games.draw": "🤝 НИЧЬЯ! Сбор раунда: <b>-{penalty} рофл</b>.",
    "games.limit": (
        "🛑 <b>Суточный лимит достигнут!</b>\n\n"
        "В игре {game} ты уже забрал {limit} побед на сегодня. Лимит обновится в 00:00 UTC.\n\n"
        "⚡ Снять лимит на 24 часа — 5 ★, на 30 дней — 99 ★ (раздел «Игровые» в /shop)."
    ),
    "games.no_coins": "❌ У тебя 0 рофлов — нечем оплатить сбор раунда. Забери доход с фермы в /farm!",
    "games.balance": "💰 Баланс: <b>{balance} рофлов</b>",
    "games.btn_retry": "🎮 Сыграть ещё раз!",
    "games.btn_hub": "🕹️ Игровая зона",
    "games.level_up": (
        "🏅 <b>УРОВЕНЬ ИНТЕЛЛЕКТА ПОВЫШЕН: {level}!</b> Награда: <b>+{bonus} рофлов</b>!\n"
        "Следующий уровень: {next_required} верных ответов → +{next_reward} рофлов."
    ),
    "games.level_progress": "📚 До уровня <b>{level}</b>: ещё <b>{left}</b> верных (награда +{reward} рофлов).",
    "games.name.rps": "Камень-Ножницы-Бумага",
    "games.name.hl": "Больше/Меньше",
    "games.name.quiz": "Викторина",
    "games.name.coin": "Орёл/Решка",
    "games.name.dice": "Кубики",
    "games.name.safe": "Сейф",

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>КАМЕНЬ-НОЖНИЦЫ-БУМАГА</b>\n\n"
        "Победа: <b>+{reward}</b> · Проигрыш/ничья: <b>-{penalty}</b>\n"
        "Лимит побед в сутки: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Камень",
    "rps.scissors": "✂️ Ножницы",
    "rps.paper": "🧻 Бумага",
    "rps.draw": "🤝 <b>Ничья!</b> Оба выбрали {bot}.",
    "rps.win": "🏆 <b>Победа!</b> {user} бьёт {bot}.",
    "rps.lose": "💀 <b>Бот победил.</b> {bot} бьёт {user}.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>БОЛЬШЕ ИЛИ МЕНЬШЕ</b>\n\nБот выставил число: <b>{base}</b>.\n"
        "Скрытое число будет больше или меньше?\n"
        "Победа: <b>+{reward}</b> · Проигрыш: <b>-{penalty}</b> · Лимит: <b>{limit}</b> побед"
    ),
    "hl.btn_up": "📈 Больше",
    "hl.btn_down": "📉 Меньше",
    "hl.result": "🎲 <b>ИТОГ РАУНДА</b>\n\nЧисло бота: <b>{base}</b> · Скрытое: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>ВИКТОРИНА · {category}</b>\n"
        "🏅 Уровень интеллекта: <b>{level}</b> · До уровня {next_level}: "
        "<b>{progress}/{required}</b> верных (+{reward} рофлов)\n\n"
        "❓ {question}\n\n"
        "⏱ <b>На ответ — {seconds} секунд!</b> Не успел — проигрыш.\n"
        "<i>Верно: <b>+{win}</b> · Ошибка: <b>-{penalty}</b> · Лимит: <b>{limit}</b> побед</i>"
    ),
    "quiz.btn_new": "🧠 Новый вопрос",
    "quiz.timeout": "⏰ <b>ВРЕМЯ ВЫШЛО!</b> На ответ даётся {seconds} секунд.",
    "quiz.stale": "⏳ Этот вопрос уже не активен. Запусти новый!",
    "quiz.stale_alert": "Этот вопрос уже не активен. Запусти новый!",
    "quiz.empty": "⚠️ База вопросов пуста. Сообщи администратору.",
    "quiz.result_header": "📊 <b>ИТОГ</b>",
    "quiz.correct": "✅ <b>Верно!</b>",
    "quiz.wrong": "❌ <b>Ошибка.</b> Правильный ответ: <code>{correct}</code>",

    # ---------------- Орёл/Решка ----------------
    "coin.intro": (
        "🪙 <b>ОРЁЛ ИЛИ РЕШКА</b>\n\n"
        "Бот подбрасывает кибер-монету. Угадай, какой стороной она упадёт!\n"
        "Победа: <b>+{reward}</b> · Проигрыш: <b>-{penalty}</b> · Лимит: <b>{limit}</b> побед"
    ),
    "coin.heads": "🦅 Орёл",
    "coin.tails": "🪙 Решка",
    "coin.result": "🪙 Монета крутится... выпал <b>{result}</b>! Твоя ставка: {choice}.",

    # ---------------- Кубики ----------------
    "dice.intro": (
        "🎲 <b>КУБИКИ</b>\n\n"
        "Ты и бот бросаете по кубику. У кого больше очков — тот забирает раунд!\n"
        "Победа: <b>+{reward}</b> · Проигрыш/ничья: <b>-{penalty}</b> · Лимит: <b>{limit}</b> побед"
    ),
    "dice.btn_roll": "🎲 БРОСИТЬ КУБИКИ",
    "dice.toast": "Кубики брошены!",
    "dice.result": "🎲 Твой кубик (первый): <b>{player}</b> · Кубик бота: <b>{bot}</b>",

    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>КИБЕР-СЕЙФ</b>\n\n"
        "Внутри — куш <b>{jackpot} рофлов</b>! Дверца заперта кодом от 1 до {codes}. "
        "У тебя одна попытка.\n"
        "Вскрыл: <b>+{jackpot}</b> · Сигнализация: <b>-{penalty}</b> · Лимит: <b>{limit}</b> побед"
    ),
    "safe.btn_retry": "🔐 Взломать ещё раз!",
    "safe.win": "🔓 <b>Сейф вскрыт!</b> Код был: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Сработала сигнализация!</b> Ты набрал {guess}, а код был: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>ДУЭЛИ 1-НА-1: КАМЕНЬ-НОЖНИЦЫ-БУМАГА НА СТАВКУ</b>\n"
        "..................................................\n\n"
        "Выбирай стол по карману — как в покере. Ставка списывается сразу, "
        "соперник — живой игрок ROFL HUB!\n\n"
        "💰 Банк = обе ставки. Победитель забирает <b>{payout_percent}%</b> банка, "
        "<b>{burn_percent}%</b> сгорает навсегда (дефляция!).\n"
        "🤝 Ничья — мгновенная переигровка жестов, банк на столе.\n"
        "⏱ На жест — <b>{move_timeout} секунд</b>, молчуну жест выберет генератор случайности.\n"
        "🏆 Победы в дуэлях идут в зачёт твоей команды в Битвах!\n\n"
        "👇 <b>ВЫБЕРИ СТОЛ:</b>"
    ),
    "duel.btn_table": "⚔️ Стол {stake} рофлов",
    "duel.btn_cancel": "❌ Покинуть стол (вернуть ставку)",
    "duel.btn_move_rock": "🪨 Камень",
    "duel.btn_move_scissors": "✂️ Ножницы",
    "duel.btn_move_paper": "🧻 Бумага",
    "duel.waiting": (
        "🪑 <b>Ты за столом {stake} рофлов.</b> Ставка в банке.\n"
        "Ждём второго бойца... Как только он сядет — вам обоим придёт выбор жеста!\n"
        "<i>Очередь живёт {ttl} минут, потом ставка вернётся автоматически.</i>"
    ),
    "duel.cancelled": "🚪 Ты покинул стол. Ставка <b>{stake} рофлов</b> вернулась на баланс.",
    "duel.expired": "⌛ Соперник за столом {stake} так и не нашёлся. Ставка <b>{stake} рофлов</b> возвращена.",
    "duel.matched": (
        "⚔️ <b>СОПЕРНИК НАЙДЕН! Стол {stake} рофлов.</b>\n"
        "Банк: <b>{bank} рофлов</b> · Победителю: <b>{payout}</b>\n\n"
        "⏱ У тебя <b>{timeout} секунд</b> на выбор жеста!"
    ),
    "duel.move_saved": "✊ Жест принят! Ждём жест соперника...",
    "duel.draw_replay": (
        "🤝 <b>НИЧЬЯ! Раунд {round}.</b> Оба показали одинаковый жест.\n"
        "Банк на столе. ⏱ Снова {timeout} секунд — выбери жест:"
    ),
    "duel.win": (
        "🏆 <b>ДУЭЛЬ ТВОЯ!</b>\n\n"
        "Твой жест {winner_move} бьёт {loser_move}.\n"
        "💰 Выигрыш: <b>+{payout} рофлов</b> · 🔥 Сгорело в банке: {burned}\n"
        "💼 Баланс: <b>{balance} рофлов</b>"
    ),
    "duel.lose": (
        "💀 <b>ДУЭЛЬ ПРОИГРАНА.</b>\n\n"
        "{winner_move} соперника бьёт твой {loser_move}.\n"
        "📉 Ставка <b>{stake} рофлов</b> ушла в банк победителя.\n"
        "Реванш?"
    ),
    "duel.reaper_prefix": "⏰ <b>Тайм-аут раунда!</b> Недостающие жесты выбрал генератор случайности.\n\n",
    "duel.bad_table": "❌ Такого стола не существует.",
    "duel.already_in": "⚠️ Ты уже за столом или в бою! Сначала закончи текущую дуэль.",
    "duel.no_coins": "❌ Для этого стола нужно {stake} рофлов на балансе.",
    "duel.cancel_impossible": "⚠️ Эту очередь уже нельзя отменить (соперник найден или стол закрыт).",
    "duel.not_active": "⌛ Эта дуэль уже завершена.",
    "duel.not_participant": "🔒 Это не твоя дуэль!",
    "duel.move_already": "✋ Ты уже показал жест в этом раунде. Ждём соперника!",
    "duel.bad_move": "❌ Неизвестный жест.",
    "duel.btn_rematch": "⚔️ Реванш (к столам)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА ROFL HUB</b>\n"
        "..................................................\n\n"
        "Приглашай друзей и получай <b>+{bonus} рофлов</b> за каждого, "
        "кто зарегистрируется по твоей персональной ссылке!\n\n"
        "🔗 <b>Твоя ссылка (нажми, чтобы скопировать):</b>\n<code>{link}</code>\n\n"
        "📊 <b>ТВОЯ СТАТИСТИКА:</b>\n"
        "👥 Приглашено друзей: <b>{invited} чел.</b>\n"
        "💰 Заработано на рефералах: <b>{earned} рофлов</b>\n\n"
        "..................................................\n"
        "<i>Кидай ссылку в чаты класса, друзьям и в соцсети — чем больше банда, тем быстрее растёт твой баланс!</i>"
    ),
    "ref.btn_share": "📣 Поделиться ссылкой",
    "ref.share_text": "Залетай в игровую экосистему ROFL HUB!",

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>ПЕРЕВОД РОФЛОВ ДРУГОМУ ИГРОКУ</b>\n"
        "..................................................\n\n"
        "Формат команды:\n"
        "<code>/transfer ID сумма</code> — по ID Паспорта (виден в /profile)\n"
        "<code>/transfer @username сумма</code> — по юзернейму\n"
        "<code>/transfer ROFL-HUB-777 сумма</code> — по VIP ID с аукциона\n\n"
        "Примеры:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Минимальная сумма: <b>{min} рофлов</b>"
    ),
    "tr.not_found": "❌ Получатель не найден. Проверь ID Паспорта или @username — игрок должен быть зарегистрирован в боте.",
    "tr.self": "🤨 Перевести монеты самому себе нельзя — это была бы вечная экономика!",
    "tr.blocked": "🚫 Этот игрок заблокирован — переводы ему недоступны.",
    "tr.min": "❌ Минимальная сумма перевода — {min} рофлов.",
    "tr.insufficient": "❌ Недостаточно рофлов! Твой баланс: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Недостаточно рофлов на балансе.",
    "tr.confirm": (
        "🔄 <b>ПОДТВЕРДИ ПЕРЕВОД:</b>\n\n"
        "👤 Получатель: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Сумма списания: <b>{amount} рофлов</b>{fee_line}\n"
        "💰 Адресат получит: <b>{received} рофлов</b>\n\n"
        "<i>Переводы отменить нельзя — проверь получателя!</i>"
    ),
    "tr.fee_line": "\n🔥 Комиссия хаба: <b>{fee} рофлов</b> (сгорит)",
    "tr.btn_confirm": "✅ ПОДТВЕРДИТЬ ПЕРЕВОД",
    "tr.btn_cancel": "❌ Отмена",
    "tr.cancelled_toast": "Перевод отменён",
    "tr.cancelled": "❌ <b>Перевод отменён.</b> Монеты остались на месте.",
    "tr.not_yours": "🔒 Это не твой перевод!",
    "tr.done_toast": "✅ Перевод выполнен!",
    "tr.done": (
        "✅ <b>ПЕРЕВОД ВЫПОЛНЕН!</b>\n\n"
        "💸 Отправлено: <b>{amount} рофлов</b> игроку ID <code>{recipient_id}</code>\n"
        "💰 Твой баланс: <b>{balance} рофлов</b>"
    ),
    "tr.received": (
        "💰 <b>Тебе перевели {amount} рофлов!</b>\n"
        "Отправитель: ID <code>{sender_id}</code>. Баланс уже пополнен — проверь /profile!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>МАГАЗИН ROFL HUB</b>\nПокупки — через официальные Telegram Stars. Выбери категорию кнопками внизу.",
    "shop.cat_farm": (
        "🚜 <b>МАГАЗИН · ДЛЯ ФЕРМЫ</b>\n"
        "..................................................\n"
        "Роботы на 30 дней, топливо, холодильники, бусты и Мастер-дрон.\n"
        "📦 Твой холодильник сейчас: <b>{capacity} котлет</b>\n"
        "..................................................\n"
        "👇 <b>Выбери товар:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>МАГАЗИН · ИГРОВЫЕ</b>\n"
        "..................................................\n"
        "Снятие лимитов побед, паки рофлов и лицензия Мега-Клана.\n"
        "..................................................\n"
        "👇 <b>Выбери товар:</b>"
    ),
    "pay.invoice_desc": "Мгновенная доставка внутриигрового контента ROFL HUB.",
    "pay.invoice_error": "⚠️ Не удалось сформировать счёт Telegram Stars. Попробуй позже.",
    "pay.success": "🎉 <b>Платёж подтверждён!</b>\n🧾 <code>{charge}</code>\n💵 Списано: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Оплата прошла, но доставка временно не удалась. Мы уже в курсе.\n"
        "Сохрани номер платежа: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Stars возвращены на твой счёт автоматически.",
    "pay.keep_charge": "Сохрани номер платежа для возврата: <code>{charge}</code>",
    "pay.already": "✅ Этот платёж уже был обработан, товар выдан ранее.",
    "pay.support": (
        "🛟 <b>ПОДДЕРЖКА ПО ПЛАТЕЖАМ TELEGRAM STARS</b>\n"
        "..................................................\n\n"
        "Все товары ROFL HUB — цифровые и доставляются мгновенно после оплаты.\n\n"
        "⚙️ <b>Если оплата прошла, а товар не пришёл:</b>\n"
        "бот автоматически возвращает Stars при сбое доставки. Если этого не случилось — "
        "пришли сюда номер платежа (он есть в чеке, формат <code>xxxx...</code>) и опиши проблему. "
        "Администрация проверит платёж по базе и решит вопрос в течение 24 часов.\n\n"
        "💫 <b>Политика возвратов:</b>\n"
        "возврат возможен, если товар не был получен или выдан с ошибкой. "
        "Корректно доставленные цифровые товары возврату не подлежат.\n\n"
        "..................................................\n"
        "<i>Этот раздел — официальная точка поддержки покупок по правилам Telegram.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 На склад добавлено: <b>{qty} котлет</b>.",
    "dlv.miner": "🤖 Робот <b>«{name}»</b> доставлен на твою ферму.\n⏳ Срок службы: до <b>{until} UTC</b>.",
    "dlv.miner_junior": "Младший Майнер",
    "dlv.miner_premium": "Кибер-Бурильщик",
    "dlv.fridge": "📦 Холодильник расширен до <b>{capacity} котлет</b>.",
    "dlv.coins": "💰 Зачислено <b>+{amount} рофлов</b>.",
    "dlv.boost_nuclear": "🔋 Ядерный Разгон x5 активен до <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Азотное Охлаждение +40% активен до <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Мастер-дрон охраняет ферму до <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Лимиты побед сняты до <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Команда получила статус <b>МЕГА-КЛАН</b>: до {max} мест.",
    "dlv.err_fridge": "У тебя уже холодильник такого или большего объёма.",
    "dlv.err_no_team": "У тебя нет созданной команды. Сначала создай её через /create_team.",
    "dlv.err_mega": "Твоя команда уже имеет статус Мега-Клана.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>У тебя пока нет созданной команды!</b>\n\nТы можешь зарегистрировать личную банду прямо сейчас, нажав на кнопку ниже.",
    "clan.btn_create": "🏆 Создать Команду за 100к",
    "clan.btn_members": "👥 СПИСОК ТИММЕЙТОВ",
    "clan.btn_leave": "🚪 Покинуть команду / Бросить банду",
    "clan.btn_dashboard": "🏆 Дашборд команды",
    "clan.status_clan": "👑 СТАТУС: КЛАН ИМПЕРИИ",
    "clan.status_team": "👥 СТАТУС: ОБЫЧНАЯ КОМАНДА",
    "clan.dashboard": (
        "🏆 <b>ИНФОРМАЦИОННЫЙ ДАШБОРД ТВОЕЙ КОМАНДЫ</b>\n"
        "..................................................\n\n"
        "📌 Название: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Капитан банды: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Девиз: <i>«{motto}»</i>\n"
        "🔮 Символ эмблемы: {symbol}\n\n"
        "👥 Состав участников: <b>{members} / {max_members} чел.</b>\n"
        "..................................................\n\n"
        "👇 <b>НАВИГАЦИЯ:</b>"
    ),
    "clan.members_only": "🔒 Список участников виден только членам этой команды!",
    "clan.members_gone": "❌ Команда уже расформирована.",
    "clan.members_header": (
        "👥 <b>СОСТАВ КОМАНДЫ «{name}»</b>\n"
        "🧠 — уровень игрового интеллекта (прокачивается только в /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Страница <b>{page} / {pages}</b> · Всего бойцов: <b>{members}</b>\n"
        "<i>Кликай по @username тиммейта, чтобы написать ему, собрать свой чат "
        "и позвать банду на командные состязания!</i>"
    ),
    "clan.btn_prev": "⬅️ Назад",
    "clan.btn_next": "Вперёд ➡️",
    "clan.join_ok": (
        "🎉 <b>ПОЗДРАВЛЯЕМ, ТЫ В ИГРЕ!</b>\n\nТы успешно вступил в команду <b>{name}</b>!\n"
        "📍 Пиши команду /my_team, чтобы проверить состав!"
    ),
    "clan.leave_ok": "🚪 Ты успешно покинул команду <b>{name}</b>. Теперь ты вольная птица!",
}

EN: dict[str, str] = {
    # ---------------- common ----------------
    "common.no_profile": "⚠️ Profile not found. Press /start to register.",
    "common.btn_menu": "💿 Main Menu /menu",
    "common.blocked": "🚫 Your account has been blocked by the ROFL HUB administration.",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Welcome back, @{username}!</b>\nYour progress is safe. The navigation panel is at the bottom of the screen.",
    "start.btn_continue": "🛸 CONTINUE",
    "start.btn_cutlet": "What's a cyber-cutlet?🥩🤔",
    "start.btn_fight": "Tell me quick — then BATTLE!",
    "start.console": "🚀 <b>Control console activated! Use the buttons at the bottom of the screen.</b>",
    "start.intro1": (
        "👋 <b>Hi! I'm ROFL HUB BOT — the main bot of the ROFL HUB gaming ecosystem. "
        "A new-generation hub of games and knowledge!</b>\n\n"
        "<b>Here you can:</b>\n"
        "🎮 Play chat-bot games against the bot and other players\n"
        "💸 Earn game currency for wins, or launch a farm that mines it around the clock\n"
        "🤼 Create a team and storm the leaderboard\n"
        "🏆 Upgrade your team into a clan and fight in the international rating\n"
        "💰 Win a million-coin jackpot together with your crew\n"
        "👑 Buy a feature post on our social pages or website to promote yourself or your blog\n\n"
        "<b>This chat-bot can:</b>\n"
        "🎮 Show the list of all ROFL HUB games, channels and websites\n"
        "⚡ Award coins for games, team and clan battles, achievements, activity and referrals\n"
        "🔄 Transfer game coins to another ROFL HUB player\n"
        "💎 Sell website publications and VIP spots for creators and bloggers\n"
        "🚀 Sell boosters, titles, statuses and much more...\n\n"
        "<i>Press “CONTINUE” and I'll tell you more 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>HERE ARE YOUR FIRST SIGN-UP REWARDS!</b>\n"
        "..................................................\n"
        "💸 You received: <b>{balance} coins</b>\n"
        "🥩 You received: <b>{cutlets} cyber-cutlet</b>\n"
        "..................................................\n"
        "This is your welcome bonus for joining the ROFL HUB club.\n\n"
        "🔒 <i>The bonus is granted only once, at registration.</i>\n\n"
        "Coins can be spent in many ways — they are the backbone of the hub's economy. Guard them well...\n\n"
        "⁉️ <b>But you surely have a question:</b> what's this cutlet? Who do I feed it to?"
    ),
    "start.intro3": (
        "<b>FIRST, WHY DO GAME COINS MATTER SO MUCH?</b>\n\n"
        "Coins power all trading, contests and purchases in <b>ROFL HUB</b>. "
        "It's almost the only game currency in the world you can mine for free!\n"
        "..................................................\n"
        "<b>There are many ways to earn them:</b>\n"
        "- Invite friends with your referral link\n"
        "- Win games against the bot\n"
        "- Win duels against other players\n"
        "- Join team and clan battles\n"
        "- Claim daily login bonuses and quests\n"
        "- Get a robot that mines coins 24/7 (Miner Bot / Cyber-Driller)\n"
        "..................................................\n"
        "<b>If you own a level-two robot (the Cyber-Driller) — it must be fed every day. "
        "That's where the cyber-cutlet comes in: fuel for automatic mining, "
        "given out for free every day! Your job is simple — drop by and feed your robot.</b>\n\n"
        "Miss a feeding — the robot powers down and mining stops.\n\n"
        "The Miner Bot (level one) needs no fuel. "
        "Important! Every robot is bought for 30 days — then buy it again or get a Master Drone. "
        "You'll figure it out as you go:) Let's not get distracted.\n\n"
        "A little more about <b>ROFL HUB</b>, so you understand how everything works here.\n\n"
        "🛑 <b>This is the last message of our introduction. After this — straight to battle:)</b>"
    ),
    "start.intro4": (
        "<b>THE SHORT VERSION. ROFL HUB IS:</b>\n"
        "- Chat-bot games for every taste\n"
        "- Create your own team (up to 50 players)\n"
        "- Upgrade it into a clan (up to 1000 players)\n"
        "- Team and clan battles for prizes\n"
        "- The ROFL HUB CHANNEL with fun and knowledge\n"
        "- Instagram page — rofl_hub_global\n"
        "- Website rofl-hub.com for chatting and promotion without sign-up\n"
        "- Thousands of players worldwide — your new friends may be among them!\n"
        "..................................................\n"
        "<b>As promised, this is the final message. Now — to battle! Useful commands:</b>\n\n"
        "/menu — quick control of all features\n"
        "/games — list of all games\n"
        "/faq — frequently asked questions\n"
        "/rules — user agreement\n"
    ),

    # ---------------- menu & game zone ----------------
    "menu.text": (
        "📱 <b>ROFL HUB ECOSYSTEM — MAIN MENU</b>\n"
        "..................................................\n\n"
        "👤 <b>PROFILE & PASSPORT:</b>\n"
        "• /start — Begin the intro and register an account\n"
        "• /profile — Your passport, balance and team in real time\n"
        "• /my_stats — Your historical stats for the last 30 days\n\n"
        "🚜 <b>CYBER-FARM & AUTOMATION:</b>\n"
        "• /farm — Fuel hub: refueling and robot mining speed\n"
        "• /shop — Marketplace: miners, cutlets and hub upgrades\n\n"
        "🕹️ <b>GAME ROOM:</b>\n"
        "• /games — Inline hub of all games against the bot\n"
        "• /quiz — Speed quiz: 10 seconds per answer, levels and bonuses\n"
        "• /duel — 1-on-1 DUELS with real players: tables 10/100/1000\n"
        "• /rps, /high_low, /coin, /dice, /safe — Quick games for rofls\n\n"
        "👥 <b>CREW MANAGEMENT:</b>\n"
        "• /create_team — Register your own team for 100,000 rofls\n"
        "• /my_team — Crew dashboard and the TEAMMATE LIST with 🧠 levels\n"
        "• /all_teams — Roulette of random teams\n\n"
        "💸 <b>MONEY & FRIENDS:</b>\n"
        "• /invite — Your referral link: +1000 rofls per friend\n"
        "• /transfer — Send rofls to another player\n\n"
        "📚 <b>LEGAL:</b>\n"
        "• /faq — Frequently asked questions\n"
        "• /rules — User agreement\n"
        "..................................................\n"
        "<i>⚙️ Use the permanent two-column game panel at the bottom of the screen for instant navigation!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>WELCOME TO THE ROFL HUB GAME ZONE!</b>\n"
        "..................................................\n\n"
        "Fight the bot in quick duels or take the intellectual sprint test "
        "to win big — or lose it all!\n\n"
        "💸 A win pays: <b>+2 rofls</b> (Cyber-Safe: <b>+5</b>)\n"
        "💀 A loss or draw costs: <b>-1 rofl</b>\n"
        "🧠 The Quiz has a 10-second timer and intellect levels: level 1 is 10 correct answers and <b>+100 rofls</b>, "
        "each next level is 10 answers longer — but the reward grows by 100!\n\n"
        "..................................................\n"
        "👇 <b>TAP A BUTTON BELOW TO START A ROUND RIGHT NOW:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz (/quiz)",
    "menu.btn_rps": "🪨 RPS (/rps)",
    "menu.btn_hl": "📈 High/Low (/high_low)",
    "menu.btn_coin": "🪙 Heads/Tails (/coin)",
    "menu.btn_dice": "🎲 Dice (/dice)",
    "menu.btn_safe": "🔐 Cyber-Safe (/safe)",
    "menu.btn_duel": "⚔️ 1-on-1 DUELS (/duel)",

    # ---------------- farm ----------------
    "farm.btn_bonus": "🎁 CLAIM BONUS (a cutlet every 24h)",
    "farm.btn_load1": "🥩 Load 1 cutlet",
    "farm.btn_loadall": "⚡ Load ALL",
    "farm.btn_shop": "🏪 Open the Shop /shop",
    "farm.status_all_fueled": "🟢 All Cyber-Drillers are fueled and mining coins!",
    "farm.status_partial": "🟡 {fueled} of {total} Cyber-Drillers are fueled. The rest are waiting for cutlets in the fridge!",
    "farm.status_no_fuel": "🔴 The Cyber-Drillers have stopped! Not enough fuel in the fridge.",
    "farm.status_no_drills": "💡 Get Cyber-Drillers in /shop to boost your income.",
    "farm.boost_nuclear": "🔋 Nuclear Boost x5 until {until} UTC (cutlet burn ×3)",
    "farm.boost_nitrogen": "❄️ Nitrogen Cooling +40% until {until} UTC",
    "farm.boost_drone": "🛸 Master Drone extends robot life until {until} UTC",
    "farm.no_boosts": "No active boosts — check out /shop.",
    "farm.burnout": "🔥 Next robot burnout: <b>{until} UTC</b>\n",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB CENTRAL FUEL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Active robots at the plant: <b>{total}</b>\n"
        "• Miner Bots ({junior_rate} rofls/h): <code>{junior}</code>\n"
        "• Cyber-Drillers ({premium_rate} rofls/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>YOUR FARM'S CURRENT SPEED:</b>\n"
        "• Output per hour: <b>+{speed_hour} rofls</b>\n"
        "• Output per day: <b>+{speed_day} rofls</b>\n\n"
        "⚡ <b>BOOSTS:</b>\n{boosts}\n\n"
        "📋 <b>PLANT STATUS:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>AUTOMATIC FRIDGE STATUS:</b>\n"
        "🥩 Fuel stock: <b>{fridge} / {capacity}</b>\n"
        "💼 Cutlets in inventory: <code>{inv}</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Important: robots live 30 days (the Master Drone pauses wear). "
        "A Cyber-Driller burns one whole cutlet from the fridge per 24 hours of work. "
        "Keep an eye on the fuel!</i>"
    ),
    "farm.bonus_ok": "🎁 A cyber-cutlet was added to your inventory! Come back in 24 hours.",
    "farm.bonus_wait": "⏳ Bonus already claimed! Next cutlet in {hours}h {minutes}m.",
    "farm.no_inv_cutlets": "❌ No cyber-cutlets in your inventory! Buy some in /shop",
    "farm.fridge_full": "📦 Your fridge is already full!",

    # ---------------- profile ----------------
    "profile.caption": (
        "📋 <b>ROFL HUB PLAYER DASHBOARD</b>\n"
        "..................................................\n\n"
        "🆔 Your Passport ID: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Coins right now: <b>{balance} rofls</b>\n"
        "🏆 Your status: <b>{team}</b>\n"
        "🧠 Intellect level: <b>{level}</b> · to level {next_level}: "
        "<b>{left}</b> correct answers in /quiz (reward: +{reward} rofls)\n\n"
        "..................................................\n"
        "<i>This is what you own right now. Use the buttons to jump to other sections!</i>"
    ),
    "profile.no_team": "No team",
    "profile.team_label": "Team",
    "profile.clan_label": "Clan",
    "profile.btn_farm": "🚜 My Cyber-Farm",
    "profile.btn_shop": "🏪 Shop /shop",
    "profile.stats": (
        "📊 <b>GAME ACHIEVEMENT STATS (30 DAYS)</b>\n"
        "..................................................\n\n"
        "🧠 Game intellect level: <b>{level}</b> (total correct answers: {total})\n"
        "🎮 Duel rounds played: <b>{played}</b>\n"
        "🏆 Victories won: <code>{won}</code>\n"
        "👥 Active friends invited: <b>{refs}</b>\n\n"
        "..................................................\n"
        "<i>Stats keep your historical achievements even if the coins you won were already spent in the market!</i>"
    ),
    "img.passport": "PASSPORT ID: {user_id}",
    "img.owner": "LEADER: @{username}",
    "img.balance": "Balance: {balance} rofls",
    "img.fridge": "In fridge: {fridge} / {capacity}",
    "img.inv": "Cutlets in stock: {inv}",
    "img.junior": "Miner Bots: {count}",
    "img.premium": "Cyber-Drillers: {count}",

    # ---------------- games engine ----------------
    "games.win": "🎉 VICTORY! Awarded: <b>+{reward} rofls.</b>",
    "games.lose": "💀 DEFEAT! Round fee: <b>-{penalty} rofl</b>.",
    "games.draw": "🤝 DRAW! Round fee: <b>-{penalty} rofl</b>.",
    "games.limit": (
        "🛑 <b>Daily limit reached!</b>\n\n"
        "You've already taken {limit} wins in {game} today. The limit resets at 00:00 UTC.\n\n"
        "⚡ Remove the limit for 24 hours — 5 ★, for 30 days — 99 ★ (the “Gaming” section in /shop)."
    ),
    "games.no_coins": "❌ You have 0 rofls — nothing to pay the round fee with. Collect your farm income in /farm!",
    "games.balance": "💰 Balance: <b>{balance} rofls</b>",
    "games.btn_retry": "🎮 Play again!",
    "games.btn_hub": "🕹️ Game zone",
    "games.level_up": (
        "🏅 <b>INTELLECT LEVEL UP: {level}!</b> Reward: <b>+{bonus} rofls</b>!\n"
        "Next level: {next_required} correct answers → +{next_reward} rofls."
    ),
    "games.level_progress": "📚 To level <b>{level}</b>: <b>{left}</b> more correct (reward +{reward} rofls).",
    "games.name.rps": "Rock-Paper-Scissors",
    "games.name.hl": "High/Low",
    "games.name.quiz": "Quiz",
    "games.name.coin": "Heads/Tails",
    "games.name.dice": "Dice",
    "games.name.safe": "Safe",

    # ---------------- RPS ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>ROCK-PAPER-SCISSORS</b>\n\n"
        "Win: <b>+{reward}</b> · Loss/draw: <b>-{penalty}</b>\n"
        "Daily win limit: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Rock",
    "rps.scissors": "✂️ Scissors",
    "rps.paper": "🧻 Paper",
    "rps.draw": "🤝 <b>Draw!</b> Both picked {bot}.",
    "rps.win": "🏆 <b>Victory!</b> {user} beats {bot}.",
    "rps.lose": "💀 <b>The bot won.</b> {bot} beats {user}.",

    # ---------------- High/Low ----------------
    "hl.intro": (
        "🎲 <b>HIGH OR LOW</b>\n\nThe bot set the number: <b>{base}</b>.\n"
        "Will the hidden number be higher or lower?\n"
        "Win: <b>+{reward}</b> · Loss: <b>-{penalty}</b> · Limit: <b>{limit}</b> wins"
    ),
    "hl.btn_up": "📈 Higher",
    "hl.btn_down": "📉 Lower",
    "hl.result": "🎲 <b>ROUND RESULT</b>\n\nBot's number: <b>{base}</b> · Hidden: <b>{secret}</b>",

    # ---------------- quiz ----------------
    "quiz.round": (
        "🧠 <b>QUIZ · {category}</b>\n"
        "🏅 Intellect level: <b>{level}</b> · To level {next_level}: "
        "<b>{progress}/{required}</b> correct (+{reward} rofls)\n\n"
        "❓ {question}\n\n"
        "⏱ <b>{seconds} seconds to answer!</b> Too slow — you lose.\n"
        "<i>Correct: <b>+{win}</b> · Mistake: <b>-{penalty}</b> · Limit: <b>{limit}</b> wins</i>\n"
        "<i>🌐 Questions are in Russian for now — the English pack is coming soon!</i>"
    ),
    "quiz.btn_new": "🧠 New question",
    "quiz.timeout": "⏰ <b>TIME'S UP!</b> You get {seconds} seconds to answer.",
    "quiz.stale": "⏳ This question is no longer active. Start a new one!",
    "quiz.stale_alert": "This question is no longer active. Start a new one!",
    "quiz.empty": "⚠️ The question base is empty. Tell the administrator.",
    "quiz.result_header": "📊 <b>RESULT</b>",
    "quiz.correct": "✅ <b>Correct!</b>",
    "quiz.wrong": "❌ <b>Wrong.</b> The correct answer: <code>{correct}</code>",

    # ---------------- Heads/Tails ----------------
    "coin.intro": (
        "🪙 <b>HEADS OR TAILS</b>\n\n"
        "The bot flips a cyber-coin. Guess which side it lands on!\n"
        "Win: <b>+{reward}</b> · Loss: <b>-{penalty}</b> · Limit: <b>{limit}</b> wins"
    ),
    "coin.heads": "🦅 Heads",
    "coin.tails": "🪙 Tails",
    "coin.result": "🪙 The coin spins... it's <b>{result}</b>! Your bet: {choice}.",

    # ---------------- Dice ----------------
    "dice.intro": (
        "🎲 <b>DICE</b>\n\n"
        "You and the bot each roll a die. Higher roll takes the round!\n"
        "Win: <b>+{reward}</b> · Loss/draw: <b>-{penalty}</b> · Limit: <b>{limit}</b> wins"
    ),
    "dice.btn_roll": "🎲 ROLL THE DICE",
    "dice.toast": "Dice rolled!",
    "dice.result": "🎲 Your die (first): <b>{player}</b> · Bot's die: <b>{bot}</b>",

    # ---------------- Safe ----------------
    "safe.intro": (
        "🔐 <b>CYBER-SAFE</b>\n\n"
        "Inside — a <b>{jackpot} rofl</b> jackpot! The door is locked with a code from 1 to {codes}. "
        "You get one try.\n"
        "Cracked: <b>+{jackpot}</b> · Alarm: <b>-{penalty}</b> · Limit: <b>{limit}</b> wins"
    ),
    "safe.btn_retry": "🔐 Crack it again!",
    "safe.win": "🔓 <b>Safe cracked!</b> The code was: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Alarm triggered!</b> You entered {guess}, the code was: <b>{code}</b>.",

    # ---------------- duels ----------------
    "duel.intro": (
        "⚔️ <b>1-ON-1 DUELS: ROCK-PAPER-SCISSORS FOR A STAKE</b>\n"
        "..................................................\n\n"
        "Pick a table that fits your wallet — just like poker. The stake is taken "
        "immediately, and your opponent is a real ROFL HUB player!\n\n"
        "💰 The pot = both stakes. The winner takes <b>{payout_percent}%</b> of the pot, "
        "<b>{burn_percent}%</b> burns forever (deflation!).\n"
        "🤝 A draw means an instant gesture replay — the pot stays on the table.\n"
        "⏱ You get <b>{move_timeout} seconds</b> per gesture; stay silent and the random "
        "generator picks for you.\n"
        "🏆 Duel wins count for your team in Battles!\n\n"
        "👇 <b>PICK A TABLE:</b>"
    ),
    "duel.btn_table": "⚔️ Table {stake} rofls",
    "duel.btn_cancel": "❌ Leave the table (refund stake)",
    "duel.btn_move_rock": "🪨 Rock",
    "duel.btn_move_scissors": "✂️ Scissors",
    "duel.btn_move_paper": "🧻 Paper",
    "duel.waiting": (
        "🪑 <b>You're at the {stake} rofl table.</b> Your stake is in the pot.\n"
        "Waiting for a second fighter... Once they sit down, you'll both get the gesture pick!\n"
        "<i>The queue lives {ttl} minutes, then your stake returns automatically.</i>"
    ),
    "duel.cancelled": "🚪 You left the table. The <b>{stake} rofl</b> stake is back on your balance.",
    "duel.expired": "⌛ No opponent showed up at the {stake} table. Your <b>{stake} rofl</b> stake was refunded.",
    "duel.matched": (
        "⚔️ <b>OPPONENT FOUND! Table {stake} rofls.</b>\n"
        "Pot: <b>{bank} rofls</b> · Winner takes: <b>{payout}</b>\n\n"
        "⏱ You have <b>{timeout} seconds</b> to pick your gesture!"
    ),
    "duel.move_saved": "✊ Gesture locked in! Waiting for your opponent...",
    "duel.draw_replay": (
        "🤝 <b>DRAW! Round {round}.</b> Both showed the same gesture.\n"
        "The pot stays. ⏱ {timeout} seconds again — pick your gesture:"
    ),
    "duel.win": (
        "🏆 <b>THE DUEL IS YOURS!</b>\n\n"
        "Your {winner_move} beats {loser_move}.\n"
        "💰 Winnings: <b>+{payout} rofls</b> · 🔥 Burned from the pot: {burned}\n"
        "💼 Balance: <b>{balance} rofls</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL LOST.</b>\n\n"
        "The opponent's {winner_move} beats your {loser_move}.\n"
        "📉 Your <b>{stake} rofl</b> stake went to the winner's pot.\n"
        "Rematch?"
    ),
    "duel.reaper_prefix": "⏰ <b>Round timeout!</b> The missing gestures were picked by the random generator.\n\n",
    "duel.bad_table": "❌ No such table exists.",
    "duel.already_in": "⚠️ You're already at a table or in a fight! Finish your current duel first.",
    "duel.no_coins": "❌ You need {stake} rofls on your balance for this table.",
    "duel.cancel_impossible": "⚠️ This queue can no longer be cancelled (an opponent was found or the table is closed).",
    "duel.not_active": "⌛ This duel is already over.",
    "duel.not_participant": "🔒 This is not your duel!",
    "duel.move_already": "✋ You already showed your gesture this round. Waiting for the opponent!",
    "duel.bad_move": "❌ Unknown gesture.",
    "duel.btn_rematch": "⚔️ Rematch (back to tables)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",

    # ---------------- referral ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB REFERRAL PROGRAM</b>\n"
        "..................................................\n\n"
        "Invite friends and get <b>+{bonus} rofls</b> for everyone "
        "who registers via your personal link!\n\n"
        "🔗 <b>Your link (tap to copy):</b>\n<code>{link}</code>\n\n"
        "📊 <b>YOUR STATS:</b>\n"
        "👥 Friends invited: <b>{invited}</b>\n"
        "💰 Earned from referrals: <b>{earned} rofls</b>\n\n"
        "..................................................\n"
        "<i>Share the link with classmates, friends and socials — the bigger the crew, the faster your balance grows!</i>"
    ),
    "ref.btn_share": "📣 Share the link",
    "ref.share_text": "Join the ROFL HUB gaming ecosystem!",

    # ---------------- transfers ----------------
    "tr.help": (
        "🔄 <b>SEND ROFLS TO ANOTHER PLAYER</b>\n"
        "..................................................\n\n"
        "Command format:\n"
        "<code>/transfer ID amount</code> — by Passport ID (see /profile)\n"
        "<code>/transfer @username amount</code> — by username\n"
        "<code>/transfer ROFL-HUB-777 amount</code> — by an auction VIP ID\n\n"
        "Examples:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Minimum amount: <b>{min} rofls</b>"
    ),
    "tr.not_found": "❌ Recipient not found. Check the Passport ID or @username — the player must be registered in the bot.",
    "tr.self": "🤨 You can't transfer coins to yourself — that would be a perpetual economy!",
    "tr.blocked": "🚫 This player is blocked — transfers to them are unavailable.",
    "tr.min": "❌ The minimum transfer is {min} rofls.",
    "tr.insufficient": "❌ Not enough rofls! Your balance: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Not enough rofls on your balance.",
    "tr.confirm": (
        "🔄 <b>CONFIRM THE TRANSFER:</b>\n\n"
        "👤 Recipient: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Amount to send: <b>{amount} rofls</b>{fee_line}\n"
        "💰 The recipient gets: <b>{received} rofls</b>\n\n"
        "<i>Transfers cannot be undone — double-check the recipient!</i>"
    ),
    "tr.fee_line": "\n🔥 Hub fee: <b>{fee} rofls</b> (burned)",
    "tr.btn_confirm": "✅ CONFIRM TRANSFER",
    "tr.btn_cancel": "❌ Cancel",
    "tr.cancelled_toast": "Transfer cancelled",
    "tr.cancelled": "❌ <b>Transfer cancelled.</b> Your coins stayed put.",
    "tr.not_yours": "🔒 This is not your transfer!",
    "tr.done_toast": "✅ Transfer complete!",
    "tr.done": (
        "✅ <b>TRANSFER COMPLETE!</b>\n\n"
        "💸 Sent: <b>{amount} rofls</b> to player ID <code>{recipient_id}</code>\n"
        "💰 Your balance: <b>{balance} rofls</b>"
    ),
    "tr.received": (
        "💰 <b>You received {amount} rofls!</b>\n"
        "Sender: ID <code>{sender_id}</code>. Your balance is already topped up — check /profile!"
    ),

    # ---------------- shop & payments ----------------
    "shop.header": "🏪 <b>ROFL HUB SHOP</b>\nPurchases go through official Telegram Stars. Pick a category with the buttons below.",
    "shop.cat_farm": (
        "🚜 <b>SHOP · FOR THE FARM</b>\n"
        "..................................................\n"
        "Robots for 30 days, fuel, fridges, boosts and the Master Drone.\n"
        "📦 Your fridge now holds: <b>{capacity} cutlets</b>\n"
        "..................................................\n"
        "👇 <b>Pick an item:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>SHOP · GAMING</b>\n"
        "..................................................\n"
        "Win-limit removal, rofl packs and the Mega-Clan license.\n"
        "..................................................\n"
        "👇 <b>Pick an item:</b>"
    ),
    "pay.invoice_desc": "Instant delivery of ROFL HUB in-game content.",
    "pay.invoice_error": "⚠️ Couldn't create the Telegram Stars invoice. Try again later.",
    "pay.success": "🎉 <b>Payment confirmed!</b>\n🧾 <code>{charge}</code>\n💵 Charged: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 The payment went through, but delivery temporarily failed. We're already on it.\n"
        "Keep your payment number: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Your Stars were refunded automatically.",
    "pay.keep_charge": "Keep the payment number for a refund: <code>{charge}</code>",
    "pay.already": "✅ This payment was already processed, the item was delivered earlier.",
    "pay.support": (
        "🛟 <b>TELEGRAM STARS PAYMENT SUPPORT</b>\n"
        "..................................................\n\n"
        "All ROFL HUB items are digital and delivered instantly after payment.\n\n"
        "⚙️ <b>If you paid but the item didn't arrive:</b>\n"
        "the bot refunds Stars automatically when delivery fails. If that didn't happen — "
        "send your payment number here (it's in the receipt, format <code>xxxx...</code>) and describe "
        "the problem. The administration will check the payment in the database and resolve it within 24 hours.\n\n"
        "💫 <b>Refund policy:</b>\n"
        "a refund is possible if the item was not received or was delivered incorrectly. "
        "Correctly delivered digital items are non-refundable.\n\n"
        "..................................................\n"
        "<i>This section is the official purchase support point per Telegram rules.</i>"
    ),

    # ---------------- delivery ----------------
    "dlv.cutlets": "🥩 Added to your inventory: <b>{qty} cutlets</b>.",
    "dlv.miner": "🤖 Robot <b>“{name}”</b> delivered to your farm.\n⏳ Service life: until <b>{until} UTC</b>.",
    "dlv.miner_junior": "Miner Bot",
    "dlv.miner_premium": "Cyber-Driller",
    "dlv.fridge": "📦 Fridge expanded to <b>{capacity} cutlets</b>.",
    "dlv.coins": "💰 Credited <b>+{amount} rofls</b>.",
    "dlv.boost_nuclear": "🔋 Nuclear Boost x5 active until <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Nitrogen Cooling +40% active until <b>{until} UTC</b>.",
    "dlv.drone": "🛸 The Master Drone guards your farm until <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Win limits removed until <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Your team received the <b>MEGA-CLAN</b> status: up to {max} seats.",
    "dlv.err_fridge": "You already own a fridge of this size or bigger.",
    "dlv.err_no_team": "You don't have a team yet. Create one first via /create_team.",
    "dlv.err_mega": "Your team already has the Mega-Clan status.",

    # ---------------- teams/clans (main surfaces) ----------------
    "clan.no_team": "⚠️ <b>You don't have a team yet!</b>\n\nYou can register your own crew right now by tapping the button below.",
    "clan.btn_create": "🏆 Create a Team for 100k",
    "clan.btn_members": "👥 TEAMMATE LIST",
    "clan.btn_leave": "🚪 Leave the team / Quit the crew",
    "clan.btn_dashboard": "🏆 Team dashboard",
    "clan.status_clan": "👑 STATUS: EMPIRE CLAN",
    "clan.status_team": "👥 STATUS: REGULAR TEAM",
    "clan.dashboard": (
        "🏆 <b>YOUR TEAM'S DASHBOARD</b>\n"
        "..................................................\n\n"
        "📌 Name: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Crew captain: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Motto: <i>“{motto}”</i>\n"
        "🔮 Emblem symbol: {symbol}\n\n"
        "👥 Members: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGATION:</b>"
    ),
    "clan.members_only": "🔒 The member list is visible only to members of this team!",
    "clan.members_gone": "❌ This team has already been disbanded.",
    "clan.members_header": (
        "👥 <b>TEAM “{name}” ROSTER</b>\n"
        "🧠 — game intellect level (trained only in /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Page <b>{page} / {pages}</b> · Total fighters: <b>{members}</b>\n"
        "<i>Tap a teammate's @username to message them, build your own chat "
        "and call the crew to team battles!</i>"
    ),
    "clan.btn_prev": "⬅️ Back",
    "clan.btn_next": "Next ➡️",
    "clan.join_ok": (
        "🎉 <b>CONGRATULATIONS, YOU'RE IN!</b>\n\nYou joined team <b>{name}</b>!\n"
        "📍 Use /my_team to check the roster!"
    ),
    "clan.leave_ok": "🚪 You left team <b>{name}</b>. You're a free bird now!",
}

STRINGS: dict[str, dict[str, str]] = {"ru": RU, "en": EN}


def t(lang: str | None, key: str, **kwargs) -> str:
    """Текст по ключу на языке игрока. ru — эталон и запасной вариант."""
    resolved = resolve_lang(lang)
    template = STRINGS[resolved].get(key) or RU[key]
    return template.format(**kwargs) if kwargs else template
