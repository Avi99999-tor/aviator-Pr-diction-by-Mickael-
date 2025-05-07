import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Aviator Mode ARIMA - Prédiction T+20", layout="centered")
st.title("🎯 Mode ARIMA Aviator - Prédiction T+20")

# Entrée des multiplicateurs
user_input = st.text_area("Entrez les derniers multiplicateurs (max 20, ex: 1.57x 2.43x 74.16x):")

if user_input:
    try:
        # Nettoyage
        raw_data = [float(x.replace('x','')) for x in user_input.strip().split()]
        
        # Indication s’il y a un jackpot (>50x)
        jackpot_detected = any(val >= 50 for val in raw_data)
        if jackpot_detected:
            st.warning("Jackpot détecté ! (valeurs > 50x) — Ces points ne sont pas utilisés pour la prédiction.")
            clean_data = [val for val in raw_data if val < 50]
        else:
            clean_data = raw_data

        # Garder maximum 20 dernières valeurs
        if len(clean_data) > 20:
            clean_data = clean_data[-20:]
            st.info("Seules les 20 dernières valeurs sans jackpot sont prises.")

        df = pd.Series(clean_data)

        last_T = st.number_input("Numéro de la dernière tour (T...):", min_value=0, step=1)

        # Modèle ARIMA
        model = ARIMA(df, order=(2,1,2))  # azo ovaina arakaraka ny training
        model_fit = model.fit()

        preds = model_fit.forecast(steps=20)

        st.subheader("🔮 Prédiction T+1 à T+20")
        for i, val in enumerate(preds):
            st.write(f"T{int(last_T) + i + 1} → {round(val, 2)}x")

    except Exception as e:
        st.error(f"Erreur: {e}")
else:
    st.info("Ampidiro ny multiplicateurs an'ny tours farany (ex: 1.02x 2.45x 3.12x ...)")
