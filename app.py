import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.title("1H HD 720p - PARA STREAMLIT 1GB")
st.cache_data.clear()

mp3 = st.file_uploader("MP3 3min", type=["mp3"])
f1 = st.file_uploader("Foto1", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2", type=["jpg","png","webp"], key="2")

if f1 and f2 and mp3 and st.button("CREAR 1H - NO PASA DE RAM", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3"); open(au,"wb").write(mp3.getvalue())
        i1=os.path.join(tmp,"1.jpg"); i2=os.path.join(tmp,"2.jpg")
        for u,o in [(f1,i1),(f2,i2)]:
            Image.open(u).convert("RGB").resize((1280,720)).save(o,"JPEG",quality=85)
        v1=os.path.join(tmp,"v1.mp4"); v2=os.path.join(tmp,"v2.mp4")
        silent="/tmp/silent.mp4"; final="/tmp/final.mp4"
        st.write("⏳ 1/3 Foto1 30min...")
        subprocess.run([FFMPEG,"-y","-loop","1","-i",i1,"-t","1800","-vf","format=yuv420p","-r","24","-c:v","libx264","-preset","ultrafast","-crf","26",v1], check=True)
        st.write("⏳ 2/3 Foto2 30min...")
        subprocess.run([FFMPEG,"-y","-loop","1","-i",i2,"-t","1800","-vf","format=yuv420p","-r","24","-c:v","libx264","-preset","ultrafast","-crf","26",v2], check=True)
        st.write("⏳ 3/3 Uniendo + Audio 60min...")
        lst=os.path.join(tmp,"list.txt"); open(lst,"w").write(f"file '{v1}'\nfile '{v2}'\n")
        subprocess.run([FFMPEG,"-y","-f","concat","-safe","0","-i",lst,"-c","copy",silent], check=True)
        subprocess.run([FFMPEG,"-y","-stream_loop","21","-i",au,"-i",silent,"-t","3600","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","128k","-movflags","+faststart",final], check=True)
        st.success("✅ LISTO 60:00 HD - NO SE PASO DE RAM")
        st.video(final)
        st.download_button("📥 DESCARGAR 1H 60:00", open(final,"rb").read(), "1H_60min_HD.mp4", use_container_width=True)
