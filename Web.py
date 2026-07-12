import streamlit as st
import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import yt_dlp
import os

# --- FONKSİYON EN ÜSTTE TANIMLANDI ---
def apply_effects(frame):
    # Çerçeveyi kopyalıyoruz (cv2'nin hata vermemesi için gerekli)
    new_frame = frame.copy()
    # Daire çiz
    cv2.circle(new_frame, (640, 360), 100, (0, 0, 255), 5)
    # Metin yaz
    cv2.putText(new_frame, "Onemli An!", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return new_frame

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici - Pro Sürüm")

# 1. Video Kaynağı
option = st.radio("İçerik kaynağını seç:", ("Bilgisayardan Yükle", "YouTube Linki"))

if option == "Bilgisayardan Yükle":
    uploaded_file = st.file_uploader("Videonuzu yükleyin:", type=["mp4"])
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

# 2. Müzik
music_file = st.file_uploader("Arka plana eklemek için müzik/ses yükleyin:", type=["mp3", "wav", "ogg", "aac", "m4a"])
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun?")

# 3. İşlem
if st.button("Düzenlemeyi Başlat"):
    if not os.path.exists("input.mp4"):
        st.warning("Önce bir video hazırlayın!")
    else:
        with st.spinner('Video işleniyor...'):
            try:
                video = VideoFileClip("input.mp4")
                
                # Müzik ekleme
                if music_file is not None:
                    with open("temp_music_file", "wb") as f:
                        f.write(music_file.getbuffer())
                    audio_bg = AudioFileClip("temp_music_file").with_volume_scaled(0.2)
                    final_audio = CompositeAudioClip([video.audio.with_volume_scaled(0.5), audio_bg.with_duration(video.duration)])
                    video = video.with_audio(final_audio)
                
                # GÜNCEL TRANSFORMATION
                # 'transform' artık sadece 'frame' alır, 't' parametresine gerek yok
                final_clip = video.subclipped(0, 10).transform(apply_effects)
                
                final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
                st.success("İşlem tamamlandı!")
                st.video("final_video.mp4")
            except Exception as e:
                st.error(f"Hata: {e}")


def apply_effects(frame, *args):
    # *args, gönderilen diğer tüm parametreleri (t gibi) yutar ve hatayı yok eder
    new_frame = frame.copy()
    
    # Daire ve yazı çizimi
    cv2.circle(new_frame, (640, 360), 100, (0, 0, 255), 5)
    cv2.putText(new_frame, "Onemli An!", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return new_frame
