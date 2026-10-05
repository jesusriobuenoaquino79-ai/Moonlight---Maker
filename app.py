import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.title("FINAL 2 PASOS - 1H HD 60:00")

mp3 = st.file_uploader("MP3 3min", type=["mp3"])
f1 = st.file_uploader("Foto1", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2", type=["jpg","png","webp"], key="2")

if f1 and f2 and mp3 and st.button("CREAR EN 2 PASOS", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au = os.path.join(tmp,"a.mp3")
        open(au,"wb").write(mp3.getvalue())
        i1 = os.path.join(tmp,"1.jpg"); i2 = os.path.join(tmp,"2.jpg")
        for u,o in [(f1,i1),(f2,i2)]:
            Image.open(u).convert("RGB").resize((1920,1080)).save(o,"JPEG",quality=90)
        silent = "/tmp/silent.mp4"
        final = "/tmp/final_1h_hd.mp4"

        st.write("⏳ Paso 1/2: Video sin audio...")
        cmd1=[FFMPEG,"-y","-framerate","1","-loop","1","-t","1800","-i",i1,"-framerate","1","-loop","1","-t","1800","-i",i2,"-filter_complex","[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[v0][v1]xfade=transition=fade:duration=3:offset=1797,format=yuv420p,fps=30[v]","-map","[v]","-t","3600","-c:v","libx264","-preset","veryfast","-crf","20","-r","30","-an",silent]
        subprocess.run(cmd1, check=True)

        st.write("⏳ Paso 2/2: Pegando audio 60min...")
        cmd2=[FFMPEG,"-y","-stream_loop","21","-i",au,"-i",silent,"-t","3600","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",final]
        subprocess.run(cmd2, check=True)

        st.success("✅ LISTO 60:00 HD REAL")
        st.video(final)
        st.download_button("📥 DESCARGAR", open(final,"rb").read(), "1H_HD_60min.mp4", use_container_width=True)
