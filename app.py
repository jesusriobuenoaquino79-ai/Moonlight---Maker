import streamlit as st, tempfile, glob, os, time
from moviepy.editor import *
from PIL import Image

st.title("🌧️ Cabaña Lluviosa con Progreso")

audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
st.success(f"Musica: {audio_fijo} ✅")

imagen = st.file_uploader("Sube tu foto", type=["jpg","png","webp"])

if st.button("🚀 CREAR VIDEO 1 HORA", type="primary"):
    if not imagen:
        st.error("Sube la foto mi rey")
    else:
        # AQUI ESTA EL INDICADOR QUE ME PEDISTE
        barra = st.progress(0, text="Iniciando...")
        estado = st.status("🔄 En proceso...", expanded=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t:
            t.write(imagen.getvalue())
            img_path = t.name

        estado.write("✅ 1/5 Foto recibida")
        barra.progress(20, text="20% - Foto recibida")

        im = Image.open(img_path)
        im = im.resize((1280, 720))
        im.save(img_path)

        estado.write("✅ 2/5 Imagen optimizada a 720p")
        barra.progress(40, text="40% - Imagen lista")
        time.sleep(1)

        audio = AudioFileClip(audio_fijo)
        loops = int(3600 / audio.duration) + 1
        final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

        estado.write("✅ 3/5 Audio en bucle de 1 hora creado")
        barra.progress(70, text="70% - Audio listo - EMPEZANDO VIDEO (esto es lo que más demora)")

        video = ImageClip(img_path).set_duration(3600).set_audio(final_audio)
        out = tempfile.mktemp(suffix=".mp4")

        estado.write("⏳ 4/5 CREANDO VIDEO... No te salgas, esto demora 4-6 min")
        # Este es el paso lento
        video.write_videofile(out, fps=24, preset='ultrafast', threads=4, codec="libx264", audio_codec="aac", logger=None)

        barra.progress(95, text="95% - Video creado, preparando descarga")
        estado.write("✅ 5/5 ¡Video terminado!")
        estado.update(label="¡COMPLETADO! 🎉", state="complete")

        barra.progress(100, text="100% - ¡LISTO MI REY!")
        st.success("¡VIDEO LISTO!")
        st.balloons()
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name="cabana-lluviosa-1hora.mp4")
