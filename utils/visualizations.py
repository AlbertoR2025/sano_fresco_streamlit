import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from scipy import stats

def crear_grafico_tendencia_ventas(kpis_df):
    """Gráfico de Tendencias SIMPLIFICADO - Claro y Legible"""
    from plotly.subplots import make_subplots
    import numpy as np
    from scipy import stats
    
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles=['📈 Evolución de Ventas con Tendencia'],
        specs=[[{"secondary_y": False}]]
    )
    
    if 'fecha' not in kpis_df.columns or 'ventas_totales' not in kpis_df.columns:
        fig.add_annotation(text="Datos insuficientes para gráfico", showarrow=False)
        return fig

    # Preparar datos
    df_clean = kpis_df.dropna(subset=['fecha', 'ventas_totales'])
    df_clean = df_clean.sort_values('fecha')
    
    # Convertir fechas a números para regresión
    df_clean['fecha_num'] = (df_clean['fecha'] - df_clean['fecha'].min()).dt.days
    
    # === SOLO VENTAS PRINCIPALES ===
    
    # Ventas con área (más suave)
    fig.add_trace(
        go.Scatter(
            x=df_clean['fecha'],
            y=df_clean['ventas_totales'],
            mode='lines',
            name='💰 Ventas Diarias',
            line=dict(color='#059669', width=3),
            fill='tozeroy',
            fillcolor='rgba(5, 150, 105, 0.15)',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Ventas: <b>$%{y:,.0f}</b><extra></extra>'
        ),
        row=1, col=1
    )
    
    # Media móvil 7 días (más suave)
    df_clean['ma7_ventas'] = df_clean['ventas_totales'].rolling(window=7, min_periods=1).mean()
    fig.add_trace(
        go.Scatter(
            x=df_clean['fecha'],
            y=df_clean['ma7_ventas'],
            mode='lines',
            name='📈 Tendencia (7 días)',
            line=dict(color='#dc2626', width=3, dash='solid'),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Tendencia: <b>$%{y:,.0f}</b><extra></extra>'
        ),
        row=1, col=1
    )
    
    # === ANÁLISIS ESTADÍSTICO SIMPLE ===
    
    # Calcular estadísticas básicas
    if len(df_clean) > 1:
        slope_ventas, intercept_ventas, r_value_ventas, p_value_ventas, std_err_ventas = stats.linregress(
            df_clean['fecha_num'], df_clean['ventas_totales']
        )
        
        # Calcular crecimiento porcentual
        crecimiento_diario = slope_ventas / df_clean['ventas_totales'].mean() * 100
        crecimiento_anual = crecimiento_diario * 365
        
        # Agregar estadísticas en una caja limpia
        fig.add_annotation(
            x=0.98, y=0.98,
            xref='paper', yref='paper',
            text=f'<b>📊 Estadísticas</b><br>' +
                 f'Crecimiento Diario: <b>{crecimiento_diario:+.2f}%</b><br>' +
                 f'Crecimiento Anual: <b>{crecimiento_anual:+.1f}%</b><br>' +
                 f'Tendencia: <b>{"📈" if crecimiento_diario > 0 else "📉"}</b>',
            showarrow=False,
            font=dict(size=14, color='#0891b2'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#0891b2',
            borderwidth=2,
            align='right'
        )
    
    # === CONFIGURACIÓN SIMPLE Y LIMPIA ===
    
    fig.update_layout(
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
        )
    )
    
    # Configurar ejes más limpios
    fig.update_xaxes(
        title_text="Fecha",
        tickfont=dict(size=12),
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True
    )
    fig.update_yaxes(
        title_text="Ventas ($)",
        tickfont=dict(size=12),
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True
    )
    
    return fig

