from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_links_by_producer(producer_name: str) -> list:
    url = "https://www.yachtall.com/ru/lodki"
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        toggle = wait.until(EC.element_to_be_clickable((By.ID, 'manfbbox_tglhead')))
        toggle.click()
        print("✅ Раскрыт блок производителей")
    except:
        print("❌ Не удалось раскрыть блок производителей")
        driver.quit()
        return []

    try:
        # Обновлённый XPath: ищет <label>, внутри которого есть <a> с нужным текстом
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

    # Ждём загрузку результатов
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

# Тест вручную (можно удалить, если не нужно)
if __name__ == "__main__":
    name = input("Введите производителя (например, Beneteau): ")
    result_links = get_links_by_producer(name)
    for link in result_links:
        print(link)