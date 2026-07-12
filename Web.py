import streamlit as st
import numpy as np
import cv2
import os
import google.generativeai as genai
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from functools import partial
import yt_dlp

# --- KONFİGÜRASYON ---
# Streamlit'in sol altındaki Manage App -> Secrets kısmına GOOGLE_API_KEY ekle!
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def analyze_frame_with_gemini(frame):
    """Her kareyi Gemini'ye gönderip önemli bir olay var mı diye soruyoruz."""
    # Görüntüyü geçici olarak kaydet
    cv2.imwrite("temp_frame.jpg", frame)
    sample_file = genai.upload_file("temp_frame.jpg")
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([sample_file, "Bu oyun görüntüsünde önemli bir aksiyon (düşman, hamle, yazı) var mı? Varsa 'EVET' de ve kısaca ne olduğunu söyle, yoksa 'HAYIR' de."])
    
    return response.text

def apply_effects(get_frame, t, user_prompt):
    frame = get_frame(t)
    # Analiz fonksiyonunu her 30 karede bir çalıştır (performans için)
    if int(t * 30) % 30 == 0: 
        analysis = analyze_frame_with_gemini(frame)
        if "EVET" in analysis.upper():
            cv2.circle(frame, (640, 360), 100, (0, 0, 255), 5)
            cv2.putText(frame, "ONEMLI AN!", (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame

# --- ARAYÜZ (Aynı kalabilir, sadece buton içini değiştiriyoruz) ---
st.title("🎬 AI Akıllı Video Editör")
user_prompt = st.text_input("Ne tür anları yakalayalım? (Örn: 'Satranç hamlesi', 'PUBG çatışma')")

if st.button("Akıllı Düzenlemeyi Başlat"):
    # ... (Dosya yükleme ve indirme kısımları aynı kalacak) ...
    video = VideoFileClip("input.mp4")
    # Akıllı dönüştürme
    processed_func = partial(apply_effects, user_prompt=user_prompt)
    final_clip = video.transform(processed_func)
    final_clip.write_videofile("final_video.mp4")
    st.video("final_video.mp4")
