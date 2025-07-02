import sqlite3
import time
from yacht_parser.Parser.get_links_by_producer import get_links_by_producer
from parse_yacht import parse_yacht

conn = sqlite3.connect("../Data/yacht.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS yachts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    location TEXT,
    build_year TEXT,
    price TEXT,
    description TEXT,
    image_urls TEXT,
    url TEXT
)
""")
conn.commit()

producer = input("Введите имя производителя: ").strip()
links = get_links_by_producer(producer)
print(f"\nНайдено ссылок: {len(links)}")

for link in links:
    parse_yacht(link, cursor)
    time.sleep(1)

conn.commit()
conn.close()