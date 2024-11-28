import os
from dotenv import load_dotenv

load_dotenv()
TelegramBotApiToken = os.getenv('TELEGRAM_BOT_API_TOKEN')

class Telegram:
    telegram_bot_api_token: str = TelegramBotApiToken
    telegram_api_url: str = "https://api.telegram.org/bot{TelegramBotApiToken}"

telegram = Telegram()