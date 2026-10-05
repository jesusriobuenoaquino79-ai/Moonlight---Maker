import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.title("1H DIRECTO - ARREGLADO")

mp3 = st.file_uploader("MP3", type=["mp3"])
f1 = st.file_uploader("Foto1", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2", type=["jpg","png","webp"], key="2")

if st.button("CREAR 1H DIRECTO", use_container_width=True):
    if not mp3 or not f1 or not f2:
        st.error("Sube MP3 + 2 fotos")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            au = os.path.join(tmp,"a.mp3")
            open(au,"wb").write(mp3.getvalue())
            i1 = os.path.join(tmp,"1.jpg")
            i2 = os.path.join(tmp,"2.jpg")
            # Obligo las 2 a 1280x720
            def prep(up, out):
                im = Image.open(up).convert("RGB")
                im = im.resize((1280,720))
                im.save(out, "JPEG", quality=75)
            prep(f1, i1)
            prep(f2, i2)

            out = "/tmp/final.mp4"
            st.write("⏳ Creando 1 hora directo (2 min)... no cierres")

            cmd = [
                FFMPEG, "-y",
                "-loop","1","-t","3600","-r","1","-i", i1,
                "-loop","1","-t","3600","-r","1","-i", i2,
                "-i", au,
                "-filter_complex", "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[v0];[1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[v1];[v0][v1]xfade=transition=fade:duration=2:offset=1798,format=yuv420p[v]",
                "-map","[v]","-map","2:a",
                "-t","3600","-c:v","libx264","-crf","28","-preset","veryfast","-r","24",
                "-c:a","aac","-b:a","128k","-movflags","+faststart","-shortest", out
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                st.success("✅ LISTO 1 HORA")
                st.video(out)
                st.download_button("📥 DESCARGAR 1H YA COMPRIMIDO", open(out,"rb").read(), "1h_2fotos_comprimido.mp4", "video/mp4", use_container_width=True)
            except subprocess.CalledProcessError as e:
                st.error(f"Error: {e.stderr[-500:]}")
