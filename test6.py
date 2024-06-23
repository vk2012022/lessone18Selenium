from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    time.sleep(2)  # Лучше использовать явное ожидание

# Пример использования функций setup_driver и search_wikipedia
driver = setup_driver()
search_wikipedia(driver, "Python programming language")

# Ваш код для обработки результатов поиска

driver.quit()
