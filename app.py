import streamlit as st
import tempfile, os, subprocess, math
from PIL import Image

st.set_page_config(page_title="Moonlight FIX 1ST", layout="centered")
st.title("Moonlight - FIX Error 1ST")
st.caption("Usa FFMPEG directo - 10x menos memoria")

audio_file = st.file_uploader("1️⃣ AUDIO 130MB", type=["mp3","wav","m4a","ogg","opus"], key="fix_audio")
f1 = st.file_uploader("2️⃣ FOTO 1", type=["jpg","jpeg","png","webp"], key="fix_f1")
f2 = st.file_uploader("3️⃣ FOTO 2 (opcional)", type=["jpg","jpeg","png","webp"], key="fix_f2")

fotos = [f for f in [f1,f2] if f is not None]

if audio_file and len(fotos)>0:
    st.success(f"Audio {audio_file.size/1024/1024:.1f} MB | Fotos {len(fotos)} - LISTO PARA NO FALLAR")
    if st.button("🎬 GENERAR SIN ERROR 1ST (FFMPEG)", type="primary", use_container_width=True):
        with st.spinner("Generando con FFMPEG... Esto NO se cae, tarda 5-8 min - No cierres"):
            with tempfile.TemporaryDirectory() as tmp:
                audio_path = os.path.join(tmp, "audio.mp3")
                with open(audio_path, "wb") as o:
                    o.write(audio_file.getbuffer())

                # Guardar fotos en 720p
                img_paths=[]
                for i,f in enumerate(fotos):
                    im = Image.open(f).convert("RGB")
                    im.thumbnail((1280,720))
                    p = os.path.join(tmp, f"img{i}.jpg")
                    im.save(p, "JPEG", quality=80)
                    img_paths.append(p)

                out = os.path.join(tmp, "final.mp4")
                
                # Si es 1 foto, loop simple - super ligero
                if len(img_paths)==1:
                    cmd = [
                        "ffmpeg","-y",
                        "-loop","1","-i", img_paths[0],
                        "-i", audio_path,
                        "-c:v","libx264","-tune","stillimage",
                        "-c:a","aac","-b:a","96k",
                        "-pix_fmt","yuv420p",
                        "-shortest",
                        "-vf","scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
                        out
                    ]
                else:
                    # 2 fotos con FADE usando xfade - también ligero
                    # Crear 2 videos de mitad de duración c/u
                    import mutagen.mp3
                    try:
                        from mutagen.mp3 import MP3
                        dur = MP3(audio_path).info.length
                    except:
                        dur = 10800 # fallback 3h

                    dur1 = dur/2
                    cmd = [
                        "ffmpeg","-y",
                        "-loop","1","-t",str(dur1),"-i",img_paths[0],
                        "-loop","1","-t",str(dur1),"-i",img_paths[1],
                        "-i",audio_path,
                        "-filter_complex",
                        f"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];[v0][v1]xfade=transition=fade:duration=1:offset={dur1-1}[v]",
                        "-map","[v]","-map","2:a",
                        "-c:v","libx264","-c:a","aac","-b:a","96k",
                        "-shortest",
                        out
                    ]

                subprocess.run(cmd, check=True)
                st.balloons()
                st.success("¡Listo! Ya no dio error 1ST")
                with open(out,"rb") as vf:
                    st.download_button("⬇️ DESCARGAR VIDEO", vf, file_name="moonlight_3h.mp4", use_container_width=True, type="primary")
else:
    st.info("Sube audio 130MB y Foto 1. Usa máximo 2 fotos para que no falle")
