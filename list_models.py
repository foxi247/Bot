# list_models.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY не найден в .env")
    exit(1)

genai.configure(api_key=API_KEY)

print("🔍 Доступные модели с поддержкой generateContent:\n")
try:
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"✅ {model.name}")
except Exception as e:
    print(f"⚠️ Ошибка при получении списка моделей: {e}")