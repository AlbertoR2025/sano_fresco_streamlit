import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import io
import base64
import plotly.graph_objects as go

# Agregar utils al path
sys.path.append(str(Path(__file__).parent))

# Importaciones corregidas - SIN crear_analisis_estacionalidad
from utils.visualizations import (
    crear_grafico_tendencia_ventas,
    crear_grafico_distribucion_clientes,
    crear_grafico_top_productos,
    crear_heatmap_ventas_mensual,
    crear_gauge_chart,
    crear_mapa_correlaciones,
    crear_waterfall_contribucion,
    crear_sankey_segmentos,
    crear_treemap_productos,
    crear_grafico_pareto,
    crear_grafico_progreso_objetivos
)

from utils.metrics import (
    calcular_metricas_globales,
    calcular_crecimiento,
    identificar_productos_estrella,
    segmentar_clientes_valor
)

# Configuración de la página
st.set_page_config(
    page_title="Sano y Fresco - Dashboard Ejecutivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado MEJORADO con imagen de fondo en banner
st.markdown("""
    <style>
    /* ===== BANNER CON IMAGEN DE FONDO ===== */
    .banner {
        background: linear-gradient(rgba(46, 134, 171, 0.85), rgba(6, 214, 160, 0.85)), 
                    url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        padding: 1.5rem 2rem;
        text-align: center;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 6px 20px rgba(0, 0, 0, 0.2),
            0 1px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }

    /* Efecto hover en el banner */
    .banner:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 5px 15px rgba(0, 0, 0, 0.3);
    }

    /* Overlay animado */
    .banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
        animation: rotate 25s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Título principal */
    .main-header {
        font-size: 3rem;
        font-weight: 900;
        color: #FFFFFF !important;
        text-shadow: 
            0 3px 12px rgba(0,0,0,0.6),
            0 6px 20px rgba(0,0,0,0.4),
            0 9px 30px rgba(0,0,0,0.3),
            0 2px 4px rgba(0,0,0,0.8);
        margin: 0;
        position: relative;
        letter-spacing: 2px;
        animation: fadeInDown 1s ease-out;
    }

    /* Forzar color blanco para SANO Y FRESCO */
    .banner h1 {
        color: #FFFFFF !important;
        text-shadow: 
            0 3px 12px rgba(0,0,0,0.6),
            0 6px 20px rgba(0,0,0,0.4),
            0 9px 30px rgba(0,0,0,0.3),
            0 2px 4px rgba(0,0,0,0.8) !important;
    }

    .banner .main-header {
        color: #FFFFFF !important;
        text-shadow: 
            0 3px 12px rgba(0,0,0,0.6),
            0 6px 20px rgba(0,0,0,0.4),
            0 9px 30px rgba(0,0,0,0.3),
            0 2px 4px rgba(0,0,0,0.8) !important;
    }

    /* CSS adicional para forzar blanco */
    div[data-testid="stMarkdownContainer"] h1 {
        color: #FFFFFF !important;
        text-shadow: 
            0 3px 12px rgba(0,0,0,0.6),
            0 6px 20px rgba(0,0,0,0.4),
            0 9px 30px rgba(0,0,0,0.3),
            0 2px 4px rgba(0,0,0,0.8) !important;
    }

    .stMarkdown h1 {
        color: #FFFFFF !important;
        text-shadow: 
            0 3px 12px rgba(0,0,0,0.6),
            0 6px 20px rgba(0,0,0,0.4),
            0 9px 30px rgba(0,0,0,0.3),
            0 2px 4px rgba(0,0,0,0.8) !important;
    }

    .sub-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #FFFFFF;
        text-shadow: 
            0 2px 8px rgba(0,0,0,0.7),
            0 4px 12px rgba(0,0,0,0.5),
            0 1px 3px rgba(0,0,0,0.9);
        margin-top: 0.5rem;
        position: relative;
        letter-spacing: 1px;
        animation: fadeInUp 1.2s ease-out;
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ===== TARJETAS KPI MEJORADAS CON EFECTOS VIVOS ===== */
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
        position: relative;
        overflow: hidden;
    }

    /* Efecto de brillo turquesa que se desliza */
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(6, 214, 160, 0.3), 
            rgba(46, 134, 171, 0.4),
            rgba(6, 214, 160, 0.3),
            transparent);
        transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1;
        border-radius: 14px;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(6, 214, 160, 0.2), 0 8px 20px rgba(46, 134, 171, 0.15);
        border-left: 5px solid #118AB2;
    }

    /* Ajuste de las métricas de Streamlit dentro de las tarjetas */
    .metric-card [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #2E86AB !important;
    }

    .metric-card [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #6C757D !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-card [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* ===== TABS MEJORADOS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 25px;
        background-color: #F8F9FA;
        border-radius: 12px 12px 0 0;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E9ECEF;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E86AB 0%, #06D6A0 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(46, 134, 171, 0.3);
    }

    /* ===== MODO RÁPIDO ===== */
    .fast-mode {
        border: 2px solid #FFD166;
        background: linear-gradient(135deg, #FFF9EC 0%, #FFFBF0 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(255, 209, 102, 0.15);
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 12px rgba(255, 209, 102, 0.15); }
        50% { box-shadow: 0 6px 20px rgba(255, 209, 102, 0.25); }
    }

    /* ===== AJUSTES GENERALES ===== */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }

    /* Títulos de secciones */
    h2 {
        color: #0891b2;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid #06D6A0;
        padding-bottom: 0.5rem;
    }

    /* Títulos de Streamlit específicos */
    .stMarkdown h2 {
        color: #0891b2 !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 2.5rem !important;
        border-bottom: 3px solid #06D6A0 !important;
        padding-bottom: 0.5rem !important;
        font-size: 2.2rem !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
    }

    /* Todos los elementos h2 en Streamlit */
    div[data-testid="stMarkdownContainer"] h2 {
        color: #0891b2 !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 2.5rem !important;
        border-bottom: 3px solid #06D6A0 !important;
        padding-bottom: 0.5rem !important;
        font-size: 2.2rem !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
    }

    /* Sidebar mejorado */
    .css-1d391kg {
        background-color: #FFFFFF;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }

    /* Título de sidebar con color del tema */
    .css-1d391kg h1 {
        color: #2E86AB !important;
        font-weight: 700 !important;
    }

    /* Selectores específicos para h3 en sidebar - MISMO FORMATO QUE TÍTULOS PRINCIPALES */
    .stSidebar h3 {
        color: #0891b2 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
        font-size: 1.5rem !important;
    }

    div[data-testid="stSidebar"] h3 {
        color: #0891b2 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
        font-size: 1.5rem !important;
    }

    .stSidebar .stMarkdown h3 {
        color: #0891b2 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
        font-size: 1.5rem !important;
    }

    /* Forzar color en todos los h3 de sidebar */
    .stSidebar h3, .stSidebar h3 *, 
    div[data-testid="stSidebar"] h3, 
    div[data-testid="stSidebar"] h3 * {
        color: #0891b2 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(8, 145, 178, 0.3) !important;
        font-size: 1.5rem !important;
    }

    /* Selectores específicos para h4 en sidebar - TAMAÑO MÁS PEQUEÑO */
    .stSidebar h4 {
        color: #0891b2 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(8, 145, 178, 0.2) !important;
        font-size: 1.1rem !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stSidebar"] h4 {
        color: #0891b2 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(8, 145, 178, 0.2) !important;
        font-size: 1.1rem !important;
        line-height: 1.2 !important;
    }

    .stSidebar .stMarkdown h4 {
        color: #0891b2 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(8, 145, 178, 0.2) !important;
        font-size: 1.1rem !important;
        line-height: 1.2 !important;
    }

    /* Forzar color en todos los h4 de sidebar */
    .stSidebar h4, .stSidebar h4 *, 
    div[data-testid="stSidebar"] h4, 
    div[data-testid="stSidebar"] h4 * {
        color: #0891b2 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(8, 145, 178, 0.2) !important;
        font-size: 1.1rem !important;
        line-height: 1.2 !important;
    }

    # Dentro de tu st.markdown con el CSS, agrega esto al final:

    /* ===== KPI CARDS MEJORADAS (Todo en una tarjeta) ===== */

    /* Sidebar más limpio */
    .css-1d391kg {
        background-color: #FFFFFF;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        padding: 1rem !important;
    }

    /* Botón de descarga con gradiente */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #06D6A0 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3) !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        line-height: 1.2 !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
    }

    /* Botones del sidebar */
    .stButton > button {
        background: linear-gradient(135deg, #2E86AB 0%, #06D6A0 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(46, 134, 171, 0.3);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(46, 134, 171, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Header con imagen de fondo
st.markdown("""
    <div class="banner">
        <h1 class="main-header">🥑 SANO Y FRESCO</h1>
        <p class="sub-header">Dashboard Ejecutivo | Inteligencia de Negocios 2025</p>
    </div>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS MEJORADA ---
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    """Cargar todos los datasets con validación"""
    try:
        kpis = pd.read_csv('data/kpis_diarios.csv')
        if kpis.empty:
            st.error("❌ El archivo kpis_diarios.csv está vacío")
            return None, None, None
            
        kpis['fecha'] = pd.to_datetime(kpis['fecha'])
        clientes = pd.read_csv('data/analisis_clientes.csv')
        
        # Manejar columnas de fecha si existen
        if 'primera_compra' in clientes.columns:
            clientes['primera_compra'] = pd.to_datetime(clientes['primera_compra'])
        if 'ultima_compra' in clientes.columns:
            clientes['ultima_compra'] = pd.to_datetime(clientes['ultima_compra'])
            
        productos = pd.read_csv('data/analisis_productos.csv')
        
        return kpis, clientes, productos
    except FileNotFoundError as e:
        st.error(f"❌ Error cargando archivos: {e}")
        st.info("📁 Asegúrate de que los archivos estén en la carpeta 'data/': kpis_diarios.csv, analisis_clientes.csv, analisis_productos.csv")
        return None, None, None
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        return None, None, None

# Cargar datos
with st.spinner('🔄 Cargando datos...'):
    kpis, clientes, productos = load_data()

if kpis is None or clientes is None or productos is None:
    st.error("No se pudieron cargar los datos. Verifica los archivos en la carpeta 'data/'.")
    st.stop()



# Calcular métricas globales
metricas = calcular_metricas_globales(kpis)
clientes = segmentar_clientes_valor(clientes)

# --- SIDEBAR SIMPLIFICADA ---
# Título usando st.markdown con CSS específico
st.sidebar.markdown("### Panel de Control")
st.sidebar.markdown("---")

# Solo filtros de fecha
st.sidebar.markdown("#### 📅 Período de Análisis")

fecha_min = kpis['fecha'].min().date()
fecha_max = kpis['fecha'].max().date()

fecha_inicio = st.sidebar.date_input(
    "Fecha inicio",
    value=fecha_min,
    min_value=fecha_min,
    max_value=fecha_max,
    label_visibility="collapsed"
)

fecha_fin = st.sidebar.date_input(
    "Fecha fin",
    value=fecha_max,
    min_value=fecha_min,
    max_value=fecha_max,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Botón de exportación con formato mejorado
csv = kpis.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Descargar Reporte\nCSV",
    data=csv,
    file_name="reporte_sano_fresco.csv",
    mime="text/csv",
    type="primary"
)

# Variables necesarias
modo_rapido = False
mostrar_graficos_pesados = True
kpis_filtrado = kpis
metricas_filtradas = metricas
clientes_filtrados = clientes

# --- KPIS PRINCIPALES MEJORADOS ---
st.markdown("## 📊 Métricas / KPIs")

# Crear las 4 columnas
col1, col2, col3, col4 = st.columns(4)

# KPI 1: Ventas Totales
with col1:
    st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">💰</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Ventas Totales
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #059669; margin: 10px 0;">
                ${:,.0f}
            </div>
            <div style="font-size: 0.9rem; color: #059669; font-weight: 600;">
                ▲ ${:.1f}M
            </div>
        </div>
    """.format(
        metricas_filtradas['ventas_totales'],
        metricas_filtradas['ventas_totales']/1000000
    ), unsafe_allow_html=True)

# KPI 2: Pedidos
with col2:
    st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">🛒</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Pedidos
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #2563eb; margin: 10px 0;">
                {:,}
            </div>
            <div style="font-size: 0.9rem; color: #2563eb; font-weight: 600;">
                ▲ {:.0f}/día
            </div>
        </div>
    """.format(
        metricas_filtradas['pedidos_totales'],
        metricas_filtradas['pedidos_totales'] / max(1, metricas_filtradas['dias_operacion'])
    ), unsafe_allow_html=True)

# KPI 3: Ticket Promedio
with col3:
    st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">🎫</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Ticket Promedio
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #d97706; margin: 10px 0;">
                ${:.2f}
            </div>
            <div style="font-size: 0.9rem; color: #d97706; font-weight: 600;">
                ◆ Objetivo: $25.00
            </div>
        </div>
    """.format(metricas_filtradas['ticket_promedio']), unsafe_allow_html=True)

# KPI 4: Clientes Únicos
with col4:
    st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem; margin-right: 10px;">👥</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #6C757D; text-transform: uppercase;">
                    Clientes Únicos
                </span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 700; color: #7c3aed; margin: 10px 0;">
                {:,}
            </div>
            <div style="font-size: 0.9rem; color: #7c3aed; font-weight: 600;">
                ▲ {:,} registrados
            </div>
        </div>
    """.format(
        metricas_filtradas['clientes_unicos'],
        len(clientes_filtrados)
    ), unsafe_allow_html=True)

