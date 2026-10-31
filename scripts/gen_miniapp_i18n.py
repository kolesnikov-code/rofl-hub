"""
Переводы приложения на 12 языков из языковых паков — ОТДЕЛЬНЫМИ файлами static/webapp/i18n/<код>.json.

Запуск из корня проекта: python -m scripts.gen_miniapp_i18n
ru/en живут в index.html руками, остальные 12 языков приходят из shared/locale_packs/<код>.py (словарь MINIAPP).
Раньше все 12 вшивались в index.html (≈630 КБ из 1,2 МБ) — каждый игрок качал и разбирал все языки ради одного.
Теперь в блоке I18N_EXTRA_START / I18N_EXTRA_END — только список языков и версия (хэш), приложение грузит свой
файл параллельно с /api/me, а версия в адресе даёт телефону кэшировать его навсегда.
"""
from __future__ import annotations

import hashlib

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from shared.locales import MINIAPP_PACKS  # noqa: E402

INDEX = PROJECT_ROOT / "static" / "webapp" / "index.html"
START = "// I18N_EXTRA_START"
END = "// I18N_EXTRA_END"


I18N_DIR = PROJECT_ROOT / "static" / "webapp" / "i18n"


def main() -> None:
    packs = {code: pack for code, pack in sorted(MINIAPP_PACKS.items()) if pack}
    I18N_DIR.mkdir(exist_ok=True)
    digest = hashlib.sha1()
    for code, pack in packs.items():
        data = json.dumps(pack, ensure_ascii=False, separators=(",", ":"))
        (I18N_DIR / f"{code}.json").write_text(data, encoding="utf-8", newline="\n")
        digest.update(code.encode() + data.encode("utf-8"))
    for stale in I18N_DIR.glob("*.json"):
        if stale.stem not in packs:
            stale.unlink()
    html = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    replacement = (f"{START} — {len(packs)} языков в static/webapp/i18n/, автогенерация scripts/gen_miniapp_i18n.py, "
                   f"не редактировать руками\n  const I18N_PACKS = {json.dumps(sorted(packs))};\n"
                   f"  const I18N_VER = \"{digest.hexdigest()[:12]}\";\n  {END}")
    new_html, count = pattern.subn(lambda _m: replacement, html)   # функция: «\n» в текстах не становится переводом строки
    if count != 1:
        raise SystemExit("Маркеры I18N_EXTRA не найдены в index.html")
    INDEX.write_text(new_html, encoding="utf-8", newline="\n")
    print(f"Переводы приложения обновлены: языков {len(packs)}, "
          f"ключей на язык {len(next(iter(packs.values()))) if packs else 0}")


if __name__ == "__main__":
    main()
