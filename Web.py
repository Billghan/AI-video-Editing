import streamlit as st
import cv2
import numpy as np
from moviepy.editor import *

def add_circle_and_text(frame):
    # Daire çiz (Örn: Ekranın ortasına)
    cv2.circle(frame, (640, 360), 100, (0, 0, 255), 5)
    # Altyazı ekle
    cv2.putText(frame, "Buraya Dikkat!", (500, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame

# Video işleme kısmı
if st.button("Düzenlemeyi Başlat"):
    video = VideoFileClip("input.mp4")
    
    # 1. Müziğin sesini kıs (volumex ile)
    if music_file is not None:
        audio = AudioFileClip("temp_music_file").volumex(0.2)
        video = video.set_audio(CompositeAudioClip([video.audio.volumex(0.5), audio]))

    # 2. Görüntüye efekt ekle (fl_image ile her kareyi değiştiriyoruz)
    final_video = video.fl_image(add_circle_and_text)
    
    final_video.write_videofile("final.mp4", codec="libx264")
    st.video("final.mp4")
