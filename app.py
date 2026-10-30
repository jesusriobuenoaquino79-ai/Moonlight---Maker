import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
import subprocess

st.set_page_config(page_title="Healing - CANVA 1 ARCHIVO", layout="centered")
st.title("🏔️ HEALING MAKER - MODO CANVA")
st.write("Ahora subes 1 solo video de Canva (29:58) que ya trae audio + video")

modo = st.radio("Elige el modo:", ["MODO 1 HORA - 1 Video -> 60min", "MODO 3 HORAS - 1 Video -> 180min"])

# --- MODO 1 HORA CON 1 SOLO VIDEO ---
if modo == "MODO 1 HORA - 1 Video -> 60min":
    st.header("MODO 1 HORA - CANVA")
    v1 = st.file_uploader("1️⃣ VIDEO CANVA 29:58", type=["mp4","mov","mkv"], key="v1_1h_canva")
    if v1:
        st.video(v1)
        if st.button("🚀 Crear 1 HORA desde 1 video", key="btn1h_canva"):
            with tempfile.TemporaryDirectory() as tmp:
                v1_p = os.path.join(tmp, "v1.mp4")
                out_p = os.path.join(tmp, "final_1h.mp4")
                with open(v1_p,"wb") as out: out.write(v1.getbuffer())
                
                st.info("Creando 1 hora... ahora es súper rápido (15 seg)")
                # Truco: loop 1 vez más, sin re-codificar
                # -stream_loop 1 = lo repite 2 veces total
                cmd = ["ffmpeg", "-y", "-stream_loop", "1", "-i", v1_p, "-c", "copy", "-t", "3596", out_p]
                subprocess.run(cmd, check=True)
                
                st.success("¡1 Hora lista! De 29:58 te hice 59:56")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 1 HORA", f, file_name="Healing_1HORA_CANVA.mp4", mime="video/mp4")

# --- MODO 3 HORAS CON 1 SOLO VIDEO ---
else:
    st.header("MODO 3 HORAS - CANVA")
    v_single = st.file_uploader("VIDEO CANVA 29:58 (se repetirá 6 veces)", type=["mp4","mov","mkv"], key="v_3h_canva")
    if v_single:
        st.video(v_single)
        if st.button("🚀 Crear 3 HORAS desde 1 video", key="btn3h_canva"):
            with tempfile.TemporaryDirectory() as tmp:
                v_p = os.path.join(tmp, "v.mp4")
                out_p = os.path.join(tmp, "final_3h.mp4")
                with open(v_p,"wb") as out: out.write(v_single.getbuffer())

                st.info("Uniendo 6 veces... ahora tarda 20 segundos, no 5 min")
                
                # MODO ULTRA RÁPIDO: ffmpeg lo repite 6 veces sin usar RAM
                # -stream_loop 5 = reproduce 1 + 5 = 6 veces
                # -t 10800 = corta exacto a 3 horas
                cmd = [
                    "ffmpeg", "-y",
                    "-stream_loop", "5",
                    "-i", v_p,
                    "-c", "copy",
                    "-t", "10800",
                    out_p
                ]
                subprocess.run(cmd, check=True)

                st.success("¡3 Horas listas! Sin recodificar, sin trabarse")
                with open(out_p,"rb") as f:
                    st.download_button("⬇️ Descargar 3 HORAS", f, file_name="Healing_3HORAS_CANVA.mp4", mime="video/mp4")

st.divider()
st.caption("MODO CANVA V2: Ya no recodifica. Usa -c copy, 10x más rápido y no se cae.")
