import streamlit as st
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips
import tempfile
import os

st.set_page_config(page_title="Moonlight Maker 1H", layout="centered")
st.title("Maker - Video 1 HORA 🌙")
st.caption("Versión arreglada - acepta cualquier audio")

# --- CONFIGURACION ---
# Usamos type=None para que NUNCA más te salga el ! rojo
audio_file = st.file_uploader("2. Sube tu audio sleep.mp3 (ahora acepta todo)", type=None)

use_default = st.checkbox("Usar luna por defecto 🌙 (recomendado)", value=True)
img_file = st.file_uploader("1. Imagen opcional", type=None)

titulo = st.text_input("Título del video", "Moonlight Dreams - 1 Hour")

def crear_luna():
    img = Image.new('RGB', (1920, 1080), (10,12,40))
    d = ImageDraw.Draw(img)
    d.ellipse((1300,100,1750,550), fill=(255,235,130))
    for x,y in [(200,150),(500,300),(800,180),(400,800)]:
        d.ellipse((x,y,x+6,y+6), fill=(255,255,255))
    return img

if st.button("✨ CREAR VIDEO DE 1 HORA", type="primary"):
    if not audio_file:
        st.error("Sube primero el audio")
        st.stop()

    with st.spinner("Creando... esto tarda 2 minutos, no cierres"):
        tmp = tempfile.mkdtemp()
        img_path = os.path.join(tmp, "img.jpg")
        audio_path = os.path.join(tmp, "audio_input")
        
        # Guardar imagen
        pil_img = crear_luna() if use_default or not img_file else Image.open(img_file).convert("RGB")
        pil_img.save(img_path)

        # Guardar audio tal cual viene, sin importar si es mp3, m4a, ogg
        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        # Procesar
        audio_clip = AudioFileClip(audio_path)
        loops = int(3600 / audio_clip.duration) + 1
        audio_final = concatenate_audioclips([audio_clip]*loops).subclip(0, 3600)
        
        clip = ImageClip(img_path).set_duration(3600).set_audio(audio_final)
        clip = clip.set_fps(24)
        
        out_path = os.path.join(tmp, "video_1h.mp4")
        clip.write_videofile(out_path, codec='libx264', audio_codec='aac', fps=24, logger=None)
        
        st.success("¡LISTO!")
        st.video(out_path)
        with open(out_path, "rb") as v:
            st.download_button("📥 DESCARGAR VIDEO", v, file_name=f"{titulo}.mp4", mime="video/mp4")
