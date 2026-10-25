import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="ADAPTATIVO - FINAL FIX", layout="centered")
st.title("ADAPTATIVO - 1, 2, 3 Fotos")
st.write("Con 1, 2 o 3 fotos funciona igual + FADE")

# AUDIO
audio_file = st.file_uploader("1. MP3 de 3H (124MB)", type=["mp3","wav","m4a","ogg"], key="audio_final")

# FOTOS
st.markdown("### 2. Fotos (Orden fijo)")
c1, c2, c3 = st.columns(3)
with c1:
    f1 = st.file_uploader("Foto 1 - Obligatoria", type=["jpg","jpeg","png","webp"], key="f1_final")
    if f1: 
        st.image(f1, width=150)
        st.caption(f"✅ {f1.name}")
with c2:
    f2 = st.file_uploader("Foto 2 - Opcional", type=["jpg","jpeg","png","webp"], key="f2_final")
    if f2: 
        st.image(f2, width=150)
        st.caption(f"✅ {f2.name}")
with c3:
    f3 = st.file_uploader("Foto 3 - Opcional", type=["jpg","jpeg","png","webp"], key="f3_final")
    if f3: 
        st.image(f3, width=150)
        st.caption(f"✅ {f3.name}")

fotos = [f for f in [f1, f2, f3] if f is not None]

st.divider()

# ESTATUS Y BOTON SIEMPRE VISIBLE
if not audio_file:
    st.warning("Falta el audio de 124MB")
elif len(fotos) == 0:
    st.warning("Falta al menos la Foto 1")
else:
    st.success(f"Listo: Audio {audio_file.name} | {len(fotos)} foto(s)")
    st.info(f"Duración por foto: 3H / {len(fotos)} = {(3/len(fotos)):.1f}H cada una")

    if st.button("🎬 GENERAR VIDEO CON FADE - CLICK AQUI", type="primary", use_container_width=True):
        with st.spinner("Generando video de 3H... tarda 3-4 min..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = os.path.join(tmpdir, "audio.mp3")
                with open(audio_path, "wb") as f:
                    f.write(audio_file.read())
                
                audio = AudioFileClip(audio_path)
                dur_total = audio.duration

                img_paths = []
                for i, file in enumerate(fotos):
                    p = os.path.join(tmpdir, f"img_{i}.jpg")
                    with open(p, "wb") as out:
                        out.write(file.read())
                    img_paths.append(p)

                num = len(img_paths)
                dur_por_foto = dur_total / num
                fade = 1.5

                clips = [ImageClip(p).set_duration(dur_por_foto) for p in img_paths]

                if num == 1:
                    video_final = clips[0]
                else:
                    final_clips = [clips[0]]
                    for c in clips[1:]:
                        final_clips.append(c.crossfadein(fade))
                    video_final = concatenate_videoclips(final_clips, method="compose", padding=-fade)

                video_final = video_final.set_audio(audio).set_duration(dur_total)
                output_path = os.path.join(tmpdir, "final.mp4")
                video_final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.success("¡Video listo!")
                with open(output_path, "rb") as vf:
                    st.download_button("⬇️ DESCARGAR VIDEO MP4", vf, file_name="moonlight_3h.mp4", use_container_width=True)
