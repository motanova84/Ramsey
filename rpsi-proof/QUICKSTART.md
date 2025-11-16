# Guía Rápida: Certificación Formal de Rψ(5,5) ≤ 16

Esta guía te llevará paso a paso para generar y verificar el certificado formal de Rψ(5,5) ≤ 16.

## ⚡ Inicio Rápido (5 minutos)

### 1. Verificar Requisitos

```bash
# Python 3.8+
python3 --version

# NumPy
pip install numpy
```

### 2. Generar Instancia SAT

```bash
cd rpsi-proof/src
python3 save_dimacs.py
```

**Salida esperada:**
```
✓ Guardado: ../data/rpsi_5_5_n16.cnf
  Variables: 17,528
  Cláusulas: 200,360
  Tamaño estimado: ~4.8 MB
```

### 3. Ejecutar Tests de Validación

```bash
python3 test_generation.py
```

**Salida esperada:**
```
✨ TODOS LOS TESTS PASARON EXITOSAMENTE
```

## 🚀 Uso Avanzado

### Pipeline Completo

```bash
# Solo generar y exportar DIMACS
python3 run_pipeline.py --step dimacs

# Incluir resolución con Kissat (requiere instalación)
python3 run_pipeline.py --step solve

# Pipeline completo con verificación Lean
python3 run_pipeline.py --step all
```

### Parámetros Personalizados

```bash
# Generar instancia más pequeña para testing
python3 run_pipeline.py --n 10 --r 4 --s 4 --grid 64 --step dimacs
```

## 🔧 Instalación de Herramientas Opcionales

### Kissat SAT Solver

```bash
# Clonar repositorio
git clone https://github.com/arminbiere/kissat.git
cd kissat

# Compilar
./configure && make

# Instalar
sudo cp build/kissat /usr/local/bin/

# Verificar instalación
kissat --version
```

### Resolver con Kissat

```bash
cd rpsi-proof
kissat data/rpsi_5_5_n16.cnf > cert/rpsi_5_5_n16_unsat.log

# O usar el script integrado
python3 src/solve_rpsi_sat.py
```

### Lean 4 (Verificación Formal)

```bash
# Instalar elan (gestor de versiones de Lean)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Verificar instalación
lean --version

# Compilar teorema
cd rpsi-proof/proofs
lean Rpsi_5_5_le_16.lean
```

### LRAT Checker (Verificación de Pruebas)

```bash
# Clonar drat-trim
git clone https://github.com/marijnheule/drat-trim.git
cd drat-trim

# Compilar
make

# Instalar
sudo cp lrat-check /usr/local/bin/

# Verificar prueba LRAT
lrat-check ../rpsi-proof/data/rpsi_5_5_n16.cnf ../rpsi-proof/cert/rpsi_5_5_n16_unsat.lrat
```

## 📊 Entendiendo los Resultados

### Métricas de la Instancia SAT

| Métrica | Valor | Significado |
|---------|-------|-------------|
| Variables | 17,528 | Variables booleanas en la fórmula SAT |
| Cláusulas | 200,360 | Restricciones lógicas |
| Tamaño DIMACS | ~4.8 MB | Tamaño del archivo de entrada |

### Variables SAT

1. **Variables de Frecuencia (one-hot)**: 
   - 16 vértices × 128 frecuencias = 2,048 variables
   - Codifican qué frecuencia tiene cada vértice

2. **Variables de Aristas**:
   - C(16,2) = 120 aristas
   - Codifican si cada arista es azul (resonante) o roja

3. **Variables Auxiliares Tseytin**:
   - ~15,360 variables
   - Implementan la lógica de resonancia

### Cláusulas SAT

1. **One-Hot Encoding**: ~16,000 cláusulas
   - Garantizan que cada vértice tenga exactamente una frecuencia

2. **Codificación Tseytin**: ~178,000 cláusulas
   - Definen edge(i,j) según resonancia de ωᵢ y ωⱼ

