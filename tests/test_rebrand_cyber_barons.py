"""🏷 04.11: игра переименована ROFL HUB → Cyber Barons (на час была Bot Barons) (новый бот @CyberBaronsBot). Старое имя игроку не показываем."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = re.compile(r"ROFL HUB|ROFL-HUB-|RoflHub|rofl-hub-card|Bot Barons|BotBaronsBot", re.IGNORECASE)   # и промежуточное имя 04.11
# Внутренние имена (не видны игроку) и миграция переименования — можно
ALLOWED = ("shared/database.py",)


def _player_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.split()
    return [f for f in out if f.startswith(("shared/", "bots/", "static/", "data/"))
            and f.endswith((".py", ".html", ".js", ".json", ".csv")) and f not in ALLOWED]


def test_old_name_is_gone_from_everything_players_see():
    left = []
    for f in _player_files():
        text = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
        for m in OLD.finditer(text):
            left.append(f"{f}: …{text[max(0, m.start() - 30):m.end() + 10]}…")
    assert not left, "\n".join(left[:20])


def test_new_name_bot_and_vip_prefix():
    from bots.main_bot.webapp_admin import VIP_PREFIX
    from shared.locales import SUPPORTED_LANGS, t
    assert VIP_PREFIX == "BARON-"
    for lang in SUPPORTED_LANGS:
        assert "Cyber Barons" in t(lang, "start.intro1"), lang      # первое знакомство — с новым именем
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "cyber-barons-card.jpg" in html and "Cyber Barons" in html
    bot_src = (ROOT / "bots" / "main_bot" / "bot.py").read_text(encoding="utf-8")
    assert 'MenuButtonWebApp(text="🎮 Cyber Barons"' in bot_src


def test_vip_rename_migration_is_idempotent_sql():
    from shared.database import SCHEMA_STATEMENTS
    sql = " ".join(SCHEMA_STATEMENTS)
    assert "UPDATE vip_aliases SET alias = 'BARON-' || substr(alias, 10) WHERE alias LIKE 'ROFL-HUB-%'" in sql
    assert len("ROFL-HUB-") + 1 == 10   # substr с 10-го символа — всё после старого префикса
