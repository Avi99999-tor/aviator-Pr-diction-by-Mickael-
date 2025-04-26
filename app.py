import streamlit as st
from datetime import datetime, timedelta

# LOGIN
def check_login(username, password):
    return username == "Aviator26" and password == "288612bymicka"

# STRATEGIE
def get_prediction(m1, m2, m3, heure):
    valid = m1 > m3

    # Prendre uniquement les chiffres après la virgule
    after_virg_1 = int(str(m1).split('.')[-1])
    after_virg_2 = int(str(m2).split('.')[-1])
    after_virg_3 = int(str(m3).split('.')[-1])

    t_base = heure
    temps_ajoute = timedelta()

    # Déterminer le temps de prédiction
    if 0 <= after_virg_2 <= 19:
        temps_ajoute = timedelta(minutes=5, seconds=10)
    elif 20 <= after_virg_2 <= 39:
        if any(x >= 50 for x in [after_virg_1, after_virg_2, after_virg_3]) and len(
            [x for x in [after_virg_1, after_virg_2, after_virg_3] if x >= 50]) == 1:
            temps_ajoute = timedelta(minutes=7, seconds=10)
        else:
            temps_ajoute = timedelta(minutes=6, seconds=10)
    elif 10 <= after_virg_2 <= 19:
        temps_ajoute = timedelta(minutes=5, seconds=10)

    heure_prediction = t_base + temps_ajoute

    # Condition spéciale
    special_case = after_virg_1 > 50 and after_virg_2 > 50

    return valid, heure_prediction.time(), special_case

# APP
def main():
    st.set_page_config(page_title="PREDICTION DE MICKAEL - Top Exacte", layout="centered")
    st.title("PREDICTION DE MICKAEL - Top Exacte")

    # Login
    if "authenticated" not in st.session_state:
        username = st.text_input("Nom utilisateur")
        password = st.text_input("Code", type="password")
        if st.button("Se connecter"):
            if check_login(username, password):
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Nom d'utilisateur ou code incorrect.")
        return

    # Input
    st.subheader("Entrer les trois derniers multiplicateurs")
    m1 = st.number_input("Multiplicateur 1", format="%.2f")
    m2 = st.number_input("Multiplicateur 2 (repère)", format="%.2f")
    m3 = st.number_input("Multiplicateur 3", format="%.2f")

    st.subheader("Entrer l'heure du multiplicateur repère")
    heure = st.time_input("Heure (hh:mm:ss)")

    if st.button("Valider la prédiction"):
        heure_obj = datetime.combine(datetime.today(), heure)
        valid, result_time, special = get_prediction(m1, m2, m3, heure_obj)

        st.subheader("Résultat de la prédiction")

        if valid:
            st.success(f"Heure prédite : {result_time} | Résultat attendu : X2 ou X3")
            if special:
                st.info("Cas spécial détecté : X5 ou X10 probable pendant cette période.")
        else:
            st.warning(f"Prédiction invalide : condition non respectée.")
            st.text("Si la prédiction est incorrecte, miser sur le tour suivant : X2, X5 ou X10.")

if __name__ == "__main__":
    main()
