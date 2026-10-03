import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H ULTRA RAPIDO", page_icon="⚡", layout="centered")
st.title("⚡ 1 HORA ULTRA RAPIDO - 2-3 Min")

musica = st.file_uploader("🎵 MP3 2:50 a 3:10", type=["mp3"], key="mp3_fast")
foto1 = st.file_uploader("📷 Foto 1 (0-30m)", type=["jpg","png","webp","jpeg"], key="f1_fast")
foto2 = st.file_uploader("📷 Foto 2 (30-60m)", type=["jpg","png","webp","jpeg"], key="f2_fast")

if musica and foto1 and foto2:
    if st.button("🚀 CREAR VIDEO 1 HORA RAPIDO", type="primary", use_container_width=True):
        barra = st.progress(0, text="Iniciando...")
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                audio_in = os.path.join(tmpdir, "in.mp3")
                with open(audio_in, "wb") as f: f.write(musica.getbuffer())

                def prep(f_up, out):
                    im = Image.open(f_up).convert("RGB")
                    w,h = im.size
                    r = max(1280/w, 720/h)
                    im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                    im = im.crop(((im.width-1280)//2, (im.height-720)//2, (im.width-1280)//2+1280, (im.height-720)//2+720))
                    im.save(out, "JPEG", quality=85)

                img1 = os.path.join(tmpdir, "img1.jpg")
                img2 = os.path.join(tmpdir, "img2.jpg")
                prep(foto1, img1); prep(foto2, img2)

                v1 = os.path.join(tmpdir, "v1.mp4")
                v2 = os.path.join(tmpdir, "v2.mp4")
                final = os.path.join(tmpdir, "final_1h.mp4")

                barra.progress(20, text="Foto 1 - 30 min (1fps = rápido)...")
                # CAMBIO CLAVE: -r 1 y ultrafast en vez de 24fps
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-r", "1", "-i", img1, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "30", v1], check=True)

                barra.progress(50, text="Foto 2 - 30 min (1fps = rápido)...")
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-r", "1", "-i", img2, "-t", "1800", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-tune", "stillimage", "-crf", "30", v2], check=True)

                barra.progress(80, text="Uniendo + Loop Audio...")
                subprocess.run([
                    FFMPEG, "-y",
                    "-i", v1, "-i", v2, "-stream_loop", "25", "-i", audio_in,
                    "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=1:offset=1799,format=yuv420p[v]",
                    "-map", "[v]", "-map", "2:a",
                    "-t", "3600",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
                    "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart",
                    final
                ], check=True)

                barra.progress(100, text="¡Listo!")
                st.success("¡VIDEO 1 HORA LISTO! ⚡")
                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR 1 HORA", f.read(), file_name="video-1hora-rapido.mp4", type="primary", use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")
