import streamlit as st
import tempfile
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips

st.set_page_config(page_title="CABAÑA LLUVIOSA - 1 HORA", page_icon="🌙")
st.title("🌙 Cabaña Lluviosa - Video 1 Hora")
st.write("Sube tu imagen + tu música con lluvia de Flow")

titulo = st.text_input("Título del video", "Noche de Paz en la Cabaña - 1 Hora")

st.write("---")
imagen_file = st.file_uploader("1️⃣ Sube tu imagen bonita", type=["jpg","jpeg","png","webp"])
audio_file = st.file_uploader("2️⃣ Sube tu música MP3 con lluvia", type=["mp3","wav","m4a","ogg"])

if st.button("✨ CREAR VIDEO 1 HORA", type="primary"):
    if imagen_file is None or audio_file is None:
        st.error("¡Falta la imagen o la música! Sube las dos 🙏")
    else:
        with st.spinner("Creando tu video de 1 hora... 3 min ⏳"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                tmp_audio.write(audio_file.getvalue())
                audio_path = tmp_audio.name

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
                st.success("¡VIDEO LISTO MI REY! 🎉")
                with open(output_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO", f, file_name=f"{titulo}.mp4", mime="video/mp4")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
