import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import io
import base64

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
    crear_grafico_velocimetro_multiple
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
    page_icon="🥑",
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
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            0 1px 8px rgba(0, 0, 0, 0.2);
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
        font-size: 4.5rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 
            0 2px 10px rgba(0,0,0,0.5),
            0 4px 20px rgba(0,0,0,0.3),
            0 8px 30px rgba(0,0,0,0.2);
        margin: 0;
        position: relative;
        letter-spacing: 4px;
        animation: fadeInDown 1s ease-out;
    }

    .sub-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #FFFFFF;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);
        margin-top: 1rem;
        position: relative;
        letter-spacing: 2px;
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

    /* ===== TARJETAS KPI ESTILO POWER BI ===== */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        padding: 1.8rem 1.5rem;
        border-radius: 16px;
        border-left: 6px solid #2E86AB;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.08),
            0 1px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    /* Efecto de brillo sutil en la tarjeta */
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.5s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 12px 30px rgba(46, 134, 171, 0.15),
            0 5px 15px rgba(0, 0, 0, 0.1);
        border-left-color: #06D6A0;
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
        background-color: #F5F7FA;
    }

    /* Títulos de secciones */
    h2 {
        color: #2E86AB;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #06D6A0;
        padding-bottom: 0.5rem;
    }

    /* Sidebar mejorado */
    .css-1d391kg {
        background-color: #FFFFFF;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }

    # Dentro de tu st.markdown con el CSS, agrega esto al final:

    /* ===== KPI CARDS MEJORADAS (Todo en una tarjeta) ===== */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        padding: 1.8rem 1.5rem;
        border-radius: 16px;
        border-left: 6px solid #2E86AB;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.08),
            0 1px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-height: 140px;
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
            rgba(255, 255, 255, 0.4), 
            transparent);
        transition: left 0.6s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 12px 30px rgba(46, 134, 171, 0.2),
            0 5px 15px rgba(0, 0, 0, 0.15);
        border-left-color: #06D6A0;
    }

    /* Sidebar más limpio */
    .css-1d391kg {
        background-color: #FFFFFF;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        padding: 1rem !important;
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
        <p class="sub-header">Dashboard Ejecutivo | Inteligencia de Negocios 2023</p>
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

# --- SIDEBAR MINIMALISTA ---
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("---")

# Solo filtros de fecha
st.sidebar.markdown("### 📅 Período de Análisis")

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

# --- FILTRADO DE DATOS (ANTES DE USARLO EN SIDEBAR) ---
kpis_filtrado = kpis[
    (kpis['fecha'] >= pd.to_datetime(fecha_inicio)) &
    (kpis['fecha'] <= pd.to_datetime(fecha_fin))
]

# Solo 2 métricas clave
st.sidebar.metric(
    "📊 Días Analizados", 
    len(kpis_filtrado),
    delta=None
)

st.sidebar.metric(
    "📈 Rango", 
    f"{fecha_inicio.strftime('%d/%m')} - {fecha_fin.strftime('%d/%m')}",
    delta=None
)

st.sidebar.markdown("---")

# Filtros opcionales colapsados
with st.sidebar.expander("🔧 Filtros Avanzados"):
    # Filtro por segmento
    segmentos_disponibles = ['Todos'] + list(clientes['segmento'].unique())
    segmento_seleccionado = st.selectbox(
        "Segmento de Cliente",
        segmentos_disponibles,
        label_visibility="collapsed"
    )
    
    # Modo rápido
    modo_rapido = st.checkbox(
        "🚀 Modo Rápido", 
        value=False,
        help="Muestra solo gráficos esenciales"
    )
    
    mostrar_graficos_pesados = st.checkbox(
        "📊 Gráficos Avanzados", 
        value=True,
        help="Mostrar análisis complejos"
    )

st.sidebar.markdown("---")

# Botón de exportación compacto
if st.sidebar.button("📥 Exportar Reporte", use_container_width=True):
    # Generar reporte simple
    reporte_df = pd.DataFrame({
        'Métrica': ['Ventas Totales', 'Pedidos Totales', 'Ticket Promedio', 'Clientes Únicos'],
        'Valor': [
            metricas['ventas_totales'],
            metricas['pedidos_totales'],
            metricas['ticket_promedio'],
            metricas['clientes_unicos']
        ]
    })
    csv = reporte_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="reporte_sano_fresco.csv" style="text-decoration: none; color: #06D6A0;">📥 Descargar CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Filtrar clientes por segmento
if segmento_seleccionado != 'Todos':
    clientes_filtrados = clientes[clientes['segmento'] == segmento_seleccionado]
else:
    clientes_filtrados = clientes

# Recalcular métricas con datos filtrados
metricas_filtradas = calcular_metricas_globales(kpis_filtrado)

# Indicador de modo rápido
if modo_rapido:
    st.markdown('<div class="fast-mode">🚀 <strong>Modo Rápido Activado:</strong> Mostrando solo gráficos esenciales</div>', 
                unsafe_allow_html=True)

# --- KPIS PRINCIPALES MEJORADOS ---
st.markdown("## 📊 KPIs Clave de Desempeño")

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
            <div style="font-size: 2.2rem; font-weight: 700; color: #2E86AB; margin: 10px 0;">
                ${:,.0f}
            </div>
            <div style="font-size: 0.9rem; color: #06D6A0; font-weight: 600;">
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
            <div style="font-size: 2.2rem; font-weight: 700; color: #2E86AB; margin: 10px 0;">
                {:,}
            </div>
            <div style="font-size: 0.9rem; color: #06D6A0; font-weight: 600;">
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
            <div style="font-size: 2.2rem; font-weight: 700; color: #2E86AB; margin: 10px 0;">
                ${:.2f}
            </div>
            <div style="font-size: 0.9rem; color: #FFD166; font-weight: 600;">
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
            <div style="font-size: 2.2rem; font-weight: 700; color: #2E86AB; margin: 10px 0;">
                {:,}
            </div>
            <div style="font-size: 0.9rem; color: #06D6A0; font-weight: 600;">
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

# --- ANÁLISIS DE CORRELACIONES ---
if not modo_rapido and mostrar_graficos_pesados:
    st.markdown("## 🔗 Mapa de Correlaciones")
    with st.spinner('Calculando correlaciones...'):
        st.plotly_chart(
            crear_mapa_correlaciones(kpis_filtrado),
            use_container_width=True
        )

st.markdown("---")

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
        st.plotly_chart(
            crear_grafico_top_productos(productos, 'ventas_totales', 15),
            use_container_width=True
        )

    with tab2:
        st.plotly_chart(
            crear_grafico_top_productos(productos, 'pedidos_unicos', 15),
            use_container_width=True
        )

    with tab3:
        st.plotly_chart(
            crear_grafico_top_productos(productos, 'precio_promedio', 15),
            use_container_width=True
        )

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

# --- OBJETIVOS ---
st.markdown("---")
st.markdown("## 🎯 Progreso vs Objetivos")

# Objetivos más realistas basados en tus datos
objetivos = {
    'ventas': 5000000,      # 5 millones
    'pedidos': 250000,      # 250 mil pedidos (ajustado)
    'clientes': 15000       # 15 mil clientes (ajustado)
}

st.plotly_chart(
    crear_grafico_velocimetro_multiple(metricas_filtradas, objetivos),
    use_container_width=True
)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;'>
    <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d;'>📊 Análisis de Datos 2023 | 🔄 Actualizado en Tiempo Real | 🚀 v2.0 Mejorado</p>
    <p style='color: #6c757d; font-size: 0.8rem;'>Modo Rápido: {modo_rapido} | Gráficos Avanzados: {avanzados}</p>
</div>
""".format(
    modo_rapido="✅ Activado" if modo_rapido else "❌ Desactivado",
    avanzados="✅ Activados" if mostrar_graficos_pesados else "❌ Desactivados"
), unsafe_allow_html=True)
