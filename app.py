import streamlit as st from datetime import datetime, timedelta

--- LOGIN PAGE ---

def login_page(): st.title("PREDICTION DE MICKAEL") st.subheader("Connexion")

username = st.text_input("Nom d'utilisateur")
password = st.text_input("Code", type="password")

if st.button("Se connecter"):
    if username == "Aviator26" and password == "288612bymicka":
        st.session_state['logged_in'] = True
        st.experimental_rerun()
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect")

--- PREDICTION PAGE ---

def prediction_page(): st.title("Entrez les données pour la prédiction")

col1, col2, col3 = st.columns(3)
with col1:
    multiplicateur1 = st.number_input("Multiplicateur 1", min_value=0.0, step=0.01)
with col2:
    multiplicateur2 = st.number_input("Multiplicateur 2 (Repère)", min_value=0.0, step=0.01)
with col3:
    multiplicateur3 = st.number_input("Multiplicateur 3", min_value=0.0, step=0.01)

st.write("\n**Entrez l'heure du multiplicateur repère**")
heure = st.number_input("Heure", min_value=0)
minute = st.number_input("Minute", min_value=0)
seconde = st.number_input("Seconde", min_value=0)

if st.button("Valider les données"):
    process_prediction(multiplicateur1, multiplicateur2, multiplicateur3, heure, minute, seconde)

if st.button("Réinitialiser"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

--- PROCESSING PAGE ---

def process_prediction(m1, m2, m3, h, m, s): st.title("Résultat de la Prédiction")

heure_repere = datetime(2024,1,1,h,m,s)
resultat = ""

# Stratégie temps
if 0 <= m2 < 20:
    base_minute = 5
elif 20 <= m2 <= 39:
    base_minute = 6
else:
    base_minute = 7

# Condition Special
special = False
if m1 >= 50 and m3 >= 50:
    special = True
elif m1 >= 50 and m3 < 50 and 20 <= m2 <= 39:
    base_minute = 7

# Calcul du temps
prediction_time = heure_repere + timedelta(minutes=base_minute, seconds=10)

# Affichage
if special:
    st.success(f"Prediction Speciale entre {prediction_time.strftime('%H:%M:%S')} et {(prediction_time + timedelta(minutes=1)).strftime('%H:%M:%S')} : X5 ou X10")
    st.warning("Attention : Intervalle special pour X5 et X10")
else:
    st.success(f"Prochaine prediction à {prediction_time.strftime('%H:%M:%S')} : X2 ou X3")

# Avertissement
if m1 >= 50 or m2 >= 50 or m3 >= 50:
    st.error("ATTENTION : Présence d'un X50 ou double rose - Prédiction risquée")

--- MAIN ---

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']: login_page() else: prediction_page()

