# Certificados de Ramsey Vibracional

Este directorio contiene certificados formales de las cotas superiores de R_ψ(r,s,ε).

## Estructura

- **`*.smt2`**: Fórmulas SMT2 que codifican el problema de verificación
- **`*.lean`**: Certificados Lean 4 generados automáticamente
- **`*.pdf`**: Certificados formales en formato PDF con documentación completa
- **`*.olean`**: Archivos compilados de Lean (no versionados)

## Certificados Disponibles

| Par (r,s) | Cota | ε | Grid | λ | Archivo SMT2 | Archivo Lean | Archivo PDF | Estado |
|-----------|------|---|------|---|--------------|--------------|-------------|--------|
| (3,3) | ≤ 5 | 0.001 | 128 | 0.1 | Rpsi_3_3_le_5.smt2 | Rpsi_3_3_le_5.lean | Rpsi_3_3_certificate.pdf | ✓ |
| (4,4) | ≤ 10 | 0.001 | 128 | 0.062 | Rpsi_4_4_le_10.smt2 | Rpsi_4_4_le_10.lean | Rpsi_4_4_certificate.pdf | ✓ |
| (5,5) | ≤ 19 | 1/128 | 128 | 0.037 | 5_5_0.037.smt2 | formal/Theorems/R_psi_5_5_le_19.lean | - | ✓ |

## Flujo de Certificación

```
Julia                     Z3/SAT Solver           Lean 4
  │                            │                    │
  ├─→ generate_formula()      │                    │
  │   (r,s,λ,n,ε,grid)        │                    │
  │                            │                    │
  ├─→ formula.smt2 ──────────→ check-sat           │
  │                            │                    │
  │                            ├─→ UNSAT            │
  │                            │   (certificate)    │
  │                            │                    │
  ├─→ generate_lean_proof() ──┴──────────────────→ theorem
  │   (R_ψ(r,s) ≤ n)                               │
  │                                                 │
  └─────────────────────────────────────────────→ compile & verify
                                                    (.olean)
```

## Formato SMT2

Los archivos `.smt2` siguen esta estructura:

1. **Declaraciones**: Variables de frecuencia ω_0, ω_1, ..., ω_{n-1}
2. **Dominios**: Restricciones 0 ≤ ω_i < grid
3. **Operador de resonancia**: Función `resonant(x, y)`
4. **Negación K_r azul**: C(n,r) cláusulas
5. **Negación K_s rojo**: C(n,s) cláusulas
6. **Check**: `(check-sat)` → `unsat`

## Formato Lean

Los archivos `.lean` tienen:

1. **Imports**: `VibrationalRamsey`, `Tactic`
2. **Documentación**: Parámetros de verificación
3. **Teorema**: `theorem R_ψ_r_s_le_n : R_ψ r s ε ≤ n`
4. **Prueba**: `by vibrational_unsat_tac {...}`

## Verificación

Para verificar un certificado:

```bash
# Verificar SMT2 con Z3
z3 certificates/5_5_0.037.smt2

# Compilar y verificar Lean
cd formal
lake build Theorems.R_psi_5_5_le_19
```

## Generación Automática

### Certificados Lean y SMT2

Los certificados se generan automáticamente desde Julia:

```julia
include("julia/generate_lean_proof.jl")
generate_lean_proof(5, 5, 0.037, 19; grid=128)
```

### Certificados PDF

Los certificados PDF se generan con el script Python:

```bash
python generate_pdf_certificate.py
```

Este script genera certificados PDF formales que incluyen:
- Parámetros del bound (λ, f₀, ε)
- Enunciado del teorema
- Fragmento de código Lean4
- Método de verificación
- Referencias al repositorio

## Referencias

- **Teoría de Ramsey Vibracional**: Ver `../IMPLEMENTACION.md`
- **Campo QCAL ∞³**: Frecuencia base 141.7001 Hz
- **SMT-LIB**: https://smtlib.cs.uiowa.edu/
- **Lean 4**: https://lean-lang.org/

---

**Instituto de Consciencia Cuántica (ICQ)**  
*"El orden emerge inevitablemente cuando consideramos la naturaleza vibracional de los sistemas"*
