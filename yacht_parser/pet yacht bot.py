import random

from pip._internal import locations
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder

#MOKs data
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

#use our API token from Bot-Father
TELEGRAM_API_TOKEN = '7961888782:AAF2TARBP9dYZkv7IhnXsAvzlCdRNK7DW8s'

#Function to start
async def start(update: Update, context):
    await update.message.reply_text('Hello! Im your chat-bot. Write something to me!')

#func to handle message
async def handle_message(update, context):
    user_message = update.message.text.lower()
    print(f"We've got {user_message}")

    if 'поиск' in user_message or 'найди' in user_message:
        #asking yacht type
        await update.message.reply_text(f'What type of yacht you try to find Motor, Sail, Cata or others: {user_message}')
    elif 'моторная яхта' in user_message or 'парусная яхта' in user_message or 'катамаран' in user_message:
        #ask for budget
        yacht_type = user_message
        context.user_data['yacht_type'] = yacht_type
        await update.message.reply_text(f'What is your budget?')

    elif user_message.isdigit():
        budget = int(user_message)
        yacht_type = context.user_data['yacht_type']

        #taking data
        yachts = fetch_yacht_data(yacht_type, budget)

        #send to user
        for yacht in yachts:
            await update.message.reply_text(f"finded {yacht['type']} for {yacht['price']} is located in {yacht['location']}. More information: {yacht['url']}")

        #new search
        await update.message.reply_text("Do you wanna new search? Write 'new search' to create a new search'.")


#create our bot
def main():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    #Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    #starting bot
    application.run_polling()

if __name__ == '__main__':
    main()


