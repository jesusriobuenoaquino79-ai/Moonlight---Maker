import streamlit as st
import tempfile
import os
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="Moonlight Maker 🌙", layout="centered")
st.title("🌙 Moonlight Maker")
st.write("Sube 1 imagen + 1 audio = Video listo para YouTube")

imagen = st.file_uploader("1. Imagen", type=["jpg","png","jpeg"])
audio = st.file_uploader("2. Audio 1 hora", type=["mp3","wav","m4a"])
titulo = st.text_input("Titulo", "Moonlight Dreams - Sleep Music")

if st.button("CREAR VIDEO ✨"):
    if not imagen or not audio:
        st.error("Sube imagen y audio mi rey")
    else:
        with st.spinner("Creando tu video de 1 hora... no cierres"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as i:
                i.write(imagen.getbuffer())
                img_path = i.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as a:
                a.write(audio.getbuffer())
                aud_path = a.name
            audio_clip = AudioFileClip(aud_path)
            video_clip = ImageClip(img_path, duration=audio_clip.duration).set_audio(audio_clip).resize(height=1080)
            out = f"/tmp/{titulo}.mp4"
            video_clip.write_videofile(out, fps=24, codec='libx264', audio_codec='aac', logger=None)
            st.success("¡VIDEO LISTO!")
            with open(out, "rb") as f:
                st.download_button("📥 DESCARGAR VIDEO", f, file_name=f"{titulo}.mp4")
