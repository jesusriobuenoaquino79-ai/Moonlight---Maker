import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
st.title("1H DIRECTO - SIN 3/4")
mp3=st.file_uploader("MP3",type=["mp3"])
f1=st.file_uploader("Foto1",type=["jpg","png","webp"],key="1")
f2=st.file_uploader("Foto2",type=["jpg","png","webp"],key="2")

if st.button("CREAR 1H DIRECTO",use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3")
        open(au,"wb").write(mp3.getvalue())
        i1=os.path.join(tmp,"1.jpg")
        i2=os.path.join(tmp,"2.jpg")
        Image.open(f1).convert("RGB").save(i1)
        Image.open(f2).convert("RGB").save(i2)
        out="/tmp/final.mp4"
        st.write("⏳ Creando 1 hora directo (2 min)...")
        # 1 hora directa, 1fps para que no se cuelgue
        cmd=[FFMPEG,"-y","-loop","1","-r","1","-i",i1,"-loop","1","-r","1","-i",i2,"-i",au,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=2:offset=1798,format=yuv420p[v]","-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-crf","30","-preset","veryfast","-r","24","-c:a","aac","-b:a","96k","-movflags","+faststart","-shortest",out]
        subprocess.run(cmd,check=True)
        st.success("✅ LISTO 1 HORA")
        st.video(out)
        st.download_button("📥 DESCARGAR (70MB)",open(out,"rb").read(),"1h_2fotos.mp4")
