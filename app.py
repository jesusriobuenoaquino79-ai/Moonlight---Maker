import streamlit as st
import tempfile
import glob
import os
import subprocess
from PIL import Image
from moviepy.editor import AudioFileClip, concatenate_audioclips

st.set_page_config(page_title="Moonlight Dreams", page_icon="🌙", layout="centered")
st.title("🌙 Moonlight Dreams - Video 1 Hora TURBO")

# 1. Busca el MP3 mas nuevo en la carpeta
try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Música encontrada: {audio_fijo} ✅")
except:
    st.error("No hay ningún MP3 en la carpeta. Sube uno a GitHub junto al app.py")
    st.stop()

# 2. Subir fotos
st.write("Sube las 2 fotos del video")
foto1 = st.file_uploader("Foto 1 (0-30 min)", type=["jpg","png","webp","jpeg"], key="f1")
foto2 = st.file_uploader("Foto 2 (30-60 min)", type=["jpg","png","webp","jpeg"], key="f2")

if foto1:
    st.image(foto1, width=200, caption="Foto 1 lista ✅")
if foto2:
    st.image(foto2, width=200, caption="Foto 2 lista ✅")

boton = st.button("🚀 CREAR VIDEO 1 HORA - TURBO", type="primary", disabled=not (foto1 and foto2))

if boton:
    barra = st.progress(0, text="Iniciando...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            img1_path = os.path.join(tmpdir, "img1.jpg")
            img2_path = os.path.join(tmpdir, "img2.jpg")
            audio_1h = os.path.join(tmpdir, "audio1h.mp3")
            v1 = os.path.join(tmpdir, "v1.mp4")
            v2 = os.path.join(tmpdir, "v2.mp4")
            lista = os.path.join(tmpdir, "lista.txt")
            out = os.path.join(tmpdir, "final.mp4")

            # Preparar fotos a 1280x720 sin estirar
            for f, p in [(foto1, img1_path), (foto2, img2_path)]:
                im = Image.open(f).convert("RGB")
                w, h = im.size
                ratio = max(1280/w, 720/h)
                im = im.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
                left = (im.width - 1280)//2
                top = (im.height - 720)//2
                im = im.crop((left, top, left+1280, top+720))
                im.save(p, "JPEG", quality=90)

            barra.progress(20, text="Creando audio 1 hora...")
            # Audio 1 hora con moviepy (mas estable que ffmpeg stream_loop)
            audio = AudioFileClip(audio_fijo)
            loops = int(3600 / audio.duration) + 1
            final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)
            final_audio.write_audiofile(audio_1h, logger=None, codec='libmp3lame')
            audio.close()
            final_audio.close()

            barra.progress(50, text="Video parte 1 (30 min)...")
            subprocess.run(f'ffmpeg -y -loop 1 -framerate 8 -i "{img1_path}" -t 1800 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -r 8 "{v1}"', shell=True, check=True)

            barra.progress(70, text="Video parte 2 (30 min)...")
            subprocess.run(f'ffmpeg -y -loop 1 -framerate 8 -i "{img2_path}" -t 1800 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -r 8 "{v2}"', shell=True, check=True)

            barra.progress(85, text="Uniendo video + audio...")
            with open(lista, "w") as f:
                f.write(f"file '{v1}'\nfile '{v2}'\n")

            subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{lista}" -i "{audio_1h}" -c:v copy -c:a aac -shortest "{out}"', shell=True, check=True)

            barra.progress(100, text="¡Listo!")
            st.success("¡VIDEO DE 1 HORA LISTO MI REY! 🔥")
            st.balloons()
            st.video(out)

            with open(out, "rb") as f:
                st.download_button("📥 DESCARGAR VIDEO FINAL", f.read(), file_name="moonlight-dreams-1hora.mp4", type="primary", use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Si dice 'ffmpeg not found', crea un archivo packages.txt en GitHub con la palabra ffmpeg adentro y dale a Reboot App.")
