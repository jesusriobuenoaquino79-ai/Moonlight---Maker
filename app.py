import streamlit as st
from PIL import Image
import io
from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips

st.set_page_config(page_title="Moonlight Maker - 1 HORA", layout="centered")
st.title("Maker - 1 HORA 🌙")
st.write("Sube 1 imagen + 1 audio de 3 min")

# 1. Imagen
st.write("1. Imagen (si no puedes, marca abajo)")
img_file = st.file_uploader("Upload imagen", type=["jpg","jpeg","png"], label_visibility="collapsed", key="img")
use_default = st.checkbox("Usar imagen por defecto de luna 🌙", value=True)

# 2. Audio - FIX: type=None para que acepte sleep.mp3
st.write("2. Audio de 3 min (MP3 de Flow/Suno)")
audio_file = st.file_uploader("Upload audio", type=None, label_visibility="collapsed", key="audio")

titulo = st.text_input("Titulo", value="Moonlight Dreams - 1 Hour 432Hz")

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not audio_file:
        st.error("Sube el audio sleep.mp3")
    else:
        # Imagen por defecto
        if use_default or not img_file:
            # crea luna amarilla simple
            img = Image.new('RGB', (1920,1080), color=(10,10,30))
            # dibuja luna simple con PIL
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.ellipse((1400, 100, 1700, 400), fill=(255,220,100))
            image_source = img
        else:
            image_source = Image.open(img_file)

        with st.spinner("Creando video de 1 hora... esto tarda 1-2 min"):
            # Guardar audio temporal
            with open("/tmp/input.mp3","wb") as f:
                f.write(audio_file.read())

            audio = AudioFileClip("/tmp/input.mp3")
            # loop hasta 1 hora (3600 seg)
            loops = int(3600 // audio.duration) + 1
            audio_looped = concatenate_audioclips([audio]*loops).subclip(0,3600)

            # Imagen fija 1 hora
            img_clip = ImageClip(image_source).set_duration(3600).set_audio(audio_looped)
            img_clip = img_clip.set_fps(24)

            output_path = f"/tmp/{titulo}.mp4"
            img_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

            st.success("¡Video creado!")
            st.video(output_path)
            with open(output_path, "rb") as vid:
                st.download_button("📥 Descargar Video", vid, file_name=f"{titulo}.mp4", mime="video/mp4")
