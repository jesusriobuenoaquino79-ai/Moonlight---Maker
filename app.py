import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image
import tempfile, os

st.set_page_config(page_title="Moonlight 3H Light", layout="centered")
st.title("Moonlight 3H - Versión Ligera")
st.caption("Arregla error Code: 1ST - Para audio de 130MB")

audio_file = st.file_uploader("1️⃣ AUDIO 130MB", type=["mp3","wav","m4a","ogg","opus"])
f1 = st.file_uploader("2️⃣ FOTO 1", type=["jpg","jpeg","png","webp"])
f2 = st.file_uploader("3️⃣ FOTO 2 (opcional)", type=["jpg","jpeg","png","webp"])

fotos = [f for f in [f1, f2] if f is not None]

if audio_file and len(fotos)>0:
    st.success(f"Audio: {audio_file.size/1024/1024:.1f} MB | Fotos: {len(fotos)} - OK")
    if st.button("🎬 GENERAR (ahora sí, ligero)", type="primary", use_container_width=True):
        with st.spinner("Generando... No toques nada, tarda 3-4 min, es normal que parezca congelado"):
            with tempfile.TemporaryDirectory() as tmp:
                audio_path = os.path.join(tmp, "audio.mp3")
                with open(audio_path, "wb") as o:
                    o.write(audio_file.getbuffer())
                
                audio = AudioFileClip(audio_path)
                
                img_paths=[]
                for i, f in enumerate(fotos):
                    # REDUCIR FOTO A 720p para no explotar memoria
                    im = Image.open(f)
                    im.thumbnail((1280,720))
                    p = os.path.join(tmp, f"img{i}.jpg")
                    im.save(p, "JPEG", quality=85)
                    img_paths.append(p)

                dur = audio.duration / len(img_paths)
                clips = [ImageClip(p).set_duration(dur) for p in img_paths]

                if len(clips)==1:
                    final = clips[0]
                else:
                    fc=[clips[0]]
                    for c in clips[1:]:
                        fc.append(c.crossfadein(1.0))
                    final = concatenate_videoclips(fc, method="compose", padding=-1.0)

                final = final.set_audio(audio).set_duration(audio.duration)
                out = os.path.join(tmp, "final.mp4")
                final.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast", logger=None)
                
                st.balloons()
                st.success("¡Listo! Ya no se cayó")
                with open(out,"rb") as vf:
                    st.download_button("⬇️ DESCARGAR VIDEO", vf, file_name="moonlight_3h.mp4", use_container_width=True, type="primary")
else:
    st.info("Sube audio 130MB y Foto 1. Usa 2 fotos máximo para que no de error 1ST")
