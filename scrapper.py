import requests
from bs4 import BeautifulSoup

def scrape_form(form_link: str):
    """
    Scrape un Microsoft Form et retourne la liste des questions trouvées
    """
    try:
        response = requests.get(form_link)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement du formulaire : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Microsoft Forms stocke les questions dans des balises <div> avec class spécifique
    questions = []

    # Exemple basé sur ton snippet "Envoyer / Effacer le formulaire"
    for q_div in soup.find_all("div", class_="M7eMe"):  # parfois 'Qr7Oae', 'W85ice'
        q_text = q_div.get_text(strip=True)
        if q_text:
            questions.append(q_text)

    # Sécurité : si rien trouvé, on renvoie une valeur factice
    if not questions:
        print("⚠️ Aucune question trouvée, retour factice pour test")
        questions = ["Question exemple : La virtualisation permet d’exécuter plusieurs systèmes d’exploitation ?"]

    return questions
