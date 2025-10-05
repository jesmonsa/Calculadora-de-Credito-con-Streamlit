import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Crédito",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .formula-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def calcular_cuota_mensual(monto, tasa_anual, plazo_anos):
    """
    Calcula la cuota mensual usando la fórmula de amortización estándar
    """
    if tasa_anual == 0:
        return monto / (plazo_anos * 12)
    
    tasa_mensual = tasa_anual / 100 / 12
    num_pagos = plazo_anos * 12
    
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)**num_pagos) / ((1 + tasa_mensual)**num_pagos - 1)
    return cuota

def generar_tabla_amortizacion(monto, tasa_anual, plazo_anos, cuota_seguro=0):
    """
    Genera la tabla de amortización completa con cálculos precisos
    """
    cuota_mensual = calcular_cuota_mensual(monto, tasa_anual, plazo_anos)
    tasa_mensual = tasa_anual / 100 / 12
    num_pagos = plazo_anos * 12
    
    tabla = []
    saldo_pendiente = monto
    
    for mes in range(1, num_pagos + 1):
        if tasa_anual == 0:
            interes = 0
            abono_capital = cuota_mensual
        else:
            interes = saldo_pendiente * tasa_mensual
            abono_capital = cuota_mensual - interes
        
        # Para el último pago, ajustar para que el saldo sea exactamente 0
        if mes == num_pagos:
            abono_capital = saldo_pendiente
            cuota_ajustada = interes + abono_capital
        else:
            cuota_ajustada = cuota_mensual
        
        saldo_pendiente -= abono_capital
        
        # Asegurar que el saldo no sea negativo
        if saldo_pendiente < 0.01:
            saldo_pendiente = 0
        
        tabla.append({
            'Mes': mes,
            'Cuota Crédito': round(cuota_ajustada, 2),
            'Interés': round(interes, 2),
            'Abono Capital': round(abono_capital, 2),
            'Seguro': round(cuota_seguro, 2),
            'Pago Total': round(cuota_ajustada + cuota_seguro, 2),
            'Saldo Pendiente': round(saldo_pendiente, 2)
        })
    
    return pd.DataFrame(tabla)

