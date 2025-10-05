# 🧮 Calculadora de Crédito con Streamlit

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Una aplicación web interactiva y profesional para calcular cuotas de crédito, generar tablas de amortización detalladas y analizar pagos financieros con visualizaciones avanzadas.

## ✨ Características Principales

- 🧮 **Cálculo preciso** de cuotas mensuales usando fórmulas estándar de amortización
- 📊 **Tabla de amortización completa** con desglose mes a mes
- 📈 **Gráficos interactivos** de distribución anual de pagos
- 💾 **Exportación de datos** en formato PDF y CSV
- 🎨 **Interfaz moderna** con navegación lateral intuitiva
- 🛡️ **Incluye seguros** y análisis detallado de costos
- 📱 **Responsive design** que funciona en cualquier dispositivo

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Rápida

1. **Clona el repositorio:**
```bash
git clone https://github.com/jesmonsa/Calculadora-de-Credito-con-Streamlit.git
cd Calculadora-de-Credito-con-Streamlit
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecuta la aplicación:**
```bash
streamlit run calculadora_credito/app.py
```

4. **Abre tu navegador** en `http://localhost:8501`

## 📋 Funcionalidades Detalladas

### 🎯 Página 1: Entrada de Datos y Resumen
- **Parámetros del crédito:** Monto, tasa anual, plazo, seguro mensual
- **Resumen compacto:** Métricas clave en formato visual
- **Gráfico anual:** Distribución de pagos por año (capital, intereses, seguros)
- **Análisis detallado:** Totales y proporciones

### 📅 Página 2: Tabla de Amortización
- **Tabla completa:** Desglose mes a mes con todas las columnas
- **Organización inteligente:** Pestañas para créditos largos (>1 año)
- **Exportación:** Descarga en PDF (formato profesional) y CSV
- **Métricas por período:** Resúmenes detallados

### 📊 Columnas de la Tabla de Amortización
- **Mes:** Número del período
- **Cuota Crédito:** Pago mensual del crédito (sin seguro)
- **Interés:** Porción correspondiente a intereses
- **Abono Capital:** Porción que reduce el capital
- **Seguro:** Cuota mensual de seguro
- **Pago Total:** Total mensual (crédito + seguro)
- **Saldo Pendiente:** Capital restante

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje principal
- **Streamlit** - Framework web para la interfaz
- **Pandas** - Manipulación de datos
- **Plotly** - Gráficos interactivos
- **ReportLab** - Generación de PDFs
- **NumPy** - Cálculos matemáticos

## 📦 Dependencias

```
streamlit==1.50.0
pandas==2.3.3
plotly==5.17.0
reportlab==4.2.5
numpy==2.3.3
```

## 🎨 Capturas de Pantalla

### Interfaz Principal
- Navegación lateral intuitiva
- Parámetros de entrada claros
- Métricas visuales destacadas

### Tabla de Amortización
- Formato profesional y legible
- Organización en pestañas para créditos largos
- Botones de exportación prominentes

### Gráficos Interactivos
- Distribución anual de pagos
- Barras apiladas con hover informativo
- Colores distintivos para cada componente

## 🔧 Configuración Avanzada

### Personalización de Parámetros
- **Monto:** $1,000 - $10,000,000
- **Tasa:** 0% - 50% anual
- **Plazo:** 1 - 30 años
- **Seguro:** $0 - $500 mensual

### Fórmula de Amortización
```
Cuota = P × (r × (1 + r)^n) / ((1 + r)^n - 1)
```
Donde:
- P = Monto del préstamo
- r = Tasa de interés mensual
- n = Número total de pagos mensuales

## 📈 Casos de Uso

- **Personas:** Calcular cuotas de préstamos personales
- **Empresas:** Análisis de financiamiento empresarial
- **Inmobiliario:** Evaluación de créditos hipotecarios
- **Educativo:** Herramienta de aprendizaje financiero
- **Profesionales:** Consultores financieros y asesores

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Jesús Monsalve**
- GitHub: [@jesmonsa](https://github.com/jesmonsa)
- Proyecto: [Calculadora de Crédito](https://github.com/jesmonsa/Calculadora-de-Credito-con-Streamlit)

## 🙏 Agradecimientos

- Streamlit por el excelente framework web
- Plotly por las visualizaciones interactivas
- ReportLab por la generación de PDFs
- Comunidad Python por las librerías de apoyo

## 📞 Soporte

Si tienes preguntas o encuentras algún problema:

1. Revisa los [Issues existentes](https://github.com/jesmonsa/Calculadora-de-Credito-con-Streamlit/issues)
2. Crea un nuevo Issue con detalles del problema
3. Incluye información del sistema y pasos para reproducir

---

⭐ **¡Si te gusta este proyecto, no olvides darle una estrella!** ⭐
