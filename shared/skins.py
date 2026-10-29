"""
✨ Скины (решение владельца 30.10: «скины должно быть видно и ими можно понтоваться»).

Скин ничего не даёт к силе — только вид и статус. Спрос создают пять вещей:
1) ВИДНО ДРУГИМ: рамка и титул — в паспорте, ТОПе и составе команды; костюм — на аватаре персонажа; маркер — точка
   отряда на карте походов; сумка — фон ячеек;
2) РЕДКОСТЬ НАСТОЯЩАЯ: у сезонных скинов тираж с номером («№37 из 500»), продажа — только до конца сезона;
3) РЫНОК: экземпляр продаётся другому игроку за монеты (товар биржи s_<экземпляр>, пол цены по редкости, комиссия сгорает);
4) ИСТОРИЯ: скин копит счётчик — победы в играх (костюм) и дошедшие походы (маркер);
5) КОЛЛЕКЦИЯ: весь набор сезона → бесплатный титул-награда, которого нельзя купить.
ПРОКАЧКА — МНОГОСТУПЕНЧАТАЯ (владелец 30.10): 10 уровней, 6 ступеней (Заводской → Закалённый → Боевой → Ветеран →
Легендарный → Бессмертный), каждая ступень — новый эффект. Опыт — двумя путями: ЗАКАЛКА (скин поглощает другой экземпляр,
тот исчезает навсегда; SKIN_MERGE_XP по редкости) и БОЕВОЙ ОПЫТ (события игры, пока скин надет: SKIN_EVENT_XP, пишет
shared/trophies.record). Высокие уровни требуют ещё и числа поглощений (SKIN_LEVELS: опыт + слияния) — одной игрой или
одним слиянием не дойти. Платных случайных кейсов нет: за ★ — конкретный скин, случайности — только в бесплатных наградах.

Экземпляры — таблица user_skins (у каждого свой номер тиража). user_id = 0 — экземпляр в эскроу биржи.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

TARGETS = ("suit", "frame", "title", "marker", "bag")
RARITIES = ("common", "rare", "epic", "legendary", "mythic")
RARITY_COLOR = {"common": "#b0b8d0", "rare": "#3fa9ff", "epic": "#b77bff", "legendary": "#ffb43a", "mythic": "#ff3d6e"}
# Уровень N: (опыт, поглощений) — нужны ОБА условия
SKIN_LEVELS = ((0, 0), (20, 0), (60, 0), (150, 1), (300, 1), (600, 2), (1000, 3), (1600, 4), (2500, 6), (4000, 8))
SKIN_MAX_LEVEL = len(SKIN_LEVELS)
# Ступени: (с какого уровня, ключ подписи) — каждая ступень включает свой эффект в приложении
SKIN_STAGES = ((1, "factory"), (2, "tempered"), (4, "combat"), (6, "veteran"), (8, "legend"), (10, "immortal"))
SKIN_MERGE_XP = {"common": 20, "rare": 50, "epic": 120, "legendary": 300, "mythic": 800}   # за поглощённый экземпляр
RARITY_XP = SKIN_MERGE_XP
# боевой опыт надетого скина за событие игры
SKIN_EVENT_XP = {"game_win": 1, "duel": 1, "duel_win": 3, "raid": 2, "raid_win": 3, "raid_def": 2, "expedition": 5,
                 "craft": 2, "tech": 10, "quest": 5, "chest": 3}
SKIN_MIN_PRICE = {"common": 300, "rare": 1000, "epic": 3000, "legendary": 10000, "mythic": 50000}   # 🪙 на бирже
ESCROW_OWNER = 0

AURORA_UNTIL = datetime(2026, 12, 1, tzinfo=timezone.utc)    # сезон ноября 2026: потом набор не продаётся никогда

# look: c1/c2 — градиент, fx — анимация (shimmer, pulse, aurora, flame, glitch, none); маркер — эмодзи точки на карте.
# stars=None — не продаётся (награды, аукционы владельца); edition=None — без тиража.
SKINS: dict[str, dict] = {
    # --- 🌌 Сезонный набор «Северное сияние» (ноябрь 2026) ---
    "aur_suit": {"set": "aurora", "target": "suit", "rarity": "legendary", "stars": 1000, "edition": 500,
                 "until": AURORA_UNTIL, "look": {"c1": "#2bffb1", "c2": "#8a5cff", "fx": "aurora"},
                 "name": "Северное сияние", "name_en": "Northern Lights"},
    "aur_frame": {"set": "aurora", "target": "frame", "rarity": "epic", "stars": 300, "edition": 1000,
                  "until": AURORA_UNTIL, "look": {"c1": "#2bffb1", "c2": "#8a5cff", "fx": "aurora"},
                  "name": "Рамка «Северное сияние»", "name_en": "Northern Lights frame"},
    "aur_title": {"set": "aurora", "target": "title", "rarity": "rare", "stars": 150, "edition": 1000,
                  "until": AURORA_UNTIL, "look": {"c1": "#2bffb1", "c2": "#8a5cff", "fx": "shimmer"},
                  "name": "Северный свет", "name_en": "Northern Light", "text": "Северный свет", "text_en": "Northern Light"},
    "aur_marker": {"set": "aurora", "target": "marker", "rarity": "rare", "stars": 100, "edition": 2000,
                   "until": AURORA_UNTIL, "look": {"c1": "#2bffb1", "c2": "#8a5cff", "fx": "pulse", "emoji": "🌌"},
                   "name": "Маркер «Сияние»", "name_en": "Aurora marker"},
    "aur_bag": {"set": "aurora", "target": "bag", "rarity": "rare", "stars": 100, "edition": 2000,
                "until": AURORA_UNTIL, "look": {"c1": "#0e3b3a", "c2": "#2a1850", "fx": "aurora"},
                "name": "Сумка «Северное сияние»", "name_en": "Northern Lights bag"},
    # награда за весь набор — купить нельзя
    "aur_keeper": {"set": "aurora_reward", "target": "title", "rarity": "legendary", "stars": None, "edition": None,
                   "look": {"c1": "#2bffb1", "c2": "#ffd23f", "fx": "aurora"},
                   "name": "Хранитель сияния", "name_en": "Keeper of the Lights",
                   "text": "Хранитель сияния", "text_en": "Keeper of the Lights"},
    # --- 👑 Мифический тираж — только аукцион или подарок владельца ---
    "myth_polar": {"set": "mythic", "target": "suit", "rarity": "mythic", "stars": None, "edition": 100,
                   "look": {"c1": "#ffffff", "c2": "#ff3d6e", "fx": "flame"},
                   "name": "Полярная корона", "name_en": "Polar Crown"},
    # --- Постоянная коллекция ---
    "neo_frame": {"set": "core", "target": "frame", "rarity": "common", "stars": 50, "edition": None,
                  "look": {"c1": "#00ffe1", "c2": "#00b3ff", "fx": "pulse"}, "name": "Рамка «Неон»", "name_en": "Neon frame"},
    "carbon_suit": {"set": "core", "target": "suit", "rarity": "common", "stars": 75, "edition": None,
                    "look": {"c1": "#3a3f4b", "c2": "#14171f", "fx": "none"}, "name": "Карбон", "name_en": "Carbon"},
    "gold_suit": {"set": "core", "target": "suit", "rarity": "epic", "stars": 400, "edition": 1000,
                  "look": {"c1": "#ffe27a", "c2": "#c48a12", "fx": "shimmer"}, "name": "Золотой стандарт", "name_en": "Gold Standard"},
    "chrome_frame": {"set": "core", "target": "frame", "rarity": "rare", "stars": 120, "edition": None,
                     "look": {"c1": "#e8ecff", "c2": "#6b7598", "fx": "shimmer"}, "name": "Рамка «Хром»", "name_en": "Chrome frame"},
    "wander_title": {"set": "core", "target": "title", "rarity": "common", "stars": 50, "edition": None,
                     "look": {"c1": "#00ffe1", "c2": "#00ffe1", "fx": "none"},
                     "name": "Неоновый странник", "name_en": "Neon Wanderer", "text": "Неоновый странник", "text_en": "Neon Wanderer"},
    "rocket_marker": {"set": "core", "target": "marker", "rarity": "common", "stars": 50, "edition": None,
                      "look": {"c1": "#ff8a4c", "c2": "#ffd23f", "fx": "none", "emoji": "🚀"},
                      "name": "Маркер «Ракета»", "name_en": "Rocket marker"},
    "carbon_bag": {"set": "core", "target": "bag", "rarity": "common", "stars": 50, "edition": None,
                   "look": {"c1": "#1b1f29", "c2": "#0b0d12", "fx": "none"}, "name": "Сумка «Карбон»", "name_en": "Carbon bag"},
}
SET_REWARDS = {"aurora": "aur_keeper"}       # набор → скин-награда за коллекцию


def _register_pass_skins() -> None:
    """🎟 Эксклюзивные скины пропуска сезона (по теме месяца) — с ноября 2026 на два года вперёд."""
    from shared.season_pass import pass_skins
    for year in (2026, 2027, 2028):
        for month in range(1, 13):
            if (year, month) >= (2026, 11):
                SKINS.update(pass_skins(f"{year}-{month:02d}"))


_register_pass_skins()


class SkinError(Exception):
    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)


def skin_sku(skin_id: str) -> str:
    return f"skin_{skin_id}"


def skin_level(xp: int, merged: int = 0) -> int:
    """Уровень = самый высокий, для которого хватает и опыта, и поглощений (ступени идут подряд)."""
    level = 1
    for i, (need_xp, need_merged) in enumerate(SKIN_LEVELS):
        if xp >= need_xp and merged >= need_merged:
            level = i + 1
        else:
            break
    return level


def skin_stage(level: int) -> str:
    return [key for start, key in SKIN_STAGES if level >= start][-1]


def next_level_need(xp: int, merged: int) -> dict | None:
    """Что нужно до следующего уровня: {"level", "xp", "merged"} (сколько не хватает) или None на максимуме."""
    level = skin_level(xp, merged)
    if level >= SKIN_MAX_LEVEL:
        return None
    need_xp, need_merged = SKIN_LEVELS[level]
    return {"level": level + 1, "xp": max(0, need_xp - xp), "merged": max(0, need_merged - merged)}


def for_sale(skin_id: str, now: datetime) -> bool:
    s = SKINS.get(skin_id)
    return bool(s and s.get("stars") and (s.get("until") is None or now < s["until"]))


def skin_name(skin_id: str, lang: str) -> str:
    s = SKINS[skin_id]
    return s["name"] if lang == "ru" else s.get("name_en", s["name"])


def public_catalog(lang: str) -> dict:
    """Описание скинов для приложения (вид, редкость, цена, тираж) — рисуется на клиенте.
    Скины пропусков будущих сезонов не отдаём (их ещё нельзя получить), прошлых — отдаём (они есть у игроков)."""
    from shared.economy import utcnow
    from shared.season_pass import sale_season
    horizon = sale_season(utcnow())
    out = {}
    for sid, s in SKINS.items():
        if s.get("pass") and s["pass"] > horizon:
            continue
        out[sid] = {"target": s["target"], "rarity": s["rarity"], "set": s["set"], "look": s["look"],
                    "name": skin_name(sid, lang), "stars": s.get("stars"), "edition": s.get("edition"),
                    "until": s["until"].isoformat() if s.get("until") else None,
                    "text": (s.get("text") if lang == "ru" else s.get("text_en", s.get("text")))}
    return out


def skin_asset(instance_id: int) -> str:
    return f"s_{instance_id}"


def parse_skin_asset(asset: str) -> int | None:
    parts = (asset or "").split("_")
    if len(parts) == 2 and parts[0] == "s" and parts[1].isdigit():
        return int(parts[1])
    return None


# ============================================================================
# БД
# ============================================================================
async def minted(conn, skin_id: str) -> int:
    return await conn.fetchval("SELECT COUNT(*) FROM user_skins WHERE skin_id = $1", skin_id)


async def grant(conn, user_id: int, skin_id: str, source: str, now: datetime) -> dict:
    """Выпускает новый экземпляр с номером тиража (внутри транзакции). SkinError("skin.err_sold_out"), если тираж кончился."""
    s = SKINS.get(skin_id)
    if s is None:
        raise SkinError("skin.err_unknown")
    await conn.execute("SELECT pg_advisory_xact_lock(301030, hashtext($1))", skin_id)   # номера без гонок
    serial = await minted(conn, skin_id) + 1
    if s.get("edition") and serial > s["edition"]:
        raise SkinError("skin.err_sold_out")
    row = await conn.fetchrow(
        "INSERT INTO user_skins (user_id, skin_id, target, serial, source, created_at) VALUES ($1, $2, $3, $4, $5, $6) "
        "RETURNING id, serial", user_id, skin_id, s["target"], serial, source[:32], now)
    await _collection_reward(conn, user_id, s["set"], now)
    logger.info("[SKIN] %s получил(а) %s №%s (%s)", user_id, skin_id, serial, source)
    return {"id": row["id"], "serial": row["serial"], "skin": skin_id}


async def _collection_reward(conn, user_id: int, set_id: str, now: datetime) -> None:
    """Собран весь набор сезона — бесплатная награда (один раз на игрока)."""
    reward = SET_REWARDS.get(set_id)
    if not reward:
        return
    need = {sid for sid, s in SKINS.items() if s["set"] == set_id}
    have = {r["skin_id"] for r in await conn.fetch(
        "SELECT DISTINCT skin_id FROM user_skins WHERE user_id = $1 AND skin_id = ANY($2::text[])", user_id, list(need))}
    if have == need and not await conn.fetchval(
            "SELECT 1 FROM user_skins WHERE user_id = $1 AND skin_id = $2", user_id, reward):
        await grant(conn, user_id, reward, "collection", now)


async def owned(conn, user_id: int) -> list[dict]:
    rows = await conn.fetch(
        "SELECT id, skin_id, target, serial, xp, merged, equipped, stats, created_at FROM user_skins "
        "WHERE user_id = $1 ORDER BY created_at DESC", user_id)
    out = []
    for r in rows:
        level = skin_level(r["xp"], r["merged"])
        out.append({**dict(r), "stats": _stats(r["stats"]), "level": level, "stage": skin_stage(level),
                    "next": next_level_need(r["xp"], r["merged"]), "created_at": r["created_at"].isoformat()})
    return out


def _stats(raw) -> dict:
    import json
    if not raw:
        return {}
    return json.loads(raw) if isinstance(raw, str) else dict(raw)


async def _mine(conn, user_id: int, instance_id: int):
    row = await conn.fetchrow("SELECT * FROM user_skins WHERE id = $1 FOR UPDATE", instance_id)
    if row is None or row["user_id"] != user_id:
        raise SkinError("skin.err_not_yours")
    return row


async def equip(conn, user_id: int, instance_id: int) -> None:
    row = await _mine(conn, user_id, instance_id)
    await conn.execute("UPDATE user_skins SET equipped = FALSE WHERE user_id = $1 AND target = $2 AND equipped",
                       user_id, row["target"])
    await conn.execute("UPDATE user_skins SET equipped = TRUE WHERE id = $1", instance_id)


async def unequip(conn, user_id: int, instance_id: int) -> None:
    await _mine(conn, user_id, instance_id)
    await conn.execute("UPDATE user_skins SET equipped = FALSE WHERE id = $1", instance_id)


async def absorb(conn, user_id: int, instance_id: int, fodder_id: int) -> dict:
    """Закалка: скин поглощает другой экземпляр игрока (тот исчезает навсегда). Возвращает новый уровень и опыт."""
    if instance_id == fodder_id:
        raise SkinError("skin.err_self")
    main = await _mine(conn, user_id, instance_id)
    food = await _mine(conn, user_id, fodder_id)
    if food["equipped"]:
        raise SkinError("skin.err_equipped")
    if skin_level(main["xp"], main["merged"]) >= SKIN_MAX_LEVEL:
        raise SkinError("skin.err_max")
    # поглощённый отдаёт опыт по редкости и половину своего накопленного (его история не пропадает даром)
    gain = SKIN_MERGE_XP[SKINS[food["skin_id"]]["rarity"]] + food["xp"] // 2
    xp, merged = main["xp"] + gain, main["merged"] + 1 + food["merged"] // 2
    before = skin_level(main["xp"], main["merged"])
    await conn.execute("DELETE FROM user_skins WHERE id = $1", fodder_id)
    await conn.execute("UPDATE user_skins SET xp = $2, merged = $3 WHERE id = $1", instance_id, xp, merged)
    logger.info("[SKIN] %s: закалка #%s поглотила #%s (%s), опыт %s", user_id, instance_id, fodder_id, food["skin_id"], xp)
    level = skin_level(xp, merged)
    return {"xp": xp, "merged": merged, "level": level, "stage": skin_stage(level), "gain": gain, "up": level > before}


async def looks(conn, user_ids: list[int]) -> dict[int, dict]:
    """Надетые скины игроков для чужих глаз: {uid: {target: {skin, level, serial}}}."""
    if not user_ids:
        return {}
    rows = await conn.fetch("SELECT user_id, target, skin_id, xp, merged, serial FROM user_skins "
                            "WHERE equipped AND user_id = ANY($1::bigint[])", list(set(user_ids)))
    out: dict[int, dict] = {}
    for r in rows:
        level = skin_level(r["xp"], r["merged"])
        out.setdefault(r["user_id"], {})[r["target"]] = {"skin": r["skin_id"], "level": level,
                                                         "stage": skin_stage(level), "serial": r["serial"]}
    return out


# --- биржа: экземпляр уходит в эскроу (владелец 0) и переходит покупателю ---
async def to_escrow(conn, user_id: int, instance_id: int) -> str:
    row = await _mine(conn, user_id, instance_id)
    await conn.execute("UPDATE user_skins SET user_id = $2, equipped = FALSE WHERE id = $1", instance_id, ESCROW_OWNER)
    return row["skin_id"]


async def from_escrow(conn, user_id: int, instance_id: int) -> None:
    await conn.execute("UPDATE user_skins SET user_id = $2 WHERE id = $1 AND user_id = $3", instance_id, user_id, ESCROW_OWNER)


async def instance_rarity(conn, instance_id: int) -> str | None:
    sid = await conn.fetchval("SELECT skin_id FROM user_skins WHERE id = $1", instance_id)
    return SKINS[sid]["rarity"] if sid in SKINS else None
