import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

st.title("1H FINAL - PARA MP3 DE 3 MIN")

mp3 = st.file_uploader("MP3 2:50 a 3:10", type=["mp3"])
f1 = st.file_uploader("Foto1", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2", type=["jpg","png","webp"], key="2")

if st.button("CREAR 1H BIEN HECHA - 60 MIN REAL", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au = os.path.join(tmp,"a.mp3")
        open(au,"wb").write(mp3.getvalue())
        i1 = os.path.join(tmp,"1.jpg")
        i2 = os.path.join(tmp,"2.jpg")

        def prep(up, out):
            im = Image.open(up).convert("RGB").resize((1920,1080))
            im.save(out, "JPEG", quality=95)
        prep(f1, i1); prep(f2, i2)

        out = "/tmp/final_60min.mp4"
        st.write("⏳ Creando 1H real... 4 min, no cierres")

        # PARA MP3 DE 2:50 - 3:10:
        # stream_loop 21 = 22 repeticiones
        # 2:50 x 22 = 62 min -> lo corta a 60 min exactos con -t 3600
        cmd = [FFMPEG,"-y",
               "-loop","1","-t","3600","-framerate","30","-i", i1,
               "-loop","1","-t","3600","-framerate","30","-i", i2,
               "-stream_loop","21","-i", au,
               "-filter_complex","[0:v]scale=1920:1080,crop=1920:1080[v0];[1:v]scale=1920:1080,crop=1920:1080[v1];[v0][v1]xfade=transition=fade:duration=3:offset=1797,format=yuv420p[v]",
               "-map","[v]","-map","2:a",
               "-t","3600","-c:v","libx264","-crf","20","-preset","medium","-r","30",
               "-c:a","aac","-b:a","192k","-movflags","+faststart", out]

        subprocess.run(cmd, check=True)
        st.success("✅ LISTO - 60 MINUTOS REALES")
        st.video(out)
        st.download_button("📥 DESCARGAR 1H 60MIN PRO (YA COMPRIMIDA)", open(out,"rb").read(), "1h_60min_REAL.mp4", use_container_width=True)
