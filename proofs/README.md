# Pruebas Formales en Lean 4

Este directorio contiene teoremas formales en Lean 4 para los números de Ramsey vibracionales Rψ(r,s).

## Archivos

- `Rpsi_5_5_le_16.lean` - Prueba formal de que Rψ(5,5; f₀=141.7001, ε=0.037, grid=128) ≤ 16

## Estructura del Teorema

```lean
theorem Rψ_5_5_le_16 :
  ∀ (c : VibColoring 16),
    (∃ S : Finset (Fin 16), S.card = 5 ∧ ∀ e ∈ S.offDiag, c.color e.1 e.2) ∨
    (∃ S : Finset (Fin 16), S.card = 5 ∧ ∀ e ∈ S.offDiag, ¬c.color e.1 e.2)
```

Este teorema establece que para cualquier coloración vibracional de 16 vértices:
- O existe un clique de 5 vértices con todas las aristas resonantes (azul)
- O existe un clique de 5 vértices con todas las aristas no-resonantes (rojo)

## Compilación

Para verificar las pruebas con Lean 4:

```bash
# En el directorio raíz del proyecto
lake build

# Verificar archivo específico
lean proofs/Rpsi_5_5_le_16.lean
```

## Dependencias

Las pruebas dependen de:
- Mathlib 4.3.0+ - Biblioteca matemática estándar de Lean 4
- `Mathlib.Combinatorics.SimpleGraph.Basic` - Teoría de grafos
- `Mathlib.Data.Finset.Basic` - Conjuntos finitos

## Método de Prueba

La prueba completa combina:

1. **Generación SAT** (`src/generate_rpsi_sat.py`) - Codifica el problema como CNF
2. **Resolución SAT** (`src/solve_rpsi_sat.py`) - Kissat prueba UNSAT
3. **Certificado LRAT** (`cert/rpsi_5_5_n16_unsat.lrat`) - Certificado verificable
4. **Formalización Lean** (este archivo) - Teorema matemático formal

## Conceptos Clave

### VibColoring

Estructura que define una coloración vibracional:
- `ω : Fin n → Fin grid` - Asignación de frecuencias discretizadas
- `color : Fin n → Fin n → Bool` - Color de cada arista
- `valid` - Garantía de que el color es determinado por resonancia

### Resonancia

Dos frecuencias i, j son resonantes si:
```
|ω_val i - ω_val j| mod f₀ ≤ ε  ∨  |ω_val i - ω_val j| mod f₀ ≥ f₀ - ε
```

donde:
- f₀ = 141.7001 Hz (frecuencia base)
- ε = 0.037 Hz (umbral de resonancia)
- grid = 128 (discretización del espacio de frecuencias)

## Estado Actual

La prueba usa `sorry` como placeholder mientras se integra el certificado LRAT con Lean 4. 
La estrategia completa incluye:

- Verificación exhaustiva por model checking finito (128^16 asignaciones discretizadas)
- Certificado LRAT verificado independientemente
- Integración mediante FFI o metaprogramación de Lean

## Referencias

- [Lean 4 Documentation](https://lean-lang.org/lean4/doc/)
- [Mathlib Documentation](https://leanprover-community.github.io/mathlib4_docs/)
- Paper: "Rψ(5,5) ≤ 16 via Vibrational Resonance and SAT"
