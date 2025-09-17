from utils import load_forms_list
from scrapper import scrape_form

def main():
    forms = load_forms_list("forms_list_example.csv")
    results = []

    for f in forms:
        print(f"🔎 Scraping : {f['form_name']} ({f['form_link']})")
        data = scrape_form(f["form_link"])
        results.append(data)

    # Affichage des résultats
    for r in results:
        print("\n=== Résultat ===")
        print(f"Titre : {r.get('title')}")
        print(f"Questions : {r.get('questions')}")
        print(f"Lien : {r.get('link')}\n")

if __name__ == "__main__":
    main()
