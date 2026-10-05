import streamlit as st, tempfile, os, subprocess, time
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H CROSSFADE SUAVE", layout="centered")

if 'generando' not in st.session_state:
    st.session_state.generando = False

bloqueado = st.session_state.generando
st.title("🎬 1H - Crossfade Suave + Fijas")

# SUBIDORES FUERA DEL FORM - 1 TOQUE
st.write("### 1. Sube tus archivos")
musica = st.file_uploader("🎵 MP3 (2:50 a 3:10)", type=["mp3"], disabled=bloqueado, key="mp3_final")
c1,c2 = st.columns(2)
with c1: foto1 = st.file_uploader("📷 Foto 1 (0-30m)", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f1_final")
with c2: foto2 = st.file_uploader("📷 Foto 2 (30-60m)", type=["jpg","jpeg","png","webp"], disabled=bloqueado, key="f2_final")

if musica: st.success(f"✅ Audio: {musica.name}")
if foto1: st.success(f"✅ Foto 1 OK")
if foto2: st.success(f"✅ Foto 2 OK")

st.divider()
txt = "⏳ GENERANDO 40 SEG - BLOQUEADO 🔒" if bloqueado else "🚀 CREAR 1H CON CROSSFADE"
crear = st.button(txt, type="primary", use_container_width=True, disabled=bloqueado)

if crear:
    if not musica or not foto1 or not foto2:
        st.warning("⚠️ Sube los 3 archivos")
    else:
        st.session_state.generando = True
        st.rerun()

# PROCESO
pct = st.empty()
bar = st.empty()
ti = st.empty()
info = st.empty()

if st.session_state.generando and musica and foto1 and foto2:
    t0=time.time()
    pbar = bar.progress(0)
    pct.markdown("## 🔒 0% - INICIANDO")

    with tempfile.TemporaryDirectory() as tmp:
        try:
            au=os.path.join(tmp,"a.mp3")
            with open(au,"wb") as f: f.write(m
