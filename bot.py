import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from database.db import init_db

from handlers.start import router as start_router
from handlers.balance import router as balance_router
from handlers.profile import router as profile_router
from handlers.ai_menu import router as ai_menu_router
from handlers.gemini_handler import router as gemini_router
from handlers.nanobanano_handler import router as nanobanano_router
logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "gemini_bot_secure_2025_xyz"
WEBHOOK_PORT = int(os.environ.get("PORT", 8000))

async def on_startup(bot: Bot) -> None:
    await init_db()
    base_url = os.environ.get("WEBHOOK_URL")
    if not base_url:
        logging.error("❌ Не найден публичный URL (RAILWAY_PUBLIC_URL или RENDER_EXTERNAL_URL)")
        return
    await bot.set_webhook(f"{base_url}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)
    logging.info(f"✅ Webhook установлен: {base_url}{WEBHOOK_PATH}")

def main() -> None:
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(balance_router)
    dp.include_router(profile_router)
    dp.include_router(ai_menu_router)
    dp.include_router(gemini_router)
    dp.include_router(nanobanano_router)
    dp.startup.register(on_startup)
    app = web.Application()
    
    # Healthcheck для Railway
    async def healthcheck(request):
        return web.json_response({"status": "ok"})
    app.router.add_get("/health", healthcheck)
    
    # Webhook
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=WEBHOOK_PORT)

if __name__ == "__main__":
    main()