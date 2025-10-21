import replicate
import requests
from aiogram import Router, types
from aiogram.filters import Command
from config import REPLICATE_API_TOKEN # Убедись, что токен добавлен в config.py

router = Router()

# Установка токена из конфига
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

@router.message(Command("generate_image")) # Или по нажатию кнопки
async def generate_image(message: types.Message):
    user_id = message.from_user.id
    prompt = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "A generic image of a cat"

    try:
        # Запуск модели
        output = replicate_client.run(
            "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
            input={
                "width": 768,
                "height": 768,
                "prompt": prompt,
                "refine": "expert_ensemble_refiner",
                "apply_watermark": False,
                "num_inference_steps": 25
            }
        )

        if output and len(output) > 0:
            image_url = output[0] # Берём первый URL из результата
            # Отправляем фото в чат
            await message.answer_photo(photo=image_url, caption=f"Generated image for: {prompt}")
        else:
            await message.answer("Failed to generate image: No output received.")
    except Exception as e:
        print(f"Error generating image with Replicate: {e}") # Логируем ошибку
        await message.answer(f"An error occurred while generating the image: {str(e)}")

# Не забудь импортировать и использовать этот роутер в bot.py, как делали с gemini_router
