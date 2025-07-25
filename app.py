import streamlit as st
from PIL import Image
import pytesseract
import re

# --- Functions ---

# Extract decimal part and compute mod 10
def extract_mod10(odd_str):
    match = re.search(r"\d+\.(\d+)", odd_str)
    if match:
        decimal = match.group(1)
        return int(decimal) % 10
    return None

# Process image and return OCR text & mod10 value
def process_image_mod10(image):
    text = pytesseract.image_to_string(image)
    odds = re.findall(r"\d+\.\d+", text)
    if len(odds) >= 2:
        mod_over = extract_mod10(odds[0])
        mod_under = extract_mod10(odds[1])
        if mod_over is not None and mod_under is not None:
            mod_total = int(f"{mod_over}{mod_under}")
            return mod_over, mod_under, mod_total, text
    return None, None, None, text

# --- Streamlit UI ---

st.set_page_config(page_title="MOD10 OCR Comparator", layout="centered")
st.title("🎯 MOD10 Match Pattern Detector")
st.markdown("Téléverser deux captures d’écran avec les cotes Over 1.5 / Under 1.5 pour deux matchs virtuels.")

col1, col2 = st.columns(2)

with col1:
    img1 = st.file_uploader("📥 Capture Match 1", type=["png", "jpg", "jpeg"], key="m1")
with col2:
    img2 = st.file_uploader("📥 Capture Match 2", type=["png", "jpg", "jpeg"], key="m2")

if img1 and img2:
    st.markdown("## 🔍 Résultats OCR & Mod10")
    over1, under1, mod1, text1 = process_image_mod10(Image.open(img1))
    over2, under2, mod2, text2 = process_image_mod10(Image.open(img2))

    if mod1 is not None and mod2 is not None:
        st.markdown("### 📄 Match 1")
        st.code(text1)
        st.write(f"➡️ Over mod10: {over1}, Under mod10: {under1}, Total: **{mod1}**")

        st.markdown("### 📄 Match 2")
        st.code(text2)
        st.write(f"➡️ Over mod10: {over2}, Under mod10: {under2}, Total: **{mod2}**")

        # Check for match or ±1 similarity
        if mod1 == mod2:
            st.success(f"✅ Matchs identiques — Résultat MOD10: {mod1}")
        elif abs(mod1 - mod2) == 1:
            st.warning(f"⚠️ Matchs similaires (écart ±1) — {mod1} vs {mod2}")
        else:
            st.error(f"❌ Aucune correspondance MOD10 — {mod1} ≠ {mod2}")
    else:
        st.warning("⚠️ OCR n'a pas pu extraire correctement les cotes. Vérifiez les images.")
else:
    st.info("🕐 En attente des deux captures pour lancer l’analyse...")
