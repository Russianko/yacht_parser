def parse_yacht(url, cursor):
    import requests
    from bs4 import BeautifulSoup
    import json
    import re

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Нет названия"

        def extract_price_number(text):
            match = re.search(r"(\d{1,3}(?:[\.,]\d{3})*|\d+)", text.replace('\xa0', '').replace(' ', ''))
            if match:
                return int(match.group(1).replace('.', '').replace(',', ''))
            return None

        def get_text(label_name):
            for tr in soup.find_all("div", class_="tr"):
                label = tr.find("div", class_="td")
                if label and label_name in label.text:
                    tds = tr.find_all("div", class_="td")
                    return tds[1].get_text(strip=True) if len(tds) >= 2 else "Не указано"
            return "Не указано"

        location = get_text("Место стоянки")
        build_year = get_text("Год постройки")
        price = get_text("Цена")
        numeric_price = extract_price_number(price)

        if numeric_price is None:
            log_message = f"[⚠️] Не удалось извлечь цену: '{price}' | {title} | {url}"
            print(log_message)
            with open("errors.log", "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
            return  # можно заменить на `numeric_price = -1` если хочешь сохранять

        desc_block = soup.find("div", id="dataDesc_box")
        description = desc_block.get_text(separator="\n", strip=True) if desc_block else "Нет описания"

        image_urls = set()
        main_img = soup.find("img", {"alt": lambda x: x and "фото" in x})
        if main_img:
            image_urls.add(main_img.get("src"))

        for img in soup.select("div.thumbglry-box img"):
            for attr in ["src", "data-src"]:
                src = img.get(attr)
                if src and src.endswith(".jpg"):
                    image_urls.add(src)

        images_str = json.dumps(list(image_urls), ensure_ascii=False)

        cursor.execute("""
            INSERT OR IGNORE INTO yachts(title, location, build_year, price, price_number, description, image_urls, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, location, build_year, price, numeric_price, description, images_str, url)
        )

        print(f"✅ Добавлена: {title}")
    except Exception as e:
        log_message = f"[❌] Ошибка парсинга {url}: {e}"
        print(log_message)
        with open("errors.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")