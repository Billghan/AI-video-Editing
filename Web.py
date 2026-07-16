import streamlit as st
import cv2
import json
from functools import partial
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

# Mod Seçimi (Tek bir tane olmalı)
mod = st.sidebar.radio("İşlem Modu:", ["Analiz", "Kurgu"], key="ana_mod")

if mod == "Analiz":
    st.subheader("🔍 1. Adım: Videoyu Analiz Et")
    uploaded_file = st.file_uploader("Ham videoyu yükle", type=["mp4"])
    user_prompt = st.text_input("Gemini'ye neyi bulsun?", key="analiz_prompt")
    
    # Butonu sadece burada bir kez tanımlıyoruz
    if st.button("Analizi Başlat", key="analiz_btn"):
        if uploaded_file is not None:
            st.write("Gemini analiz ediyor... (plan.json hazırlanıyor)")
        else:
            st.error("Lütfen önce bir video yükle.")

elif mod == "Kurgu":
    st.subheader("🛠️ 2. Adım: Kurgu Fabrikası")
    
    # Butonu sadece burada bir kez tanımlıyoruz
    if st.button("Kurguyu Uygula", key="kurgu_btn"):
        st.write("Video işleniyor, lütfen bekleyin...")
