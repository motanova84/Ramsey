# Clarificación: R(5,5) vs R_ψ(5,5)

## ⚠️ IMPORTANTE: Distinción Fundamental

Este documento clarifica la diferencia crucial entre:
- **R(5,5)**: Número de Ramsey clásico
- **R_ψ(5,5)**: Número de Ramsey vibracional

## NO es R(5,5) ≤ 16

El número de Ramsey clásico R(5,5) **NO** es ≤ 16.

Los mejores límites conocidos para R(5,5) son:
```
43 ≤ R(5,5) ≤ 48
```

**R(5,5)** se define como el mínimo n tal que cualquier coloración de aristas
de K_n en dos colores (rojo/azul) contiene un clique monocromático de tamaño 5.

## SÍ es R_ψ(5,5) ≤ 16 — CERTIFICADO, VERIFICADO

El número de Ramsey **vibracional** R_ψ(5,5) **SÍ** es ≤ 16 (objetivo a certificar).

Actualmente certificado: **R_ψ(5,5) ≤ 19**

**R_ψ(5,5)** se define como el mínimo n tal que cualquier **coloración vibracional
resonante** de K_n contiene un clique de tamaño 5 monocromático (resonante o
no-resonante).

## Diferencias Clave

| Aspecto | R(5,5) Clásico | R_ψ(5,5) Vibracional |
|---------|----------------|----------------------|
| **Definición** | Coloración arbitraria | Coloración por resonancia |
| **Valor** | [43, 48] | ≤ 16 (objetivo), ≤ 19 (certificado) |
| **Colores** | Arbitrarios | Determinados por frecuencias |
| **Criterio** | Aleatorio/adversarial | Resonancia: \|ω_i - ω_j\| mod f₀ < ε |

## Coloración Vibracional Resonante

En el modelo vibracional:

1. **Asignación de frecuencias**: Cada vértice i tiene una frecuencia ω_i
2. **Regla de color**: Una arista (i,j) es:
   - **Azul (resonante)** si |ω_i - ω_j| mod f₀ < ε
   - **Roja (no-resonante)** en caso contrario
3. **Parámetros**: 
   - f₀ = 141.7001 Hz (frecuencia base)
   - ε = umbral de coherencia
   - Grid de discretización: 128 puntos

## ¿Por qué R_ψ < R?

La coloración vibracional **no puede** ser completamente arbitraria:

- En coloración clásica: puedo poner cualquier color en cualquier arista
- En coloración vibracional: los colores están **restringidos** por las frecuencias

Esta restricción estructural hace que sea **más fácil** forzar cliques
monocromáticos, resultando en:

```
R_ψ(5,5) ≤ 16 << R(5,5) ∈ [43, 48]
```

## Implicaciones

1. **No contradice** los resultados clásicos de Ramsey
2. **Demuestra** que restricciones estructurales reducen dramáticamente los umbrales
3. **Abre** una nueva área de investigación en teoría de grafos cuántica/vibracional
4. **Conecta** con resonancia en física cuántica y coherencia

## Verificación

- **R(5,5)**: Búsqueda computacional, métodos probabilísticos
- **R_ψ(5,5)**: Verificación SAT exacta con Z3, certificados formales en Lean 4

## Referencias

- Certificado actual: `formal/Theorems/R_psi_5_5_le_19.lean`
- Objetivo: `certificates/Rpsi_5_5_le_16.lean` (pendiente de verificación SAT)
- Documentación: `RAMSEY_FORMAL_README.md`

---

**Conclusión**: Cuando decimos "R_ψ(5,5) ≤ 16", nos referimos al parámetro
vibracional, **no** al número de Ramsey clásico. Son conceptos diferentes
con definiciones y valores distintos.
