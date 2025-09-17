import requests
from bs4 import BeautifulSoup
import pandas as pd

def load_forms_list(file_path):
    """Charge le CSV des formulaires"""
    df = pd.read_csv(file_path, sep=";")
    return [{"name": row["name"], "link": row["link"]} for _, row in df.iterrows()]

def scrape_form(url):
    """Scrape les questions et titre d'un Microsoft Form"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title").get_text(strip=True) if soup.find("title") else "Sans titre"
        questions = [q.get_text(" ", strip=True) for q in soup.find_all("div") if q.get_text(strip=True)]

        return {"title": title, "questions": questions}
    except Exception as e:
        return {"title": "Erreur", "questions": [f"Impossible de scraper {url} : {e}"]}
