import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import pytz
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN ---
st.set_page_config(
    page_title="THE WARRIOR BROTHERS",
    page_icon="logo.png",
    layout="wide"
)

# Conexión con Google Sheets (Usa la Service Account de tus Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# Configuración de zona horaria para Ecuador
zona_ec = pytz.timezone('America/Guayaquil')
hoy_ecuador = datetime.now(zona_ec).date()

# --- 1. SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Ingresa la contraseña:", type="password")
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
        fecha_entrega = st.date_input("📅 Fecha de entrega:", value=hoy_ecuador, min_value=hoy_ecuador)
    
    submit = st.form_submit_button("💾 GENERAR RECIBO")

if submit:
    if nombre and celular:
        # --- CÁLCULOS ---
        saldo = total - abono
        ahora = datetime.now(zona_ec)
        f_h = ahora.strftime("%d/%m/%Y %H:%M")
        f_e = fecha_entrega.strftime("%d/%m/%Y")

        # --- GUARDAR EN GOOGLE SHEETS ---
        try:
            # Leemos la pestaña "Data" (asegúrate de que así se llame en tu Excel)
            df_actual = conn.read(worksheet="Data")
            
            # Nueva fila con los nombres exactos de tus columnas
            nueva_fila = pd.DataFrame([{
                "Fecha": f_h,
                "Cliente": nombre.upper(),
                "Celular": celular,
                "Articulo": articulo,
                "Reparación": reparacion,
                "Total": total,
                "Abono": abono,
                "Saldo entrega": saldo
            }])
            
            # Unimos los datos y actualizamos la hoja
            df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
            conn.update(worksheet="Data", data=df_final)
            st.success(f"✅ ¡Datos guardados en Google Sheets para {nombre.upper()}!")
            
        except Exception as e:
            st.error(f"⚠️ Error al guardar en la nube: {e}")

        # --- GENERADOR DE WHATSAPP ---
        e_zapato, e_martillo = "👞", "🔨"
        e_check = "✅"
        e_llave, e_bolsa, e_billete = "🛠️", "💰", "💵"
        e_tarjeta, e_calen, e_alerta, e_chispas = "💳", "📅", "⚠️", "✨"

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
            f"{e_calen} *Entrega estimada:* {f_e}\n\n"
            f"{e_alerta} *NOTA IMPORTANTE:*\n"
            "- Una vez ingresada la obra, no se realizarán devoluciones.\n"
            "- Trabajos no retirados en 2 meses serán liquidados.\n\n"
            f"¡Gracias por su confianza! {e_chispas}"
        )

        texto_url = urllib.parse.quote(msg_wa)
        num_limpio = celular.lstrip('0')
        link_wa = f"https://api.whatsapp.com/send?phone=593{num_limpio}&text={texto_url}"

        st.markdown(f"""
            <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px; margin-top:20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    📲 ENVIAR RECIBO POR WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)

    else:
        st.error("⚠️ Por favor completa el nombre y el celular.")

st.markdown("<br><center style='color: #888;'>© 2026 The Warrior Brothers | Loja, Ecuador 🛡️⚒️</center>", unsafe_allow_html=True)
