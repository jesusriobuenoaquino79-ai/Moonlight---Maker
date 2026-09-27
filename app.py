import streamlit as st
import tempfile
import os
import glob
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips

st.set_page_config(page_title="HORA - Híbrido PRO", page_icon="🌙")
st.title("🌙 HORA - Versión Híbrida PRO")
st.write("Usa tu imagen + el audio de GitHub automáticamente")

titulo = st.text_input("Título", "Moonlight Dreams - 1 Hour")

# Buscar audio en GitHub (ya lo tienes subido)
mp3s = glob.glob("*.mp3")
if mp3s:
    audio_path_repo = mp3s[0]
    st.success(f"Audio de GitHub listo: {audio_path_repo} ✅")
else:
    audio_path_repo = None
    st.error("No hay audio en GitHub")

st.write("---")
st.subheader("Sube SOLO tu imagen bonita (el audio ya está)")
imagen_file = st.file_uploader("Imagen del lago", type=["jpg","jpeg","png","webp"])

st.write("---")
st.write("Si quieres usar otra música diferente, súbela aquí (opcional):")
audio_file_optional = st.file_uploader("Música opcional (si no subes, uso la de GitHub)", type=["mp3","wav","m4a","ogg"])

if st.button("✨ CREAR VIDEO 1 HORA", type="primary"):
    if not mp3s and audio_file_optional is None:
        st.error("No hay audio")
    elif imagen_file is None:
        st.error("¡Sube la imagen del lago!")
    else:
        with st.spinner("Creando tu video PRO... 3 min ⏳"):
            # AUDIO: si sube uno nuevo usa ese, si no usa el de GitHub
            if audio_file_optional is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                    tmp_audio.write(audio_file_optional.getvalue())
                    audio_path = tmp_audio.name
                st.info("Usando tu música nueva")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                    with open(audio_path_repo, "rb") as f:
                        tmp_audio.write(f.read())
                    audio_path = tmp_audio.name
                st.info(f"Usando audio de GitHub: {audio_path_repo}")

            # IMAGEN: la que subiste
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(imagen_file.getvalue())
                img_path = tmp_img.name

            try:
                audio = AudioFileClip(audio_path)
                loops = int(3600 / audio.duration) + 1
                final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)
                image_clip = ImageClip(img_path).set_duration(3600)
                video = image_clip.set_audio(final_audio)
                output_path = tempfile.mktemp(suffix=".mp4")
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
                st.success("¡VIDEO CON TU IMAGEN DEL LAGO LISTO! 🎉")
                with open(output_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO", f, file_name=f"{titulo}.mp4", mime="video/mp4")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
