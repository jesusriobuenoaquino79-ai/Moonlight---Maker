import streamlit as st, tempfile, os, subprocess, time
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H HD BLOQUEADO", page_icon="🔒", layout="centered")

if 'generando' not in st.session_state:
    st.session_state.generando = False

st.title("🎬 1H HD - CONGELADO")

# SI ESTA GENERANDO, TODO BLOQUEADO
bloqueado = st.session_state.generando

with st.form("form_bloqueado"):
    musica = st.file_uploader("🎵 MP3 2:50 a 3:10", type=["mp3"], disabled=bloqueado, key="mp3_block")
    col1, col2 = st.columns(2)
    with col1:
        foto1 = st.file_uploader("📷 Foto 1 (0-30m)", type=["jpg","png","webp","jpeg"], disabled=bloqueado, key="f1_block")
    with col2:
        foto2 = st.file_uploader("📷 Foto 2 (30-60m)", type=["jpg","png","webp","jpeg"], disabled=bloqueado, key="f2_block")

    zoom_intensidad = st.slider("Zoom", 0.05, 0.30, 0.12, disabled=bloqueado)
    velocidad = st.slider("Velocidad", 1, 10, 2, disabled=bloqueado)

    texto_boton = "⏳ GENERANDO... NO TOQUES NADA" if bloqueado else "🚀 CREAR 1H HD"
    submitted = st.form_submit_button(texto_boton, type="primary", use_container_width=True, disabled=bloqueado)

# LUGAR PARA PORCENTAJE GIGANTE
porcentaje_texto = st.empty()
barra = st.empty()
tiempo_texto = st.empty()
estado_texto = st.empty()

if submitted:
    if not musica or not foto1 or not foto2:
        st.warning("⚠️ Sube las 3 cosas")
        st.session_state.generando = False
    else:
        st.session_state.generando = True
        inicio = time.time()

        # MOSTRAR QUE ESTA BLOQUEADO
        porcentaje_texto.markdown("## 🔒 0% - INICIANDO - NO MUEVAS NADA")
        progress_bar = barra.progress(0)
        estado_texto.info("🔒 Valores congelados - Zoom y Velocidad bloqueados")

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                audio_in = os.path.join(tmpdir, "in.mp3")
                with open(audio_in, "wb") as f:
                    f.write(musica.getvalue())

                def prep(f_up, out):
                    im = Image.open(f_up).convert("RGB")
                    w,h = im.size
                    r = max(1280/w, 720/h) * 1.3
                    im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                    im = im.crop(((im.width-int(1280*1.3))//2, (im.height-int(720*1.3))//2, (im.width-int(1280*1.3))//2+int(1280*1.3), (im.height-int(720*1.3))//2+int(720*1.3)))
                    im.resize((1536, 864), Image.LANCZOS).save(out, "JPEG", quality=85)

                img1 = os.path.join(tmpdir, "img1.jpg")
                img2 = os.path.join(tmpdir, "img2.jpg")

                porcentaje_texto.markdown("### 📸 10% - PREPARANDO FOTOS")
                progress_bar.progress(10)
                tiempo_texto.write(f"⏱️ Tiempo: {int(time.time()-inicio)}s")
                prep(foto1, img1)
                prep(foto2, img2)

                v1 = os.path.join(tmpdir, "v1.mp4")
                v2 = os.path.join(tmpdir, "v2.mp4")
                final = os.path.join(tmpdir, "final_1h.mp4")

                z = f"1+{zoom_intensidad}*abs(sin(on*{velocidad*0.001}))"

                # FOTO 1 - 30 MIN
                porcentaje_texto.markdown("### 🎬 20% - CREANDO FOTO 1 (0-30 min) - ESTO TARDA 4-6 MIN, ES NORMAL")
                progress_bar.progress(20)
                estado_texto.warning("⏳ NO SE HA CONGELADO - Está trabajando, espera... Foto 1 es la más lenta")
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img1, "-t", "1800",
                    "-vf", f"scale=1536:864,zoompan=z='{z}':d=1:s=1280x720:fps=24,scale=1280:720",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "28", v1
                ], check=True)

                porcentaje_texto.markdown("### 🎬 50% - FOTO 1 LISTA - CREANDO FOTO 2 (30-60 min)")
                progress_bar.progress(50)
                tiempo_texto.write(f"⏱️ Tiempo: {int(time.time()-inicio)}s - Ya pasó la mitad")
                estado_texto.success("✅ Foto 1 terminada - Ahora Foto 2")

                # FOTO 2 - 30 MIN
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-framerate", "24", "-i", img2, "-t", "1800",
                    "-vf", f"scale=1536:864,zoompan=z='{z}':d=1:s=1280x720:fps=24,scale=1280:720",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "28", v2
                ], check=True)

                porcentaje_texto.markdown("### 🔗 80% - UNIENDO VIDEOS + AUDIO LOOP 1 HORA")
                progress_bar.progress(80)
                tiempo_texto.write(f"⏱️ Tiempo: {int(time.time()-inicio)}s - Casi listo")

                subprocess.run([
                    FFMPEG, "-y", "-i", v1, "-i", v2, "-stream_loop", "25", "-i", audio_in,
                    "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=1:offset=1799,format=yuv420p[v]",
                    "-map", "[v]", "-map", "2:a", "-t", "3600",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", final
                ], check=True)

                porcentaje_texto.markdown("## ✅ 100% - ¡VIDEO TERMINADO!")
                progress_bar.progress(100)
                tiempo_texto.write(f"⏱️ Tiempo total: {int(time.time()-inicio)//60} min {int(time.time()-inicio)%60} seg")
                estado_texto.success("🎉 ¡LISTO! Ya puedes descargar")

                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR 1H HD", f.read(), file_name="video-1hora-HD-BLOQUEADO.mp4", type="primary", use_container_width=True)

                # DESBLOQUEAR AL TERMINAR
                st.session_state.generando = False

            except Exception as e:
                st.session_state.generando = False
                porcentaje_texto.markdown("### ❌ ERROR")
                st.error(f"Error: {e}")
                st.exception(e)

if st.session_state.generando:
    st.warning("🔒 GENERANDO... No toques zoom ni velocidad, están congelados por seguridad")
