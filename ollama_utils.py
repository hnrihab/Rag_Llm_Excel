from langchain_ollama import OllamaLLM

# Initialise le LLM Ollama
llm = OllamaLLM(model="llama3.2")  # Assure-toi que ton serveur Ollama est lancé

def ask_llm(prompt: str):
    """Envoie une question au LLM Ollama et récupère la réponse"""
    try:
        response = llm(prompt)
        return response
    except Exception as e:
        return f"Erreur Ollama : {e}"
