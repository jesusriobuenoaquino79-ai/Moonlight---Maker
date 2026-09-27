import streamlit as st
import tempfile
import os
import glob
from PIL import Image
from moviepy.editor import AudioFileClip, ImageClip, concatenate_audioclips

st.set_page_config(page_title="HORA LUNA", page_icon="🌙")
st.title("HORA 🌙 - Video 1 Hora")
st.write("Crea tu video de 1 hora para YouTube")

titulo = st.text_input("Título del video", "Moonlight Dreams - 1 Hour Relaxing Sleep Music")

# --- BUSCAR AUDIO: agarra CUALQUIER mp3 que tengas en GitHub ---
st.write("---")
mp3s = glob.glob("*.mp3")
if mp3s:
    audio_path_repo = mp3s[0]
    st.success(f"Audio encontrado: {audio_path_repo} ✅ {os.path.getsize(audio_path_repo)/1024/1024:.2f} MB")
    has_audio_repo = True
else:
    st.warning("No encontré ningún mp3 en GitHub. Súbelo con Add file > Upload")
    has_audio_repo = False
    audio_path_repo = None

# --- IMAGEN ---
st.subheader("Imagen del video")
st.write("Sube la imagen bonita del lago que te di")
imagen_file = st.file_uploader("Imagen (jpg, png)", type=["jpg","jpeg","png","webp"])

if st.button("✨ CREAR VIDEO DE 1 HORA", type="primary"):
    if not has_audio_repo and not mp3s:
        st.error("No hay audio en GitHub. Sube tu mp3 primero")
    else:
        with st.spinner("Creando tu video de 1 hora... tarda 3-5 min, no cierres la app ⏳"):
            # Guardar audio temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                with open(audio_path_repo, "rb") as f:
                    tmp_audio.write(f.read())
                audio_path = tmp_audio.name

            # Guardar imagen - SIEMPRE usa la que subas
            if imagen_file is not None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                    tmp_img.write(imagen_file.getvalue())
                    img_path = tmp_img.name
                st.info("Usando tu imagen bonita del lago ✅")
            else:
                # respaldo solo si no subes nada
                img = Image.new('RGB', (1280,720), color=(10,15,30))
                from PIL import ImageDraw
                draw = ImageDraw.Draw(img)
                draw.ellipse((900,100,1100,300), fill=(255,230,120))
                img_path = tempfile.mktemp(suffix=".jpg")
                img.save(img_path)
                st.info("No subiste imagen, usando respaldo amarillo")

            try:
                audio = AudioFileClip(audio_path)
                # cuantas veces repetir para llegar a 1 hora (3600 seg)
                loops = int(3600 / audio.duration) + 1
                final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

                image_clip = ImageClip(img_path).set_duration(3600)
                video = image_clip.set_audio(final_audio)

                output_path = tempfile.mktemp(suffix=".mp4")
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)

                st.success("¡Video de 1 hora listo! 🎉")
                with open(output_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name=f"{titulo}.mp4", mime="video/mp4")

                st.balloons()

            except Exception as e:
                st.error(f"Error: {e}")
