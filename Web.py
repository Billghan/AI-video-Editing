import streamlit as st
import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import yt_dlp
import os

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

# 2. Müzik Yükleme
music_file = st.file_uploader("Arka plana eklemek için müzik/ses yükleyin:", type=["mp3", "wav", "ogg", "aac", "m4a"])

# 3. PROMPT KUTUSU GERİ GELDİ
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: İlk 10 saniyeyi al)")

# 4. İşlem
if st.button("Düzenlemeyi Başlat"):
    if not os.path.exists("input.mp4"):
        st.warning("Önce bir video hazırlayın!")
    elif not user_prompt:
        st.warning("Lütfen bir komut girin!")
    else:
        with st.spinner('Video işleniyor...'):
            try:
                video = VideoFileClip("input.mp4")
                
                # Müzik işlemleri
                if music_file is not None:
                    with open("temp_music_file", "wb") as f:
                        f.write(music_file.getbuffer())
                    audio_bg = AudioFileClip("temp_music_file").with_volume_scaled(0.2)
                    final_audio = CompositeAudioClip([video.audio.with_volume_scaled(0.5), audio_bg.with_duration(video.duration)])
                    video = video.with_audio(final_audio)
                
                # Çizim Fonksiyonu
                def apply_effects(get_frame, t):
                    frame = get_frame(t)
                    cv2.circle(frame, (640, 360), 100, (0, 0, 255), 5)
                    cv2.putText(frame, "Onemli An!", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    return frame

                final_clip = video.subclipped(0, 10).fl(apply_effects)
                final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
                
                st.success("İşlem tamamlandı!")
                st.video("final_video.mp4")
                
            except Exception as e:
                st.error(f"Hata: {e}")

# Çizim Fonksiyonu (Aynı kalıyor)
                def apply_effects(frame, t):
                    # Not: Transform fonksiyonu 'frame, t' sırasıyla alır
                    cv2.circle(frame, (640, 360), 100, (0, 0, 255), 5)
                    cv2.putText(frame, "Onemli An!", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    return frame

                # GÜNCEL KULLANIM:
                final_clip = video.subclipped(0, 10).transform(apply_effects)
