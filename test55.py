from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    options = Options()
    options.headless = False  # Ставьте True, если не хотите видеть окно браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_wikipedia(driver, query):
    driver.get("https://www.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i+1}: {paragraph.text[:100]}...")  # Выводим первые 100 символов для удобства
    return paragraphs

def list_internal_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a[href^='/wiki/']")
    for i, link in enumerate(links):
        print(f"Ссылка {i+1}: {link.text} ({link.get_attribute('href')})")
    return links

def main():
    driver = setup_driver()
    try:
        query = input("Введите запрос: ")
        search_wikipedia(driver, query)

        while True:
            action = input("Выберите действие:\n1. Листать параграфы текущей статьи\n2. Перейти на одну из связанных страниц\n3. Выйти\nВведите номер действия: ")
            if action == '1':
                paragraphs = list_paragraphs(driver)
            elif action == '2':
                links = list_internal_links(driver)
                link_choice = input("Введите номер ссылки, на которую хотите перейти (или 'exit' для выхода): ")
                if link_choice.lower() == 'exit':
                    break
                link_choice = int(link_choice) - 1
                if 0 <= link_choice < len(links):
                    driver.get(links[link_choice].get_attribute('href'))
                    time.sleep(2)
                    while True:
                        sub_action = input("Выберите действие:\n1. Листать параграфы статьи\n2. Перейти на одну из внутренних статей\n3. Выйти\nВведите номер действия: ")
                        if sub_action == '1':
                            paragraphs = list_paragraphs(driver)
                        elif sub_action == '2':
                            sub_links = list_internal_links(driver)
                            sub_link_choice = input("Введите номер ссылки, на которую хотите перейти (или 'exit' для выхода): ")
                            if sub_link_choice.lower() == 'exit':
                                break
                            sub_link_choice = int(sub_link_choice) - 1
                            if 0 <= sub_link_choice < len(sub_links):
                                driver.get(sub_links[sub_link_choice].get_attribute('href'))
                                time.sleep(2)
                                list_paragraphs(driver)
                            else:
                                print("Неправильный номер ссылки.")
                        elif sub_action == '3':
                            break
                        else:
                            print("Неправильное действие. Попробуйте снова.")
                else:
                    print("Неправильный номер ссылки.")
            elif action == '3':
                break
            else:
                print("Неправильное действие. Попробуйте снова.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
