import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H FULL HD ZOOM", page_icon="🎬", layout="centered")
st.title("🎬 1 HORA FULL HD 1080p - ZOOM VIVO")

with st.form("upload_form_hd"):
    musica = st.file_uploader("🎵 MP3 2:50 a 3:10", type=["mp3"], key="mp3_hd_1080_final")
    col1, col2 = st.columns(2)
    with col1:
        foto1 = st.file_uploader("📷 Foto 1 (0-30m)", type=["jpg","png","webp","jpeg"], key="f1_hd_1080_final")
    with col2:
        foto2 = st.file_uploader("📷 Foto 2 (30-60m)", type=["jpg","png","webp","jpeg"], key="f2_hd_1080_final")

    zoom_intensidad = st.slider("Intensidad Zoom", 0.05, 0.30, 0.12)
    velocidad = st.slider("Velocidad", 1, 10, 2)
    submitted = st.form_submit_button("🚀 CREAR VIDEO 1H FULL HD", type="primary", use_container_width=True)

if submitted:
    if not musica or not foto1 or not foto2:
        st.warning("⚠️ Sube las 3 cosas: MP3 + Foto 1 + Foto 2")
    else:
        barra = st.progress(0, text="Iniciando...")
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                audio_in = os.path.join(tmpdir, "in.mp3")
                with open(audio_in, "wb") as f:
                    f.write(musica.getvalue())

                def prep(f_up, out):
                    im = Image.open(f_up).convert("RGB")
                    w,h = im.size
                    # FIX HD: Forzamos todo a 1920x1080
                    r = max(1920/w, 1080/h) * 1.4
                    im = im.resize((int(w*r), int(h*r)), Image.LANCZOS)
                    im = im.crop(((im.width-int(1920*1.4))//2, (im.height-int(1080*1.4))//2, (im.width-int(1920*1.4))//2+int(1920*1.4), (im.height-int(1080*1.4))//2+int(1080*1.4)))
                    im_big = im.resize((2304, 1296), Image.LANCZOS)
                    im_big.save(out, "JPEG", quality=92)

                img1 = os.path.join(tmpdir, "img1.jpg")
                img2 = os.path.join(tmpdir, "img2.jpg")

                barra.progress(10, text="Preparando fotos en HD...")
                prep(foto1, img1)
                prep(foto2, img2)

                st.success("✅ Fotos HD agarradas!")
                c1, c2 = st.columns(2)
                with c1: st.image(img1, caption="Foto 1 HD OK")
                with c2: st.image(img2, caption="Foto 2 HD OK")

                v1 = os.path.join(tmpdir, "v1.mp4")
                v2 = os.path.join(tmpdir, "v2.mp4")
                final = os.path.join(tmpdir, "final_1h.mp4")

                zoom_formula = f"1+{zoom_intensidad}*abs(sin(on*{velocidad*0.001}))"

                barra.progress(20, text="Foto 1 - 30 min FULL HD...")
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-framerate", "30", "-i", img1, "-t", "1800",
                    "-vf", f"scale=2304:1296,zoompan=z='{zoom_formula}':d=1:s=1920x1080:fps=30,scale=1920:1080",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "26", v1
                ], check=True)

                barra.progress(50, text="Foto 2 - 30 min FULL HD...")
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-framerate", "30", "-i", img2, "-t", "1800",
                    "-vf", f"scale=2304:1296,zoompan=z='{zoom_formula}':d=1:s=1920x1080:fps=30,scale=1920:1080",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "26", v2
                ], check=True)

                barra.progress(80, text="Uniendo + Audio Loop 1H...")
                subprocess.run([
                    FFMPEG, "-y", "-i", v1, "-i", v2, "-stream_loop", "25", "-i", audio_in,
                    "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=1:offset=1799,format=yuv420p[v]",
                    "-map", "[v]", "-map", "2:a", "-t", "3600",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", final
                ], check=True)

                barra.progress(100, text="¡Listo FULL HD!")
                st.success("¡VIDEO FULL HD 1080p LISTO! 🎬 YA NO ES SD")
                st.balloons()
                st.video(final)
                with open(final,"rb") as f:
                    st.download_button("📥 DESCARGAR FULL HD 1080p", f.read(), file_name="video-1hora-FULL-HD-1080p.mp4", type="primary", use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")
                st.exception(e)