def crear_grafico_distribucion_clientes(clientes_df):
    """Gráfico de DONUT (circular) de distribución de clientes por segmento"""
    if 'segmento' not in clientes_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Columna 'segmento' no encontrada", showarrow=False)
        return fig

    segmentos = clientes_df['segmento'].value_counts()
    
    # Colores exactos como en la imagen de muestra
    colores_mapa = {
        'Perdido': '#06D6A0',      # Verde agua
        'En Riesgo': '#2E86AB',    # Azul
        'VIP': '#FFD166',          # Amarillo dorado
        'Recurrentes': '#EF476F',  # Rojo/rosa
        'Unica Compra': '#6C757D', # Gris
        'Bajo': '#545B62',        # Gris oscuro como en la imagen
        'Medio': '#FFD166',        # Amarillo como en la imagen
        'Alto': '#118AB2',         # Azul turquesa como en la imagen
        'Premium': '#06D6A0'       # Verde turquesa como en la imagen
    }
    
    colores_ordenados = [colores_mapa.get(seg, '#118AB2') for seg in segmentos.index]
    
    # Crear gráfico DONUT PREMIUM con efecto mejorado
    fig = go.Figure(data=[go.Pie(
        labels=segmentos.index,
        values=segmentos.values,
        marker=dict(
            colors=colores_ordenados,
            line=dict(color='white', width=3)
        ),
        pull=[0.05 if i == 0 else 0 for i in range(len(segmentos))]  # Destacar el primero
    )])
    
    # Aplicar configuración donut premium
    fig.update_traces(
        hole=0.45,
        hoverinfo="label+percent+value",
        textinfo="percent",
        textposition="inside",
        textfont=dict(size=15, color="white")
    )
    
    # Layout premium con texto centrado y fondo transparente
    total_clientes = segmentos.sum()
    fig.update_layout(
        annotations=[dict(text=f'{total_clientes:,}<br>Clientes', x=0.5, y=0.5, font_size=16, showarrow=False, font_color='#2C3E50')],
        title=dict(
            text="Distribución de Clientes por Segmento",
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#2C3E50')
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.2,
            x=0.5,
            xanchor='center',
            bgcolor='rgba(255,255,255,0.7)',
            bordercolor='#A9D9E8',
            borderwidth=1,
            font=dict(color='#333333')
        ),
        template="plotly",
        height=420,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif")
    )
    
    return fig

