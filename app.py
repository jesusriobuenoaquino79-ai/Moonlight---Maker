import streamlit as st, tempfile, glob, os
from moviepy.editor import *
from PIL import Image

st.set_page_config(page_title="Moonlight Dreams", page_icon="🌙")
st.title("🌙 Moonlight Dreams - Video 1 Hora")

# Busca MP3
try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Música: {audio_fijo} ✅ - {AudioFileClip(audio_fijo).duration/60:.1f} min")
except:
    st.error("No hay MP3 en la carpeta. Súbele uno.")
    st.stop()

st.write("Sube las 2 fotos del video - Ya no toca darle 2 veces")

foto1 = st.file_uploader("Foto 1 (0-30 min)", type=["jpg","png","webp","jpeg"], key="f1")
foto2 = st.file_uploader("Foto 2 (30-60 min)", type=["jpg","png","webp","jpeg"], key="f2")

# Esto es lo que arregla que toque darle 2 veces
if foto1:
    st.image(foto1, width=200, caption="Foto 1 lista ✅")
if foto2:
    st.image(foto2, width=200, caption="Foto 2 lista ✅")

boton = st.button("🚀 CREAR VIDEO 1 HORA", type="primary", disabled=not (foto1 and foto2))

if boton:
    barra = st.progress(0, text="Iniciando...")
    estado = st.status("🔄 En proceso...", expanded=True)

    # Guardar fotos
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t1:
        t1.write(foto1.getvalue())
        img_path1 = t1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as t2:
        t2.write(foto2.getvalue())
        img_path2 = t2.name

    def preparar_img(path):
        im = Image.open(path).convert("RGB")
        # Recorte inteligente para que no se estire
        w, h = im.size
        target_w, target_h = 1280, 720
        ratio = max(target_w/w, target_h/h)
        new_w, new_h = int(w*ratio), int(h*ratio)
        im = im.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - target_w)//2
        top = (new_h - target_h)//2
        im = im.crop((left, top, left+target_w, top+target_h))
        im.save(path, "JPEG", quality=90)

    preparar_img(img_path1)
    preparar_img(img_path2)

    estado.write("✅ Fotos listas")
    barra.progress(30)

    audio = AudioFileClip(audio_fijo)
    loops = int(3600 // audio.duration) + 2
    final_audio = concatenate_audioclips([audio]*loops).subclip(0, 3600)

    estado.write("✅ Audio en loop 1 hora")
    barra.progress(60)

    # VIDEO CON FUNDIDO SUAVE - 100% compatible
    clip1 = ImageClip(img_path1, duration=1800)
    clip2 = ImageClip(img_path2, duration=1800).crossfadein(1.5)

    video_final = concatenate_videoclips([clip1, clip2], method="compose")
    video_final = video_final.set_audio(final_audio)

    estado.write("⏳ Renderizando... 4-6 min, no cierres")
    barra.progress(85)

    out = tempfile.mktemp(suffix=".mp4")
    video_final.write_videofile(out, fps=24, preset='ultrafast', threads=4, codec="libx264", audio_codec="aac", logger=None)

    barra.progress(100)
    estado.update(label="¡COMPLETADO! 🎉", state="complete")

    st.success("¡VIDEO LISTO MI REY!")
    st.balloons()
    st.video(out)
    with open(out,"rb") as f:
        st.download_button("📥 DESCARGAR VIDEO FINAL", f, file_name="moonlight-1hora.mp4", type="primary")

    # Limpieza
    for p in [img_path1, img_path2, out]:
        try: os.remove(p)
        except: pass
