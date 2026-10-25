import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="ADAPTATIVO - ORDEN FIJO", layout="centered")
st.title("ADAPTATIVO - Orden Fijo")
st.caption("Foto 1, 2, 3 en orden - funciona en celular")

# 1. AUDIO - CUALQUIER PESO
audio_file = st.file_uploader(
    "1️⃣ AUDIO - Sube tu MP3 (129MB, 124MB, el que tengas)", 
    type=["mp3","wav","m4a","ogg","opus"],
    key="audio_orden_fijo"
)
if audio_file:
    st.success(f"Audio: {audio_file.name}")

st.divider()

# 2. FOTOS SEPARADAS - UNA DEBAJO DE OTRA - ORDEN FIJO
st.markdown("### 2️⃣ FOTOS EN ORDEN FIJO")
st.write("Sube en orden. Foto 1 es la primera del video, luego la 2, luego la 3.")

f1 = st.file_uploader(
    "📸 FOTO 1 - Primera del video (OBLIGATORIA)", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_1_orden"
)
if f1:
    st.image(f1, width=250)
    st.success(f"✅ Foto 1 lista: {f1.name} - Esta va PRIMERA")

f2 = st.file_uploader(
    "📸 FOTO 2 - Segunda del video (Opcional)", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_2_orden"
)
if f2:
    st.image(f2, width=250)
    st.success(f"✅ Foto 2 lista: {f2.name} - Esta va SEGUNDA")

f3 = st.file_uploader(
    "📸 FOTO 3 - Tercera del video (Opcional)", 
    type=["jpg","jpeg","png","webp"], 
    key="foto_3_orden"
)
if f3:
    st.image(f3, width=250)
    st.success(f"✅ Foto 3 lista: {f3.name} - Esta va TERCERA")

fotos = []
nombres_orden = []
if f1:
    fotos.append(f1)
    nombres_orden.append(f"1. {f1.name} (PRIMERA)")
if f2:
    fotos.append(f2)
    nombres_orden.append(f"2. {f2.name} (SEGUNDA)")
if f3:
    fotos.append(f3)
    nombres_orden.append(f"3. {f3.name} (TERCERA)")

st.divider()

# 3. BOTON
if not audio_file:
    st.warning("Falta el audio")
elif len(fotos) == 0:
    st.warning("Falta la Foto 1 - Toca el primer botón de Foto 1")
else:
    st.info(f"Orden final del video:")
    for n in nombres_orden:
        st.write(n)
    st.write(f"Cada foto durará {3/len(fotos):.1f} horas con FADE")

    if st.button("🎬 GENERAR VIDEO CON FADE EN ORDEN FIJO", type="primary", use_container_width=True):
        with st.spinner(f"Generando video de 3H con {len(fotos)} foto(s) en orden... No cierres"):
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
                st.success("¡Video listo en orden fijo con FADE!")
                with open(output_path, "rb") as vf:
                    st.download_button(
                        "⬇️ DESCARGAR VIDEO MP4", 
                        vf, 
                        file_name="moonlight_3h_orden_fijo.mp4",
                        use_container_width=True,
                        type="primary"
                    )