st.markdown("---")

# --- SECCIÓN: TENDENCIAS ---
st.markdown("## 📈 Análisis de Tendencias")

if not modo_rapido:
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            crear_grafico_tendencia_ventas(kpis_filtrado),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            crear_grafico_distribucion_clientes(clientes_filtrados),
            use_container_width=True
        )
else:
    # En modo rápido, solo mostrar el gráfico principal
    st.plotly_chart(
        crear_grafico_tendencia_ventas(kpis_filtrado),
        use_container_width=True
    )


# --- ANÁLISIS DE PRODUCTOS MEJORADO ---
st.markdown("## 🏆 Análisis Profundo de Productos")

if not modo_rapido:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Top Ventas", 
        "🔥 Más Frecuentes", 
        "💎 Mayor Precio",
        "💰 Cascada Contribución",
        "📊 Análisis Pareto"
    ])

    with tab1:
        # Crear gráfico directamente con ordenamiento garantizado
        top_ventas = productos.nlargest(15, 'ventas_totales')
        fig = go.Figure(data=[
            go.Bar(
                y=top_ventas['nombre_producto'],
                x=top_ventas['ventas_totales'],
                orientation='h',
                text=top_ventas['ventas_totales'],
                texttemplate='<b>$%{text:,.0f}</b>',
                textposition='outside',
                marker=dict(
                    color='#0891b2',  # Color del tema
                    line=dict(color='#047857', width=3),  # Borde grueso para efecto
                    # Efecto Power BI con esquinas redondeadas
                    cornerradius=8  # Esquinas redondeadas para efecto moderno
                )
            )
        ])
        fig.update_layout(
            xaxis_title='Ventas Totales ($)',
            yaxis_title='',
            height=500,
            font=dict(size=12, family='Arial, sans-serif'),
            margin=dict(l=60, r=60, t=40, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder':'total ascending'},
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            ),
            # Efecto Power BI con sombra
            barmode='group',
            bargap=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Crear gráfico directamente con ordenamiento garantizado
        top_pedidos = productos.nlargest(15, 'pedidos_unicos')
        fig = go.Figure(data=[
            go.Bar(
                y=top_pedidos['nombre_producto'],
                x=top_pedidos['pedidos_unicos'],
                orientation='h',
                text=top_pedidos['pedidos_unicos'],
                texttemplate='<b>%{text:,.0f}</b>',
                textposition='outside',
                marker=dict(
                    color='#06D6A0',  # Verde turquesa del tema
                    line=dict(color='#047857', width=3),  # Borde grueso para efecto
                    # Efecto Power BI con esquinas redondeadas
                    cornerradius=8  # Esquinas redondeadas para efecto moderno
                )
            )
        ])
        fig.update_layout(
            xaxis_title='Pedidos Únicos',
            yaxis_title='',
            height=500,
            font=dict(size=12, family='Arial, sans-serif'),
            margin=dict(l=60, r=60, t=40, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder':'total ascending'},
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Crear gráfico directamente con ordenamiento garantizado
        top_precio = productos.nlargest(15, 'precio_promedio')
        fig = go.Figure(data=[
            go.Bar(
                y=top_precio['nombre_producto'],
                x=top_precio['precio_promedio'],
                orientation='h',
                text=top_precio['precio_promedio'],
                texttemplate='<b>$%{text:.2f}</b>',
                textposition='outside',
                marker=dict(
                    color='#059669',  # Verde del tema
                    line=dict(color='#047857', width=3),  # Borde grueso para efecto
                    # Efecto Power BI con esquinas redondeadas
                    cornerradius=8  # Esquinas redondeadas para efecto moderno
                )
            )
        ])
        fig.update_layout(
            xaxis_title='Precio Promedio ($)',
            yaxis_title='',
            height=500,
            font=dict(size=12, family='Arial, sans-serif'),
            margin=dict(l=60, r=60, t=40, b=60),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder':'total ascending'},
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.plotly_chart(
            crear_waterfall_contribucion(productos, 10),
            use_container_width=True
        )
        st.info("💡 **Insight:** Este gráfico muestra cómo cada producto contribuye al total de ventas.")

    with tab5:
        st.plotly_chart(
            crear_grafico_pareto(productos),
            use_container_width=True
        )
        st.warning("⚠️ **Regla 80/20:** Identifica qué productos generan el 80% de tus ingresos.")
else:
    # En modo rápido, solo mostrar pestañas esenciales
    tab1, tab2 = st.tabs(["📊 Top Ventas", "📈 Análisis Pareto"])
    
    with tab1:
        st.plotly_chart(
            crear_grafico_top_productos(productos, 'ventas_totales', 10),
            use_container_width=True
        )
    
    with tab2:
        st.plotly_chart(
            crear_grafico_pareto(productos),
            use_container_width=True
        )

# --- VISUALIZACIONES AVANZADAS ---
if not modo_rapido and mostrar_graficos_pesados:
    st.markdown("---")
    st.markdown("## 🗺️ Visualizaciones Avanzadas")

    col1, col2 = st.columns(2)

    with col1:
        with st.spinner('Generando diagrama Sankey...'):
            st.plotly_chart(
                crear_sankey_segmentos(clientes_filtrados),
                use_container_width=True
            )

    with col2:
        st.plotly_chart(
            crear_treemap_productos(productos),
            use_container_width=True
        )

# --- HEATMAP ---
if not modo_rapido:
    st.markdown("## 🗓️ Patrón de Ventas Semanal")
    st.plotly_chart(
        crear_heatmap_ventas_mensual(kpis_filtrado),
        use_container_width=True
    )

# --- ANÁLISIS DE CORRELACIONES (AL FINAL) ---
if not modo_rapido and mostrar_graficos_pesados:
    st.markdown("---")
    st.markdown("## 🔗 Mapa de Correlaciones")
    with st.spinner('Calculando correlaciones...'):
        st.plotly_chart(
            crear_mapa_correlaciones(kpis_filtrado),
            use_container_width=True
        )

# --- OBJETIVOS (AL FINAL) ---
st.markdown("---")
st.markdown("## 🎯 Progreso vs Objetivos")

# Objetivos más realistas basados en tus datos
objetivos = {
    'ventas': 5000000,      # 5 millones
    'pedidos': 250000,      # 250 mil pedidos (ajustado)
    'clientes': 15000       # 15 mil clientes (ajustado)
}

st.plotly_chart(
    crear_grafico_progreso_objetivos(metricas_filtradas, objetivos),
    use_container_width=True
)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;'>
    <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
    <p style='color: #6c757d; font-size: 0.9rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
</div>
""", unsafe_allow_html=True)

# JavaScript AGRESIVO para forzar el color del título de sidebar
st.markdown("""
<script>
// Función para aplicar estilos AGRESIVAMENTE a h3 y h4
function forceSidebarTitleColor() {
    // Buscar TODOS los elementos h3 posibles
    const h3Selectors = [
        '.stSidebar h3',
        'div[data-testid="stSidebar"] h3',
        '.stSidebar .stMarkdown h3',
        'h3[data-testid="stSidebar"]',
        '.stSidebar h3 *',
        'div[data-testid="stSidebar"] h3 *'
    ];
    
    h3Selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.setProperty('color', '#0891b2', 'important');
            element.style.setProperty('font-weight', '700', 'important');
            element.style.setProperty('text-shadow', '2px 2px 4px rgba(8, 145, 178, 0.3)', 'important');
            element.style.setProperty('font-size', '1.5rem', 'important');
        });
    });
    
    // Buscar TODOS los elementos h4 posibles (más pequeños)
    const h4Selectors = [
        '.stSidebar h4',
        'div[data-testid="stSidebar"] h4',
        '.stSidebar .stMarkdown h4',
        'h4[data-testid="stSidebar"]',
        '.stSidebar h4 *',
        'div[data-testid="stSidebar"] h4 *'
    ];
    
    h4Selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            element.style.setProperty('color', '#0891b2', 'important');
            element.style.setProperty('font-weight', '600', 'important');
            element.style.setProperty('text-shadow', '1px 1px 2px rgba(8, 145, 178, 0.2)', 'important');
            element.style.setProperty('font-size', '1.1rem', 'important');
            element.style.setProperty('line-height', '1.2', 'important');
        });
    });
    
    // Buscar por texto específico y aplicar a TODOS los elementos
    const allElements = document.querySelectorAll('*');
    allElements.forEach(element => {
        if (element.textContent && element.textContent.includes('Panel de Control')) {
            element.style.setProperty('color', '#0891b2', 'important');
            element.style.setProperty('font-weight', '700', 'important');
            element.style.setProperty('text-shadow', '2px 2px 4px rgba(8, 145, 178, 0.3)', 'important');
            element.style.setProperty('font-size', '1.5rem', 'important');
        }
        if (element.textContent && element.textContent.includes('Período de Análisis')) {
            element.style.setProperty('color', '#0891b2', 'important');
            element.style.setProperty('font-weight', '600', 'important');
            element.style.setProperty('text-shadow', '1px 1px 2px rgba(8, 145, 178, 0.2)', 'important');
            element.style.setProperty('font-size', '1.1rem', 'important');
            element.style.setProperty('line-height', '1.2', 'important');
        }
    });
}

// Ejecutar múltiples veces para asegurar que se aplique
setTimeout(forceSidebarTitleColor, 500);
setTimeout(forceSidebarTitleColor, 1000);
setTimeout(forceSidebarTitleColor, 2000);
setTimeout(forceSidebarTitleColor, 3000);

// También ejecutar cuando cambie el DOM
const observer = new MutationObserver(forceSidebarTitleColor);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)