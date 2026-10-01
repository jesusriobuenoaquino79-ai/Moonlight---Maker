import streamlit as st, tempfile, glob, os, subprocess
from PIL import Image
from moviepy.editor import AudioFileClip, concatenate_audi audioclips
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

st.set_page_config(page_title="Moonlight Dreams", page_icon="🌙", layout="centered")
st.title("🌙 Moonlight Dreams - Video 1 Hora YOUTUBE READY")

try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Música: {audio_fijo} ✅")
except:
    st.error("No hay MP3")
    st.stop()

foto1 = st.file_uploader("Foto 1 (0-30 min)", type=["jpg","png","webp","jpeg"], key="f1")
foto2 = st.file_uploader("Foto 2 (30-60 min)", type=["jpg","png","webp","jpeg"], key="f2")

if foto1: st.image(foto1, width=200, caption="Foto 1 ✅")
if foto2: st.image(foto2, width=200, caption="Foto 2 ✅")

boton = st.button("🚀 CREAR VIDEO 1 HORA - PARA YOUTUBE", type="primary", disabled=not (foto1 and foto2))

if boton:
    barra = st.progress(0, text="Iniciando...")
    with tempfile.TemporaryDirectory() as tmpdir:
        img1_path = os.path.join(tmpdir, "img1.jpg")
        img2_path = os.path.join(tmpdir, "img2.jpg")
        audio_1h = os.path.join(tmpdir, "audio1h.mp3")
        v1 = os.path.join(tmpdir, "v1.mp4")
        v2 = os.path.join(tmpdir, "v2.mp4")
        lista = os.path.join(tmpdir, "lista.txt")
        out_temp = os.path.join(tmpdir, "final_temp.mp4")
        out_final = os.path.join(tmpdir, "final_youtube.mp4")

        for f, p in [(foto1, img1_path), (foto2, img2_path)]:
            im = Image.open(f).convert("RGB")
            w,h = im.size
            ratio = max(1280/w, 720/h)
            im = im.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            im = im.crop(((im.width-1280)//2, (im.height-720)//2, (im.width-1280)//2+1280, (im.height-720)//2+720))
            im.save(p, "JPEG", quality=85)

        barra.progress(20, text="Audio 1 hora...")
        audio = AudioFileClip(audio_fijo)
        loops = int(3600 / audio.duration) + 1
        final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)
        final_audio.write_audiofile(audio_1h, logger=None, codec='libmp3lame', bitrate="128k")
        audio.close()
        final_audio.close()

        barra.progress(40, text="Video parte 1 (optimizado)...")
        # CAMBIO CLAVE 1: de ultrafast a veryfast + crf 28 (10 veces más liviano)
        subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img1_path, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", "-r", "24", v1], check=True)

        barra.progress(60, text="Video parte 2 (optimizado)...")
        subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img2_path, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", "-r", "24", v2], check=True)

        barra.progress(80, text="Uniendo...")
        with open(lista, "w") as f:
            f.write(f"file '{v1}'\nfile '{v2}'\n")
        subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lista, "-i", audio_1h, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", out_temp], check=True)

        barra.progress(90, text="Comprimiendo para YouTube (180MB)...")
        # CAMBIO CLAVE 2: recompresión final para YouTube
        subprocess.run([FFMPEG, "-y", "-i", out_temp, "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out_final], check=True)

        size_mb = os.path.getsize(out_final) / (1024*1024)

        barra.progress(100, text="¡Listo!")
        st.success(f"¡VIDEO LISTO MI REY! 🔥 Ahora pesa {size_mb:.1f} MB (antes 3000MB)")
        st.balloons()
        st.video(out_final)
        with open(out_final,"rb") as f:
            st.download_button(f"📥 DESCARGAR VIDEO YOUTUBE ({size_mb:.0f} MB)", f.read(), file_name="moonlight-1hora-YOUTUBE.mp4", type="primary", use_container_width=True)
