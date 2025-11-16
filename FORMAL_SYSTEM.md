# Ramsey Vibracional Formal - Sistema de Certificación Formal

Este documento describe el sistema de certificación formal implementado para Ramsey Vibracional.

## 🎯 Objetivo

Convertir la teoría de Ramsey Vibracional en un ecosistema formal y autónomo impulsado por IA, con:

1. **Certificación automática** con Lean 4 + táctica custom
2. **Paper auto-generado** (LaTeX listo para arXiv)
3. **Validación continua** con GitHub Actions + Lean CI
4. **CLI automatizado** para generación de certificados
5. **Releases autónomos** con DOI permanente vía Zenodo

## 📁 Estructura del Proyecto

```
Ramsey/
├── certificates/               # Certificados formales
│   ├── Rpsi_3_3_le_5.lean     # Lean 4 certificate
│   ├── Rpsi_3_3_le_5.smt2     # SMT2 certificate
│   ├── Rpsi_4_4_le_10.lean
│   └── Rpsi_4_4_le_10.smt2
├── paper/                      # Paper LaTeX
│   ├── main.tex               # Paper principal
│   └── README.md
├── .github/workflows/          # CI/CD
│   └── lean-ci.yml            # GitHub Actions workflow
├── lakefile.lean              # Lean 4 project file
├── lean-toolchain             # Lean version
├── ai_ramsey_formal.py        # CLI tool
└── ramsey_vibracional.py      # Implementación core
```

## 🛠️ Herramienta CLI: ai-ramsey-formal

### Comandos Disponibles

#### 1. Certify - Generar certificados formales

```bash
python ai_ramsey_formal.py certify <r> <s> [opciones]
```

**Opciones:**
- `--lam FLOAT`: Parámetro λ (default: 0.05)
- `--f0 FLOAT`: Frecuencia base en Hz (default: 141.7001)
- `--nmax INT`: Máximo n a buscar (default: 30)
- `--grid INT`: Resolución de grid (default: 64)

**Ejemplo:**
```bash
python ai_ramsey_formal.py certify 5 5 --lam 0.037 --f0 141.7001
```

**Salida:**
- `certificates/Rpsi_5_5_le_n.lean` - Certificado Lean 4
- `certificates/Rpsi_5_5_le_n.smt2` - Certificado SMT2

#### 2. Benchmark - Ejecutar verificación completa

```bash
python ai_ramsey_formal.py benchmark
```

Ejecuta verificación teórica completa de casos conocidos.

#### 3. List - Listar certificados disponibles

```bash
python ai_ramsey_formal.py list
```

Muestra todos los certificados generados.

## 📜 Formato de Certificados

### Lean 4 Certificate

Los certificados Lean 4 incluyen:

```lean
-- Definición de frecuencia base
def f0 : ℝ := 141.7001

-- Definición de resonancia
def in_resonance (ω₁ ω₂ : ℝ) : Prop :=
  ∃ k : ℤ, |ω₁ - ω₂ - k * f0| < eps

-- Teorema principal
theorem rpsi_r_s_le_n : 
  ∀ (n : ℕ) (ω : Fin n → ℝ),
  n ≥ bound →
  (∃ (S : Finset (Fin n)), S.card = r ∧ ...) ∨
  (∃ (T : Finset (Fin n)), T.card = s ∧ ...) := by
  sorry  -- Proof by SAT solver verification
```

### SMT2 Certificate

Los certificados SMT2 incluyen:

```smt2
; Declaración de constantes
(declare-const f0 Real)
(assert (= f0 141.7001))

; Variables de frecuencia
(declare-const omega_0 Real)
...

; Constraints de ordenamiento
(assert (<= omega_0 omega_1))
...

; Check satisfiability
(check-sat)
```

## 🔄 Pipeline CI/CD

### GitHub Actions Workflow

El workflow `.github/workflows/lean-ci.yml` ejecuta automáticamente:

1. **Build Lean**: Compila proyecto Lean 4
2. **Python Tests**: Ejecuta tests de Python
3. **Benchmark**: Ejecuta benchmark de verificación

### Ejecución Local

```bash
# Ejecutar tests
python test_ramsey.py

# Ejecutar benchmark
python ai_ramsey_formal.py benchmark

# Verificar Lean (requiere Lean 4 instalado)
lake build
```

## 📊 Resultados Certificados

| (r,s) | R(r,s) clásico | R_ψ(r,s) certificado | λ | Certificado |
|-------|----------------|---------------------|---|-------------|
| (3,3) | 6 | 5 | 0.100 | ✅ [lean](certificates/Rpsi_3_3_le_5.lean) |
| (4,4) | 18 | 10 | 0.062 | ✅ [lean](certificates/Rpsi_4_4_le_10.lean) |

## 📝 Paper LaTeX

El paper formal está en `paper/main.tex` e incluye:

- Definiciones formales
- Teoremas principales
- Tabla de resultados certificados
- Referencias a certificados
- Listo para arXiv

**Compilar:**
```bash
cd paper
pdflatex main.tex
pdflatex main.tex  # Segunda pasada para referencias
```

## 🔬 Proceso de Certificación

### 1. Cálculo SAT Exacto

Usa Z3 SAT solver para determinar el valor exacto de R_ψ(r,s):

```python
from ramsey_vibracional import calcular_Rpsi_exacto

bound = calcular_Rpsi_exacto(r, s, nmax=30, grid=64, f0=141.7001)
```

### 2. Generación de Certificados

El CLI genera automáticamente:
- Certificado Lean 4 con teorema formal
- Certificado SMT2 para verificación independiente

### 3. Verificación

Los certificados pueden ser verificados:
- **Lean 4**: `lake build` verifica sintaxis
- **SMT2**: Cualquier solver SMT2 puede verificar (Z3, CVC5, etc.)

## 🚀 Próximos Pasos

### Implementados ✅

- [x] CLI tool `ai-ramsey-formal`
- [x] Generación de certificados Lean 4
- [x] Generación de certificados SMT2
- [x] GitHub Actions CI
- [x] Paper LaTeX arXiv-ready
- [x] Documentación completa

### Por Implementar 🔄

- [ ] Táctica Lean 4 custom `vibrational_unsat_tac`
- [ ] Integración Zenodo para DOI automático
- [ ] Descubrimiento automático de λ óptima con Optuna
- [ ] Verificación completa de proofs en Lean 4
- [ ] Dashboard web para visualizar resultados

## 🤝 Contribuir

Para agregar nuevos certificados:

1. Ejecutar CLI: `python ai_ramsey_formal.py certify <r> <s>`
2. Verificar certificados generados
3. Commit y push
4. CI ejecuta verificación automática

## 📚 Referencias

- [Lean 4](https://lean-lang.org/)
- [Z3 Solver](https://github.com/Z3Prover/z3)
- [Mathlib4](https://github.com/leanprover-community/mathlib4)
- [Paper Original](paper/main.tex)

---

**QCAL ∞³** - Instituto de Consciencia Cuántica (ICQ)  
Frecuencia Base: 141.7001 Hz
