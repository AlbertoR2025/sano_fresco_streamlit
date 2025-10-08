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

st.title("🥑 SANO Y FRESCO - Test de Importaciones")

# Probar importaciones una por una
try:
    st.write("🔄 Probando importaciones...")
    
    # Importar funciones básicas primero
    from utils.visualizations import crear_grafico_tendencia_ventas
    st.success("✅ crear_grafico_tendencia_ventas importada")
    
    from utils.visualizations import crear_grafico_distribucion_clientes
    st.success("✅ crear_grafico_distribucion_clientes importada")
    
    from utils.visualizations import crear_grafico_top_productos
    st.success("✅ crear_grafico_top_productos importada")
    
    from utils.visualizations import crear_heatmap_ventas_mensual
    st.success("✅ crear_heatmap_ventas_mensual importada")
    
    from utils.visualizations import crear_gauge_chart
    st.success("✅ crear_gauge_chart importada")
    
    from utils.visualizations import crear_mapa_correlaciones
    st.success("✅ crear_mapa_correlaciones importada")
    
    from utils.visualizations import crear_waterfall_contribucion
    st.success("✅ crear_waterfall_contribucion importada")
    
    from utils.visualizations import crear_sankey_segmentos
    st.success("✅ crear_sankey_segmentos importada")
    
    from utils.visualizations import crear_treemap_productos
    st.success("✅ crear_treemap_productos importada")
    
    from utils.visualizations import crear_grafico_pareto
    st.success("✅ crear_grafico_pareto importada")
    
    from utils.visualizations import crear_grafico_progreso_objetivos
    st.success("✅ crear_grafico_progreso_objetivos importada")
    
    st.success("🎉 ¡Todas las importaciones funcionan correctamente!")
    
except Exception as e:
    st.error(f"❌ Error en importación: {str(e)}")
    st.exception(e)

# Probar carga de datos
try:
    st.write("🔄 Probando carga de datos...")
    
    kpis_df = pd.read_csv('data/kpis_diarios.csv')
    st.success(f"✅ KPIs cargados: {len(kpis_df)} registros")
    
    productos_df = pd.read_csv('data/analisis_productos.csv')
    st.success(f"✅ Productos cargados: {len(productos_df)} registros")
    
    clientes_df = pd.read_csv('data/analisis_clientes.csv')
    st.success(f"✅ Clientes cargados: {len(clientes_df)} registros")
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {str(e)}")
    st.exception(e)

# Probar una función simple
try:
    st.write("🔄 Probando función simple...")
    
    # Crear datos de prueba
    test_data = pd.DataFrame({
        'fecha': pd.date_range('2024-01-01', periods=30),
        'ventas_totales': [1000 + i*10 for i in range(30)]
    })
    
    # Probar función de tendencias
    fig = crear_grafico_tendencia_ventas(test_data)
    st.success("✅ Función crear_grafico_tendencia_ventas ejecutada correctamente")
    
    st.plotly_chart(fig, use_container_width=True)
    
except Exception as e:
    st.error(f"❌ Error ejecutando función: {str(e)}")
    st.exception(e)
