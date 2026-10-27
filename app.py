import streamlit as st
import tempfile, os, subprocess

st.set_page_config(page_title="Moonlight - 1 HORA", layout="centered")
st.title("Moonlight - MODO CANVA 1 HORA")
st.caption("Sube tu video de 29:58 + tu audio de 60min - Te lo duplica a 1 hora con fade suave")

video_file = st.file_uploader("1️⃣ VIDEO CANVA 29:58", type=["mp4","mov","mkv"], key="video_canva")
audio_file = st.file_uploader("2️⃣ AUDIO 60min (las 3 pistas)", type=["mp3","wav","m4a","ogg","opus"], key="audio_60")

if video_file and audio_file:
    st.success(f"Video: {video_file.size/1024/1024:.1f} MB | Audio: {audio_file.size/1024/1024:.1f} MB")
    if st.button("🎬 GENERAR VIDEO 1 HORA - 59:56", type="primary", use_container_width=True):
        with st.spinner("Generando tu video de 1 hora... 2-4 minutos, no cierres la ventana"):
            with tempfile.TemporaryDirectory() as tmp:
                video_path = os.path.join(tmp, "canva.mp4")
                with open(video_path, "wb") as o:
                    o.write(video_file.getbuffer())

                audio_path = os.path.join(tmp, "audio.mp3")
                with open(audio_path, "wb") as o:
                    o.write(audio_file.getbuffer())

                out = os.path.join(tmp, "final_1hora.mp4")
                
                cmd = [
                    "ffmpeg","-y",
                    "-i", video_path,
                    "-i", audio_path,
                    "-filter_complex",
                    "[0:v]split=2[v1][v2];[v1]fade=t=in:st=0:d=2,fade=t=out:st=1790:d=8,setpts=PTS-STARTPTS[v1f];[v2]fade=t=in:st=0:d=2,fade=t=out:st=3590:d=6,setpts=PTS-STARTPTS[v2f];[v1f][v2f]concat=n=2:v=1:a=0[v]",
                    "-map","[v]","-map","1:a",
                    "-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",
                    "-c:a","aac","-b:a","96k",
                    "-shortest",
                    out
                ]

                subprocess.run(cmd, check=True)
                st.balloons()
                st.success("¡Listo Soli! Video de 59:56 generado")
                with open(out,"rb") as vf:
                    st.download_button("⬇️ DESCARGAR VIDEO FINAL 1 HORA", vf, file_name="moonlight_1hora_final.mp4", use_container_width=True, type="primary")
else:
    st.info("👆 Sube primero tu video de Canva de 29:58 y tu audio de 60 min")
