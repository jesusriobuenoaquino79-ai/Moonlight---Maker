import streamlit as st, tempfile, glob, os
from moviepy.editor import *

st.title("🌧️ Cabaña Lluviosa")

# Agarra tu música nueva automático
audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
st.write(f"Musica: {audio_fijo} ✅")

imagen = st.file_uploader("Sube tu foto", type=["jpg","png","webp"])

if st.button("CREAR VIDEO 1 HORA"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t:
        t.write(imagen.getvalue())
        img = t.name
    audio = AudioFileClip(audio_fijo)
    final_audio = concatenate_audioclips([audio]*int(3600/audio.duration+1)).subclip(0,3600)
    video = ImageClip(img).set_duration(3600).set_audio(final_audio)
    out = tempfile.mktemp(suffix=".mp4")
    video.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    st.success("¡Listo!")
    st.download_button("DESCARGAR VIDEO", open(out,"rb"), "cabana-lluviosa-1hora.mp4")
