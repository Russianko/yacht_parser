import os
from pip._internal import locations
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder
from dotenv import load_dotenv
from yacht_parser.Bot.handlers import search_handler
from yacht_parser.Bot.handlers import start, handle_message, search_handler

#create our bot
def main():
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    #Register command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('search', search_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен.")
    # Начало работы бота
    app.run_polling()



#загрузка переменных из .env
load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')



if __name__ == '__main__':
    main()


