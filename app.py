import streamlit as st
import tempfile, subprocess
from pathlib import Path
import imageio_ffmpeg

st.set_page_config(page_title="Video Maker V8 - Final Rapido")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

st.title("Video Maker V8 - Final")

destino = st.radio("¿Para qué canal?", ["Moonlight Dreams - 12s + 3H Negro (RÁPIDO)", "Cabaña - Video 29:58 + 1 Foto = 1H"])

st.divider()

if destino == "Moonlight Dreams - 12s + 3H Negro (RÁPIDO)":
    st.success("MODO BLACK SCREEN - Sin fade, ultra rápido")
    st.write("Subes tu video de Canva y te saco 12s + resto negro 3h")
    
    video_file = st.file_uploader("Sube tu VIDEO de Canva (mp4)", type=["mp4","mov"], key="moon")

    if st.button("Crear 3H Black Screen") and video_file:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_video = tmp_path / "input.mp4"
            out_path = tmp_path / "final_3h.mp4"
            input_video.write_bytes(video_file.read())
            
            image_duration = 12
            total_seconds = 10800
            black_seconds = total_seconds - image_duration
            
            bar = st.progress(0)
            st.info(f"{image_duration}s con imagen + {black_seconds}s negro = 3H. Sin renderizar, 10 segundos.")

            part1 = tmp_path / "part1.mp4"
            subprocess.run([ffmpeg_exe, "-y", "-i", str(input_video), "-t", str(image_duration), "-c", "copy", str(part1)], check=True)
            bar.progress(30)

            audio_loop = tmp_path / "audio.aac"
            subprocess.run([ffmpeg_exe, "-y", "-i", str(input_video), "-filter_complex", "[0:a]aloop=loop=-1:size=2e+09[a]", "-map", "[a]", "-t", str(black_seconds), "-c:a", "aac", str(audio_loop)], check=True)
            bar.progress(60)

            black_one_sec = tmp_path / "black1s.mp4"
            subprocess.run([ffmpeg_exe, "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:r=30:d=1", "-c:v", "libx264", "-preset", "ultrafast", "-t", "1", str(black_one_sec)], check=True)
            
            black_long = tmp_path / "black_long.mp4"
            subprocess.run([ffmpeg_exe, "-y", "-stream_loop", str(black_seconds-1), "-i", str(black_one_sec), "-i", str(audio_loop), "-t", str(black_seconds), "-c", "copy", str(black_long)], check=True)
            bar.progress(85)

            list_file = tmp_path / "list.txt"
            list_file.write_text(f"file '{part1}'\nfile '{black_long}'\n")
            subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(out_path)], check=True)
            bar.progress(100)

            st.success("Listo Moonlight 3H Black Screen - Sin fade")
            with open(out_path, "rb") as f:
                st.download_button("DESCARGAR 3H", f, file_name="moonlight_3h_black_fast.mp4")

else:
    st.subheader("Cabaña - Video 29:58 + 1 Foto = 1 Hora (CON FADE)")
    st.write("Este SÍ lleva fade, porque es de imagen a imagen")
    
    video_file = st.file_uploader("Video 29:58 con imagen 1", type=["mp4","mov"], key="cab_v")
    img2 = st.file_uploader("Segunda foto", type=["jpg","png","jpeg"], key="cab_i2")

    if st.button("Crear 1H Cabaña") and video_file and img2:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_video = tmp_path / "input.mp4"
            p2 = tmp_path / "img2.jpg"
            out_path = tmp_path / "final_1h.mp4"
            input_video.write_bytes(video_file.read())
            p2.write_bytes(img2.read())

            st.info("Creando 1H con fade entre las 2 imágenes")
            cmd = [
                ffmpeg_exe, "-y",
                "-i", str(input_video),
                "-loop", "1", "-t", "1798", "-i", str(p2),
                "-filter_complex",
                "[0:v]fade=t=out:st=1796:d=2[v0];"
                "[1:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0002,1.3)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',fade=t=in:st=0:d=2,fps=30[v1];"
                "[v0][v1]concat=n=2:v=1:a=0[v];"
                "[0:a]aloop=loop=-1:size=2e+09[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", "-t", "3596",
                str(out_path)
            ]
            subprocess.run(cmd, check=True)
            st.success("Listo Cabaña 1H con fade")
            with open(out_path, "rb") as f:
                st.download_button("DESCARGAR 1H CABAÑA", f, file_name="cabana_1h_fade.mp4")