def crear_grafico_top_productos(productos_df, metrica='ventas_totales', top_n=15):
    """Gráfico horizontal de top productos"""
    if metrica not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text=f"Columna '{metrica}' no encontrada", showarrow=False)
        return fig

    # Los datos ya vienen ordenados desde app.py
    fig = go.Figure(data=[
        go.Bar(
            y=productos_df['nombre_producto'],
            x=productos_df[metrica],
            orientation='h',
            text=productos_df[metrica],
            texttemplate='%{text:,.0f}',
            textposition='outside',
            marker=dict(
                color=productos_df[metrica],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=metrica.replace("_", " ").title())
            )
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Productos por {metrica.replace("_", " ").title()}',
        xaxis_title=metrica.replace("_", " ").title(),
        yaxis_title='',
        height=500,
        template='plotly_white',
        showlegend=False,
        yaxis={'categoryorder':'total descending'}
    )
    
    return fig

def crear_heatmap_ventas_mensual(kpis_df):
    """Heatmap MEJORADO - Colores del tema y mejor legibilidad"""
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
    
    # Crear heatmap con colores del tema y mejor contraste
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[
            [0.0, '#0891b2'],      # Turquesa (color base más oscuro)
            [0.3, '#06D6A0'],      # Verde turquesa
            [0.6, '#059669'],      # Verde
            [0.8, '#047857'],      # Verde oscuro
            [1.0, '#065f46']       # Verde muy oscuro
        ],
        text=pivot.values,
        texttemplate='<b>$%{text:,.0f}</b>',
        textfont={"size": 14, "color": "white"},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> - <b>Mes %{x}</b><br>' +
                     'Ventas Promedio: <b>$%{z:,.0f}</b><br>' +
                     '<extra></extra>'
    ))
    
    # Agregar sombra al texto para mejor legibilidad
    fig.update_traces(
        textfont=dict(
            size=14,
            color="white",
            family="Arial Black"  # Fuente más gruesa para mejor contraste
        )
    )
    
    # Actualizar layout sin título redundante
    fig.update_layout(
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=60, r=60, t=40, b=60),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(
                text="Mes",
                font=dict(size=14, color='#0891b2')
            ),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text="Día de la Semana",
                font=dict(size=14, color='#0891b2')
            ),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        )
    )
    
    # Mejorar la barra de colores
    fig.update_layout(
        coloraxis=dict(
            colorbar=dict(
                title=dict(
                    text='Ventas ($)',
                    font=dict(size=14, color='#0891b2')
                ),
                tickfont=dict(size=12),
                len=0.8,
                y=0.5,
                yanchor='middle'
            )
        )
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
    """Mapa de calor de correlaciones MEJORADO - Elegante y Profesional"""
    cols_numericas = [
        'ventas_totales', 'pedidos_totales', 'ticket_promedio',
        'productos_por_pedido', 'clientes_unicos'
    ]
    
    # Filtrar solo columnas existentes
    cols_disponibles = [col for col in cols_numericas if col in kpis_df.columns]
    
    if len(cols_disponibles) < 2:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay suficientes métricas para correlación", 
            showarrow=False,
            font=dict(size=16, color='#6c757d')
        )
        return fig
    
    # Calcular matriz de correlación
    corr_matrix = kpis_df[cols_disponibles].corr()
    
    # Crear nombres más legibles
    nombres_legibles = {
        'ventas_totales': '💰 Ventas',
        'pedidos_totales': '🛒 Pedidos', 
        'ticket_promedio': '🎫 Ticket Promedio',
        'productos_por_pedido': '📦 Productos/Pedido',
        'clientes_unicos': '👥 Clientes'
    }
    
    # Renombrar columnas para mostrar
    corr_display = corr_matrix.copy()
    corr_display.columns = [nombres_legibles.get(col, col) for col in corr_display.columns]
    corr_display.index = [nombres_legibles.get(col, col) for col in corr_display.index]
    
    # Crear heatmap con go.Heatmap para mejor control
    fig = go.Figure(data=go.Heatmap(
        z=corr_display.values,
        x=corr_display.columns,
        y=corr_display.index,
        colorscale=[
            [0.0, '#dc2626'],    # Rojo para correlación negativa fuerte
            [0.25, '#f87171'],   # Rojo claro
            [0.5, '#f8f9fa'],    # Blanco para correlación cero
            [0.75, '#60a5fa'],   # Azul claro
            [1.0, '#2563eb']     # Azul para correlación positiva fuerte
        ],
        zmin=-1,
        zmax=1,
        text=corr_display.round(2).values,
        texttemplate='%{text}',
        textfont={'size': 14, 'color': 'white'},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>' +
                     'Correlación: <b>%{z:.3f}</b><br>' +
                     '<extra></extra>'
    ))
    
    # Actualizar layout con estilo profesional
    fig.update_layout(
        height=600,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=100, r=50, t=100, b=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            side='bottom',
            tickfont=dict(size=12),
            tickangle=45
        ),
        yaxis=dict(
            side='left',
            tickfont=dict(size=12)
        )
    )
    
    # Agregar barra de colores personalizada
    fig.update_layout(
        coloraxis=dict(
            colorbar=dict(
                title=dict(
                    text='Correlación',
                    font=dict(size=14, color='#0891b2')
                ),
                tickfont=dict(size=12),
                len=0.8,
                y=0.5,
                yanchor='middle'
            )
        )
    )
    
    return fig

def crear_waterfall_contribucion(productos_df, top_n=10):
    """Gráfico de cascada MEJORADO - Colores del tema y sin título redundante"""
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
        text=[f"<b>${v:,.0f}</b>" for v in valores],
        textposition="outside",
        textfont=dict(size=12, color='#0891b2'),
        connector={"line": {"color": "#0891b2", "width": 2}},
        decreasing={"marker": {"color": "#dc2626"}},  # Rojo del tema
        increasing={"marker": {"color": "#06D6A0"}},   # Verde turquesa del tema
        totals={"marker": {"color": "#0891b2"}}        # Turquesa del tema
    ))
    
    fig.update_layout(
        showlegend=False,
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=60, r=60, t=40, b=60),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text='Ventas ($)',
                font=dict(size=14, color='#0891b2')
            ),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        )
    )
    
    return fig

