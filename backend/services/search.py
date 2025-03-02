from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_aliexpress_by_image(image_path):
    """Automates AliExpress search-by-image using Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.aliexpress.com/image-search/")
        time.sleep(2)

        upload_button = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        upload_button.send_keys(image_path)
        time.sleep(5)

        products = driver.find_elements(By.CSS_SELECTOR, ".item-title")
        search_results = [product.text for product in products[:5]]

        return search_results

    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()