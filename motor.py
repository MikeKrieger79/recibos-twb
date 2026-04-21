import streamlit as st
import pandas as pd
from datetime import datetime, time
import urllib.parse
import pytz

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="THE WARRIOR BROTHERS",
    page_icon="logo.png",
    layout="wide"
)

# Configuración de zona horaria para Ecuador
zona_ec = pytz.timezone('America/Guayaquil')
ahora_ec = datetime.now(zona_ec)
hoy_ecuador = ahora_ec.date()
hora_default = time(16, 0)

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Contraseña:", type="password")
    if st.button("Entrar"):
        if password == "WARRIOR2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Incorrecta.")
    st.stop()

# --- 2. CABECERA ---
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>THE WARRIOR BROTHERS</h1>
        <p style='color: #888;'>Especialistas en Cuero y Calzado</p>
    </div>
    """, unsafe_allow_html=True
)

# --- 3. FORMULARIO ---
with st.form("form_warrior", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("👤 Cliente:")
        celular = st.text_input("📱 WhatsApp (09...):")
        articulo = st.text_input("💼 Artículo:")
    with col2:
        reparacion = st.text_input("🛠️ Reparación:")
        total = st.number_input("💰 Total ($):", min_value=0.0)
        abono = st.number_input("💵 Abono ($):", min_value=0.0)
        fecha_entrega = st.date_input("📅 Entrega:", value=hoy_ecuador)
        hora_entrega = st.time_input("🕒 Hora:", value=hora_default)
    
    submit = st.form_submit_button("💾 GENERAR RECIBO")

if submit:
    if nombre and celular:
        saldo = total - abono
        f_e = fecha_entrega.strftime("%d/%m/%Y")
        h_e = hora_entrega.strftime("%I:%M %p")

        # MENSAJE ACTUALIZADO CON PÁGINA WEB
        msg_wa = (
            f"👞🔨 *THE WARRIOR BROTHERS*\n"
            f"------------------------------------------\n"
            f"¡Hola *{nombre.upper()}*! ✅\n"
            f"Confirmamos la recepción de su *{articulo.lower()}*:\n\n"
            f"🛠️ *Trabajo:* {reparacion}\n"
            f"------------------------------------------\n"
            f"💰 *Total:* ${total:.2f}\n"
            f"💵 *Abono:* ${abono:.2f}\n"
            f"💳 *Saldo pendiente:* *${saldo:.2f}*\n"
            f"------------------------------------------\n"
            f"📅 *Entrega estimada:* {f_e}\n"
            f"🕒 *A partir de las:* {h_e}\n\n"
            
            f"🌐 *VISITA NUESTRA WEB PROFESIONAL:* ✨\n"
            f"Mira nuestros trabajos de Alta Gama aquí:\n"
            f"👉 https://warriorbrothersloja.mystrikingly.com/\n\n"
            
            f"⚠️ *NOTA IMPORTANTE:*\n"
            f"- Una vez ingresada la obra, no se realizarán devoluciones.\n"
            f"- Trabajos no retirados en 2 meses serán liquidados.\n\n"
            
            f"✨ *¡SÍGUENOS EN NUESTRAS REDES!* ✨\n"
            f"🔵 facebook.com/TheWarriorBrothersLoja\n"
            f"📸 instagram.com/thewarriorbrothers2023\n"
            f"🎬 tiktok.com/@the.warrior.broth\n\n"
            f"¡Gracias por su confianza! 🛡️⚒️"
        )

        texto_url = urllib.parse.quote(msg_wa)
        num_limpio = celular.lstrip('0')
        link_wa = f"https://api.whatsapp.com/send?phone=593{num_limpio}&text={texto_url}"

        st.markdown(f"""
            <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">
                    📲 ENVIAR RECIBO Y WEB
                </div>
            </a>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Falta nombre o celular.")

st.markdown("<br><center style='color: #888;'>© 2026 The Warrior Brothers | Loja, Ecuador 🛡️⚒️</center>", unsafe_allow_html=True)
