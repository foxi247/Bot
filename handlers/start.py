# handlers/start.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import create_user, get_balance

router = Router()

# Главное меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💰 Баланс"),
            KeyboardButton(text="👤 Профиль"),
        ],
        [
            KeyboardButton(text="🤖 ИИ-сервисы"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    
    await create_user(user_id, username)
    balance = await get_balance(user_id)
    
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Твой ID: <code>{user_id}</code>\n"
        f"Текущий баланс: <b>{balance}</b> монет 💰\n\n"
        f"Выбери действие в меню ниже:",
        reply_markup=main_menu_kb
    )