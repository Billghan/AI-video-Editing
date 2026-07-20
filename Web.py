import streamlit as st
import json
import yt_dlp
from moviepy import VideoFileClip
# Modülleri en tepede bağlıyoruz
import analiz
import işlem

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
    video_url = st.text_input("Videonun URL adresini girin:", key="video_url")
    user_prompt = st.text_input("Gemini'ye neyi bulsun?", key="analiz_prompt")
    
    if st.button("Analizi Başlat", key="analiz_btn"):
        if video_url:
            with st.spinner("Video analiz ediliyor..."):
                # analiz.py içindeki fonksiyon çağrıldı
                sonuc = analiz.analiz_et(video_url, user_prompt)
                st.json(sonuc)
                st.session_state['analiz_sonucu'] = sonuc
                st.success("Analiz tamamlandı!")
        else:
            st.error("Lütfen önce geçerli bir video linki girin.")

elif mod == "Kurgu":
    st.subheader("🛠️ 2. Adım: Kurgu Fabrikası")
    
    if st.button("Kurguyu Uygula", key="kurgu_btn"):
        if 'analiz_sonucu' in st.session_state:
            with st.spinner("Kurgu yapılıyor, lütfen bekleyin..."):
                # işlem.py içindeki fonksiyon çağrıldı
                # Buraya video indirme kodunu da entegre edeceğiz
                cikti = işlem.kurgula("temp_video.mp4", st.session_state['analiz_sonucu'])
                st.success(f"Video hazır: {cikti}")
        else:
            st.error("Önce Analiz modundan bir plan oluşturmalısın!")
