import streamlit as st
import pandas as pd

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

# Cargar datos con manejo de errores
try:
    st.write("🔄 Cargando datos...")
    
    kpis_df = pd.read_csv('data/kpis_diarios.csv')
    productos_df = pd.read_csv('data/analisis_productos.csv')
    clientes_df = pd.read_csv('data/analisis_clientes.csv')
    
    st.success("✅ Datos cargados correctamente")
    
    # Mostrar información básica
    st.write(f"📊 KPIs: {len(kpis_df)} registros")
    st.write(f"🛒 Productos: {len(productos_df)} registros")
    st.write(f"👥 Clientes: {len(clientes_df)} registros")
    
    # Calcular métricas reales
    ventas_totales = kpis_df['ventas_totales'].sum()
    pedidos_totales = kpis_df['pedidos_unicos'].sum()
    clientes_unicos = kpis_df['clientes_unicos'].sum()
    
    # Métricas dinámicas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Ventas Totales", f"${ventas_totales:,.0f}")

    with col2:
        st.metric("🛒 Pedidos Totales", f"{pedidos_totales:,.0f}")

    with col3:
        st.metric("👥 Clientes Únicos", f"{clientes_unicos:,.0f}")
    
    # Mostrar datos
    st.subheader("📋 Vista Previa de Datos KPIs")
    st.dataframe(kpis_df.head())
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {str(e)}")
    
    # Métricas de prueba como fallback
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