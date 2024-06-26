import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def find_chrome_profile_path():
    # Default Chrome profile path on Windows
    default_chrome_path = os.path.join(os.getenv('LOCALAPPDATA'),  'Chrome', 'User Data')

    # Check if the default path exists
    if os.path.exists(default_chrome_path):
        return default_chrome_path

    # Search for Chrome profile path within common directories
    search_paths = [
        os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local',  'Chrome', 'User Data'),
        os.path.join(os.getenv('APPDATA'),  'Chrome', 'User Data')
    ]

    for path in search_paths:
        if os.path.exists(path):
            return path

    return None
def login():
    # Enter the name of the group you want to mention
    group_name = input("enter group name :")

    # Enter the message you want to send
    msg_ = input("enter message :")

    chrome_profile_path = find_chrome_profile_path()
    if chrome_profile_path is None:
        print("Chrome profile path not found.")
        return

    try:
        # Create ChromeOptions and set the user-data-dir to the Chrome profile path
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={chrome_profile_path}")

        # Create a driver object with the specified options
        driver = webdriver.Chrome(options=options)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com/")

        # Wait for the QR code to be scanned
        wait = WebDriverWait(driver, 450)
        time.sleep(10)
        try:
            group_title = wait.until(ec.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]')))
            group_title.click()
        except TimeoutException:
            print(f"Group '{group_name}' not found. Please check the group name or make sure the group exists.")
            return

        # XPath for the input box
        input_box_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        input_box = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, input_box_xpath)))
        time.sleep(5)

        # Extract HTML content from a specific element using XPath
        element = driver.find_element(By.XPATH, "//*[@id='main']/header/div[2]/div[2]/span")
        element_html = element.get_attribute("outerHTML")

        contacts = element_html.split('"')[1].split(', ')
        time.sleep(5)
        for contact in contacts[:len(contacts) - 1]:
            input_box.send_keys('@')
            input_box.send_keys(contact)
            input_box.send_keys(Keys.ENTER)

        input_box.send_keys(msg_)

        time.sleep(2)
        input_box.send_keys(Keys.ENTER)

        time.sleep(100)
    finally:
        # Close the driver
        if 'driver' in locals():
            driver.quit()
login()

