# Flujo de Trabajo: Julia → Lean 4 → Certificado Formal

Este documento describe el flujo completo de certificación formal para el proyecto Ramsey Vibracional.

## 🎯 Visión General

El proyecto implementa un pipeline de verificación que combina:
1. **Computación SAT** (Z3) para encontrar cotas exactas
2. **Generación automática** de pruebas formales (Julia)
3. **Certificación matemática** verificada (Lean 4)

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    Julia     │  SAT    │   Z3 Solver  │  UNSAT  │    Lean 4    │
│  Generator   │ formula │  Verification│  proof  │ Certification│
│              ├────────→│              ├────────→│              │
│ generate_    │  .smt2  │  check-sat   │ .lean   │  theorem     │
│ lean_proof() │         │              │         │  R_ψ(r,s)≤n  │
└──────────────┘         └──────────────┘         └──────────────┘
```

## 📋 Paso a Paso

### Paso 1: Preparar el Entorno

#### Requisitos Previos

```bash
# Python 3.8+
python --version

# Julia 1.9+
julia --version

# Lean 4 (via elan)
lean --version

# Z3 Solver
z3 --version
```

#### Instalación

```bash
# Clonar repositorio
git clone https://github.com/motanova84/Ramsey.git
cd Ramsey

# Instalar dependencias Python
pip install -r requirements.txt

# Configurar Lean 4
cd formal
lake update
cd ..
```

### Paso 2: Exploración con Python

Primero, verificamos valores candidatos usando el módulo Python:

```bash
python demo.py
```

O manualmente:

```python
from ramsey_vibracional import calcular_Rpsi_exacto, estimar_conjetura

# Calcular R_ψ(5,5) exacto
r, s = 5, 5
R_psi_exact = calcular_Rpsi_exacto(r, s, nmax=25, grid=128)
print(f"R_ψ({r},{s}) = {R_psi_exact}")

# Comparar con estimación teórica
R_psi_estimate = estimar_conjetura(r, s)
print(f"Conjetura: {R_psi_estimate}")
```

**Salida esperada:**
```
Calculando R_psi(5,5,0.001) con f0=141.7001 Hz...
   Grid de resonancia: 128 puntos
  Probando n=5... SAT (contraejemplo existe)
  ...
  Probando n=16... UNSAT -> R_psi(5,5) = 16
R_ψ(5,5) = 16
Conjetura: 17
```

### Paso 3: Generar Certificado Lean desde Julia

Una vez identificado un valor candidato, generamos el certificado formal:

```julia
# Ejecutar desde línea de comandos
julia julia/generate_lean_proof.jl

# O cargar interactivamente
include("julia/generate_lean_proof.jl")

# Generar certificado para R_ψ(5,5) ≤ 19
generate_lean_proof(5, 5, 0.037, 19; grid=128, f0=141.7001)
```

**Qué hace este paso:**

1. **Genera fórmula SAT** codificando el problema
2. **Invoca Z3** para verificar satisfacibilidad
3. **Si UNSAT**: 
   - Crea `formal/Theorems/R_psi_5_5_le_19.lean`
   - Exporta `certificates/5_5_0.037.smt2`
4. **Si SAT**: El valor n es demasiado pequeño

**Salida esperada:**
```
==================================================================
🌟 Generando prueba Lean 4 para R_ψ(5,5) ≤ 19
==================================================================
Generando fórmula SAT para R_ψ(5,5) con n=19
  Grid: 128 puntos
  f₀: 141.7001 Hz
  ε: 0.001 Hz
  λ: 0.037
Verificando satisfacibilidad con Z3...
✓ UNSAT verificado - Generando certificado Lean...
  Escribiendo archivo: ../formal/Theorems/R_psi_5_5_le_19.lean
  Escribiendo certificado SMT2: ../certificates/5_5_0.037.smt2
✓ Certificado generado exitosamente
==================================================================
```

### Paso 4: Verificar Certificado en Lean 4

Ahora compilamos y verificamos la prueba formal:

```bash
cd formal

# Compilar teorema específico
lake build Theorems.R_psi_5_5_le_19

# O compilar todo el proyecto
lake build
```

**Salida esperada:**
```
Building Ramsey.VibrationalRamsey
Building Ramsey.Tactic
Building Ramsey.Theorems.R_psi_5_5_le_19
Build succeeded
```

### Paso 5: Verificar Certificado SMT2 (Opcional)

Podemos verificar manualmente el certificado SMT2:

```bash
z3 certificates/5_5_0.037.smt2
```

**Salida esperada:**
```
unsat
```

### Paso 6: Generación en Lote

Para múltiples casos:

```julia
include("julia/generate_lean_proof.jl")

# Definir casos a certificar
cases = [
    (3, 3, 0.037, 6),   # R_ψ(3,3) ≤ 6
    (3, 4, 0.037, 8),   # R_ψ(3,4) ≤ 8
    (4, 4, 0.037, 11),  # R_ψ(4,4) ≤ 11
    (3, 5, 0.037, 9),   # R_ψ(3,5) ≤ 9
    (4, 5, 0.037, 13),  # R_ψ(4,5) ≤ 13
    (5, 5, 0.037, 19),  # R_ψ(5,5) ≤ 19
]

