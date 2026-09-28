import streamlit as st, tempfile, glob, os, time
from moviepy.editor import *
from PIL import Image

st.title("🌙 Moonlight Dreams - Video 1 Hora (2 Fotos)")

try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Musica: {audio_fijo} ✅")
except:
    st.error("No hay MP3 en la carpeta mi rey")
    st.stop()

# UN SOLO UPLOADER PARA 2 FOTOS - MAS ESTABLE
fotos = st.file_uploader("Sube las 2 fotos (selecciona las 2 a la vez)", type=["jpg","png","webp"], accept_multiple_files=True)

if st.button("🚀 CREAR VIDEO 1 HORA", type="primary"):
    if not fotos or len(fotos) < 2:
        st.error(f"¡Mi rey, tienes que subir 2 fotos! Solo subiste {len(fotos) if fotos else 0}. Selecciónalas las 2 juntas.")
    else:
        foto1 = fotos[0]
        foto2 = fotos[1]

        barra = st.progress(0, text="Iniciando...")
        estado = st.status("🔄 En proceso...", expanded=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t1:
            t1.write(foto1.getvalue())
            img_path1 = t1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t2:
            t2.write(foto2.getvalue())
            img_path2 = t2.name

        estado.write("✅ 1/6 Fotos recibidas")
        barra.progress(15, text="15% - Fotos recibidas")

        for p in [img_path1, img_path2]:
            im = Image.open(p)
            im = im.resize((1280, 720))
            im.save(p)

        estado.write("✅ 2/6 Imágenes optimizadas a 720p")
        barra.progress(30, text="30% - Imágenes listas")

        audio = AudioFileClip(audio_fijo)
        loops = int(3600 / audio.duration) + 1
        final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

        estado.write("✅ 3/6 Audio 1 hora creado")
        barra.progress(50, text="50% - Audio listo")

        estado.write("⏳ 4/6 Creando clip 1...")
        barra.progress(65, text="65% - Clip 1 (0-30min)")
        clip1 = ImageClip(img_path1, duration=1800).resize((1280,720))
        clip1 = clip1.resize(lambda t: 1 + 0.00008 * t).set_position(("center","center"))

        estado.write("⏳ 5/6 Creando clip 2...")
        barra.progress(80, text="80% - Clip 2 (30-60min)")
        clip2 = ImageClip(img_path2, duration=1800).resize((1280,720))
        clip2 = clip2.resize(lambda t: 1.12 - 0.00008 * t).set_position(("center","center"))
        clip2 = clip2.crossfadein(2)

        video_final = concatenate_videoclips([clip1, clip2], method="compose")
        video_final = video_final.set_audio(final_audio)

        estado.write("⏳ 6/6 RENDERIZANDO... No te salgas, 5-7 min")
        barra.progress(90, text="90% - Renderizando")
        out = tempfile.mktemp(suffix=".mp4")
        video_final.write_videofile(out, fps=24, preset='ultrafast', threads=4, codec="libx264", audio_codec="aac", logger=None)

        barra.progress(100, text="100% - ¡LISTO MI REY!")
        estado.update(label="¡COMPLETADO! 🎉", state="complete")

        st.success("¡VIDEO LISTO CON 2 FOTOS!")
        st.balloons()
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("📥 DESCARGAR VIDEO 1 HORA (2 FOTOS)", f, file_name="moonlight-dreams-1hora-2fotos.mp4")
