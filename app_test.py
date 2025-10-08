import streamlit as st
import pandas as pd

# Configuración básica
st.set_page_config(
    page_title="Sano y Fresco - Test",
    page_icon="🥑",
    layout="wide"
)

st.title("🥑 SANO Y FRESCO - Dashboard Test")

# Cargar datos
try:
    kpis = pd.read_csv('data/kpis_diarios.csv')
    st.success(f"✅ Datos cargados: {len(kpis)} registros")
    
    # Mostrar primeras filas
    st.subheader("📊 Primeras filas de datos")
    st.dataframe(kpis.head())
    
    # Métricas básicas
    st.subheader("📈 Métricas Básicas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Ventas Totales", f"${kpis['ventas_totales'].sum():,.0f}")
    
    with col2:
        st.metric("Pedidos Totales", f"{kpis['pedidos_unicos'].sum():,}")
    
    with col3:
        st.metric("Ticket Promedio", f"${kpis['ticket_promedio'].mean():.2f}")
    
    # Gráfico simple
    st.subheader("📈 Gráfico de Ventas")
    st.line_chart(kpis.set_index('fecha')['ventas_totales'])
    
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("Verifica que los archivos de datos estén en la carpeta 'data/'")
