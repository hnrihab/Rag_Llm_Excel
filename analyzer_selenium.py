from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_form(url, chrome_binary_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_binary_path
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.get(url)
    time.sleep(3)  # laisser le temps de charger

    questions_data = []
    question_blocks = driver.find_elements(By.CSS_SELECTOR, "div[jscontroller='sWGJ4b']")

    for block in question_blocks:
        try:
            question_text = block.find_element(By.CSS_SELECTOR, "div[role='heading'] span").text
            options = []

            # Radio
            options += [o.get_attribute("aria-label") for o in block.find_elements(By.CSS_SELECTOR, "div[role='radio']")]

            # Checkboxes
            options += [o.get_attribute("aria-label") for o in block.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")]

            # Dropdown
            options += [o.text for o in block.find_elements(By.CSS_SELECTOR, "div[role='listbox'] span")]

            if not options:
                options.append("Pas d'options détectées (question ouverte ou texte libre)")

            questions_data.append({"question": question_text, "options": options})

        except:
            continue

    driver.quit()
    return questions_data
