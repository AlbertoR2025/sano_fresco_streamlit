import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
    </style>
""", unsafe_allow_html=True)

# Header con imagen de fondo
st.markdown("""
    <div class="banner">
        <h1 class="main-header">🥑 SANO Y FRESCO</h1>
        <p class="sub-header">Dashboard Ejecutivo | Inteligencia de Negocios 2025</p>
    </div>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data(ttl=3600)
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

# Calcular métricas básicas
ventas_totales = kpis['ventas_totales'].sum()
pedidos_totales = kpis['pedidos_unicos'].sum()
ticket_promedio = kpis['ticket_promedio'].mean()
clientes_unicos = kpis['clientes_unicos'].sum()

# --- KPIS PRINCIPALES MEJORADOS ---
st.markdown("## 📊 Métricas / KPIs")

# Crear las 4 columnas
col1, col2, col3, col4 = st.columns(4)

# KPI 1: Ventas Totales
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
                ▲ ${ventas_totales/1000000:.1f}M
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI 2: Pedidos
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
                {pedidos_totales:,}
            </div>
            <div style="font-size: 0.9rem; color: #2563eb; font-weight: 600;">
                ▲ {pedidos_totales / max(1, len(kpis)):.0f}/día
            </div>
        </div>
    """, unsafe_allow_html=True)

# KPI 3: Ticket Promedio
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

# KPI 4: Clientes Únicos
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
                {clientes_unicos:,}
            </div>
            <div style="font-size: 0.9rem; color: #7c3aed; font-weight: 600;">
                ▲ {len(clientes):,} registrados
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SECCIÓN: TENDENCIAS ---
st.markdown("## 📈 Análisis de Tendencias")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de tendencia de ventas
    fig_ventas = go.Figure()
    fig_ventas.add_trace(go.Scatter(
        x=kpis['fecha'],
        y=kpis['ventas_totales'],
        mode='lines',
        name='Ventas Diarias',
        line=dict(color='#059669', width=3),
        fill='tozeroy',
        fillcolor='rgba(5, 150, 105, 0.15)'
    ))
    fig_ventas.update_layout(
        title="Evolución de Ventas",
        xaxis_title="Fecha",
        yaxis_title="Ventas ($)",
        height=400,
        template="plotly_white"
    )
    st.plotly_chart(fig_ventas, use_container_width=True)

with col2:
    # Gráfico donut de distribución de clientes
    if 'segmento' in clientes.columns:
        segmentos = clientes['segmento'].value_counts()
        total_clientes = segmentos.sum()
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=segmentos.index,
            values=segmentos.values,
            hole=0.45,
            marker=dict(
                colors=['#545B62', '#FFD166', '#06D6A0', '#118AB2'],
                line=dict(color='white', width=3)
            ),
            hoverinfo="label+percent+value",
            textinfo="percent",
            textposition="inside",
            textfont=dict(size=15, color="white")
        )])
        
        fig_donut.update_layout(
            annotations=[dict(text=f'{total_clientes:,}<br>Clientes', x=0.5, y=0.5, font_size=16, showarrow=False, font_color='#2C3E50')],
            title="Distribución de Clientes por Segmento",
            showlegend=True,
            legend=dict(orientation="h", y=-0.2),
            template="plotly",
            height=420,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif")
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No se encontró información de segmentación de clientes")

# --- ANÁLISIS DE PRODUCTOS ---
st.markdown("## 🏆 Análisis de Productos")

# Top productos por ventas
top_productos = productos.nlargest(10, 'ventas_totales')

fig_productos = go.Figure(data=[
    go.Bar(
        y=top_productos['nombre_producto'],
        x=top_productos['ventas_totales'],
        orientation='h',
        text=top_productos['ventas_totales'],
        texttemplate='<b>$%{text:,.0f}</b>',
        textposition='outside',
        marker=dict(
            color='#0891b2',
            line=dict(color='#047857', width=3),
            cornerradius=8
        )
    )
])

fig_productos.update_layout(
    title="Top 10 Productos por Ventas",
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
    )
)

st.plotly_chart(fig_productos, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;'>
    <h3 style='color: #2E86AB;'>🥑 Sano y Fresco Dashboard</h3>
    <p style='color: #6c757d;'>📊 Análisis de Datos 2025 | 🔄 Actualizado en Tiempo Real</p>
    <p style='color: #6c757d; font-size: 0.9rem;'>🐍 Desarrollado con Python | ⚡ Powered by Streamlit | 📈 Visualización Interactiva</p>
</div>
""", unsafe_allow_html=True)
