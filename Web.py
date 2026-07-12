import streamlit as st
import moviepy.video.io.VideoFileClip as vf
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
import yt_dlp
import os

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici - Pro Sürüm")

# Video Kaynağı
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

# MÜZİK YÜKLEME
music_file = st.file_uploader("Arka plana eklemek için müzik/ses yükleyin:", type=["mp3", "wav", "ogg", "aac", "m4a"])

# --- İŞTE PROMPT YAZMA YERİ BURADA ---
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: İlk 15 saniyeyi kes)")

if st.button("Düzenlemeye Başla"):
    if not os.path.exists("input.mp4"):
        st.warning("Önce bir video hazırlayın!")
    elif not user_prompt:
        st.warning("Lütfen bir komut girin!")
    else:
        with st.spinner('Video işleniyor...'):
            try:
                video = vf.VideoFileClip("input.mp4")
                
                if music_file is not None:
                    with open("temp_music_file", "wb") as f:
                        f.write(music_file.getbuffer())
                    
                    audio_bg = AudioFileClip("temp_music_file")
                    audio_bg = audio_bg.with_volume_scaled(0.3)
                    
                    final_audio = CompositeAudioClip([video.audio, audio_bg.with_duration(video.duration)])
                    video = video.with_audio(final_audio)
                
            # ... diğer kodlar ...
                
                # Güncellenmiş satır: .subclipped kullanıyoruz
                final = video.subclipped(0, 10) 
                final.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
                
                st.success("İşlem tamamlandı!")
                st.video("final_video.mp4")
                
            except Exception as e:
                st.error(f"Hata: {e}")
