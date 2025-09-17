import pandas as pd

def load_forms_list(file_path: str):
    df = pd.read_csv(file_path, sep=";")  # 👈 ajoute sep=";" pour lire les ;
    
    # Renommer les colonnes pour uniformiser
    df = df.rename(columns={
        "name": "form_name",
        "link": "form_link"
    })
    
    return df.to_dict(orient="records")
