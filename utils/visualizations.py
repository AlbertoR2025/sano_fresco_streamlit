import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

def crear_grafico_tendencia_ventas(kpis_df):
    """Gráfico de línea con tendencia de ventas diarias"""
    fig = go.Figure()
    
    if 'fecha' not in kpis_df.columns or 'ventas_totales' not in kpis_df.columns:
        fig.add_annotation(text="Datos insuficientes para gráfico", showarrow=False)
        return fig

    # Línea principal
    fig.add_trace(go.Scatter(
        x=kpis_df['fecha'],
        y=kpis_df['ventas_totales'],
        mode='lines',
        name='Ventas Diarias',
        line=dict(color='#2E86AB', width=2),
        fill='tozeroy',
        fillcolor='rgba(46, 134, 171, 0.1)'
    ))
    
    # Media móvil 7 días
    kpis_df['ma7'] = kpis_df['ventas_totales'].rolling(window=7).mean()
    fig.add_trace(go.Scatter(
        x=kpis_df['fecha'],
        y=kpis_df['ma7'],
        mode='lines',
        name='Media Móvil 7 días',
        line=dict(color='#A23B72', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Evolución de Ventas Diarias 2023',
        xaxis_title='Fecha',
        yaxis_title='Ventas ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def crear_grafico_distribucion_clientes(clientes_df):
    """Gráfico de DONUT (circular) de distribución de clientes por segmento"""
    if 'segmento' not in clientes_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Columna 'segmento' no encontrada", showarrow=False)
        return fig

    segmentos = clientes_df['segmento'].value_counts()
    
    # Colores profesionales más vibrantes
    colores_mapa = {
        'Perdido': '#06D6A0',      # Verde agua
        'En Riesgo': '#2E86AB',    # Azul
        'VIP': '#FFD166',          # Amarillo dorado
        'Recurrentes': '#EF476F',  # Rojo/rosa
        'Unica Compra': '#6C757D', # Gris
        'Bajo': '#6C757D',
        'Medio': '#FFD166',
        'Alto': '#2E86AB',
        'Premium': '#06D6A0'
    }
    
    colores_ordenados = [colores_mapa.get(seg, '#118AB2') for seg in segmentos.index]
    
    # Crear gráfico de DONUT (pie con hole)
    fig = go.Figure(data=[go.Pie(
        labels=segmentos.index,
        values=segmentos.values,
        hole=0.5,  # Esto crea el efecto donut
        marker=dict(
            colors=colores_ordenados,
            line=dict(color='white', width=3)
        ),
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(size=14, color='black'),
        hovertemplate='<b>%{label}</b><br>' +
                      'Clientes: %{value:,}<br>' +
                      'Porcentaje: %{percent}<br>' +
                      '<extra></extra>',
        pull=[0.05 if i == 0 else 0 for i in range(len(segmentos))]  # Destacar el primero
    )])
    
    # Agregar texto central
    total_clientes = segmentos.sum()
    fig.add_annotation(
        text=f"<b>{total_clientes:,}</b><br>Clientes",
        x=0.5, y=0.5,
        font=dict(size=20, color='#2E86AB', family='Arial Black'),
        showarrow=False
    )
    
    fig.update_layout(
        title={
            'text': 'Distribución de Clientes por Segmento',
            'font': {'size': 18, 'color': '#2E86AB'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=12)
        ),
        template='plotly_white',
        height=450,
        margin=dict(l=20, r=150, t=60, b=20)
    )
    
    return fig

def crear_grafico_top_productos(productos_df, metrica='ventas_totales', top_n=15):
    """Gráfico horizontal de top productos"""
    if metrica not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text=f"Columna '{metrica}' no encontrada", showarrow=False)
        return fig

    top = productos_df.nlargest(top_n, metrica)
    
    fig = px.bar(
        top,
        y='nombre_producto',
        x=metrica,
        orientation='h',
        title=f'Top {top_n} Productos por {metrica.replace("_", " ").title()}',
        color=metrica,
        color_continuous_scale='Viridis',
        text=metrica
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=500,
        xaxis_title=metrica.replace("_", " ").title(),
        yaxis_title='',
        template='plotly_white'
    )
    
    return fig

def crear_heatmap_ventas_mensual(kpis_df):
    """Heatmap de ventas por mes y día de la semana"""
    if 'fecha' not in kpis_df.columns or 'ventas_totales' not in kpis_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes para heatmap", showarrow=False)
        return fig

    kpis_df = kpis_df.copy()
    kpis_df['mes'] = kpis_df['fecha'].dt.month
    kpis_df['dia_semana'] = kpis_df['fecha'].dt.day_name()
    
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    pivot = kpis_df.pivot_table(
        values='ventas_totales',
        index='dia_semana',
        columns='mes',
        aggfunc='mean'
    )
    
    pivot = pivot.reindex(dias_orden)
    pivot.index = dias_espanol
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Blues',
        text=pivot.values,
        texttemplate='$%{text:,.0f}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title='Promedio de Ventas por Día de la Semana y Mes',
        xaxis_title='Mes',
        yaxis_title='Día de la Semana',
        height=400,
        template='plotly_white'
    )
    
    return fig

def crear_gauge_chart(valor, valor_objetivo, titulo):
    """Gráfico de gauge para mostrar progreso vs objetivo"""
    porcentaje = (valor / valor_objetivo) * 100 if valor_objetivo != 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': titulo, 'font': {'size': 20}},
        delta={'reference': valor_objetivo, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, valor_objetivo * 1.2], 'tickformat': '$,.0f'},
            'bar': {'color': "#2E86AB"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, valor_objetivo * 0.5], 'color': '#EF476F'},
                {'range': [valor_objetivo * 0.5, valor_objetivo * 0.75], 'color': '#FFD166'},
                {'range': [valor_objetivo * 0.75, valor_objetivo], 'color': '#06D6A0'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': valor_objetivo
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig

# ========== NUEVAS VISUALIZACIONES IMPACTANTES ==========

def crear_mapa_correlaciones(kpis_df):
    """Mapa de calor de correlaciones entre métricas"""
    cols_numericas = [
        'ventas_totales', 'pedidos_unicos', 'ticket_promedio',
        'productos_por_pedido', 'clientes_unicos'
    ]
    
    # Filtrar solo columnas existentes
    cols_disponibles = [col for col in cols_numericas if col in kpis_df.columns]
    
    if len(cols_disponibles) < 2:
        fig = go.Figure()
        fig.add_annotation(text="No hay suficientes métricas para correlación", showarrow=False)
        return fig
    
    corr_matrix = kpis_df[cols_disponibles].corr()
    
    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=list(corr_matrix.columns),
        y=list(corr_matrix.index),
        annotation_text=corr_matrix.round(2).values,
        colorscale='RdBu',
        showscale=True,
        zmid=0
    )
    
    fig.update_layout(
        title='🔗 Correlación entre Métricas de Negocio',
        height=500,
        template='plotly_white',
        xaxis={'side': 'bottom'}
    )
    
    return fig

