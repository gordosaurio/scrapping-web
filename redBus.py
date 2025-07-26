from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


origin_city = input("Ingrese la ciudad de origen: ")

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

driver.get("https://www.redbus.co/")
wait = WebDriverWait(driver, 20)

time.sleep(2)

origin_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="src"]')))
origin_field.click()
origin_field.clear()

for index, letter in enumerate(origin_city):
    origin_field.send_keys(letter)
    time.sleep(0.3)

time.sleep(2)

origin_field.send_keys(Keys.ARROW_DOWN)
time.sleep(0.2)
origin_field.send_keys(Keys.ARROW_UP)
time.sleep(0.2)
origin_field.send_keys(Keys.ENTER)

time.sleep(5)

driver.quit()
