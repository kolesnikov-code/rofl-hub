from aiogram import Router, types, F
from aiogram.filters import Command
import html

router = Router()

@router.message(Command("help"))
@router.message(F.text == "Список команд")
async def cmd_help(message: types.Message):

    help_text = (
        "<b>ДОСТУПНЫЕ КОМАНДЫ:</b>\n\n"
        "<b>Основные:</b>\n"
        
        "/start - запустить чат-бота заново\n"
        "/stats - показать твою статистику\n"
        "/referral_link - твоя реферральная ссылка\n\n"
        
        "<b>Взаимодействие с другими игроками:</b>\n"
        "/send_coin - перевод монет другому игроку\n"
        "/make_team - создать команду (до 50 игроков)\n"
        "/make_clan - создать клан (до 1000 игроков)\n\n"
        
        "<b>Магазин:</b>\n"        
        "/buy_coins - купить игровые монеты\n"
        "/buy_boost - купить ускоритель (+2 монеты за победу)\n"
        "/buy_miner - купить робота-майнера (автодобыча монет)\n"
        "/buy_post - купить публикацию на сайте\n"
        "/buy_vip - купить VIP-место на сайте\n"
        "/buy_top_id - купить красивый ID ROFL HUB\n\n"
        
        "<b>Все проекты:</b>\n"
        "/rofl_hub_all - все каналы, игры и сайты ROFL HUB (общий список)\n"
        "/games_bot - ссылка на единый чат-бот с играми\n\n"
        
        "<b>Поддержка:</b>\n"
        "/faq - частые вопросы\n"
        "/help - показать это сообщение\n"
        "/support - обращение админу (жалоба на игрока, проблемы с сервисом)\n"


    )

    await message.answer(help_text, parse_mode="HTML")