def crear_waterfall_contribucion(productos_df, top_n=10):
    """Gráfico de cascada mostrando contribución de productos"""
    if 'ventas_totales' not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes", showarrow=False)
        return fig
    
    top = productos_df.nlargest(top_n, 'ventas_totales')
    otros_ventas = productos_df.nsmallest(len(productos_df) - top_n, 'ventas_totales')['ventas_totales'].sum()
    
    productos_list = list(top['nombre_producto']) + ['Otros']
    valores = list(top['ventas_totales']) + [otros_ventas]
    
    fig = go.Figure(go.Waterfall(
        name="Contribución",
        orientation="v",
        measure=["relative"] * len(productos_list),
        x=productos_list,
        y=valores,
        text=[f"${v:,.0f}" for v in valores],
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#EF476F"}},
        increasing={"marker": {"color": "#06D6A0"}},
        totals={"marker": {"color": "#2E86AB"}}
    ))
    
    fig.update_layout(
        title=f"💰 Contribución de Top {top_n} Productos a Ventas Totales",
        showlegend=False,
        height=500,
        template='plotly_white',
        xaxis_tickangle=-45
    )
    
    return fig

def crear_sankey_segmentos(clientes_df):
    """Diagrama Sankey del flujo de valor por segmento"""
    if 'segmento' not in clientes_df.columns or 'gasto_total' not in clientes_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes para Sankey", showarrow=False)
        return fig
    
    segmentos = clientes_df.groupby('segmento').agg({
        'gasto_total': 'sum',
        'id_cliente': 'count'
    }).reset_index()
    
    segmentos = segmentos.sort_values('gasto_total', ascending=False)
    
    # Crear nodos
    source = list(range(len(segmentos)))
    target = [len(segmentos)] * len(segmentos)
    value = list(segmentos['gasto_total'])
    labels = list(segmentos['segmento']) + ['Total Ingresos']
    
    colors = ['#06D6A0', '#118AB2', '#FFD166', '#EF476F', '#6C757D', '#2E86AB']
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=colors[:len(labels)]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(46, 134, 171, 0.3)'
        )
    )])
    
    fig.update_layout(
        title="🌊 Flujo de Ingresos por Segmento de Clientes",
        font=dict(size=12),
        height=400
    )
    
    return fig

