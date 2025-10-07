import pandas as pd
import numpy as np

def calcular_metricas_globales(kpis_df):
    """Calcula métricas agregadas del negocio"""
    # Usar nombres exactos del CSV
    ventas_totales = kpis_df.get('ventas_totales', pd.Series([0])).sum()
    pedidos_totales = kpis_df.get('pedidos_unicos', pd.Series([0])).sum()
    ticket_promedio = kpis_df.get('ticket_promedio', pd.Series([0])).mean()
    items_promedio = kpis_df.get('productos_por_pedido', pd.Series([0])).mean()
    clientes_unicos = kpis_df.get('clientes_unicos', pd.Series([0])).sum()

    return {
        'ventas_totales': ventas_totales,
        'pedidos_totales': pedidos_totales,
        'ticket_promedio': ticket_promedio,
        'items_promedio': items_promedio,
        'clientes_unicos': clientes_unicos,
        'dias_operacion': len(kpis_df)
    }

def calcular_crecimiento(kpis_df, metrica='ventas_totales'):
    """Calcula crecimiento mes a mes"""
    kpis_df['mes'] = kpis_df['fecha'].dt.to_period('M')
    mensual = kpis_df.groupby('mes')[metrica].sum()
    crecimiento = mensual.pct_change() * 100
    return mensual, crecimiento

def segmentar_clientes_valor(clientes_df):
    """Segmenta clientes por valor (percentiles) usando 'gasto_total'"""
    clientes_df['segmento'] = pd.qcut(
        clientes_df['gasto_total'], 
        q=4, 
        labels=['Bajo', 'Medio', 'Alto', 'Premium'],
        duplicates='drop'  # Maneja duplicados si hay
    )
    return clientes_df

def identificar_productos_estrella(productos_df, top_n=10):
    """Identifica productos top por múltiples métricas usando nombres del CSV"""
    top_ventas = productos_df.nlargest(top_n, 'ventas_totales')
    top_frecuencia = productos_df.nlargest(top_n, 'pedidos_unicos')  # Proxy de frecuencia
    top_ticket = productos_df.nlargest(top_n, 'precio_promedio')  # Proxy de ticket
    
    return {
        'top_ventas': top_ventas,
        'top_frecuencia': top_frecuencia,
        'top_ticket': top_ticket
    }