from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder
from Bot.handlers import start, handle_message


def run_bot(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()  # ⚠️ Без await

