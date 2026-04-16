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

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .product-card {
        background-color: white; padding: 15px; border-radius: 15px;
        border: 1px solid #eee; text-align: center; margin-bottom: 20px;
        transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .social-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
    .social-btn { 
        padding: 12px; border-radius: 10px; text-decoration: none; 
        color: white !important; font-weight: bold; text-align: center;
        display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.85rem;
    }
    .ig { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .tk { background: #000000; border: 1px solid #fe2c55; }
    .fb { background: #1877F2; }
    .wa-main { background: #25D366; grid-column: span 2; }
    .info-box { background: #f9f9f9; padding: 20px; border-radius: 15px; border-left: 5px solid #121212; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA PÚBLICA ---
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/logo.png' style='height: 80px;'>
        <h1 style='margin: 0;'>THE WARRIOR BROTHERS</h1>
        <p style='color: #888; font-size: 1.2rem;'>Especialistas en Cuero y Calzado | Loja, Ecuador</p>
    </div>
    """, unsafe_allow_html=True
)

# --- SECCIÓN 1: CATÁLOGO DE SUELAS (PÚBLICO) ---
st.write("---")
st.markdown("<h2 style='text-align: center;'>👞 Catálogo de Suelas Disponibles</h2>", unsafe_allow_html=True)

# Aquí puedes ir añadiendo tus 60 suelas poco a poco
suelas = [
    {"nombre": "Suela Montaña Vibram", "precio": "18.00", "img": "https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/suela1.jpg"},
    {"nombre": "Suela Casual Crepe", "precio": "12.50", "img": "https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/suela2.jpg"},
    {"nombre": "Suela Track Trabajo", "precio": "15.00", "img": "https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/suela3.jpg"},
    {"nombre": "Suela de Vestir Goma", "precio": "10.00", "img": "https://raw.githubusercontent.com/youbanders590-ctrl/WarriorBrothersApp/main/suela4.jpg"},
]

cols_suelas = st.columns(4)
for i, item in enumerate(suelas):
    with cols_suelas[i % 4]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{item['img']}" style="width:100%; border-radius:10px; height:150px; object-fit:cover;">
                <h4 style="margin: 10px 0 5px 0;">{item['nombre']}</h4>
                <p style="color: #121212; font-weight: bold; font-size: 1.1rem;">${item['precio']}</p>
                <a href="https://wa.me/593994718745?text=Hola, deseo cotizar la suela: {item['nombre']}" target="_blank" style="text-decoration:none;">
                    <div style="background:#121212; color:white; padding:8px; border-radius:8px; font-size:0.8rem;">Consultar</div>
                </a>
            </div>
        """, unsafe_allow_html=True)

# --- SECCIÓN 2: REDES Y CONTACTO ---
st.write("---")
col_info, col_mapa = st.columns([1, 1.2])

with col_info:
    st.markdown(f"""
        <div class="info-box">
            <h3 style="margin-top:0;">📱 Nuestras Redes</h3>
            <div class="social-grid">
                <a href="https://www.instagram.com/thewarriorbrothers2023" class="social-btn ig" target="_blank">📸 Instagram</a>
                <a href="https://www.tiktok.com/@the.warrior.broth" class="social-btn tk" target="_blank">🎵 TikTok</a>
                <a href="https://www.facebook.com/TheWarriorBrothersLoja" class="social-btn fb" target="_blank">👤 Facebook</a>
                <a href="https://wa.me/593994718745" class="social-btn wa-main" target="_blank">💬 WhatsApp</a>
            </div>
        </div>
        <div class="info-box" style="margin-top: 15px; border-left-color: #FFD700;">
            <h3 style="margin-top:0;">📍 Ubicación</h3>
            <p>Lauro Guerrero y José A. Eguiguren, Loja</p>
            <p><b>Horario:</b> Lun-Vie (08:00-19:00) | Sáb (08:00-15:30)</p>
        </div>
    """, unsafe_allow_html=True)

with col_mapa:
    # Mapa estático de ejemplo (puedes reemplazar el link con un iframe de Google Maps)
    st.markdown("""
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3980.123456789!2d-79.2045!3d-3.9931!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zM8KwNTknMzUuMiJTIDc5wrAxMicyNy4wIlc!5e0!3m2!1ses!2sec!4v1234567890" width="100%" height="300" style="border:0; border-radius:15px;" allowfullscreen="" loading="lazy"></iframe>
    """, unsafe_allow_html=True)

# --- SECCIÓN 3: SISTEMA DE RECIBOS (PRIVADO) ---
st.write("---")
st.subheader("🔐 Panel de Administración")

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    password = st.text_input("Contraseña de taller:", type="password")
    if st.button("Acceder al Sistema"):
        if password == "WARRIOR2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Acceso denegado.")
else:
    # Formulario de recibos
    with st.form("form_warrior", clear_on_submit=True):
        st.info("Generador de Recibos Digitales")
        c1, c2 = st.columns(2)
        with c1:
            nombre = st.text_input("👤 Cliente:")
            celular = st.text_input("📱 WhatsApp:")
            articulo = st.text_input("💼 Artículo:")
        with c2:
            reparacion = st.text_input("🛠️ Reparación:")
            total = st.number_input("💰 Total ($):", min_value=0.0)
            abono = st.number_input("💵 Abono ($):", min_value=0.0)
            fecha_entrega = st.date_input("📅 Entrega:", value=hoy_ecuador)
            hora_entrega = st.time_input("🕒 Hora:", value=hora_default)
        
        submit = st.form_submit_button("💾 GENERAR Y NOTIFICAR")

    if submit and nombre and celular:
        saldo = total - abono
        f_e = fecha_entrega.strftime("%d/%m/%Y")
        h_e = hora_entrega.strftime("%I:%M %p")
        
        msg_wa = (
            f"👞🔨 *THE WARRIOR BROTHERS*\n"
            f"¡Hola *{nombre.upper()}*! ✅\n"
            f"Confirmamos la recepción de su *{articulo.lower()}*:\n\n"
            f"🛠️ *Trabajo:* {reparacion}\n"
            f"💰 *Total:* ${total:.2f} | *Abono:* ${abono:.2f}\n"
            f"💳 *Saldo pendiente:* *${saldo:.2f}*\n"
            f"📅 *Entrega:* {f_e} a las {h_e}\n\n"
            f"📍 Link de ubicación: https://www.facebook.com/TheWarriorBrothersLoja\n"
            f"¡Gracias por su confianza! ✨"
        )
        
        link_wa = f"https://api.whatsapp.com/send?phone=593{celular.lstrip('0')}&text={urllib.parse.quote(msg_wa)}"
        st.markdown(f'<a href="{link_wa}" target="_blank"><div style="background:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📲 ENVIAR POR WHATSAPP</div></a>', unsafe_allow_html=True)

st.markdown("<br><center style='color: #888;'>© 2026 The Warrior Brothers | Loja, Ecuador 🛡️⚒️</center>", unsafe_allow_html=True)
