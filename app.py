import streamlit as st, tempfile, os, subprocess, json
from PIL import Image
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FFPROBE = imageio_ffmpeg.get_ffprobe_exe()

st.title("ADAPTATIVO - 1, 2, 3 Fotos")
st.cache_data.clear()

mp3 = st.file_uploader("MP3 Ya Hecho - 1H, 3H, lo que sea", type=["mp3","wav","m4a","ogg"])
fotos = st.file_uploader("Sube 1, 2 o 3 Fotos", type=["jpg","png","webp"], accept_multiple_files=True)

if fotos and mp3 and st.button(f"CREAR VIDEO CON {len(fotos)} FOTO(S)", use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3"); open(au,"wb").write(mp3.getvalue())
        
        # 1. Duración del audio
        probe = subprocess.run([FFPROBE, "-v", "quiet", "-print_format", "json", "-show_format", au], capture_output=True, text=True)
        duracion = float(json.loads(probe.stdout)["format"]["duration"])
        por_foto = duracion / len(fotos)
        loops = int(por_foto / 5) - 1
        
        st.write(f"🎵 Audio: {duracion/60:.1f} min total | {len(fotos)} foto(s) = {por_foto/60:.1f} min cada una")

        clips = []
        for idx, f in enumerate(fotos):
            st.write(f"⏳ {idx+1}/{len(fotos)}: Procesando foto {idx+1}...")
            img_path = os.path.join(tmp, f"{idx}.jpg")
            Image.open(f).convert("RGB").resize((1280,720)).save(img_path,"JPEG",quality=80)
            
            v5 = os.path.join(tmp, f"v{idx}_5.mp4")
            v_full = os.path.join(tmp, f"v{idx}.mp4")
            subprocess.run([FFMPEG,"-y","-loop","1","-i",img_path,"-t","5","-vf","format=yuv420p","-r","24","-c:v","libx264","-preset","ultrafast",v5], check=True)
            subprocess.run([FFMPEG,"-y","-stream_loop",str(loops),"-i",v5,"-c","copy",v_full], check=True)
            clips.append(v_full)

        silent="/tmp/silent.mp4"; final="/tmp/final.mp4"
        lst=os.path.join(tmp,"list.txt"); open(lst,"w").write("\n".join([f"file '{c}'" for c in clips]))
        subprocess.run([FFMPEG,"-y","-f","concat","-safe","0","-i",lst,"-c","copy",silent], check=True)
        subprocess.run([FFMPEG,"-y","-i",au,"-i",silent,"-t",str(duracion),"-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","128k","-movflags","+faststart",final], check=True)

        st.success(f"✅ LISTO {duracion/3600:.2f}H CON {len(fotos)} FOTO(S)")
        st.video(final)
        st.download_button(f"📥 DESCARGAR {duracion/3600:.1f}H", open(final,"rb").read(), f"video_{len(fotos)}fotos_{duracion/60:.0f}min.mp4", use_container_width=True)
