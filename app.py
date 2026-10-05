import streamlit as st, tempfile, os, subprocess, time
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H RAPIDO", layout="centered")

if 'generando' not in st.session_state:
    st.session_state.generando = False

st.title("⚡ 1H RAPIDO 5 MIN - BLOQUEADO")

bloqueado = st.session_state.generando

with st.form("form_rapido"):
    musica = st.file_uploader("🎵 MP3", type=["mp3"], disabled=bloqueado)
    c1,c2 = st.columns(2)
    with c1: foto1 = st.file_uploader("📷 Foto 1", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f1r")
    with c2: foto2 = st.file_uploader("📷 Foto 2", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f2r")
    zoom = st.slider("Zoom", 0.05, 0.25, 0.10, disabled=bloqueado)
    vel = st.slider("Velocidad", 1, 10, 2, disabled=bloqueado)
    txt = "⏳ GENERANDO 5 MIN - NO TOQUES" if bloqueado else "🚀 CREAR RAPIDO 1H"
    go = st.form_submit_button(txt, type="primary", use_container_width=True, disabled=bloqueado)

pct = st.empty()
bar = st.empty()
ti = st.empty()
info = st.empty()

if go:
    if not musica or not foto1 or not foto2:
        st.warning("Sube todo")
        st.session_state.generando=False
    else:
        st.session_state.generando=True
        t0=time.time()
        pbar = bar.progress(0)
        pct.markdown("## 0% INICIANDO - BLOQUEADO 🔒")

        with tempfile.TemporaryDirectory() as tmp:
            try:
                au=os.path.join(tmp,"a.mp3")
                with open(au,"wb") as f: f.write(musica.getvalue())

                def prep(up,out):
                    im=Image.open(up).convert("RGB")
                    im = im.resize((1280,720), Image.LANCZOS)
                    im.save(out, "JPEG", quality=80)

                i1=os.path.join(tmp,"1.jpg"); i2=os.path.join(tmp,"2.jpg")
                pct.markdown("### 5% Preparando fotos"); pbar.progress(5)
                prep(foto1,i1); prep(foto2,i2)

                v1=os.path.join(tmp,"v1.mp4"); v2=os.path.join(tmp,"v2.mp4"); final=os.path.join(tmp,"final.mp4")
                z=f"1+{zoom}*sin(on*{vel*0.002})"

                pct.markdown("### 20% Foto1 0-30m - Tarda 2 min"); pbar.progress(20)
                info.info("⏳ Normal que se quede 2 min en 20%, no está congelado")
                # MAS RAPIDO: 15 fps y d=2 (procesa la mitad de frames)
                subprocess.run([FFMPEG,"-y","-loop","1","-framerate","15","-i",i1,"-t","1800","-vf",f"scale=1280:720,zoompan=z='{z}':d=2:s=1280x720:fps=15","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-crf","30",v1], check=True)

                pct.markdown("### 55% Foto1 lista - Foto2 30-60m"); pbar.progress(55)
                ti.write(f"⏱️ {int(time.time()-t0)}s - Ya va más de la mitad")
                subprocess.run([FFMPEG,"-y","-loop","1","-framerate","15","-i",i2,"-t","1800","-vf",f"scale=1280:720,zoompan=z='{z}':d=2:s=1280x720:fps=15","-c:v","libx264","-pix_fmt","yuv420p","-preset","ultrafast","-crf","30",v2], check=True)

                pct.markdown("### 85% Uniendo + audio loop"); pbar.progress(85)
                subprocess.run([FFMPEG,"-y","-i",v1,"-i",v2,"-stream_loop","25","-i",au,"-filter_complex","[0:v][1:v]xfade=transition=fade:duration=1:offset=1799,format=yuv420p[v]","-map","[v]","-map","2:a","-t","3600","-c:v","libx264","-preset","ultrafast","-crf","30","-c:a","aac","-b:a","96k","-movflags","+faststart",final], check=True)

                pct.markdown("## ✅ 100% LISTO"); pbar.progress(100)
                ti.write(f"⏱️ Total: {int(time.time()-t0)//60}m {int(time.time()-t0)%60}s")
                info.success("¡Terminado!")
                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR", f.read(), "1h-rapido.mp4", type="primary", use_container_width=True)
                st.session_state.generando=False
            except Exception as e:
                st.session_state.generando=False
                st.error(f"{e}")
