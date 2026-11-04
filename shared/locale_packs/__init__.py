"""
Языковые паки Cyber Barons. Каждый модуль <код>.py экспортирует:
- BUTTONS: dict[key, str] — 8 reply-кнопок;
- STRINGS: dict[key, str] — все ключи интерфейса (эталон ключей — RU в shared/locales.py);
- MINIAPP: dict[key, str] — словарь Mini App (эталон — I18N в static/webapp/index.html);
- COMMANDS: dict[cmd, str] — описания команд синего меню (эталон — BOT_COMMANDS в bot.py).

Сборка — в shared/locales.py. Русский и английский живут в самом locales.py.
"""
