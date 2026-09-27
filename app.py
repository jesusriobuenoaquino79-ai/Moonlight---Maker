import streamlit as st
from PIL import Image
import tempfile, os
from moviepy.editor import ImageClip, AudioFileClip, afx

st.set_page_config(page_title="Moonlight Maker", page_icon="🌙")
st.title("Maker - 1 HORA")
st.write("Sube 1 imagen + 1 audio de 3 min y te creo video de 1 HORA en bucle")

# TRUCO: ahora acepta todo tipo de imagen y tiene imagen por defecto
image_file = st.file_uploader("1. Imagen bonita", type=["jpg","jpeg","png","webp","heic","bmp"])
usar_default = st.checkbox("No puedo subir imagen, usar imagen por defecto de luna 🌙")

audio_file = st.file_uploader("2. Audio corto (3 min GRATIS)", type=["mp3","wav","m4a","ogg","opus"])
titulo = st.text_input("Titulo", "Moonlight Dreams - 1 Hour")

if st.button("✨ CREAR VIDEO DE 1 HORA"):
    if not audio_file:
        st.error("Sube el audio primero mi rey")
    elif not image_file and not usar_default:
        st.error("Sube la imagen o marca 'usar imagen por defecto'")
    else:
        with st.spinner("Creando video de 1 hora... espera 2 min"):
            try:
                # Si no hay imagen, creamos una negra con luna
                if usar_default or not image_file:
                    img = Image.new('RGB', (1920, 1080), color=(10, 10, 30))
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                        img.save(tmp_img.name)
                        img_path = tmp_img.name
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                        img = Image.open(image_file).convert("RGB").resize((1920,1080))
                        img.save(tmp_img.name)
                        img_path = tmp_img.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_aud:
                    tmp_aud.write(audio_file.read())
                    aud_path = tmp_aud.name

                audio = AudioFileClip(aud_path)
                final_audio = audio.fx(afx.audio_loop, duration=3600)
                video = ImageClip(img_path, duration=3600).set_audio(final_audio).set_fps(24)
                out_path = os.path.join(tempfile.gettempdir(), "moonlight_1h.mp4")
                video.write_videofile(out_path, codec="libx264", audio_codec="aac", logger=None)
                
                st.success("¡VIDEO DE 1 HORA LISTO MI REY!")
                st.video(out_path)
                with open(out_path, "rb") as f:
                    st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name=f"{titulo}.mp4")
            except Exception as e:
                st.error(f"Error: {e}")
