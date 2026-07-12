import streamlit as st
import google.generativeai as genai
from moviepy.editor import VideoFileClip
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici")

# API Anahtarını al
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Secrets ayarlarında GEMINI_API_KEY bulunamadı.")
    st.stop()

# Video Yükleme
uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])

if uploaded_file is not None:
    # Geçici dosyaya yaz
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_input.mp4")

    if st.button("Düzenlemeye Başla"):
        with st.spinner('Video işleniyor...'):
            try:
                # Videoyu MoviePy ile aç ve ilk 10 saniyeyi kırp
                clip = VideoFileClip("temp_input.mp4")
                final = clip.subclip(0, 10)
                final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
                
                st.success("İşlem tamamlandı!")
                st.video("output.mp4")
            except Exception as e:
                st.error(f"Hata: {e}")
