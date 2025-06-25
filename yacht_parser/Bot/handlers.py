from telegram import Update
from telegram.ext import ContextTypes
from Parser.mock_data import fetch_yacht_data

# Команда /Start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я бот для поиска яхт.\nНапиши 'поиск' или 'найди', чтобы начать.")

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    print(f"[LOG] Пользователь: {user_message}")

    if 'поиск' in user_message or 'найди' in user_message:
        #asking yacht type
        await update.message.reply_text(f'(моторная яхта, парусная яхта, катамаран...): {user_message}')
    elif any(x in user_message for x in ['моторная яхта', 'парусная яхта', 'катамаран']):
        context.user_data['yacht_type'] = user_message
        await update.message.reply_text('Укажите ваш бюджет в цифрах:')

    elif user_message.isdigit():
        budget = int(user_message)
        yacht_type = context.user_data.get('yacht_type', 'люксовая яхта')

        #taking data
        yachts = fetch_yacht_data(yacht_type, budget)

        #send to user
        for yacht in yachts:
            await update.message.reply_text(f"Нашел {yacht['type']} за {yacht['price']} \nв регионе {yacht['location']}. Больше информации: {yacht['url']}")

        #new search
        await update.message.reply_text("🔄 Хотите начать новый поиск? Напишите 'поиск' или 'найди'.")

    else:
        await update.message.reply_text("🤖 Я вас не понял. Напишите 'поиск' или 'найди', чтобы начать.")
