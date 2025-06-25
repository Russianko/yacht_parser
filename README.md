# Yacht Parser & Telegram Bot

Проект для поиска и анализа яхт с сайта [yachtall.com](https://www.yachtall.com/) с последующей выдачей результатов через Telegram-бота.

## 🧭 Возможности

- Парсинг сайта yachtall.com по заданному производителю и сбор:
  - Названия
    - Года постройки
  - Локации
  - Цены
  - Описания
  - Фотографий
- Сохранение данных в SQLite-базу
- Telegram-бот с функцией поиска по базе

## 📁 Структура проекта
<pre lang="nohighlight"><code>```

yacht_parser/
├── Bot/
│   ├── bot_logic.py             # Логика Telegram-бота
│   ├── handlers.py              # Хендлеры команд и сообщений
│   └── pet yacht bot.py         # Точка входа для запуска бота
│
├── Parser/
│   ├── get_links_by_producer.py # Получение ссылок на яхты по бренду
│   ├── parse_yacht.py           # Парсинг данных яхты
│   ├── main.py                  # Основной скрипт запуска парсера
│   ├── mock_data.py             # Заглушки (при необходимости)
│   └── yacht.db                 # Локальная база данных SQLite
│
├── .env.example                 # Пример переменных окружения (TOKEN и т.д.)
└── main.py                      # Альтернативная точка входа

``` </code></pre>
## 🚀 Как запустить

1. Установите зависимости:


pip install -r requirements.txt

    Скопируйте .env.example и переименуйте в .env, добавив свой Telegram API токен:

TELEGRAM_API_TOKEN=your_token_here

    Запуск парсера:

python yacht_parser/Parser/main.py

    Запуск бота:

python yacht_parser/Bot/pet\ yacht\ bot.py

🛠️ Используемые технологии

    Python 3.10+

    Selenium + BeautifulSoup

    SQLite

    python-telegram-bot

    dotenv

📌 Примечания

    Для работы Selenium требуется ChromeDriver, совместимый с вашей версией Chrome.

    База данных yacht.db создается автоматически, если отсутствует.