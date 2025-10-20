# utils/gemini_api.py
import google.generativeai as genai
from data.config import GEMINI_API_KEY
import asyncio

# Настройка API-ключа
genai.configure(api_key=GEMINI_API_KEY)

# Настройки модели
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="models/gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

async def generate_gemini_response(prompt: str) -> str:
    """Асинхронный вызов Gemini API с таймаутом."""
    try:
        # Запускаем синхронный вызов в отдельном потоке (т.к. SDK синхронный)
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=30.0
        )
        return response.text.strip()
    except asyncio.TimeoutError:
        return "❌ Превышено время ожидания ответа от ИИ."
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            return "⚠️ Ошибка: неверный API-ключ Gemini. Обратитесь к администратору."
        elif "block_reason" in error_msg.lower():
            return "🚫 Запрос заблокирован политикой безопасности Gemini."
        else:
            return f"⚠️ Ошибка Gemini: {error_msg[:200]}..."