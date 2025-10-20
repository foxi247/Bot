# check_webhook.py
import asyncio
from aiogram import Bot
from data.config import TELEGRAM_BOT_TOKEN

async def check():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    info = await bot.get_webhook_info()
    print("URL:", info.url)
    print("Pending updates:", info.pending_update_count)
    print("Last error:", info.last_error_message)
    await bot.session.close()

asyncio.run(check())