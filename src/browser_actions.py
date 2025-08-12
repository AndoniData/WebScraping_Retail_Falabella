from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import time


def start_browser(url):
    """Function to create a Selenium Wire browser session."""
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, seleniumwire_options={'disable_encoding': True})
    driver.get(url)
    return driver

def next_page_click(driver, button_id):
    """Function to click the next page button."""
    try:
        next_button = driver.find_element("id", button_id)
        next_button.click()
        return True
    except Exception as e:
        print(f"Could not click next page button: {e}")
        return False

def wait_for_requests(driver, wait_time=5):
    """Function to wait for a specified time to allow requests to complete."""
    time.sleep(wait_time)

def close_browser(driver):
    """Function to close the browser session."""
    driver.close()