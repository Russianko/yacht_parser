import os
from dotenv import load_dotenv
from Bot.bot_logic import run_bot

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if __name__ == '__main__':
    run_bot(TELEGRAM_API_TOKEN)