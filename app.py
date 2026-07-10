import streamlit as st
import datetime

# Ustawienia strony
st.set_page_config(page_title="AlbaMaintenance AI", layout="wide")

st.title("⚙️ AlbaMaintenance AI")
st.subheader("System Zarządzania Utrzymaniem Ruchu")

# Formularz wpisu
with st.form("raport_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        data_wpisu = st.date_input("DATA WPISU", datetime.date.today())
        zmiana = st.selectbox("ZMIANA", ["Zmiana A", "Zmiana B", "Zmiana C"])
        maszyna = st.selectbox("MASZYNA", ["Maszyna 1", "Maszyna 2", "Linia Produkcyjna"])
    
    with col2:
        czas_przestoju = st.number_input("CZAS PRZESTOJU (min)", min_value=0)
        notatka_glosowa = st.file_uploader("NOTATKA GŁOSOWA (dla pracowników UR)", type=["mp3", "wav"])
    
    surowy_opis = st.text_area("SUROWY OPIS AWARII")
    
    submit_button = st.form_submit_button("Zapisz raport")

# Sekcje po zapisaniu
if submit_button:
    st.success("Raport zapisany pomyślnie!")
    
    # Symulacja raportu AI
    st.divider()
    st.markdown("### 🤖 RAPORT AI")
    st.info("Analiza w toku: System sugeruje sprawdzenie czujnika zbliżeniowego oraz weryfikację napięcia silnika.")
    
    # Polecenia kierownika (dostępne dla wszystkich do wglądu)
    st.markdown("### 👨‍💼 POLECENIA KIEROWNIKA")
    st.text_area("Wpisz wytyczne tutaj...", value="Czekam na diagnozę od UR.", key="kierownik")