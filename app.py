import streamlit as st, tempfile, glob, os
from moviepy.editor import *
from PIL import Image

st.title("🌙 Moonlight Dreams - Video 1 Hora")

try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Musica: {audio_fijo} ✅")
except:
    st.error("No hay MP3 en la carpeta")
    st.stop()

# FORMULARIO PARA QUE NO SE BORRE EN CELULAR
with st.form("form_fotos"):
    st.write("Sube las 2 fotos del video")
    foto1 = st.file_uploader("Foto 1 (0-30 min)", type=["jpg","png","webp"], key="f1_form")
    foto2 = st.file_uploader("Foto 2 (30-60 min)", type=["jpg","png","webp"], key="f2_form")
    boton = st.form_submit_button("🚀 CREAR VIDEO 1 HORA", type="primary")

if boton:
    if not foto1 or not foto2:
        st.error("¡Mi rey, falta una foto! Sube las 2.")
    else:
        barra = st.progress(0, text="Iniciando...")
        estado = st.status("🔄 En proceso...", expanded=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t1:
            t1.write(foto1.getvalue())
            img_path1 = t1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t2:
            t2.write(foto2.getvalue())
            img_path2 = t2.name

        estado.write("✅ Fotos recibidas")
        barra.progress(30)

        for p in [img_path1, img_path2]:
            im = Image.open(p)
            im = im.resize((1280, 720))
            im.save(p)

        audio = AudioFileClip(audio_fijo)
        loops = int(3600 / audio.duration) + 1
        final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

        estado.write("✅ Audio listo")
        barra.progress(60)

        clip1 = ImageClip(img_path1, duration=1800).resize((1280,720))
        clip2 = ImageClip(img_path2, duration=1800).resize((1280,720))
        clip2 = clip2.crossfadein(1)
        video_final = concatenate_videoclips([clip1, clip2], method="compose")
        video_final = video_final.set_audio(final_audio)

        estado.write("⏳ Renderizando... 4-6 min")
        barra.progress(90)

        out = tempfile.mktemp(suffix=".mp4")
        video_final.write_videofile(out, fps=24, preset='ultrafast', threads=4, codec="libx264", audio_codec="aac", logger=None)

        barra.progress(100)
        estado.update(label="¡COMPLETADO! 🎉", state="complete")

        st.success("¡VIDEO LISTO!")
        st.balloons()
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("📥 DESCARGAR VIDEO", f, file_name="moonlight-2fotos.mp4")
