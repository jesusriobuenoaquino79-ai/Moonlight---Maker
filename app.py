import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="ADAPTATIVO - 1,2,3 Fotos - FIX", layout="centered")
st.title("ADAPTATIVO - 1, 2, 3 Fotos - FIX")
st.write("MP3 Ya Hecho - 1H, 3H, lo que sea")

# 1. AUDIO
audio_file = st.file_uploader("MP3 Ya Hecho (1H, 3H, lo que sea)", type=["mp3","wav","m4a","ogg"], key="audio")
st.caption("200MB per file • MP3, WAV, M4A, OGG")

# 2. FOTOS - 3 BOTONES SEPARADOS - ORDEN FIJO
st.markdown("### 📸 Fotos - Orden Fijo")
col1, col2, col3 = st.columns(3)

with col1:
    foto1 = st.file_uploader("Foto 1 (Obligatoria)", type=["jpg","jpeg","png","webp"], key="f1")
    if foto1:
        st.success(f"✅ {foto1.name}")
        st.image(foto1, width=150)

with col2:
    foto2 = st.file_uploader("Foto 2 (Opcional)", type=["jpg","jpeg","png","webp"], key="f2")
    if foto2:
        st.success(f"✅ {foto2.name}")
        st.image(foto2, width=150)

with col3:
    foto3 = st.file_uploader("Foto 3 (Opcional)", type=["jpg","jpeg","png","webp"], key="f3")
    if foto3:
        st.success(f"✅ {foto3.name}")
        st.image(foto3, width=150)

fotos = []
if foto1: fotos.append(foto1)
if foto2: fotos.append(foto2)
if foto3: fotos.append(foto3)

# 3. GENERAR
if audio_file and len(fotos) > 0:
    st.info(f"Audio: {audio_file.name} | Fotos: {len(fotos)} en orden fijo")

    if st.button("Generar Video con FADE", type="primary"):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "audio.mp3")
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            
            audio = AudioFileClip(audio_path)
            duracion_total = audio.duration
            st.write(f"Duración: {duracion_total/3600:.2f} horas")

            img_paths = []
            for i, f in enumerate(fotos):
                p = os.path.join(tmpdir, f"img_{i}.jpg")
                with open(p, "wb") as out:
                    out.write(f.read())
                img_paths.append(p)

            num = len(img_paths)
            dur_por_foto = duracion_total / num
            fade = 1.5

            clips = []
            for p in img_paths:
                clips.append(ImageClip(p).set_duration(dur_por_foto))

            if num == 1:
                video_final = clips[0]
            else:
                final_clips = [clips[0]]
                for c in clips[1:]:
                    final_clips.append(c.crossfadein(fade))
                video_final = concatenate_videoclips(final_clips, method="compose", padding=-fade)

            video_final = video_final.set_audio(audio).set_duration(duracion_total)
            output_path = os.path.join(tmpdir, "final.mp4")
            video_final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

            st.success("¡Video listo!")
            with open(output_path, "rb") as vf:
                st.download_button("Descargar Video MP4", vf, file_name="moonlight_3h_fade.mp4")
