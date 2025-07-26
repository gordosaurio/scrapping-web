from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import locale


def ask_valid_date():
    today = datetime.now().date()
    while True:
        date_str = input("Enter departure date (DD-MM-YYYY): ")
        try:
            date_dt = datetime.strptime(date_str, "%d-%m-%Y").date()
            if date_dt < today:
                print("You can only select dates from today onwards.")
            else:
                return date_dt, date_str
        except ValueError:
            print("Invalid date format. Use DD-MM-YYYY.")


def configure_mobile_driver():
    mobile_emulation = {"deviceName": "iPhone X"}
    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def type_with_delay(element, text, delay=0.15):
    for letter in text:
        element.send_keys(letter)
        time.sleep(delay)


def select_city(driver, wait, city, city_container_xpath, input_xpath, suggestion_xpath_prefix):
    container = wait.until(EC.element_to_be_clickable((By.XPATH, city_container_xpath)))
    container.click()
    time.sleep(0.4)

    search_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    search_input.click()
    search_input.clear()
    type_with_delay(search_input, city, delay=0.1)

    first_option = wait.until(EC.element_to_be_clickable((By.XPATH, suggestion_xpath_prefix)))
    first_option.click()
    time.sleep(0.8)


def navigate_and_select_date(driver, wait, date_dt, date_str):
    months_map = {
        "ene": "01",
        "feb": "02",
        "mar": "03",
        "abr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dic": "12"
    }

    target_month_num = date_dt.strftime("%m")
    target_year = date_dt.strftime("%Y")
    target_day = str(int(date_dt.strftime("%d")))

    calendar_open_xpath = '//*[@id="root"]/div/div[3]/div[5]/div[2]/div[1]/div'
    calendar_open = wait.until(EC.element_to_be_clickable((By.XPATH, calendar_open_xpath)))
    driver.execute_script("arguments[0].click();", calendar_open)
    time.sleep(1)

    while True:
        header_xpath = '//*[@id="root"]/div/div[4]/div/div/div[1]/div[2]'
        header = wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
        header_text = header.text.strip().lower()

        parts = header_text.split()
        if len(parts) >= 2:
            abbrev_month = parts[0]
            current_year = parts[1]
        else:
            print(f"[WARN] Unable to parse calendar header: '{header_text}'")
            abbrev_month = ""
            current_year = ""

        current_month_num = months_map.get(abbrev_month, None)

        print(f"[DEBUG] Calendar header: month = '{abbrev_month}' ({current_month_num}), year = '{current_year}'")

        if current_month_num == target_month_num and current_year == target_year:
            print("[DEBUG] Month and year match, exiting month navigation loop.")
            break

        try:
            next_button_xpath = '//*[@id="root"]/div/div[4]/div/div/div[1]/div[3]'
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            print("[DEBUG] Next month button found, clicking to advance month.")
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            print(f"[ERROR] Could not find or click next month button: {e}")
            print("[INFO] Exiting month navigation loop.")
            break
        
        time.sleep(1.5)

    day_xpath = f"//span[normalize-space(text())='{target_day}' and not(contains(@class,'DayTiles__CalendarDaysSpanDisabled'))]"
    try:
        day_element = wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
        driver.execute_script("arguments[0].click();", day_element)
        print(f"[INFO] Selected day {target_day} of month {abbrev_month} year {target_year}.")
    except Exception as e:
        print(f"[ERROR] Could not select day {target_day}: {e}")

    print("[INFO] Pausing for 5 seconds to visually verify selected date in the calendar...")
    time.sleep(2)


def click_search_button(driver, wait):
    search_button_xpath = '//*[@id="root"]/div/div[3]/button'
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
    search_button.click()
    print("[INFO] Search button clicked, search initiated.")


def main():
    origin_city = input("Enter origin city: ")
    destination_city = input("Enter destination city: ")
    departure_date, departure_date_str = ask_valid_date()

    driver = configure_mobile_driver()
    wait = WebDriverWait(driver, 20)

    driver.get("https://m.redbus.co/")
    time.sleep(2)

    select_city(
        driver, wait, origin_city,
        city_container_xpath='//*[@id="sourceCity"]/div/div',
        input_xpath='//*[@id="suggestInput"]',
        suggestion_xpath_prefix='//*[@id="sourceCity"]/div/div[3]/ul/li[1]/div/div/span[2]'
    )

    select_city(
        driver, wait, destination_city,
        city_container_xpath='//*[@id="destinationCity"]/div/div',
        input_xpath='//*[@id="suggestInput"]',
        suggestion_xpath_prefix='//*[@id="destinationCity"]/div/div[3]/ul/li[1]/div/div/span[2]'
    )

    navigate_and_select_date(driver, wait, departure_date, departure_date_str)

    time.sleep(1)

    click_search_button(driver, wait)

    time.sleep(3)

    driver.quit()


if __name__ == "__main__":
    main()
