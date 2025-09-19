# app.py
import streamlit as st
import json
import pandas as pd
import os

st.title("📊 Analyse des Quiz Microsoft Forms avec Ollama")

# Charger tous les fichiers JSON
files = [f for f in os.listdir("results") if f.endswith(".json")]

if not files:
    st.warning("⚠️ Aucun résultat trouvé. Lance d'abord analyzer.py")
else:
    selected_file = st.selectbox("📂 Choisir un quiz", files)

    with open(f"results/{selected_file}", "r", encoding="utf-8") as f:
        data = json.load(f)

    st.subheader(f"📌 Quiz : {data['quiz_name']}")
    
    # Affichage brut JSON
    st.json(data)

    # Affichage tabulaire
    df = pd.DataFrame(data["questions"])
    st.dataframe(df)
