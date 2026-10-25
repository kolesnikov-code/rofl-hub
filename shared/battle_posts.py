"""
📣 Посты битв и акций в канал — ОДНИМ сообщением сразу на всех 14 языках (решение владельца 27.10:
в канале каждый видит свой язык, личных рассылок нет — сами не пишем, ничего не нарушаем).

Общая часть (название, сроки, призы эмодзи и числами, рудники, таблица) — один раз; под ней по
строке на каждый язык: флаг + зачёт, номинация и призыв. Свои формулировки номинаций владельца
выводятся как есть (он пишет их на нужных языках сам). Лимит Telegram — 4096 символов.
"""
from __future__ import annotations

import html
import os

from shared.locales import t

# Порядок и флаги — как в сетке выбора языка при /start (bots/main_bot/handlers/start.py)
POST_LANGS = (("en", "🇺🇸"), ("es", "🇪🇸"), ("uz", "🇺🇿"), ("fr", "🇫🇷"), ("ru", "🇷🇺"), ("pt", "🇧🇷"),
              ("de", "🇩🇪"), ("it", "🇮🇹"), ("pl", "🇵🇱"), ("id", "🇮🇩"), ("zh", "🇨🇳"), ("hi", "🇮🇳"),
              ("ar", "🇦🇪"), ("bn", "🇧🇩"))
TG_LIMIT = 4096
DOTS = "." * 40
MAX_PRIZE_LINES = 10


def _medal(place: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, f"{place}.")


def _nom(lang: str, battle) -> str:
    from shared.battles import BATTLE_NOMINATIONS, MANUAL_NOMINATIONS
    key = battle["nomination_key"]
    if key in BATTLE_NOMINATIONS or key in MANUAL_NOMINATIONS:
        return t(lang, f"nom.{key}")
    return html.escape(battle["nomination_text"] or "")


def _mines_line(mine_ids: list[int], kinds: dict[int, str]) -> str:
    from shared.resources import RESOURCE_ICONS
    return "⛏ " + " · ".join(f"{_medal(i)} №{m} {RESOURCE_ICONS.get(kinds.get(m, ''), '')}".rstrip()
                            for i, m in enumerate(mine_ids, start=1))


def _fit(lines: list[str]) -> str:
    text = "\n".join(lines)
    return text if len(text) <= TG_LIMIT else text[:TG_LIMIT - 1] + "…"


def build_announce(battle, prizes: dict[int, list[dict]], mine_kinds: dict[int, str]) -> str:
    from shared.battles import battle_mines, battery_fee
    from shared.prizes import rewards_label
    scope = battle["scope"] or "teams"
    mines = battle_mines(battle)
    lines = [f"⚔️ <b>{html.escape(battle['title'])}</b>",
             f"🕐 {battle['starts_at']:%d.%m %H:%M} → 🏁 {battle['ends_at']:%d.%m %H:%M} UTC", ""]
    for place in sorted(prizes)[:MAX_PRIZE_LINES]:
        lines.append(f"{_medal(place)} {html.escape(rewards_label(prizes[place]))}")
    if len(prizes) > MAX_PRIZE_LINES:
        lines.append(f"… +{len(prizes) - MAX_PRIZE_LINES}")
    if mines:
        lines.append(_mines_line(mines, mine_kinds))
    lines += ["", DOTS]
    for lang, flag in POST_LANGS:
        line = t(lang, "post.battle_line", scope=t(lang, f"post.scope_{scope}"), nom=_nom(lang, battle))
        if mines:
            line += " " + t(lang, "post.fee_part", fee=battery_fee(False), fee_clan=battery_fee(True))
        lines.append(f"{flag} {line}")
    bot = os.getenv("MAIN_BOT_USERNAME", "RoflHubGame_Bot").lstrip("@")
    lines += [DOTS] + ([f"👉 @{bot}"] if bot else [])
    return _fit(lines)


def build_auction_announce(auction, deep_link: str) -> str:
    """Анонс VIP-аукциона на всех языках: лот, старт, шаг, финиш, ссылка для ставки."""
    alias = html.escape(auction["vip_alias"] or auction["item_title"])
    lines = [f"💎 <b>{alias}</b>",
             f"💰 {auction['current_price']:,} 🪙 · 🚀 +{auction['min_step']:,} 🪙".replace(",", " ")
             + (f" · 🏁 {auction['ends_at']:%d.%m %H:%M} UTC" if auction["ends_at"] else ""), "", DOTS]
    for lang, flag in POST_LANGS:
        lines.append(f"{flag} {t(lang, 'post.auction_line', alias=alias)}")
    lines += [DOTS, f"👉 {deep_link}"]
    return _fit(lines)


