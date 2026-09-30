import streamlit as st, tempfile, glob, os, subprocess
from PIL import Image

st.set_page_config(page_title="Moonlight Dreams", page_icon="🌙")
st.title("🌙 Moonlight Dreams - Video 1 Hora TURBO")

try:
    audio_fijo = sorted(glob.glob("*.mp3"), key=os.path.getmtime, reverse=True)[0]
    st.success(f"Música: {audio_fijo} ✅")
except:
    st.error("No hay MP3 en la carpeta")
    st.stop()

foto1 = st.file_uploader("Foto 1 (0-30 min)", type=["jpg","png","webp","jpeg"], key="f1")
foto2 = st.file_uploader("Foto 2 (30-60 min)", type=["jpg","png","webp","jpeg"], key="f2")

if foto1: st.image(foto1, width=200)
if foto2: st.image(foto2, width=200)

boton = st.button("🚀 CREAR VIDEO 1 HORA - TURBO", type="primary", disabled=not (foto1 and foto2))

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

if boton:
    barra = st.progress(0, text="Iniciando...")

    with tempfile.TemporaryDirectory() as tmpdir:
        img1_path = os.path.join(tmpdir, "img1.jpg")
        img2_path = os.path.join(tmpdir, "img2.jpg")
        audio_1h = os.path.join(tmpdir, "audio1h.mp3")
        v1 = os.path.join(tmpdir, "v1.mp4")
        v2 = os.path.join(tmpdir, "v2.mp4")
        out = os.path.join(tmpdir, "final.mp4")
        lista = os.path.join(tmpdir, "lista.txt")

        # Guardar y ajustar fotos
        for f, p in [(foto1, img1_path), (foto2, img2_path)]:
            im = Image.open(f).convert("RGB")
            w,h = im.size
            ratio = max(1280/w, 720/h)
            im = im.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            im = im.crop(((im.width-1280)//2, (im.height-720)//2, (im.width-1280)//2+1280, (im.height-720)//2+720))
            im.save(p, "JPEG", quality=90)

        barra.progress(20, text="Audio 1 hora...")
        # Audio en loop a 1 hora - esto es instantáneo con ffmpeg
        run(f'ffmpeg -y -stream_loop 20 -i "{audio_fijo}" -t 3600 -c:a aac -b:a 128k "{audio_1h}"')

        barra.progress(40, text="Video parte 1...")
        # Video 1 de 30 min a 10fps (super liviano)
        run(f'ffmpeg -y -loop 1 -framerate 10 -i "{img1_path}" -t 1800 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -r 10 "{v1}"')

        barra.progress(60, text="Video parte 2...")
        run(f'ffmpeg -y -loop 1 -framerate 10 -i "{img2_path}" -t 1800 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -r 10 "{v2}"')

        barra.progress(80, text="Uniendo...")
        with open(lista, "w") as f:
            f.write(f"file '{v1}'\nfile '{v2}'\n")

        # Une videos y pega audio de 1 hora
        run(f'ffmpeg -y -f concat -safe 0 -i "{lista}" -i "{audio_1h}" -c:v copy -c:a aac -shortest "{out}"')

        barra.progress(100, text="¡Listo!")
        st.success("¡VIDEO LISTO MI REY! 🔥")
        st.balloons()
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("📥 DESCARGAR VIDEO 1 HORA", f, file_name="moonlight-1hora.mp4", type="primary")
