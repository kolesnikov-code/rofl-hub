"""
Единый источник чисел экономики Cyber Barons.

Все спорные величины из ТЗ живут ЗДЕСЬ и только здесь. Меняется константа —
меняется поведение всего бота. Никаких «магических чисел» в обработчиках.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------
# Валюта и стартовые бонусы
# --------------------------------------------------------------------------
AWAY_MIN_MINUTES = 10         # «Пока тебя не было» (владелец 13.11): окно — если приложение не открывали дольше
START_BALANCE = 500           # монет при регистрации (решение владельца 28.10: было 1000)
START_CUTLETS_INVENTORY = 1   # кибер-котлет на склад при регистрации
REFERRAL_REVENUE_SHARE = 0.20  # доля от трат реферала (учёт для выплат)
REFERRAL_SHARE_DAYS = 365
# Рефералка (решение владельца 26.10, против фейковых аккаунтов): за регистрацию НИЧЕГО.
# Единственная награда — +500 рефереру ОДИН раз, когда друг стал «активным»: дошёл до
# 3 уровня интеллекта в викторине (60 верных ответов) И забрал 3 ежедневные котлеты
# (кулдаун 24 ч → минимум двое суток живой игры). Флаг — users.qualified_at.
REFERRAL_QUALIFY_QUIZ_LEVEL = 3
REFERRAL_QUALIFY_BONUS_CLAIMS = 3
REFERRAL_QUALIFIED_BONUS = 500
# В ту же разовую награду (уточнение владельца 26.10): котлета на склад и по 10 каждого ресурса
# (ресурсы — с учётом вместимости склада, как любая добыча).
REFERRAL_QUALIFIED_CUTLETS = 1
REFERRAL_QUALIFIED_RESOURCES = 10
# Задание во вкладке «Друзья» (владелец 30.10): столько активных друзей — полный костюм на выбор, один раз
REFERRAL_SUIT_FRIENDS = 10
REFERRAL_TOP_LIMIT = 20       # рейтинг «у кого больше друзей» в приложении

# Удаление аккаунта (решение владельца 26.10): заморозка на 7 дней, потом обезличивание.
ACCOUNT_DELETE_GRACE_DAYS = 7
ACCOUNT_DELETE_CONFIRM_SECONDS = 10   # кнопка «Да, удалить» срабатывает не раньше — успеть прочитать
ACCOUNT_REAPER_INTERVAL_SECONDS = 3600

# --------------------------------------------------------------------------
# Продуктовая аналитика
# --------------------------------------------------------------------------
EVENTS_RETENTION_DAYS = 180       # события старше — чистятся полночным прогоном
VIRAL_WINDOW_DAYS = 14            # окно K-factor: приглашения за 14 дней после регистрации
ACTIVATION_WINDOW_HOURS = 24      # воронка новичка: рег → онбординг → игра → покупка за 24 ч
LIMIT_TO_UNLIMIT_WINDOW_HOURS = 24  # конверсия «упёрся в лимит → купил безлимит» за 24 ч
RETENTION_COHORT_DAYS = (1, 3, 7, 30)
TOP_RICH_PERCENT = 1              # доля монет у топ-N% игроков в отчёте экономики
PROMOTER_CODE_MAX_LEN = 16        # код промоутера/канала: [a-z0-9_-], до 16 символов

# --------------------------------------------------------------------------
# Ферма: роботы
# --------------------------------------------------------------------------
MINER_RATE_PER_HOUR = {
    "intern": 1,    # Робот-Стажёр: бесплатный, вечный, без топлива (решение владельца 22.10)
    "junior": 5,    # Младший Майнер, топливо не нужно
    "premium": 10,  # Кибер-Бурильщик, ест котлеты
}
# Робот-Стажёр: один выдаётся каждому при активации в /farm, ещё по одному — за уровни
# интеллекта, кратные 10 (10, 20, 30…; решение владельца 26.10 — никаких лишних «бесплатных»
# монет). Награда не падает на ферму сама: копится в users.interns_pending и забирается кнопкой.
INTERN_LEVEL_STEP = 10
# Апгрейд Стажёра до ВЕЧНОГО Младшего Майнера (999 ★): нужно не меньше
# INTERN_UPGRADE_REFERRALS активных друзей (3 уровень интеллекта + 3 ежедневные котлеты).
INTERN_UPGRADE_REFERRALS = 3
PERMANENT_ROBOT_YEARS = 100   # «вечный» робот = срок службы 100 лет
MINER_LICENSE_DAYS = 30
CUTLET_ENERGY_SECONDS = 24 * 3600   # одна котлета = 24 часа работы одного бурильщика
PREMIUM_CUTLETS_PER_CYCLE_BASE = 1  # котлет на цикл 24ч без буста
NUCLEAR_FUEL_MULTIPLIER = 3         # расход котлет при Ядерном разгоне
NUCLEAR_SPEED_MULTIPLIER = 5        # скорость добычи при Ядерном разгоне
NITROGEN_BONUS_PERCENT = 40         # Азотное охлаждение: +40% к базовой мощности
BOOST_DAYS = 30
DRONE_DAYS = 365
DAILY_CUTLET_BONUS_COOLDOWN_SECONDS = 24 * 3600

# Внутренняя точность начислений: копим монето-микросекунды, чтобы ни одна
# «копейка времени» не терялась между ленивыми пересчётами.
MINING_ACC_PER_ROFL = 3600 * 1_000_000  # µs работы на 1 монета при ставке 1 монета/ч

# --------------------------------------------------------------------------
# Игры и лимиты
# --------------------------------------------------------------------------
WIN_REWARD = 2
LOSE_PENALTY = 1
SAFE_WIN_REWARD = 5       # Сейф: шанс 1 из 4, выигрыш больше (EV = +0.5 монеты за раунд)
SAFE_CODES_COUNT = 4      # вариантов кода на дверце сейфа
DAILY_WIN_LIMITS = {
    "quiz": 30,
    "rps": 15,
    "hl": 15,
    "safe": 15,
    # 27.10 — новые игры приложения (шаг 2 плана владельца)
    "math": 30,      # ➗ быстрый счёт — как викторина
    "flags": 30,     # 🏳️ флаги и столицы
    "code": 10,      # 💻 взлом кода (быки и коровы) — партия длинная
    "memory": 15,    # 🃏 мемори
}
# Монеты за победу по играм (по умолчанию WIN_REWARD); сложнее игра — щедрее
GAME_WIN_REWARDS = {"safe": 5, "code": 5, "memory": 3}
# «Каждые N побед — ресурс» (решение владельца 27.10): ценный ресурс — за серию, а не за раунд.
# Викторина: 🪨 камень за каждые 10 верных ответов (30 в день → 3 камня), математика — ⚡ за каждые 10.
GAME_MILESTONES = {"quiz": ("stone", 10), "math": ("energy", 10)}
# Предзагрузка следующего вопроса (27.10): таймер стартует, когда вопрос показан (/api/<игра>/start), но не позже
# чем через PREFETCH_SLACK_SECONDS после выдачи — больше форы заранее загруженный вопрос не даёт
PREFETCH_SLACK_SECONDS = 10   # у вопроса и так 20–30 с — 10 с форы не делают погоду, а «Дальше» мгновенный
MATH_ANSWER_SECONDS = 20       # ➗ пример решается быстрее вопроса викторины
FLAGS_ANSWER_SECONDS = 20
CODE_DIGITS = 4                # 💻 4 разные цифры
CODE_MAX_ATTEMPTS = 10         # не взломал за 10 попыток — проигрыш
MEMORY_PAIRS = 6               # 🃏 12 карточек
MEMORY_MAX_MOVES = 12          # нашёл все пары за ≤ 12 ходов (ход = открыть две карточки) — победа
DEFAULT_DAILY_WIN_LIMIT = 15
QUIZ_ANSWER_SECONDS = 30   # 26.10: владелец — «за 15 секунд только переварить вопрос успеваю» (было 15, до того 10)
# Игры в приложении (26.10): викторина раундами по 10 вопросов, подсказка 50/50 за монеты (сгорают),
# небольшой запас на сеть при ответе (таймер считает сервер — ответ после него засчитывается как «не успел»)
QUIZ_ROUND_SIZE = 10
QUIZ_HINT_COST = 10
# ⚠️ Жалоба на вопрос (владелец 27.10): после ответа в приложении; не больше N жалоб в сутки UTC на игрока
QUIZ_REPORT_DAILY_LIMIT = 20
GAME_ANSWER_GRACE_SECONDS = 3
# Прогрессивные уровни викторины (решение владельца 13.10.2026):
# уровень N закрывается за N*10 верных ответов (счётчик итерации обнуляется),
# награда за уровень N — N*100 монет. 1-й: 10 ответов → +100; 100-й: 1000 → +10 000.
QUIZ_LEVEL_STEP_ANSWERS = 10
QUIZ_LEVEL_REWARD_PER_LEVEL = 100


def win_reward_for(game_type: str) -> int:
    """Выигрыш за раунд: у сложных игр и Сейфа (ниже шанс) повышенный, у остальных базовый."""
    if game_type == "safe":
        return SAFE_WIN_REWARD
    return GAME_WIN_REWARDS.get(game_type, WIN_REWARD)


def quiz_answers_required(level: int) -> int:
    """Сколько верных ответов нужно набрать в итерации, чтобы закрыть уровень level."""
    if level <= 0:
        raise ValueError("level must be positive")
    return level * QUIZ_LEVEL_STEP_ANSWERS


def quiz_level_reward(level: int) -> int:
    """Награда за закрытие уровня level."""
    if level <= 0:
        raise ValueError("level must be positive")
    return level * QUIZ_LEVEL_REWARD_PER_LEVEL
UNLIMIT_DAY_HOURS = 24
UNLIMIT_MONTH_DAYS = 30

# --------------------------------------------------------------------------
# Команды, дуэли, турниры
# --------------------------------------------------------------------------
TEAM_CREATE_COST = 100_000
TEAM_MAX_MEMBERS = 50
# 🛡 ОТРЯДЫ (владелец 27.10, после оценки 9 агентов: «половина вкладок недоступна одиночке»): маленькая команда
# до 5 бойцов за 7 500 🪙 — все командные механики (станция, взаимопомощь, биржа команды, налёты, битвы, рудники).
# Капитан может расширить отряд до команды, доплатив разницу (итого столько же, сколько команда сразу).
SQUAD_CREATE_COST = 7_500
SQUAD_MAX_MEMBERS = 5
SQUAD_UPGRADE_COST = TEAM_CREATE_COST - SQUAD_CREATE_COST
MEGA_CLAN_MAX_MEMBERS = 1000
TEAM_LIST_PAGE_SIZE = 25      # тиммейтов на страницу в /my_team (Мега-Клан — до 40 страниц)
TEAM_NAME_MAX_LEN = 32
TEAM_MOTTO_MAX_LEN = 100
TEAM_SYMBOL_MAX_LEN = 5
TEAM_ROULETTE_SIZE = 6        # случайных свободных команд в рулетке приложения (в чате — 3)
TEAM_SEARCH_LIMIT = 20

# --------------------------------------------------------------------------
# Дуэли: 3 уровня столов «как в покере», сжигание 20% банка
# --------------------------------------------------------------------------
DUEL_TABLES = (10, 100, 1000)          # ставки столов, монет
DUEL_MOVE_TIMEOUT_SECONDS = 60         # на выбор жеста; не успел — жест случайный
DUEL_WAITING_TTL_MINUTES = 30          # очередь без соперника отменяется с возвратом ставки
# ⚔️ Вызов друга по ссылке (27.10): приватная дуэль ждёт именно этого друга сутки, потом ставка возвращается
DUEL_INVITE_TTL_HOURS = 24
DUEL_INVITE_CODE_LEN = 8
# 🕵️ ДЕЛО ДНЯ (27.10): одно мини-дело на всех в сутки UTC. Первая улика бесплатно, каждая следующая — «ход».
# Награда только за раскрытие и тем больше, чем меньше улик понадобилось (индекс = открытых улик).
DAILY_CASE_REWARD = {1: 40, 2: 30, 3: 20, 4: 10}   # 27.10, вечер: под новые награды квестов (20–50)
DAILY_CASE_STREAK_BONUS_EVERY = 7       # каждый 7-й день серии раскрытых дел — бонус
DAILY_CASE_STREAK_BONUS = 50
# 📸 Карточка достижений: картинка хранится в памяти сервера для «поделиться», не дольше часа и не больше 2 МБ
SHARE_CARD_TTL_SECONDS = 3600
SHARE_CARD_MAX_BYTES = 2_000_000

# --------------------------------------------------------------------------
# Переводы монет между игроками
# --------------------------------------------------------------------------
TRANSFER_MIN_AMOUNT = 10
# Переводы отправлять могут только «активные» аккаунты — тот же порог, что у активного друга
# в рефералке (решение 26.10: фейки со стартовыми 1000 🪙 не сливают монеты на основной).
TRANSFER_SENDER_MIN_QUIZ_LEVEL = 3
TRANSFER_SENDER_MIN_BONUS_CLAIMS = 3
TRANSFER_FEE_PERCENT = 0      # комиссия сжигается; на старте 0, поднять — одно число


def transfer_fee(amount: int) -> int:
    return amount * TRANSFER_FEE_PERCENT // 100


# --------------------------------------------------------------------------
# Биржа котлет (решение владельца 22.10): P2P котлеты за монеты, комиссия сжигается
# --------------------------------------------------------------------------
MARKET_FEE_PERCENT = 10        # сгорает с каждой продажи — дефляция монет (платит продавец)
MARKET_MIN_PRICE = 1           # минимальная цена ресурса, 🪙 за штуку
MARKET_MAX_PRICE = 100_000
MARKET_MAX_QTY = 100           # котлет в одном ордере
MARKET_RESOURCE_MAX_QTY = 1000  # ресурса в одном ордере
MARKET_MAX_OPEN_ORDERS = 8     # открытых ордеров на игрока (все товары и обе стороны вместе)
MARKET_SHOWCASE_LIMIT = 6      # ордеров на витрине /market (по одной кнопке в ряд)
MARKET_APP_LIST_LIMIT = 200    # лучших ордеров в приложении — листаются постранично
MARKET_APP_SWAPS_LIMIT = 100   # предложений обмена в приложении
# Новые сырьё и материалы (27.10) торгуются; ☢️ Ядро — тоже, но только за монеты и от 5000 (решение 26.10)
MARKET_ASSETS = ("cutlet", "metal", "hydrogen", "crystal", "parts",
                 "stone", "wood", "fire", "energy", "battery", "cow", "core")
# ПОЛЫ ЦЕН (решение владельца 26.10, расчёт — в CLAUDE.md): дешевле не продать и не заявить на покупку.
# Чем дороже товар, тем больше монет сгорает комиссией с каждой сделки — владелец стимулирует торговлю ради сжигания.
# Логика: лёгкие в добыче (детали, кристаллы) дешевле, сырьё бустов (металл, водород) дороже — бусты из
# купленных ресурсов всегда дороже магазинных за ★; огонь и батарейки — не дешевле своих ингредиентов
# (огонь: 10 🪵 + 5 🪨 = 850 за 5; батарейки: 5 ⚡ + 5 ⛏ + 1 🔥 = 500 за 2, +20% за труд и инструменты).
MARKET_MIN_PRICES = {
    "parts": 10, "crystal": 10, "metal": 20, "hydrogen": 20, "stone": 30, "energy": 50, "wood": 70,
    "fire": 170, "battery": 300,
    "cow": 1000,       # 🐄 = 3 котлеты в мастерской; её берут те, кому срочно нужно топливо на Ядерный разгон
    "core": 5000,      # ☢️ только из призов владельца — самый редкий товар
    "cutlet": 200,     # пол котлеты — см. ниже (защита магазина)
}
MARKET_COW_MIN_PRICE = MARKET_MIN_PRICES["cow"]
MARKET_HISTORY_DAYS = 7        # график цены и индекс биржи

# ПОЛ ЦЕНЫ КОТЛЕТЫ (решение владельца 24.10): топливо — исключительное право магазина.
# Котлета на бирже не может стоить меньше, чем котлета из магазина в пересчёте на монеты:
# самый выгодный пак котлет 100 шт. = 449 ★ (4,49 ★/шт), самый выгодный пак монет
# 100 000 🪙 = 2499 ★ (≈40 🪙/★) → 4,49 × 40 ≈ 180 🪙. Пол 200 🪙 — с запасом:
# Звёздами котлета всегда выгоднее, а на бирже её берут «киты» с бустами (с Ядерным
# разгоном котлета приносит до 560 🪙), когда в магазин идти не хочется.
SHOP_CUTLET_BEST_STARS_X100 = 449   # ★ за 100 котлет (самый выгодный пак) — сверяется тестом с каталогом
SHOP_COINS_PER_STAR_BEST = 40       # 🪙 за ★ в самом выгодном паке монет — сверяется тестом
MARKET_CUTLET_MIN_PRICE = MARKET_MIN_PRICES["cutlet"]


def market_min_price(asset: str) -> int:
    if asset.startswith("g_"):
        return GEAR_MIN_PRICE   # 🧥 деталь костюма (30.10)
    if asset.startswith("a_"):
        return ARTIFACT_MIN_PRICE   # 💠 артефакт (30.10)
    if asset.startswith("s_"):
        return 300                  # ✨ скин: точный пол — по редкости экземпляра (shared/skins.SKIN_MIN_PRICE)
    return MARKET_MIN_PRICES.get(asset, MARKET_MIN_PRICE)


# Анти-фейк биржи (аудит 26.10, 2.3–2.6):
# новый (неактивный) аккаунт покупает не дороже N× минимальной цены — иначе фейк со стартовыми монетами
# «покупает» 1 деталь у основного аккаунта за 500 и обходит порог переводов;
MARKET_NEWBIE_PRICE_MULT = 3
# обмен ресурс ↔ ресурс: ценности сторон (по минимальным ценам) различаются не больше чем во столько раз
SWAP_MAX_VALUE_RATIO = 3
# командные награды (битвы, походы, рудники) — только тем, кто в команде не меньше суток (аудит 2.7)
TEAM_REWARD_MIN_HOURS = 24


def team_veteran_sql(alias: str, moment_sql: str) -> str:
    """SQL: игрок alias в команде не меньше TEAM_REWARD_MIN_HOURS к моменту moment_sql (NULL — старожил)."""
    return (f"COALESCE({alias}.team_joined_at, '-infinity'::timestamptz) <= "
            f"({moment_sql}) - make_interval(hours => {int(TEAM_REWARD_MIN_HOURS)})")


def swap_value_ok(give_kind: str, give_qty: int, want_kind: str, want_qty: int) -> bool:
    give, want = give_qty * market_min_price(give_kind), want_qty * market_min_price(want_kind)
    return max(give, want) <= SWAP_MAX_VALUE_RATIO * min(give, want)


# Обмен ресурс ↔ ресурс без монет (предложения «отдам X за Y»)
SWAP_MAX_OPEN = 5
SWAP_MAX_QTY = 10_000


# Биржа команды (решение владельца 26.10): лоты видят и покупают только тиммейты, комиссия ниже
# общей — мотивация собирать команду и прокачивать её до Мега-Клана (за Stars). Пол цены котлеты
# действует и внутри команды: топливо из магазина по-прежнему выгоднее.
TEAM_MARKET_FEE_PERCENT = 5
CLAN_MARKET_FEE_PERCENT = 2


def team_market_fee_percent(max_members: int) -> int:
    """Комиссия биржи команды: Мега-Клан — 2%, обычная команда — 5% (общая биржа — 10%)."""
    return CLAN_MARKET_FEE_PERCENT if max_members >= MEGA_CLAN_MAX_MEMBERS else TEAM_MARKET_FEE_PERCENT


def market_fee(total: int, shuttle: bool = False, team_percent: int | None = None) -> int:
    """
    Комиссия сделки (платит продавец); Шаттл ПРОДАВЦА — льготная, чужим Шаттлом не воспользоваться.
    team_percent — сделка на бирже команды: берётся меньшая из ставок.
    """
    percent = SHUTTLE_MARKET_FEE_PERCENT if shuttle else MARKET_FEE_PERCENT
    if team_percent is not None:
        percent = min(percent, team_percent)
    fee = total * percent // 100
    return max(fee, 1) if total > 0 and percent > 0 else fee   # мелкая сделка не становится бесплатным переводом


# Взаимопомощь в команде: тиммейт просит ресурс — остальные дарят. Только ресурсы (котлеты —
# топливо из магазина, их не дарят), дарить могут только активные аккаунты, лимит на дарителя в сутки.
TEAM_HELP_MAX_QTY = 200          # максимум одной просьбы
TEAM_HELP_DAILY_GIVE = 100       # сколько ресурсов один игрок может подарить за сутки UTC
TEAM_HELP_LIST_LIMIT = 50
# Дарить ресурсы может только активный аккаунт (владелец 30.10 смягчил 7 ур. + 10 котлет до порога друга;
# фермы фейков ловит раздел «🕵️ Проверка» пульта — shared/abuse.py)
TEAM_HELP_GIVER_MIN_QUIZ_LEVEL = REFERRAL_QUALIFY_QUIZ_LEVEL      # владелец 30.10: порог «активного аккаунта» (3 ур. + 3 котлеты)
TEAM_HELP_GIVER_MIN_BONUS_CLAIMS = REFERRAL_QUALIFY_BONUS_CLAIMS

# --------------------------------------------------------------------------
# СКЛАД ИЗДЕЛИЙ (решение владельца 26.10): всё, что собрано в мастерской приложения
# (часы бустов, дрона, щита, пробники Безлимита), ложится на склад и включается кнопкой,
# когда игроку удобно. Постоянные улучшения (броня, склад, Шаттл) действуют сразу.
# --------------------------------------------------------------------------
# Порядок = порядок плашек на складе. Виды изделий:
# - часовые личные (ITEM_COLUMNS: продлевают users.<колонка>) и Термос (окно thermos_from/until);
# - часовые командные (TEAM_ITEM_EFFECTS: Знамя — окно бонуса добычи, Купол — щит всей команды);
# - разовые (ONE_SHOT_COLUMNS: «заряд» на следующее действие; Форсаж — сразу сбрасывает перезарядку).
ITEM_EFFECTS = (
    "nitrogen", "nuclear", "drone", "shield", "unlimit",
    "camo", "trap", "drill", "thermos", "banner", "dome",
    "meds", "forsage", "economizer", "cargo", "stamp",
)
ITEM_COLUMNS = {
    "nitrogen": "boost_nitrogen_until",
    "nuclear": "boost_nuclear_until",
    "drone": "drone_until",
    "shield": "raid_shield_until",
    "unlimit": "unlimit_until",
    "camo": "raid_camo_until",       # 🎭 не показываться в разведке
    "trap": "raid_trap_until",       # 🪤 провалившийся налётчик отдаёт вдвое больше
    "drill": "raid_drill_until",     # 🎯 ничья в обороне засчитывается как провал налётчика
    "meds": "meds_until",            # 💊 иммунитет: без него в походах «болеют» и теряют часть добычи
}
TEAM_ITEM_EFFECTS = ("banner", "dome")
ONE_SHOT_COLUMNS = {
    "economizer": "raid_free_fuel",  # ⛽ следующий вылет без водорода
    "cargo": "raid_cargo",           # 📦 добыча следующего налёта +50%
    "stamp": "market_free_sales",    # 📜 следующая продажа на бирже без комиссии
}
ITEM_FARM_EFFECTS = ("nitrogen", "nuclear", "drone", "thermos")   # меняют ферму — закрыть прошлое время
THERMOS_FUEL_CYCLE_SECONDS = 24 * 3600 * 4 // 3   # 🧊 котлеты хватает на 32 ч вместо 24 (едят на 25% медленнее)
BANNER_BONUS_PERCENT = 5          # 🏳️ Знамя: +5% к добыче всей команде
CARGO_LOOT_PERCENT = 150          # 📦 Трюм: добыча налёта ×1,5 (и потолок ×1,5)
TRAP_FAIL_MULTIPLIER = 2          # 🪤 Приманка: провалившийся налётчик отдаёт вдвое больше
FORSAGE_COOLDOWN_HOURS = 24       # 🔥 Форсаж — не чаще раза в сутки
# Ремдрон станции убран (решение владельца 27.10: ресурсы из воздуха не создаём)

# --------------------------------------------------------------------------
# РУДНИКИ (решение владельца 26.10): карта на 40 рудников, каждая битва команд — ровно за
# один рудник. Победитель держит его 72 ч: КАЖДЫЙ боец команды получает 1 ресурс рудника в час.
# Потом рудник свободен, но захватить его можно только в новой битве.
# --------------------------------------------------------------------------
MINES_COUNT = 30                  # сид рудников — shared/database.py (тест сверяет); 28.10 ночью: 100 → 30
MINE_HOLD_HOURS = 24              # 28.10: рудник у команды сутки — поиграть успеют все
MINE_YIELD_PER_MEMBER_HOUR = 1
MINE_PAYOUT_INTERVAL_SECONDS = 300


# 30 рудников — 6 ресурсов ПОРОВНУ, по 5 каждого (28.10); Ядра на рудниках нет, ⚡ — из игр и сундука
MINE_KINDS = ("metal", "hydrogen", "crystal", "parts", "stone", "wood")
MINE_CORE_EVERY_HOURS = 24        # ☢️ каждые сутки удержания — каждому бойцу 1 Ядро (не больше 3 за рудник)
MINE_SICK_EVERY_HOURS = 7         # 💊 без Аптечки каждый 7-й час добычи «болеешь» (≈15% потерь)


def mine_kind(mine_id: int) -> str:
    """Ресурс рудника: по кругу металл → водород → кристаллы → детали → камень → древесина → ⚡."""
    return MINE_KINDS[(mine_id - 1) % len(MINE_KINDS)]
DUEL_BURN_PERCENT = 20
# ⚡ С Безлимитом («премиум» на сутки или месяц) комиссия победителя вдвое ниже (владелец 27.10, вечер)
DUEL_BURN_PERCENT_PREMIUM = 10


# --------------------------------------------------------------------------
# РЕСУРСЫ (волна 22.10, вечер): в каждой игре добывается свой ресурс — клей экосистемы.
# Ресурсы не покупаются за Stars и не продаются за монеты: только добыча и мастерская.
# --------------------------------------------------------------------------
RESOURCE_KINDS = ("metal", "hydrogen", "crystal", "parts")
GAME_RESOURCE = {          # игра → ресурс за победу
    "rps": "metal",        # ⛏ Металл — КНБ (и дуэли)
    "hl": "hydrogen",      # 💧 Водород — Больше/Меньше
    "quiz": "crystal",     # 💎 Кристаллы — Викторина (+ 🪨 за каждые 10 верных — GAME_MILESTONES)
    "safe": "parts",       # ⚙️ Детали — Кибер-Сейф (шанс 1 из 4 — даём больше)
    "flags": "crystal",    # 💎 Флаги и столицы
    "code": "parts",       # ⚙️ Взлом кода — логика, детали ×2
    "memory": "hydrogen",  # 💧 Мемори
    # ➗ математика — без ресурса за раунд: ⚡ за каждые 10 верных (GAME_MILESTONES)
}
RESOURCE_PER_WIN = {"rps": 1, "hl": 1, "quiz": 1, "safe": 3, "flags": 1, "code": 2, "memory": 1}
# Дуэли НЕ добывают ресурсы (владелец 27.10, вечер): только ставки монет и комиссия — ресурсы дают другие игры
# 🗺 Ротация квестов v2 (владелец 27.10): в списке до 10 квестов (эпики — сверх, их включает владелец отдельно);
# за сутки UTC засчитываются 3 НОВЫХ прохождения, потом непройденные гаснут до 00:00 (Безлимит снимает ограничение);
# переигрывать пройденное можно сколько угодно.
QUEST_ROTATION_SIZE = 10
QUEST_DAILY_NEW = 3
# Награда за ПЕРВОЕ прохождение (владелец 27.10, вечер: «квесты так быстро набивают кошельки — спрос на роботов упадёт»):
# обычный квест 20–50 🪙 (reward_coins в JSON, валидатор держит вилку) и 1–2 🪨 камня, эпик — ровно 100 🪙 и 5 🪨.
QUEST_REWARD_MIN, QUEST_REWARD_MAX = 20, 50
QUEST_EPIC_REWARD = 100
QUEST_STONE_KIND = "stone"
QUEST_STONE_SMALL, QUEST_STONE_BIG, QUEST_STONE_EPIC = 1, 2, 5
QUEST_STONE_BIG_FROM = 40     # квест с наградой от 40 🪙 (длиннее и сложнее) даёт 2 камня


def quest_stones(reward_coins: int, epic: bool) -> int:
    if epic:
        return QUEST_STONE_EPIC
    return QUEST_STONE_BIG if reward_coins >= QUEST_STONE_BIG_FROM else QUEST_STONE_SMALL
RESOURCE_MAX_STOCK = 100_000  # технический потолок запаса на ресурс (защита от переполнения)
# СКЛАД С ЛИМИТОМ (решение владельца 25.10): добыча сверх вместимости пропадает — ресурсы
# не лежат мёртвым грузом, их тратят или продают на бирже. Расширение — в мастерской.
RES_CAPACITY_BASE = 500           # вместимость на КАЖДЫЙ ресурс

# --------------------------------------------------------------------------
# НОВЫЕ РЕСУРСЫ (решение владельца 27.10: «экономика с хитростью, чтобы интерес не угасал»).
# Склад, вместимость и журнал — те же, что у базовых (user_resources / resource_ledger).
# RESOURCE_KINDS (4 базовых) по-прежнему участвуют в налётах, станции, взаимопомощи и сундуке;
# новые — в своих механиках. Откуда берутся:
#   🪨 камень — дуэли, рудники, сундук;   🪵 древесина — квесты, рудники, сундук;
#   🔥 огонь — Костёр в мастерской (древесина + камень);   ⚡ электричество — шанс в любой победе, рудники, сундук;
#   🔋 батарейки — мастерская (⚡ + металл + огонь);   🐄 коровы — квесты, 7-й день серии сундука, биржа;
#   ☢️ Ядро — ТОЛЬКО командные активности: призовые места битв и сутки удержания рудника.
# --------------------------------------------------------------------------
EXTRA_KINDS = ("stone", "wood", "fire", "energy", "battery", "cow", "core")
ALL_KINDS = RESOURCE_KINDS + EXTRA_KINDS
# Обмен ресурс ↔ ресурс (без монет) — без Ядра: оно продаётся только за монеты не дешевле пола
TRADEABLE_KINDS = RESOURCE_KINDS + ("stone", "wood", "fire", "energy", "battery", "cow")
ENERGY_WIN_CHANCE_PERCENT = 25    # ⚡ шанс получить 1 электричество за любую победу в соло-игре
CHEST_SPECIALS = (("wood", 10), ("stone", 10), ("energy", 3))   # особый бонус сундука (по дню)
CHEST_STREAK_COW = 1              # 🐄 корова в сундук каждого 7-го дня серии
MINE_CORE_MAX = 0                 # ☢️ на рудниках Ядро не выдаётся (28.10: только призы владельца)
BATTLE_BATTERY_FEE_TEAM = 5       # 🔋 заявка команды на битву за рудники (тиммейты скидываются батарейками)
BATTLE_BATTERY_FEE_CLAN = 25      # 🔋 заявка Мега-Клана
RAID_SICK_LOSS_PERCENT = 15       # 💊 без Аптечки часть трофея налёта «пропадает в лазарете»

# --------------------------------------------------------------------------
# ЛАБОРАТОРИЯ: инструменты (как в S.T.A.L.K.E.R. — набор открывает уровень сложных сборок, не
# тратится) и технологии. 1-й уровень любой технологии (кроме науки) — с первого дня, если есть
# набор и ресурсы; каждый следующий уровень ТОЙ ЖЕ технологии — ровно через TECH_COOLDOWN_DAYS
# после предыдущего (решение владельца 27.10: «чтобы улучшения были желанными и ценными»).
# Наука N-го уровня открывается, когда ВСЕ остальные технологии изучены до N-го. Ничего не сбрасывается.
# --------------------------------------------------------------------------
TOOL_ICONS = {1: "⚒️", 2: "🛠", 3: "🔬", 4: "🧬"}
TOOL_COSTS = {
    1: {"metal": 60, "wood": 40, "fire": 5},
    2: {"parts": 120, "crystal": 60, "energy": 20, "fire": 10},
    3: {"crystal": 250, "parts": 200, "energy": 60, "battery": 5},
    4: {"crystal": 500, "parts": 400, "energy": 150, "core": 5},
}
TECHS: dict[str, dict] = {
    # 📡 связь: 1 — налёты и командные активности (доход с рудника); дальше −20 мин перезарядки налёта
    "comm": {"icon": "📡", "max": 5, "base": {"metal": 30, "energy": 10}},
    # 🔭 разведка: без неё налётов нет; цели в разведке = 2 + уровень
    "scout": {"icon": "🔭", "max": 5, "base": {"crystal": 20, "energy": 10}},
    # ⚔️ нападение: без него налётов нет; каждый уровень после первого +8% к добыче
    "attack": {"icon": "⚔️", "max": 5, "base": {"metal": 40, "parts": 20, "energy": 10}},
    # 🛡 оборона: каждый уровень −8% к тому, что налётчик унесёт у тебя
    "defense": {"icon": "🛡", "max": 5, "base": {"hydrogen": 40, "parts": 20, "energy": 10}},
    # 📚 наука: +1% к добыче фермы и трофеям за уровень; нужно Ядро и остальные технологии того же уровня
    "science": {"icon": "📚", "max": 5, "base": {"crystal": 100, "parts": 100, "energy": 50, "core": 3},
                "linear": True},
}
TECH_COOLDOWN_DAYS = 30           # следующий уровень той же технологии — через 30 дней после предыдущего
COMM_BATTERIES = {2: 2, 3: 4, 4: 6, 5: 8}   # 🔋 связь со 2-го уровня требует батарейки
TECH_ORDER = ("comm", "scout", "attack", "defense", "science")
RAID_ATTACK_BONUS_PER_LEVEL = 8
RAID_DEFENSE_PER_LEVEL = 8
SCIENCE_PERCENT_PER_LEVEL = 1
COMM_COOLDOWN_MINUTES_PER_LEVEL = 20


def tech_tool_required(tech: str, level: int) -> int:
    """Какой набор инструментов нужен для уровня level технологии."""
    if tech == "science":
        return 2 if level <= 2 else (3 if level == 3 else 4)
    return 1 if level <= 2 else level - 1   # 1–2 → ⚒️, 3 → 🛠, 4 → 🔬, 5 → 🧬 (у всех одинаково)


def tech_cost(tech: str, level: int) -> dict[str, int]:
    """Цена уровня level (растёт квадратично; наука — линейно, но с Ядром и долгой перезарядкой)."""
    info = TECHS[tech]
    mult = level if info.get("linear") else level * level
    cost = {k: v * mult for k, v in info["base"].items() if v}
    if tech == "comm" and level in COMM_BATTERIES:
        cost["battery"] = COMM_BATTERIES[level]
    return cost


def tech_cooldown_days(tech: str, level: int) -> int:
    """Сколько дней ждать после получения уровня level, чтобы взять следующий (у всех одинаково)."""
    return TECH_COOLDOWN_DAYS


def science_gate_ok(levels: dict[str, int], next_level: int) -> bool:
    """Наука next_level-го уровня — когда все остальные технологии изучены хотя бы до него."""
    return all(levels.get(k, 0) >= next_level for k in TECHS if k != "science")


def raid_loot_percent(attack: int, defense: int, science: int) -> int:
    """Итоговый процент трофея: нападение атакующего и наука против обороны цели (не ниже 50%)."""
    pct = 100 + RAID_ATTACK_BONUS_PER_LEVEL * max(0, attack - 1) + SCIENCE_PERCENT_PER_LEVEL * science
    pct -= RAID_DEFENSE_PER_LEVEL * defense
    return max(50, pct)


def raid_candidates(scout_level: int) -> int:
    return 2 + max(1, scout_level)


def raid_cooldown_hours(comm_level: int) -> float:
    return RAID_ATTACK_COOLDOWN_HOURS - COMM_COOLDOWN_MINUTES_PER_LEVEL * max(0, comm_level - 1) / 60


# --------------------------------------------------------------------------
# 🐎 ЛОШАДИ И ТЕЛЕГИ: логистика биржи. Лошадей продаёт сама игра за монеты (монеты сгорают —
# дефляция), телега собирается в мастерской и ездит только с лошадью.
# Лотов = база + лошади + телеги (по +1 за каждую; телег не больше, чем лошадей); заряженный Шаттл — свой лимит.
# --------------------------------------------------------------------------
HORSE_PRICES = (1500, 3000, 6000, 10000, 15000)
MAX_HORSES = len(HORSE_PRICES)
MAX_CARTS = 5
MARKET_BASE_LOTS = 2
SHUTTLE_CHARGE_DAYS = 30          # 🔋 Шаттл летает на батарейке: 1 батарейка = 30 дней льгот


def market_lots(horses: int, carts: int, shuttle_active: bool) -> int:
    if shuttle_active:
        return SHUTTLE_MARKET_MAX_OPEN_ORDERS
    return MARKET_BASE_LOTS + horses + min(carts, horses)


# --------------------------------------------------------------------------
# 🏆 СЕЗОНЫ (решение владельца 27.10): сезон = календарный месяц UTC (12 в году — удобно под
# каникулы и праздники). Монеты, роботы и покупки НЕ сбрасываются — сбрасываются только таблицы:
# ТОП «заработано за сезон», рейтинг команд по битвам сезона, рейтинг друзей.
# --------------------------------------------------------------------------
# Честный заработок в игре (+ game_win:*). БЕЗ биржи и переводов (аудит 26.10): два своих аккаунта, перепродающие
# друг другу 1 деталь за 100 000, накручивали бы ТОП сезона и номинацию битв «заработок».
SEASON_EARN_REASONS = ("mining", "quiz_level_up", "duel_win", "quest_reward", "daily_chest", "referral_qualified")
# Итоги битв и экспедиций: зависший статус «подводятся итоги» (рестарт посреди выдачи) повторяется через столько минут
FINISH_RETRY_MINUTES = 10
SEASON_BATTLE_POINTS = {1: 10, 2: 7, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1}
SEASON_TOP_SIZE = 100
SEASON_FIRST = "2026-10"          # первый сезон (раньше сезонов не было — итоги не подводятся)
# Призы сезона назначает владелец сам (/reward → «ТОП прошлого сезона»): автоматом — только значок
# в паспорт ТОП-10 (решение владельца 27.10: «халявных монет должно быть поменьше»).
SEASON_BADGE_PLACES = 10


def season_key(moment: datetime) -> str:
    return f"{moment.year:04d}-{moment.month:02d}"


def season_bounds(moment: datetime) -> tuple[datetime, datetime]:
    """[начало, конец) сезона, в который попадает moment (UTC)."""
    start = moment.astimezone(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
    return start, end
# СКЛАД (решение владельца 27.10): 500 → 1000 → 2000 → 3000 → 4000 → 5000 каждого ресурса.
# Каждое расширение на 20% дороже прошлого и требует на одно наименование ресурса больше.
# Изделий на складе — суммарно до ITEMS_CAPACITY_PERCENT от вместимости (500 → 50 изделий всех видов).
STORAGE_CAPS = (1000, 2000, 3000, 4000, 5000)
STORAGE_COST_KINDS = ("metal", "parts", "hydrogen", "crystal", "stone", "wood")
STORAGE_BASE_COST = 400           # всего ресурсов за первое расширение (дальше ×1,2 за уровень)
STORAGE_COST_GROWTH_PERCENT = 20
ITEMS_CAPACITY_PERCENT = 10


def _storage_levels() -> tuple[tuple[int, dict], ...]:
    levels, total = [], STORAGE_BASE_COST
    for i, cap in enumerate(STORAGE_CAPS):
        kinds = STORAGE_COST_KINDS[:2 + i]
        each = -(-total // len(kinds) // 10) * 10            # поровну, вверх до десятков
        levels.append((cap, {k: each for k in kinds}))
        total = total * (100 + STORAGE_COST_GROWTH_PERCENT) // 100
    return tuple(levels)


STORAGE_LEVELS: tuple[tuple[int, dict], ...] = _storage_levels()   # (новая вместимость, цена расширения)
RES_CAPACITY_MAX = STORAGE_CAPS[-1]


def items_capacity(res_capacity: int) -> int:
    """Сколько изделий (суммарно всех видов) помещается на склад такой вместимости."""
    return max(1, res_capacity * ITEMS_CAPACITY_PERCENT // 100)


def next_storage_level(capacity: int) -> tuple[int, dict] | None:
    """Следующее расширение склада или None, если максимум."""
    for cap, cost in STORAGE_LEVELS:
        if cap > capacity:
            return cap, dict(cost)
    return None

# --------------------------------------------------------------------------
# МАСТЕРСКАЯ: рецепты из ресурсов. id → цена {ресурс: кол-во} и эффект.
# Временные эффекты — часы существующих лицензий (ничего не выдаётся «задним числом»:
# прошлое время фермы закрывается ДО продления). Постоянные — уровни брони и Шаттл.
# --------------------------------------------------------------------------
WORKSHOP_RECIPES: dict[str, dict] = {
    "nitro_6h": {"cost": {"metal": 20, "hydrogen": 20}, "effect": "nitrogen", "hours": 6},
    "nuclear_3h": {"cost": {"metal": 40, "hydrogen": 30, "parts": 10}, "effect": "nuclear", "hours": 3},
    "drone_24h": {"cost": {"metal": 25, "parts": 25}, "effect": "drone", "hours": 24},
    "shield_24h": {"cost": {"metal": 10, "crystal": 10}, "effect": "shield", "hours": 24},
    # Синтез котлеты — ОЧЕНЬ дорого (решение владельца 24.10): топливо — право магазина,
    # синтез нужен лишь как мотивация «котлета есть — заведу Бурильщика».
    "cutlet": {"cost": {"metal": 50, "hydrogen": 50, "crystal": 50, "parts": 50}, "effect": "cutlet", "qty": 1},
    "armor": {"cost": None, "effect": "armor"},       # цена зависит от уровня (ARMOR_LEVEL_COSTS)
    "storage": {"cost": None, "effect": "storage"},   # расширение склада (STORAGE_LEVELS)
    # Шаттл: 1000 каждого ресурса + 1000 🪙 (решение владельца 24.10)
    "shuttle": {"cost": {"metal": 1000, "hydrogen": 1000, "crystal": 1000, "parts": 1000},
                "coins": 1000, "effect": "shuttle"},
}
# Новые изделия (решение владельца 26.10). week_limit — сборок на игрока за неделю UTC.
WORKSHOP_RECIPES.update({
    "camo_12h": {"cost": {"crystal": 20, "parts": 10}, "effect": "camo", "hours": 12},
    "trap_24h": {"cost": {"metal": 30, "parts": 20}, "effect": "trap", "hours": 24},
    "drill_24h": {"cost": {"metal": 20}, "effect": "drill", "hours": 24},
    "forsage": {"cost": {"hydrogen": 40}, "effect": "forsage"},
    "economizer": {"cost": {"parts": 25}, "effect": "economizer"},
    "cargo": {"cost": {"metal": 40, "parts": 30}, "effect": "cargo"},
    "thermos_24h": {"cost": {"crystal": 60, "parts": 40}, "effect": "thermos", "hours": 24, "week_limit": 1},
    "stamp": {"cost": {"crystal": 50}, "effect": "stamp", "week_limit": 1},
    # Командные изделия — дорогие (тиммейты скидываются ресурсами), у Мега-Клана ×TEAM_ITEM_CLAN_MULTIPLIER
    "banner_24h": {"cost": {"metal": 150, "hydrogen": 150, "crystal": 150, "parts": 150, "fire": 10, "core": 1},
                   "effect": "banner", "hours": 24, "tool": 2, "team": True},
    "dome_12h": {"cost": {"metal": 300, "hydrogen": 300, "crystal": 300, "parts": 300, "fire": 20, "battery": 10,
                          "core": 3}, "effect": "dome", "hours": 12, "tool": 3, "team": True},
    # ---- 27.10: новое сырьё. Костёр — огонь из древесины и камня
    "bonfire": {"cost": {"wood": 10, "stone": 5}, "effect": "make", "make": {"fire": 5}},
    "battery": {"cost": {"energy": 5, "metal": 5, "fire": 1}, "effect": "make", "make": {"battery": 2}, "tool": 1},
    "cart": {"cost": {"wood": 40, "metal": 20, "fire": 2}, "effect": "cart", "tool": 1},
    "meds_72h": {"cost": {"crystal": 20, "fire": 2, "energy": 3}, "effect": "meds", "hours": 72, "tool": 2},
})
# Котлеты из коровы (решение владельца 26.10): 🐄 1 + 🔥 2 → 🥩 3. Себестоимость по полам биржи
# (1000 + 340) / 3 ≈ 447 🪙 за котлету — дороже пола 200 и магазина (~180–196 🪙): Звёзды не теряют.
WORKSHOP_RECIPES["cutlet"]["cost"] = {"cow": 1, "fire": 2}
WORKSHOP_RECIPES["cutlet"]["qty"] = 3
WORKSHOP_RECIPES["shuttle"]["tool"] = 3
# 🤖 Боевые дроны (28.10): эксклюзив уровня Шаттла — 1000 каждого базового ресурса + своё + 1000 🪙,
# набор 🔬; одна сборка = один дрон. Альтернатива — DRONE_COIN_PRICE монет (кнопка «Купить» в мастерской).
_DRONE_BASE = {"metal": 1000, "hydrogen": 1000, "crystal": 1000, "parts": 1000, "battery": 10}
WORKSHOP_RECIPES.update({
    "drone_guard": {"cost": {**_DRONE_BASE, "stone": 300}, "coins": 1000, "effect": "bdrone", "drone": "guard", "tool": 3},
    "drone_attack": {"cost": {**_DRONE_BASE, "fire": 50}, "coins": 1000, "effect": "bdrone", "drone": "attack", "tool": 3},
    "drone_spy": {"cost": {**_DRONE_BASE, "energy": 150}, "coins": 1000, "effect": "bdrone", "drone": "spy", "tool": 3},
})
WORKSHOP_RECIPES["thermos_24h"]["tool"] = 2
TEAM_ITEM_CLAN_MULTIPLIER = 5     # Купол/Знамя Мега-Клана защищают до 1000 бойцов — и стоят в 5 раз дороже
# Поэтапное открытие (решение владельца 26.10): новичку — по одному рецепту в сутки с момента
# старта в экосистеме, от самого простого и полезного к легендарному. Ветераны видят всё.
WORKSHOP_UNLOCK_HOURS = 24
WORKSHOP_UNLOCK_ORDER = (
    "nitro_6h",       # день 1: +40% к добыче — польза сразу
    "bonfire",        # день 2: огонь — без него ни инструментов, ни батареек
    "shield_24h",     # день 3: щит впрок — защита новичка кончается на 3-й день
    "battery",        # батарейки для разведки (нужны ⚒️ грубые инструменты из Лаборатории)
    "drone_24h",      # роботы не стареют
    "economizer",     # бесплатный вылет
    "storage",        # склад 1000
    "cart",           # телега: +1 лот на бирже (телег ≤ лошадей)
    "nuclear_3h",     # ×5 к добыче
    "camo_12h",
    "meds_72h",
    "forsage",
    "cutlet",
    "trap_24h",
    "drill_24h",
    "cargo",
    "thermos_24h",
    "armor",
    "stamp",
    "banner_24h",
    "dome_12h",
    "shuttle",        # легенда
    "drone_guard",    # 🤖 боевые дроны — эксклюзив после Шаттла
    "drone_attack",
    "drone_spy",
)


def recipe_unlock_at(recipe_id: str, created_at: datetime) -> datetime:
    """Когда рецепт откроется игроку, пришедшему в created_at."""
    return created_at + timedelta(hours=WORKSHOP_UNLOCK_HOURS * WORKSHOP_UNLOCK_ORDER.index(recipe_id))


# Кибер-броня роботов: +10% к добыче за уровень, 3 уровня, ТОЛЬКО НА 30 ДНЕЙ
# (решение владельца 24.10: навсегда — только покупки за Stars). Повторный крафт
# поднимает уровень (или обновляет максимальный) и заново отсчитывает 30 дней.
ARMOR_BONUS_PER_LEVEL = 10
ARMOR_MAX_LEVEL = 3
ARMOR_DAYS = 30
ARMOR_LEVEL_COSTS = {
    1: {"metal": 100, "parts": 50},
    2: {"metal": 250, "crystal": 100, "parts": 120},
    3: {"metal": 500, "hydrogen": 200, "crystal": 200, "parts": 250},
}
# Шаттл: постоянная льгота на бирже (комиссия 10% → 5%) и логистика побольше
SHUTTLE_MARKET_FEE_PERCENT = 5
SHUTTLE_MARKET_MAX_QTY = 500
SHUTTLE_RESOURCE_MAX_QTY = 5000
SHUTTLE_MARKET_MAX_OPEN_ORDERS = 16

# --------------------------------------------------------------------------
# НАЛЁТЫ: решение против решения — жест атакующего против оборонительной стойки цели.
# Добыча — ТОЛЬКО ресурсы (монеты, роботы и котлеты неприкосновенны).
# --------------------------------------------------------------------------
RAID_FUEL_HYDROGEN = 5            # 💧 на вылет (реванш — бесплатно)
RAID_ATTACK_COOLDOWN_HOURS = 3    # между вылетами одного игрока
RAID_VICTIM_COOLDOWN_HOURS = 12   # одну цель нельзя грабить чаще
RAID_LOOT_PERCENT = 20            # доля каждого ресурса цели при победе…
RAID_LOOT_CAP = 30                # …но не больше этого за ресурс
RAID_FAIL_PERCENT = 10            # проигравший атакующий отдаёт цели долю своих…
RAID_FAIL_CAP = 15                # …но не больше этого за ресурс
RAID_MIN_TARGET_RESOURCES = 10    # цели беднее не показываются (нечего брать)
RAID_TARGET_ACTIVE_DAYS = 7       # цель — активный игрок (last_seen_at)
RAID_NEWBIE_SHIELD_DAYS = 3       # новичков не трогают первые дни
RAID_CANDIDATES = 3               # «разведка» показывает столько целей
RAID_REVENGE_HOURS = 24           # окно реванша после удачного налёта на тебя

# --------------------------------------------------------------------------
# ЕЖЕДНЕВНЫЕ ЦЕЛИ: 3 цели на день (детерминированно по игроку и дате), сундук за все три
# --------------------------------------------------------------------------
DAILY_GOALS_PER_DAY = 3
DAILY_CHEST_COINS = 50
DAILY_CHEST_RESOURCE = 10         # случайного ресурса в сундуке
DAILY_STREAK_BONUS_EVERY = 7      # каждый 7-й день подряд…
DAILY_STREAK_BONUS_COINS = 200    # …сундук жирнее на столько монет

# --------------------------------------------------------------------------
# СТАНЦИЯ КОМАНДЫ: общий проект — вклад ресурсов всей команды, уровень даёт
# всем участникам постоянный бонус к добыче (мотивация звать актив).
# --------------------------------------------------------------------------
STATION_MAX_LEVEL = 5
STATION_BONUS_PER_LEVEL = 2       # +2% к добыче каждому участнику за уровень (макс +10%)
STATION_LEVEL_BASE_COST = 300     # уровень L стоит L×300 КАЖДОГО ресурса
STATION_DONATE_OPTIONS = (10, 50)  # кнопки вклада (+ «всё»)
STATION_FEED_LIMIT = 5            # последних вкладов в ленте


def station_level_cost(level: int) -> int:
    """Сколько каждого ресурса нужно вложить, чтобы закрыть уровень level."""
    if level <= 0:
        raise ValueError("level must be positive")
    return level * STATION_LEVEL_BASE_COST


def armor_cost(next_level: int) -> dict[str, int] | None:
    """Цена уровня брони (на максимуме — цена продления максимального уровня)."""
    return ARMOR_LEVEL_COSTS.get(min(next_level, ARMOR_MAX_LEVEL))


def armor_level_active(level: int, until: datetime | None, now: datetime) -> int:
    """Действующий уровень брони: после окончания 30 дней — ноль."""
    return level if is_active(until, now) else 0


def farm_bonus_percent(armor_level: int, station_level: int) -> int:
    """Постоянный бонус к добыче: личная броня + станция команды."""
    armor = max(0, min(armor_level, ARMOR_MAX_LEVEL)) * ARMOR_BONUS_PER_LEVEL
    station = max(0, min(station_level, STATION_MAX_LEVEL)) * STATION_BONUS_PER_LEVEL
    return armor + station


def raid_loot(defender_stock: int, percent: int = 100) -> int:
    """Сколько ресурса уходит атакующему при победе (percent — множитель Трюма, 150 = ×1,5)."""
    return min(RAID_LOOT_CAP * percent // 100, max(0, defender_stock) * RAID_LOOT_PERCENT * percent // 10000)


def raid_fail_loss(attacker_stock: int, multiplier: int = 1) -> int:
    """Сколько ресурса атакующий отдаёт цели при провале (multiplier — Приманка цели)."""
    return min(RAID_FAIL_CAP * multiplier, max(0, attacker_stock) * RAID_FAIL_PERCENT * multiplier // 100)


def market_limits(shuttle: bool, asset: str = "cutlet") -> tuple[int, int]:
    """(макс. штук в ордере, макс. открытых ордеров) — с Шаттлом логистика шире."""
    if asset == "cutlet":
        qty = SHUTTLE_MARKET_MAX_QTY if shuttle else MARKET_MAX_QTY
    elif asset.startswith("g_") or asset.startswith("a_"):
        qty = GEAR_MARKET_MAX_QTY
    elif asset.startswith("s_"):
        qty = 1                     # ✨ скин — единственный экземпляр
    else:
        qty = SHUTTLE_RESOURCE_MAX_QTY if shuttle else MARKET_RESOURCE_MAX_QTY
    return qty, (SHUTTLE_MARKET_MAX_OPEN_ORDERS if shuttle else MARKET_MAX_OPEN_ORDERS)
TOURNAMENT_ENTRY_FEE = 5000
TOURNAMENT_WINNERS_PERCENT = 1


# --------------------------------------------------------------------------
# Общие чистые помощники (без БД, без Telegram)
# --------------------------------------------------------------------------
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def extend_expiry(current: datetime | None, now: datetime, days: int) -> datetime:
    """
    Продление срочной лицензии (буст, безлимит, дрон).

    Если лицензия ещё активна — прибавляем дни к её концу (покупки складываются).
    Если истекла или не было — отсчитываем от «сейчас».
    """
    if days <= 0:
        raise ValueError("days must be positive")
    base = now
    if current is not None and current > now:
        base = current
    return base + timedelta(days=days)


def extend_expiry_hours(current: datetime | None, now: datetime, hours: int) -> datetime:
    if hours <= 0:
        raise ValueError("hours must be positive")
    base = now
    if current is not None and current > now:
        base = current
    return base + timedelta(hours=hours)


def is_active(expiry: datetime | None, now: datetime) -> bool:
    return expiry is not None and expiry > now


def permanent_expiry(now: datetime) -> datetime:
    """Дата сгорания «вечного» робота (Стажёр, апгрейд до вечного Майнера)."""
    return now.replace(year=now.year + PERMANENT_ROBOT_YEARS)


def interns_for_level(level: int) -> int:
    """Сколько Роботов-Стажёров положено за интеллект: по одному за каждые 10 уровней."""
    return max(0, level) // INTERN_LEVEL_STEP


# --------------------------------------------------------------------------
# Звания по стажу в экосистеме (владелец 02.11 — иерархия, понятная любому возрасту; было 22.10 с ROFL/LMAO/KING).
# ⚠️ v3 (владелец 04.11): у каждого звания свой СРОК — сколько часов его носят до следующего. Новичок — сразу после
# регистрации на 72 ч (= защита от налётов, время разобраться в экосистеме), Рядовой 7 дней, Боец 15, Капитан 30,
# Генерал 100, Легенда 200, Властелин — высшее, навсегда.
# --------------------------------------------------------------------------
RANK_DURATIONS_HOURS: tuple[tuple[str, int | None], ...] = (
    ("rookie", RAID_NEWBIE_SHIELD_DAYS * 24),   # Новичок — первые 72 ч, пока действует защита новичка
    ("private", 168),     # Рядовой — 7 дней
    ("fighter", 360),     # Боец — 15 дней
    ("captain", 720),     # Капитан — 30 дней
    ("general", 2400),    # Генерал — 100 дней
    ("legend", 4800),     # Легенда — 200 дней
    ("overlord", None),   # Властелин — высшее, навсегда
)
# (часов стажа с регистрации, ключ звания) — звание начинается, когда истекли сроки всех предыдущих
RANKS: tuple[tuple[int, str], ...] = tuple(
    (sum(h for _, h in RANK_DURATIONS_HOURS[:i]), key) for i, (key, _) in enumerate(RANK_DURATIONS_HOURS))


def rank_key_for(created_at: datetime | None, now: datetime) -> str | None:
    """Ключ звания по стажу (с первой минуты — Новичок) или None, если дата регистрации неизвестна."""
    if created_at is None:
        return None
    hours = max(0.0, (now - created_at).total_seconds() / 3600)
    key = RANKS[0][1]
    for threshold_hours, rank in RANKS:
        if hours >= threshold_hours:
            key = rank
    return key


def miner_hourly_rate(kind: str, *, nuclear_active: bool = False, nitrogen_active: bool = False,
                      bonus_percent: int = 0) -> int:
    """
    Ставка робота в монетах/час с учётом бустов. Эффекты складываются:
    Азот +40% к базе (5→7, 10→14), затем Ядерный разгон ×5 (7→35, 14→70).
    bonus_percent (броня + станция команды) — для ВИТРИН, округление вниз;
    точное начисление с бонусом делает движок фермы в микросекундах.
    """
    rate = MINER_RATE_PER_HOUR[kind]
    if nitrogen_active:
        rate = rate * (100 + NITROGEN_BONUS_PERCENT) // 100
    if nuclear_active:
        rate *= NUCLEAR_SPEED_MULTIPLIER
    if bonus_percent:
        rate = rate * (100 + bonus_percent) // 100
    return rate


def cutlets_per_cycle(nuclear_active: bool) -> int:
    """Сколько котлет съедает один бурильщик при старте цикла 24ч."""
    return PREMIUM_CUTLETS_PER_CYCLE_BASE * (NUCLEAR_FUEL_MULTIPLIER if nuclear_active else 1)


def daily_bonus_seconds_left(last_claim: datetime | None, now: datetime) -> int:
    """0 — бонус доступен; иначе сколько секунд ждать (округление вверх)."""
    if last_claim is None:
        return 0
    passed = (now - last_claim).total_seconds()
    left = DAILY_CUTLET_BONUS_COOLDOWN_SECONDS - passed
    return max(0, -int(-left // 1))  # ceil


def tournament_winners_count(participants: int) -> int:
    """1% участников, округление вверх в пользу игрока: 30 участников → 1 победитель."""
    if participants <= 0:
        return 0
    return -(-participants * TOURNAMENT_WINNERS_PERCENT // 100)  # ceil


def duel_burn_percent(premium: bool = False) -> int:
    return DUEL_BURN_PERCENT_PREMIUM if premium else DUEL_BURN_PERCENT


def duel_payout(stake_each: int, premium: bool = False) -> tuple[int, int]:
    """Возвращает (выплата победителю, сожжено) для дуэли с равными ставками; premium — у победителя Безлимит."""
    if stake_each <= 0:
        raise ValueError("stake must be positive")
    bank = stake_each * 2
    burned = bank * duel_burn_percent(premium) // 100
    return bank - burned, burned


# --------------------------------------------------------------------------
# 🤖 БОЕВЫЕ ДРОНЫ (решение владельца 28.10): Дрон-защитник, Атакующий дрон, Дрон-шпион — личные спутники
# в налётах и экспедициях. Количество не ограничено, действие суммируется (с потолком), но каждый —
# эксклюзивная ачивка: сборка как у Шаттла или покупка за большие монеты (монеты сгорают).
# Дроны не лежат на складе изделий (лимит 10% их не касается) и не тратятся.
# --------------------------------------------------------------------------
DRONE_KINDS = ("guard", "attack", "spy")
DRONE_COIN_PRICE = 100_000           # 🪙 за дрона (ledger drone_buy, сгорают); 26.10: рецепт по полам биржи ≈ 75 000
DRONE_RAID_ATTACK_PCT = 5            # ⚔️ каждый атакующий дрон: +5% к трофею налёта…
DRONE_RAID_GUARD_PCT = 5             # 🛡 каждый защитник цели: −5% к трофею налётчика…
DRONE_RAID_CAP_PCT = 50              # …но не больше ±50% (суммарно)
DRONE_RAID_MIN_LOOT_PCT = 25         # трофей с дронами не опускается ниже четверти
DRONE_SPY_TARGETS = 1                # 🛰 каждый шпион: +1 цель в разведке налётов…
DRONE_SPY_TARGETS_CAP = 5            # …не больше +5
DRONE_EXP_CARGO_PCT = 3              # экспедиции: атакующие дроны отряда — +3% к добыче на силовых развилках
DRONE_EXP_GUARD_PCT = 5              # защитники отряда — −5% к потерям груза
DRONE_EXP_SPEED_PCT = 2              # шпионы отряда — путь короче на 2%
DRONE_EXP_CARGO_CAP = 60
DRONE_EXP_GUARD_CAP = 60
DRONE_EXP_SPEED_CAP = 30


def drone_raid_loot_percent(base_percent: int, attacker_attack: int, defender_guard: int) -> int:
    """Процент трофея налёта с учётом атакующих дронов налётчика и защитников цели."""
    bonus = min(DRONE_RAID_CAP_PCT, max(0, attacker_attack) * DRONE_RAID_ATTACK_PCT)
    cut = min(DRONE_RAID_CAP_PCT, max(0, defender_guard) * DRONE_RAID_GUARD_PCT)
    if not bonus and not cut:
        return base_percent
    return max(DRONE_RAID_MIN_LOOT_PCT, base_percent + bonus - cut)


def drone_spy_targets(spies: int) -> int:
    return min(DRONE_SPY_TARGETS_CAP, max(0, spies) * DRONE_SPY_TARGETS)


def drone_exp_effects(attack: int, guard: int, spy: int) -> dict[str, int]:
    """Проценты отряда в экспедиции: cargo (+к добыче силовых развилок), guard (−потери), speed (−путь)."""
    return {"cargo": min(DRONE_EXP_CARGO_CAP, max(0, attack) * DRONE_EXP_CARGO_PCT),
            "guard": min(DRONE_EXP_GUARD_CAP, max(0, guard) * DRONE_EXP_GUARD_PCT),
            "speed": min(DRONE_EXP_SPEED_CAP, max(0, spy) * DRONE_EXP_SPEED_PCT)}


# --------------------------------------------------------------------------
# 🗺 ЭКСПЕДИЦИИ (решение владельца 28.10): цели на карте мира ставит владелец в пульте (до 10 сразу),
# у каждой — свой час итогов. Отряды идут с разных сторон карты; по дороге — развилки, которые
# решает голосование команды (в соло — сам игрок). Не успел дойти к часу итогов — не участвуешь.
# Снаряжение: соло — водород; команда — батарейки; Мега-Клан — батарейки + котлеты в провиант.
# --------------------------------------------------------------------------
EXP_MAP_W, EXP_MAP_H = 160, 100      # условные единицы карты мира (вся карта видна сразу)
EXP_MAX_TARGETS = 10                 # целей на карте одновременно
# 26.10: на карте мира — и соло, и командные походы (формат задаёт владелец при создании цели); рудники — только командам
EXP_SCOPES = ("solo", "team", "clan", "teams")   # teams — команды и кланы в одном зачёте
# 30.10 (владелец: «5–6 часов ждать — накаляет»): путь — от и до минут по расстоянию от дома отряда до цели;
# ближе к цели — быстрее, и на карте видно, как точки соперников ползут к ней. Соло 10–30 мин, команда/клан 30–120.
EXP_TRAVEL_RANGE = {"solo": (10, 30), "team": (30, 120), "clan": (35, 120)}
EXP_MAX_DISTANCE = 189.0             # ≈ диагональ карты 160×100 — самый дальний путь
EXP_MIN_TRAVEL_MINUTES = 5           # пол после всех ускорений (шпионы, костюм военного)
EXP_SOLO_HYDROGEN = 10               # 💧 соло-вылазка
EXP_BATTERIES = {"team": 5, "clan": 25}           # 🔋 снаряжение отряда (вносят бойцы по одной)
EXP_CLAN_CUTLETS = 10                # 🥩 провиант Мега-Клана (решение владельца: командам котлеты не нужны)
EXP_BASE_CARGO = 100                 # стартовый груз — по нему места в итогах
EXP_FORKS_DEFAULT = 3
EXP_FORKS_MAX = 5
EXP_MAX_PLACES = 100


def exp_mode_allowed(scope: str, mode: str) -> bool:
    """Может ли отряд такого вида (solo/team/clan) идти к цели с таким зачётом."""
    return mode == scope or (scope == "teams" and mode in ("team", "clan"))


def exp_peek_budget(spies: int, scout_level: int, forks: int, first_of_season: bool) -> int:
    """
    🔎 Сколько развилок отряд может разведать (увидеть последствия до решения) — решение владельца 28.10:
    первая экспедиция сезона — вслепую; дальше столько, сколько у лидера отряда (соло — сам игрок,
    команда — капитан) 🛰 Дронов-шпионов И уровней 🔭 разведки — по меньшему, но не больше развилок.
    """
    if first_of_season:
        return 0
    return max(0, min(spies, scout_level, forks))


def exp_travel_minutes(distance: float, mode: str, spy_pct: int = 0, suit_pct: int = 0) -> int:
    """Минуты пути: от и до EXP_TRAVEL_RANGE по расстоянию; шпионы сокращают путь, 🪖 костюм военного — ещё на suit_pct%."""
    lo, hi = EXP_TRAVEL_RANGE[mode]
    minutes = lo + (hi - lo) * min(1.0, max(0.0, distance) / EXP_MAX_DISTANCE)
    minutes = minutes * (100 - max(0, min(spy_pct, DRONE_EXP_SPEED_CAP))) / 100
    minutes = minutes * (100 - max(0, min(suit_pct, 50))) / 100
    return max(EXP_MIN_TRAVEL_MINUTES, int(round(minutes)))


# --------------------------------------------------------------------------
# 🧍 ПЕРСОНАЖ И КОСТЮМЫ (решение владельца 30.10). Костюм — 5 деталей (шлем, куртка, перчатки, штаны, ботинки);
# бонус работает, только когда надет ПОЛНЫЙ комплект одного костюма (уровень костюма = меньший из уровней деталей).
# Детали выпадают случайно (пульт владельца, призы битв и экспедиций): не больше GEAR_SEASON_CAP за сезон на игрока —
# ровно один костюм, но у всех разные детали, поэтому одинаковые собирают через биржу (комиссия сгорает).
# ТРИ УРОВНЯ (владелец 31.10): 1 Базовый, 2 Улучшенный, 3 Легендарный — каждый чуть сильнее. Прокачка детали — труд:
# ресурсы + монеты (сгорают) + опыт детали (события, которые она пережила надетой — shared/trophies) + на Легендарный
# ещё технология в тему костюма. Все 6 костюмов на Улучшенном уровне сплавляются в нано-экзо-броню (все бонусы
# сразу, уровня GEAR_EXO_LEVEL); сплавленные детали исчезают навсегда.
# --------------------------------------------------------------------------
GEAR_SUITS = ("el", "mn", "ml", "st", "sc", "en")   # электрик, шахтёр, военный, маскировка, учёный, инженер
GEAR_EXO = "exo"                                     # нано-экзо-броня (только сплавом, на бирже не торгуется)
GEAR_SLOTS = ("head", "body", "hands", "legs", "feet")
GEAR_MAX_LEVEL = 3
GEAR_LEVEL_KEYS = {1: "basic", 2: "improved", 3: "legendary"}   # названия уровней — ключи gear.lvl_*
GEAR_SEASON_CAP = len(GEAR_SLOTS)    # деталей за сезон на игрока — ровно один костюм
GEAR_MIN_PRICE = 500                 # пол цены детали на бирже (продажа и заявка)
GEAR_MARKET_MAX_QTY = 5              # деталей в одном ордере
# Сила бонуса полного костюма по уровню, в процентах (у каждого костюма — своя «линия»)
SUIT_BONUS = {
    "el": {1: 50, 2: 60, 3: 70},   # ⚡ шанс электричества за победу в соло-игре (без костюма — ENERGY_WIN_CHANCE_PERCENT)
    "mn": {1: 5, 2: 8, 3: 10},     # ⛏ раз в сутки: % от монет, добытых фермой за прошлые сутки UTC (округление вниз)
    "ml": {1: 10, 2: 15, 3: 20},   # 🪖 налёты: +% трофея; экспедиции: +% к добыче развилок и −% пути
    "st": {1: 30, 2: 50, 3: 60},   # 🥷 шанс не попасть в разведку налётчика
    "sc": {1: 20, 2: 30, 3: 40},   # 🔬 перерыв между уровнями технологий короче на %
    "en": {1: 10, 2: 15, 3: 20},   # 🔧 ресурсы рецептов мастерской дешевле на % (округление вверх — в пользу экосистемы)
}
# Прокачка детали на уровень N (ключ — НОВЫЙ уровень): ресурсы в тему костюма + монеты (сгорают, ledger gear_upgrade)
GEAR_UPGRADE_COST = {
    2: {
        "el": {"energy": 20, "battery": 1, "metal": 50},
        "mn": {"metal": 150, "stone": 80},
        "ml": {"metal": 100, "parts": 100, "fire": 10},
        "st": {"hydrogen": 120, "wood": 80},
        "sc": {"crystal": 150, "energy": 10},
        "en": {"parts": 150, "battery": 1, "crystal": 30},
    },
    # Легендарный: 🔋 3 + 🔥 20 + профильный ресурс ×300
    3: {
        "el": {"battery": 3, "fire": 20, "energy": 300},
        "mn": {"battery": 3, "fire": 20, "stone": 300},
        "ml": {"battery": 3, "fire": 20, "metal": 300},
        "st": {"battery": 3, "fire": 20, "hydrogen": 300},
        "sc": {"battery": 3, "fire": 20, "crystal": 300},
        "en": {"battery": 3, "fire": 20, "parts": 300},
    },
}
GEAR_UPGRADE_COINS = {2: 300, 3: 1000}
# Опыт детали — сколько событий (победы, дуэли, налёты, походы, крафт, квесты…) она пережила надетой, всего за жизнь
GEAR_UPGRADE_XP = {2: 25, 3: 100}
# Легендарный уровень — только с технологией Лаборатории в тему костюма: (технология, уровень)
GEAR_UPGRADE_TECH = {3: {"el": ("comm", 2), "mn": ("scout", 2), "ml": ("attack", 2),
                         "st": ("defense", 2), "sc": ("science", 1), "en": ("comm", 2)}}
GEAR_EXO_LEVEL = 2   # экзо-броня: сплав деталей Улучшенного уровня, бонусы — тоже Улучшенного
# Сплав всех 30 деталей Улучшенного уровня в нано-экзо-броню (ledger gear_exo)
GEAR_EXO_COST = {"core": 1, "battery": 5, "energy": 50}
GEAR_EXO_COINS = 3000


def gear_asset(suit: str, slot: str) -> str:
    """Ключ товара биржи для детали 1-го уровня: g_<костюм>_<слот> (≤ 16 символов колонки asset)."""
    return f"g_{suit}_{slot}"


def parse_gear_asset(asset: str) -> tuple[str, str] | None:
    parts = (asset or "").split("_")
    if len(parts) == 3 and parts[0] == "g" and parts[1] in GEAR_SUITS and parts[2] in GEAR_SLOTS:
        return parts[1], parts[2]
    return None


GEAR_ASSETS = tuple(gear_asset(s, p) for s in GEAR_SUITS for p in GEAR_SLOTS)


def suit_bonus(suit: str | None, level: int | None, line: str) -> int:
    """% бонуса линии line (el/mn/ml/st/sc/en) у надетого полного костюма; экзо-броня даёт все линии Улучшенного уровня."""
    if not suit or not level:
        return 0
    if suit == GEAR_EXO:
        return SUIT_BONUS[line][GEAR_EXO_LEVEL]
    if suit != line:
        return 0
    return SUIT_BONUS[line].get(min(int(level), GEAR_MAX_LEVEL), 0)


def energy_chance_percent(suit: str | None, level: int | None, art: dict | None = None) -> int:
    """Шанс ⚡ за победу: костюм электрика заменяет базовые 25%, артефакты добавляются сверху (не больше 95%)."""
    base = suit_bonus(suit, level, "el") or ENERGY_WIN_CHANCE_PERCENT
    return min(95, base + gear_bonus(None, None, art, "el"))


def discounted_cost(cost: dict[str, int], pct: int) -> dict[str, int]:
    """Скидка инженера: каждый ресурс дешевле на pct%, округление ВВЕРХ (в пользу экосистемы)."""
    if not pct:
        return dict(cost)
    return {k: -(-v * (100 - pct) // 100) for k, v in cost.items()}


def miner_bonus(mined: int, pct: int) -> int:
    """Бонус шахтёра за сутки: % от добытого, округление ВНИЗ (каждая монета — против инфляции)."""
    return max(0, mined) * max(0, pct) // 100


def tech_cooldown_cut(days: float, pct: int) -> float:
    return days * (100 - max(0, pct)) / 100



# --------------------------------------------------------------------------
# ⏱ ДОСРОЧНЫЕ ИТОГИ (владелец 30.10): у экспедиции, битвы (акции, рудники) и аукциона — точное время окончания
# И (по желанию) «раньше, если наберётся N»: дошедших до цели игроков / участников битвы / игроков, сделавших
# ставку. Итоги — по тому, что наступит раньше (shared/autofinish.py, демон админ-бота).
# --------------------------------------------------------------------------
FINISH_COUNTS = (10, 100, 1000, 10000)


def finish_count_ok(value) -> int | None:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return None
    return n if n in FINISH_COUNTS else None


# --------------------------------------------------------------------------
# 💠 АРТЕФАКТЫ (владелец 30.10): камни на «пояс» персонажа — ARTIFACT_SLOTS окошек под аватаром. Каждый вид усиливает
# свою линию бонусов (те же, что у костюмов) и складывается с костюмом. Бесплатно — не больше ARTIFACT_SEASON_CAP за
# сезон (подарок разработчика, экспедиции); остальное — биржа (пол ARTIFACT_MIN_PRICE).
# --------------------------------------------------------------------------
ARTIFACT_SLOTS = ("a1", "a2", "a3")
ARTIFACT_KINDS = GEAR_SUITS                     # вид артефакта = линия бонуса
ARTIFACT_BAG_SLOT = "art"                       # в сумке артефакт — деталь со «слотом» art и костюмом a<вид>
ARTIFACT_BONUS = {"el": 10, "mn": 2, "ml": 5, "st": 10, "sc": 10, "en": 5}
ARTIFACT_SEASON_CAP = 1
ARTIFACT_MIN_PRICE = 1000
ARTIFACT_ICONS = {"el": "🌩", "mn": "🍀", "ml": "🌇", "st": "👻", "sc": "🔮", "en": "🤖"}


def art_code(kind: str) -> str:
    """Код артефакта в сумке/поясе (колонка suit VARCHAR(3)): a + вид."""
    return "a" + kind


def art_kind(code: str | None) -> str | None:
    if code and len(code) == 3 and code[0] == "a" and code[1:] in ARTIFACT_KINDS:
        return code[1:]
    return None


def art_asset(kind: str) -> str:
    return f"a_{kind}"


def parse_art_asset(asset: str) -> str | None:
    parts = (asset or "").split("_")
    return parts[1] if len(parts) == 2 and parts[0] == "a" and parts[1] in ARTIFACT_KINDS else None


ART_ASSETS = tuple(art_asset(k) for k in ARTIFACT_KINDS)


def art_bonus_total(kinds) -> dict[str, int]:
    """Сумма бонусов надетых артефактов по линиям: {"el": 20, …}."""
    out: dict[str, int] = {}
    for k in kinds:
        if k in ARTIFACT_BONUS:
            out[k] = out.get(k, 0) + ARTIFACT_BONUS[k]
    return out


def gear_bonus(suit: str | None, level: int | None, art: dict | None, line: str) -> int:
    """Весь бонус линии: полный костюм + артефакты пояса."""
    extra = 0
    if art:
        try:
            extra = int((art if isinstance(art, dict) else {}).get(line, 0))
        except (TypeError, ValueError):
            extra = 0
    return suit_bonus(suit, level, line) + extra


def art_of(row) -> dict:
    """users.art_bonus из строки БД (JSONB приходит строкой или словарём)."""
    import json
    raw = row["art_bonus"] if row is not None and "art_bonus" in row.keys() else None
    if not raw:
        return {}
    return json.loads(raw) if isinstance(raw, str) else dict(raw)


def user_bonus(row, line: str) -> int:
    """Бонус линии по строке users (suit, suit_level, art_bonus)."""
    if row is None:
        return 0
    return gear_bonus(row["suit"], row["suit_level"], art_of(row), line)


# --------------------------------------------------------------------------
# 🎁 ПОДАРКИ ОТ РАЗРАБОТЧИКА (владелец 30.10): «Подарить всем» — не рассылка (бан Telegram за тысячи сообщений), а
# плашка в паспорте с кнопкой «Забрать»; подарки копятся до срока. Вещи с сезонным лимитом (детали, артефакты) видит
# и получает только тот, кто ещё не добрал лимит сезона — справедливо и старожилам, и новичкам.
# --------------------------------------------------------------------------
GIFT_LIST_LIMIT = 20
