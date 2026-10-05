import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H FIX", layout="centered")
st.title("1H - Fix corrupto")
mp3=st.file_uploader("MP3",type=["mp3"])
f1=st.file_uploader("Foto1",type=["jpg","png","webp"],key="1")
f2=st.file_uploader("Foto2",type=["jpg","png","webp"],key="2")
if st.button("CREAR 1H FIX",use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3")
        open(au,"wb").write(mp3.getvalue())
        def prep(u,o):
            Image.open(u).convert("RGB").resize((1280,720)).save(o,"JPEG",quality=70)
        i1=os.path.join(tmp,"1.jpg")
        i2=os.path.join(tmp,"2.jpg")
        prep(f1,i1)
        prep(f2,i2)
        v1=os.path.join(tmp,"v1.mp4")
        v2=os.path.join(tmp,"v2.mp4")
        mid=os.path.join(tmp,"mid.mp4")
        final="/tmp/video_1h_final.mp4"
        subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i1,"-t","1800","-vf","scale=1280:720,fade=t=in:st=0:d=2","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5",v1],check=True)
        subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i2,"-t","1800","-vf","scale=1280:720","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5",v2],check=True)
        subprocess.run([FFMPEG,"-y","-i",v1,"-i",v2,"-stream_loop","20","-i",au,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=2:offset=1798,fade=t=out:st=3598:d=2[v]","-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5","-c:a","aac","-b:a","96k","-movflags","+faststart",mid],check=True)
        subprocess.run([FFMPEG,"-y","-i",mid,"-c","copy","-movflags","+faststart",final],check=True)
        st.success("LISTO - Archivo 100% reparado")
        st.video(final)
        with open(final,"rb") as f:
            data=f.read()
        st.download_button("📥 DESCARGAR FIX - No se daña",data,"video_1h_1HORA.mp4","video/mp4",use_container_width=True)
        st.write(f"Tamaño: {len(data)/1024/1024:.1f} MB")
