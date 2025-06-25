# 🛥️ Yacht Parser

Pet-проект на Python для поиска и анализа яхт по заданным параметрам.  
Собирает данные с сайтов, сохраняет в базу, и может управляться через Telegram-бота.

## 🚀 Возможности

- 🔎 Парсинг яхт с сайта
- 💬 Telegram-бот для общения с пользователем
- 🗂 Сохранение данных в SQLite
- 🧠 Гибкая фильтрация (парусная, моторная, бюджет и т.п.)
- 🧪 Структурированный код для расширения

## 📦 Стек технологий

- Python 3.10+
- `requests`, `beautifulsoup4`
- SQLite
- Telegram Bot API (`python-telegram-bot`)
- `pickle` для cookies

## ⚙️ Как запустить

```bash
git clone https://github.com/Russianko/yacht_parser.git
cd yacht_parser
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
python "pet yacht bot.py"



📂 Структура проекта

yacht_parser/
├── Books parser.py         # учебный парсер с books.toscrape.com
├── pet yacht bot.py        # Telegram-бот
├── Trainies.py             # тренировочный код
├── sub trainees.py         # вспомогательные сценарии
├── yacht.db                # база данных яхт
├── cookies.pkl             # cookies для авторизации
└── .gitignore              # исключения

🧠 Планы

Подключение реального сайта о яхтах

Добавить логирование

Обработка изображений яхт

Настройка фильтров и параметров запроса

Отправка подборок яхт в Telegram

🤝 Автор

Github: Russianko

🧭 Проект в разработке. Буду рад комментариям и фидбеку!# yacht_parser