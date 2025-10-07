import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def crear_grafico_tendencia_ventas(kpis_df):
    """Gráfico de línea con tendencia de ventas diarias"""
    fig = go.Figure()
    
    # Verificar columnas
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
    """Gráfico de distribución de clientes por segmento usando 'segmento'"""
    if 'segmento' not in clientes_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Columna 'segmento' no encontrada", showarrow=False)
        return fig

    segmentos = clientes_df['segmento'].value_counts()
    
    colores = {
        'VIP': '#06D6A0',
        'Recurrentes': '#118AB2',
        'En Riesgo': '#FFD166',
        'Perdido': '#EF476F',
        'Bajo': '#6C757D',  # Ajustado para segmentos del CSV
        'Medio': '#FFD166',
        'Alto': '#118AB2',
        'Premium': '#06D6A0'
    }
    
    fig = go.Figure(data=[go.Bar(
        x=segmentos.index,
        y=segmentos.values,
        marker_color=[colores.get(seg, '#6C757D') for seg in segmentos.index],
        text=segmentos.values,
        textposition='auto',
    )])
    
    fig.update_layout(
        title='Distribución de Clientes por Segmento',
        xaxis_title='Segmento',
        yaxis_title='Cantidad de Clientes',
        template='plotly_white',
        height=400
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

    kpis_df['mes'] = kpis_df['fecha'].dt.month
    kpis_df['dia_semana'] = kpis_df['fecha'].dt.day_name()
    
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    pivot = kpis_df.pivot_table(
        values='ventas_totales',
        index='dia_semana',
        columns='mes',
        aggfunc='mean'
    )
    
    pivot = pivot.reindex(dias_orden)
    
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