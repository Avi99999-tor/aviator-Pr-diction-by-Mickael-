import streamlit as st
import numpy as np

st.title("Prédiction Aviator - Mode ARIMA Simplifié")

# Input données utilisateur
input_text = st.text_area("Entrez les 20 derniers multiplicateurs (séparés par espace ou virgule):")

if input_text:
    try:
        # Nettoyage et parsing
        data = [float(val.replace('x', '')) for val in input_text.replace(",", " ").split()]
        data = data[::-1]  # renversina ilay lisitra: ny vaovao indrindra ho farany

        if len(data) < 10:
            st.warning("Ampidiro farafahakeliny 10 valeurs.")
        else:
            # Calculer les différences successives (Δ1)
            diff1 = [data[i] - data[i+1] for i in range(len(data)-1)]

            # Moyenne des tendances récentes
            mean = np.mean(data)
            trend = np.mean(diff1[-5:])  # tendance farany 5

            # Prédiction T+1 à T+20 (avec ajout tendance tsikelikely)
            prediction = []
            next_val = data[0]
            for i in range(20):
                next_val = max(1.0, next_val + trend * np.random.uniform(0.8, 1.2))  # mitovy amin'ny ARIMA dynamique
                prediction.append(round(next_val, 2))

            st.success("Résultat des prédictions T+1 à T+20 :")
            for i, val in enumerate(prediction, 1):
                st.write(f"T+{i}: {val}x")

    except Exception as e:
        st.error(f"Erreur de traitement: {e}")
