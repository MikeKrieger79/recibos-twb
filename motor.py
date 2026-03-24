import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import pytz

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Warrior Brothers", page_icon="🛡️")
zona_ec = pytz.timezone('America/Guayaquil')

# --- DISEÑO ---
st.title("🛡️ Los Hermanos Guerreros")
st.write("Registro rápido de trabajos")

with st.form("form_warrior", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("👤 Cliente:")
        celular = st.text_input("📱 WhatsApp (ej: 0987654321):")
        articulo = st.text_input("💼 Artículo:")
    with col2:
        reparacion = st.text_input("🛠️ Reparación:")
        total = st.number_input("💰 Total ($):", min_value=0.0)
        abono = st.number_input("💵 Abono ($):", min_value=0.0)
        dias = st.number_input("📅 Días entrega:", min_value=1, value=3)
    
    submit = st.form_submit_button("💾 GENERAR RECIBO")

if submit:
    if nombre and celular:
        saldo = total - abono
        ahora = datetime.now(zona_ec)
        f_e = (ahora + timedelta(days=dias)).strftime("%d/%m/%Y")

        # Emojis en código puro para evitar rombos en PC
        e_escudo, e_check, e_maleta = "\U0001F6E1", "\u2705", "\U0001F4BC"
        e_llave, e_bolsa, e_billete = "\U0001F6E0", "\U0001F4B0", "\U0001F4B5"
        e_tarjeta, e_calen, e_alerta, e_chispas = "\U0001F4B3", "\U0001F4D3", "\u26A0", "\u2728"

        msg_wa = (
            f"{e_escudo} *THE WARRIOR BROTHERS*\n"
            "------------------------------------------\n"
            f"¡Hola *{nombre.upper()}*! {e_check}\n"
            "Confirmamos la recepción de su artículo:\n\n"
            f"{e_maleta} *Artículo:* {articulo}\n"
            f"{e_llave} *Trabajo:* {reparacion}\n"
            "------------------------------------------\n"
            f"{e_bolsa} *Total:* ${total:.2f}\n"
            f"{e_billete} *Abono:* ${abono:.2f}\n"
            f"{e_tarjeta} *Saldo pendiente:* *${saldo:.2f}*\n"
            "------------------------------------------\n"
            f"{e_calen} *Entrega estimada:* {f_e}\n\n"
            f"{e_alerta} *NOTA IMPORTANTE:*\n"
            "- No se realizarán devoluciones de abonos.\n"
            "- Trabajos no retirados en 2 meses serán liquidados.\n\n"
            f"¡Gracias por su confianza! {e_chispas}"
        )

        texto_url = urllib.parse.quote(msg_wa)
        link_wa = f"https://api.whatsapp.com/send?phone=593{celular.lstrip('0')}&text={texto_url}"

        st.success("✅ Recibo listo para enviar")
        st.markdown(f'''
            <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">
                    📲 ENVIAR POR WHATSAPP
                </div>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.error("Faltan datos del cliente.")