def generar_datos_anuales(tabla_amortizacion, cuota_seguro):
    """
    Genera datos agregados por año para el gráfico de barras apiladas
    """
    # Crear una copia para no modificar la tabla original
    tabla_copia = tabla_amortizacion.copy()
    
    # Agregar columna de año
    tabla_copia['Año'] = ((tabla_copia['Mes'] - 1) // 12) + 1
    
    # Agrupar por año y sumar
    datos_anuales = tabla_copia.groupby('Año').agg({
        'Abono Capital': 'sum',
        'Interés': 'sum',
        'Seguro': 'sum'
    }).reset_index()
    
    # Renombrar columnas para mejor presentación
    datos_anuales.columns = ['Año', 'Capital', 'Intereses', 'Seguros']
    
    return datos_anuales

def generar_pdf_tabla_amortizacion(tabla_amortizacion, monto, tasa_anual, plazo_anos, cuota_seguro):
    """
    Genera un PDF con la tabla de amortización
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title = Paragraph("Tabla de Amortización", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Información del crédito
    info_text = f"""
    <b>Información del Crédito:</b><br/>
    Monto: ${monto:,.2f}<br/>
    Tasa Anual: {tasa_anual:.2f}%<br/>
    Plazo: {plazo_anos} años<br/>
    Seguro Mensual: ${cuota_seguro:,.2f}
    """
    info = Paragraph(info_text, styles['Normal'])
    story.append(info)
    story.append(Spacer(1, 12))
    
    # Preparar datos para la tabla
    data = [['Mes', 'Cuota Crédito', 'Interés', 'Abono Capital', 'Seguro', 'Pago Total', 'Saldo Pendiente']]
    
    for _, row in tabla_amortizacion.iterrows():
        data.append([
            str(int(row['Mes'])),
            f"${row['Cuota Crédito']:,.2f}",
            f"${row['Interés']:,.2f}",
            f"${row['Abono Capital']:,.2f}",
            f"${row['Seguro']:,.2f}",
            f"${row['Pago Total']:,.2f}",
            f"${row['Saldo Pendiente']:,.2f}"
        ])
    
    # Crear tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer

def obtener_parametros_credito():
    """
    Obtiene los parámetros del crédito desde el sidebar
    """
    st.sidebar.header("📝 Parámetros del Crédito")
    
    monto = st.sidebar.number_input(
        "Monto del préstamo ($)",
        min_value=1000,
        max_value=10000000,
        value=100000,
        step=1000,
        help="Ingresa el monto del préstamo (entre $1,000 y $10,000,000)"
    )
    
    tasa_anual = st.sidebar.number_input(
        "Tasa de interés anual (%)",
        min_value=0.0,
        max_value=50.0,
        value=12.0,
        step=0.1,
        help="Ingresa la tasa de interés anual (entre 0% y 50%)"
    )
    
    plazo_anos = st.sidebar.number_input(
        "Plazo en años",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        help="Ingresa el plazo del crédito (entre 1 y 30 años)"
    )
    
    cuota_seguro = st.sidebar.number_input(
        "Cuota mensual de seguro ($)",
        min_value=0,
        max_value=500,
        value=30,
        step=5,
        help="Ingresa la cuota mensual de seguro (entre $0 y $500)"
    )
    
    return monto, tasa_anual, plazo_anos, cuota_seguro

def pagina_entrada_datos_resumen():
    """
    Página de entrada de datos, resumen y gráfico
    """
    st.markdown('<h1 class="main-header">💰 Calculadora de Crédito</h1>', unsafe_allow_html=True)
    
    # Obtener parámetros
    monto, tasa_anual, plazo_anos, cuota_seguro = obtener_parametros_credito()
    
    # Información adicional
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Información")
    st.sidebar.info("""
    Esta calculadora utiliza la fórmula estándar de amortización para calcular las cuotas mensuales.
    
    Los resultados son aproximados y pueden variar según las condiciones específicas del prestamista.
    """)
    
    # Cálculos principales
    if st.sidebar.button("🔄 Calcular", type="primary"):
        # Calcular métricas principales
        cuota_mensual = calcular_cuota_mensual(monto, tasa_anual, plazo_anos)
        total_pagado = cuota_mensual * plazo_anos * 12
        intereses_pagados = total_pagado - monto
        total_seguros = cuota_seguro * plazo_anos * 12
        total_general = total_pagado + total_seguros
        
        # Generar tabla de amortización
        tabla_amortizacion = generar_tabla_amortizacion(monto, tasa_anual, plazo_anos, cuota_seguro)
        
        # Guardar en session state para usar en otras páginas
        st.session_state.tabla_amortizacion = tabla_amortizacion
        st.session_state.parametros = {
            'monto': monto,
            'tasa_anual': tasa_anual,
            'plazo_anos': plazo_anos,
            'cuota_seguro': cuota_seguro,
            'cuota_mensual': cuota_mensual,
            'total_pagado': total_pagado,
            'intereses_pagados': intereses_pagados,
            'total_seguros': total_seguros,
            'total_general': total_general
        }
        
        # Mostrar resumen compacto
        st.markdown("## 📊 Resumen del Crédito")
        
        # Métricas principales en formato compacto
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Monto", f"${monto:,.0f}")
            st.metric("📈 Tasa Anual", f"{tasa_anual:.1f}%")
        
        with col2:
            st.metric("⏱️ Plazo", f"{plazo_anos} años")
            st.metric("💵 Cuota Crédito", f"${cuota_mensual:,.0f}")
        
        with col3:
            st.metric("🛡️ Cuota Seguro", f"${cuota_seguro:,.0f}")
            st.metric("📅 Total Cuotas", f"{plazo_anos * 12}")
        
        with col4:
            st.metric("💸 Total a Pagar", f"${total_general:,.0f}")
            st.metric("📊 Intereses Totales", f"${intereses_pagados:,.0f}")
        
        # Resumen detallado en formato compacto
        st.markdown("### 📋 Detalles del Crédito")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **💰 Financiamiento:**
            - Monto del préstamo: ${monto:,.2f}
            - Tasa de interés anual: {tasa_anual:.2f}%
            - Plazo: {plazo_anos} años ({plazo_anos * 12} pagos)
            
            **💵 Pagos Mensuales:**
            - Cuota del crédito: ${cuota_mensual:,.2f}
            - Cuota de seguro: ${cuota_seguro:,.2f}
            - Total mensual: ${cuota_mensual + cuota_seguro:,.2f}
            """)
        
        with col2:
            st.markdown(f"""
            **📊 Totales:**
            - Total de cuotas: ${total_pagado:,.2f}
            - Total de seguros: ${total_seguros:,.2f}
            - Total a pagar: ${total_general:,.2f}
            - Intereses totales: ${intereses_pagados:,.2f}
            - Total de seguros: ${total_seguros:,.2f}
            """)
        
        # Gráfico de distribución anual
        st.markdown("## 📊 Distribución Anual de Pagos")
        
        # Generar datos anuales
        datos_anuales = generar_datos_anuales(tabla_amortizacion, cuota_seguro)
        
        # Crear gráfico de barras apiladas con Plotly
        fig = go.Figure()
        
        # Agregar barras para cada componente
        fig.add_trace(go.Bar(
            name='Capital',
            x=datos_anuales['Año'],
            y=datos_anuales['Capital'],
            marker_color='#1f77b4',
            hovertemplate='<b>Año %{x}</b><br>Capital: $%{y:,.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Intereses',
            x=datos_anuales['Año'],
            y=datos_anuales['Intereses'],
            marker_color='#ff7f0e',
            hovertemplate='<b>Año %{x}</b><br>Intereses: $%{y:,.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='Seguros',
            x=datos_anuales['Año'],
            y=datos_anuales['Seguros'],
            marker_color='#2ca02c',
            hovertemplate='<b>Año %{x}</b><br>Seguros: $%{y:,.2f}<extra></extra>'
        ))
        
        # Configurar el layout del gráfico
        fig.update_layout(
            title='Distribución de Pagos por Año',
            xaxis_title='Año del Crédito',
            yaxis_title='Monto ($)',
            barmode='stack',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified',
            yaxis=dict(tickformat='$,.0f')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Resumen anual compacto
        st.markdown("### 📋 Resumen por Año")
        resumen_anual = datos_anuales.copy()
        resumen_anual['Total Año'] = resumen_anual['Capital'] + resumen_anual['Intereses'] + resumen_anual['Seguros']
        resumen_anual['Capital'] = resumen_anual['Capital'].apply(lambda x: f"${x:,.0f}")
        resumen_anual['Intereses'] = resumen_anual['Intereses'].apply(lambda x: f"${x:,.0f}")
        resumen_anual['Seguros'] = resumen_anual['Seguros'].apply(lambda x: f"${x:,.0f}")
        resumen_anual['Total Año'] = resumen_anual['Total Año'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(
            resumen_anual,
            width='stretch',
            hide_index=True,
            column_config={
                "Año": st.column_config.NumberColumn("Año", help="Año del crédito"),
                "Capital": st.column_config.TextColumn("Capital", help="Capital pagado en el año"),
                "Intereses": st.column_config.TextColumn("Intereses", help="Intereses pagados en el año"),
                "Seguros": st.column_config.TextColumn("Seguros", help="Seguros pagados en el año"),
                "Total Año": st.column_config.TextColumn("Total Año", help="Total pagado en el año")
            }
        )
    
    else:
        # Mensaje inicial
        st.markdown("## 👋 ¡Bienvenido a la Calculadora de Crédito!")
        
        st.markdown("""
        Esta aplicación te permite calcular:
        
        ✅ **Cuota mensual** de tu crédito
        ✅ **Total pagado** al final del período
        ✅ **Intereses pagados** durante todo el crédito
        ✅ **Tabla de amortización completa** con desglose mes a mes
        
        ### 🚀 Cómo usar:
        1. Completa los parámetros del crédito en la barra lateral
        2. Haz clic en "Calcular" para ver los resultados
        3. Explora la tabla de amortización en la segunda página
        4. Descarga los resultados si lo necesitas
        
        ### 📊 Características:
        - Validación de rangos para todos los campos
        - Cálculos precisos usando fórmulas estándar
        - Interfaz moderna y responsive
        - Tabla de amortización organizada en pestañas para créditos largos
        - Gráficos visuales para mejor comprensión
        - Exportación de datos en formato CSV y PDF
        """)
        
        # Ejemplo de uso
        st.markdown("### 💡 Ejemplo de Uso")
        st.markdown("""
        **Prueba con estos valores:**
        - Monto: $100,000
        - Tasa: 12% anual
        - Plazo: 5 años
        - Seguro: $30/mes
        
        Esto te dará una cuota mensual de aproximadamente $2,224.44
        """)

def pagina_tabla_amortizacion():
    """
    Página de tabla de amortización con descarga PDF
    """
    st.markdown('<h1 class="main-header">📅 Tabla de Amortización</h1>', unsafe_allow_html=True)
    
    # Verificar si hay datos calculados
    if 'tabla_amortizacion' not in st.session_state or 'parametros' not in st.session_state:
        st.warning("⚠️ Primero debes calcular el crédito en la página de 'Entrada de Datos y Resumen'")
        st.info("💡 Ve a la primera página, ingresa los parámetros del crédito y haz clic en 'Calcular'")
        return
    
    # Obtener datos del session state
    tabla_amortizacion = st.session_state.tabla_amortizacion
    parametros = st.session_state.parametros
    
    # Mostrar información del crédito
    st.markdown("## 📋 Información del Crédito")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Monto", f"${parametros['monto']:,.0f}")
        st.metric("📈 Tasa Anual", f"{parametros['tasa_anual']:.1f}%")
    
    with col2:
        st.metric("⏱️ Plazo", f"{parametros['plazo_anos']} años")
        st.metric("💵 Cuota Crédito", f"${parametros['cuota_mensual']:,.0f}")
    
    with col3:
        st.metric("🛡️ Cuota Seguro", f"${parametros['cuota_seguro']:,.0f}")
        st.metric("📅 Total Cuotas", f"{parametros['plazo_anos'] * 12}")
    
    with col4:
        st.metric("💸 Total a Pagar", f"${parametros['total_general']:,.0f}")
        st.metric("📊 Intereses Totales", f"${parametros['intereses_pagados']:,.0f}")
    
    # Tabla de amortización
    st.markdown("## 📅 Tabla de Amortización Completa")
    st.markdown("Esta tabla muestra el desglose mes a mes de tu crédito, incluyendo el interés pagado, abono al capital, cuota total y saldo pendiente.")
    
    # Organizar en pestañas si el plazo es mayor a 1 año
    if parametros['plazo_anos'] > 1:
        # Dividir en períodos de 4 años
        periodos = []
        for i in range(0, parametros['plazo_anos'], 4):
            inicio = i * 12 + 1
            fin = min((i + 4) * 12, parametros['plazo_anos'] * 12)
            periodos.append((f"Años {i+1}-{min(i+4, parametros['plazo_anos'])}", inicio, fin))
        
        tabs = st.tabs([periodo[0] for periodo in periodos])
        
        for i, (nombre_periodo, inicio, fin) in enumerate(periodos):
            with tabs[i]:
                periodo_df = tabla_amortizacion[(tabla_amortizacion['Mes'] >= inicio) & (tabla_amortizacion['Mes'] <= fin)].copy()
                
                # Formatear los números para mejor visualización
                periodo_df_display = periodo_df.copy()
                periodo_df_display['Cuota Crédito'] = periodo_df_display['Cuota Crédito'].apply(lambda x: f"${x:,.2f}")
                periodo_df_display['Interés'] = periodo_df_display['Interés'].apply(lambda x: f"${x:,.2f}")
                periodo_df_display['Abono Capital'] = periodo_df_display['Abono Capital'].apply(lambda x: f"${x:,.2f}")
                periodo_df_display['Seguro'] = periodo_df_display['Seguro'].apply(lambda x: f"${x:,.2f}")
                periodo_df_display['Pago Total'] = periodo_df_display['Pago Total'].apply(lambda x: f"${x:,.2f}")
                periodo_df_display['Saldo Pendiente'] = periodo_df_display['Saldo Pendiente'].apply(lambda x: f"${x:,.2f}")
                
                st.dataframe(
                    periodo_df_display, 
                    width='stretch', 
                    hide_index=True,
                    column_config={
                        "Mes": st.column_config.NumberColumn("Mes", help="Número del mes del crédito"),
                        "Cuota Crédito": st.column_config.TextColumn("Cuota Crédito", help="Pago mensual del crédito (sin seguro)"),
                        "Interés": st.column_config.TextColumn("Interés", help="Porción de la cuota que corresponde a intereses"),
                        "Abono Capital": st.column_config.TextColumn("Abono Capital", help="Porción de la cuota que reduce el capital"),
                        "Seguro": st.column_config.TextColumn("Seguro", help="Cuota mensual de seguro"),
                        "Pago Total": st.column_config.TextColumn("Pago Total", help="Total a pagar mensualmente (crédito + seguro)"),
                        "Saldo Pendiente": st.column_config.TextColumn("Saldo Pendiente", help="Capital restante después de cada pago")
                    }
                )
                
                # Mostrar resumen del período
                st.markdown(f"**📊 Resumen del período {nombre_periodo}:**")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total Pagado", f"${periodo_df['Pago Total'].sum():,.2f}")
                with col2:
                    st.metric("Intereses", f"${periodo_df['Interés'].sum():,.2f}")
                with col3:
                    st.metric("Capital", f"${periodo_df['Abono Capital'].sum():,.2f}")
                with col4:
                    st.metric("Seguros", f"${periodo_df['Seguro'].sum():,.2f}")
                with col5:
                    st.metric("Meses", f"{len(periodo_df)}")
    else:
        # Mostrar tabla completa para créditos de 1 año o menos
        tabla_display = tabla_amortizacion.copy()
        tabla_display['Cuota Crédito'] = tabla_display['Cuota Crédito'].apply(lambda x: f"${x:,.2f}")
        tabla_display['Interés'] = tabla_display['Interés'].apply(lambda x: f"${x:,.2f}")
        tabla_display['Abono Capital'] = tabla_display['Abono Capital'].apply(lambda x: f"${x:,.2f}")
        tabla_display['Seguro'] = tabla_display['Seguro'].apply(lambda x: f"${x:,.2f}")
        tabla_display['Pago Total'] = tabla_display['Pago Total'].apply(lambda x: f"${x:,.2f}")
        tabla_display['Saldo Pendiente'] = tabla_display['Saldo Pendiente'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            tabla_display, 
            width='stretch', 
            hide_index=True,
            column_config={
                "Mes": st.column_config.NumberColumn("Mes", help="Número del mes del crédito"),
                "Cuota Crédito": st.column_config.TextColumn("Cuota Crédito", help="Pago mensual del crédito (sin seguro)"),
                "Interés": st.column_config.TextColumn("Interés", help="Porción de la cuota que corresponde a intereses"),
                "Abono Capital": st.column_config.TextColumn("Abono Capital", help="Porción de la cuota que reduce el capital"),
                "Seguro": st.column_config.TextColumn("Seguro", help="Cuota mensual de seguro"),
                "Pago Total": st.column_config.TextColumn("Pago Total", help="Total a pagar mensualmente (crédito + seguro)"),
                "Saldo Pendiente": st.column_config.TextColumn("Saldo Pendiente", help="Capital restante después de cada pago")
            }
        )
        
        # Mostrar resumen para créditos cortos
        st.markdown("**📊 Resumen del crédito:**")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Pagado", f"${tabla_amortizacion['Pago Total'].sum():,.2f}")
        with col2:
            st.metric("Intereses", f"${tabla_amortizacion['Interés'].sum():,.2f}")
        with col3:
            st.metric("Capital", f"${tabla_amortizacion['Abono Capital'].sum():,.2f}")
        with col4:
            st.metric("Seguros", f"${tabla_amortizacion['Seguro'].sum():,.2f}")
        with col5:
            st.metric("Meses", f"{len(tabla_amortizacion)}")
    
    # Botones de descarga
    st.markdown("## 💾 Exportar Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Descarga CSV
        csv = tabla_amortizacion.to_csv(index=False)
        st.download_button(
            label="📥 Descargar Tabla de Amortización (CSV)",
            data=csv,
            file_name=f"tabla_amortizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Descarga PDF
        if st.button("📄 Generar PDF", type="primary"):
            try:
                pdf_buffer = generar_pdf_tabla_amortizacion(
                    tabla_amortizacion,
                    parametros['monto'],
                    parametros['tasa_anual'],
                    parametros['plazo_anos'],
                    parametros['cuota_seguro']
                )
                
                st.download_button(
                    label="📥 Descargar Tabla de Amortización (PDF)",
                    data=pdf_buffer.getvalue(),
                    file_name=f"tabla_amortizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error al generar PDF: {str(e)}")
                st.info("💡 Asegúrate de tener instalada la librería reportlab: pip install reportlab")

def main():
    # Menú lateral para navegación
    st.sidebar.title("🧮 Calculadora de Crédito")
    st.sidebar.markdown("---")
    
    # Opciones del menú
    opcion = st.sidebar.radio(
        "📋 Navegación",
        ["📊 Entrada de Datos y Resumen", "📅 Tabla de Amortización"],
        index=0
    )
    
    # Router simple para mostrar la página correspondiente
    if opcion == "📊 Entrada de Datos y Resumen":
        pagina_entrada_datos_resumen()
    elif opcion == "📅 Tabla de Amortización":
        pagina_tabla_amortizacion()

if __name__ == "__main__":
    main()