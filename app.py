import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Prédiction by Mickael", page_icon="⚡")

# --- TITRE & LOGIN ---
st.title("PREDICTION DE MICKAEL - Top Exacte")

with st.expander("Connexion"):
    user = st.text_input("Nom utilisateur")
    code = st.text_input("Code", type="password")
    if user != "Aviator26" or code != "288612bymicka":
        st.warning("Nom ou code incorrect.")
        st.stop()

# --- FORMULAIRE ---
st.subheader("Entrer les 3 derniers multiplicateurs")

col1, col2, col3 = st.columns(3)
with col1:
    m1 = st.number_input("Multiplicateur 1", min_value=0.00, step=0.01, format="%.2f")
with col2:
    m2 = st.number_input("Multiplicateur 2 (repère)", min_value=0.00, step=0.01, format="%.2f")
with col3:
    m3 = st.number_input("Multiplicateur 3", min_value=0.00, step=0.01, format="%.2f")

st.subheader("Entrer l'heure du multiplicateur repère")

h = st.number_input("Heure", min_value=0, max_value=23, step=1)
mn = st.number_input("Minute", min_value=0, max_value=59, step=1)
s = st.number_input("Seconde", min_value=0, max_value=59, step=1)

# --- PRÉDICTION ---
if st.button("Valider la prédiction"):

    def get_prediction_time(rep_val, base_time):
        if rep_val < 20:
            return base_time + timedelta(minutes=5, seconds=10)
        elif rep_val < 40:
            return base_time + timedelta(minutes=6, seconds=10)
        else:
            return base_time + timedelta(minutes=6, seconds=10)

    def get_special_time(rep_val, base_time):
        if rep_val < 20:
            start = base_time + timedelta(minutes=5, seconds=10)
        else:
            start = base_time + timedelta(minutes=6, seconds=10)
        end = start + timedelta(minutes=1)
        return start, end

    rep_val = int(round((m2 % 1) * 100))
    base_time = datetime(2023, 1, 1, h, mn, s)

    condition1 = m1 > m3
    special_pred = False

    if m1 >= 50 and m3 >= 50:
        special_pred = True
        start, end = get_special_time(rep_val, base_time)
    elif m1 >= 50:
        if rep_val < 20:
            prediction_time = base_time + timedelta(minutes=6, seconds=10)
        else:
            prediction_time = base_time + timedelta(minutes=7, seconds=10)
    else:
        prediction_time = get_prediction_time(rep_val, base_time)

    # --- AFFICHAGE ---
    st.markdown("---")
    if special_pred:
        st.success(f"**PRÉDICTION SPÉCIALE : X5 X10**")
        st.write(f"Heure : **{start.time()} à {end.time()}**")
        st.info("Si la prédiction est incorrecte, miser X2 X5 X10 au tour suivant")
    elif condition1:
        st.success(f"**PRÉDICTION : X2 X3**")
        st.write(f"Heure : **{prediction_time.time()}**")
        st.info("Si la prédiction est incorrecte, miser X2 X5 X10 au tour suivant")
    else:
        st.error("Prédiction non valide (Multiplicateur 1 doit être supérieur au 3)")
