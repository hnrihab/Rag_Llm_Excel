from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Configuration du navigateur ---
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r"C:\Users\pc\Downloads\chrome-win64\chrome-win64\chrome.exe"
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless=new")  # Headless pour ne pas ouvrir la fenêtre

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager(driver_version="140.0.7339.82").install()),
    options=chrome_options
)

# --- URL du formulaire ---
form_url = "https://docs.google.com/forms/d/e/1FAIpQLScdO8838uuPAJ2H7ayDbKFDpUjb-vkfmB461XOPKsds0oU2Jg/viewform"
driver.get(form_url)
time.sleep(3)  # Attente pour que le formulaire charge

questions_data = []

# --- Récupération de toutes les questions ---
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

        # Si aucune option détectée, considérer comme question texte libre
        if not options:
            options.append("Pas d'options détectées (question ouverte ou texte libre)")

        questions_data.append({"question": question_text, "options": options})

    except Exception as e:
        # Ignorer les blocs qui ne sont pas des questions
        continue

# --- Affichage complet ---
for i, q in enumerate(questions_data):
    print(f"\nQuestion {i+1}: {q['question']}")
    for opt in q['options']:
        print("-", opt)

driver.quit()
