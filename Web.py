import streamlit as st
import google.generativeai as genai
import moviepy.video.io.VideoFileClip as vf
import yt_dlp
import os

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici - YouTube Destekli")

# API Anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Anahtarı eksik!")
    st.stop()

# Video Kaynağı Seçimi
option = st.radio("İçerik kaynağını seç:", ("Bilgisayardan Yükle", "YouTube Linki"))

if option == "Bilgisayardan Yükle":
    uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])
    if uploaded_file is not None:
        with open("input.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.video("input.mp4")
else:
    youtube_url = st.text_input("YouTube linkini yapıştırın:")
    if st.button("YouTube Videosunu İndir"):
        with st.spinner('YouTube videosu indiriliyor...'):
            ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            st.success("Video başarıyla indirildi!")
            st.video("input.mp4")

# Düzenleme Komutu
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: İlk 10 saniyeyi al)")

if st.button("Düzenlemeye Başla"):
    if not os.path.exists("input.mp4"):
        st.warning("Lütfen önce bir video yükleyin veya indirin.")
    elif not user_prompt:
        st.warning("Lütfen bir komut girin!")
    else:
        with st.spinner('Video işleniyor...'):
            try:
                clip = vf.VideoFileClip("input.mp4")
                # Basit örnek
                final = clip.subclip(0, 10) 
                final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
                st.success("İşlem tamamlandı!")
                st.video("output.mp4")
            except Exception as e:
                st.error(f"Hata: {e}")
