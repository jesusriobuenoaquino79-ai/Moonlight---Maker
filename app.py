import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H 2 Fotos", layout="centered")
st.title("1H - 2 Fotos en 2 Min")
mp3=st.file_uploader("MP3",type=["mp3"])
f1=st.file_uploader("Foto1 (pueblo)",type=["jpg","png","webp"],key="1")
f2=st.file_uploader("Foto2 (nevado)",type=["jpg","png","webp"],key="2")

if st.button("CREAR 1H CON 2 FOTOS",use_container_width=True):
    if not mp3 or not f1 or not f2:
        st.error("¡Sube MP3, Foto1 y Foto2!")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            st.write("⏳ 1/4 Preparando fotos...")
            au=os.path.join(tmp,"a.mp3")
            open(au,"wb").write(mp3.getvalue())
            def prep(u,o):
                Image.open(u).convert("RGB").resize((1280,720)).save(o,"JPEG",quality=65)
            i1=os.path.join(tmp,"1.jpg")
            i2=os.path.join(tmp,"2.jpg")
            prep(f1,i1)
            prep(f2,i2)

            st.write("⏳ 2/4 Creando clip de 2 fotos (1 min)...")
            v1=os.path.join(tmp,"v1.mp4")
            v2=os.path.join(tmp,"v2.mp4")
            base=os.path.join(tmp,"base.mp4")
            subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i1,"-t","152","-vf","scale=1280:720,fade=t=in:st=0:d=2","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5",v1],check=True)
            subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i2,"-t","152","-vf","scale=1280:720","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5",v2],check=True)
            subprocess.run([FFMPEG,"-y","-i",v1,"-i",v2,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=2:offset=150,format=yuv420p[v]","-map","[v]","-t","300","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5",base],check=True)

            st.write("⏳ 3/4 Repitiendo a 1 hora...")
            final="/tmp/final_1h_2fotos.mp4"
            list_txt=os.path.join(tmp,"list.txt")
            with open(list_txt,"w") as f:
                for _ in range(12): f.write(f"file '{base}'\n")
            subprocess.run([FFMPEG,"-y","-f","concat","-safe","0","-i",list_txt,"-stream_loop","12","-i",au,"-t","3600","-c:v","libx264","-crf","32","-preset","ultrafast","-r","5","-c:a","aac","-b:a","96k","-movflags","+faststart","-shortest",final],check=True)

            st.success("✅ ¡LISTO! 2 fotos - 1 hora")
            st.video(final)
            with open(final,"rb") as f:
                st.download_button("📥 DESCARGAR 1H - 2 FOTOS (65MB)",f.read(),"pueblo_nevado_1H_2fotos.mp4","video/mp4",use_container_width=True)
