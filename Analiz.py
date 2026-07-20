import google.generativeai as genai
import streamlit as st

def analiz_et(video_url, prompt):
    # API Anahtarını Streamlit secrets'tan alıyoruz
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    full_prompt = f"Video linki: {video_url}. Kullanıcı isteği: {prompt}. Videodaki gereksiz, sabit anların saniye aralıklarını [başlangıç, bitiş] formatında, sadece JSON listesi olarak ver."
    
    response = model.generate_content(full_prompt)
    # Gemini'den gelen metni temizleyip JSON listesine çeviriyoruz
    return response.text
