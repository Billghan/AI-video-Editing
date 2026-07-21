from moviepy import VideoFileClip
import json
import streamlit as st

def kurgula(video_path, zaman_damgalari_json):
    # Zaman damgalarını listeye çevir
    kesilecekler = json.loads(zaman_damgalari_json)
    # Burada video işleme kodları olacak
    return "cikti_video.mp4"
