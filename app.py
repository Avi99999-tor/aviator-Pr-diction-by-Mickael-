import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Aviator ARIMA+ Strategy", layout="wide")
st.title("🚀 Aviator Predictor - ARIMA Boosted + Seed Strategy")
st.markdown("Intégrez vos 20 dernières multiplicateurs et obtenez des prédictions ARIMA améliorées avec logique de seed et alertes.")

# Input
data_input = st.text_area(
    "**Entrez jusqu'à 20 derniers multiplicateurs (ex: 1.87x 1.26x ...)**", height=100
)
last_t = st.number_input("Numéro de la dernière tour (ex: 32 si 1.87x est le T32)", min_value=1, value=1)

if data_input:
    # Parse
    try:
        raw = [float(x.replace('x','').replace('X','')) for x in data_input.split()]
        # trim to last 20
        hist = raw[-20:]
        if len(hist) < 5:
            st.error("Veuillez entrer au moins 5 valeurs pour la prédiction.")
        else:
            # ARIMA raw
            df = pd.Series(hist)
            model = ARIMA(df, order=(2,1,2))
            res = model.fit()
            raw_pred = res.forecast(steps=20)
            # Booster detection
            booster_count = sum(1 for v in hist if v >= 5)
            booster_factor = 1 + booster_count/10
            # Improved prediction
            improved = []
            np.random.seed(42)
            for i, val in enumerate(raw_pred, start=1):
                pred = round(val,2)
                # apply booster for next 3
                if i<=3 and booster_count>0:
                    pred *= booster_factor
                # decimal mod logic
                dec = int(str(pred).split('.')[-1]) % 10
                if dec in [0,8]:
                    # trap zone
                    pred = 1.00 + np.random.uniform(0,0.1)
                elif dec>=5:
                    pred += 0.3
                # add jitter
                pred += np.random.uniform(-0.1,0.1)
                improved.append(round(pred,2))
            # Display
            st.subheader("Prédictions T+1 à T+20")
            df_pred = pd.DataFrame({
                "Tour": [f"T{last_t+i}" for i in range(1,21)],
                "ARIMA_Raw": raw_pred.round(2).values,
                "ARIMA_Boosted": improved
            })
            st.dataframe(df_pred)
            # Strategy signals
            st.subheader("💡 Signaux de Stratégie")
            signals = []
            for idx, row in df_pred.iterrows():
                tour=row['Tour']; val=row['ARIMA_Boosted']; dec=int(str(val).split('.')[-1]) % 10
                signal=""
                if idx==4:
                    signal="Entry Mid-Range"
                if idx==5:
                    signal="Boost Probable"
                if idx==8:
                    signal="Take-Profit"
                if idx==9:
                    signal="Stop-Loss Alert"
                signals.append((tour, val, signal))
            df_sig=pd.DataFrame(signals, columns=["Tour","Pred","Signal"])            
            st.table(df_sig)
    except Exception as e:
        st.error(f"Erreur de parsing: {e}")
else:
    st.info("Entrez d'abord vos multiplicateurs.")
