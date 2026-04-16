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
# Hora predeterminada para la entrega (ej: 4:00 PM)
hora_default = time(16, 0)

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Acceso Privado - The Warrior Brothers")
    password = st.text_input("Ingresa la contraseña del taller:", type="password")
    if st.button("Entrar"):
        if password == "WARRIOR2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")
    st.stop()

# --- 2. APLICACIÓN PRINCIPAL ---
st.markdown(
    """
    <div style='display: flex; align-items: center; justify-content: center; gap: 15px;'>
        <img src='https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/logo.png' style='height: 50px;'>
        <h1 style='margin: 0;'>THE WARRIOR BROTHERS</h1>
    </div>
    <h3 style='text-align: center; color: #888; margin-top: 5px;'>Especialistas en Cuero y Calzado</h3>
    <br>
    """,
    unsafe_allow_html=True
)

# Formulario de entrada
with st.form("form_warrior", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("👤 Cliente:")
        celular = st.text_input("📱 WhatsApp (ej: 09...):")
        articulo = st.text_input("💼 Tipo de Artículo (Zapato, Maleta, Chompa):")
    with col2:
        reparacion = st.text_input("🛠️ Reparación a realizar:")
        total = st.number_input("💰 Total ($):", min_value=0.0)
        abono = st.number_input("💵 Abono ($):", min_value=0.0)
        # Sección de entrega con Fecha y Hora
        fecha_entrega = st.date_input("📅 Fecha de entrega:", value=hoy_ecuador, min_value=hoy_ecuador)
        hora_entrega = st.time_input("🕒 Hora de entrega:", value=hora_default)
    
    submit = st.form_submit_button("💾 GENERAR RECIBO")

if submit:
    if nombre and celular:
        # --- CÁLCULOS ---
        saldo = total - abono
        ahora = datetime.now(zona_ec)
        f_h = ahora.strftime("%d/%m/%Y %H:%M")
        f_e = fecha_entrega.strftime("%d/%m/%Y")
        h_e = hora_entrega.strftime("%I:%M %p") # Formato 12 horas (AM/PM)

        # --- GENERADOR DE MENSAJE WHATSAPP CON REDES SOCIALES ---
        e_zapato, e_martillo = "👞", "🔨"
        e_check = "✅"
        e_llave, e_bolsa, e_billete = "🛠️", "💰", "💵"
        e_tarjeta, e_calen, e_alerta, e_chispas = "💳", "📅", "⚠️", "✨"
        e_reloj = "🕒"
        e_camara, e_musica, e_user = "📸", "🎵", "👤"

        msg_wa = (
            f"{e_zapato}{e_martillo} *THE WARRIOR BROTHERS*\n"
            "------------------------------------------\n"
            f"¡Hola *{nombre.upper()}*! {e_check}\n"
            f"Confirmamos la recepción de su *{articulo.lower()}*:\n\n"
            f"{e_llave} *Trabajo:* {reparacion}\n"
            "------------------------------------------\n"
            f"{e_bolsa} *Total:* ${total:.2f}\n"
            f"{e_billete} *Abono:* ${abono:.2f}\n"
            f"{e_tarjeta} *Saldo pendiente:* *${saldo:.2f}*\n"
            "------------------------------------------\n"
            f"{e_calen} *Entrega estimada:* {f_e}\n"
            f"{e_reloj} *A partir de las:* {h_e}\n\n"
            f"{e_alerta} *NOTA IMPORTANTE:*\n"
            "- Una vez ingresada la obra, no se realizarán devoluciones.\n"
            "- Trabajos no retirados en 2 meses serán liquidados.\n\n"
            f"{e_chispas} *¡SÍGUENOS EN NUESTRAS REDES!* {e_chispas}\n"
            f"{e_user} *Facebook:* https://www.facebook.com/TheWarriorBrothersLoja\n"
            f"{e_camara} *Instagram:* https://www.instagram.com/thewarriorbrothers2023\n"
            f"{e_musica} *TikTok:* https://www.tiktok.com/@the.warrior.broth\n\n"
            f"¡Gracias por su confianza! 🛡️⚒️"
        )

        texto_url = urllib.parse.quote(msg_wa)
        num_limpio = celular.lstrip('0')
        # Código de país 593 para Ecuador
        link_wa = f"https://api.whatsapp.com/send?phone=593{num_limpio}&text={texto_url}"

        st.markdown(f"""
            <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px; margin-top:20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    📲 ENVIAR RECIBO Y REDES POR WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)

    else:
        st.error("⚠️ Por favor completa el nombre y el celular.")

st.markdown("<br><center style='color: #888;'>© 2026 The Warrior Brothers | Loja, Ecuador 🛡️⚒️</center>", unsafe_allow_html=True)
