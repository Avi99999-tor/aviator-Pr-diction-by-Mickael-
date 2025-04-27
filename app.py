import streamlit as st from datetime import datetime, timedelta

--- Login Page ---

def login(): st.title("Top Exacte - Connexion") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Aviator26" and password == "288612bymicka": st.session_state.logged_in = True st.experimental_rerun() else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Top Tours Prediction ---

def predict_top_tours(m1, m2, m3, tour_repere): results = []

# Vérifier que multiplicateur 1 et 3 finissent par chiffre pair
if int(str(m1)[-1]) % 2 == 0 and int(str(m3)[-1]) % 2 == 0:
    chiffre1 = int(str(m1).split(".")[-1][:2])
    chiffre3 = int(str(m3).split(".")[-1][:2])

    # Détection du risque
    risque = chiffre1 < chiffre3

    # Sélection du saut selon chiffre après virgule de m2
    chiffre_apres_virgule = int(str(m2).split(".")[-1][:2])
    if 0 <= chiffre_apres_virgule <= 9:
        offsets = [13, 14, 15]
    elif 10 <= chiffre_apres_virgule <= 19:
        offsets = [12, 13, 14]
    elif 20 <= chiffre_apres_virgule <= 29:
        offsets = [11, 12, 13]
    elif 30 <= chiffre_apres_virgule <= 39:
        offsets = [14, 15, 16]
    elif 50 <= chiffre_apres_virgule <= 59:
        offsets = [11, 12, 13]
    elif 70 <= chiffre_apres_virgule <= 79:
        offsets = [6, 7, 8]
    elif 80 <= chiffre_apres_virgule <= 89:
        offsets = [15, 16, 17]
    else:
        return ["Aucune prédiction fiable pour ce chiffre."]

    predictions = [tour_repere + offset for offset in offsets]
    return predictions, risque
else:
    return None, None

--- Top Intervalle Prediction ---

def predict_top_intervalle(m1, m2, m3, heure, minute, seconde): resultats = [] heure_repere = datetime.strptime(f"{heure}:{minute}:{seconde}", "%H:%M:%S")

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

--- Main Page ---

def main_page(): st.title("Top Exacte - Prédiction Aviator")

if st.button("Se déconnecter"):
    st.session_state.logged_in = False
    st.experimental_rerun()

strategie = st.selectbox("Choisir la stratégie:", ("Top Tours", "Top Intervalle"))

if strategie == "Top Tours":
    st.header("Top Tours")
    m1 = st.number_input("Multiplicateur 1", step=0.01)
    m2 = st.number_input("Multiplicateur 2 (Repère)", step=0.01)
    m3 = st.number_input("Multiplicateur 3", step=0.01)
    tour_repere = st.number_input("Numéro de Tour du Multiplicateur 2", step=1)

    if st.button("Calculer Prédiction Top Tours"):
        predictions, risque = predict_top_tours(m1, m2, m3, tour_repere)
        if predictions:
            st.success(f"Prédictions: T{predictions[0]} / T{predictions[1]} / T{predictions[2]} => X4 X10")
            if risque:
                st.warning("Prédiction RISQUE détectée: chiffre après virgule du Multiplicateur 1 < Multiplicateur 3")
        else:
            st.error("Condition non respectée (Multiplicateur 1 et 3 doivent être paire)")

elif strategie == "Top Intervalle":
    st.header("Top Intervalle")
    m1 = st.number_input("Multiplicateur 1", step=0.01, key="m1_interv")
    m2 = st.number_input("Multiplicateur 2 (Repère)", step=0.01, key="m2_interv")
    m3 = st.number_input("Multiplicateur 3", step=0.01, key="m3_interv")
    heure = st.number_input("Heure", min_value=0, max_value=23, step=1)
    minute = st.number_input("Minute", min_value=0, max_value=59, step=1)
    seconde = st.number_input("Seconde", min_value=0, max_value=59, step=1)

    if st.button("Calculer Prédiction Top Intervalle"):
        resultats = predict_top_intervalle(m1, m2, m3, heure, minute, seconde)
        if resultats:
            st.success("Résultats de Prédiction :")
            for resultat in resultats:
                if resultat[2] == "normal":
                    st.write(f"Heure de prochaine multiplicateur : **{resultat[0].strftime('%H:%M:%S')}** ({resultat[1]})")
                    st.info("Si la prédiction est incorrecte, miser X2, X5 ou X10 au tour suivant.")
                elif resultat[2] == "special":
                    start, end = resultat[0]
                    st.write(f"Intervalle spécial : **{start.strftime('%H:%M:%S')} à {end.strftime('%H:%M:%S')}** ({resultat[1]})")
                    st.warning("PRÉDICTION SPÉCIALE : Intervalle X5/X10. Soyez attentif !")

--- App Control ---

if "logged_in" not in st.session_state: st.session_state.logged_in = False

if st.session_state.logged_in: main_page() else: login()

