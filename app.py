import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.title("1H HD - TRUCO 5 SEG LOOP")
st.cache_data.clear()

mp3 = st.file_uploader("MP3 3min", type=["mp3"])
f1 = st.file_uploader("Foto1", type=["jpg","png","webp"], key="1")
f2 = st.file_uploader("Foto2", type=["jpg","png","webp"], key="2")

if f1 and f2 and mp3 and st.button("CREAR 1H EN 60 SEG", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3"); open(au,"wb").write(mp3.getvalue())
        i1=os.path.join(tmp,"1.jpg"); i2=os.path.join(tmp,"2.jpg")
        for u,o in [(f1,i1),(f2,i2)]:
            Image.open(u).convert("RGB").resize((1280,720)).save(o,"JPEG",quality=80)
        
        v1_5=os.path.join(tmp,"v1_5.mp4"); v2_5=os.path.join(tmp,"v2_5.mp4")
        v1=os.path.join(tmp,"v1.mp4"); v2=os.path.join(tmp,"v2.mp4")
        silent="/tmp/silent.mp4"; final="/tmp/final.mp4"

        st.write("⏳ 1/4: 5 seg foto1...")
        subprocess.run([FFMPEG,"-y","-loop","1","-i",i1,"-t","5","-vf","format=yuv420p","-r","24","-c:v","libx264","-preset","ultrafast",v1_5], check=True)
        st.write("⏳ 2/4: Estirando a 30min...")
        subprocess.run([FFMPEG,"-y","-stream_loop","359","-i",v1_5,"-c","copy",v1], check=True)
        
        st.write("⏳ 3/4: 5 seg foto2 + estirar...")
        subprocess.run([FFMPEG,"-y","-loop","1","-i",i2,"-t","5","-vf","format=yuv420p","-r","24","-c:v","libx264","-preset","ultrafast",v2_5], check=True)
        subprocess.run([FFMPEG,"-y","-stream_loop","359","-i",v2_5,"-c","copy",v2], check=True)

        st.write("⏳ 4/4: Uniendo + Audio 60min...")
        lst=os.path.join(tmp,"list.txt"); open(lst,"w").write(f"file '{v1}'\nfile '{v2}'\n")
        subprocess.run([FFMPEG,"-y","-f","concat","-safe","0","-i",lst,"-c","copy",silent], check=True)
        subprocess.run([FFMPEG,"-y","-stream_loop","21","-i",au,"-i",silent,"-t","3600","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","128k","-movflags","+faststart",final], check=True)

        st.success("✅ LISTO 60:00 EN 60 SEG")
        st.video(final)
        st.download_button("📥 DESCARGAR 1H", open(final,"rb").read(), "1H_60min_HD.mp4", use_container_width=True)
