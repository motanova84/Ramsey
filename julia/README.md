# Julia → Lean 4 Bridge

Este directorio contiene el código Julia que actúa como puente entre la verificación SAT (usando Z3) y la certificación formal en Lean 4.

## 🎯 Propósito

1. **Generar fórmulas SAT** para verificar cotas de R_ψ(r,s,ε)
2. **Invocar Z3** para resolver las fórmulas
3. **Generar certificados Lean 4** automáticamente cuando se obtiene UNSAT
4. **Validar modelos SAT** para asegurar contraejemplos válidos

## 📁 Archivos

- **`generate_lean_proof.jl`**: Generador principal de pruebas Lean
- **`validate_model.jl`**: Validador de modelos SAT
- **`README.md`**: Esta documentación

## 🚀 Uso Rápido

### Requisitos

```bash
# Instalar Julia (https://julialang.org/downloads/)
# Versión recomendada: Julia 1.9+

julia --version
```

### Instalación de Paquetes (Futuro)

Para una implementación completa, se necesitarían:

```julia
using Pkg

# Paquetes requeridos (no instalados aún)
# Pkg.add("Z3")          # Interfaz Julia para Z3
# Pkg.add("PyCall")      # Para integración con Python si es necesario
# Pkg.add("JSON")        # Para manejo de configuración
```

### Generar un Certificado

```julia
# Cargar el módulo
include("generate_lean_proof.jl")

# Generar certificado para R_ψ(5,5) ≤ 19
generate_lean_proof(5, 5, 0.037, 19; grid=128, f0=141.7001)

# Resultado:
#   - formal/Theorems/R_psi_5_5_le_19.lean
#   - certificates/5_5_0.037.smt2
```

### Generación en Lote

```julia
include("generate_lean_proof.jl")

# Casos a certificar
cases = [
    (3, 3, 0.037, 6),   # R_ψ(3,3) ≤ 6
    (4, 4, 0.037, 11),  # R_ψ(4,4) ≤ 11
    (5, 5, 0.037, 19),  # R_ψ(5,5) ≤ 19
]

# Generar todos los certificados
batch_generate_proofs(cases; grid=128, f0=141.7001)
```

### Validar un Modelo

```julia
include("validate_model.jl")

# Validar una asignación de frecuencias
frequencies = [10.0, 45.0, 85.0, 125.0, 20.0]
valid, reason = validate_model(frequencies, 3, 3, 0.001, 141.7001)

println("Resultado: ", valid ? "VÁLIDO ✓" : "INVÁLIDO ✗")
println("Razón: ", reason)
```

## 📚 API Reference

### `make_vibrational_formula`

Genera una fórmula SAT para verificar si n ≥ R_ψ(r,s,ε).

```julia
make_vibrational_formula(r, s, lam, n; grid=128, f0=141.7001, eps=0.001)
```

**Parámetros:**
- `r::Int`: Tamaño del clique azul buscado
- `s::Int`: Tamaño del clique rojo buscado
- `lam::Float64`: Parámetro lambda vibracional
- `n::Int`: Número de vértices a verificar
- `grid::Int`: Resolución de discretización (default: 128)
- `f0::Float64`: Frecuencia base de coherencia (default: 141.7001 Hz)
- `eps::Float64`: Umbral de coherencia (default: 0.001 Hz)

**Retorna:** Fórmula SAT compatible con Z3

**Ejemplo:**
```julia
formula = make_vibrational_formula(5, 5, 0.037, 19; grid=128)
```

### `check_sat`

Verifica satisfacibilidad de la fórmula SAT usando Z3.

```julia
check_sat(formula)
```

**Parámetros:**
- `formula`: Fórmula SAT generada por `make_vibrational_formula`

**Retorna:** `(status, model)` donde:
- `status`: `:sat`, `:unsat` o `:unknown`
- `model`: Modelo satisfaciente (si existe) o `nothing`

**Ejemplo:**
```julia
status, model = check_sat(formula)
if status == :unsat
    println("✓ Cota verificada")
end
```

### `generate_lean_proof`

Genera un archivo `.lean` con certificado de prueba si la verificación SAT tiene éxito.

```julia
generate_lean_proof(r, s, lam, n; grid=128, f0=141.7001, eps=0.001)
```

**Parámetros:**
- `r::Int`: Tamaño del clique azul
- `s::Int`: Tamaño del clique rojo
- `lam::Float64`: Parámetro lambda vibracional
- `n::Int`: Cota superior a certificar
- `grid::Int`: Resolución de discretización (default: 128)
- `f0::Float64`: Frecuencia base (default: 141.7001 Hz)
- `eps::Float64`: Umbral de coherencia (default: 0.001 Hz)

**Efectos:**
- Si UNSAT: Genera `formal/Theorems/R_ψ_{r}_{s}_le_{n}.lean`
- Exporta también `certificates/{r}_{s}_{lam}.smt2`

**Retorna:** `true` si exitoso, `false` en caso contrario

**Ejemplo:**
```julia
success = generate_lean_proof(5, 5, 0.037, 19)
if success
    println("✓ Certificado generado")
end
```

### `batch_generate_proofs`

Genera pruebas Lean en lote para múltiples casos.

```julia
batch_generate_proofs(cases; grid=128, f0=141.7001)
```

**Parámetros:**
- `cases::Vector{Tuple{Int,Int,Float64,Int}}`: Vector de tuplas (r, s, lam, n)
- `grid::Int`: Resolución de discretización
- `f0::Float64`: Frecuencia base

**Retorna:** Vector de resultados (r, s, n, success)

### `validate_model`

