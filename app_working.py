import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import plotly.graph_objects as go

# Agregar utils al path
sys.path.append(str(Path(__file__).parent))

# Configuración de la página
st.set_page_config(
    page_title="🥑 Sano y Fresco Dashboard",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado SIMPLIFICADO
st.markdown("""
<style>
/* ===== BANNER SIMPLE ===== */
.banner {
    background: linear-gradient(135deg, #2E86AB, #06D6A0);
    padding: 3rem 2rem;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(46, 134, 171, 0.3);
}

.banner h1 {
    color: white !important;
    margin: 0;
    font-size: 3rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.banner p {
    color: white !important;
    margin: 0.5rem 0 0 0;
    font-size: 1.2rem;
}

/* ===== TARJETAS KPI SIMPLES ===== */
.metric-card {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.07);
    border-left: 5px solid #06D6A0;
    transition: all 0.3s ease;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12);
}

/* ===== TÍTULOS ===== */
.stMarkdown h2 {
    color: #0891b2 !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
    margin-bottom: 2.5rem !important;
}

/* ===== SIDEBAR ===== */
.stSidebar h3 {
    color: #0891b2 !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
    font-size: 1.5rem !important;
}

.stSidebar h4 {
    color: #0891b2 !important;
    font-weight: 600 !important;
    text-shadow: 1px 1px 2px rgba(8, 145, 178, 0.2) !important;
    font-size: 1.1rem !important;
    line-height: 1.2 !important;
}
</style>
""", unsafe_allow_html=True)

# Banner
st.markdown("""
<div class="banner">
    <h1>🥑 SANO Y FRESCO</h1>
    <p>Dashboard Ejecutivo de Análisis de Datos</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### Panel de Control")
st.sidebar.markdown("#### 📅 Período de Análisis")

# Filtros de fecha
fecha_inicio = st.sidebar.date_input("Fecha Inicio", value=pd.to_datetime('2024-01-01').date())
fecha_fin = st.sidebar.date_input("Fecha Fin", value=pd.to_datetime('2024-12-31').date())

# Botón de descarga
st.sidebar.markdown("---")
if st.sidebar.button("📥 Descargar Reporte", type="primary"):
    st.sidebar.success("✅ Reporte descargado")

# Cargar datos
@st.cache_data
def cargar_datos():
    try:
        kpis_df = pd.read_csv('data/kpis_diarios.csv')
        productos_df = pd.read_csv('data/analisis_productos.csv')
        clientes_df = pd.read_csv('data/analisis_clientes.csv')
        return kpis_df, productos_df, clientes_df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None

kpis_df, productos_df, clientes_df = cargar_datos()

if kpis_df is not None:
    # Filtrar datos por fecha
    kpis_df['fecha'] = pd.to_datetime(kpis_df['fecha'])
    kpis_filtrado = kpis_df[
        (kpis_df['fecha'].dt.date >= fecha_inicio) & 
        (kpis_df['fecha'].dt.date <= fecha_fin)
    ]
    
    # Calcular métricas básicas
    ventas_totales = kpis_filtrado['ventas_totales'].sum()
    pedidos_totales = kpis_filtrado['pedidos_unicos'].sum()
    ticket_promedio = kpis_filtrado['ticket_promedio'].mean()
    clientes_unicos = kpis_filtrado['clientes_unicos'].sum()
    
    # KPIs
    st.markdown("## 📊 Métricas / KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">💰</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Ventas Totales
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #059669; margin: 10px 0;">
                ${ventas_totales:,.0f}
            </div>
            <div style="font-size: 0.9rem; color: #059669; font-weight: 600;">
                ▲ {ventas_totales/1000000:.1f}M
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">🛒</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Pedidos
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #2563eb; margin: 10px 0;">
                {pedidos_totales:,.0f}
            </div>
            <div style="font-size: 0.9rem; color: #2563eb; font-weight: 600;">
                ▲ {pedidos_totales / max(1, len(kpis_filtrado)):.0f}/día
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">🎫</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Ticket Promedio
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #d97706; margin: 10px 0;">
                ${ticket_promedio:.2f}
            </div>
            <div style="font-size: 0.9rem; color: #d97706; font-weight: 600;">
                ◆ Objetivo: $25.00
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">👥</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Clientes Únicos
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #7c3aed; margin: 10px 0;">
                {clientes_unicos:,.0f}
            </div>
            <div style="font-size: 0.9rem; color: #7c3aed; font-weight: 600;">
                ▲ {len(clientes_df):,} registrados
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico simple de tendencias
    st.markdown("## 📈 Análisis de Tendencias")
    
    # Crear gráfico simple
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=kpis_filtrado['fecha'],
        y=kpis_filtrado['ventas_totales'],
        mode='lines',
        name='Ventas Diarias',
        line=dict(color='#059669', width=3)
    ))
    
    fig.update_layout(
        title="Evolución de Ventas",
        xaxis_title="Fecha",
        yaxis_title="Ventas ($)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top productos
    st.markdown("## 🏆 Top Productos")
    
    if productos_df is not None:
        top_productos = productos_df.nlargest(10, 'ventas_totales')
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=top_productos['ventas_totales'],
            y=top_productos['nombre_producto'],
            orientation='h',
            marker_color='#0891b2',
            text=[f"${x:,.0f}" for x in top_productos['ventas_totales']],
            textposition='outside'
        ))
        
        fig_bar.update_layout(
            title="Top 10 Productos por Ventas",
            xaxis_title="Ventas ($)",
            yaxis_title="Producto",
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
        <p style='color: #6c757d;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
        <p style='color: #6c757d; font-size: 0.9rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudieron cargar los datos. Verifica que los archivos CSV estén en la carpeta 'data/'")
