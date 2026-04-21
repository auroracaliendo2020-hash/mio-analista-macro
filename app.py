import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from duckduckgo_search import DDGS

# 1. Configurazione della Pagina
st.set_page_config(page_title="Analista Macro Real-Time", page_icon="📊", layout="wide")

# 2. Funzione di ricerca personalizzata (Sostituisce quella che dava errore)
def cerca_notizie(query):
    try:
        with DDGS() as ddgs:
            risultati = [r['body'] for r in ddgs.text(query, max_results=5, region='it-it', safesearch='off', timelimit='m')]
            return "\n\n".join(risultati)
    except Exception as e:
        return f"Non è stato possibile recuperare notizie in tempo reale: {e}"

# 3. Interfaccia Utente
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci Groq API Key", type="password")
    st.info("Utilizziamo Llama 3.3 e ricerca diretta DuckDuckGo.")

st.title("📊 Analista Macroeconomico con Notizie Live")
domanda = st.text_input("Cosa vuoi monitorare oggi?", placeholder="Esempio: Previsioni tassi BCE oggi")

# 4. Logica di Analisi
if st.button("Avvia Analisi"):
    if not api_key:
        st.warning("⚠️ Inserisci la tua API Key di Groq!")
    elif not domanda:
        st.warning("⚠️ Scrivi una domanda!")
    else:
        try:
            llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0.2)
            
            with st.spinner("🕵️ Ricerca notizie e analisi in corso..."):
                # Usiamo la nostra funzione sicura
                notizie_fresche = cerca_notizie(domanda)
                
                prompt = f"""
                Sei un analista economico. Usa queste notizie recenti:
                {notizie_fresche}
                
                Rispondi a: {domanda}
                Fornisci un'analisi tecnica e una stima delle probabilità in Italiano.
                """
                
                risposta = llm.invoke([HumanMessage(content=prompt)])
                
                st.success("✅ Analisi Completata")
                st.markdown("### 📝 Report dell'Analista")
                st.write(risposta.content)
                
                with st.expander("Vedi i dati grezzi trovati"):
                    st.write(notizie_fresche)
                        
        except Exception as e:
            st.error(f"Errore tecnico: {e}")

st.markdown("---")
st.caption("Versione 2026 - Ottimizzata per Python 3.14")
