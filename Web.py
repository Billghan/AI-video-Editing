import streamlit as st
import google.generativeai as genai
import moviepy.video.io.VideoFileClip as vf
import yt_dlp
import os

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici - YouTube Destekli")

# API Anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Anahtarı eksik!")
    st.stop()

# Video Kaynağı Seçimi
option = st.radio("İçerik kaynağını seç:", ("Bilgisayardan Yükle", "YouTube Linki"))

if option == "Bilgisayardan Yükle":
    uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])
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

# Düzenleme Komutu
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: İlk 10 saniyeyi al)")

if st.button("Düzenlemeye Başla"):
    if not os.path.exists("input.mp4"):
        st.warning("Lütfen önce bir video yükleyin veya indirin.")
    elif not user_prompt:
        st.warning("Lütfen bir komut girin!")
    else:
        with st.spinner('Video işleniyor...'):
            try:
                clip = vf.VideoFileClip("input.mp4")
                # Basit örnek
                final = clip.subclip(0, 10) 
                final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
                st.success("İşlem tamamlandı!")
                st.video("output.mp4")
            except Exception as e:
                st.error(f"Hata: {e}")

# ... (Üstteki kodların aynısı kalıyor)

# MÜZİK YÜKLEME ALANI
music_file = st.file_uploader("Arka plana eklemek için bir müzik yükleyin (MP3):", type=["mp3"])

if st.button("Müzik ve Videoyu Birleştir"):
    if not os.path.exists("input.mp4"):
        st.warning("Lütfen önce video yükleyin!")
    elif music_file is None:
        st.warning("Lütfen bir müzik dosyası seçin!")
    else:
        with st.spinner('Müzik videoya ekleniyor...'):
            # Video ve Müziği Yükle
            video_clip = vf.VideoFileClip("input.mp4")
            audio_clip = vf.AudioFileClip(music_file)
            
            # Müziği videonun uzunluğuna eşitle (loop et veya kırp)
            # Burada sadece basit bir eşitleme yapıyoruz
            final_audio = audio_clip.subclip(0, video_clip.duration)
            
            # Sesi videoya ata
            final_video = video_clip.set_audio(final_audio)
            
            # Kaydet
            final_video.write_videofile("output_music.mp4", codec="libx264", audio_codec="aac")
            st.success("İşlem tamamlandı!")
            st.video("output_music.mp4")
