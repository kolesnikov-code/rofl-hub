from aiogram import Router, types, F
from aiogram.filters import Command
from shared.db_stats import get_complete_user_data
from shared.strings import get_plural_cutlets
router = Router()


# ----------------------------------------------------------------
# 💰 КОМАНДА: /balance
# ----------------------------------------------------------------
@router.message(Command("balance"))
async def cmd_balance(message: types.Message):
    data = await get_complete_user_data(message.from_user.id)
    if not data:
        await message.answer("⚠️ Ты еще не зарегистрирован в системе! Нажми /start")
        return
    await message.answer(
        f"💰 <b>ТВОЙ КОШЕЛЁК ROFL HUB:</b>\n..................................................\n\n"
        f"🪙 На твоем счету: <code>{data['balance']}</code> рофлов",
        parse_mode="HTML")


# ----------------------------------------------------------------
# 📊 КОМАНДА: /my_stats
# ----------------------------------------------------------------
@router.message(Command("my_stats"))
async def cmd_my_stats(message: types.Message):
    data = await get_complete_user_data(message.from_user.id)
    if not data: return

    display_id = f"👑 <b>VIP ID:</b> <code>{data['rofl_hub_id']}</code>" if data[
        'rofl_hub_id'] else f"📎 <b>ID Паспорта:</b> <code>{message.from_user.id}</code>"

    # ГЕНИАЛЬНАЯ СТРОКА: Прогоняем число из базы через наш математический фильтр!
    cutlets_text = get_plural_cutlets(data['inv_cutlets'])

    profile_text = (
        f"🛸 <b>ЛИЧНЫЙ ПРОФИЛЬ ИГРОКА @{message.from_user.username or 'NoName'}</b>\n"
        f"..................................................\n\n"
        f"{display_id}\n"
        f"💰 <b>Баланс на счету:</b> <code>{data['balance']}</code> рофлов\n"
        f"🥩 <b>В твоем инвентаре:</b> {cutlets_text}\n"  # Текст встанет идеально!
        f"👥 <b>Твоя банда:</b> <code>{data['ref_count']}</code> рефералов\n\n"
        f"..................................................\n\n"
        f"📊 <b>БОЕВАЯ СТАТИСТИКА ДУЭЛЕЙ:</b>\n"
        f"• Сыграно раундов: <code>{data['games_played']}</code>\n"
        f"• Успешных побед: <code>{data['games_won']}</code>"
    )
    await message.answer(profile_text, parse_mode="HTML")


# ----------------------------------------------------------------
# 👥 КОМАНДА: /referral_link
# ----------------------------------------------------------------
@router.message(Command("referral_link"))
async def cmd_referral_link(message: types.Message):
    ref_link = f"https://t.me{message.from_user.id}"
    ref_text = (
        f"👥 <b>ТВОЯ РЕФЕРАЛЬНАЯ ССЫЛКА:</b>\n"
        f"..................................................\n"
        f"<code>{ref_link}</code>\n"
        f"..................................................\n"
        f"🎁 Скопируй ссылку и кидай друзьям! За каждого, кто придёт по твоему приглашению, "
        f"ты МГНОВЕННО получишь <b>+1 000 рофлов</b> на счет!"
    )
    await message.answer(ref_text, parse_mode="HTML")


# ----------------------------------------------------------------
# 🚜 КОМАНДА: /farm
# ----------------------------------------------------------------
@router.message(Command("my_farm"))
async def cmd_farm(message: types.Message):
    data = await get_complete_user_data(message.from_user.id)
    if not data: return

    my_farm_text = (
        f"🚜 <b>КИБЕР-ФЕРМА АВТОДОБЫЧИ МОНЕТ</b>\n"
        f"..................................................\n\n"
        f"🥩 В кармане лежит: <b>{data['inv_cutlets']} Кибер-Котлета</b>\n"
        f"🤖 Активных роботов-майнеров: <b>0 шт.</b>\n\n"
        f"..................................................\n\n"
        f"💿 <b>ВНИМАНИЕ!</b>\n"
        f"Твоя котлета лежит без дела! Введи команду /buy_miner, "
        f"чтобы купить Бурильщика и запустить круглосуточный пассивный фарм!"
    )
    await message.answer(my_farm_text, parse_mode="HTML")
