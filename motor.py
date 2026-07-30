import re
import urllib.parse
from datetime import datetime, time

import pandas as pd
import pytz
import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="THE WARRIOR BROTHERS", page_icon="logo.png", layout="wide"
)

# Configuración de zona horaria para Ecuador
zona_ec = pytz.timezone("America/Guayaquil")
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
            st.error("Contraseña incorrecta.")
    st.stop()

# --- 2. CABECERA ---
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>THE WARRIOR BROTHERS</h1>
        <p style='color: #888;'>Especialistas en Cuero y Calzado</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 3. FORMULARIO ---
with st.form("form_warrior"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("👤 Cliente:")
        celular = st.text_input("📱 WhatsApp (ej. 0991234567):")
        articulo = st.text_input("💼 Artículo:")
    with col2:
        reparacion = st.text_input("🛠️ Reparación:")
        total = st.number_input("💰 Total ($):", min_value=0.0, step=0.50)
        abono = st.number_input("💵 Abono ($):", min_value=0.0, step=0.50)
        fecha_entrega = st.date_input("📅 Entrega:", value=hoy_ecuador)
        hora_entrega = st.time_input("🕒 Hora:", value=hora_default)

    submit = st.form_submit_button("💾 GENERAR RECIBO")

# --- 4. PROCESAMIENTO Y GENERACIÓN DE RECIBO ---
if submit:
    if not nombre or not celular or not articulo:
        st.error("⚠️ Por favor completa los campos obligatorios: Cliente, WhatsApp y Artículo.")
    elif abono > total:
        st.warning("⚠️ El abono no puede ser mayor que el total.")
    else:
        # Limpieza estricta del número de teléfono (deja solo dígitos)
        num_digitos = re.sub(r"\D", "", celular)

        # Normalización para Ecuador (+593)
        if num_digitos.startswith("593"):
            num_final = num_digitos
        elif num_digitos.startswith("0"):
            num_final = f"593{num_digitos[1:]}"
        else:
            num_final = f"593{num_digitos}"

        saldo = total - abono
        f_e = fecha_entrega.strftime("%d/%m/%Y")
        h_e = hora_entrega.strftime("%I:%M %p")

        msg_wa = (
            f"👞🔨 *THE WARRIOR BROTHERS*\n"
            f"------------------------------------------\n"
            f"¡Hola *{nombre.strip().upper()}*! ✅\n"
            f"Confirmamos la recepción de su *{articulo.strip().lower()}*:\n\n"
            f"🛠️ *Trabajo:* {reparacion.strip()}\n"
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
        link_wa = f"https://api.whatsapp.com/send?phone={num_final}&text={texto_url}"

        # Guardar en estado de sesión para persistencia visual
        st.session_state["ultimo_link"] = link_wa
        st.session_state["ultimo_cliente"] = nombre.strip().upper()

if "ultimo_link" in st.session_state:
    st.success(f"Recibo listo para **{st.session_state['ultimo_cliente']}**")
    st.markdown(
        f"""
        <a href="{st.session_state['ultimo_link']}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">
                📲 ENVIAR RECIBO POR WHATSAPP
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    "<br><hr><center style='color: #888;'>© 2026 The Warrior Brothers | Loja, Ecuador 🛡️⚒️</center>",
    unsafe_allow_html=True,
)
