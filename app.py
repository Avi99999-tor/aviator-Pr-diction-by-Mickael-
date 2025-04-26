import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Prediction de Mickael", page_icon="🎯", layout="centered")

st.title("PREDICTION DE MICKAEL")

st.subheader("Entrer les trois derniers historiques")

# Inputs pour les trois derniers multiplicateurs
tour1 = st.text_input("1er multiplicateur (ex: 3.41)")
tour2 = st.text_input("2ème multiplicateur (ex: 1.08)")
tour3 = st.text_input("3ème multiplicateur (ex: 1.13)")

st.subheader("Entrer l'heure du multiplicateur de référence")
col1, col2, col3 = st.columns(3)
with col1:
    heure = st.number_input("Heure", 0, 23, 10)
with col2:
    minute = st.number_input("Minute", 0, 59, 23)
with col3:
    seconde = st.number_input("Seconde", 0, 59, 31)

def get_decimal(value):
    try:
        return int(str(value).split(".")[1])
    except:
        return 0

def is_croissant(t1, t2, t3):
    v1 = get_decimal(t1)
    v2 = get_decimal(t2)
    v3 = get_decimal(t3)
    return v1 < v2 < v3

def has_above_50(t1, t2, t3):
    v = [get_decimal(t1), get_decimal(t2), get_decimal(t3)]
    return sum(1 for x in v if x > 50)

def prediction_valid(t1, t2, t3):
    return is_croissant(t1, t2, t3)

def get_predictions(base_time, t1, t2, t3):
    add_base = timedelta(minutes=5, seconds=10)
    if has_above_50(t1, t2, t3) == 1:
        add_base = timedelta(minutes=6, seconds=10)
        second_pred = timedelta(minutes=7, seconds=10)
    else:
        second_pred = add_base + timedelta(minutes=1)
    return [base_time + add_base, base_time + second_pred]

if st.button("Prédire"):
    if tour1 and tour2 and tour3:
        try:
            t1, t2, t3 = float(tour1), float(tour2), float(tour3)
            base_time = datetime.now().replace(hour=heure, minute=minute, second=seconde, microsecond=0)
            predictions = get_predictions(base_time, t1, t2, t3)
            is_valid = prediction_valid(t1, t2, t3)

            for p in predictions:
                color = "red" if is_valid else "black"
                icon = "✅" if is_valid else "❌"
                st.markdown(f"<h3 style='color:{color}'>{icon} Prédiction : {p.strftime('%H:%M:%S')}</h3>", unsafe_allow_html=True)

            st.success("Analyse terminée !")
        except Exception as e:
            st.error("Erreur lors de l’analyse. Vérifiez vos entrées.")
    else:
        st.warning("Veuillez remplir tous les champs.")

# Bouton export (visualisation seulement)
st.download_button("Exporter le Résultat", data="Prediction Aviator", file_name="prediction.txt")
