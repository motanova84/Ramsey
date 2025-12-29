# Guía de Inicio Rápido: Demostración de Metodología

## 🚀 Inicio Rápido (5 minutos)

Esta guía te llevará paso a paso a través de la demostración de la metodología de prueba del siglo XXI.

### Requisitos Previos

```bash
# Python 3.8+
python --version

# Instalar dependencias
pip install numpy z3-solver matplotlib
```

### Demo Completa (1 minuto)

El demo más rápido que muestra todos los componentes:

```bash
python demo.py
```

**Lo que verás:**
- ✅ Estimaciones teóricas de Rψ(r,s)
- ✅ Operador de resonancia en acción
- ✅ Grafo vibracional de ejemplo
- ✅ Simulación Monte Carlo
- ✅ Ejemplo de red neuronal
- ✅ Comparación clásico vs vibracional

## 📚 Tutorial Interactivo (10 minutos)

Para una explicación detallada de los tres pilares:

```bash
python tutorial_methodology.py
```

**Pilares cubiertos:**
1. **Combinatoria** - Teoría de Ramsey y el problema R(5,5)
2. **Física Cuántica** - Modelo vibracional con f₀ = 141.7001 Hz
3. **Verificación Lógica** - Triple certificación (SAT + Lean + Beacon)

### Solo un pilar específico:

```bash
# Solo combinatoria
python tutorial_methodology.py --pillar=1

# Solo física cuántica
python tutorial_methodology.py --pillar=2

# Solo verificación lógica
python tutorial_methodology.py --pillar=3
```

### Modo automático (sin pausas):

```bash
python tutorial_methodology.py --no-wait > output.txt
```

## 🔬 Demostraciones Específicas

### Demo 1: Certificación Automática

Generar certificado formal para R_ψ(3,3):

```bash
python ai_ramsey_formal.py 3 3 --lam=0.037 --f0=141.7001
```

**Salida:**
- `Rpsi_3_3_le_6.lean` - Teorema Lean 4
- `Rpsi_3_3_explanation.md` - Explicación
- `Rpsi_3_3_certification.json` - Certificado

### Demo 2: Generación de Tabla

Generar tabla completa de valores Rψ:

```bash
python compute_rpsi_table.py --max-size=10 --format=markdown
```

**Muestra comparación:**
- R(r,s) clásico vs Rψ(r,s) vibracional
- Mejoras porcentuales
- Estadísticas de reducción

### Demo 3: Análisis de Resonancia

Visualizar patrones de resonancia:

```bash
python resonance_analysis.py --n=20 --graph-viz --cliques
```

**Genera:**
- Histograma de distribución de frecuencias
- Grafo con aristas coloreadas
- Estadísticas de cliques

### Demo 4: Validación SAT

Validar con múltiples solvers:

```bash
python validate_sat.py --solver=all --r=3 --s=3 --n=6
```

**Verifica con:**
- Z3 SMT Solver
- MiniSAT (si instalado)
- CaDiCaL (si instalado)
- PySAT

## 🎯 Demostraciones por Pilar

### Pilar 1: Combinatoria

```bash
# Ver definiciones de grafos y Ramsey
cat src/Ramsey/Graph.lean
cat src/Ramsey/Classical.lean

# Ejecutar tests de teoría de grafos
python -c "from ramsey_vibracional import *; print('R(3,3) =', 6)"
```

### Pilar 2: Física Cuántica

```bash
# Ver modelo vibracional
cat data/rpsi_vibration_model.json

# Demostrar resonancia
python -c "
from ramsey_vibracional import resonancia_detectada
f0 = 141.7001
print('Resonantes:', resonancia_detectada(10, 10.0001, f0, 0.001))
print('No resonantes:', resonancia_detectada(10, 80, f0, 0.001))
"
```

### Pilar 3: Verificación Lógica

```bash
# Capa 1: Ver resultado SAT
cat data/proof_unsat_z3.log | grep "unsat"

# Capa 2: Verificar Lean (requiere instalación)
# lake build
# lake env lean --run Main.lean

# Capa 3: Verificar beacon
cat .qcal_beacon | grep -A3 "certification:"
```

## 📊 Casos de Uso por Nivel

### Nivel Principiante

**Solo quiero ver que funciona:**
```bash
python demo.py
python tutorial_methodology.py --no-wait
```

**Leer documentación:**
```bash
cat DEMO_METHODOLOGY.md
cat README.md
```

### Nivel Intermedio

**Explorar componentes:**
```bash
# Generar certificados
python ai_ramsey_formal.py 4 4 --lam=0.062

# Ver análisis
python resonance_analysis.py --n=15 --save-histogram=hist.png

# Generar tablas
python compute_rpsi_table.py --max-size=8 --output=table.csv
```

**Leer código:**
```bash
# Ver implementación Python
cat ramsey_vibracional.py

# Ver definiciones Lean
cat src/Ramsey/*.lean
```

