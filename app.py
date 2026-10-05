import streamlit as st
import tempfile
import os
import subprocess
import time
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H CROSSFADE SUAVE", layout="centered")

if 'generando' not in st.session_state:
    st.session_state.generando = False

bloqueado = st.session_state.generando
st.title("🎬 1H - Crossfade Suave + Fijas")

st.write("### 1. Sube tus archivos")
musica = st.file_uploader("🎵 MP3 (2:50 a 3:10)", type=["mp3"], disabled=bloqueado, key="mp3_final_ok")
c1,c2 = st.columns(2)
with c1:
    foto1 = st.file_uploader("📷 Foto 1 (0-30m)", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f1_final_ok")
with c2:
    foto2 = st.file_uploader("📷 Foto 2 (30-60m)", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f2_final_ok")

if musica:
    st.success(f"✅ Audio: {musica.name}")
if foto1:
    st.success("✅ Foto 1 OK")
if foto2:
    st.success("✅ Foto 2 OK")

st.divider()
txt = "⏳ GENERANDO 40 SEG - BLOQUEADO" if bloqueado else "🚀 CREAR 1H CON CROSSFADE"
crear = st.button(txt, type="primary", use_container_width=True, disabled=bloqueado)

if crear:
    if not musica or not foto1 or not foto2:
        st.warning("Sube los 3 archivos")
    else:
        st.session_state.generando = True
        st.rerun()

pct = st.empty()
bar = st.empty()
ti = st.empty()
info = st.empty()

if st.session_state.generando and musica and foto1 and foto2:
    t0 = time.time()
    pbar = bar.progress(0)
    pct.markdown("## 🔒 0% - INICIANDO")

    with tempfile.TemporaryDirectory() as tmp:
        try:
            au = os.path.join(tmp, "a.mp3")
            with open(au, "wb") as f:
                f.write(musica.getvalue())

            def prep(up, out):
                img = Image.open(up).convert("RGB")
                img = img.resize((1280, 720), Image.LANCZOS)
                img.save(out, "JPEG", quality=85)

            i1 = os.path.join(tmp, "1.jpg")
            i2 = os.path.join(tmp, "2.jpg")
            pct.markdown("### 10% Preparando fotos")
            pbar.progress(10)
            prep(foto1, i1)
            prep(foto2, i2)

            v1 = os.path.join(tmp, "v1.mp4")
            v2 = os.path.join(tmp, "v2.mp4")
            final = os.path.join(tmp, "final.mp4")

            pct.markdown("### 20% Foto 1 con Fade In suave")
            pbar.progress(20)
            info.info("Entrada suave 2 seg - Imagen fija - 15 seg")
            subprocess.run([FFMPEG, "-y", "-loop", "1", "-i", i1, "-t", "1800", "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fade=t=in:st=0:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "28", "-r", "24", v1], check=True)

            pct.markdown("### 55% Foto 2 fija")
            pbar.progress(55)
            ti.write(f"Tiempo: {int(time.time()-t0)}s")
            subprocess.run([FFMPEG, "-y", "-loop", "1", "-i", i2, "-t", "1800", "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "28", "-r", "24", v2], check=True)

            pct.markdown("### 85% Crossfade medio + loop audio")
            pbar.progress(85)
            subprocess.run([FFMPEG, "-y", "-i", v1, "-i", v2, "-stream_loop", "25", "-i", au, "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=2:offset=1798,format=yuv420p,fade=t=out:st=3598:d=2[v]", "-map", "[v]", "-map", "2:a", "-t", "3600", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", final], check=True)

            pct.markdown("## ✅ 100% LISTO")
            pbar.progress(100)
            ti.write(f"Total: {int(time.time()-t0)}s")
            info.success("Listo!")
            st.balloons()
            st.video(final)
            with open(final, "rb") as f:
                st.download_button("📥 DESCARG
