from selenium import webdriver  # pip install selenium
import time

browser = webdriver.Chrome()  # Optional argument, if not specified will search path.
browser.get('https://en.wikipedia.org/wiki/Document_Object_Model')
browser.save_screenshot("dom.png")
time.sleep(5)
#print(driver.title)
#driver.quit()
browser.get("https://ru.wikipedia.org/wiki/Selenium")
browser.save_screenshot("selenium.png")
time.sleep(3)
browser.refresh()
time.sleep(3)