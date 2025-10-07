import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Agregar utils al path
sys.path.append(str(Path(__file__).parent))

from utils.metrics import (
    calcular_metricas_globales,
    calcular_crecimiento,
    identificar_productos_estrella,
    segmentar_clientes_valor
)
from utils.visualizations import (
    crear_grafico_tendencia_ventas,
    crear_grafico_distribucion_clientes,
    crear_grafico_top_productos,
    crear_heatmap_ventas_mensual,
    crear_gauge_chart
)

# Configuración de la página
st.set_page_config(
    page_title="Sano y Fresco - Dashboard Ejecutivo",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
    <style>
    /* Banner superior */
    .banner {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 2.5rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }

    .banner:hover {
        transform: scale(1.01);
        transition: transform 0.3s ease;
    }

    /* Título principal */
    .main-header {
        font-size: 4.5rem;
        font-weight: 700;
        color: #FFFFFF;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.7);
        -webkit-text-stroke: 1px #2E86AB;
        margin: 0;
        animation: fadeIn 1.5s ease-in-out;
    }

    /* Subtítulo */
    .sub-header {
        font-size: 1.8rem;
        color: #F1C40F;
        font-style: italic;
        margin-top: 0.5rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* Estilo de notificaciones */
    .status-message {
        font-size: 1rem;
        color: #28A745;
        font-weight: 500;
        padding: 0.5rem 1rem;
        background-color: #e9f7ef;
        border-radius: 5px;
        display: inline-block;
        margin-bottom: 1rem;
    }

    /* Estilo de las métricas */
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 0.6rem;
        border-left: 5px solid #2E86AB;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-2px);
    }

    /* Ajuste general */
    .stApp {
        background-color: #F5F6F5;
        padding: 1rem 2rem;
    }

    /* Animación de entrada */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        padding: 1rem;
        background-color: #FFFFFF;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header mejorado con banner
st.markdown("""
    <div class="banner">
        <h1 class="main-header">🥑 Sano y Fresco</h1>
        <p class="sub-header">Tu Dashboard Ejecutivo para un Negocio Saludable</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("### 📊 Dashboard Ejecutivo 2023 | Sistema de Rescate Empresarial")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    """Cargar todos los datasets"""
    kpis = pd.read_csv('data/kpis_diarios.csv')
    kpis['fecha'] = pd.to_datetime(kpis['fecha'])
    clientes = pd.read_csv('data/analisis_clientes.csv')
    clientes['primera_compra'] = pd.to_datetime(clientes['primera_compra'])
    clientes['ultima_compra'] = pd.to_datetime(clientes['ultima_compra'])
    productos = pd.read_csv('data/analisis_productos.csv')
    return kpis, clientes, productos

# Cargar datos
with st.spinner('Procesando datos...'):
    kpis, clientes, productos = load_data()

if not all(col in kpis.columns for col in ['ventas_totales', 'fecha', 'pedidos_unicos']):
    st.error("Error: Faltan columnas en kpis_diarios.csv.")
elif not all(col in clientes.columns for col in ['gasto_total', 'segmento']):
    st.error("Error: Faltan columnas en analisis_clientes.csv.")
elif not all(col in productos.columns for col in ['ventas_totales', 'pedidos_unicos', 'precio_promedio']):
    st.error("Error: Faltan columnas en analisis_productos.csv.")
else:
    st.markdown('<div class="status-message">Datos procesados con éxito</div>', unsafe_allow_html=True)

# Calcular métricas globales
metricas = calcular_metricas_globales(kpis)

# Resegmentar clientes si es necesario (usando 'gasto_total')
clientes = segmentar_clientes_valor(clientes)

# --- SIDEBAR ---
st.sidebar.header("🎛️ Filtros y Configuración")

# Filtro de fechas
fecha_min = kpis['fecha'].min().date()
fecha_max = kpis['fecha'].max().date()

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

# Filtrar datos por fecha
kpis_filtrado = kpis[
    (kpis['fecha'] >= pd.to_datetime(fecha_inicio)) &
    (kpis['fecha'] <= pd.to_datetime(fecha_fin))
]

st.sidebar.markdown("---")
st.sidebar.info(f"""
📅 **Período seleccionado:**  
{fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}

📊 **Días analizados:** {len(kpis_filtrado)}
""")

# --- KPIS PRINCIPALES ---
st.markdown("## 📈 KPIs Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="💰 Ventas Totales",
        value=f"${metricas['ventas_totales']:,.0f}",
        delta=f"{(metricas['ventas_totales'] / 1000000):.1f}M"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="🛒 Pedidos",
        value=f"{metricas['pedidos_totales']:,}",
        delta=f"{(metricas['pedidos_totales'] / metricas['dias_operacion']):.0f}/día"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="🎫 Ticket Promedio",
        value=f"${metricas['ticket_promedio']:.2f}",
        delta="Objetivo: $25"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="👥 Clientes Únicos",
        value=f"{metricas['clientes_unicos']:,}",
        delta=f"{len(clientes)} registrados"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- GRÁFICOS PRINCIPALES ---
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        crear_grafico_tendencia_ventas(kpis_filtrado),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        crear_grafico_distribucion_clientes(clientes),
        use_container_width=True
    )

# --- ANÁLISIS DE PRODUCTOS ---
st.markdown("## 🏆 Análisis de Productos")

tab1, tab2, tab3 = st.tabs(["📊 Top Ventas", "🔥 Más Frecuentes", "💎 Mayor Precio Promedio"])

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

# --- HEATMAP ---
st.markdown("## 🗓️ Patrón de Ventas por Día y Mes")
st.plotly_chart(
    crear_heatmap_ventas_mensual(kpis_filtrado),
    use_container_width=True
)

# --- OBJETIVOS ---
st.markdown("## 🎯 Progreso vs Objetivos")

objetivo_ventas = 5000000  # 5M (ajusta según necesidades)
objetivo_pedidos = 2500000  # 2.5M
objetivo_clientes = 150000  # 150K

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(
        crear_gauge_chart(
            metricas['ventas_totales'],
            objetivo_ventas,
            "Ventas vs Objetivo"
        ),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        crear_gauge_chart(
            metricas['pedidos_totales'],
            objetivo_pedidos,
            "Pedidos vs Objetivo"
        ),
        use_container_width=True
    )

with col3:
    st.plotly_chart(
        crear_gauge_chart(
            metricas['clientes_unicos'],
            objetivo_clientes,
            "Clientes vs Objetivo"
        ),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d;'>
    <p>🥑 Sano y Fresco Dashboard | Desarrollado con Streamlit | © 2024</p>
</div>
""", unsafe_allow_html=True)