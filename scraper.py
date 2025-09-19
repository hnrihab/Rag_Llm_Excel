# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_form(form_url, chrome_path):
    """
    Scrape Google Form pour récupérer les questions et options.
    
    Args:
        form_url (str): URL du formulaire Google Form
        chrome_path (str): Chemin vers l'exécutable Chrome
    
    Returns:
        List[Dict]: Liste de dictionnaires {"question": str, "options": List[str]}
    """
    # Configuration Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-accelerated-2d-canvas")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless=new")  # Mode headless


    # Driver
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(driver_version="140.0.7339.82").install()),
    options=chrome_options
)


    driver.get(form_url)
    time.sleep(3)  # Attente pour que le formulaire charge

    questions_data = []
    question_blocks = driver.find_elements(By.CSS_SELECTOR, "div[jscontroller='sWGJ4b']")

    for block in question_blocks:
        try:
            # Texte de la question
            question_text = block.find_element(By.CSS_SELECTOR, "div[role='heading'] span").text

            options = []

            # Radio buttons
            options += [o.get_attribute("aria-label") for o in block.find_elements(By.CSS_SELECTOR, "div[role='radio']")]

            # Checkboxes
            options += [o.get_attribute("aria-label") for o in block.find_elements(By.CSS_SELECTOR, "div[role='checkbox']")]

            # Dropdown / listbox
            options += [o.text for o in block.find_elements(By.CSS_SELECTOR, "div[role='listbox'] span")]

            # Si aucune option détectée, question ouverte
            if not options:
                options.append("Pas d'options détectées (question ouverte ou texte libre)")

            questions_data.append({"question": question_text, "options": options})
        except Exception:
            continue

    driver.quit()
    return questions_data

# Pour tester directement ce module
if __name__ == "__main__":
    CHROME_PATH = r"C:\Users\pc\Downloads\chrome-win64\chrome-win64\chrome.exe"
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf85iLtqXCiI4B_D7MsacbSeoTfX5VrkoMfXWMA7TToYp6gjg/viewform?usp=sharing&ouid=109456949329574446591"
    data = scrape_form(FORM_URL, CHROME_PATH)
    for i, q in enumerate(data):
        print(f"\nQuestion {i+1}: {q['question']}")
        for opt in q['options']:
            print("-", opt)
