import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.title("1H HD 1080p LIVIANO - NO SE PEGA")

mp3 = st.file_uploader("MP3 3min", type=["mp3"])
f1 = st.file_uploader("Foto1 1920x1080", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2 1920x1080", type=["jpg","png","webp"], key="2")

if st.button("CREAR 1H HD RAPIDO", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au = os.path.join(tmp,"a.mp3")
        open(au,"wb").write(mp3.getvalue())
        i1 = os.path.join(tmp,"1.jpg")
        i2 = os.path.join(tmp,"2.jpg")
        def prep(up, out):
            im = Image.open(up).convert("RGB").resize((1920,1080))
            im.save(out, "JPEG", quality=95)
        prep(f1, i1); prep(f2, i2)
        out = "/tmp/HD_FAST.mp4"
        st.write("⏳ HD liviano 3-5 min... no cierres")
        cmd = [FFMPEG,"-y",
               "-framerate","1","-loop","1","-t","3600","-i", i1,
               "-framerate","1","-loop","1","-t","3600","-i", i2,
               "-stream_loop","21","-i", au,
               "-filter_complex","[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[v0][v1]xfade=transition=fade:duration=3:offset=1797,format=yuv420p,fps=30[v]",
               "-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-crf","20","-preset","veryfast","-r","30","-c:a","aac","-b:a","192k","-movflags","+faststart", out]
        subprocess.run(cmd, check=True)
        st.success("✅ LISTO 60 MIN 1080p")
        st.video(out)
        st.download_button("📥 DESCARGAR 1H HD 60MIN", open(out,"rb").read(), "1h_HD_60min.mp4", use_container_width=True)
