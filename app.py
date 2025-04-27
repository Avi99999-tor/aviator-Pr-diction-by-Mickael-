import streamlit as st
from datetime import datetime, timedelta

# --- Login Page ---
def login():
    st.title("Top Exacte - Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "Aviator26" and password == "288612bymicka":
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# --- Prediction Intervalle (Version Nouvelle) ---
def predict_intervalle_schema(schema, m2, heure, minute, seconde):
    if m2 >= 50:
        return "Avertissement : Multiplicateur supérieur à 50. Pas de prédiction.", None, None

    chiffre = int(str(m2).split(".")[1][:2])
    heure_repere = datetime.strptime(f"{heure}:{minute}:{seconde}", "%H:%M:%S")

    if schema == "Schéma 1":
        if 0 <= chiffre <= 19:
            prediction_time = heure_repere + timedelta(minutes=5, seconds=10)
        elif 20 <= chiffre <= 39:
            prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
        else:
            return "Pas de prédiction possible avec ce chiffre après virgule.", None, None
        type_prediction = "X2 X3 (Normal)"

    elif schema == "Schéma 2":
        if 0 <= chiffre <= 19:
            prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
        elif 20 <= chiffre <= 39:
            prediction_time = heure_repere + timedelta(minutes=7, seconds=10)
        else:
            return "Pas de prédiction possible avec ce chiffre après virgule.", None, None
        type_prediction = "X2 X3 (Normal)"

    elif schema == "Schéma 3":
        if 0 <= chiffre <= 19:
            prediction_time = heure_repere + timedelta(minutes=5, seconds=10)
        elif 20 <= chiffre <= 39:
            prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
        else:
            return "Pas de prédiction possible avec ce chiffre après virgule.", None, None
        type_prediction = "X5 X10 (Spécial)"

    else:
        return "Schéma invalide.", None, None

    return None, prediction_time, type_prediction

# --- Prediction Tours (Ancienne Version) ---
def predict_tours(m1, m2, m3, tour2):
    chiffre1 = int(str(m1).split(".")[1][:2])
    chiffre3 = int(str(m3).split(".")[1][:2])

    if m1 % 2 == 0 and m3 % 2 == 0:
        risque = chiffre1 < chiffre3

        ajout = []
        if 0 <= chiffre1 <= 9:
            ajout = [13, 14, 15]
        elif 10 <= chiffre1 <= 19:
            ajout = [12, 13, 14]
        elif 20 <= chiffre1 <= 29:
            ajout = [11, 12, 13]
        elif 30 <= chiffre1 <= 39:
            ajout = [14, 15, 16]
        elif 50 <= chiffre1 <= 59:
            ajout = [11, 12, 13]
        elif 70 <= chiffre1 <= 79:
            ajout = [6, 7, 8]
        elif 80 <= chiffre1 <= 89:
            ajout = [15, 16, 17]

        if ajout:
            predictions = [f"T{tour2 + a}" for a in ajout]
            return predictions, risque
        else:
            return None, None
    else:
        st.warning("Multiplicateur 1 et 3 doivent être pairs (terminés par 0,2,4,6,8).")
        return None, None

# --- Main Page ---
def main_page():
    st.title("Top Exacte - Prédiction Aviator")

    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

    st.header("Choisir la stratégie")
    strategie = st.selectbox("Stratégie :", ["Top Intervalle", "Top Tours"])

    if strategie == "Top Intervalle":
        st.subheader("Top Intervalle (Nouveau Mode)")
        
        schema = st.selectbox("Sélectionner le type de schéma :", ["Schéma 1", "Schéma 2", "Schéma 3"])
        m2 = st.number_input("Multiplicateur Repéré (ex: 12.34)", step=0.01)

        st.header("Entrer l'heure du multiplicateur repère")
        heure = st.number_input("Heure", min_value=0, max_value=23, step=1)
        minute = st.number_input("Minute", min_value=0, max_value=59, step=1)
        seconde = st.number_input("Seconde", min_value=0, max_value=59, step=1)

        if st.button("Calculer la Prédiction Intervalle"):
            avertissement, prediction_time, type_prediction = predict_intervalle_schema(schema, m2, heure, minute, seconde)

            if avertissement:
                st.warning(avertissement)
            else:
                st.success(f"Prédiction : **{prediction_time.strftime('%H:%M:%S')}** ({type_prediction})")
                st.info("Attention : Si X50 ou plus apparaît, ne pas suivre cette prédiction. Si coupure, passer en prédiction Tours.")

    else:
        st.subheader("Top Tours")
        col1, col2, col3 = st.columns(3)
        with col1:
            m1 = st.number_input("Multiplicateur 1", step=0.01, key="tour_m1")
        with col2:
            m2 = st.number_input("Multiplicateur 2 (repère)", step=0.01, key="tour_m2")
        with col3:
            m3 = st.number_input("Multiplicateur 3", step=0.01, key="tour_m3")

        tour2 = st.number_input("Numéro de tour du multiplicateur 2", step=1)

        if st.button("Calculer la Prédiction Tours"):
            predictions, risque = predict_tours(m1, m2, m3, tour2)
            if predictions:
                if risque:
                    st.warning("**Prédiction Risque** :")
                else:
                    st.success("**Prédiction Normale** :")

                st.write(f"Prédiction Tours : {' / '.join(predictions)} —> **X4 X10 X20**")
            else:
                st.error("Pas de prédiction possible avec ces données.")

# --- App Control ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_page()
else:
    login()
