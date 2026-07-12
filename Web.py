import streamlit as st
import google.generativeai as genai

# Sayfa başlığı
st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici")

# Secrets'tan API anahtarını al
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Settings -> Secrets kısmına GEMINI_API_KEY eklediğinden emin ol.")
    st.stop()

# Basit bir arayüz örneği
st.write("Hoş geldin! Videonla ilgili ne yapmak istediğini yaz.")
user_input = st.text_input("Komutunu buraya gir:")

if st.button("Düzenlemeye Başla"):
    if user_input:
        st.success(f"İşlem başlatılıyor: {user_input}")
        # Buraya Gemini model çağrılarını ekleyeceğiz
    else:
        st.warning("Lütfen bir komut gir.")
