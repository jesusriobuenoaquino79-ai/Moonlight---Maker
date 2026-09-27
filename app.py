import streamlit as st
import tempfile
import os
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips

st.set_page_config(page_title="HORA - Creador", page_icon="🎬")
st.title("🎬 HORA - Creador de Videos 1 Hora")
st.write("Sube CUALQUIER música y CUALQUIER imagen. Yo te armo el video.")

titulo = st.text_input("Título del video", "Mi Video 1 Hora")

st.write("---")
st.subheader("1️⃣ Sube tu música (mp3, wav, m4a)")
audio_file = st.file_uploader("Música", type=["mp3","wav","m4a","ogg"])

st.subheader("2️⃣ Sube tu imagen (jpg, png, webp)")
imagen_file = st.file_uploader("Imagen", type=["jpg","jpeg","png","webp"])

st.write("---")

if st.button("✨ CREAR VIDEO DE 1 HORA", type="primary"):
    if audio_file is None:
        st.error("¡Falta la música! Súbela arriba")
    elif imagen_file is None:
        st.error("¡Falta la imagen! Súbela arriba")
    else:
        with st.spinner("Creando tu video... tarda 3-4 min, no cierres ⏳"):
            # Guardar audio subido
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                tmp_audio.write(audio_file.getvalue())
                audio_path = tmp_audio.name

            # Guardar imagen subida
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(imagen_file.getvalue())
                img_path = tmp_img.name

            try:
                audio = AudioFileClip(audio_path)
                st.info(f"Tu audio dura {audio.duration/60:.1f} minutos. Lo voy a repetir hasta 1 hora.")

                loops = int(3600 / audio.duration) + 1
                final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

                image_clip = ImageClip(img_path).set_duration(3600)
                video = image_clip.set_audio(final_audio)

                output_path = tempfile.mktemp(suffix=".mp4")
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)

                st.success("¡VIDEO DE 1 HORA LISTO! 🎉🎉")
                with open(output_path, "rb") as f:
                    st.download_button(
                        "📥 DESCARGAR VIDEO",
                        f,
                        file_name=f"{titulo}.mp4",
                        mime="video/mp4"
                    )
                st.balloons()

            except Exception as e:
                st.error(f"Error: {e}")

st.write("---")
st.caption("Hecho para ti. Ya no hay luna amarilla. Solo lo que TÚ subas.")
