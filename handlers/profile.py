# handlers/profile.py
from aiogram import Router, types
from database.db import get_user

router = Router()

@router.message(lambda message: message.text == "👤 Профиль")
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Профиль не найден. Напиши /start.")
        return

    user_id, username, balance, role = user
    await message.answer(
        f"👤 <b>Профиль</b>\n\n"
        f"ID: <code>{user_id}</code>\n"
        f"Имя: @{username}\n"
        f"Роль: {role}\n"
        f"Баланс: {balance} монет\n\n"
        f"История запросов будет здесь позже."
    )