"""
Единый источник чисел экономики ROFL HUB.

Все спорные величины из ТЗ живут ЗДЕСЬ и только здесь. Меняется константа —
меняется поведение всего бота. Никаких «магических чисел» в обработчиках.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------
# Валюта и стартовые бонусы
# --------------------------------------------------------------------------
START_BALANCE = 1000          # монет при регистрации
START_CUTLETS_INVENTORY = 1   # кибер-котлет на склад при регистрации
REFERRAL_SIGNUP_BONUS = 1000  # монет рефереру за регистрацию друга
REFERRAL_REVENUE_SHARE = 0.20  # доля от трат реферала (учёт для выплат)
REFERRAL_SHARE_DAYS = 365
# Квалифицированный реферал (решение владельца 13.10 вечером): друг считается «живым»,
# когда сыграл 30 раундов; рефереру — ещё +1000, строго один раз (users.qualified_at).
REFERRAL_QUALIFY_ROUNDS = 30
REFERRAL_QUALIFIED_BONUS = 1000

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
    "intern": 1,    # Робот Стажёр: бесплатный, вечный, без топлива (решение владельца 22.10)
    "junior": 5,    # Младший Майнер, топливо не нужно
    "premium": 10,  # Кибер-Бурильщик, ест котлеты
}
# Робот Стажёр: один выдаётся каждому при активации в /farm, ещё по одному — за каждый
# уровень интеллекта, кратный INTERN_LEVEL_STEP (10, 20, 30…). Ставка фиксированная.
INTERN_LEVEL_STEP = 10
# Апгрейд Стажёра до ВЕЧНОГО Младшего Майнера (999 ★): нужно не меньше
# INTERN_UPGRADE_REFERRALS квалифицированных друзей (сыгравших 30 раундов).
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
}
DEFAULT_DAILY_WIN_LIMIT = 15
QUIZ_ANSWER_SECONDS = 15   # решение владельца 13.10: за 10 секунд не успеть прочитать вопрос
# Прогрессивные уровни викторины (решение владельца 13.10.2026):
# уровень N закрывается за N*10 верных ответов (счётчик итерации обнуляется),
# награда за уровень N — N*100 монет. 1-й: 10 ответов → +100; 100-й: 1000 → +10 000.
QUIZ_LEVEL_STEP_ANSWERS = 10
QUIZ_LEVEL_REWARD_PER_LEVEL = 100


def win_reward_for(game_type: str) -> int:
    """Выигрыш за раунд: у Сейфа повышенный (ниже шанс), у остальных базовый."""
    return SAFE_WIN_REWARD if game_type == "safe" else WIN_REWARD


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
MEGA_CLAN_MAX_MEMBERS = 1000
TEAM_LIST_PAGE_SIZE = 25      # тиммейтов на страницу в /my_team (Мега-Клан — до 40 страниц)

# --------------------------------------------------------------------------
# Дуэли: 3 уровня столов «как в покере», сжигание 20% банка
# --------------------------------------------------------------------------
DUEL_TABLES = (10, 100, 1000)          # ставки столов, монет
DUEL_MOVE_TIMEOUT_SECONDS = 60         # на выбор жеста; не успел — жест случайный
DUEL_WAITING_TTL_MINUTES = 30          # очередь без соперника отменяется с возвратом ставки

# --------------------------------------------------------------------------
# Переводы монет между игроками
# --------------------------------------------------------------------------
TRANSFER_MIN_AMOUNT = 10
TRANSFER_FEE_PERCENT = 0      # комиссия сжигается; на старте 0, поднять — одно число


def transfer_fee(amount: int) -> int:
    return amount * TRANSFER_FEE_PERCENT // 100


# --------------------------------------------------------------------------
# Биржа котлет (решение владельца 22.10): P2P котлеты за монеты, комиссия сжигается
# --------------------------------------------------------------------------
MARKET_FEE_PERCENT = 10        # сгорает с каждой продажи — дефляция монет
MARKET_MIN_PRICE = 1           # монет за котлету
MARKET_MAX_PRICE = 100_000
MARKET_MAX_QTY = 100           # котлет в одном ордере
MARKET_MAX_OPEN_ORDERS = 5     # открытых ордеров на игрока
MARKET_SHOWCASE_LIMIT = 6      # ордеров на витрине /market (по одной кнопке в ряд)


def market_fee(total: int, shuttle: bool = False) -> int:
    """Комиссия сделки на бирже; у владельцев Шаттла (мастерская) — льготная."""
    percent = SHUTTLE_MARKET_FEE_PERCENT if shuttle else MARKET_FEE_PERCENT
    return total * percent // 100
DUEL_BURN_PERCENT = 20


# --------------------------------------------------------------------------
# РЕСУРСЫ (волна 22.10, вечер): в каждой игре добывается свой ресурс — клей экосистемы.
# Ресурсы не покупаются за Stars и не продаются за монеты: только добыча и мастерская.
# --------------------------------------------------------------------------
RESOURCE_KINDS = ("metal", "hydrogen", "crystal", "parts")
GAME_RESOURCE = {          # игра → ресурс за победу
    "rps": "metal",        # ⛏ Металл — КНБ (и дуэли)
    "hl": "hydrogen",      # 💧 Водород — Больше/Меньше
    "quiz": "crystal",     # 💎 Кристаллы — Викторина
    "safe": "parts",       # ⚙️ Детали — Кибер-Сейф (шанс 1 из 4 — даём больше)
}
RESOURCE_PER_WIN = {"rps": 1, "hl": 1, "quiz": 1, "safe": 3}
DUEL_RESOURCE_REWARD = {10: 2, 100: 4, 1000: 8}   # ⛏ Металл победителю дуэли по столу
QUEST_RESOURCE_BUNDLE = 5     # каждого ресурса за ПЕРВОЕ прохождение квеста
RESOURCE_MAX_STOCK = 100_000  # потолок запаса на ресурс (защита от переполнения)

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
    "cutlet": {"cost": {"hydrogen": 15, "parts": 10}, "effect": "cutlet", "qty": 1},
    "armor": {"cost": None, "effect": "armor"},       # цена зависит от уровня (ARMOR_LEVEL_COSTS)
    "shuttle": {"cost": {"metal": 150, "hydrogen": 150, "crystal": 100, "parts": 100},
                "effect": "shuttle"},
}
# Кибер-броня роботов: постоянный бонус к добыче, 3 уровня по +10%
ARMOR_BONUS_PER_LEVEL = 10
ARMOR_MAX_LEVEL = 3
ARMOR_LEVEL_COSTS = {
    1: {"metal": 100, "parts": 50},
    2: {"metal": 250, "crystal": 100, "parts": 120},
    3: {"metal": 500, "hydrogen": 200, "crystal": 200, "parts": 250},
}
# Шаттл: постоянная льгота на бирже (комиссия 10% → 5%) и логистика побольше
SHUTTLE_MARKET_FEE_PERCENT = 5
SHUTTLE_MARKET_MAX_QTY = 500
SHUTTLE_MARKET_MAX_OPEN_ORDERS = 10

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
    """Цена следующего уровня брони или None, если максимум."""
    return ARMOR_LEVEL_COSTS.get(next_level)


def farm_bonus_percent(armor_level: int, station_level: int) -> int:
    """Постоянный бонус к добыче: личная броня + станция команды."""
    armor = max(0, min(armor_level, ARMOR_MAX_LEVEL)) * ARMOR_BONUS_PER_LEVEL
    station = max(0, min(station_level, STATION_MAX_LEVEL)) * STATION_BONUS_PER_LEVEL
    return armor + station


def raid_loot(defender_stock: int) -> int:
    """Сколько ресурса уходит атакующему при победе."""
    return min(RAID_LOOT_CAP, max(0, defender_stock) * RAID_LOOT_PERCENT // 100)


def raid_fail_loss(attacker_stock: int) -> int:
    """Сколько ресурса атакующий отдаёт цели при провале."""
    return min(RAID_FAIL_CAP, max(0, attacker_stock) * RAID_FAIL_PERCENT // 100)


def market_limits(shuttle: bool) -> tuple[int, int]:
    """(макс. котлет в ордере, макс. открытых ордеров) — с Шаттлом логистика шире."""
    if shuttle:
        return SHUTTLE_MARKET_MAX_QTY, SHUTTLE_MARKET_MAX_OPEN_ORDERS
    return MARKET_MAX_QTY, MARKET_MAX_OPEN_ORDERS
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
    """Сколько Роботов Стажёров положено за интеллект: по одному за каждые 10 уровней."""
    return max(0, level) // INTERN_LEVEL_STEP


# --------------------------------------------------------------------------
# Звания по стажу в экосистеме (решение владельца 22.10): справа от имени игрока.
# От низшего к крутейшему; ROFL/LMAO/DEAD — латиницей на всех языках.
# --------------------------------------------------------------------------
RANKS: tuple[tuple[int, str], ...] = (
    (1, "rookie"),      # 1 день
    (7, "fighter"),     # неделя
    (30, "legend"),     # месяц
    (90, "rofl"),       # 3 месяца
    (180, "lmao"),      # полгода
    (365, "dead"),      # год и больше
)


def rank_key_for(created_at: datetime | None, now: datetime) -> str | None:
    """Ключ звания по стажу или None (меньше суток в экосистеме)."""
    if created_at is None:
        return None
    days = (now - created_at).total_seconds() / 86400
    key = None
    for threshold_days, rank in RANKS:
        if days >= threshold_days:
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


def duel_payout(stake_each: int) -> tuple[int, int]:
    """Возвращает (выплата победителю, сожжено) для дуэли с равными ставками."""
    if stake_each <= 0:
        raise ValueError("stake must be positive")
    bank = stake_each * 2
    burned = bank * DUEL_BURN_PERCENT // 100
    return bank - burned, burned
