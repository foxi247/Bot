# handlers/ai_menu.py
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Inline-меню выбора ИИ
ai_services_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🧠 Gemini (текст)", callback_data="ai_gemini"),
    ],
    [
        InlineKeyboardButton(text="🎨 Nano Banano (изображения)", callback_data="ai_nanobanano"),
    ]
])

@router.message(lambda message: message.text == "🤖 ИИ-сервисы")
async def ai_services_menu(message: types.Message):
    await message.answer(
        "Выбери ИИ-сервис:",
        reply_markup=ai_services_kb
    )