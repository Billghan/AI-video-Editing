import streamlit as st
import google.generativeai as genai
import moviepy.video.io.VideoFileClip as vf  # Modern çağırma yöntemi

st.set_page_config(page_title="AI Video Düzenleyici", page_icon="🎬")
st.title("🎬 AI Video Düzenleyici")

# API Anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Anahtarı eksik!")
    st.stop()

uploaded_file = st.file_uploader("Videonuzu yükleyin (MP4):", type=["mp4"])

if uploaded_file is not None:
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video("temp_input.mp4")

    if st.button("Düzenlemeye Başla"):
        with st.spinner('Video işleniyor...'):
            try:
                # Modern yöntemi kullanıyoruz
                clip = vf.VideoFileClip("temp_input.mp4")
                final = clip.subclip(0, 10)
                final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
                st.success("İşlem tamamlandı!")
                st.video("output.mp4")
            except Exception as e:
                st.error(f"Hata: {e}")
