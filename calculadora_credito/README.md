# Instrucciones para Ejecutar la Calculadora de Crédito

## Requisitos Previos
- Python 3.7 o superior instalado
- pip (gestor de paquetes de Python)

## Instalación y Ejecución

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación
```bash
streamlit run app.py
```

### 3. Abrir en el Navegador
La aplicación se abrirá automáticamente en tu navegador predeterminado, generalmente en:
```
http://localhost:8501
```

## Características de la Aplicación

✅ **Campos de Entrada:**
- Monto del préstamo (con validación de rango)
- Tasa de interés anual (con validación de rango)
- Plazo en años (con validación de rango)

✅ **Resultados Calculados:**
- Cuota mensual
- Total pagado al final del período
- Intereses pagados
- **Tabla de amortización completa** con desglose mes a mes

✅ **Interfaz Adicional:**
- Métricas visuales con delta
- Tabla de resumen completo
- Gráfico de distribución (capital vs intereses)
- **Tabla de amortización mes a mes** (nueva funcionalidad)
- Información técnica sobre los cálculos
- Diseño responsive y moderno

## Fórmula Utilizada
La aplicación utiliza la fórmula estándar de amortización para calcular la cuota mensual:
```
Cuota = P × (r × (1 + r)^n) / ((1 + r)^n - 1)
```

Donde:
- P = Monto del préstamo
- r = Tasa de interés mensual
- n = Número total de pagos mensuales

## Tabla de Amortización
La aplicación genera una tabla de amortización completa que muestra:
- **Mes**: Número del mes del crédito
- **Cuota Total**: Pago mensual fijo
- **Interés**: Porción de la cuota que corresponde a intereses
- **Abono Capital**: Porción de la cuota que reduce el capital
- **Saldo Pendiente**: Capital restante después de cada pago

Para créditos largos (más de 1 año), la tabla se organiza en pestañas por períodos de 4 años para facilitar la navegación.

## Notas Importantes
- Los cálculos son aproximados y pueden variar según las condiciones específicas del prestamista
- La calculadora no incluye seguros, comisiones u otros cargos adicionales
- Consulta con tu institución financiera para obtener términos exactos


