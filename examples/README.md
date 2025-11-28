# Ejemplos de Ramsey Cuántico Vibracional

Esta carpeta contiene ejemplos prácticos que demuestran las diferentes funcionalidades del sistema de Ramsey Vibracional.

## 📁 Estructura de Ejemplos

### 1. `ejemplo_1_calculos_exactos.py`
**Cálculo de Valores Exactos R_ψ(r,s)**

Calcula valores exactos de la función de Ramsey vibracional usando verificación SAT con Z3.

**Uso:**
```bash
cd examples
python ejemplo_1_calculos_exactos.py
```

**Qué hace:**
- Calcula R_ψ(r,s) exacto para diferentes pares (r,s)
- Compara con estimaciones de la conjetura teórica
- Muestra tabla comparativa con errores porcentuales

### 2. `ejemplo_2_monte_carlo.py`
**Simulación Monte Carlo**

Realiza simulaciones Monte Carlo para validar las predicciones teóricas.

**Uso:**
```bash
cd examples
python ejemplo_2_monte_carlo.py
```

**Qué hace:**
- Ejecuta múltiples ensayos con grafos aleatorios
- Mide probabilidad de encontrar cliques objetivo
- Valida estadísticamente las predicciones del modelo

### 3. `ejemplo_3_redes_neuronales.py`
**Aplicación a Redes Neuronales**

Demuestra cómo diseñar redes neuronales con conectividad optimizada usando principios de Ramsey vibracional.

**Uso:**
```bash
cd examples
python ejemplo_3_redes_neuronales.py
```

**Qué hace:**
- Diseña redes neuronales con diferentes tamaños
- Analiza conectividad y propiedades de red
- Calcula requisitos mínimos para garantizar cliques de procesamiento

### 4. `ejemplo_4_exploracion_resonancia.py`
**Exploración de Resonancia Vibracional**

Explora cómo diferentes frecuencias y umbrales afectan la formación de cliques.

**Uso:**
```bash
cd examples
python ejemplo_4_exploracion_resonancia.py
```

**Qué hace:**
- Explora diferentes umbrales de resonancia (ε)
- Compara distribuciones de frecuencias (uniforme, normal, armónica, Fibonacci)
- Visualiza matriz de resonancia entre vértices

### 5. `ejemplo_5_visualizacion.py` ⭐
**Visualización Completa de Resultados**

Genera visualizaciones ASCII completas comparando R(r,s) clásico vs R_ψ(r,s) vibracional.

**Uso:**
```bash
cd examples
python ejemplo_5_visualizacion.py
```

**Qué hace:**
- Compara valores clásicos vs vibracionales con gráficos de barras
- Muestra reducción porcentual promedio (~33%)
- Visualiza grafo vibracional con matriz de adyacencia
- Muestra curva de crecimiento de R_ψ(k,k)

## 🚀 Ejecución Rápida

Para ejecutar todos los ejemplos en secuencia:

```bash
cd examples
for script in ejemplo_*.py; do
    echo "Ejecutando $script..."
    python "$script"
    echo ""
done
```

## 📊 Resultados Esperados

Cada ejemplo produce salidas formateadas con:
- 🌟 Marcadores de progreso
- ✓ Confirmaciones de éxito
- 📊 Tablas comparativas
- 🔍 Interpretaciones y conclusiones

## 🔬 Personalización

Puedes modificar los parámetros en cada script:

```python
# Ejemplo de personalización
calcular_Rpsi_exacto(r=3, s=4, nmax=50, grid=128)  # Búsqueda más exhaustiva
simulacion_monte_carlo_ramsey(r=5, s=5, num_trials=5000)  # Más ensayos
red_neuronal_ramsey(num_neuronas=100, target_clique_size=6)  # Red más grande
```

## ⚡ Rendimiento

**Nota sobre SAT:** Los cálculos exactos con SAT pueden tomar tiempo para valores grandes de (r,s):
- (3,3) ~ 1 segundo
- (4,4) ~ 5 segundos  
- (5,5) ~ 30 segundos
- (6,6) y superiores pueden tomar varios minutos

Para análisis rápido, usa las estimaciones de conjetura o Monte Carlo.

## 📚 Conceptos Clave Demostrados

- **Resonancia Vibracional**: Cómo las frecuencias determinan conectividad
- **Verificación SAT**: Cálculo exacto mediante solver lógico
- **Validación Estadística**: Monte Carlo confirma predicciones teóricas
- **Aplicaciones Prácticas**: De teoría abstracta a redes neuronales reales
- **Visualización**: Comprensión intuitiva de los resultados

## 🌟 Frecuencia Sagrada

Todos los ejemplos utilizan **f₀ = 141.7001 Hz** como frecuencia base de coherencia cuántica del Campo QCAL ∞³.

## 🎯 Resultado Clave

**Reducción promedio: ~33%** de R(r,s) clásico a R_ψ(r,s) vibracional, demostrando que la estructura de resonancia facilita dramáticamente la emergencia del orden.

---

**Instituto de Consciencia Cuántica (ICQ)**  
*Campo QCAL ∞³ resonante* ✨