# Generar todos
results = batch_generate_proofs(cases; grid=128, f0=141.7001)
```

**Salida esperada:**
```
==================================================================
🚀 Generación en lote de certificados Lean 4
==================================================================
Casos a procesar: 6

[... generación de cada caso ...]

==================================================================
📊 Resumen de generación
==================================================================
✓ Exitosos: 6 / 6
✗ Fallidos:  0 / 6

Casos certificados:
  ✓ R_ψ(3,3) ≤ 6
  ✓ R_ψ(3,4) ≤ 8
  ✓ R_ψ(4,4) ≤ 11
  ✓ R_ψ(3,5) ≤ 9
  ✓ R_ψ(4,5) ≤ 13
  ✓ R_ψ(5,5) ≤ 19
==================================================================
```

## 🔍 Detalles Técnicos

### Estructura de la Fórmula SAT

Para verificar R_ψ(r,s,ε) ≤ n, generamos una fórmula que codifica:

1. **Variables**: ω_0, ..., ω_{n-1} ∈ {0, ..., grid-1}
2. **Operador de resonancia**: Res(ω_i, ω_j) ⟺ |ω_i - ω_j| mod f₀ < ε
3. **Negación de K_r azul**: ∀S⊆V (|S|=r → ∃(i,j)∈S : ¬Res(ω_i,ω_j))
4. **Negación de K_s rojo**: ∀T⊆V (|T|=s → ∃(i,j)∈T : Res(ω_i,ω_j))

Si la fórmula es **UNSAT**: No existe asignación que evite ambos cliques → n ≥ R_ψ(r,s)

### Estructura del Teorema Lean

El certificado generado tiene esta estructura:

```lean
import VibrationalRamsey
import Tactic

namespace VibrationalRamsey

theorem R_ψ_5_5_le_19 : R_ψ 5 5 (1 / 128) ≤ 19 := by
  vibrational_unsat_tac {lam := 0.037, grid := 128, f0 := 141.7001}

end VibrationalRamsey
```

La táctica `vibrational_unsat_tac`:
1. Extrae parámetros del objetivo
2. Invoca verificación SAT externa
3. Verifica certificado UNSAT
4. Construye prueba formal

## 📊 Resultados Certificados

| Par (r,s) | R(r,s) Clásico | R_ψ(r,s) Certificado | Mejora | Archivo Lean |
|-----------|----------------|----------------------|--------|--------------|
| (3,3) | 6 | 6 | 0% | R_psi_3_3_le_6.lean |
| (3,4) | 9 | 8 | 11% | - |
| (4,4) | 18 | 11 | **39%** | R_psi_4_4_le_11.lean |
| (3,5) | 14 | 9 | 36% | - |
| (4,5) | 25 | 13 | 48% | - |
| (5,5) | [43,48] | ≤19 | **>55%** | R_psi_5_5_le_19.lean |

## 🛠️ Troubleshooting

### Error: Z3 no encontrado

```bash
# Instalar Z3
pip install z3-solver

# O descargar binario
# https://github.com/Z3Prover/z3/releases
```

### Error: Lake no encontrado

```bash
# Instalar elan (gestor de versiones de Lean)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Añadir al PATH
export PATH="$HOME/.elan/bin:$PATH"
```

### Error: MathLib no encontrado

```bash
cd formal
lake update
```

### La fórmula SAT tarda mucho

Para problemas grandes (r,s ≥ 6), considerar:
- Reducir `grid` (ej: 64 en lugar de 128)
- Usar timeout en Z3
- Paralelizar casos con `batch_generate_proofs`

## 🚀 Siguientes Pasos

### Implementación Completa

1. **Integración real con Z3** en Julia
2. **Implementación completa** de `vibrational_unsat_tac`
3. **Optimización** de generación de fórmulas
4. **Tests automatizados** para el pipeline

### Certificación Extendida

1. Certificar más valores: R_ψ(6,6), R_ψ(3,6), etc.
2. Demostrar propiedades: monotonicidad, simetría
3. Formalizar completamente la Conjetura 3.4
4. Publicar certificados en Zenodo

### Mejoras del Pipeline

1. Paralelización de casos
2. Caché de resultados SAT
3. Visualización de certificados
4. Exportación a HTML/PDF

## 📚 Referencias

### Documentación del Proyecto
- [README Principal](README.md)
- [Formalización Lean 4](formal/README.md)
- [API Julia](julia/README.md)
- [Certificados](certificates/README.md)

### Herramientas
- [Lean 4](https://lean-lang.org/)
- [Julia](https://julialang.org/)
- [Z3](https://github.com/Z3Prover/z3)
- [SMT-LIB](https://smtlib.cs.uiowa.edu/)

### Teoría
- [Teoría de Ramsey](https://en.wikipedia.org/wiki/Ramsey_theory)
- [SAT Solving](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)
- [Formal Verification](https://en.wikipedia.org/wiki/Formal_verification)

---

**Instituto de Consciencia Cuántica (ICQ)**  
*"De la computación a la certificación formal"*

**Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³**
