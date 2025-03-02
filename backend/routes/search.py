from flask import Blueprint, request, jsonify
# from services.search import search_aliexpress_by_image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

search_bp = Blueprint("search", __name__)

@search_bp.route("/", methods=["POST"])
def search():
    data = request.get_json()
    image_path = data.get("image_path")

    if not image_path:
        return jsonify({"error": "Image path required"}), 400

    results = search_aliexpress_by_image(image_path)
    return jsonify({"search_results": results})


def check_on_aliexpress():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in the background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    current_dir = os.getcwd()
    print("Current working directory:", current_dir)
    img = f'{current_dir}\\test.png'
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.aliexpress.com/")
        time.sleep(3)
        try:
            dont_allow = driver.find_element(By.XPATH, "//*[contains(text(), 'אל תאפשרו')]")
            dont_allow.click()
            print("Clicked the 'Don't Allow' popup!")
        except Exception as e:
            print("Could not find or click 'אל תאפשרו':", e)
        search_word = driver.find_element(By.CSS_SELECTOR, '[id="search-words"]')
        search_aera = search_word.find_element(By.XPATH, "..")
        time.sleep(3)
        search_by_picture_image = search_aera.find_elements(By.TAG_NAME, 'img')
        for search_img in search_by_picture_image:
            print(search_img, 'foung')
            search_img.click()
            upload_text = driver.find_element(By.XPATH,"//*[contains(text(), 'חיפוש באמצעות תמונה')]")
            print(upload_text, "find img")
            area = upload_text.find_element(By.XPATH, "..")
            file_input = area.find_element(By.CSS_SELECTOR, "input[type='file']")
            is_hidden = file_input.value_of_css_property("display") == "none"
            print(f"Is input hidden? {is_hidden}")
            if is_hidden:
                driver.execute_script("arguments[0].style.display = 'block';", file_input)
                print("Input field is now visible!")

            print("Uploading image...")
            print(img)
            file_input.send_keys(img)
            time.sleep(2)
            match_items = []
            card_list = driver.find_element(By.ID, 'card-list')
            if(card_list):
                items = card_list.find_elements(By.TAG_NAME, 'a')
                print(len(items))
                for item in items:
                    href = item.get_attribute('href')
                    img = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    print(href, img)
                    match_items.append({
                        href:href,
                        img: img
                    })
            return match_items

 

    finally:
        input("press enter to exit...")
        # driver.quit()

def check_on_google():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in the background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    current_dir = os.getcwd()
    print("Current working directory:", current_dir)
    img = f'{current_dir}\\test.png'
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://lens.google.com")
        time.sleep(3)
        items = []
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(img)
        time.sleep(3)
        product = driver.find_element(By.XPATH,"//*[contains(text(), 'מוצרים)]")
        product.click()
        time.sleep(2)
        cards = driver.find_elements(By.ID, 'search')
        imgs = cards.find_elements(By.TAG_NAME, 'img')
        a_tags = cards.find_elements(By.TAG_NAME, 'a')
        for i in range(len(imgs)):
            current_img = imgs[i].get_attribute('src')
            current_a = a_tags[i].get_attribute('href')
            items.append({
                img: current_img,
                href: current_a
            })
        return items

        
        
    finally:
        input("press enter to exit...")
        # driver.quit()

def check_match_results():
    pass

def main():
    retults = check_on_google()
    print(retults)