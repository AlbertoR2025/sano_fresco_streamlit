import streamlit as st
import pandas as pd

# Configuración básica
st.set_page_config(
    page_title="🥑 Sano y Fresco Dashboard",
    page_icon="🥑",
    layout="wide"
)

# Banner mejorado
st.markdown("""
<div style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #2E86AB, #06D6A0); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(46, 134, 171, 0.3);'>
    <h1 style='color: white; margin: 0; font-size: 3.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🥑 SANO Y FRESCO</h1>
    <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: 500;'>Dashboard Ejecutivo de Análisis de Datos</p>
</div>
""", unsafe_allow_html=True)

# Sidebar mejorado
st.sidebar.markdown("### 🎛️ Panel de Control")
st.sidebar.markdown("---")

# Contenido principal
st.markdown("## 📊 Análisis de Datos en Tiempo Real")

# Cargar datos con manejo de errores mejorado
try:
    with st.spinner('🔄 Cargando datos desde archivos CSV...'):
        kpis_df = pd.read_csv('data/kpis_diarios.csv')
        productos_df = pd.read_csv('data/analisis_productos.csv')
        clientes_df = pd.read_csv('data/analisis_clientes.csv')
    
    st.success("✅ ¡Datos cargados exitosamente!")
    
    # Información de los datasets
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"📊 **KPIs Diarios:** {len(kpis_df):,} registros")
    
    with col2:
        st.info(f"🛒 **Productos:** {len(productos_df):,} productos")
    
    with col3:
        st.info(f"👥 **Clientes:** {len(clientes_df):,} clientes")
    
    # Calcular métricas principales
    ventas_totales = kpis_df['ventas_totales'].sum()
    pedidos_totales = kpis_df['pedidos_unicos'].sum()
    clientes_unicos = kpis_df['clientes_unicos'].sum()
    ticket_promedio = kpis_df['ticket_promedio'].mean()
    
    # Métricas principales con mejor formato
    st.markdown("## 💰 Métricas Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Ventas Totales",
            value=f"${ventas_totales:,.0f}",
            delta=f"{ventas_totales/1000000:.1f}M"
        )
    
    with col2:
        st.metric(
            label="🛒 Pedidos Totales",
            value=f"{pedidos_totales:,.0f}",
            delta=f"{pedidos_totales/1000:.0f}K"
        )
    
    with col3:
        st.metric(
            label="👥 Clientes Únicos",
            value=f"{clientes_unicos:,.0f}",
            delta=f"{clientes_unicos/1000:.0f}K"
        )
    
    with col4:
        st.metric(
            label="🎫 Ticket Promedio",
            value=f"${ticket_promedio:.2f}",
            delta="$25.00 objetivo"
        )
    
    # Vista de datos mejorada
    st.markdown("## 📋 Vista de Datos KPIs")
    
    # Agregar filtros básicos
    fecha_min = pd.to_datetime(kpis_df['fecha']).min().date()
    fecha_max = pd.to_datetime(kpis_df['fecha']).max().date()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_inicio = st.date_input("📅 Fecha Inicio", value=fecha_min, min_value=fecha_min, max_value=fecha_max)
    
    with col2:
        fecha_fin = st.date_input("📅 Fecha Fin", value=fecha_max, min_value=fecha_min, max_value=fecha_max)
    
    # Filtrar datos
    kpis_df['fecha'] = pd.to_datetime(kpis_df['fecha'])
    kpis_filtrado = kpis_df[
        (kpis_df['fecha'].dt.date >= fecha_inicio) & 
        (kpis_df['fecha'].dt.date <= fecha_fin)
    ]
    
    st.dataframe(kpis_filtrado.head(10), use_container_width=True)
    
    # Estadísticas del período filtrado
    st.markdown("## 📈 Estadísticas del Período")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Registros", f"{len(kpis_filtrado):,}")
    
    with col2:
        ventas_periodo = kpis_filtrado['ventas_totales'].sum()
        st.metric("💰 Ventas Período", f"${ventas_periodo:,.0f}")
    
    with col3:
        ventas_promedio = kpis_filtrado['ventas_totales'].mean()
        st.metric("📈 Promedio Diario", f"${ventas_promedio:,.0f}")
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {str(e)}")
    st.warning("⚠️ Mostrando datos de prueba...")
    
    # Métricas de prueba como fallback
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Ventas", "$1,000,000", "5.2%")
    
    with col2:
        st.metric("🛒 Pedidos", "5,000", "12%")
    
    with col3:
        st.metric("👥 Clientes", "1,200", "8%")
    
    with col4:
        st.metric("🎫 Ticket", "$25.00", "Objetivo")

# Footer mejorado
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 3rem; border: 1px solid #dee2e6;'>
    <h3 style='color: #2E86AB; margin: 0; font-size: 1.5rem;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d; margin: 0.5rem 0; font-size: 1rem;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
    <p style='color: #6c757d; margin: 0; font-size: 0.9rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
</div>
""", unsafe_allow_html=True)