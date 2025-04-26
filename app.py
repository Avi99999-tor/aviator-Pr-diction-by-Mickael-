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

# --- Prediction Function ---
def predict(m1, m2, m3, heure, minute, seconde):
    resultats = []
    heure_repere = datetime.strptime(f"{heure}:{minute}:{seconde}", "%H:%M:%S")

    # Vérification de la condition 1
    if m1 > m3:
        # Cas spéciaux
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
            # Cas normal
            if m2 < 20:
                prediction_time = heure_repere + timedelta(minutes=5, seconds=10)
            elif 20 <= m2 <= 39:
                prediction_time = heure_repere + timedelta(minutes=6, seconds=10)
            resultats.append((prediction_time, "X2 X3", "normal"))
    else:
        st.warning("Condition non valide : Multiplicateur 1 doit être supérieur à Multiplicateur 3.")

    return resultats

# --- Main Page ---
def main_page():
    st.title("Top Exacte - Prédiction Aviator")

    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

    st.header("Entrer les multiplicateurs")
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

    if st.button("Calculer la Prédiction"):
        resultats = predict(m1, m2, m3, heure, minute, seconde)

        st.success("Résultats de Prédiction :")
        for resultat in resultats:
            if resultat[2] == "normal":
                st.write(f"Heure de prochaine multiplicateur : **{resultat[0].strftime('%H:%M:%S')}** ({resultat[1]})")
                st.info("Si la prédiction est incorrecte, miser X2, X5 ou X10 au tour suivant.")
            elif resultat[2] == "special":
                start, end = resultat[0]
                st.write(f"Intervalle spécial : **{start.strftime('%H:%M:%S')} à {end.strftime('%H:%M:%S')}** ({resultat[1]})")
                st.warning("PRÉDICTION SPÉCIALE : Intervalle X5/X10. Soyez attentif !")

    if st.button("Réinitialiser"):
        st.experimental_rerun()

# --- App Control ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_page()
else:
    login()
