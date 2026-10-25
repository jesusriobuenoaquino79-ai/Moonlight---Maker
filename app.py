import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="ADAPTATIVO - FIX FOTOS", layout="centered")
st.title("ADAPTATIVO - 1, 2, 3 Fotos")
st.caption("Audio + Fotos con FADE suave")

# 1. AUDIO - SIN PESO FIJO
audio_file = st.file_uploader(
    "1️⃣ Sube tu MP3 ya hecho (1H, 2H, 3H - el que tengas)", 
    type=["mp3","wav","m4a","ogg","opus"],
    key="audio_unico"
)

# 2. FOTOS - AHORA UNO DEBAJO DEL OTRO PARA QUE SI SUBA EN EL CELU
st.markdown("### 2️⃣ Fotos (1 obligatoria, las otras opcionales)")

f1 = st.file_uploader(
    "Foto 1 - Obligatoria - Toca aqui", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_1_final_v2"
)
if f1:
    st.image(f1, width=200)
    st.success(f"Foto 1 cargada: {f1.name}")

f2 = st.file_uploader(
    "Foto 2 - Opcional - Toca aqui", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_2_final_v2"
)
if f2:
    st.image(f2, width=200)
    st.success(f"Foto 2 cargada: {f2.name}")

f3 = st.file_uploader(
    "Foto 3 - Opcional - Toca aqui", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_3_final_v2"
)
if f3:
    st.image(f3, width=200)
    st.success(f"Foto 3 cargada: {f3.name}")

fotos = [f for f in [f1, f2, f3] if f is not None]

st.divider()

# 3. BOTON QUE SIEMPRE APARECE
if not audio_file:
    st.warning("⬆️ Falta subir el audio")
elif len(fotos) == 0:
    st.warning("⬆️ Falta subir al menos Foto 1. Tócala arriba, ahora ya sube al primer toque.")
else:
    st.success(f"¡Todo listo! Audio: {audio_file.name} | {len(fotos)} foto(s) en orden fijo")
    
    if st.button("🎬 GENERAR VIDEO CON FADE", type="primary", use_container_width=True):
        with st.spinner(f"Generando video con {len(fotos)} foto(s)... Esto tarda 3-5 min, no cierres la ventana"):
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = os.path.join(tmpdir, "audio.mp3")
                with open(audio_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                audio = AudioFileClip(audio_path)
                dur_total = audio.duration

                img_paths = []
                for i, file in enumerate(fotos):
                    p = os.path.join(tmpdir, f"img_{i}.jpg")
                    with open(p, "wb") as out:
                        out.write(file.getbuffer())
                    img_paths.append(p)

                num = len(img_paths)
                dur_por_foto = dur_total / num
                fade = 1.0

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
                video_final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)

                st.balloons()
                st.success("¡Video de 3H listo con FADE!")
                with open(output_path, "rb") as vf:
                    st.download_button(
                        "⬇️ DESCARGAR VIDEO MP4", 
                        vf, 
                        file_name="video_3h_fade.mp4",
                        use_container_width=True,
                        type="primary"
                    )
