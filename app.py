import streamlit as st
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="MOD10 Matches Analyzer", page_icon="⚽", layout="centered")

st.title("MOD10 Matches Analyzer ⚽")
st.write("Upload capture(s) and analyze Over/Under MOD10 patterns.")

uploaded_files = st.file_uploader("Upload image(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

def extract_cotes(text):
    import re
    # Maka cotes Over/Under: ohatra "Over 1.17", "Under 2.33"
    pattern = r'(Over|Under)\s+(\d+\.\d+)'
    return re.findall(pattern, text)

def mod10_from_cote(cote):
    # Maka décimale (ohatra 1.17 → 17) dia mod10
    dec = str(cote).split('.')[-1]
    if dec.isdigit():
        return int(dec) % 10
    return None

if uploaded_files:
    for idx, file in enumerate(uploaded_files):
        st.header(f"Sary {idx+1}: {file.name}")
        image = Image.open(file)
        st.image(image, width=300)
        # OCR
        text = pytesseract.image_to_string(image, lang='eng')
        st.text_area("OCR Result", text, height=120)
        cotes = extract_cotes(text)
        if cotes:
            st.write("### Cotes Over/Under & MOD10")
            for kind, cote in cotes:
                mod10 = mod10_from_cote(cote)
                st.write(f"{kind} {cote} → décimale: {str(cote).split('.')[-1]} → MOD10: **{mod10}**")
        else:
            st.warning("Tsy nahita cote Over/Under")