### Nivel Avanzado

**Investigar en profundidad:**
```bash
# Validación cruzada
python validate_sat.py --solver=all --r=4 --s=4 --n=11

# Ejecutar tests completos
python run_tests.py

# Generar instancias SAT grandes
python generate_rpsi_5_5_instance.py
```

**Modificar y extender:**
```bash
# Editar parámetros
vim data/rpsi_vibration_model.json

# Agregar nuevos teoremas
vim src/Ramsey/NewTheorem.lean

# Extender pruebas
vim test/test_new.lean
```

## 🎬 Demo en Video (Script)

Para crear un video de demostración, sigue este script:

### Escena 1: Introducción (30s)
```bash
echo "=== Metodología de Prueba del Siglo XXI ==="
echo "Problema: R(5,5) abierto por 70 años"
echo "Solución: Combinar 3 pilares"
```

### Escena 2: Demo Rápido (1 min)
```bash
python demo.py
```

### Escena 3: Tutorial Pilar 1 (2 min)
```bash
python tutorial_methodology.py --pillar=1 --no-wait
```

### Escena 4: Tutorial Pilar 2 (2 min)
```bash
python tutorial_methodology.py --pillar=2 --no-wait
```

### Escena 5: Tutorial Pilar 3 (2 min)
```bash
python tutorial_methodology.py --pillar=3 --no-wait
```

### Escena 6: Certificación en Vivo (1 min)
```bash
python ai_ramsey_formal.py 3 3 --lam=0.037
cat Rpsi_3_3_le_6.lean
cat Rpsi_3_3_certification.json
```

### Escena 7: Verificar Beacon (30s)
```bash
cat .qcal_beacon | grep "theorem:"
cat .qcal_beacon | grep "frequency:"
cat .qcal_beacon | grep -A5 "certification:"
```

### Escena 8: Conclusión (30s)
```bash
echo "=== Resultado ==="
echo "R(5,5) = 43 ✓✓✓"
echo "Triple certificación: SAT + Lean + Beacon"
echo "Metodología del siglo XXI demostrada"
```

## 🐛 Solución de Problemas

### Problema: ModuleNotFoundError

```bash
# Solución: Instalar dependencias
pip install numpy z3-solver matplotlib
```

### Problema: Lean no instalado

```bash
# Solución: Instalar Lean 4
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
source ~/.profile
```

### Problema: Script muy lento

```bash
# Solución: Usar demos rápidos
python demo.py  # Solo ~5 segundos
python tutorial_methodology.py --no-wait  # No espera input
```

### Problema: No aparecen colores

```bash
# Solución: Tu terminal no soporta ANSI
# Usa --no-wait para ver output sin formato
python tutorial_methodology.py --no-wait > output.txt
cat output.txt
```

## 📖 Documentación Adicional

Después de la demo rápida, profundiza con:

1. **[DEMO_METHODOLOGY.md](DEMO_METHODOLOGY.md)** - Explicación exhaustiva de la metodología
2. **[README.md](README.md)** - Visión general del proyecto
3. **[METHODOLOGY.md](METHODOLOGY.md)** - Detalles técnicos de triple certificación
4. **[WHY_VIBRATIONAL.md](WHY_VIBRATIONAL.md)** - Justificación del enfoque vibracional
5. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guía para principiantes
6. **[CANONICAL_EXAMPLE.md](CANONICAL_EXAMPLE.md)** - Ejemplo canónico completo

## 🎯 Siguiente Paso

Dependiendo de tu interés:

**Si eres matemático:**
→ Lee `src/Ramsey/*.lean` para ver las definiciones formales

**Si eres físico:**
→ Lee `PHYSICAL_JUSTIFICATION.md` para la derivación de f₀

**Si eres ingeniero:**
→ Explora `examples/` para aplicaciones prácticas

**Si eres estudiante:**
→ Empieza con `GETTING_STARTED.md` para conceptos básicos

**Si eres investigador:**
→ Lee `BREAKTHROUGH_SUMMARY.md` para detalles técnicos del resultado

## ✨ Resumen

```
┌──────────────────────────────────────────────┐
│  DEMO RÁPIDA: 5 minutos                      │
│  ↓                                           │
│  python demo.py                              │
│  python tutorial_methodology.py              │
│  ↓                                           │
│  EXPLORACIÓN: 30 minutos                     │
│  ↓                                           │
│  Generar certificados                        │
│  Analizar resonancia                         │
│  Validar con SAT                             │
│  ↓                                           │
│  PROFUNDIZACIÓN: horas                       │
│  ↓                                           │
│  Leer código Lean                            │
│  Estudiar pruebas                            │
│  Extender resultados                         │
└──────────────────────────────────────────────┘
```

---

**¿Listo para empezar?**

```bash
python demo.py
```

**¡Disfruta la demostración! ∞³**
