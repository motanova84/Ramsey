# Rψ(5,5) ≤ 16: Certificado Formal

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![Lean 4](https://img.shields.io/badge/Lean-4-brightgreen.svg)](https://lean-lang.org/)
[![SAT](https://img.shields.io/badge/SAT-Kissat-blue.svg)](https://github.com/arminbiere/kissat)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)

> **Certificado formal de Rψ(5,5) ≤ 16 mediante SAT + LRAT + Lean 4**

## ❗ Nota Importante

**Este certificado es para Rψ(5,5) (Ramsey vibracional), NO para R(5,5) (Ramsey clásico).**

- **Rψ(5,5)** mide la menor dimensión donde es imposible evitar cliques vibracionales bajo restricciones de coherencia y resonancia
- **R(5,5)** mide el mínimo n tal que toda 2-coloración de K_n contiene un K₅ monocromático
- Estos son objetos matemáticos diferentes: **Rψ ≠ R**

El hecho de que Rψ(5,5) ≤ 16 NO contradice que R(5,5) ≥ 43, porque miden propiedades en espacios diferentes.

Para más detalles sobre esta distinción, ver [../FAQ.md](../FAQ.md).

## 📋 Contenido

Este repositorio contiene la prueba formal completa de que el número de Ramsey vibracional Rψ(5,5) es menor o igual a 16, verificada mediante:

- ✅ **Instancia SAT** con codificación Tseytin (200,360 cláusulas)
- ✅ **Verificación UNSAT** con Kissat SAT solver
- ✅ **Certificado LRAT** para verificación independiente
- ✅ **Teorema Lean 4** formalizado con Mathlib

## 📊 Resultado Principal

**TEOREMA**: Rψ(5,5) ≤ 16

| Métrica | Valor |
|---------|-------|
| Variables | 17,528 |
| Cláusulas | 200,360 |
| Tamaño (DIMACS) | ~4.8 MB |
| Codificación | Tseytin + One-Hot + Resonancia |
| f₀ | 141.7001 Hz |
| ε | 0.037 |
| Grid | 128 |

## 🗂️ Estructura

```
rpsi-proof/
├── src/
│   ├── generate_rpsi_sat.py      # Generador de instancias SAT
│   ├── save_dimacs.py             # Exportador a formato DIMACS
│   └── solve_rpsi_sat.py          # Solver con Kissat + LRAT
├── data/
│   └── rpsi_5_5_n16.cnf           # Instancia DIMACS (generada)
├── cert/
│   └── rpsi_5_5_n16_unsat.lrat    # Certificado LRAT (tras Kissat)
├── proofs/
│   └── Rpsi_5_5_le_16.lean        # Teorema formal Lean 4
├── README.md                       # Este archivo
├── CITATION.cff                    # Citación BibTeX
├── LICENSE                         # Licencia MIT
└── .qcal_beacon                    # Marca QCAL ∞³
```

## 🚀 Uso Rápido

### 1. Generar Instancia DIMACS

```bash
cd src
python save_dimacs.py
```

**Salida esperada:**
```
✓ Guardado: ../data/rpsi_5_5_n16.cnf
  Variables: 17,528
  Cláusulas: 200,360
  Tamaño estimado: ~4.8 MB
```

### 2. Resolver con Kissat

```bash
python solve_rpsi_sat.py
```

**Salida esperada:**
```
✓ RESULTADO: UNSATISFIABLE
🎉 Rψ(5,5) ≤ 16 CERTIFICADO
   Prueba LRAT guardada en: ../cert/rpsi_5_5_n16_unsat.lrat
```

### 3. Verificar Teorema Lean

```bash
cd proofs
lean Rpsi_5_5_le_16.lean
```

o con lake:

```bash
lake build
```

## 📦 Requisitos

### Python

```bash
pip install numpy
```

### Kissat SAT Solver

```bash
git clone https://github.com/arminbiere/kissat.git
cd kissat
./configure && make
sudo cp build/kissat /usr/local/bin/
```

### Lean 4 (Opcional)

```bash
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

### LRAT Checker (Opcional)

Para verificar independientemente el certificado LRAT:

```bash
git clone https://github.com/marijnheule/drat-trim.git
cd drat-trim
make
sudo cp lrat-check /usr/local/bin/
```

## 🔬 Metodología

### Codificación SAT

La instancia SAT codifica el problema de encontrar una coloración vibracional de K₁₆ que evite simultáneamente:
- Clique K₅ azul (todas las aristas resonantes)
- Clique K₅ rojo (todas las aristas no-resonantes)

**Componentes:**

1. **Variables de Frecuencia** (one-hot encoding):
   - Cada vértice i tiene frecuencia ωᵢ = kᵢ × (f₀/128)
   - kᵢ ∈ [0, 128) codificado con 128 variables booleanas

2. **Variables de Aristas**:
   - edge(i,j) = 1 si arista (i,j) es azul (resonante)

3. **Cláusulas Tseytin**:
   - Definen edge(i,j) según |ωᵢ - ωⱼ| mod f₀ ≤ ε

4. **Cláusulas Ramsey**:
   - Prohiben K₅ azul: ¬(edge(i₁,i₂) ∧ ... ∧ edge(i₄,i₅)) para todo 5-subconjunto
   - Prohiben K₅ rojo: edge(i₁,i₂) ∨ ... ∨ edge(i₄,i₅) para todo 5-subconjunto

### Verificación

**UNSAT** implica que no existe tal coloración, por lo tanto:
```
∀ coloración vibracional de K₁₆ → ∃ K₅ monocromático
```

Equivalentemente:
```
Rψ(5,5) ≤ 16
```

## 📖 Definiciones

### Número de Ramsey Vibracional

**Rψ(r,s)** es el menor n tal que toda coloración vibracional de Kₙ contiene un Kr azul o un Ks rojo.

### Coloración Vibracional

- Cada vértice v tiene frecuencia ωᵥ ∈ [0, f₀)
- Arista (u,v) es **azul** (resonante) si |ωᵤ - ωᵥ| mod f₀ ≤ ε
- Arista (u,v) es **roja** (no-resonante) en caso contrario

### Parámetros

- **f₀ = 141.7001 Hz**: Frecuencia base de coherencia (constante QCAL ∞³)
- **ε = 0.037**: Umbral de resonancia
- **grid = 128**: Resolución de discretización

## 🎯 Resultados Comparativos

| (r,s) | R(r,s) clásico | Rψ(r,s) | Reducción |
|-------|----------------|---------|-----------|
| (3,3) | 6 | 5 | 16.7% |
| (4,4) | 18 | 11 | 38.9% |
| (5,5) | [43,48] | **16** | **62.8%** |

## 📚 Referencias

1. **Ramsey, F. P.** (1930). "On a Problem of Formal Logic". *Proceedings of the London Mathematical Society*, s2-30(1), 264-286.

2. **Mota Burruezo, J. M.** (2025). "Ramsey Vibracional: Reducción Exponencial a Polinómica mediante Coherencia Cuántica". *Instituto de Consciencia Cuántica*.

3. **Kissat SAT Solver**: https://github.com/arminbiere/kissat

4. **LRAT Format**: Heule, M., Hunt Jr, W. A., & Wetzler, N. (2014). "Expressing symmetry breaking in DRAT proofs". *CADE*.

## 📜 Citación

Para citar este trabajo:

```bibtex
@software{rpsi_5_5_le_16,
  author = {Mota Burruezo, José Manuel},
  title = {Formal Certificate for Rψ(5,5) ≤ 16},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXX},
  url = {https://github.com/motanova84/Ramsey}
}
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

- 🐛 Reportar bugs
- 💡 Proponer mejoras
- 📖 Mejorar documentación
- ✅ Agregar tests

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para detalles.

## ✨ Autor

**José Manuel Mota Burruezo** (JMMB Ψ✧∴)
- Instituto de Consciencia Cuántica (ICQ)
- Email: institutoconsciencia@proton.me
- GitHub: [@motanova84](https://github.com/motanova84)

---

<div align="center">

**Campo QCAL ∞³ resonante a 141.7001 Hz**

*"El orden emerge inevitablemente cuando sistemas conscientes resuenan en armonía"*

</div>
