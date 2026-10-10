import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


def get_farm_keyboard() -> types.InlineKeyboardMarkup:
    """Кнопки управления фермой: только заправка и мгновенный переход в магазин!"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🥩 Заправить 1 шт.", callback_data="farm_action:load_1"),
            types.InlineKeyboardButton(text="⚡ Заправить ВСЁ", callback_data="farm_action:load_all")
        ],
        [
            types.InlineKeyboardButton(text="🏪 Зайти в Магазин /shop", callback_data="open_shop_from_farm")
        ]
    ])


@router.message(Command("farm"))
@router.message(Command("my_farm"))
async def cmd_farm(message: types.Message):
    user_id = message.from_user.id

    from bots.main_bot.handlers.profile import apply_lazy_mining_earnings

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Накатываем автоматические часовые начисления монет прямо при вызове фермы!
            user = await apply_lazy_mining_earnings(user_id, conn)
            if not user:
                await message.answer("⚠️ Профиль не найден. Нажми /start")
                return

    total_miners = user["miner_junior_count"] + user["miner_premium_count"]

    # Расчитываем актуальный статус активности Кибер-Бурильщиков на автопилоте
    if user["miner_premium_count"] > 0:
        if user["fridge_cutlets"] > 0:
            status_work = "🟢 Кибер-Бурильщики активны и добывают валюту автоматически!"
        else:
            status_work = "🔴 Кибер-Бурильщики остановились! В холодильнике кончилось топливо."
    else:
        status_work = "💡 Заведи Кибер-Бурильщиков в /shop для мега-дохода."

    farm_text = (
        f"🚜 <b>ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🤖 Активных роботов на заводе: <b>{total_miners} шт.</b>\n"
        f"• Младшие Майнеры (вечные): <code>{user['miner_junior_count']} шт.</code>\n"
        f"• Кибер-Бурильщики (SaaS): <code>{user['miner_premium_count']} шт.</code>\n\n"
        f"📋 <b>СТАТУС ИГРОВОГО ЗАВОДА:</b>\n"
        f"{status_work}\n\n"
        f"..................................................\n\n"
        f"📦 <b>СОСТОЯНИЕ АВТОМАТИЧЕСКОГО ХОЛОДИЛЬНИКА:</b>\n"
        f"🥩 Запас топлива: <b>{user['fridge_cutlets']} / {user['fridge_capacity']} шт.</b>\n"
        f"💼 Котлеты на складе инвентаря: <code>{user['inv_cutlets']} шт.</code>\n\n"
        f"..................................................\n\n"
        f"💿 <i>Младшие Майнеры косят монеты вечно и бесплатно. Кибер-Бурильщики автоматически потребляют по 1 котлете в сутки из холодильника! Просто держи его заправленным!</i>"
    )

    await message.answer(farm_text, reply_markup=get_farm_keyboard(), parse_mode="HTML")


@router.callback_query(F.data.startswith("farm_action:"))
async def process_farm_inline_actions(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) < 2:
        await callback.answer()
        return
    action = parts

    await callback.answer()

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return

            inv_cutlets = user["inv_cutlets"]
            fridge_cutlets = user["fridge_cutlets"]
            fridge_capacity = user["fridge_capacity"]

            if action == "load_1":
                if inv_cutlets <= 0:
                    await callback.message.answer("❌ У тебя в инвентаре нет кибер-котлет! Купи их в /shop")
                    return
                if fridge_cutlets >= fridge_capacity:
                    await callback.message.answer("📦 Твой Холодильник уже полностью забит!")
                    return
                await conn.execute(
                    "UPDATE users SET inv_cutlets = inv_cutlets - 1, fridge_cutlets = fridge_cutlets + 1 WHERE user_id = $1",
                    user_id)

            elif action == "load_all":
                if inv_cutlets <= 0:
                    await callback.message.answer("❌ У тебя в инвентаре нет кибер-котлет!")
                    return
                available_space = fridge_capacity - fridge_cutlets
                if available_space <= 0:
                    await callback.message.answer("📦 Твой Холодильник забит до отказа!")
                    return
                actual_load = min(inv_cutlets, available_space)
                await conn.execute(
                    "UPDATE users SET inv_cutlets = inv_cutlets - $1, fridge_cutlets = fridge_cutlets + $1 WHERE user_id = $2",
                    actual_load, user_id)

            updated = await conn.fetchrow(
                "SELECT fridge_cutlets, inv_cutlets, fridge_capacity, miner_junior_count, miner_premium_count FROM users WHERE user_id = $1",
                user_id
            )

    total_miners = updated["miner_junior_count"] + updated["miner_premium_count"]
    if updated["miner_premium_count"] > 0:
        if updated["fridge_cutlets"] > 0:
            status_work = "🟢 Кибер-Бурильщики активны и добывают валюту автоматически!"
        else:
            status_work = "🔴 Кибер-Бурильщики остановились! В холодильнике кончилось топливо."
    else:
        status_work = "💡 Заведи Кибер-Бурильщиков в /shop для мега-дохода."

    updated_text = (
        f"🚜 <b>ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🤖 Активных роботов на заводе: <b>{total_miners} шт.</b>\n"
        f"• Младшие Майнеры (вечные): <code>{updated['miner_junior_count']} шт.</code>\n"
        f"• Кибер-Бурильщики (SaaS): <code>{updated['miner_premium_count']} шт.</code>\n\n"
        f"📋 <b>СТАТУС ИГРОВОГО ЗАВОДА:</b>\n"
        f"{status_work}\n\n"
        f"..................................................\n\n"
        f"📦 <b>СОСТОЯНИЕ АВТОМАТИЧЕСКОГО ХОЛОДИЛЬНИКА:</b>\n"
        f"🥩 Запас топлива: <b>{updated['fridge_cutlets']} / {updated['fridge_capacity']} шт.</b>\n"
        f"💼 Котлеты на складе инвентаря: <code>{updated['inv_cutlets']} шт.</code>\n\n"
        f"..................................................\n\n"
        f"💿 <i>Младшие Майнеры косят монеты вечно и бесплатно. Кибер-Бурильщики автоматически потребляют по 1 котлете в сутки из холодильника! Просто держи его заправленным!</i>"
    )

    try:
        await callback.message.edit_text(updated_text, reply_markup=get_farm_keyboard(), parse_mode="HTML")
    except Exception:
        pass


@router.callback_query(F.data == "open_farm_from_profile")
async def open_farm_from_profile_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_farm(callback.message)
