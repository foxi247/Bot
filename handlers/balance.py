# handlers/balance.py
from aiogram import Router, types
from database.db import get_balance

router = Router()

@router.message(lambda message: message.text == "💰 Баланс")
async def show_balance(message: types.Message):
    balance = await get_balance(message.from_user.id)
    await message.answer(
        f"💰 Твой текущий баланс: <b>{balance}</b> монет.\n\n"
        f"Хочешь пополнить? Напиши /pay или выбери опцию позже."
    )