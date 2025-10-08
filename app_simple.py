import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Agregar utils al path
sys.path.append(str(Path(__file__).parent))

# Configuración básica de Streamlit
st.set_page_config(
    page_title="🥑 Sano y Fresco Dashboard",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Banner simple
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #06D6A0, #118AB2); border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🥑 SANO Y FRESCO</h1>
    <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Dashboard Ejecutivo de Análisis de Datos</p>
</div>
""", unsafe_allow_html=True)

# Sidebar simple
st.sidebar.markdown("### Panel de Control")
st.sidebar.markdown("#### 📅 Período de Análisis")

# Cargar datos básicos
try:
    # Cargar datos
    kpis_df = pd.read_csv('data/kpis_diarios.csv')
    productos_df = pd.read_csv('data/analisis_productos.csv')
    clientes_df = pd.read_csv('data/analisis_clientes.csv')
    
    st.success("✅ Datos cargados correctamente")
    
    # Mostrar información básica
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Registros KPIs", len(kpis_df))
    
    with col2:
        st.metric("🛒 Total Productos", len(productos_df))
    
    with col3:
        st.metric("👥 Total Clientes", len(clientes_df))
    
    # Mostrar primeras filas de datos
    st.subheader("📋 Vista Previa de Datos")
    
    tab1, tab2, tab3 = st.tabs(["KPIs", "Productos", "Clientes"])
    
    with tab1:
        st.dataframe(kpis_df.head())
    
    with tab2:
        st.dataframe(productos_df.head())
    
    with tab3:
        st.dataframe(clientes_df.head())
        
except Exception as e:
    st.error(f"❌ Error cargando datos: {str(e)}")
    st.stop()

# Footer simple
st.markdown("""
<div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
    <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
    <p style='color: #6c757d; font-size: 0.9rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
</div>
""", unsafe_allow_html=True)
