import streamlit as st
from PIL import Image
import tempfile, os
from moviepy.editor import ImageClip, AudioFileClip, afx

st.set_page_config(page_title="Moonlight Maker", page_icon="🌙")
st.title("Maker - 1 HORA 🌙")
st.write("Sube 1 imagen + 1 audio de 3 min")

# ACEPTA CUALQUIER IMAGEN
image_file = st.file_uploader("1. Imagen (si no puedes, marca abajo)", type=None)
usar_default = st.checkbox("Usar imagen por defecto de luna 🌙")

# ACEPTA CUALQUIER AUDIO - ESTE ES EL ARREGLO
audio_file = st.file_uploader("2. Audio de 3 min (MP3 de Flow/Suno)", type=None)

titulo = st.text_input("Titulo", "Moonlight Dreams - 1 Hour 432Hz")

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not audio_file:
        st.error("Sube el audio de tu canción mi rey, el MP3 que descargaste de Flow")
    else:
        with st.spinner("Creando... 2 min"):
            try:
                if usar_default or not image_file:
                    img = Image.new('RGB', (1920, 1080), color=(15,15,35))
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                        img.save(tmp_img.name)
                        img_path = tmp_img.name
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                        img = Image.open(image_file).convert("RGB").resize((1920,1080))
                        img.save(tmp_img.name)
                        img_path = tmp_img.name

                # guarda audio como venga
                ext = ".mp3"
                if audio_file.name:
                    ext = "." + audio_file.name.split(".")[-1]
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_aud:
                    tmp_aud.write(audio_file.read())
                    aud_path = tmp_aud.name

                audio = AudioFileClip(aud_path)
                final_audio = audio.fx(afx.audio_loop, duration=3600)
                video = ImageClip(img_path, duration=3600).set_audio(final_audio).set_fps(24)
                out_path = os.path.join(tempfile.gettempdir(), "moonlight_1h.mp4")
                video.write_videofile(out_path, codec="libx264", audio_codec="aac", logger=None)
                
                st.success("¡LISTO MI REY! 1 HORA CREADA")
                st.video(out_path)
                with open(out_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO", f, file_name=f"{titulo}.mp4")
            except Exception as e:
                st.error(f"Error: {e} - Prueba con el MP3 de Flow en 432Hz")
