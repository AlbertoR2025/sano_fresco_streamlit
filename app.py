import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date

# Configuración de la página
st.set_page_config(
    page_title="🥑 Sano y Fresco Dashboard",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado MEJORADO
st.markdown("""
<style>
/* ===== BANNER CON GRADIENTE AVANZADO ===== */
.banner {
    background: linear-gradient(135deg, #2E86AB, #06D6A0);
    padding: 3rem 2rem;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.banner:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.banner h1 {
    color: white !important;
    margin: 0;
    font-size: 4rem;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    font-weight: 900;
    letter-spacing: 3px;
}

.banner p {
    color: white !important;
    margin: 0.5rem 0 0 0;
    font-size: 1.4rem;
    font-weight: 500;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.3);
}

/* ===== TARJETAS KPI CON BRILLO Y EFECTOS ===== */
.metric-card {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-left: 6px solid #06D6A0;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(6, 214, 160, 0.15), 
        transparent);
    transition: left 0.8s ease;
}

.metric-card:hover::before {
    left: 100%;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    border-left: 6px solid #118AB2;
}

/* Colores temáticos específicos para cada tarjeta */
.metric-card:nth-child(1) {
    border-left-color: #06D6A0;
}
.metric-card:nth-child(1):hover {
    border-left-color: #118AB2;
    box-shadow: 0 15px 35px rgba(6, 214, 160, 0.2);
}

.metric-card:nth-child(2) {
    border-left-color: #2563eb;
}
.metric-card:nth-child(2):hover {
    border-left-color: #1d4ed8;
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.2);
}

.metric-card:nth-child(3) {
    border-left-color: #d97706;
}
.metric-card:nth-child(3):hover {
    border-left-color: #b45309;
    box-shadow: 0 15px 35px rgba(217, 119, 6, 0.2);
}

.metric-card:nth-child(4) {
    border-left-color: #7c3aed;
}
.metric-card:nth-child(4):hover {
    border-left-color: #6d28d9;
    box-shadow: 0 15px 35px rgba(124, 58, 237, 0.2);
}

/* ===== TÍTULOS CON SOMBRA ===== */
.stMarkdown h2 {
    color: #0891b2 !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
    margin-bottom: 2.5rem !important;
    font-size: 2.2rem !important;
    border-bottom: 3px solid #06D6A0 !important;
    padding-bottom: 0.5rem !important;
}

/* ===== SIDEBAR MEJORADO ===== */
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

/* ===== BOTONES MEJORADOS ===== */
.stButton > button {
    background: linear-gradient(135deg, #2E86AB 0%, #06D6A0 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(46, 134, 171, 0.4);
}

/* ===== FONDO GENERAL ===== */
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}
</style>
""", unsafe_allow_html=True)

# Banner principal
st.markdown("""
<div class="banner">
    <h1>🥑 SANO Y FRESCO</h1>
    <p>Dashboard Ejecutivo | Inteligencia de Negocios 2025</p>
</div>
""", unsafe_allow_html=True)

# Sidebar mejorado
st.sidebar.markdown("### 🎛️ Panel de Control")
st.sidebar.markdown("---")
st.sidebar.markdown("#### 📅 Período de Análisis")

# Cargar datos con caché
@st.cache_data(ttl=3600)
def load_data():
    try:
        kpis_df = pd.read_csv('data/kpis_diarios.csv')
        productos_df = pd.read_csv('data/analisis_productos.csv')
        clientes_df = pd.read_csv('data/analisis_clientes.csv')
        
        # Convertir fechas
        kpis_df['fecha'] = pd.to_datetime(kpis_df['fecha'])
        
        return kpis_df, productos_df, clientes_df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None

# Cargar datos
with st.spinner('🔄 Cargando datos...'):
    kpis_df, productos_df, clientes_df = load_data()

if kpis_df is not None:
    # Filtros de fecha en sidebar
    fecha_min = kpis_df['fecha'].min().date()
    fecha_max = kpis_df['fecha'].max().date()
    
    fecha_inicio = st.sidebar.date_input(
        "Fecha inicio",
        value=fecha_min,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    fecha_fin = st.sidebar.date_input(
        "Fecha fin",
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # Filtrar datos
    kpis_filtrado = kpis_df[
        (kpis_df['fecha'].dt.date >= fecha_inicio) & 
        (kpis_df['fecha'].dt.date <= fecha_fin)
    ]
    
    # Calcular métricas
    ventas_totales = kpis_filtrado['ventas_totales'].sum()
    pedidos_totales = kpis_filtrado['pedidos_unicos'].sum()
    ticket_promedio = kpis_filtrado['ticket_promedio'].mean()
    clientes_unicos = kpis_filtrado['clientes_unicos'].sum()
    
    # Botón de descarga
    st.sidebar.markdown("---")
    csv = kpis_filtrado.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Descargar Reporte CSV",
        data=csv,
        file_name=f"reporte_sano_fresco_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        type="primary"
    )
    
    # KPIs principales con tarjetas avanzadas
    st.markdown("## 📊 Métricas / KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 2rem; margin-right: 12px;">💰</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: #6C757D; text-transform: uppercase; letter-spacing: 1px;">
                    Ventas Totales
                </span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; color: #059669; margin: 15px 0; text-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);">
                ${ventas_totales:,.0f}
            </div>
            <div style="font-size: 1rem; color: #059669; font-weight: 600;">
                ▲ {ventas_totales/1000000:.1f}M Total
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 2rem; margin-right: 12px;">🛒</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: #6C757D; text-transform: uppercase; letter-spacing: 1px;">
                    Pedidos
                </span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; color: #2563eb; margin: 15px 0; text-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);">
                {pedidos_totales:,.0f}
            </div>
            <div style="font-size: 1rem; color: #2563eb; font-weight: 600;">
                ▲ {pedidos_totales / max(1, len(kpis_filtrado)):.0f}/día
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 2rem; margin-right: 12px;">🎫</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: #6C757D; text-transform: uppercase; letter-spacing: 1px;">
                    Ticket Promedio
                </span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; color: #d97706; margin: 15px 0; text-shadow: 0 2px 4px rgba(217, 119, 6, 0.2);">
                ${ticket_promedio:.2f}
            </div>
            <div style="font-size: 1rem; color: #d97706; font-weight: 600;">
                ◆ Objetivo: $25.00
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 2rem; margin-right: 12px;">👥</span>
                <span style="font-size: 0.9rem; font-weight: 600; color: #6C757D; text-transform: uppercase; letter-spacing: 1px;">
                    Clientes Únicos
                </span>
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; color: #7c3aed; margin: 15px 0; text-shadow: 0 2px 4px rgba(124, 58, 237, 0.2);">
                {clientes_unicos:,.0f}
            </div>
            <div style="font-size: 1rem; color: #7c3aed; font-weight: 600;">
                ▲ {len(clientes_df):,} registrados
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de tendencias
    st.markdown("## 📈 Análisis de Tendencias")
    
    # Crear gráfico de líneas con Plotly
    fig = go.Figure()
    
    # Línea de ventas con área
    fig.add_trace(go.Scatter(
        x=kpis_filtrado['fecha'],
        y=kpis_filtrado['ventas_totales'],
        mode='lines',
        name='💰 Ventas Diarias',
        line=dict(color='#059669', width=4),
        fill='tozeroy',
        fillcolor='rgba(5, 150, 105, 0.1)',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Ventas: <b>$%{y:,.0f}</b><extra></extra>'
    ))
    
    # Media móvil
    kpis_filtrado['ma7'] = kpis_filtrado['ventas_totales'].rolling(window=7, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=kpis_filtrado['fecha'],
        y=kpis_filtrado['ma7'],
        mode='lines',
        name='📈 Tendencia (7 días)',
        line=dict(color='#dc2626', width=3, dash='dash'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Tendencia: <b>$%{y:,.0f}</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="📈 Evolución de Ventas con Tendencia",
            font=dict(size=20, color='#0891b2'),
            x=0.5
        ),
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=60, r=60, t=80, b=60),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        xaxis=dict(
            title="Fecha",
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Ventas ($)",
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top productos
    st.markdown("## 🏆 Análisis Profundo de Productos")
    
    if productos_df is not None:
        # Top productos por ventas
        top_productos = productos_df.nlargest(15, 'ventas_totales')
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=top_productos['ventas_totales'],
            y=top_productos['nombre_producto'],
            orientation='h',
            marker=dict(
                color='#0891b2',
                line=dict(color='#047857', width=2),
                cornerradius=8
            ),
            text=[f"${x:,.0f}" for x in top_productos['ventas_totales']],
            textposition='outside',
            textfont=dict(size=12, color='#0891b2'),
            hovertemplate='<b>%{y}</b><br>Ventas: <b>$%{x:,.0f}</b><extra></extra>'
        ))
        
        fig_bar.update_layout(
            title=dict(
                text="📊 Top 15 Productos por Ventas",
                font=dict(size=18, color='#0891b2'),
                x=0.5
            ),
            height=600,
            font=dict(size=12, family='Arial, sans-serif'),
            margin=dict(l=200, r=60, t=80, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="Ventas ($)",
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=11),
                categoryorder='total ascending'
            ),
            bargap=0.3
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer mejorado
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; margin-top: 3rem; border: 2px solid #dee2e6; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h3 style='color: #2E86AB; margin: 0; font-size: 1.8rem; text-shadow: 1px 1px 3px rgba(46, 134, 171, 0.2);'>🥑 Sano y Fresco Dashboard</h3>
        <p style='color: #6c757d; margin: 0.8rem 0; font-size: 1.1rem; font-weight: 500;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
        <p style='color: #6c757d; margin: 0; font-size: 0.95rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudieron cargar los datos. Verifica que los archivos CSV estén en la carpeta 'data/'")