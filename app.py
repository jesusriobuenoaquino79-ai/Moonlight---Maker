import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="ADAPTATIVO - 1,2,3 Fotos - FIX", layout="centered")
st.title("ADAPTATIVO - 1, 2, 3 Fotos - FIX")
st.write("MP3 Ya Hecho - 1H, 3H, lo que sea")

# 1. AUDIO
audio_file = st.file_uploader("MP3 Ya Hecho", type=["mp3","wav","m4a","ogg"], key="audio")
st.caption("200MB per file • MP3, WAV, M4A, OGG")

# 2. FOTOS
fotos = st.file_uploader("Sube 1, 2 o 3 Fotos", type=["jpg","png","webp","jpeg"], 
                         accept_multiple_files=True, key="fotos")
st.caption("200MB per file • JPG, PNG, WEBP")

if audio_file and fotos:
    st.info(f"Audio: {audio_file.name} | Fotos: {len(fotos)}")
    
    if len(fotos) > 3:
        st.error("Solo máximo 3 fotos")
    else:
        if st.button("Generar Video con FADE", type="primary"):
            with tempfile.TemporaryDirectory() as tmpdir:
                # Guardar audio
                audio_path = os.path.join(tmpdir, "audio.mp3")
                with open(audio_path, "wb") as f:
                    f.write(audio_file.read())
                
                audio = AudioFileClip(audio_path)
                duracion_total = audio.duration
                st.write(f"Duración audio: {duracion_total/3600:.2f} horas")

                # Guardar imagenes
                img_paths = []
                for i, f in enumerate(fotos):
                    p = os.path.join(tmpdir, f"img_{i}.jpg")
                    with open(p, "wb") as out:
                        out.write(f.read())
                    img_paths.append(p)

                # Crear clips repartidos
                num = len(img_paths)
                dur_por_foto = duracion_total / num
                fade = 1.5  # segundos de fade entre imagen e imagen

                clips = []
                for path in img_paths:
                    clips.append(ImageClip(path).set_duration(dur_por_foto))

                # Concatenar con crossfade
                if num == 1:
                    video_final = clips[0]
                else:
                    # video con fade
                    video_final = concatenate_videoclips(clips, method="compose")
                    # Para el fade suave usamos crossfade
                    # Truco: ponemos cada clip con crossfadein excepto el primero
                    final_clips = [clips[0]]
                    for c in clips[1:]:
                        final_clips.append(c.crossfadein(fade))
                    video_final = concatenate_videoclips(final_clips, method="compose", padding=-fade)

                video_final = video_final.set_audio(audio).set_duration(duracion_total)
                
                output_path = os.path.join(tmpdir, "video_final.mp4")
                video_final.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
                
                st.success("Video listo!")
                with open(output_path, "rb") as vf:
                    st.download_button("Descargar Video MP4", vf, file_name="moonlight_3h_fade.mp4")
