import streamlit as st
import tempfile
from PIL import Image
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips
import os

st.set_page_config(page_title="HORA LUNA", page_icon="🌙")
st.title("HORA 🌙 - Video 1 Hora")

titulo = st.text_input("Título del video", "Moonlight Dreams - 1 Hour Relaxing Sleep Music")

# AUDIO: busca el mp3 en el repo
audio_path_repo = "sleep.mp3"
if os.path.exists(audio_path_repo):
    st.success(f"Audio encontrado: {audio_path_repo} ✅")
    audio_file = open(audio_path_repo, "rb")
    # para que moviepy lo pueda leer, lo guardaremos despues
    audio_file_bytes = open(audio_path_repo, "rb").read()
    has_audio = True
else:
    st.warning("Sube el sleep.mp3 a GitHub")
    audio_file = st.file_uploader("Sube tu audio mp3", type=["mp3"])
    has_audio = audio_file is not None
    audio_file_bytes = None

# IMAGEN - ya sin bug
st.write("---")
st.subheader("Imagen del video")
imagen_file = st.file_uploader("Sube la imagen bonita que te di (lago + luna)", type=["jpg","jpeg","png","webp"])

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not os.path.exists(audio_path_repo) and not audio_file:
        st.error("Sube primero el sleep.mp3")
    else:
        with st.spinner("Creando tu video de 1 hora... esto tarda 3-5 min, no cierres"):
            # Guardar audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                if audio_file_bytes:
                    tmp_audio.write(audio_file_bytes)
                else:
                    tmp_audio.write(audio_file.read())
                audio_path = tmp_audio.name

            # Guardar imagen - ARREGLADO: si subes imagen, SIEMPRE usa esa
            if imagen_file is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(imagen_file.read())
                    img_path = tmp_img.name
                st.info("Usando tu imagen bonita ✅")
            else:
                # solo respaldo si no subiste nada
                img = Image.new('RGB', (1280,720), color=(10,15,30))
                from PIL import ImageDraw
                draw = ImageDraw.Draw(img)
                draw.ellipse((900,100,1100,300), fill=(255,230,120))
                img_path = tempfile.mktemp(suffix=".jpg")
                img.save(img_path)
                st.info("No subiste imagen, usando luna simple")

            try:
                audio = AudioFileClip(audio_path)
                loops = int(3600 / audio.duration) + 1
                final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

                image_clip = ImageClip(img_path).set_duration(3600)
                video = image_clip.set_audio(final_audio)

                output_path = tempfile.mktemp(suffix=".mp4")
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)

                st.success("¡Video listo! 🎉")
                with open(output_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name=f"{titulo}.mp4")

            except Exception as e:
                st.error(f"Error: {e}")
