# bot_local.py — для локального запуска через polling
import asyncio
import logging
from aiogram import Bot, Dispatcher
from data.config import TELEGRAM_BOT_TOKEN
from database.db import init_db

# Импорты роутеров
from handlers.start import router as start_router
from handlers.balance import router as balance_router
from handlers.profile import router as profile_router
from handlers.ai_menu import router as ai_menu_router
from handlers.gemini_handler import router as gemini_router  # ← важно: gemini_router

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(profile_router)
    dp.include_router(ai_menu_router)
    dp.include_router(gemini_router)  # ← исправлено!

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())