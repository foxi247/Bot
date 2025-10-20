# handlers/gemini_handler.py
import asyncio
from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import get_balance, update_balance
from utils.gemini_api import generate_gemini_response

router = Router()

class GeminiState(StatesGroup):
    waiting_for_prompt = State()

@router.callback_query(F.data == "ai_gemini")
async def start_gemini(callback: types.CallbackQuery, state: FSMContext):
    balance = await get_balance(callback.from_user.id)
    if balance < 1:
        await callback.message.answer(
            "❌ Недостаточно монет! Пополните баланс (1 монета = 1 запрос)."
        )
        await callback.answer()
        return

    await callback.message.answer("🧠 Введите ваш запрос для Gemini:")
    await state.set_state(GeminiState.waiting_for_prompt)
    await callback.answer()

@router.message(GeminiState.waiting_for_prompt)
async def process_gemini_prompt(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    prompt = message.text.strip()

    if not prompt:
        await message.answer("Пожалуйста, введите непустой текст.")
        return

    balance = await get_balance(user_id)
    if balance < 1:
        await message.answer("❌ Недостаточно монет! Пополните баланс.")
        await state.clear()
        return

    # Списываем 1 монету
    await update_balance(user_id, -1)
    
    # Анимация "загрузки"
    progress_msg = await message.answer("🔄 Запрос к Gemini: 10%...")
    for percent in [30, 60, 90]:
        await asyncio.sleep(0.6)
        await progress_msg.edit_text(f"🔄 Запрос к Gemini: {percent}%...")
    await asyncio.sleep(0.6)
    await progress_msg.edit_text("✅ Получаю ответ...")

    # Вызов Gemini
    response = await generate_gemini_response(prompt)

    # Возвращаем результат
    await progress_msg.delete()
    await message.answer(
        f"🧠 <b>Gemini ответил:</b>\n\n{response}",
        parse_mode="HTML"
    )
    await state.clear()