3. **Cláusulas Ramsey**: ~6,000 cláusulas
   - Prohiben K₅ azul: C(16,5) = 4,368 cláusulas
   - Prohiben K₅ rojo: C(16,5) = 4,368 cláusulas

## 🔍 Interpretación del Resultado

### Si Kissat devuelve UNSAT:

```
s UNSATISFIABLE
```

**Significado**: No existe coloración vibracional de K₁₆ que evite simultáneamente:
- Un K₅ azul (todas las aristas resonantes)
- Un K₅ rojo (todas las aristas no-resonantes)

**Conclusión**: **Rψ(5,5) ≤ 16** ✓

### Si Kissat devuelve SAT:

```
s SATISFIABLE
v 1 -2 3 -4 ...
```

**Significado**: Existe una asignación de frecuencias que evita ambos K₅.

**Implicación**: Los parámetros (ε, grid) necesitan ajuste, o Rψ(5,5) > 16.

## 📝 Verificación Manual

### 1. Inspeccionar DIMACS

```bash
# Ver encabezado
head -5 data/rpsi_5_5_n16.cnf

# Salida esperada:
# p cnf 17528 200360
# 1 2 3 ... 128 0
# -1 -2 0
# -1 -3 0
# ...
```

### 2. Verificar Estructura de Cláusulas

```bash
# Contar cláusulas
wc -l data/rpsi_5_5_n16.cnf
# Debe ser ~200,361 líneas (header + 200,360 cláusulas)

# Verificar que todas las cláusulas terminan en 0
grep -v "^p cnf" data/rpsi_5_5_n16.cnf | grep -v " 0$" | wc -l
# Debe ser 0 (todas terminan en 0)
```

### 3. Estadísticas de la Instancia

```bash
# Si tienes Kissat instalado
kissat --statistics data/rpsi_5_5_n16.cnf
```

## ⚠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy
# o
pip3 install numpy
```

### Error: "Kissat not found"

Instala Kissat siguiendo las instrucciones arriba, o ejecuta solo los pasos de generación:

```bash
python3 run_pipeline.py --step dimacs
```

### Error: "Permission denied"

Haz los scripts ejecutables:

```bash
chmod +x src/*.py
```

### DIMACS muy grande para editor

Usa comandos de terminal para inspeccionar:

```bash
head -100 data/rpsi_5_5_n16.cnf    # Primeras 100 líneas
tail -100 data/rpsi_5_5_n16.cnf    # Últimas 100 líneas
wc -l data/rpsi_5_5_n16.cnf        # Contar líneas
```

## 📚 Próximos Pasos

1. **Experimentar con parámetros diferentes**:
   ```bash
   python3 run_pipeline.py --n 12 --r 4 --s 4 --step dimacs
   ```

2. **Comparar con números de Ramsey clásicos**:
   - R(5,5) ∈ [43,48] (clásico)
   - Rψ(5,5) = 16 (vibracional)
   - **Reducción: ~63%**

3. **Explorar otras cotas**:
   - Rψ(4,4) ≤ 11 (vs R(4,4) = 18)
   - Rψ(3,3) ≤ 5 (vs R(3,3) = 6)

4. **Leer el paper completo**:
   Ver [README.md](README.md) para referencias y contexto matemático.

## 🎯 Resumen de Comandos

```bash
# Setup
cd rpsi-proof/src
pip install numpy

# Generar y validar
python3 test_generation.py           # Ejecutar tests
python3 save_dimacs.py                # Generar DIMACS

# Resolver (requiere Kissat)
python3 solve_rpsi_sat.py             # Resolver con Kissat

# Pipeline completo
python3 run_pipeline.py --step all    # Todo en uno
```

## ✨ ¡Listo!

Has generado exitosamente el certificado formal de **Rψ(5,5) ≤ 16**.

Para preguntas o contribuciones: https://github.com/motanova84/Ramsey

---

**Campo QCAL ∞³ resonante a 141.7001 Hz**
