import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from streamlit_mic_recorder import mic_recorder

# 1. Konfiguracja AI (Google Gemini)
# Upewnij się, że w Streamlit Secrets masz: GOOGLE_API_KEY = "Twój_klucz"
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AlbaMaintenance AI", layout="centered")
st.title("⚙️ AlbaMaintenance AI")
st.subheader("System Zarządzania Utrzymaniem Ruchu")

# 2. Formularz wpisu
with st.form("raport_form"):
    col1, col2 = st.columns(2)
    with col1:
        data_wpisu = st.date_input("DATA WPISU", datetime.now())
        zmiana = st.selectbox("ZMIANA", ["Zmiana A", "Zmiana B", "Zmiana C"])
    with col2:
        czas_przestoju = st.number_input("CZAS PRZESTOJU (min)", min_value=0, step=1)
        maszyna = st.selectbox("MASZYNA", ["Maszyna 1", "Maszyna 2", "Maszyna 3"])

    # Obsługa mikrofonu
    st.write("NOTATKA GŁOSOWA")
    audio = mic_recorder(start_prompt="Nagrywaj", stop_prompt="Stop", key='recorder')
    
    surowy_opis = st.text_area("SUROWY OPIS AWARII", placeholder="Wpisz opis lub skorzystaj z notatki głosowej...")
    
    submitted = st.form_submit_button("Zapisz raport")

# 3. Logika AI
if st.button("Analizuj przez AI"):
    if not surowy_opis:
        st.warning("Najpierw wpisz opis awarii!")
    else:
        with st.spinner("AI analizuje usterkę..."):
            try:
                response = model.generate_content(f"Jesteś ekspertem utrzymania ruchu. Przeanalizuj następujący opis awarii i zaproponuj rozwiązanie: {surowy_opis}")
                st.info(f"**Analiza AI:**\n\n{response.text}")
            except Exception as e:
                st.error(f"Błąd AI: {e}")

# 4. Zapis danych
if submitted:
    dane = {
        "Data": [data_wpisu],
        "Zmiana": [zmiana],
        "Maszyna": [maszyna],
        "Przestoj": [czas_przestoju],
        "Opis": [surowy_opis]
    }
    df = pd.DataFrame(dane)
    
    # Zapis do pliku CSV (działa na GitHubie wewnątrz repozytorium)
    try:
        df.to_csv("historia_awarii.csv", mode='a', header=False, index=False)
        st.success("Raport został zapisany w historii!")
    except Exception as e:
        st.error(f"Nie udało się zapisać pliku: {e}")

# Wyświetlanie historii (opcjonalnie)
if st.checkbox("Pokaż historię awarii"):
    try:
        historia = pd.read_csv("historia_awarii.csv", names=["Data", "Zmiana", "Maszyna", "Przestój", "Opis"])
        st.table(historia)
    except:
        st.write("Brak zapisanych raportów.")