from aiogram import Router, types, F
from aiogram.filters import Command
import html

router = Router()

@router.message(Command("rofl_hub_all"))
@router.message(F.text == "Все проекты и партнёры")
async def cmd_rofl_hub_all(message: types.Message):
    all_projects_text = (
        "<b>Все проекты Cyber Barons и наши партнёры:</b>\n\n"
        "Главный и единственный чат-бот экосистемы @CyberBaronsBot - других чат-ботов у нас нет! "
        "Остерегайся подделок и клонов нашего чат-бота, скорее всего это будут мошенники!\n\n"
        "ТОП игроков, команд и кланов, акции и новости — в игровом приложении бота (паспорт → «События»).\n\n"
        "..................................................\n"
        "<b>Наши друзья и партнёры:</b>\n"
        
        "Создатель Cyber Barons - @mister_telebot\n"
        # "Канал @kolesnikov_pro_zarabotok - серьезно о заработке\n"
        # "- Канал @lol_school_official - Школьная тусовка Ru|Kz|Uz|Az|Ar\n"
        # "- Канал @the_top_investor - Куда вложить деньги, когда их много?\n"
        # "- Канал @trend_skills - Кем работать? Профессии, где платят много\n"
        # "- Сайт TrendSkills - профессии, где платят много trend-skills.com\n"
        # "- Сайт полезного досуга Тесты | Игры | Квесты test-game-quest.com\n"
        # "- Канал @good_anonym - Щедрый аноним. Выполни задание и выиграй приз!\n"
        # "- Канал @code_and_money - Код и деньги | Золотая клавиатура\n"
        "..................................................\n"
        "/menu - показать общее меню\n"
    )

    await message.answer(all_projects_text, parse_mode="HTML")