def crear_treemap_productos(productos_df):
    """Treemap jerárquico de productos por ventas"""
    if 'ventas_totales' not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes", showarrow=False)
        return fig
    
    # Agregar categoría artificial para jerarquía
    productos_df = productos_df.copy()
    productos_df['categoria'] = 'Productos'
    
    fig = px.treemap(
        productos_df,
        path=['categoria', 'nombre_producto'],
        values='ventas_totales',
        color='ventas_totales',
        color_continuous_scale='Viridis',
        title='🗺️ Mapa de Calor: Ventas por Producto'
    )
    
    fig.update_traces(textposition="middle center", textfont_size=12)
    fig.update_layout(height=600)
    
    return fig

def crear_grafico_pareto(productos_df):
    """Gráfico de Pareto (80/20) para productos"""
    if 'ventas_totales' not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes", showarrow=False)
        return fig
    
    # Ordenar y calcular acumulado
    df_sorted = productos_df.sort_values('ventas_totales', ascending=False).reset_index(drop=True)
    df_sorted['ventas_acumuladas'] = df_sorted['ventas_totales'].cumsum()
    df_sorted['porcentaje_acumulado'] = (df_sorted['ventas_acumuladas'] / df_sorted['ventas_totales'].sum()) * 100
    
    # Crear figura con doble eje
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barras de ventas
    fig.add_trace(
        go.Bar(
            x=df_sorted['nombre_producto'],
            y=df_sorted['ventas_totales'],
            name="Ventas",
            marker_color='#2E86AB'
        ),
        secondary_y=False
    )
    
    # Línea acumulada
    fig.add_trace(
        go.Scatter(
            x=df_sorted['nombre_producto'],
            y=df_sorted['porcentaje_acumulado'],
            name="% Acumulado",
            line=dict(color='#EF476F', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    # Línea del 80%
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="green",
        annotation_text="Regla 80/20",
        secondary_y=True
    )
    
    fig.update_layout(
        title="📊 Análisis de Pareto: ¿Qué productos generan el 80% de ventas?",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        xaxis_tickangle=-45
    )
    
    fig.update_yaxes(title_text="Ventas ($)", secondary_y=False)
    fig.update_yaxes(title_text="% Acumulado", secondary_y=True, range=[0, 105])
    
    return fig

def crear_grafico_velocimetro_multiple(metricas, objetivos):
    """Panel de velocímetros compacto CORREGIDO"""
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=('💰 Ventas', '🛒 Pedidos', '👥 Clientes')
    )
    
    configs = [
        ('ventas_totales', objetivos.get('ventas', 5000000), '$', 1, 1),
        ('pedidos_totales', objetivos.get('pedidos', 2500000), '', 1, 2),
        ('clientes_unicos', objetivos.get('clientes', 150000), '', 1, 3)
    ]
    
    colores = ['#2E86AB', '#06D6A0', '#118AB2']
    
    for i, (metrica, objetivo, prefijo, row, col) in enumerate(configs):
        valor = metricas.get(metrica, 0)
        porcentaje = (valor / objetivo * 100) if objetivo > 0 else 0
        
        # Formatear valores para mostrar de manera legible
        if valor >= 1000000:
            valor_formateado = f"{valor/1000000:.1f}M"
        elif valor >= 1000:
            valor_formateado = f"{valor/1000:.0f}K"
        else:
            valor_formateado = f"{valor:.0f}"
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=valor,
                number={
                    'prefix': prefijo,
                    'valueformat': ',.0f',
                    'font': {'size': 20}
                },
                delta={
                    'reference': objetivo,
                    'relative': False,
                    'valueformat': ',.0f',
                    'increasing': {'color': "#06D6A0"},
                    'decreasing': {'color': "#EF476F"},
                    'font': {'size': 14}
                },
                title={
                    'text': f"{porcentaje:.1f}%<br>Objetivo",
                    'font': {'size': 12}
                },
                gauge={
                    'axis': {
                        'range': [None, objetivo * 1.2],
                        'tickformat': ',.0f',
                        'tickfont': {'size': 10}
                    },
                    'bar': {'color': colores[i], 'thickness': 0.8},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, objetivo * 0.6], 'color': '#EF476F'},
                        {'range': [objetivo * 0.6, objetivo * 0.8], 'color': '#FFD166'},
                        {'range': [objetivo * 0.8, objetivo], 'color': '#06D6A0'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.8,
                        'value': objetivo
                    }
                }
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        height=300,
        template='plotly_white',
        font={'family': "Arial, sans-serif"},
        margin=dict(l=50, r=50, t=80, b=50),
        title_text="🎯 Progreso vs Objetivos Anuales",
        title_x=0.5
    )
    
    return fig

