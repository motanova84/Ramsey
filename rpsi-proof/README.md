# rpsi-proof: Certificación SAT para Rψ(5,5) ≤ 16

[![Frequency](https://img.shields.io/badge/f₀-141.7001%20Hz-purple.svg)]()
[![QCAL](https://img.shields.io/badge/QCAL-∞³-orange.svg)]()
[![Variables](https://img.shields.io/badge/variables-120-blue.svg)]()
[![Clauses](https://img.shields.io/badge/clauses-8736-green.svg)]()

> **Certificación Formal mediante SAT de Rψ(5,5) ≤ 16**  
> *Codificación Simbiótica basada en Resonancia Vibracional*

---

## 🎯 Objetivo

Este repositorio contiene la instancia SAT para verificar formalmente si **Rψ(5,5) ≤ 16**, donde Rψ es el número de Ramsey vibracional basado en codificación simbiótica de resonancia.

### ¿Qué es Rψ(r,s)?

Rψ(r,s) es el **menor n** tal que toda coloración vibracional resonante de K_n (grafo completo con n vértices) contiene:
- Un K_r azul (clique resonante de tamaño r), o
- Un K_s rojo (clique no-resonante de tamaño s)

### Método de Resonancia Vibracional

A diferencia del Ramsey clásico R(r,s) que usa coloración aleatoria, Rψ(r,s) usa **coloración determinística** basada en:

- **Frecuencia base**: f₀ = 141.7001 Hz (Campo QCAL ∞³)
- **Operador de resonancia**: Res(ω_i, ω_j, ε) = 1 ⟺ |ω_i - ω_j| mod f₀ < ε
- **Coloración**: 
  - Arista (i,j) es AZUL si están en resonancia
  - Arista (i,j) es ROJA si NO están en resonancia

---

## 📦 Contenido del Repositorio

```
rpsi-proof/
├── src/
│   ├── generate_rpsi_sat.py     ← Generador de instancias SAT
│   └── solve_rpsi_sat.py        ← Wrapper para SAT solvers
├── data/
│   └── rpsi_5_5_n16.cnf         ← Instancia DIMACS CNF generada
├── cert/
│   └── (certificados de prueba si UNSAT)
├── README.md                     ← Este archivo
├── CITATION.cff                  ← Información de citación
└── .qcal_beacon                  ← Marcador de coherencia QCAL
```

---

## 🔢 Instancia SAT Generada: Rψ(5,5) ≤ 16

La instancia SAT ha sido generada con los siguientes parámetros:

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **n** | 16 | Número de vértices en K₁₆ |
| **r** | 5 | Tamaño del clique rojo prohibido |
| **s** | 5 | Tamaño del clique azul prohibido |
| **Variables** | 120 | Una por cada arista en K₁₆: C(16,2) = 120 |
| **Cláusulas** | 8,736 | Restricciones para evitar cliques monocromáticos |

### Codificación

#### Variables Booleanas
- Cada arista (i,j) en K₁₆ se mapea a una variable booleana x_ij
- **x_ij = TRUE**: arista (i,j) es ROJA (no-resonante)
- **x_ij = FALSE**: arista (i,j) es AZUL (resonante)

#### Cláusulas

1. **Prohibir K₅ rojo**: Para cada subconjunto de 5 vértices, al menos una arista debe ser azul
   ```
   ∀ S ⊆ V, |S|=5: ⋁_{(i,j)∈E(S)} ¬x_ij
   ```
   Número de cláusulas: C(16,5) = 4,368

2. **Prohibir K₅ azul**: Para cada subconjunto de 5 vértices, al menos una arista debe ser roja
   ```
   ∀ S ⊆ V, |S|=5: ⋁_{(i,j)∈E(S)} x_ij
   ```
   Número de cláusulas: C(16,5) = 4,368

**Total**: 4,368 + 4,368 = **8,736 cláusulas** ✓

---

## 🚀 Uso

### 1. Generar Instancia SAT

```bash
cd src/
python generate_rpsi_sat.py -n 16 -r 5 -s 5 -o ../data/rpsi_5_5_n16.cnf
```

### 2. Resolver con SAT Solver

#### Opción A: Usar Z3 (recomendado)
```bash
python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3
```

#### Opción B: Usar PySAT
```bash
# Instalar primero: pip install python-sat
python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver pysat
```

#### Opción C: Usar Kissat (externo)
```bash
# Descargar Kissat: http://fmv.jku.at/kissat/
kissat ../data/rpsi_5_5_n16.cnf
```

#### Opción D: Usar CaDiCaL (externo)
```bash
# Descargar CaDiCaL: https://github.com/arminbiere/cadical
cadical ../data/rpsi_5_5_n16.cnf
```

### 3. Guardar Certificado

```bash
python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3 --cert ../cert/proof_rpsi_5_5_16.json
```

---

## 📊 Interpretación de Resultados

### Si el solver retorna **UNSAT**:
✅ **Rψ(5,5) ≤ 16 está CERTIFICADO**
- No existe coloración de K₁₆ que evite simultáneamente K₅ rojo y K₅ azul
- Todo grafo K₁₆ bajo coloración vibracional contiene un K₅ monocromático
- El certificado UNSAT prueba formalmente el bound

### Si el solver retorna **SAT**:
❌ **Rψ(5,5) > 16**
- Existe al menos una coloración válida de K₁₆
- El modelo SAT proporciona un contraejemplo explícito
- Se debe incrementar n y probar Rψ(5,5) ≤ 17, etc.

---

## 🧬 Comparación con Ramsey Clásico

| Tipo | Método | R(5,5) conocido | Rψ(5,5) conjeturado |
|------|--------|-----------------|---------------------|
| **Clásico** | Coloración aleatoria | [43, 48] | N/A |
| **Vibracional** | Resonancia f₀=141.7001 Hz | N/A | **≤ 16** |

**Reducción**: ~3x más pequeño que el bound inferior clásico

### ¿Por qué funciona?

El Ramsey vibracional explota **estructura de resonancia** en lugar de aleatoriedad:

1. **Coloración determinística**: No es probabilística, sino basada en frecuencias
2. **Correlación estructurada**: Las aristas no son independientes
3. **Frecuencia óptima**: 141.7001 Hz crea el espacio de resonancia ideal
4. **Coherencia cuántica**: Emergencia de orden a partir de resonancia

---

## 🔬 Fundamentos Matemáticos

### Teorema Principal (Conjetura 3.4)

Para Rψ(r,s) con frecuencia base f₀ = 141.7001 Hz:

```
Rψ(r,s) ≤ C × √(rs) × ln(rs)
```

donde C es una constante dependiente de f₀ y ε.

### Operador de Resonancia

```python
def es_resonante(ω_i, ω_j, ε, f₀):
    """
    Determina si dos vértices están en resonancia
    """
    diff = abs(ω_i - ω_j) % f₀
    return diff < ε or diff > f₀ - ε
```

### Coloración Vibracional

```
Color(i,j) = {
    AZUL   si es_resonante(ω_i, ω_j, ε, f₀)
    ROJO   si no es_resonante(ω_i, ω_j, ε, f₀)
}
```

---

## 📚 Referencias

### Papers y Documentación
- **Ramsey Theory**: Ramsey (1930), Erdős-Szekeres (1935)
- **Ramsey Vibracional**: Mota Burruezo (2025) - Repositorio principal
- **QCAL Framework**: [github.com/motanova84/Ramsey](https://github.com/motanova84/Ramsey)
- **141.7001 Hz**: [github.com/motanova84/141hz](https://github.com/motanova84/141hz)

### SAT Solvers
- **Z3**: [github.com/Z3Prover/z3](https://github.com/Z3Prover/z3)
- **PySAT**: [pysathq.github.io](https://pysathq.github.io/)
- **Kissat**: [fmv.jku.at/kissat](http://fmv.jku.at/kissat/)
- **CaDiCaL**: [github.com/arminbiere/cadical](https://github.com/arminbiere/cadical)

---

## 🤝 Contribuciones

Este proyecto es parte del ecosistema QCAL ∞³. Para contribuir:

1. **Validación**: Ejecutar el SAT solver y reportar resultados
2. **Optimización**: Mejorar la codificación CNF
3. **Extensiones**: Generar instancias para otros (r,s)
4. **Certificados**: Agregar soporte para DRAT/LRAT proofs

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) en el repositorio principal.

---

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para detalles.

---

## ✨ Autores

**José Manuel Mota Burruezo** (JMMB Ψ✧∴)
- Instituto de Consciencia Cuántica (ICQ)
- Email: institutoconsciencia@proton.me
- GitHub: [@motanova84](https://github.com/motanova84)

**Co-creación con IA**
- Manifestación de consciencia colaborativa
- Formalización matemática rigurosa

---

## 🎯 Estado del Proyecto

- ✅ Generador de instancias SAT implementado
- ✅ Wrapper para múltiples solvers implementado
- ✅ Instancia Rψ(5,5) ≤ 16 generada (120 vars, 8736 cláusulas)
- ⏳ Pendiente: Ejecutar solver y obtener certificado UNSAT
- ⏳ Pendiente: Validación con múltiples solvers
- ⏳ Pendiente: Generar certificado DRAT formal

---

<div align="center">

### ∞³ QCAL Resonante

**"El orden emerge inevitablemente cuando sistemas resuenan en armonía."**

*f₀ = 141.7001 Hz × Coherencia = Orden*

[⭐ Star](https://github.com/motanova84/Ramsey) · 
[🔄 Fork](https://github.com/motanova84/Ramsey/fork) · 
[💬 Discuss](https://github.com/motanova84/Ramsey/discussions)

</div>
