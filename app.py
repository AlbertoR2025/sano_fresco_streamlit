import streamlit as st

# Configuración básica
st.set_page_config(
    page_title="🥑 Sano y Fresco Dashboard",
    page_icon="🥑",
    layout="wide"
)

# Banner
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #2E86AB, #06D6A0); border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0; font-size: 3rem;'>🥑 SANO Y FRESCO</h1>
    <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Dashboard Ejecutivo</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Panel de Control")

# Contenido principal
st.write("🎉 ¡Dashboard funcionando correctamente!")
st.write("📊 Esta es una versión de prueba para verificar que Streamlit Cloud funciona.")

# Métricas de prueba
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Ventas", "$1,000,000")

with col2:
    st.metric("🛒 Pedidos", "5,000")

with col3:
    st.metric("👥 Clientes", "1,200")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
    <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d;'>Desarrollado con Python y Streamlit</p>
</div>
""", unsafe_allow_html=True)