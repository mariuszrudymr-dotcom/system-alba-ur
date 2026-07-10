import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

# Konfiguracja AI - bezpieczne ładowanie
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Błąd konfiguracji AI: {e}")
    st.stop()

st.set_page_config(page_title="AlbaMaintenance AI", layout="centered")
st.title("⚙️ AlbaMaintenance AI")

# Formularz
with st.form("raport_form"):
    data_wpisu = st.date_input("DATA WPISU", datetime.now())
    zmiana = st.selectbox("ZMIANA", ["Zmiana A", "Zmiana B", "Zmiana C"])
    czas_przestoju = st.number_input("CZAS PRZESTOJU (min)", min_value=0, step=1)
    maszyna = st.selectbox("MASZYNA", ["Maszyna 1", "Maszyna 2", "Maszyna 3"])
    
    st.write("---")
    st.write("NOTATKA GŁOSOWA")
    audio = mic_recorder(start_prompt="Nagrywaj", stop_prompt="Stop", key='recorder')
    
    surowy_opis = st.text_area("SUROWY OPIS AWARII", placeholder="Wpisz opis usterki...")
    
    submitted = st.form_submit_button("Zapisz raport i analizuj")

# Logika po wysłaniu
if submitted:
    # 1. Analiza AI
    with st.spinner("AI analizuje usterkę..."):
        try:
            prompt = f"Jesteś ekspertem utrzymania ruchu. Przeanalizuj opis awarii i zaproponuj rozwiązanie: {surowy_opis}"
            response = model.generate_content(prompt)
            st.info(f"**Analiza AI:**\n\n{response.text}")
        except Exception as e:
            st.error(f"Błąd AI: {e}")

    # 2. Zapis danych do CSV
    dane = {
        "Data": [str(data_wpisu)],
        "Zmiana": [zmiana],
        "Maszyna": [maszyna],
        "Przestoj": [czas_przestoju],
        "Opis": [surowy_opis]
    }
    df = pd.DataFrame(dane)
    
    try:
        # Sprawdzenie czy plik istnieje, by dodać nagłówek tylko raz
        import os
        file_exists = os.path.isfile("historia_awarii.csv")
        df.to_csv("historia_awarii.csv", mode='a', header=not file_exists, index=False)
        st.success("Raport został zapisany!")
    except Exception as e:
        st.error(f"Błąd zapisu pliku: {e}")

# Wyświetlanie historii
if st.checkbox("Pokaż historię awarii"):
    try:
        historia = pd.read_csv("historia_awarii.csv")
        st.table(historia)
    except:
        st.write("Brak zapisanych raportów.")