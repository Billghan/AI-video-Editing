import streamlit as st
import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import yt_dlp
import os

# moviepy v2.0+ uyumlu transform fonksiyonu
def apply_effects(get_frame, t):
    frame = get_frame(t)
    new_frame = frame.copy()
    cv2.circle(new_frame, (640, 360), 100, (0, 0, 255), 5)
    cv2.putText(new_frame, "Onemli An!", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return new_frame

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici - Pro Sürüm")

# 1. GİRİŞLER (Buraya prompt ekledik)
option = st.radio("İçerik kaynağını seç:", ("Bilgisayardan Yükle", "YouTube Linki"))
user_prompt = st.text_input("Düzenleme için prompt gir (Örn: 'Videonun ortasına daire ekle'):")
music_file = st.file_uploader("Bir müzik dosyası yükle (MP3/WAV)", type=["mp3", "wav"])

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
                        
                        if video.audio is not None:
                            video_audio = video.audio.with_volume_scaled(0.5)
                            final_audio = CompositeAudioClip([video_audio, audio_bg.with_duration(video.duration)])
                        else:
                            final_audio = audio_bg.with_duration(video.duration)
                        video = video.with_audio(final_audio)
                    
                    # DÖNÜŞÜM (Hizalaması 'try' ile aynı seviyede, 'except'in üzerinde)
                    final_clip = video.transform(lambda gf, t: apply_effects(gf, t, user_prompt))
                    final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
                    
                    st.success(f"İşlem tamamlandı! Promptunuz: {user_prompt}")
                    st.video("final_video.mp4")
                    
                except Exception as e: # TRY'IN TAM ALTINDA OLMALI
                    st.error(f"Hata: {e}")
                    
# Fonksiyonu artık prompt'u da alacak şekilde güncelliyoruz
def apply_effects(get_frame, t, prompt_text=""):
    frame = get_frame(t)
    new_frame = frame.copy()
    
    # Eğer kullanıcı "daire" yazdıysa daireyi çiz
    if "daire" in prompt_text.lower():
        cv2.circle(new_frame, (640, 360), 100, (0, 0, 255), 5)
    
    # Eğer kullanıcı "yazı" yazdıysa metni yaz
    if "yazı" in prompt_text.lower():
        cv2.putText(new_frame, "AI Video", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    return new_frame
