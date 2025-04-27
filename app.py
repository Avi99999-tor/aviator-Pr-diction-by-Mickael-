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

# --- Prediction Intervalle ---
def predict_intervalle(m1, m2, m3, heure, minute, seconde):
    resultats = []
    heure_repere = datetime.strptime(f"{heure}:{minute}:{seconde}", "%H:%M:%S")

    if m1 > m3:
        if m1 >= 50 and m3 < 50:
            if m2 < 20:
                prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
            elif 20 <= m2 <= 39:
                prediction_time = heure_repere + timedelta(minutes=7, seconds=10)
            resultats.append((prediction_time, "X2 X3", "normal"))
        elif m1 >= 50 and m3 >= 50:
            if m2 < 20:
                start = heure_repere + timedelta(minutes=5, seconds=10)
                end = heure_repere + timedelta(minutes=6, seconds=10)
            else:
                start = heure_repere + timedelta(minutes=6, seconds=10)
                end = heure_repere + timedelta(minutes=7, seconds=10)
            resultats.append(((start, end), "X5 X10", "special"))
        else:
            if m2 < 20:
                prediction_time = heure_repere + timedelta(minutes=5, seconds=10)
            elif 20 <= m2 <= 39:
                prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
            resultats.append((prediction_time, "X2 X3", "normal"))
    else:
        st.warning("Condition non valide : Multiplicateur 1 doit être supérieur à Multiplicateur 3.")

    return resultats

# --- Prediction Tours ---
def predict_tours(m1, m2, m3, tour2):
    chiffre1 = int(str(m1).split(".")[1][:2])
    chiffre3 = int(str(m3).split(".")[1][:2])

    if m1 % 2 == 0 and m3 % 2 == 0:
        if chiffre1 < chiffre3:
            risque = True
        else:
            risque = False

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
        else:
            ajout = []

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
        st.subheader("Top Intervalle")
        col1, col2, col3 = st.columns(3)
        with col1:
            m1 = st.number_input("Multiplicateur 1", step=0.01)
        with col2:
            m2 = st.number_input("Multiplicateur 2 (repère)", step=0.01)
        with col3:
            m3 = st.number_input("Multiplicateur 3", step=0.01)

        st.header("Entrer l'heure du multiplicateur repère")
        heure = st.number_input("Heure", min_value=0, max_value=23, step=1)
        minute = st.number_input("Minute", min_value=0, max_value=59, step=1)
        seconde = st.number_input("Seconde", min_value=0, max_value=59, step=1)

        if st.button("Calculer la Prédiction Intervalle"):
            resultats = predict_intervalle(m1, m2, m3, heure, minute, seconde)

            st.success("Résultats de Prédiction Intervalle :")
            for resultat in resultats:
                if resultat[2] == "normal":
                    st.write(f"Heure : **{resultat[0].strftime('%H:%M:%S')}** ({resultat[1]})")
                elif resultat[2] == "special":
                    start, end = resultat[0]
                    st.write(f"Intervalle spécial : **{start.strftime('%H:%M:%S')} à {end.strftime('%H:%M:%S')}** ({resultat[1]})")

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