def crear_sankey_segmentos(clientes_df):
    """Diagrama Sankey del flujo de valor por segmento"""
    if 'segmento' not in clientes_df.columns or 'gasto_total' not in clientes_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes para Sankey", showarrow=False)
        return fig
    
    segmentos = clientes_df.groupby('segmento', observed=True).agg({
        'gasto_total': 'sum',
        'id_cliente': 'count'
    }).reset_index()
    
    segmentos = segmentos.sort_values('gasto_total', ascending=False)
    
    # Crear nodos
    source = list(range(len(segmentos)))
    target = [len(segmentos)] * len(segmentos)
    value = list(segmentos['gasto_total'])
    labels = list(segmentos['segmento']) + ['Total Ingresos']
    
    colors = ['#059669', '#2563eb', '#7c3aed', '#d97706', '#dc2626', '#0891b2']
    
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
        height=500,
        font=dict(size=14, family='Arial, sans-serif'),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def crear_treemap_productos(productos_df):
    """Treemap jerárquico MEJORADO - Colores del tema y sin título redundante"""
    if 'ventas_totales' not in productos_df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Datos insuficientes", showarrow=False)
        return fig
    
    # Agregar categoría artificial para jerarquía
    productos_df = productos_df.copy()
    productos_df['categoria'] = 'Productos'
    
    # Crear treemap con colores del tema
    fig = px.treemap(
        productos_df,
        path=['categoria', 'nombre_producto'],
        values='ventas_totales',
        color='ventas_totales',
        color_continuous_scale=[
            [0.0, '#dc2626'],      # Rojo para valores bajos
            [0.2, '#d97706'],      # Naranja
            [0.4, '#059669'],       # Verde
            [0.6, '#0891b2'],       # Turquesa
            [0.8, '#2563eb'],       # Azul
            [1.0, '#7c3aed']        # Morado para valores altos
        ],
        hover_data={'ventas_totales': ':$,.0f'},
        hover_name='nombre_producto'
    )
    
    # Mejorar el texto y la interactividad
    fig.update_traces(
        textposition="middle center", 
        textfont_size=12,
        textfont_color='white',
        hovertemplate='<b>%{label}</b><br>' +
                     'Ventas: <b>$%{value:,.0f}</b><br>' +
                     'Porcentaje: <b>%{percentParent:.1%}</b><extra></extra>'
    )
    
    # Actualizar layout con título claro
    fig.update_layout(
        title=dict(
            text='🗺️ Mapa de Ventas por Producto',
            font=dict(size=18, color='#0891b2'),
            x=0.5
        ),
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Mejorar la barra de colores
    fig.update_layout(
        coloraxis=dict(
            colorbar=dict(
                title=dict(
                    text='Ventas ($)',
                    font=dict(size=14, color='#0891b2')
                ),
                tickfont=dict(size=12),
                len=0.8,
                y=0.5,
                yanchor='middle'
            )
        )
    )
    
    return fig

def crear_grafico_pareto(productos_df):
    """Gráfico de Pareto MEJORADO - Colores del tema y sin título redundante"""
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
    
    # Barras de ventas con colores del tema
    fig.add_trace(
        go.Bar(
            x=df_sorted['nombre_producto'],
            y=df_sorted['ventas_totales'],
            name="Ventas",
            marker_color='#0891b2',  # Turquesa del tema
            marker_line=dict(color='#047857', width=1),
            text=df_sorted['ventas_totales'],
            texttemplate='<b>$%{text:,.0f}</b>',
            textposition='outside',
            textfont=dict(size=10, color='#0891b2')
        ),
        secondary_y=False
    )
    
    # Línea acumulada con colores del tema
    fig.add_trace(
        go.Scatter(
            x=df_sorted['nombre_producto'],
            y=df_sorted['porcentaje_acumulado'],
            name="% Acumulado",
            line=dict(color='#dc2626', width=3),  # Rojo del tema
            mode='lines+markers',
            marker=dict(size=8, color='#dc2626')
        ),
        secondary_y=True
    )
    
    # Línea del 80% con color del tema
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="#059669",  # Verde del tema
        line_width=2,
        annotation_text="Regla 80/20",
        annotation_font=dict(size=12, color='#059669'),
        secondary_y=True
    )
    
    fig.update_layout(
        hovermode='x unified',
        height=500,
        font=dict(size=12, family='Arial, sans-serif'),
        margin=dict(l=60, r=60, t=40, b=60),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        )
    )
    
    fig.update_yaxes(
        title=dict(
            text="Ventas ($)",
            font=dict(size=14, color='#0891b2')
        ), 
        secondary_y=False,
        tickfont=dict(size=12),
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True
    )
    fig.update_yaxes(
        title=dict(
            text="% Acumulado",
            font=dict(size=14, color='#dc2626')
        ), 
        secondary_y=True, 
        range=[0, 105],
        tickfont=dict(size=12),
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True
    )
    
    return fig