Valida que un modelo SAT sea un contraejemplo válido para R_ψ(r,s,ε).

```julia
validate_model(frequencies, r, s, ε, f₀)
```

**Parámetros:**
- `frequencies::Vector{Float64}`: Asignación de frecuencias
- `r::Int`: Tamaño del clique azul buscado
- `s::Int`: Tamaño del clique rojo buscado
- `ε::Float64`: Umbral de coherencia
- `f₀::Float64`: Frecuencia base

**Retorna:** `(valid::Bool, reason::String)`

**Ejemplo:**
```julia
freqs = [10.0, 45.0, 85.0, 125.0, 20.0]
valid, reason = validate_model(freqs, 3, 3, 0.001, 141.7001)
```

### `resonance_detected`

Implementa el Operador de Resonancia.

```julia
resonance_detected(ω_i, ω_j, ε, f₀)
```

**Parámetros:**
- `ω_i::Float64`: Frecuencia del vértice i
- `ω_j::Float64`: Frecuencia del vértice j
- `ε::Float64`: Umbral de coherencia
- `f₀::Float64`: Frecuencia base

**Retorna:** `true` si están en resonancia, `false` en caso contrario

## 🔬 Implementación de la Fórmula SAT

### Estructura de la Fórmula

La fórmula SAT codifica el problema de verificación de R_ψ(r,s,ε) ≤ n:

```
1. Variables: ω_0, ω_1, ..., ω_{n-1} ∈ {0, 1, ..., grid-1}
   Representan frecuencias discretizadas

2. Operador de Resonancia:
   Res(ω_i, ω_j) ⟺ |ω_i - ω_j| mod grid < ε_discretizado

3. Negación de K_r azul:
   Para todo S ⊆ V con |S| = r:
     ∃ (i,j) ∈ S×S : ¬Res(ω_i, ω_j)
   
   Genera C(n,r) cláusulas

4. Negación de K_s rojo:
   Para todo T ⊆ V con |T| = s:
     ∃ (i,j) ∈ T×T : Res(ω_i, ω_j)
   
   Genera C(n,s) cláusulas
```

### Ejemplo Concreto

Para R_ψ(3,3) con n=6:

```smt2
; Variables
(declare-const w_0 Int)
(declare-const w_1 Int)
...
(declare-const w_5 Int)

; Dominios
(assert (and (>= w_0 0) (< w_0 128)))
...

; Operador de resonancia
(define-fun resonant ((x Int) (y Int)) Bool
  (or (< (abs (- x y)) 2)
      (> (abs (- x y)) 126)))

; Negación K_3 azul para {0,1,2}
(assert (or
  (not (resonant w_0 w_1))
  (not (resonant w_0 w_2))
  (not (resonant w_1 w_2))
))

; ... C(6,3) = 20 cláusulas más ...

; Negación K_3 rojo para {0,1,2}
(assert (or
  (resonant w_0 w_1)
  (resonant w_0 w_2)
  (resonant w_1 w_2)
))

; ... C(6,3) = 20 cláusulas más ...

(check-sat)
```

## 🔄 Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Especificar problema: R_ψ(r,s) ≤ n?                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. make_vibrational_formula(r, s, lam, n)                   │
│    - Crear variables de frecuencia                          │
│    - Codificar operador de resonancia                       │
│    - Generar restricciones de cliques                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. check_sat(formula)                                       │
│    - Invocar Z3                                             │
│    - Obtener resultado: SAT / UNSAT / UNKNOWN              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                    ¿UNSAT?
                    /      \
                 Sí /        \ No
                   /          \
                  ▼            ▼
    ┌─────────────────┐  ┌──────────────────┐
    │ 4a. Generar     │  │ 4b. n < R_ψ(r,s) │
    │     .lean       │  │     Contraejemplo│
    │     .smt2       │  │     existe       │
    └─────────┬───────┘  └──────────────────┘
              │
              ▼
    ┌──────────────────┐
    │ 5. Compilar con  │
    │    lake build    │
    └─────────┬────────┘
              │
              ▼
    ┌──────────────────┐
    │ 6. Certificado   │
    │    verificado ✓  │
    └──────────────────┘
```

## 🛠️ Estado de Implementación

### Implementado ✅

- [x] Estructura de archivos y funciones
- [x] Documentación completa
- [x] Ejemplos de uso
- [x] Generación de archivos .lean
- [x] Generación de archivos .smt2 (estructura)
- [x] Validador de modelos (lógica básica)

### Pendiente ⏳

- [ ] Integración real con Z3 (requiere paquete Julia)
- [ ] Generación completa de fórmulas SAT (todas las cláusulas)
- [ ] Parseo de certificados UNSAT desde Z3
- [ ] Optimización de generación de combinaciones
- [ ] Tests unitarios
- [ ] Integración con CI/CD

## 📖 Referencias

### Julia
- [Julia Language](https://julialang.org/)
- [Julia Packages](https://juliapackages.com/)

### Z3
- [Z3 Theorem Prover](https://github.com/Z3Prover/z3)
- [SMT-LIB Standard](https://smtlib.cs.uiowa.edu/)

### Este Proyecto
- [README Principal](../README.md)
- [Formalización Lean 4](../formal/)
- [Certificados](../certificates/)

## 🤝 Contribuir

Para contribuir al puente Julia:

1. Implementar la integración real con Z3
2. Optimizar la generación de fórmulas SAT
3. Agregar tests unitarios
4. Mejorar el validador de modelos
5. Documentar casos de uso adicionales

---

**Instituto de Consciencia Cuántica (ICQ)**  
*"Puente entre computación y certificación formal"*

**Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³**
