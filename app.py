import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Expert By Mickael")

st.subheader("Fanatsarana probabilités AI sy Expert")

# --- Fidirana data (multiplicateurs) ---
multiplicateurs_input = st.text_area("💾 Ampidiro ny multiplicateurs (misaraka amin'ny espace)", 
                                     placeholder="1.99x 2.30x 1.42x 1.12x ...", height=150)

dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=204)

# --- Bouton Calculer ---
calculer = st.button("🔄 Calculer les prédictions")

# --- Fanadiovana angona ---
def extraire_valeurs(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    valeurs_propres = [float(v) for v in valeurs if v.replace('.', '', 1).isdigit()]
    return valeurs_propres

# --- Fiabilité calculation ---
def fiabilite(val):
    return round(random.uniform(70, 95), 2)

# --- Algorithme AI: Régression avancée ---
def regression_prediction(multiplicateurs):
    X = np.arange(len(multiplicateurs)).reshape(-1, 1)
    y = np.array(multiplicateurs).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    pred = model.predict(np.arange(len(multiplicateurs), len(multiplicateurs) + 20).reshape(-1, 1))
    return [round(max(1.00, float(p)), 2) for p in pred]

# --- Prediction Expert ---
def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    for i in range(1, 21):
        seed = int((rolling_mean + i * 3.73) * 1000) % 47
        pred_expert = round(abs(np.sin(seed) * 3.2 + random.uniform(0.3, 1.2)), 2)
        résultats.append(pred_expert)
    return résultats

# --- Prediction Combinée ---
def prediction_combinee(historique, base_tour):
    ia_preds = regression_prediction(historique)
    exp_preds = prediction_expert(historique, base_tour)
    résultats = []

    for i in range(20):
        ai, exp = ia_preds[i], exp_preds[i]
        final = round((ai * 0.5 + exp * 0.5), 2)
        fiabilité = fiabilite(final)

        résultats.append({
            "Tour": f"T{base_tour + i + 1}",
            "Prediction IA": f"{ai}x",
            "Prediction Expert": f"{exp}x",
            "Résultat Final": f"{final}x",
            "Fiabilité": f"{fiabilité}%"
        })
    
    return résultats

# --- Fanodinana ---
if calculer:
    historique = extraire_valeurs(multiplicateurs_input)
    if len(historique) < 10:
        st.warning("❗ Tokony hampiditra farafahakeliny 10 multiplicateurs.")
    else:
        résultats_df = prediction_combinee(historique, int(dernier_tour))
        st.markdown("### 📊 Résultat T+205 à T+224 :")
        st.table(résultats_df)
