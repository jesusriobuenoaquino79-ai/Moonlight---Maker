import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
import tempfile
import os

st.set_page_config(page_title="Healing - TODAS LAS OPCIONES", layout="centered")
st.title("🏔️ HEALING MAKER - TODO EN UNO")
st.write("Una sola app para 1 hora y 3 horas")

modo = st.radio("Elige el modo:", ["MODO 1 HORA - 2 Videos (60min)", "MODO 3 HORAS - 6 Videos (180min)"])

# --- MODO 1 HORA ---
if modo == "MODO 1 HORA - 2 Videos (60min)":
    st.header("MODO 1 HORA")
    st.caption("Sube 2 videos iguales de 29:58 + 2 audios iguales de 29:58")
    v1 = st.file_uploader("1️⃣ VIDEO 1 - 30min", type=["mp4","mov","mkv"], key="v1_1h")
    v2 = st.file_uploader("2️⃣ VIDEO 2 - 30min", type=["mp4","mov","mkv"], key="v2_1h")
    a1 = st.file_uploader("3️⃣ AUDIO 1 - 30min", type=["mp3","wav","m4a","ogg","opus"], key="a1_1h")
    a2 = st.file_uploader("4️⃣ AUDIO 2 - 30min", type=["mp3","wav","m4a","ogg","opus"], key="a2_1h")

    if v1 and v2 and a1 and a2:
        if st.button("🚀 Crear 1 HORA", key="btn1h"):
            with tempfile.TemporaryDirectory() as tmp:
                paths = {}
                for name, file in [("v1","v1"),("v2","v2"),("a1","a1"),("a2","a2")]:
                    pass
                v1_p = os.path.join(tmp, "v1.mp4")
                v2_p = os.path.join(tmp, "v2.mp4")
                a1_p = os.path.join(tmp, "a1.mp3")
                a2_p = os.path.join(tmp, "a2.mp3")
                out_p = os.path.join(tmp, "final_1h.mp4")
                for p, f in [(v1_p,v1),(v2_p,v2),(a1_p,a1),(a2_p,a2)]:
                    with open(p,"wb") as out: out.write(f.getbuffer())
                
                st.info("Uniendo Video 1 + Video 2 con fade...")
                clip1 = VideoFileClip(v1_p).fadeout(0.8)
                clip2 = VideoFileClip(v2_p).fadein(0.8)
                audio1 = AudioFileClip(a1_p).audio_fadeout(0.8)
                audio2 = AudioFileClip(a2_p).audio_fadein(0.8)
                
                final_v = concatenate_videoclips([clip1, clip2], method="compose")
                final_a = concatenate_audioclips([audio1, audio2])
                final_v = final_v.set_audio(final_a)
                final_v.write_videofile(out_p, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast")
                
                st.success("¡1 Hora lista!")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 1 HORA", f, file_name="Healing_1HORA.mp4")

# --- MODO 3 HORAS ---
else:
    st.header("MODO 3 HORAS")
    st.caption("Sube 6 videos iguales de 29:58 + tu audio de 3 horas YA en loop")
    st.info("Para que no se trabe, sube 6 veces el mismo video de Canva")
    videos = []
    for i in range(6):
        videos.append(st.file_uploader(f"VIDEO {i+1} - 30min", type=["mp4","mov","mkv"], key=f"v_{i}"))
    
    audio_3h = st.file_uploader("AUDIO 3 HORAS (tus 3 pistas ya en loop x6)", type=["mp3","wav","m4a","ogg","opus"], key="a3h")

    if all(videos) and audio_3h:
        if st.button("🚀 Crear 3 HORAS", key="btn3h"):
            with tempfile.TemporaryDirectory() as tmp:
                v_paths = []
                for i, vf in enumerate(videos):
                    p = os.path.join(tmp, f"v{i}.mp4")
                    with open(p,"wb") as out: out.write(vf.getbuffer())
                    v_paths.append(p)
                a_p = os.path.join(tmp, "a3h.mp3")
                with open(a_p,"wb") as out: out.write(audio_3h.getbuffer())
                out_p = os.path.join(tmp, "final_3h.mp4")

                st.info("Uniendo 6 videos... esto tarda 3-4 min, no cierres la ventana")
                
                clips = []
                for idx, vp in enumerate(v_paths):
                    c = VideoFileClip(vp)
                    if idx != 0: c = c.fadein(0.8)
                    if idx != 5: c = c.fadeout(0.8)
                    clips.append(c)
                
                final_v = concatenate_videoclips(clips, method="compose")
                final_a = AudioFileClip(a_p)
                final_v = final_v.set_audio(final_a)
                # Corta a 3 horas exactas (10800 seg) por si se pasa 2 seg
                final_v = final_v.subclip(0, 10800)
                final_v.write_videofile(out_p, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast")

                st.success("¡3 Horas listas!")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 3 HORAS", f, file_name="Healing_3HORAS.mp4")

st.divider()
st.caption("Tip: Si tu audio de 3h es muy pesado, comprímelo a 128kbps mp3 antes de subirlo")
