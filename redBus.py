from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


start_city = input("Ingrese la ciudad de origen: ")
final_city = input("Ingrese la ciudad de destino: ")

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

driver.get("https://www.redbus.co/")
wait = WebDriverWait(driver, 20)

time.sleep(2)

start_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="src"]')))
start_field.click()
start_field.clear()

for index, letter in enumerate(start_city):
    start_field.send_keys(letter)
    time.sleep(0.3)

time.sleep(2)

start_field.send_keys(Keys.ARROW_DOWN)
time.sleep(0.2)
start_field.send_keys(Keys.ARROW_UP)
time.sleep(0.2)
start_field.send_keys(Keys.ENTER)

time.sleep(2)

final_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dest"]')))
final_field.click()
final_field.clear()

for index, letter in enumerate(final_city):
    final_field.send_keys(letter)
    time.sleep(0.3)

time.sleep(2)

final_field.send_keys(Keys.ARROW_DOWN)
time.sleep(0.2)
final_field.send_keys(Keys.ARROW_UP)
time.sleep(0.2)
final_field.send_keys(Keys.ENTER)

time.sleep(2)

driver.quit()
