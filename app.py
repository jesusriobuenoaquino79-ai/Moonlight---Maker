import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile
import os

st.set_page_config(page_title="Healing - CANVA 1 ARCHIVO", layout="centered")
st.title("🏔️ HEALING MAKER - MODO CANVA")
st.write("Ahora subes 1 solo video de Canva (29:58) que ya trae audio + video")

modo = st.radio("Elige el modo:", ["MODO 1 HORA - 1 Video -> 60min", "MODO 3 HORAS - 1 Video -> 180min"])

# --- MODO 1 HORA CON 1 SOLO VIDEO ---
if modo == "MODO 1 HORA - 1 Video -> 60min":
    st.header("MODO 1 HORA - CANVA")
    st.caption("Sube 1 video de Canva de 29:58 (con audio incluido)")
    v1 = st.file_uploader("1️⃣ VIDEO CANVA 29:58", type=["mp4","mov","mkv"], key="v1_1h_canva")

    if v1:
        st.video(v1)
        if st.button("🚀 Crear 1 HORA desde 1 video", key="btn1h_canva"):
            with tempfile.TemporaryDirectory() as tmp:
                v1_p = os.path.join(tmp, "v1.mp4")
                out_p = os.path.join(tmp, "final_1h.mp4")
                with open(v1_p,"wb") as out: out.write(v1.getbuffer())
                
                st.info("Creando 1 hora desde tu video de Canva... con fade en el medio")
                
                clip_original = VideoFileClip(v1_p)
                
                # Creamos 2 clips del mismo video con fades para que no se note el corte
                clip1 = clip_original.fadeout(0.8)
                clip2 = clip_original.fadein(0.8)

                final_v = concatenate_videoclips([clip1, clip2], method="compose")
                # El audio ya viene dentro del video, no necesitamos AUDIO separado
                final_v.write_videofile(out_p, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast")
                
                clip_original.close()
                
                st.success("¡1 Hora lista! De 29:58 te hice 59:56")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 1 HORA", f, file_name="Healing_1HORA_CANVA.mp4", mime="video/mp4")

# --- MODO 3 HORAS CON 1 SOLO VIDEO ---
else:
    st.header("MODO 3 HORAS - CANVA")
    st.caption("Sube 1 video de Canva de 29:58 y te lo multiplico x6 = 3 horas")
    v_single = st.file_uploader("VIDEO CANVA 29:58 (se repetirá 6 veces)", type=["mp4","mov","mkv"], key="v_3h_canva")

    if v_single:
        st.video(v_single)
        if st.button("🚀 Crear 3 HORAS desde 1 video", key="btn3h_canva"):
            with tempfile.TemporaryDirectory() as tmp:
                v_p = os.path.join(tmp, "v.mp4")
                out_p = os.path.join(tmp, "final_3h.mp4")
                with open(v_p,"wb") as out: out.write(v_single.getbuffer())

                st.info("Uniendo 6 veces... esto tarda 4-5 min, no cierres la ventana")
                
                base_clip = VideoFileClip(v_p)
                clips = []
                for i in range(6):
                    c = base_clip
                    if i != 0: 
                        c = c.fadein(0.8)
                    if i != 5: 
                        c = c.fadeout(0.8)
                    clips.append(c)
                
                final_v = concatenate_videoclips(clips, method="compose")
                # Ajustamos a 3 horas exactas 10800 seg
                if final_v.duration > 10800:
                    final_v = final_v.subclip(0, 10800)
                    
                final_v.write_videofile(out_p, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast")
                base_clip.close()

                st.success("¡3 Horas listas!")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 3 HORAS", f, file_name="Healing_3HORAS_CANVA.mp4", mime="video/mp4")

st.divider()
st.caption("MODO CANVA ACTIVADO: Ya no necesitas subir audios separados. El audio sale del mismo video de Canva.")
