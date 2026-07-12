import streamlit as st
import google.generativeai as genai
import moviepy.video.io.VideoFileClip as vf 

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici")

# API Anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Anahtarı eksik!")
    st.stop()

# Video Yükleme
uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])

# KOMUT YAZMA ALANI (Burayı ekledik)
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: 
