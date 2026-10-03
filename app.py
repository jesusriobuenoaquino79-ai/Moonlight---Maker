import streamlit as st, tempfile, os, subprocess
from PIL import Image
from moviepy.editor import AudioFileClip
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

st.set_page_config(page_title="Moonlight Dreams Final", page_icon="🌙", layout="centered")
st.title("🌙 Moonlight Dreams - Final 3:10 + Crossfade")

musica = st.file_uploader("🎵 MP3 de Flow/Suno (hasta 3:10)", type=["mp3"], key="mp3_final")
foto1 = st.file_uploader("📷 Foto 1 (0 - mitad)", type=["jpg","png","webp","jpeg"], key="foto1_final")
foto2 = st.file_uploader("📷 Foto 2 (mitad - final)", type=["jpg","png","webp","jpeg"], key="foto2_final")

if musica:
    st.success(f"Audio: {musica.name} ✅")
if foto1:
    st.image(foto1, width=200, caption="Foto 1 ✅")
if foto2:
    st.image(foto2, width=200, caption="Foto 2 ✅")

if musica and foto1 and foto2:
    if st.button("🚀 CREAR VIDEO", type="primary", use_container_width=True):
        try:
            barra = st.progress(0, text="Iniciando...")
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_in = os.path.join(tmpdir, "in.mp3")
                with open(audio_in, "wb") as f:
                    f.write(musica.getbuffer())

                audio_clip = AudioFileClip(audio_in)
                duracion_total = audio_clip.duration
                audio_clip.close()

                if duracion_total > 190:
                    duracion_total = 190

                duracion_mitad = duracion_total / 2
                crossfade = 1.0 # 1 segundo de transición suave
                offset = duracion_mitad - crossfade

                st.info(f"Audio: {duracion_total:.1f}s | Crossfade: {crossfade}s en {offset:.1f}s")

                def prep(f_up, out):
                    im = Image.open(f_up).convert("RGB")
                    w,h = im.size
                    r = max(1280/w, 720/h)
                    im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                    im = im.crop(((im.width-1280)//2, (im.height-720)//2, (im.width-1280)//2+1280, (im.height-720)//2+720))
                    im.save(out, "JPEG", quality=85)

                img1 = os.path.join(tmpdir, "img1.jpg")
                img2 = os.path.join(tmpdir, "img2.jpg")
                prep(foto1, img1)
                prep(foto2, img2)

                v1 = os.path.join(tmpdir, "v1.mp4")
                v2 = os.path.join(tmpdir, "v2.mp4")
                final = os.path.join(tmpdir, "final.mp4")

                barra.progress(40, text=f"Video 1: {duracion_mitad:.0f}s...")
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img1, "-t", str(duracion_mitad + crossfade), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", v1], check=True)

                barra.progress(70, text=f"Video 2: {duracion_mitad:.0f}s...")
                subprocess.run([FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img2, "-t", str(duracion_mitad + crossfade), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "28", v2], check=True)

                barra.progress(90, text="Crossfade + Audio...")
                # --- CORRECCIÓN CROSSFADE AQUÍ ---
                subprocess.run([
                    FFMPEG, "-y",
                    "-i", v1, "-i", v2, "-i", audio_in,
                    "-filter_complex", f"[0:v][1:v]xfade=transition=fade:duration={crossfade}:offset={offset}[v]",
                    "-map", "[v]", "-map", "2:a",
                    "-t", str(duracion_total),
                    "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                    final
                ], check=True)

                barra.progress(100, text="¡Listo!")
                st.success(f"¡VIDEO {duracion_total:.0f}s CON CROSSFADE LISTO! 🔥")
                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR", f.read(), file_name=f"moonlight-{int(duracion_total)}s.mp4", type="primary", use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
