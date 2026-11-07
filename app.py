import streamlit as st
import tempfile, subprocess
from pathlib import Path
import imageio_ffmpeg

st.set_page_config(page_title="Moonlight V10 SIMPLE")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

st.title("Moonlight V10 - De 30min a 3H")

video_file = st.file_uploader("Sube tu video de 30min (mp4)", type=["mp4","mov"])

if st.button("Crear 3H FINAL") and video_file:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_video = tmp_path / "input.mp4"
        out_path = tmp_path / "final_3h.mp4"
        input_video.write_bytes(video_file.read())
        
        total = 10800 # 3 horas
        primeros = 12

        st.info("Paso 1: sacando el audio de tus 30 min...")
        audio_file = tmp_path / "audio.aac"
        r1 = subprocess.run([ffmpeg_exe, "-y", "-i", str(input_video), "-vn", "-c:a", "aac", "-b:a", "128k", str(audio_file)], capture_output=True, text=True)
        if r1.returncode != 0:
            st.error("Falló sacando audio:")
            st.code(r1.stderr[-2000:])
            st.stop()

        st.info("Paso 2: creando 12s + negro + audio x6 (3h)... esto tarda 2-3 min, no le des click otra vez")
        # -stream_loop 5 = repite el audio 6 veces en total (30min x 6 = 180min = 3h)
        cmd = [
            ffmpeg_exe, "-y",
            "-i", str(input_video),
            "-stream_loop", "5", "-i", str(audio_file),
            "-f", "lavfi", "-i", f"color=c=black:s=1280x720:r=5:d={total-primeros}",
            "-filter_complex",
            f"[0:v]trim=0:{primeros},setpts=PTS-STARTPTS,scale=1280:720,fps=30[v1];"
            f"[2:v]setpts=PTS-STARTPTS[v2];"
            f"[v1][v2]concat=n=2:v=1:a=0,format=yuv420p[vout]",
            "-map", "[vout]",
            "-map", "1:a",
            "-t", str(total),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "copy",
            "-shortest",
            str(out_path)
        ]
        r2 = subprocess.run(cmd, capture_output=True, text=True)
        if r2.returncode != 0:
            st.error("Falló creando video:")
            st.code(r2.stderr[-3000:])
        else:
            st.success("¡Listo! 3H creado.")
            with open(out_path, "rb") as f:
                st.download_button("DESCARGAR VIDEO FINAL 3H", f, file_name="moonlight_3h_FINAL.mp4")
