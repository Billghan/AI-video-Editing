import google.generativeai as genai
import streamlit as st

def analiz_et(video_url, prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Model ismini API yetkine göre buraya yaz
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    full_prompt = f"Video linki: {video_url}. Kullanıcı isteği: {prompt}. Videodaki gereksiz, sabit anların saniye aralıklarını [başlangıç, bitiş] formatında, sadece JSON listesi olarak ver."
    
    response = model.generate_content(full_prompt)
    return response.text
