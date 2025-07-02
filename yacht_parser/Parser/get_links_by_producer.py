from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def get_links_by_producer(
    producer_name: str,
    max_price: int = None,
    year_from: int = None,
    year_to: int = None,
    boat_type_code: str = None  # 👈 новый параметр
) -> list:
    url = "https://www.yachtall.com/ru/lodki"

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    try:
        toggle = wait.until(EC.element_to_be_clickable((By.ID, 'manfbbox_tglhead')))
        toggle.click()
        print("✅ Раскрыт блок производителей")
    except:
        print("❌ Не удалось раскрыть блок производителей")
        driver.quit()
        return []

    try:
        checkbox_label = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//label[a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÉ', 'abcdefghijklmnopqrstuvwxyzé'), '{producer_name.lower()}')]]"
        )))
        checkbox_label.click()
        print(f"✅ Выбран производитель: {producer_name}")
    except Exception as e:
        print(f"❌ Ошибка при поиске производителя: {e}")
        driver.quit()
        return []

    time.sleep(1)

    # 💰 Выбор максимальной цены
    if max_price:
        try:
            price_select = Select(wait.until(EC.presence_of_element_located((By.ID, "sprct"))))
            available_prices = [option.get_attribute("value") for option in price_select.options if
                                option.get_attribute("value")]

            # Найдём ближайшую подходящую цену (<= max_price)
            suitable_price = max(
                (int(p) for p in available_prices if int(p) <= max_price),
                default=None
            )

            if suitable_price:
                price_select.select_by_value(str(suitable_price))
                time.sleep(1.5)
                print(f"💰 Установлена фильтрация по цене: до {suitable_price}")
            else:
                print(f"⚠️ Нет подходящей цены в списке для значения: {max_price}")
        except Exception as e:
            print(f"⚠️ Не удалось выбрать цену: {e}")


    # 🛥️ Выбор типа лодки (btcid)
    if boat_type_code:
        try:
            type_select = Select(wait.until(EC.presence_of_element_located((By.ID, "btcid"))))
            type_select.select_by_value(boat_type_code)
            print(f"🛥 Установлен тип лодки: {boat_type_code}")
        except Exception as e:
            print(f"⚠️ Не удалось выбрать тип лодки: {e}")


    # 📅 Годы постройки
    if year_from:
        try:
            ybf_select = Select(driver.find_element(By.ID, "ybf"))
            ybf_select.select_by_value(str(year_from))
            print(f"📅 Год от: {year_from}")
        except Exception as e:
            print(f"⚠️ Не удалось выбрать 'год от': {e}")

    if year_to:
        try:
            ybt_select = Select(driver.find_element(By.ID, "ybt"))
            ybt_select.select_by_value(str(year_to))
            print(f"📅 Год до: {year_to}")
        except Exception as e:
            print(f"⚠️ Не удалось выбрать 'год до': {e}")

    # Ждём обновления страницы
    time.sleep(5)

    links = set()
    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.boatlist-main-box div.boatlist-subbox a.js-hrefBoat")))
        offers = driver.find_elements(By.CSS_SELECTOR, "div.boatlist-main-box div.boatlist-subbox a.js-hrefBoat")
        for offer in offers:
            href = offer.get_attribute("href")
            if href and "/ru/lodka/" in href:
                links.add("https://www.yachtall.com" + href if href.startswith("/ru") else href)
    except Exception as e:
        print(f"❌ Ошибка при сборе ссылок: {e}")

    driver.quit()
    print(f"\n🔗 Найдено ссылок: {len(links)}")
    return list(links)