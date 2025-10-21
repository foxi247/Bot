# utils/nanobanano_api.py
import asyncio
import aiohttp
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def generate_nanobanano_image(prompt: str) -> str:
    """
    Генерирует изображение через Replicate (Stable Diffusion XL).
    Возвращает URL изображения или None в случае ошибки.
    """
    if not REPLICATE_API_TOKEN:
        raise ValueError("❌ REPLICATE_API_TOKEN не задан")

    async with aiohttp.ClientSession() as session:
        try:
            # Запуск предикшена
            async with session.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {REPLICATE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "39ed52f2a78e934b3ba6e2a89f5b1c712102b1505b650f9075e3683434f3b5fc",  # SDXL
                    "input": {
                        "prompt": f"{prompt}, 4k, high quality",
                        "negative_prompt": "blurry, low quality, text",
                        "width": 768,
                        "height": 768
                    }
                }
            ) as resp:
                if resp.status != 201:
                    error = await resp.text()
                    print(f"Ошибка создания предикшена: {error}")
                    return None
                data = await resp.json()
                prediction_id = data["id"]

            # Ожидание результата (макс. 60 сек)
            for _ in range(60):
                await asyncio.sleep(1)
                async with session.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
                ) as resp:
                    result = await resp.json()
                    if result["status"] == "succeeded":
                        return result["output"][0]  # URL изображения
                    elif result["status"] in ("failed", "canceled"):
                        print(f"Генерация провалена: {result.get('error')}")
                        return None
            return None

        except Exception as e:
            print(f"Исключение при генерации: {e}")
            return None