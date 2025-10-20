import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YUKASSA_API_KEY = os.getenv("YUKASSA_API_KEY")
YUKASSA_SHOP_ID = os.getenv("YUKASSA_SHOP_ID")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))