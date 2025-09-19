import pandas as pd
import json
import os
import ollama
from scraper import scrape_form

# --- CONFIG ---
CHROME_PATH = r"C:\Users\pc\Downloads\chrome-win64\chrome-win64\chrome.exe"

# Charger les liens du fichier Excel
df = pd.read_csv("forms_list_example.csv", sep=";")

results = []

for idx, row in df.iterrows():
    quiz_name = row["name"]
    quiz_url = row["link"]
    print(f"\n🔹 Traitement de {quiz_name} : {quiz_url}")
    
    # Étape 1 : Scraping
    print("   Étape 1/2 : Scraping du formulaire...")
    questions = scrape_form(quiz_url, CHROME_PATH)
    print(f"   ✅ {len(questions)} questions détectées")

    
# Créer un dossier pour stocker les JSON si besoin
os.makedirs("results", exist_ok=True)

quiz_results = {
    "quiz_name": quiz_name,
    "questions": []
}

for i, q in enumerate(questions, 1):
    print(f"      Étape 2/2 : Analyse de la question {i}/{len(questions)}")

    prompt = f"""
    Voici une question extraite d’un quiz Microsoft Forms :
    Question: {q['question']}
    Options: {q['options'] if q['options'] else 'Aucune option'}
    ➡️ Analyse cette question, propose une réponse correcte si possible et reformule-la clairement.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response["message"]["content"]

    quiz_results["questions"].append({
        "question": q["question"],
        "options": q["options"],
        "llm_response": reply
    })

# Sauvegarde JSON pour ce quiz
with open(f"results/{quiz_name}.json", "w", encoding="utf-8") as f:
    json.dump(quiz_results, f, indent=4, ensure_ascii=False)

print(f"✅ Résultats JSON sauvegardés : results/{quiz_name}.json")