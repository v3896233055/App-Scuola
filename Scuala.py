import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configurazione API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
except Exception as e:
    st.error("Errore: Chiave API non trovata nei Secrets!")
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="Docente Smart", layout="centered")
st.title("🍎 Assistente DidUp")

# Inizializziamo lo stato se non esiste
if 'scelta' not in st.session_state:
    st.session_state.scelta = None

# Input Classe sempre visibile
classe = st.text_input("Classe (es. 3A):", "1A")

# --- MENU BOTTONI ---
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 TEMA (20 parole)", use_container_width=True):
        st.session_state.scelta = "tema"

with col2:
    if st.button("✅ COMPITI (Correzione)", use_container_width=True):
        st.session_state.scelta = "compiti"

st.divider()

# --- LOGICA FOTOCAMERA ---
# La camera appare SOLO se hai schiacciato un bottone
if st.session_state.scelta:
    st.subheader(f"Modalità: {st.session_state.scelta.upper()}")
    
    img_file = st.camera_input("Inquadra il foglio o la lavagna")

    if img_file:
        img = Image.open(img_file)
        
        if st.session_state.scelta == "tema":
            prompt = "Analizza l'immagine e scrivi un riassunto di massimo 20 parole di quello che è stato svolto in classe per il registro didUp Famiglia."
        else:
            prompt = f"Sei un insegnante della classe {classe}. Controlla questa verifica. Indica riga, errore e correzione. Sii brevissimo e dai un voto finale."

        with st.spinner("Gemini sta pensando..."):
            try:
                response = model.generate_content([prompt, img])
                st.success("Risultato Generato:")
                st.write(response.text)
                
                # Bottone per resettare e tornare ai due tasti iniziali
                if st.button("Fatto / Reset"):
                    st.session_state.scelta = None
                    st.rerun()
            except Exception as e:

                st.error(f"Errore: {e}")

