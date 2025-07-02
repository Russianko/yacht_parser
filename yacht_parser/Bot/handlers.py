import os
import sqlite3
import textwrap
import re
from yacht_parser.Parser.parse_yacht import parse_yacht
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from yacht_parser.Parser.get_links_by_producer import get_links_by_producer
from telegram import ReplyKeyboardMarkup


# Бренды яхт
BRANDS = [
    "Bavaria", "Bayliner", "Bénéteau", "Cranchi", "Dufour",
    "Jeanneau", "Lagoon", "Princess Yachts", "Quicksilver", "Sea Ray"
]

BOAT_TYPES = ["Моторная", "Парусная", "Катамаран"]

BOAT_TYPE_CODES = {
    "Парусная": "bt1",
    "Моторная": "bt2",
    "Катамаран": "bc27"
}


PRICE_OPTIONS = [10000, 20000, 30000, 50000, 70000, 90000]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.normpath(os.path.join(BASE_DIR, '..', 'Data', 'yacht.db'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🧹 Очистка старых данных перед новым поиском
cursor.execute("DELETE FROM yachts")
conn.commit()

# Функция для извлечения числового значения из строки цены
def extract_numeric_price(price_str):
    cleaned = price_str.replace('\xa0', ' ').replace('€', '').replace('£', '')
    match = re.search(r'\d[\d\.]*', cleaned)
    if match:
        num_str = match.group(0).replace('.', '')
        return int(num_str)
    raise ValueError(f"Не удалось извлечь цену: {price_str}")

# Обработка неизвестных комманд
async def unknown_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🙈 Я понимаю только команды /start и кнопки выбора.")

# ---------- Start ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Начать поиск", callback_data="start_search")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Привет! Я бот для поиска яхт по бренду, типу и бюджету.\n\nНажмите кнопку ниже, чтобы начать 🔍",
        reply_markup=reply_markup
    )


# Запускаем выбор бренда
async def begin_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    row = []
    for i, brand in enumerate(BRANDS):
        row.append(InlineKeyboardButton(brand, callback_data=f"brand_{brand}"))
        if (i + 1) % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("🛥 Выберите бренд яхты:", reply_markup=reply_markup)



# выбираем бренд
async def brand_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    brand = query.data.replace("brand_", "")
    context.user_data['brand'] = brand
    await query.edit_message_text(f"✅ Вы выбрали бренд: {brand}")

    keyboard = [[InlineKeyboardButton(btype, callback_data=f"type_{btype}")] for btype in BOAT_TYPES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Выберите бренд яхты:", reply_markup=reply_markup)


# выбираем тип лодки
async def type_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    boat_type = query.data.replace("type_", "")
    context.user_data['type'] = boat_type


    keyboard = [[InlineKeyboardButton(f"До {price} €", callback_data=f"price_{price}")] for price in PRICE_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("💰 Выберите максимальный бюджет:", reply_markup=reply_markup)

# фильтруем цену, запускаем парсинг
async def price_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Очистка старых данных перед новым поиском
    cursor.execute("DELETE FROM yachts")
    conn.commit()
    query = update.callback_query
    await query.answer()

    price_limit = int(query.data.replace("price_", ""))
    context.user_data['budget'] = price_limit
    await query.edit_message_text(f"✅ Бюджет: до {price_limit} €")

    brand = context.user_data.get('brand')
    boat_type_name = context.user_data.get('type')
    budget = context.user_data.get('budget')

    await query.message.reply_text(f"🔍 Ищу яхты бренда {brand}, типа {boat_type_name}, до {budget} €...")

    # соответствие типа лодки значению в <select name="btcid">
    BOAT_TYPE_CODES = {
        "Парусная": "bt1",
        "Моторная": "bt2",
        "Катамаран": "bc27"
    }

    boat_type_code = BOAT_TYPE_CODES.get(boat_type_name)

    try:
        links = get_links_by_producer(brand, max_price=budget, boat_type_code=boat_type_code)
    except Exception as e:
        await query.message.reply_text(f"⚠️ Ошибка при получении ссылок: {e}")
        return

    if not links:
        await query.message.reply_text("😞 Яхты не найдены.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yachts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            location TEXT,
            build_year TEXT,
            price TEXT,
            price_number INTEGER,
            description TEXT,
            image_urls TEXT,
            url TEXT UNIQUE
        )
    """)
    conn.commit()

    for link in links:
        try:
            parse_yacht(link, cursor)
        except Exception as e:
            print(f"⚠️ Ошибка при парсинге {link}: {e}")
            continue

    conn.commit()

    cursor.execute("""
        SELECT title, price, price_number, url
        FROM yachts
        WHERE price_number IS NOT NULL AND price_number <= ?
        ORDER BY price_number ASC
    """, (budget,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await query.message.reply_text("😕 По фильтрам ничего не найдено.")
        return

    for row in rows:
        title, price, _, url = row
        await query.message.reply_text(f"🏷 {title}\n💰 {price}\n🔗 {url}")

    keyboard = [
        [InlineKeyboardButton("🚀 Начать новый поиск", callback_data="start_search")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🔁 Хотите начать новый поиск?",
        reply_markup=reply_markup
    )