def build_auction_result(auction, winner_name: str | None) -> str:
    alias = html.escape(auction["vip_alias"] or auction["item_title"])
    head = [f"🏁 💎 <b>{alias}</b>"]
    if winner_name:
        head.append(f"👑 {html.escape(winner_name)} · {auction['current_price']:,} 🪙".replace(",", " "))
    lines = head + ["", DOTS]
    key = "post.auction_won" if winner_name else "post.auction_none"
    for lang, flag in POST_LANGS:
        lines.append(f"{flag} {t(lang, key, alias=alias)}")
    lines.append(DOTS)
    return _fit(lines)


def build_results(battle, results: dict) -> str:
    from shared.prizes import rewards_label
    places = results.get("places") or []
    lines = [f"🏁 <b>{html.escape(battle['title'])}</b>", ""]
    for row in places:
        score = f" — {row['score']}" if row.get("score") is not None else ""
        extra = []
        if row.get("rewards"):
            extra.append("🎁 " + rewards_label(row["rewards"]))
        if row.get("mine_id"):
            extra.append(f"⛏ №{row['mine_id']}")
        lines.append(f"{_medal(row['place'])} <b>{html.escape(str(row['name']))}</b>{score}"
                     + (" · " + html.escape(" · ".join(extra)) if extra else ""))
    lines += ["", DOTS]
    key = "post.results_line" if places else "post.results_empty"
    for lang, flag in POST_LANGS:
        lines.append(f"{flag} {t(lang, key, nom=_nom(lang, battle))}")
    lines.append(DOTS)
    return _fit(lines)



def build_expedition_announce(target, prizes: dict[int, list[dict]], reward_all: list[dict]) -> str:
    """🗺 Новая цель экспедиции на карте мира: название, час итогов, призы — и строка на каждый язык."""
    from shared.prizes import rewards_label
    lines = [f"{html.escape(target['icon'])} <b>{html.escape(target['title'])}</b>",
             f"🏁 {target['resolve_at']:%d.%m %H:%M} UTC", ""]
    if target["descr"]:
        lines[2:2] = [f"<i>{html.escape(target['descr'][:300])}</i>"]
    for place in sorted(prizes)[:MAX_PRIZE_LINES]:
        lines.append(f"{_medal(place)} {html.escape(rewards_label(prizes[place]))}")
    if reward_all:
        lines.append(f"🎒 {html.escape(rewards_label(reward_all))}")
    lines += ["", DOTS]
    for lang, flag in POST_LANGS:
        lines.append(f"{flag} {t(lang, 'post.exp_line', scope=t(lang, 'post.scope_' + target['scope']))}")
    bot = os.getenv("MAIN_BOT_USERNAME", "RoflHubGame_Bot").lstrip("@")
    lines += [DOTS] + ([f"👉 @{bot}"] if bot else [])
    return _fit(lines)


def build_expedition_results(target, results: dict) -> str:
    """🏁 Итоги экспедиции: места по грузу (топ-3 ярко), сколько дошло и опоздало."""
    from shared.prizes import rewards_label
    places = results.get("places") or []
    lines = [f"🏁 {html.escape(target['icon'])} <b>{html.escape(target['title'])}</b>", ""]
    for row in places[:MAX_PRIZE_LINES]:
        name = html.escape(str(row["name"]))
        name = f"<b>{name}</b>" if row["place"] <= 3 else name
        extra = " · 🎁 " + html.escape(rewards_label(row["rewards"])) if row.get("rewards") else ""
        lines.append(f"{_medal(row['place'])} {name} — 📦 {row['cargo']}{extra}")
    if len(places) > MAX_PRIZE_LINES:
        lines.append(f"… +{len(places) - MAX_PRIZE_LINES}")
    lines.append(f"🚶 {results.get('arrived', 0)} · ⌛ {results.get('late', 0)}")
    lines += ["", DOTS]
    key = "post.exp_results_line" if places else "post.exp_results_empty"
    for lang, flag in POST_LANGS:
        lines.append(f"{flag} {t(lang, key)}")
    lines.append(DOTS)
    return _fit(lines)
