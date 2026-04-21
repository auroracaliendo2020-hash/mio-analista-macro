import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Analista Macro Economico", layout="wide")

# --- PROTEZIONE ACCESSO (PASSWORD) ---
# Puoi cambiare 'progetto2024' con la password che preferisci
PASSWORD_CORRETTA = "progetto2024" 

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Accesso Protetto")
        pwd = st.text_input("Inserisci la password per utilizzare l'analista:", type="password")
        if st.button("Entra"):
            if pwd == PASSWORD_CORRETTA:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Password errata")
        return False
    return True

if check_password():
    # --- RECUPERO API KEY DAI SECRETS ---
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.warning("⚠️ API Key non trovata nei Secrets. Inseriscila lateralmente per testare.")
        api_key = st.sidebar.text_input("Groq API Key", type="password")

    st.title("📊 Analista Macro Economico IA")
    st.markdown("Carica un file Excel o CSV con dati economici per ricevere un'analisi professionale.")

    # --- CARICAMENTO FILE ---
    uploaded_file = st.file_location = st.file_uploader("Scegli un file", type=['csv', 'xlsx'])

    if uploaded_file is not None and api_key:
        try:
            # Lettura dati
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.subheader("Anteprima Dati")
            st.dataframe(df.head())

            # Configurazione Modello IA
            llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-70b-versatile")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Sei un esperto analista macroeconomico. Analizza i dati forniti e spiega i trend, i rischi e le opportunità in modo professionale."),
                ("user", "Ecco i dati da analizzare:\n\n{data_summary}")
            ])

            chain = prompt | llm | StrOutputParser()

            if st.button("Genera Analisi Professionale"):
                with st.spinner("L'intelligenza artificiale sta analizzando i trend..."):
                    # Trasformiamo il dataframe in testo per l'IA
                    data_str = df.describe().to_string()
                    risposta = chain.invoke({"data_summary": data_str})
                    
                    st.success("Analisi Completata!")
                    st.markdown("### Report dell'Analista")
                    st.write(risposta)
        
        except Exception as e:
            st.error(f"Si è verificato un errore: {e}")
    elif not api_key:
        st.info("Configura la tua API Key negli Advanced Settings di Streamlit per iniziare.")
