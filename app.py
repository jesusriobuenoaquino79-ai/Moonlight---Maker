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

fotos = st.file_uploader("Sube las 2 fotos (selecciona las 2 a la vez)", type=["jpg","png","webp"], accept_multiple_files=True)

if st.button("🚀 CREAR VIDEO 1 HORA", type="primary"):
    if not fotos or len(fotos) < 2:
        st.error(f"¡Mi rey, sube 2 fotos! Solo subiste {len(fotos) if fotos else 0}")
    else:
        barra = st.progress(0, text="Iniciando...")
        estado = st.status("🔄 En proceso...", expanded=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t1:
            t1.write(fotos[0].getvalue())
            img_path1 = t1.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t2:
            t2.write(fotos[1].getvalue())
            img_path2 = t2.name

        estado.write("✅ 1/5 Fotos recibidas")
        barra.progress(20, text="20% - Fotos recibidas")

        for p in [img_path1, img_path2]:
            im = Image.open(p)
            im = im.resize((1280, 720))
            im.save(p)

        estado.write("✅ 2/5 Imágenes optimizadas")
        barra.progress(40, text="40% - Imágenes listas")

        audio = AudioFileClip(audio_fijo)
        loops = int(3600 / audio.duration) + 1
        final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

        estado.write("✅ 3/5 Audio 1 hora creado")
        barra.progress(60, text="60% - Audio listo")

        # CLIPS SIN EFECTO LAMBDA - VERSION ESTABLE
        estado.write("⏳ 4/5 Creando clips...")
        barra.progress(80, text="80% - Creando video de 2 partes")

        clip1 = ImageClip(img_path1, duration=1800).resize((1280,720))
        clip2 = ImageClip(img_path2, duration=1800).resize((1280,720))

        # Fundido de 1 segundo entre fotos
        clip2 = clip2.crossfadein(1)
        video_final = concatenate_videoclips([clip1, clip2], method="compose")
        video_final = video_final.set_audio(final_audio)

        estado.write("⏳ 5/5 RENDERIZANDO... 4-6 min, no te salgas")
        barra.progress(90, text="90% - Renderizando")

        out = tempfile.mktemp(suffix=".mp4")
        video_final.write_videofile(out, fps=24, preset='ultrafast', threads=4, codec="libx264", audio_codec="aac", logger=None)

        barra.progress(100, text="100% - ¡LISTO MI REY!")
        estado.update(label="¡COMPLETADO! 🎉", state="complete")

        st.success("¡VIDEO LISTO CON 2 FOTOS!")
        st.balloons()
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name="moonlight-dreams-2fotos.mp4")