def crear_analisis_estacionalidad(kpis_df):
    """Análisis de patrones estacionales"""
    if 'fecha' not in kpis_df.columns or 'ventas_totales' not in kpis_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes para análisis de estacionalidad", showarrow=False)
        return fig
        
    kpis_df = kpis_df.copy()
    kpis_df['mes'] = kpis_df['fecha'].dt.month
    kpis_df['dia_semana'] = kpis_df['fecha'].dt.dayofweek
    kpis_df['semana_año'] = kpis_df['fecha'].dt.isocalendar().week
    
    # Agrupar por diferentes periodos
    mensual = kpis_df.groupby('mes')['ventas_totales'].mean()
    semanal = kpis_df.groupby('dia_semana')['ventas_totales'].mean()
    
    # Nombres de meses y días
    nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    nombres_dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('📅 Patrón Mensual', '📆 Patrón Semanal'),
        horizontal_spacing=0.1
    )
    
    # Gráfico mensual
    fig.add_trace(
        go.Bar(
            x=[nombres_meses[i-1] for i in mensual.index], 
            y=mensual.values, 
            name='Mensual', 
            marker_color='#2E86AB',
            text=[f'${v:,.0f}' for v in mensual.values],
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # Gráfico semanal
    fig.add_trace(
        go.Bar(
            x=[nombres_dias[i] for i in semanal.index], 
            y=semanal.values, 
            name='Semanal', 
            marker_color='#06D6A0',
            text=[f'${v:,.0f}' for v in semanal.values],
            textposition='auto'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Mes", row=1, col=1)
    fig.update_xaxes(title_text="Día de la Semana", row=1, col=2)
    fig.update_yaxes(title_text="Ventas Promedio ($)", row=1, col=1)
    fig.update_yaxes(title_text="Ventas Promedio ($)", row=1, col=2)
    
    fig.update_layout(
        height=400, 
        showlegend=False, 
        template='plotly_white',
        title_text="Análisis de Estacionalidad - Patrones de Ventas"
    )
    return fig
