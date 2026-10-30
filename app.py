import streamlit as st
import tempfile, os, subprocess, shutil
from pathlib import Path
import imageio_ffmpeg

st.set_page_config(page_title="Moonlight Maker V3 - Black Screen")
st.title("Moonlight Maker V3 - 1:30 imagen + Black Screen")

# 1. Obtener ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

image_file = st.file_uploader("1. Sube tu imagen de la ventana (la de la luna)", type=["png","jpg","jpeg"])
audio_file = st.file_uploader("2. Sube tu audio de Canva/Suno (29:58 o el que tengas)", type=["mp3","wav","m4a","aac"])

target_hours = st.number_input("Duración final en horas", value=3.0, min_value=0.5, max_value=12.0, step=0.5)
image_duration = st.number_input("Segundos con imagen al inicio", value=90, min_value=30, max_value=180, help="90 = 1 minuto 30 segundos")

if st.button("Crear video 3 HORAS") and image_file and audio_file:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        img_path = tmp_path / "image.png"
        audio_path = tmp_path / "audio.mp3"
        out_path = tmp_path / "final_3h.mp4"
        
        img_path.write_bytes(image_file.read())
        audio_path.write_bytes(audio_file.read())
        
        total_seconds = int(target_hours * 3600)
        black_seconds = total_seconds - image_duration
        
        st.info(f"Creando: {image_duration}s con imagen + {black_seconds}s en negro = {total_seconds}s total. Esto va a ser rápido...")
        progress = st.progress(0)

        # PASO 1: Video de 90s con tu imagen + audio (con fundido a negro al final de 2 seg)
        part1 = tmp_path / "part1.mp4"
        cmd1 = [
            ffmpeg_exe, "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-t", str(image_duration),
            "-vf", f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fade=t=out:st={image_duration-2}:d=2",
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest",
            str(part1)
        ]
        subprocess.run(cmd1, check=True)
        progress.progress(30)

        # PASO 2: Video negro de 2h58m con el mismo audio en loop
        part2 = tmp_path / "part2.mp4"
        cmd2 = [
            ffmpeg_exe, "-y",
            "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=30:d={black_seconds}",
            "-i", str(audio_path),
            "-filter_complex", f"[1:a]aloop=loop=-1:size=2e+09[a]",
            "-map", "0:v", "-map", "[a]",
            "-t", str(black_seconds),
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest",
            str(part2)
        ]
        subprocess.run(cmd2, check=True)
        progress.progress(70)

        # PASO 3: Unir los dos sin re-codificar (rapidísimo)
        list_file = tmp_path / "list.txt"
        list_file.write_text(f"file '{part1}'\nfile '{part2}'\n")
        cmd3 = [
            ffmpeg_exe, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(out_path)
        ]
        subprocess.run(cmd3, check=True)
        progress.progress(100)
        
        st.success("¡Listo! Video de 3 horas creado.")
        st.video(str(out_path))
        with open(out_path, "rb") as f:
            st.download_button("DESCARGAR VIDEO 3H", f, file_name=f"moonlight_{int(target_hours)}h_blackscreen.mp4")
