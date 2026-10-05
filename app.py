import streamlit as st, tempfile, os, subprocess
from PIL import Image
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
st.set_page_config(page_title="1H ULTRA LIVIANO", layout="centered")
st.title("1H - No tumba el server")
musica=st.file_uploader("MP3",type=["mp3"])
c1,c2=st.columns(2)
with c1:
    f1=st.file_uploader("Foto1",type=["jpg","png","webp"],key="a1")
with c2:
    f2=st.file_uploader("Foto2",type=["jpg","png","webp"],key="a2")
if st.button("CREAR 1H - 60 SEG",use_container_width=True):
    with tempfile.TemporaryDirectory() as tmp:
        au=os.path.join(tmp,"a.mp3")
        open(au,"wb").write(musica.getvalue())
        def prep(u,o):
            Image.open(u).convert("RGB").resize((1280,720)).save(o,"JPEG",quality=75)
        i1=os.path.join(tmp,"1.jpg")
        i2=os.path.join(tmp,"2.jpg")
        prep(f1,i1)
        prep(f2,i2)
        v=os.path.join(tmp,"v.mp4")
        final=os.path.join(tmp,"final.mp4")
        st.write("Creando base 3 min...")
        # Crea solo 3 min primero, super rapido
        subprocess.run([FFMPEG,"-y","-loop","1","-i",i1,"-i",au,"-t","180","-vf","scale=1280:720","-c:v","libx264","-preset","ultrafast","-r","5","-c:a","aac","-shortest",v],check=True)
        st.write("Estirando a 1H con loop (esto no tumba el server)...")
        # Lo estira a 1 hora sin re-encode pesado
        subprocess.run([FFMPEG,"-y","-stream_loop","19","-i",v,"-c","copy","-t","3600",final],check=True)
        st.success("Listo! No se tumbó!")
        st.video(final)
        with open(final,"rb") as f:
            st.download_button("DESCARGAR 1H",f.read(),"1h.mp4")
