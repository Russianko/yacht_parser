import requests
import json
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"
url = base_url

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.select('article.product_pod')
books_list = []

for book in books:
    title = book.h3.a['title']
    price = book.select_one('.price_color').text
    relative_link = book.h3.a['href']  # например: "catalogue/a-light-in-the-attic_1000/index.html"
    full_link = base_url + relative_link

    book_info = {
        "title": title,
        "price": price,
        "link": full_link
    }

    books_list.append(book_info)


for i, book in enumerate(books_list, 1):
    print(f"{i}. {book['title']} — {book['price']} — {book['link']}")
print(books_list)
with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(books_list, f, ensure_ascii=False, indent=4)