def crear_grafico_progreso_objetivos(metricas, objetivos):
    """Gráfico de Gauges Circulares - ELEGANTE Y NÍTIDO"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # Calcular porcentajes
    porcentajes = {
        'Ventas': (metricas['ventas_totales'] / objetivos['ventas']) * 100,
        'Pedidos': (metricas['pedidos_totales'] / objetivos['pedidos']) * 100,
        'Clientes': (metricas['clientes_unicos'] / objetivos['clientes']) * 100
    }
    
    # Valores actuales
    valores_actuales = {
        'Ventas': metricas['ventas_totales'],
        'Pedidos': metricas['pedidos_totales'],
        'Clientes': metricas['clientes_unicos']
    }
    
    # Objetivos
    valores_objetivos = {
        'Ventas': objetivos['ventas'],
        'Pedidos': objetivos['pedidos'],
        'Clientes': objetivos['clientes']
    }
    
    # Crear subplots con gauges
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=['💰 Ventas Totales', '🛒 Pedidos Totales', '👥 Clientes Únicos']
    )
    
    # Configuración de cada gauge
    configs = [
        {
            'metrica': 'Ventas',
            'valor': valores_actuales['Ventas'],
            'objetivo': valores_objetivos['Ventas'],
            'porcentaje': porcentajes['Ventas'],
            'color': '#059669',
            'suffix': '$',
            'row': 1,
            'col': 1
        },
        {
            'metrica': 'Pedidos',
            'valor': valores_actuales['Pedidos'],
            'objetivo': valores_objetivos['Pedidos'],
            'porcentaje': porcentajes['Pedidos'],
            'color': '#2563eb',
            'suffix': '',
            'row': 1,
            'col': 2
        },
        {
            'metrica': 'Clientes',
            'valor': valores_actuales['Clientes'],
            'objetivo': valores_objetivos['Clientes'],
            'porcentaje': porcentajes['Clientes'],
            'color': '#7c3aed',
            'suffix': '',
            'row': 1,
            'col': 3
        }
    ]
    
    # Crear cada gauge
    for config in configs:
        # Formatear valor para mostrar
        if config['valor'] >= 1000000:
            valor_formateado = f"{config['valor']/1000000:.1f}M"
        elif config['valor'] >= 1000:
            valor_formateado = f"{config['valor']/1000:.0f}K"
        else:
            valor_formateado = f"{config['valor']:.0f}"
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=config['valor'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={
                    'text': f"<b>{config['metrica']}</b><br><span style='font-size:16px'>{config['porcentaje']:.1f}% del Objetivo</span>",
                    'font': {'size': 18, 'color': config['color']}
                },
                delta={
                    'reference': config['objetivo'],
                    'relative': False,
                    'valueformat': ',.0f',
                    'increasing': {'color': "#06D6A0"},
                    'decreasing': {'color': "#EF476F"},
                    'font': {'size': 16}
                },
                number={
                    'prefix': config['suffix'],
                    'valueformat': ',.0f',
                    'font': {'size': 24, 'color': config['color']}
                },
                gauge={
                    'axis': {
                        'range': [None, config['objetivo'] * 1.2],
                        'tickformat': ',.0f',
                        'tickfont': {'size': 12},
                        'tickcolor': config['color']
                    },
                    'bar': {
                        'color': config['color'],
                        'thickness': 0.8
                    },
                    'bgcolor': "white",
                    'borderwidth': 3,
                    'bordercolor': config['color'],
                    'steps': [
                        {'range': [0, config['objetivo'] * 0.5], 'color': '#f8f9fa'},
                        {'range': [config['objetivo'] * 0.5, config['objetivo'] * 0.8], 'color': '#e9ecef'},
                        {'range': [config['objetivo'] * 0.8, config['objetivo']], 'color': '#dee2e6'}
                    ],
                    'threshold': {
                        'line': {'color': "#dc2626", 'width': 4},
                        'thickness': 0.8,
                        'value': config['objetivo']
                    }
                }
            ),
            row=config['row'], col=config['col']
        )
    
    # Actualizar layout
    fig.update_layout(
        height=500,
        font={'family': "Arial, sans-serif"},
        margin=dict(l=50, r=50, t=100, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
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
    mensual = kpis_df.groupby('mes', observed=True)['ventas_totales'].mean()
    semanal = kpis_df.groupby('dia_semana', observed=True)['ventas_totales'].mean()
    
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
