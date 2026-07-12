import streamlit as st
import google.generativeai as genai
import moviepy.video.io.VideoFileClip as vf 

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici")

# API Anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Anahtarı eksik!")
    st.stop()

# Video Yükleme
uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])

# KOMUT YAZMA ALANI (Burayı ekledik)
user_prompt = st.text_input("Videonla ilgili ne yapmak istiyorsun? (Örn: İlk 10 saniyeyi al):")

if uploaded_file is not None:
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video("temp_input.mp4")

    if st.button("Düzenlemeye Başla"):
        if not user_prompt:
            st.warning("Lütfen bir komut gir!")
        else:
            with st.spinner('Video işleniyor...'):
                try:
                    clip = vf.VideoFileClip("temp_input.mp4")
                    # Şimdilik sadece örnek bir kesme yapıyoruz
                    final = clip.subclip(0, 10)
                    final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
                    st.success("İşlem tamamlandı!")
                    st.video("output.mp4")
                except Exception as e:
                    st.error(f"Hata: {e}")
