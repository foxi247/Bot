# utils/nanobanano_api.py
import asyncio
import aiohttp
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def generate_nanobanano_image(prompt: str) -> str:
    if not REPLICATE_API_TOKEN:
        raise ValueError("❌ REPLICATE_API_TOKEN не задан")

    # Актуальная версия SDXL (на октябрь 2025)
    MODEL_VERSION = "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"

    async with aiohttp.ClientSession() as session:
        try:
            # Создание задачи
            async with session.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": MODEL_VERSION,
                    "input": {
                        "prompt": prompt,
                        "negative_prompt": "ugly, blurry, text, signature",
                        "width": 768,
                        "height": 768,
                        "num_outputs": 1
                    }
                }
            ) as resp:
                if resp.status != 201:
                    error_text = await resp.text()
                    print(f"❌ Ошибка создания: {resp.status} - {error_text}")
                    return None
                data = await resp.json()
                prediction_id = data["id"]

            # Ожидание результата (до 90 сек)
            for i in range(90):
                await asyncio.sleep(1)
                async with session.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
                ) as resp:
                    result = await resp.json()
                    status = result["status"]
                    if status == "succeeded":
                        return result["output"][0]
                    elif status in ("failed", "canceled"):
                        error = result.get("error", "Неизвестная ошибка")
                        print(f"❌ Генерация провалена: {error}")
                        return None
            print("❌ Таймаут: генерация заняла больше 90 секунд")
            return None

        except Exception as e:
            print(f"💥 Исключение: {e}")
            return None