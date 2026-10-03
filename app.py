import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

st.set_page_config(page_title="Plantilla 1HORA Final", page_icon="🌙", layout="centered")
st.title("🌙 Plantilla 1 HORA - Crossfade 30min + Loop")

musica = st.file_uploader("🎵 MP3 Flow (2:50 a 3:10) - hará loop a 1 hora", type=["mp3"], key="mp3_1h_final")
foto1 = st.file_uploader("📷 Foto 1 (0 a 30 min)", type=["jpg","png","webp","jpeg"], key="foto1_1h_final")
foto2 = st.file_uploader("📷 Foto 2 (30 a 60 min)", type=["jpg","png","webp","jpeg"], key="foto2_1h_final")

if musica and foto1 and foto2:
    st.success(f"Audio: {musica.name} + 2 Fotos ✅")
    if st.button("🚀 CREAR VIDEO 1 HORA", type="primary", use_container_width=True):
        barra = st.progress(0, text="Iniciando...")
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                audio_in = os.path.join(tmpdir, "in.mp3")
                with open(audio_in, "wb") as f:
                    f.write(musica.getbuffer())

                def prep(f_up, out):
                    im = Image.open(f_up).convert("RGB")
                    w,h = im.size
                    r = max(1280/w, 720/h)
                    im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                    im = im.crop(((im.width-1280)//2, (im.height-720)//2, (im.width-1280)//2+1280, (im.height-720)//2+720))
                    im.save(out, "JPEG", quality=90)

                img1 = os.path.join(tmpdir, "img1.jpg")
                img2 = os.path.join(tmpdir, "img2.jpg")
                prep(foto1, img1)
                prep(foto2, img2)

                v1 = os.path.join(tmpdir, "v1.mp4")
                v2 = os.path.join(tmpdir, "v2.mp4")
                final = os.path.join(tmpdir, "final_1h.mp4")

                barra.progress(25, text="Creando Foto 1 (30 min)...")
                # 1800 seg = 30 min exactos
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img1, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", v1], check=True)

                barra.progress(50, text="Creando Foto 2 (30 min)...")
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img2, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", v2], check=True)

                barra.progress(85, text="Uniendo 1H + Loop Audio + Crossfade...")
                # LOGICA FINAL QUE ME PEDISTE:
                # [0:v]=30min [1:v]=30min con xfade a los 1799s (30min - 1s)
                # [2:a]=tu mp3 de 3:10 con stream_loop 20 veces = 1 hora
                subprocess.run([
                    FFMPEG, "-y",
                    "-i", v1,
                    "-i", v2,
                    "-stream_loop", "20", "-i", audio_in,
                    "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=1:offset=1799[v]",
                    "-map", "[v]", "-map", "2:a",
                    "-t", "3600",
                    "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart",
                    final
                ], check=True)

                barra.progress(100, text="¡Listo!")
                st.success("¡VIDEO 1 HORA LISTO! 🔥")
                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR 1 HORA", f.read(), file_name="video-1-hora.mp4", type="primary", use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")
