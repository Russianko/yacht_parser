import random
import os
from pip._internal import locations
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder
from dotenv import load_dotenv


#загрузка переменных из .env
load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# функция генерации мок-данных
def fetch_yacht_data(yacht_type, budget):
    yacht_types = ['Моторная яхта', 'Парусная яхта', 'Катамаран', 'Рыболовное судно', 'Люксовая яхта']
    locations = ['Средиземное море', 'Карибы', 'Тихий океан']

    yacht_data = []
    for _ in range(5):
        price = random.randint(1, budget)
        yacht = {'type': random.choice(yacht_types),
                 'price': price,
                 'location': random.choice(locations),
                 'url':'https://example.com/yacht'
                 }
        yacht_data.append(yacht)
    return yacht_data


# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("👋 Привет! Я бот для поиска яхт.\nНапиши 'поиск' или 'найди', чтобы начать.")

# Обработка обычных сообщений
async def handle_message(update, context):
    user_message = update.message.text.lower()
    print(f"[LOG] Пользователь написал {user_message}")

    if 'поиск' in user_message or 'найди' in user_message:
        #asking yacht type
        await update.message.reply_text(f'(моторная яхта, парусная яхта, катамаран...): {user_message}')
    elif 'моторная яхта' in user_message or 'парусная яхта' in user_message or 'катамаран' in user_message:
        #ask for budget
        yacht_type = user_message
        context.user_data['yacht_type'] = yacht_type
        await update.message.reply_text(f"💰 Какой у вас бюджет?")

    elif user_message.isdigit():
        budget = int(user_message)
        yacht_type = context.user_data['yacht_type']

        #taking data
        yachts = fetch_yacht_data(yacht_type, budget)

        #send to user
        for yacht in yachts:
            await update.message.reply_text(f"finded {yacht['type']} for {yacht['price']} is located in {yacht['location']}. More information: {yacht['url']}")

        #new search
        await update.message.reply_text("🔄 Хотите начать новый поиск? Напишите 'поиск' или 'найди'.")

    else:
        await update.message.reply_text("🤖 Я вас не понял. Напишите 'поиск' или 'найди', чтобы начать.")

#create our bot
def main():
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    #Register command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен.")
    # Начало работы бота
    app.run_polling()

if __name__ == '__main__':
    main()


