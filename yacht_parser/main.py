import os
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from yacht_parser.Bot.handlers import (
    start,
    brand_callback_handler,
    unknown_message_handler,
    type_callback_handler,
    price_callback_handler,
    begin_search
)




# Загрузка переменных окружения
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


def main():
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(brand_callback_handler, pattern=r"^brand_"))
    app.add_handler(CallbackQueryHandler(type_callback_handler, pattern=r"^type_"))
    app.add_handler(CallbackQueryHandler(price_callback_handler, pattern=r"^price_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message_handler))
    app.add_handler(CallbackQueryHandler(begin_search, pattern=r"^begin_search$"))
    app.add_handler(CallbackQueryHandler(begin_search, pattern="^start_search$"))


    print("✅ Бот запущен.")
    app.run_polling()


if __name__ == '__main__':
    main()