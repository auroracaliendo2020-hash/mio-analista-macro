import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Analista Macro Evoluto", layout="wide")

# --- PASSWORD ---
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
    st.error("ERRORE: API Key non configurata nei Secrets di Streamlit.")
    st.stop()

llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-70b-versatile")

st.title("🏛️ Analista Macroeconomico Strategico")
st.markdown("---")

# --- SEZIONE 1: ATTUALITÀ E DOMANDE LIBERE ---
st.subheader("💬 Analisi dell'Attualità")
user_query = st.text_input("Poni una domanda sulla situazione economica attuale (es. mercati, inflazione, geopolitica):")

if user_query:
    with st.spinner("L'analista sta elaborando una risposta..."):
        response = llm.invoke(f"Rispondi come un analista finanziario esperto: {user_query}")
        st.info(response.content)

st.markdown("---")

# --- SEZIONE 2: ANALISI DATI (EXCEL/CSV) ---
st.subheader("📊 Analisi Tecnica dei tuoi Dati")
uploaded_file = st.file_uploader("Carica i tuoi dati economici", type=['csv', 'xlsx'])

# Variabile per memorizzare il riassunto dei dati
riassunto_dati = ""

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("✅ File caricato con successo. Anteprima:")
        st.dataframe(df.head(3))
        
        riassunto_dati = df.describe().to_string()
        
        if st.button("Esegui Analisi Numerica"):
            with st.spinner("Calcolo dei trend in corso..."):
                res = llm.invoke(f"Analizza tecnicamente questi dati statistici e spiega cosa indicano: {riassunto_dati}")
                st.success("Analisi Tecnica Completata")
                st.write(res.content)
    except Exception as e:
        st.error(f"Errore: {e}")

st.markdown("---")

# --- SEZIONE 3: PANORAMICA E GIUDIZIO FINALE ---
st.subheader("🏁 Giudizio Professionale Conclusivo")
if st.button("Genera Panoramica e Sentenza Finale"):
    with st.spinner("Sintetizzando la strategia..."):
        # Se c'è un file, lo include nel giudizio, altrimenti fa un'analisi generale
        context = f"Dati caricati: {riassunto_dati}" if riassunto_dati else "Nessun file specifico caricato."
        
        final_prompt = f"""
        Basandoti sulla situazione economica globale attuale e sui seguenti dati specifici: {context}
        Fornisci:
        1. Una panoramica macroeconomica generale.
        2. Un giudizio finale (Bullish, Bearish o Neutral).
        3. Consigli strategici sui rischi da monitorare.
        Sii sintetico, autorevole e professionale.
        """
        
        final_res = llm.invoke(final_prompt)
        st.markdown("### 📝 Report di Sintesi Finale")
        st.markdown(final_res.content)
