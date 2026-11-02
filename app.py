import streamlit as st
import tempfile, subprocess
from pathlib import Path
import imageio_ffmpeg

st.set_page_config(page_title="Moonlight V9.1 FINAL")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

st.title("Moonlight FINAL - 12s + 3H Negro")

video_file = st.file_uploader("Sube tu video de Canva (mp4)", type=["mp4","mov"])

if st.button("Crear 3H FINAL sin corte") and video_file:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_video = tmp_path / "input.mp4"
        out_path = tmp_path / "final_3h.mp4"
        input_video.write_bytes(video_file.read())
        
        total = 10800 # 3 horas
        primeros = 12
        
        bar = st.progress(0)
        st.info("1. Creando audio continuo de 3h sin cortes...")

        # PASO 1: UN SOLO AUDIO DE 3H CONTINUO - Así no se corta a los 12s
        full_audio = tmp_path / "full_audio.aac"
        subprocess.run([
            ffmpeg_exe, "-y", "-i", str(input_video),
            "-filter_complex", "[0:a]aloop=loop=-1:size=2e+09[a]",
            "-map", "[a]", "-t", str(total), "-c:a", "aac", "-ar", "48000",
            str(full_audio)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        bar.progress(40)

        st.info("2. Creando video: 12s tuyos + negro...")
        # PASO 2: Video de 12s solo video sin audio
        part1_v = tmp_path / "p1_v.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-i", str(input_video), "-t", str(primeros), "-an", "-c:v", "libx264", "-preset", "ultrafast", str(part1_v)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Video negro del resto del tiempo
        black_v = tmp_path / "black_v.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=30:d={total-primeros}", "-t", str(total-primeros), "-c:v", "libx264", "-preset", "ultrafast", str(black_v)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Unimos los 2 videos sin audio
        list_txt = tmp_path / "list.txt"
        list_txt.write_text(f"file '{part1_v}'\nfile '{black_v}'\n")
        video_sin_audio = tmp_path / "video_sin_audio.mp4"
        subprocess.run([ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", str(list_txt), "-c", "copy", str(video_sin_audio)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        bar.progress(80)

        st.info("3. Uniendo todo...")
        # PASO 3: Juntar video completo + audio continuo
        subprocess.run([
            ffmpeg_exe, "-y",
            "-i", str(video_sin_audio),
            "-i", str(full_audio),
            "-map", "0:v", "-map", "1:a",
            "-c", "copy", "-t", str(total),
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        bar.progress(100)
        st.success("¡Listo! 12s + negro 3H sin corte de música.")
        
        with open(out_path, "rb") as f:
            st.download_button("DESCARGAR VIDEO FINAL 3H", f, file_name="moonlight_12s_black_3h_FINAL.mp4")
