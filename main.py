from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_driver(headless=True):
    options = Options()
    options.headless = headless  # Устанавливаем значение headless из аргумента функции
    if headless:
        options.add_argument("--headless")  # Добавляем аргумент для headless режима
    options.add_argument("--disable-gpu")  # Отключаем использование GPU
    options.add_argument("--window-size=900,600")  # Устанавливаем размер окна (обязательно для некоторых ОС)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text[:100]}...")  # Выводим первые 100 символов для удобства
    return paragraphs


def list_internal_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a[href^='/wiki/']")
    for i, link in enumerate(links):
        print(f"Ссылка {i + 1}: {link.text} ({link.get_attribute('href')})")
    return links


def main():
    while True:
        user_input = input(
            "Введите 'True' для headless режима или 'False' для отображения окна браузера: ").strip().lower()
        if user_input == 'true':
            headless = True
            break
        elif user_input == 'false':
            headless = False
            break
        else:
            print("Неправильный ввод. Пожалуйста, введите 'True' или 'False'.")

    driver = setup_driver(headless=headless)
    try:
        query = input("Введите запрос: ")
        search_wikipedia(driver, query)

        while True:
            action = input(
                "Выберите действие:\n1. Листать параграфы текущей статьи\n2. Перейти на одну из связанных страниц\n3. Выйти\nВведите номер действия: ")
            if action == '1':
                list_paragraphs(driver)
            elif action == '2':
                links = list_internal_links(driver)
                try:
                    link_choice = int(input("Введите номер ссылки, на которую хотите перейти: ")) - 1
                    if 0 <= link_choice < len(links):
                        driver.get(links[link_choice].get_attribute('href'))
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))
                    else:
                        print("Неправильный номер ссылки. Пожалуйста, попробуйте снова.")
                except ValueError:
                    print("Ошибка ввода. Пожалуйста, попробуйте снова и правильно вводите номер ссылки.")
            elif action == '3':
                break
            else:
                print("Неправильное действие. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
