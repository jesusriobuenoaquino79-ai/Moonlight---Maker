import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="Moonlight 3H", layout="centered")
st.title("Moonlight - Video 3H con FADE")

audio_file = st.file_uploader("1. Sube tu MP3 (130MB)", type=["mp3","wav","m4a","ogg"])

f1 = st.file_uploader("2. Foto 1", type=["jpg","jpeg","png","webp"])
f2 = st.file_uploader("3. Foto 2 (opcional)", type=["jpg","jpeg","png","webp"])
f3 = st.file_uploader("4. Foto 3 (opcional)", type=["jpg","jpeg","png","webp"])

fotos = [f for f in [f1, f2, f3] if f is not None]

if audio_file and len(fotos) > 0:
    st.success(f"Audio: {audio_file.name} | Fotos: {len(fotos)}")
    
    if st.button("Generar Video"):
        with st.spinner("Generando... tarda 4 min"):
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

                dur_por_foto = dur_total / len(img_paths)
                
                clips = [ImageClip(p).set_duration(dur_por_foto) for p in img_paths]

                if len(clips) == 1:
                    video_final = clips[0]
                else:
                    # FADE suave de 1 segundo
                    final_clips = [clips[0]]
                    for c in clips[1:]:
                        final_clips.append(c.crossfadein(1.0))
                    video_final = concatenate_videoclips(final_clips, method="compose", padding=-1.0)

                video_final = video_final.set_audio(audio).set_duration(dur_total)
                
                output_path = os.path.join(tmpdir, "final.mp4")
                video_final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.success("¡Listo!")
                with open(output_path, "rb") as vf:
                    st.download_button("DESCARGAR VIDEO", vf, file_name="moonlight_3h.mp4")
else:
    st.info("Sube el audio de 130MB y al menos la Foto 1")
