import asyncio
import os
from dotenv import load_dotenv
from Bot.bot_logic import import run_bot


#Загрузка переменных окружения
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def main():
    #запускаем бота
    await run_bot(TELEGRAM_API_TOKEN)

    #await run_parser() будет запускать парсер по готовности

if __name__ == '__main__':
    asyncio.run(main())

