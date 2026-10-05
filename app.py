import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

st.title("🎬 1H HD 720p - ESTABLE")

with st.form("form_estable"):
    musica = st.file_uploader("🎵 MP3", type=["mp3"], key="mp3_estable_720")
    c1,c2 = st.columns(2)
    with c1: foto1 = st.file_uploader("📷 Foto 1", type=["jpg","png","webp","jpeg"], key="f1_estable_720")
    with c2: foto2 = st.file_uploader("📷 Foto 2", type=["jpg","png","webp","jpeg"], key="f2_estable_720")
    intensidad = st.slider("Zoom", 0.05, 0.30, 0.12)
    vel = st.slider("Velocidad", 1, 10, 2)
    go = st.form_submit_button("🚀 CREAR 1H HD", type="primary", use_container_width=True)

if go:
    if not musica or not foto1 or not foto2:
        st.warning("Sube todo mi pana")
    else:
        bar = st.progress(0, text="Trabajando...")
        with tempfile.TemporaryDirectory() as tmp:
            audio = os.path.join(tmp,"a.mp3")
            with open(audio,"wb") as f: f.write(musica.getvalue())
            def prep(up, out):
                im = Image.open(up).convert("RGB")
                w,h = im.size
                r = max(1280/w, 720/h)*1.3
                im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                im = im.crop(((im.width-1280*1.3)//2,(im.height-720*1.3)//2,(im.width-1280*1.3)//2+int(1280*1.3),(im.height-720*1.3)//2+int(720*1.3)))
                im.resize((1536,864), Image.LANCZOS).save(out, quality=85)
            i1,i2 = os.path.join(tmp,"1.jpg"), os.path.join(tmp,"2.jpg")
            prep(foto1,i1); prep(foto2,i2)
            v1,v2,final = os.path.join(tmp,"v1.mp4"), os.path.join(tmp,"v2.mp4"), os.path.join(tmp,"final.mp4")
            z = f"1+{intensidad}*abs(sin(on*{vel*0.001}))"
            bar.progress(20, text="Foto 1 - 30m...")
            subprocess.run([FFMPEG,"-y","-loop","1","-framerate","24","-i",i1,"-t","1800","-vf",f"scale=1536:864,zoompan=z='{z}':d=1:s=1280x720:fps=24,scale=1280:720","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-crf","28",v1], check=True)
            bar.progress(50, text="Foto 2 - 30m...")
            subprocess.run([FFMPEG,"-y","-loop","1","-framerate","24","-i",i2,"-t","1800","-vf",f"scale=1536:864,zoompan=z='{z}':d=1:s=1280x720:fps=24,scale=1280:720","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-crf","28",v2], check=True)
            bar.progress(80, text="Uniendo...")
            subprocess.run([FFMPEG,"-y","-i",v1,"-i",v2,"-stream_loop","25","-i",audio,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=1:offset=1799,format=yuv420p[v]","-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-preset","ultrafast","-crf","28","-c:a","aac","-b:a","128k","-movflags","+faststart",final], check=True)
            bar.progress(100, text="Listo!")
            st.success("¡LISTO EN HD! No es SD")
            st.video(final)
            with open(final,"rb") as f: st.download_button("📥 DESCARGAR HD 720p", f.read(), "video-1h-HD.mp4", use_container_width=True, type="primary")
