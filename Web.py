import streamlit as st
import os
import json
import re
import time
from moviepy import VideoFileClip, concatenate_videoclips
from google import genai

# Streamlit'in güvenli kasasından bilgileri çekiyoruz
# Bu bilgiler kodun içinde yazmaz, GitHub'da görünmez!
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    APP_PASSWORD = st.secrets["APP_PASSWORD"]
except Exception as e:
    st.error("Secrets (Kasa) ayarları yapılandırılmamış! Lütfen Streamlit ayarlarından ekleyin.")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.title("Web.py - AI Video Kurgu İstasyonu")

# Şifre girişi
password = st.text_input("Giriş Şifresi:", type="password")

if password == APP_PASSWORD:
    st.success("Güvenli Giriş Başarılı!")
    
    # Prompt alanı
    user_prompt = st.text_area("Gemini için Komutunu Gir:", 
                               "Videodaki en önemli 3 anı saniye olarak bul. Sadece JSON ver: [{\"start\": 0, \"end\": 10}]")
    
    video_file = st.file_uploader("Video Dosyası Yükle", type=["mp4", "mov"])

    if video_file is not None and st.button("Düzenlemeyi Başlat"):
        temp_path = f"temp_{video_file.name}"
        with open(temp_path, "wb") as f:
            f.write(video_file.read())
        
        st.info("İşlem başladı, Gemini analiz ediyor...")
        
        try:
            # Gemini Analiz
            uploaded_file = client.files.upload(file=temp_path)
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(2)
                uploaded_file = client.files.get(name=uploaded_file.name)
            
            response = client.models.generate_content(model="gemini-3.5-flash", contents=[uploaded_file, user_prompt])
            
            # Kurgu mantığı
            match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if match:
                kesim_noktalari = json.loads(match.group())
                
                with VideoFileClip(temp_path) as video:
                    klipler = [video.subclipped(k['start'], k['end']) for k in kesim_noktalari]
                    final = concatenate_videoclips(klipler)
                    output_path = "final_output.mp4"
                    final.write_videofile(output_path, codec="libx264")
                
                st.video(output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Kurguyu İndir", f, "kurgu.mp4")
            
        except Exception as e:
            st.error(f"Hata: {e}")
        finally:
            if os.path.exists(temp_path): os.remove(temp_path)

elif password != "":
    st.error("Yanlış Şifre!")