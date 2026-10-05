import streamlit as st, tempfile, os, subprocess, time
from PIL import Image
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H RAPIDO 5FPS", layout="centered")
if 'gen' not in st.session_state:
    st.session_state.gen=False
bloq=st.session_state.gen
st.title("1H - 5FPS RAPIDO")
musica=st.file_uploader("MP3",type=["mp3"],disabled=bloq)
c1,c2=st.columns(2)
with c1:
    foto1=st.file_uploader("Foto 1",type=["jpg","jpeg","png","webp"],disabled=bloq,key="f1")
with c2:
    foto2=st.file_uploader("Foto 2",type=["jpg","jpeg","png","webp"],disabled=bloq,key="f2")
txt="GENERANDO..." if bloq else "CREAR 1H - 90 SEG"
go=st.button(txt,use_container_width=True,disabled=bloq)
if go:
    if not musica or not foto1 or not foto2:
        st.warning("Sube 3")
    else:
        st.session_state.gen=True
        st.rerun()
bar=st.empty()
pct=st.empty()
if st.session_state.gen and musica and foto1 and foto2:
    t0=time.time()
    p=bar.progress(0)
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3")
        with open(au,"wb") as f:
            f.write(musica.getvalue())
        def prep(up,out):
            Image.open(up).convert("RGB").resize((1280,720)).save(out,"JPEG",quality=80)
        i1=os.path.join(tmp,"1.jpg")
        i2=os.path.join(tmp,"2.jpg")
        prep(foto1,i1)
        prep(foto2,i2)
        v1=os.path.join(tmp,"v1.mp4")
        v2=os.path.join(tmp,"v2.mp4")
        final=os.path.join(tmp,"final.mp4")
        pct.write("20% Foto1 fade in - 5FPS super rapido")
        p.progress(20)
        # 5 FPS = 5 veces mas rapido, Streamlit si aguanta
        subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i1,"-t","1800","-vf","scale=1280:720,fade=t=in:st=0:d=2","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-r","5",v1],check=True)
        pct.write("60% Foto2 - ya paso del 20%!")
        p.progress(60)
        subprocess.run([FFMPEG,"-y","-loop","1","-r","5","-i",i2,"-t","1800","-vf","scale=1280:720","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-r","5",v2],check=True)
        pct.write("85% Uniendo 1H")
        p.progress(85)
        subprocess.run([FFMPEG,"-y","-i",v1,"-i",v2,"-stream_loop","22","-i",au,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=2:offset=1798,fade=t=out:st=3598:d=2[v]","-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-preset","ultrafast","-r","5","-c:a","aac","-b:a","128k",final],check=True)
        pct.write("100% LISTO!")
        p.progress(100)
        st.success(f"Listo en {int(time.time()-t0)}s")
        st.video(final)
        with open(final,"rb") as f:
            st.download_button("DESCARGAR 1H",f.read(),"video1h.mp4")
        st.session_state.gen=False
