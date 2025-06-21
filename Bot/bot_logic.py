from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder
from Bot.handlers import start, handle_message


#create our bot
async def run_bot(token):
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    await app.run_polling()


