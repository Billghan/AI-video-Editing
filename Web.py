import streamlit as st
import cv2
import os
import google.generativeai as genai
from moviepy.video.io.VideoFileClip import VideoFileClip
from functools import partial

# Gemini Konfigürasyonu
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_important_seconds(video_path, prompt):
    """Videoyu analiz edip önemli anların listesini döner."""
    video = VideoFileClip(video_path)
    important_seconds = []
    
    # Her 2 saniyede bir analiz yap (Hız için)
    for t in range(0, int(video.duration), 2):
        frame = video.get_frame(t)
        cv2.imwrite("temp.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        sample_file = genai.upload_file("temp.jpg")
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([sample_file, f"Bu görüntüde '{prompt}' ile ilgili önemli bir an var mı? Sadece EVET veya HAYIR de."])
        
        if "EVET" in response.text.upper():
            important_seconds.append(t)
            
    return important_seconds

def apply_smart_effects(get_frame, t, important_seconds):
    frame = get_frame(t)
    # Eğer o an önemli anlar listesindeyse efekt ekle
    if any(abs(t - sec) < 1 for sec in important_seconds):
        cv2.circle(frame, (640, 360), 100, (0, 0, 255), 5)
        cv2.putText(frame, "ONEMLI AN!", (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame

# --- BUTON İÇİ ---
if st.button("Akıllı Düzenlemeyi Başlat"):
    # 1. Önce Analiz
    st.write("Video analiz ediliyor, lütfen bekle...")
    important_moments = get_important_seconds("input.mp4", user_prompt)
    
    # 2. Sonra Render
    video = VideoFileClip("input.mp4")
    processed_func = partial(apply_smart_effects, important_seconds=important_moments)
    final_clip = video.transform(processed_func)
    
    final_clip.write_videofile("final_video.mp4")
    st.video("final_video.mp4")
