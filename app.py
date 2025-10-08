import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import io
import base64

# Agregar utils al path
sys.path.append(str(Path(__file__).parent))

# Importaciones de métricas (sin visualizaciones que usan Plotly)
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
        st.subheader("Evolución de Ventas")
        st.line_chart(kpis_filtrado.set_index('fecha')['ventas_totales'])

    with col2:
        st.subheader("Distribución de Clientes")
        if 'segmento' in clientes_filtrados.columns:
            segmentos = clientes_filtrados['segmento'].value_counts()
            st.bar_chart(segmentos)
        else:
            st.metric("Total Clientes", f"{len(clientes_filtrados):,}")
else:
    # En modo rápido, solo mostrar el gráfico principal
    st.subheader("Evolución de Ventas")
    st.line_chart(kpis_filtrado.set_index('fecha')['ventas_totales'])

# --- ANÁLISIS DE PRODUCTOS MEJORADO ---
st.markdown("## 🏆 Análisis Profundo de Productos")

if not modo_rapido:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Top Ventas", 
        "🔥 Más Frecuentes", 
        "💎 Mayor Precio",
        "📈 Análisis Pareto",
        "📋 Detalles"
    ])

    with tab1:
        st.subheader("Top 15 Productos por Ventas")
        top_ventas = productos.nlargest(15, 'ventas_totales')
        st.bar_chart(top_ventas.set_index('nombre_producto')['ventas_totales'])

    with tab2:
        st.subheader("Top 15 Productos Más Frecuentes")
        top_pedidos = productos.nlargest(15, 'pedidos_unicos')
        st.bar_chart(top_pedidos.set_index('nombre_producto')['pedidos_unicos'])

    with tab3:
        st.subheader("Top 15 Productos por Precio")
        top_precio = productos.nlargest(15, 'precio_promedio')
        st.bar_chart(top_precio.set_index('nombre_producto')['precio_promedio'])

    with tab4:
        st.subheader("Análisis Pareto (80/20)")
        # Calcular contribución acumulada
        productos_ordenados = productos.sort_values('ventas_totales', ascending=False)
        productos_ordenados['ventas_acumuladas'] = productos_ordenados['ventas_totales'].cumsum()
        productos_ordenados['porcentaje_acumulado'] = (productos_ordenados['ventas_acumuladas'] / productos_ordenados['ventas_totales'].sum()) * 100
        
        # Mostrar los primeros 20 productos
        pareto_data = productos_ordenados.head(20)
        st.bar_chart(pareto_data.set_index('nombre_producto')['porcentaje_acumulado'])
        
        # Mostrar estadísticas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Productos que generan 80%", f"{len(pareto_data[pareto_data['porcentaje_acumulado'] <= 80]):,}")
        with col2:
            st.metric("Contribución 80%", f"{pareto_data[pareto_data['porcentaje_acumulado'] <= 80]['porcentaje_acumulado'].max():.1f}%")

    with tab5:
        st.subheader("Detalles Completos de Productos")
        st.dataframe(
            productos[['nombre_producto', 'ventas_totales', 'unidades_vendidas', 'precio_promedio', 'pedidos_unicos']].round(2),
            use_container_width=True
        )
else:
    # En modo rápido, solo mostrar pestañas esenciales
    tab1, tab2 = st.tabs(["📊 Top Ventas", "📈 Análisis Pareto"])
    
    with tab1:
        st.subheader("Top 10 Productos por Ventas")
        top_ventas = productos.nlargest(10, 'ventas_totales')
        st.bar_chart(top_ventas.set_index('nombre_producto')['ventas_totales'])
    
    with tab2:
        st.subheader("Análisis Pareto")
        productos_ordenados = productos.sort_values('ventas_totales', ascending=False)
        productos_ordenados['ventas_acumuladas'] = productos_ordenados['ventas_totales'].cumsum()
        productos_ordenados['porcentaje_acumulado'] = (productos_ordenados['ventas_acumuladas'] / productos_ordenados['ventas_totales'].sum()) * 100
        pareto_data = productos_ordenados.head(15)
        st.bar_chart(pareto_data.set_index('nombre_producto')['porcentaje_acumulado'])

# --- ANÁLISIS ADICIONAL ---
st.markdown("## 📊 Análisis Adicional")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Días de Operación", metricas_filtradas['dias_operacion'])
    st.metric("Productos Únicos", len(productos))

with col2:
    st.metric("Ventas Promedio Diaria", f"${metricas_filtradas['ventas_totales']/metricas_filtradas['dias_operacion']:,.0f}")
    st.metric("Pedidos Promedio Diario", f"{metricas_filtradas['pedidos_totales']/metricas_filtradas['dias_operacion']:,.0f}")

with col3:
    st.metric("Unidades Vendidas", f"{metricas_filtradas.get('unidades_vendidas', 0):,}")
    st.metric("Productos por Pedido", f"{metricas_filtradas.get('items_promedio', 0):.1f}")

# --- ANÁLISIS DE CLIENTES ---
if not modo_rapido:
    st.markdown("## 👥 Análisis de Clientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución por Segmento")
        if 'segmento' in clientes_filtrados.columns:
            segmentos = clientes_filtrados['segmento'].value_counts()
            st.bar_chart(segmentos)
        else:
            st.info("No hay información de segmentación disponible")
    
    with col2:
        st.subheader("Métricas de Clientes")
        st.metric("Total Clientes", f"{len(clientes_filtrados):,}")
        if 'valor_total' in clientes_filtrados.columns:
            st.metric("Valor Promedio", f"${clientes_filtrados['valor_total'].mean():,.2f}")
            st.metric("Cliente Más Valioso", f"${clientes_filtrados['valor_total'].max():,.2f}")

# --- OBJETIVOS (AL FINAL) ---
st.markdown("---")
st.markdown("## 🎯 Progreso vs Objetivos")

# Objetivos más realistas basados en tus datos
objetivos = {
    'ventas': 5000000,      # 5 millones
    'pedidos': 250000,      # 250 mil pedidos
    'clientes': 15000       # 15 mil clientes
}

col1, col2, col3 = st.columns(3)

with col1:
    progreso_ventas = (metricas_filtradas['ventas_totales'] / objetivos['ventas']) * 100
    st.metric(
        "Ventas Totales",
        f"${metricas_filtradas['ventas_totales']:,.0f}",
        f"{progreso_ventas:.1f}% del objetivo"
    )
    st.progress(min(progreso_ventas / 100, 1.0))

with col2:
    progreso_pedidos = (metricas_filtradas['pedidos_totales'] / objetivos['pedidos']) * 100
    st.metric(
        "Pedidos Totales",
        f"{metricas_filtradas['pedidos_totales']:,}",
        f"{progreso_pedidos:.1f}% del objetivo"
    )
    st.progress(min(progreso_pedidos / 100, 1.0))

with col3:
    progreso_clientes = (metricas_filtradas['clientes_unicos'] / objetivos['clientes']) * 100
    st.metric(
        "Clientes Únicos",
        f"{metricas_filtradas['clientes_unicos']:,}",
        f"{progreso_clientes:.1f}% del objetivo"
    )
    st.progress(min(progreso_clientes / 100, 1.0))

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