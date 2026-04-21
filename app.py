import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq

# Configurazione Pagina
st.set_page_config(page_title="Analista Macro Evoluto", layout="wide")

# --- PASSWORD DI ACCESSO ---
PASSWORD_CORRETTA = "progetto2024" 

if "password_correct" not in st.session_state:
    st.title("🔐 Accesso Protetto")
    pwd = st.text_input("Inserisci la password:", type="password")
    if st.button("Entra"):
        if pwd == PASSWORD_CORRETTA:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Password errata")
    st.stop()

# --- RECUPERO API KEY ---
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("Configura GROQ_API_KEY nei Secrets di Streamlit!")
    st.stop()

# Modello aggiornato (Llama 3.3 è il più stabile ora)
llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

st.title("🏛️ Analista Macroeconomico Strategico")
st.markdown("---")

# 1. DOMANDE SULL'ATTUALITÀ
st.subheader("💬 Analisi dell'Attualità")
user_query = st.text_input("Chiedi all'IA sulla situazione economica attuale:")

if user_query:
    with st.spinner("L'analista sta pensando..."):
        try:
            response = llm.invoke(f"Rispondi come un analista finanziario esperto: {user_query}")
            st.info(response.content)
        except Exception as e:
            st.error(f"Errore: {e}")

st.markdown("---")

# 2. ANALISI DATI (FILE)
st.subheader("📊 Analisi Tecnica dei tuoi Dati")
uploaded_file = st.file_uploader("Carica Excel o CSV", type=['csv', 'xlsx'])

riassunto_dati = ""
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("✅ Anteprima dati:")
        st.dataframe(df.head(3))
        riassunto_dati = df.describe().to_string()
        
        if st.button("Esegui Analisi Numerica"):
            with st.spinner("Analizzando i numeri..."):
                res = llm.invoke(f"Analizza tecnicamente questi dati: {riassunto_dati}")
                st.write(res.content)
    except Exception as e:
        st.error(f"Errore file: {e}")

st.markdown("---")

# 3. GIUDIZIO FINALE
st.subheader("🏁 Giudizio Professionale Conclusivo")
if st.button("Genera Panoramica e Sentenza Finale"):
    with st.spinner("Sintetizzando il report..."):
        context = f"Dati utente: {riassunto_dati}" if riassunto_dati else "Analisi basata su scenario globale."
        final_prompt = f"Agisci come capo analista. Basandoti su {context}, dai una panoramica, un giudizio finale e consigli strategici."
        final_res = llm.invoke(final_prompt)
        st.markdown(final_res.content)
