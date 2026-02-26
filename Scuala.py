import streamlit as st
from PIL import Image
import google.generativeai as genai

# --- CONFIGURAZIONE API ---
# Prende la chiave dai Secrets che hai impostato su Streamlit Cloud
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("Chiave API non trovata! Vai in Settings > Secrets e aggiungi GEMINI_API_KEY")
except Exception as e:
    st.error(f"Errore configurazione: {e}")

# Inizializziamo il modello (1.5 Flash è perfetto per le foto)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- INTERFACCIA ---
st.set_page_config(page_title="Docente Smart", page_icon="🍎")
st.title("🍎 Assistente DidUp")

# Inizializziamo lo stato della scelta se non esiste
if 'scelta' not in st.session_state:
    st.session_state.scelta = None

# Input Classe (sempre in alto)
classe = st.text_input("Inserisci la Classe (es. 3A):", "1A")

st.write("Cosa vuoi fare oggi?")

# --- BOTTONI PRINCIPALI ---
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 TEMA", use_container_width=True):
        st.session_state.scelta = "tema"

with col2:
    if st.button("✅ COMPITI", use_container_width=True):
        st.session_state.scelta = "compiti"

st.divider()

# --- LOGICA FOTOCAMERA ---
# La fotocamera appare solo dopo aver premuto un bottone
if st.session_state.scelta:
    st.subheader(f"Modalità: {st.session_state.scelta.upper()}")
    
    # Questo apre la camera del telefono
    img_file = st.camera_input("Scatta una foto nitida")

    if img_file:
        img = Image.open(img_file)
        
        # Prepariamo il messaggio per Gemini in base al bottone premuto
        if st.session_state.scelta == "tema":
            prompt = "Analizza l'immagine (lavagna o appunti) e scrivi un testo di massimo 20 parole per il registro didUp Famiglia che spieghi cosa è stato fatto oggi in classe."
        else:
            prompt = f"Sei un insegnante della classe {classe}. Guarda la foto di questo compito/verifica. Dimmi in quali righe ci sono errori e perché. Alla fine dai un voto da 1 a 10. Sii molto sintetico."

        with st.spinner("Gemini sta analizzando..."):
            try:
                # Chiediamo a Gemini di analizzare la foto
                response = model.generate_content([prompt, img])
                
                st.success("Risultato:")
                st.write(response.text)
                
                # Bottone per resettare tutto
                if st.button("Pulisci e torna indietro"):
                    st.session_state.scelta = None
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Errore durante l'analisi: {e}")

# --- PIÈ DI PAGINA ---
st.caption("Creato per aiutare i professori con didUp")

