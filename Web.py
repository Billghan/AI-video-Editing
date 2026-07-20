import analiz
import işlem
import streamlit as st
import json
import yt_dlp # Linkten indirmek için bu kütüphaneyi kullanacağız
from moviepy import VideoFileClip

# --- 1. GİRİŞ KORUMASI ---
def check_password():
    password = st.sidebar.text_input("Şifre:", type="password")
    if password == "9Z!8W3M!!wWc8N75y4nZ":
        return True
    return False

if not check_password():
    st.warning("Lütfen giriş yapın.")
    st.stop()

# --- 2. YÖNETMEN PANELİ ---
st.title("🎬 PreBGlobal - Yönetmen Paneli")

# Mod Seçimi
mod = st.sidebar.radio("İşlem Modu:", ["Analiz", "Kurgu"], key="ana_mod")

if mod == "Analiz":
    st.subheader("🔍 1. Adım: Videoyu Analiz Et")
    # Dosya yükleyici yerine URL girişi
    video_url = st.text_input("Videonun URL adresini girin:", key="video_url")
    user_prompt = st.text_input("Gemini'ye neyi bulsun?", key="analiz_prompt")
    
    if st.button("Analizi Başlat", key="analiz_btn"):
        if video_url:
            st.write(f"Sistem '{video_url}' adresinden videoyu alıyor...")
            # Burada yt_dlp ile indirme başlatılacak
        else:
            st.error("Lütfen önce geçerli bir video linki girin.")

elif mod == "Kurgu":
    st.subheader("🛠️ 2. Adım: Kurgu Fabrikası")
    
    if st.button("Kurguyu Uygula", key="kurgu_btn"):
        st.write("Video işleniyor, lütfen bekleyin...")
