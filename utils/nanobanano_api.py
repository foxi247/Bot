# utils/nanobanano_api.py
import asyncio
import aiohttp
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def generate_nanobanano_image(prompt: str) -> str:
    if not REPLICATE_API_TOKEN:
        print("❌ REPLICATE_API_TOKEN не задан в .env или переменных окружения!")
        return None # Не вызываем ValueError, чтобы бот не падал

    # АКТУАЛЬНАЯ версия из официального примера Replicate (октябрь 2025)
    MODEL_VERSION = "7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"

    async with aiohttp.ClientSession() as session:
        try:
            # Создаём задачу генерации
            async with session.post(
                "https://api.replicate.com/v1/predictions", # <--- УБРАНЫ ПРОБЕЛЫ
                headers={
                    "Authorization": f"Token {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": MODEL_VERSION,
                    "input": {
                        "prompt": prompt,
                        "width": 768,
                        "height": 768,
                        "refine": "expert_ensemble_refiner",
                        "apply_watermark": False,
                        "num_inference_steps": 25
                    }
                }
            ) as resp:
                if resp.status != 201:
                    error_text = await resp.text()
                    print(f"❌ Ошибка создания задачи: {resp.status} — {error_text}")
                    return None
                data = await resp.json()
                prediction_id = data["id"]
                print(f"✅ Задача создана: {prediction_id}")

            # Ждём результат (макс. 100 секунд)
            print("⏳ Ожидание генерации изображения...")
            for _ in range(100):
                await asyncio.sleep(1)
                async with session.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}", # <--- УБРАН ПРОБЕЛ
                    headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
                ) as resp:
                    result = await resp.json()
                    status = result["status"]
                    print(f"   Статус задачи: {status}")
                    if status == "succeeded":
                        output_urls = result.get("output", [])
                        if output_urls:
                            print("✅ Изображение готово!")
                            return output_urls[0]  # Возвращаем URL первого изображения
                        else:
                            print("❌ Изображение готово, но URL не найден в ответе.")
                            return None
                    elif status in ("failed", "canceled"):
                        error = result.get("error", "Неизвестная ошибка")
                        print(f"❌ Генерация провалена: {error}")
                        return None
            print("❌ Таймаут: генерация дольше 100 секунд")
            return None

        except Exception as e:
            print(f"💥 Ошибка в generate_nanobanano_image: {e}")
            return None
