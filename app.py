import streamlit as st
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips
import tempfile
import os

st.set_page_config(page_title="Moonlight Maker - 1 HORA", layout="centered")

st.title("Maker - 1 HORA 🌙")
st.write("Sube 1 imagen + 1 audio de 3 min")

# 1. Imagen
st.markdown("### 1. Imagen (si no puedes, marca abajo)")
img_file = st.file_uploader("Sube imagen", type=["jpg","jpeg","png"], label_visibility="collapsed")
use_default = st.checkbox("Usar imagen por defecto de luna 🌙", value=True)

# 2. Audio - ARREGLADO: type=None para que acepte sleep.mp3 sin error rojo
st.markdown("### 2. Audio de 3 min (MP3 de Flow/Suno)")
audio_file = st.file_uploader("Sube audio", type=None, label_visibility="collapsed")

titulo = st.text_input("Titulo", value="Moonlight Dreams - 1 Hour 432Hz")

# Función para crear luna por defecto
def crear_luna_default():
    img = Image.new('RGB', (1920, 1080), color=(8, 10, 35))
    draw = ImageDraw.Draw(img)
    # Luna grande amarilla
    draw.ellipse((1300, 80, 1750, 530), fill=(255, 230, 120))
    # Estrellitas
    for x,y in [(200,150),(400,300),(800,200),(300,800),(600,700)]:
        draw.ellipse((x,y,x+8,y+8), fill=(255,255,255))
    return img

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not audio_file:
        st.error("❌ Sube el audio sleep.mp3")
        st.stop()
    
    if not use_default and not img_file:
        st.error("❌ Marca la luna por defecto o sube una imagen")
        st.stop()

    with st.spinner("Creando tu video de 1 hora... Espera 1-2 min ⏳"):

        # Imagen
        if use_default or not img_file:
            pil_img = crear_luna_default()
        else:
            pil_img = Image.open(img_file).convert("RGB")

        # Guardar imagen temporal
        temp_dir = tempfile.mkdtemp()
        img_path = os.path.join(temp_dir, "imagen.jpg")
        pil_img.save(img_path)

        # Guardar audio temporal
        audio_path = os.path.join(temp_dir, "audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio_file.read())

        # Cargar audio y hacer loop a 1 hora (3600 segundos)
        audio_clip = AudioFileClip(audio_path)
        loops_needed = int(3600 // audio_clip.duration) + 1
        audio_final = concatenate_audioclips([audio_clip]*loops_needed).subclip(0, 3600)

        # Crear video con imagen fija
        video_clip = ImageClip(img_path).set_duration(3600).set_audio(audio_final)
        video_clip = video_clip.set_fps(24)

        output_path = os.path.join(temp_dir, f"{titulo}.mp4")
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, logger=None)

        st.success("¡Video de 1 hora creado! 🎉")
        st.video(output_path)

        with open(output_path, "rb") as vid:
            st.download_button(
                label="📥 Descargar Video MP4",
                data=vid,
                file_name=f"{titulo}.mp4",
                mime="video/mp4"
            )
