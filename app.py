import streamlit as st
import time

st.set_page_config(page_title="PREDICTION DE MICKAEL", page_icon=":rocket:", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #f0f8ff; }
        h1 { font-size: 40px; color: #4b0082; font-weight: bold; text-align: center; }
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 12px; padding: 10px; font-size: 18px; }
        .stButton>button:hover { background-color: #45a049; }
        .stTextInput input, .stNumberInput input { border: 1px solid #4CAF50; }
        .stForm label { font-size: 18px; }
        .stMarkdown { font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# Login
with st.form("login_form"):
    username = st.text_input("Nom utilisateur :")
    code = st.text_input("Code :", type="password")
    submit_button = st.form_submit_button("Se connecter")

if submit_button:
    if username == "Aviator26" and code == "288612bymicka":
        st.success("Connexion réussie !")

        st.title("PREDICTION DE MICKAEL")

        # Inputs
        st.subheader("Entrer les trois derniers multiplicateurs")
        multiplicateur1 = st.number_input("Multiplicateur 1 (après virgule)", min_value=0.00, format="%.2f")
        multiplicateur2 = st.number_input("Multiplicateur 2 - REPÈRE (après virgule)", min_value=0.00, format="%.2f")
        multiplicateur3 = st.number_input("Multiplicateur 3 (après virgule)", min_value=0.00, format="%.2f")

        st.subheader("Entrer l'heure du multiplicateur repère")
        heure = st.number_input("Heure :", min_value=0, max_value=23)
        minute = st.number_input("Minute :", min_value=0, max_value=59)
        seconde = st.number_input("Seconde :", min_value=0, max_value=59)

        if st.button("Prédire"):
            with st.spinner('Calcul de la prédiction en cours...'):
                time.sleep(2)

                # STRATEGIE
                prediction_valide = False
                heure_ajoutee = 0
                secondes_ajoutees = 10
                intervalle_special = False

                if multiplicateur2 < 20:
                    heure_ajoutee = 5
                elif 20 <= multiplicateur2 <= 39:
                    heure_ajoutee = 6

                # Vérifie condition multiplicateur1 > multiplicateur3
                if multiplicateur1 > multiplicateur3:
                    prediction_valide = True

                # Condition spéciale
                if multiplicateur1 >= 50 and multiplicateur3 >= 50:
                    intervalle_special = True
                elif multiplicateur1 >= 50 and multiplicateur3 < 50:
                    if 20 <= multiplicateur2 <= 39:
                        heure_ajoutee = 7

                # Calcul de la nouvelle heure
                total_seconds = (heure * 3600) + (minute * 60) + seconde
                total_seconds += (heure_ajoutee * 60) + secondes_ajoutees

                new_hour = (total_seconds // 3600) % 24
                new_minute = (total_seconds % 3600) // 60
                new_second = (total_seconds % 60)

                # Résultats
                st.markdown("---")
                if prediction_valide:
                    if intervalle_special:
                        st.success(f"**Intervalle spécial : {new_hour:02.0f}h{new_minute:02.0f}min{new_second:02.0f}sec à {(new_minute+1)%60:02.0f}min{new_second:02.0f}sec X5 ou X10**")
                    else:
                        st.success(f"**Prochaine prédiction à : {new_hour:02.0f}h{new_minute:02.0f}min{new_second:02.0f}sec X2 ou X3**")
                        st.warning("Si la prédiction est incorrecte, entrer dans le tour suivant avec X2, X5, X10.")
                else:
                    st.error("Prédiction invalide - Vérifiez les valeurs ou attendez une autre opportunité.")

                if st.button("Réinitialiser"):
                    st.experimental_rerun()

    else:
        st.error("Nom utilisateur ou code incorrect.")
