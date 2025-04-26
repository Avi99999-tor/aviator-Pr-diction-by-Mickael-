import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="PREDICTION DE MICKAEL", layout="centered")

# Login simple
with st.sidebar:
    st.title("Connexion")
    username = st.text_input("Nom utilisateur")
    code = st.text_input("Code secret", type="password")
    if username != "Aviator26" or code != "288612bymicka":
        st.warning("Veuillez entrer les bonnes informations.")
        st.stop()

# Titre principal
st.title("PREDICTION DE MICKAEL")

# Entrée des multiplicateurs
st.subheader("Entrer les 3 derniers multiplicateurs")
m1 = st.number_input("Multiplicateur 1", step=0.01, format="%.2f")
m2 = st.number_input("Multiplicateur 2 (repère)", step=0.01, format="%.2f")
m3 = st.number_input("Multiplicateur 3", step=0.01, format="%.2f")

# Entrée de l’heure du multiplicateur repère
st.subheader("Entrer l'heure du multiplicateur repère")
col1, col2, col3 = st.columns(3)
with col1:
    heure = st.number_input("Heure", min_value=0, max_value=23, step=1)
with col2:
    minute = st.number_input("Minute", min_value=0, max_value=59, step=1)
with col3:
    seconde = st.number_input("Seconde", min_value=0, max_value=59, step=1)

# Bouton de prédiction
if st.button("Lancer la prédiction"):
    valeur_apres_virgule = int(str(m2).split(".")[1][:2])
    base_time = datetime(2023, 1, 1, heure, minute, seconde)
    prediction_time = None
    condition1 = m1 > m3

    # Détermination du délai selon la stratégie
    if 0 <= valeur_apres_virgule <= 19:
        prediction_time = base_time + timedelta(minutes=5, seconds=10)
    elif 20 <= valeur_apres_virgule <= 39:
        prediction_time = base_time + timedelta(minutes=6, seconds=10)
        # Condition 2 : si m1 ou m2 >= 50
        if any(float(str(m).split(".")[1][:2]) >= 50 for m in [m1, m2]):
            prediction_time = base_time + timedelta(minutes=7, seconds=10)
    elif 10 <= valeur_apres_virgule <= 19:
        prediction_time = base_time + timedelta(minutes=6, seconds=10)

    # Page résultat
    st.markdown("---")
    st.header("Résultat de la prédiction")

    if condition1:
        st.success(f"Heure du prochain multiplicateur : **{prediction_time.time()}**")
        st.info("Si la prédiction est incorrecte, miser sur **X2 X5 X10** au tour suivant.")
    else:
        st.error("Prédiction non valide (Multiplicateur 1 doit être supérieur à Multiplicateur 3).")
        st.info("Si la prédiction est incorrecte, miser sur **X2 X5 X10** au tour suivant.")
