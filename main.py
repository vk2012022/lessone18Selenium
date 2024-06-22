from selenium import webdriver  # pip install selenium
import time

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.google.com/')
print(driver.title)
driver.quit()