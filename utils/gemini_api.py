import asyncio
import google.generativeai as genai
from data.config import GEMINI_API_KEY

# Настройка API
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY не задан в переменных окружения!")

genai.configure(api_key=GEMINI_API_KEY)

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

# Используем рабочую модель (проверь через list_models.py!)
# ... остальной код ...

# Используем гарантированно доступную модель
MODEL_NAME = "models/gemini-2.5-flash-image"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    safety_settings=safety_settings,
)

async def generate_gemini_response(prompt: str) -> str:
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=30.0
        )
        if response.text:
            return response.text.strip()
        else:
            return "⚠️ Gemini вернул пустой ответ."
    except asyncio.TimeoutError:
        return "❌ Превышено время ожидания."
    except Exception as e:
        error_str = str(e)
        if "API_KEY_INVALID" in error_str:
            return "⚠️ Неверный API-ключ Gemini."
        elif "404" in error_str:
            return f"❌ Модель не найдена. Проверьте имя: {MODEL_NAME}"
        elif "block_reason" in error_str:
            return "🚫 Запрос заблокирован безопасностью."
        else:
            return f"⚠️ Ошибка: {error_str[:150]}..."