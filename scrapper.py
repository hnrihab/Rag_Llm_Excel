import requests
from bs4 import BeautifulSoup

def scrape_form(form_link: str):
    """
    Tente de scraper un Microsoft Form à partir de son lien.
    Retourne un dictionnaire avec titre, questions, etc.
    """
    try:
        response = requests.get(form_link)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Impossible d'accéder à {form_link} : {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extraction du titre
    title = soup.find("div", {"class": "geS5n"}).get_text(strip=True) if soup.find("div", {"class": "geS5n"}) else "Titre non trouvé"

    # Extraction des questions (exemple avec div role="listitem")
    questions = []
    for q in soup.find_all("div", {"role": "listitem"}):
        questions.append(q.get_text(" ", strip=True))

    return {
        "title": title,
        "questions": questions,
        "link": form_link
    }
