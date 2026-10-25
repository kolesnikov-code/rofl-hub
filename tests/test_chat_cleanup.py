"""
💬 Чат короче, игра — в приложении (решения владельца 28.10): кнопки фермы, профиля и команд ведут
в Mini App, удаление аккаунта — командой /delete_account, заголовки без пафоса, у декоративного
многоточия нет пустых строк ни сверху, ни снизу.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOTS = re.compile(r"\.{20,}")


def _buttons(markup):
    return [(b.text, b.web_app.url if b.web_app else b.callback_data) for row in markup.inline_keyboard for b in row]


@pytest.fixture
def with_app(monkeypatch):
    import bots.main_bot.webapp_links as links
    monkeypatch.setattr(links, "WEBAPP_URL", "https://app.example")


def test_farm_keyboard_only_bonus_refuel_and_app(with_app):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.farm import get_farm_keyboard
    texts = [b[0] for b in _buttons(get_farm_keyboard("ru"))]
    assert any("ЗАБРАТЬ БОНУС" in x for x in texts) and any("Заправить" in x for x in texts)
    assert "🏭 Ферма и биржа в приложении" in texts
    assert not any(x in " ".join(texts) for x in ("Магазин", "Мастерская", "Биржа котлет"))
    app = next(b for b in _buttons(get_farm_keyboard("ru")) if b[0].startswith("🏭"))
    assert app[1].endswith("tab=farm")


def test_farm_keyboard_without_app_keeps_chat_market(monkeypatch):
    pytest.importorskip("aiogram")
    import bots.main_bot.webapp_links as links
    monkeypatch.setattr(links, "WEBAPP_URL", "")
    from bots.main_bot.handlers.farm import get_farm_keyboard
    assert ("📈 Биржа котлет", "open_market") in _buttons(get_farm_keyboard("ru"))   # отказоустойчивость


def test_profile_has_single_open_app_button(with_app):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.profile import profile_keyboard_for
    buttons = _buttons(profile_keyboard_for("ru"))
    assert buttons == [("📱 ОТКРЫТЬ ПРИЛОЖЕНИЕ", "https://app.example?tab=passport")]


def test_delete_account_moved_to_menu_command():
    from shared.locales import t
    assert "/delete_account" in t("ru", "menu.text") and "/delete_account" in t("en", "menu.text")
    src = (ROOT / "bots" / "main_bot" / "handlers" / "account.py").read_text(encoding="utf-8")
    assert 'Command("delete_account")' in src and 'F.data == "acct_del"' in src   # старые кнопки в чате тоже работают


def test_new_headers_and_texts():
    from shared.locales import t
    farm = t("ru", "farm.dashboard", total=1, intern="", junior=0, premium=0, junior_rate=5, premium_rate=10,
             burnout="", speed_hour=1, speed_day=24, boosts="—", status="—", fridge=0, capacity=1, inv=0)
    assert "СТАТУС ФЕРМЫ:" in farm and "СКОРОСТЬ ДОБЫЧИ:" in farm and "📦 <b>ХОЛОДИЛЬНИК:</b>" in farm
    assert "Котлеты на складе: " in farm and "инвентаря" not in farm and "ТОПЛИВНЫЙ ХАБ" not in farm
    assert t("ru", "farm.intern_line", rate=1, count=1).startswith("• Роботы-Стажёры (1 🪙/ч)")
    assert "/shop" not in t("ru", "farm.status_no_drills")
    profile = t("ru", "profile.caption", user_id=1, vip="", balance=1, team="—", level=1, next_level=2, left=1, reward=200)
    assert "ТВОЙ ПРОФИЛЬ ROFL HUB" in profile and "В приложении есть всё" in profile and "ЛИЧНЫЙ КАБИНЕТ" not in profile
    clans = (ROOT / "bots" / "main_bot" / "handlers" / "clans.py").read_text(encoding="utf-8")
    assert "КОМАНДЫ И КЛАНЫ ROFL HUB" in clans and "ЦЕНТРАЛЬНЫЙ ОФИС" not in clans


def test_intern_written_with_hyphen_everywhere():
    for path in ("shared/locales.py", "static/webapp/index.html", "static/webapp/faq.html"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert not re.search(r"Робот\w* Стажёр", text), path


def test_no_blank_lines_around_decorative_dots_in_any_language():
    from shared.locales import STRINGS
    bad = []
    for lang, table in STRINGS.items():
        for key, value in table.items():
            if not isinstance(value, str) or not DOTS.search(value):
                continue
            if re.search(r"\n\s*\n" + DOTS.pattern, value) or re.search(DOTS.pattern + r"\n\s*\n", value):
                bad.append(f"{lang}:{key}")
    assert not bad, bad[:10]


def test_every_chat_handler_is_a_coroutine_and_profile_is_wired():
    """Регрессия 28.10: функция, вставленная между декораторами и обработчиком, «украла» кнопку «Мой профиль»."""
    pytest.importorskip("aiogram")
    import importlib
    import inspect
    import pkgutil
    import bots.main_bot.handlers as pkg
    seen = {}
    for mod in pkgutil.iter_modules(pkg.__path__):
        module = importlib.import_module(f"bots.main_bot.handlers.{mod.name}")
        router = getattr(module, "router", None)
        if router is None:
            continue
        for observer in (router.message, router.callback_query):
            for h in observer.handlers:
                assert inspect.iscoroutinefunction(h.callback), f"{mod.name}.{h.callback.__name__} — не обработчик"
                seen.setdefault(mod.name, set()).add(h.callback.__name__)
    assert "cmd_profile_stats" in seen["profile"]
