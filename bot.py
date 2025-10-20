# bot.py
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from database.db import init_db

# Импорты роутеров
from handlers.start import router as start_router
from handlers.balance import router as balance_router
from handlers.profile import router as profile_router
from handlers.ai_menu import router as ai_menu_router
from handlers.gemini_handler import router as gemini_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Константы
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "aK9#mQ2$vL8!pX5"  # ← можно оставить, но лучше задать в .env
WEBHOOK_PORT = int(os.environ.get("PORT", 8000))

async def on_startup(bot: Bot) -> None:
    await init_db()
    base_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not base_url:
        logging.error("RENDER_EXTERNAL_URL не задан! Webhook не будет работать.")
        return
    webhook_url = f"{base_url}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)
    logging.info(f"✅ Webhook установлен: {webhook_url}")

async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)

def main() -> None:
    from data.config import TELEGRAM_BOT_TOKEN
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(profile_router)
    dp.include_router(ai_menu_router)
    dp.include_router(gemini_router)

    # Регистрируем события
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Создаём aiohttp приложение
    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    # Запуск сервера
    web.run_app(app, host="0.0.0.0", port=WEBHOOK_PORT)

if __name__ == "__main__":
    main()