"""
Генерация словаря I18N_EXTRA в static/webapp/index.html из языковых паков.

Запуск из корня проекта: python -m scripts.gen_miniapp_i18n
Перезаписывает блок между маркерами I18N_EXTRA_START / I18N_EXTRA_END.
ru/en живут в index.html руками, остальные 12 языков приходят из
shared/locale_packs/<код>.py (словарь MINIAPP).
"""
from __future__ import annotations

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


def main() -> None:
    packs = {code: pack for code, pack in sorted(MINIAPP_PACKS.items()) if pack}
    blob = json.dumps(packs, ensure_ascii=False, indent=2)
    html = INDEX.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    replacement = (f"{START} — {len(packs)} языков, автогенерация scripts/gen_miniapp_i18n.py, "
                   f"не редактировать руками\n  const I18N_EXTRA = {blob};\n  {END}")
    new_html, count = pattern.subn(lambda _m: replacement, html)   # функция: «\n» в текстах не становится переводом строки
    if count != 1:
        raise SystemExit("Маркеры I18N_EXTRA не найдены в index.html")
    INDEX.write_text(new_html, encoding="utf-8")
    print(f"I18N_EXTRA обновлён: языков {len(packs)}, "
          f"ключей на язык {len(next(iter(packs.values()))) if packs else 0}")


if __name__ == "__main__":
    main()
