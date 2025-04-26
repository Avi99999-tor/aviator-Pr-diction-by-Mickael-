import streamlit as st
import time

# Fonction pour calculer les prédictions
def calcul_prédiction(multiplicateur_1, multiplicateur_2, multiplicateur_3, heure_repere):
    # Logique de prédiction basée sur les conditions
    # Transformation des heures et minutes en format calculable
    heure, minute, seconde = map(int, heure_repere.split(':'))
    
    if multiplicateur_2 < 20:
        prediction_time = f"{heure}:{minute + 5}:{seconde + 10}"
        prediction_text = "Prédiction valide : X2, X3"
    elif multiplicateur_2 >= 20 and multiplicateur_2 < 40:
        prediction_time = f"{heure}:{minute + 6}:{seconde + 10}"
        prediction_text = "Prédiction valide : X2, X3"
    elif multiplicateur_1 >= 50 or multiplicateur_3 >= 50:
        prediction_time = f"{heure}:{minute + 7}:{seconde + 10}"
        prediction_text = "Prédiction spéciale : X5, X10"
    else:
        prediction_time = f"{heure}:{minute + 5}:{seconde + 10}"
        prediction_text = "Prédiction valide : X2, X3"
    
    return prediction_time, prediction_text

# Titre de l'app
st.title("Prédiction de Mickael - Aviator")

# Zone de saisie pour les multiplicateurs
multiplicateur_1 = st.number_input("Multiplicateur 1:", min_value=0.0, step=0.1)
multiplicateur_2 = st.number_input("Multiplicateur 2 (Repère):", min_value=0.0, step=0.1)
multiplicateur_3 = st.number_input("Multiplicateur 3:", min_value=0.0, step=0.1)

# Zone de saisie pour l'heure du multiplicateur
heure_repere = st.text_input("Entrer l'heure du multiplicateur (hh:mm:ss):", "10:23:31")

# Bouton de validation
if st.button("Valider la prédiction"):
    # Affichage du message d'attente
    with st.spinner("Prédiction en cours..."):
        time.sleep(2)  # Temps d'attente pour simuler le calcul
    
    # Calcul de la prédiction
    prediction_time, prediction_text = calcul_prédiction(multiplicateur_1, multiplicateur_2, multiplicateur_3, heure_repere)
    
    # Affichage des résultats
    st.success(f"Prédiction : {prediction_time}")
    st.write(prediction_text)
    st.write("Si la prédiction est incorrecte, mise sur le tour suivant X2, X5, X10")
    
    # Option de réinitialisation
    if st.button("Réinitialiser"):
        st.experimental_rerun()
