import streamlit as st
import tempfile
import glob
import os
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips

st.set_page_config(page_title="CABAÑA LLUVIOSA", page_icon="🌧️")
st.title("🌧️ Cabaña Lluviosa - Video 1 Hora")
st.write("Música nueva detectada ✅")

# BUSCA TU MÚSICA NUEVA DE 2.87 MB
archivos = glob.glob("*.mp3") + glob.glob("*.MP3")
# Coge el más nuevo (el que acabas de subir)
archivos.sort(key=os.path.getmtime, reverse=True)

if archivos:
    audio_fijo = archivos[0]
    st.success(f"🎵 Usando: {audio_fijo}")
else:
    st.error("No encuentro audio")
    st.stop()

titulo = st.text_input("Título", "Noche Lluviosa en la Cabaña - 1 Hora")
imagen_file = st.file_uploader("1️⃣ Sube solo tu imagen lluviosa", type=["jpg","jpeg","png","webp"])

if st.button("✨ CREAR VIDEO 1 HORA", type="primary"):
    if imagen_file is None:
        st.error("Sube la imagen mi rey")
    else:
        with st.spinner("Creando video... 3 min"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(imagen_file.getvalue())
                img_path = tmp_img.name

            audio = AudioFileClip(audio_fijo)
            loops = int(3600 / audio.duration) + 1
            final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)
            image_clip = ImageClip(img_path).set_duration(3600)
            video = image_clip.set_audio(final_audio)
            output_path = tempfile.mktemp(suffix=".mp4")
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)

            st.success("¡VIDEO LISTO!")
            with open(output_path, "rb") as f:
                st.download_button("📥 DESCARGAR", f, file_name=f"{titulo}.mp4", mime="video/mp4")
            st.balloons()
