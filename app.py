import streamlit as st
from PIL import Image
import tempfile
import os
from moviepy.editor import *

st.set_page_config(page_title="HORA 🌙", layout="centered")
st.title("HORA 🌙")
st.write("Versión arreglada - acepta cualquier audio")

audio_file = st.file_uploader("2. Sube tu audio sleep.mp3 (ahora acepta todo)", type=None)

usar_luna = st.checkbox("Usar luna por defecto 🌙 (recomendado)", value=True)

imagen_file = st.file_uploader("1. Imagen opcional", type=["jpg","png","jpeg"])

titulo = st.text_input("Título del video", "Moonlight Dreams - 1 Hour")

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not audio_file:
        st.error("Sube primero el sleep.mp3")
    else:
        with st.spinner("Creando tu video de 1 hora... esto tarda 4 min, no cierres"):
            # Guardar audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                tmp_audio.write(audio_file.read())
                audio_path = tmp_audio.name

            # Imagen luna
            if usar_luna or not imagen_file:
                img = Image.new('RGB', (1280,720), color=(10,10,30))
                # dibuja luna amarilla simple
                from PIL import ImageDraw
                draw = ImageDraw.Draw(img)
                draw.ellipse((900,100,1100,300), fill=(255,230,100))
                img_path = tempfile.mktemp(suffix=".jpg")
                img.save(img_path)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(imagen_file.read())
                    img_path = tmp_img.name

            try:
                audio = AudioFileClip(audio_path)
                # Repetir hasta 1 hora (3600 seg)
                loops = int(3600 / audio.duration) + 1
                final_audio = concatenate_audioclips([audio]*loops).subclip(0,3600)

                image_clip = ImageClip(img_path).set_duration(3600)
                video = image_clip.set_audio(final_audio)

                output_path = tempfile.mktemp(suffix=".mp4")
                video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

                st.success("¡Video listo!")
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ DESCARGAR VIDEO DE 1 HORA", f, file_name=f"{titulo}.mp4")
            except Exception as e:
                st.error(f"Error: {e}")
