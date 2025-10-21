# handlers/nanobanano_handler.py
from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import get_balance, update_balance
from utils.nanobanano_api import generate_nanobanano_image
import asyncio

router = Router()

class NanoBananoState(StatesGroup):
    waiting_for_prompt = State()

@router.callback_query(F.data == "ai_nanobanano")
async def start_nanobanano(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    balance = await get_balance(user_id)
    if balance < 1:
        await callback.message.answer("❌ Недостаточно монет! Пополните баланс.")
        await callback.answer()
        return

    await callback.message.answer("🎨 Отправьте описание изображения для Nano Banano:")
    await state.set_state(NanoBananoState.waiting_for_prompt)
    await callback.answer()

@router.message(NanoBananoState.waiting_for_prompt)
async def process_nanobanano_prompt(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    prompt = message.text.strip()

    if not prompt:
        await message.answer("Пожалуйста, введите непустое описание.")
        return

    balance = await get_balance(user_id)
    if balance < 1:
        await message.answer("❌ Недостаточно монет!")
        await state.clear()
        return

    # Списываем 1 монету
    await update_balance(user_id, -1)

    # Анимация загрузки
    progress_msg = await message.answer("🍌 Nano Banano: 10%...")
    for percent in [30, 60, 90]:
        await asyncio.sleep(0.8)
        await progress_msg.edit_text(f"🍌 Nano Banano: {percent}%...")
    await asyncio.sleep(0.8)
    await progress_msg.edit_text("✅ Генерирую изображение...")

    # Генерация через Replicate
    image_url = await generate_nanobanano_image(prompt)

    await progress_msg.delete()

    if image_url:
        await message.answer_photo(
            photo=image_url,
            caption="✨ Ваше изображение готово! (сгенерировано через Nano Banano)"
        )
    else:
        await message.answer(
            "⚠️ Не удалось сгенерировать изображение. Попробуйте другое описание."
        )
    await state.clear()