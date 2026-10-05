from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from shared.db_vip import check_and_buy_vip_id

router = Router()


# Настраиваем состояния памяти FSM
class VipPurchaseState(StatesGroup):
    wait_for_vip_id = State()


@router.message(Command("buy_vip"))
async def cmd_buy_vip(message: types.Message, state: FSMContext):
    """Начало Аукциона Тщеславия"""
    vip_text = (
        "👑 <b>ЦИФРОВОЙ МАГАЗИН VIP ID</b>\n"
        "..................................................\n\n"
        "✨ <b>Хочешь выделить свой профиль из серой массы?</b>\n"
        "Ты можешь навсегда стереть свой скучный цифровой Telegram ID "
        "и заменить его на элитарное имя или красивые цифры "
        "(например <code>777</code>, <code>AKULA</code>, <code>BOSS</code>)!\n\n"
        "🔥 Твой новый VIP ID будет гордо отображаться в команде /my_stats!\n"
        "💳 Стоимость услуги: <b>100 000 рофлов</b>.\n\n"
        "..................................................\n"
        "👇 <b>Введи желаемый VIP ID прямо сейчас (от 3 до 15 символов):</b>\n"
        "<i>(Или введи /cancel для отмены)</i>"
    )
    await message.answer(vip_text, parse_mode="HTML")
    await state.set_state(VipPurchaseState.wait_for_vip_id)


@router.message(VipPurchaseState.wait_for_vip_id)
async def process_vip_id_input(message: types.Message, state: FSMContext):
    vip_id_candidate = message.text.strip()

    # Защита от дурака: если ребенок решил отменить
    if vip_id_candidate.startswith("/"):
        await state.clear()
        await message.answer("🛑 Покупка VIP ID отменена.")
        return

    user_id = message.from_user.id

    # Стучимся в базу в Амстердам
    result = await check_and_buy_vip_id(user_id, vip_id_candidate)

    if result == "OK":
        await message.answer(
            f"🎉 <b>ПОЗДРАВЛЯЕМ, VIP-ИГРОК!</b>\n"
            f"..................................................\n\n"
            f"Корона успешно выкуплена! Красивый ID <b>{vip_id_candidate.upper()}</b> "
            f"привязан к твоему паспорту.\n\n"
            f"🚀 <i>Проверь свой новый статус прямо сейчас, введя команду /my_stats !</i>",
            parse_mode="HTML"
        )
        await state.clear()
    else:
        # Если база выдала ошибку (занят или нет денег) — выводим текст ошибки и не сбрасываем состояние, пускай пробует еще!
        await message.answer(result, parse_mode="HTML")
