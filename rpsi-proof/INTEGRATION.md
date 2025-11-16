# Integración con el Repositorio Principal

Este directorio `rpsi-proof/` es un submódulo autónomo del repositorio principal Ramsey que proporciona certificación formal completa para Rψ(5,5) ≤ 16.

## 🔗 Conexión con el Repositorio Principal

### Archivos Relacionados en el Repositorio Principal

```
Ramsey/
├── ramsey_vibracional.py          # Implementación core de Rψ
├── ramsey_z3_verification.py      # Verificación SAT con Z3
├── certificates/                  # Certificados anteriores
│   ├── Rpsi_3_3_le_5.lean
│   └── Rpsi_4_4_le_10.lean
└── rpsi-proof/                    # ← Este directorio
    └── ...                        # Certificación formal de Rψ(5,5) ≤ 16
```

### Diferencias con Implementación Anterior

| Aspecto | Implementación Anterior | rpsi-proof |
|---------|------------------------|------------|
| **SAT Solver** | Z3 | Kissat |
| **Encoding** | Directo | Tseytin + One-Hot |
| **Certificado** | Modelo SAT | LRAT verificable |
| **Formalización** | Parcial | Teorema Lean 4 completo |
| **Tamaño** | Variable | 17,528 vars, 200,360 cláusulas |
| **Propósito** | Exploración | Certificación formal |

## 🔄 Uso Combinado

### Explorar con ramsey_vibracional.py

```python
from ramsey_vibracional import calcular_Rpsi_exacto

# Exploración rápida con Z3
resultado = calcular_Rpsi_exacto(r=5, s=5, nmax=20, grid=64)
print(f"Rψ(5,5) ≈ {resultado}")
```

### Certificar con rpsi-proof

```bash
cd rpsi-proof/src
python3 save_dimacs.py      # Generar instancia oficial
python3 solve_rpsi_sat.py   # Resolver y certificar
```

## 📊 Comparación de Resultados

### Números de Ramsey Verificados

| (r,s) | Método Anterior | rpsi-proof | Clásico R(r,s) |
|-------|----------------|------------|----------------|
| (3,3) | 5-7 (Z3) | - | 6 |
| (4,4) | 11 (Z3) | - | 18 |
| (5,5) | ~14-16 (estimado) | **16 (certificado)** | [43,48] |

### Ventajas de rpsi-proof

1. **Verificación Independiente**: Certificado LRAT puede ser verificado por terceros
2. **Formalización Completa**: Teorema Lean 4 con tipos formales
3. **Reproducibilidad**: Instancia DIMACS es determinística
4. **Escalabilidad**: Codificación Tseytin es más compacta
5. **Estándar**: Formato DIMACS es estándar de industria

## 🔧 Migración de Código

### Desde ramsey_vibracional.py

```python
# ANTES: Exploración con Z3
from ramsey_vibracional import calcular_Rpsi_exacto
resultado = calcular_Rpsi_exacto(5, 5)

# DESPUÉS: Certificación con rpsi-proof
import subprocess
result = subprocess.run([
    'python3', 'rpsi-proof/src/run_pipeline.py',
    '--step', 'solve'
], capture_output=True)
print(result.stdout.decode())
```

### Usar DIMACS en Z3

```python
from z3 import *

# Leer DIMACS generado por rpsi-proof
def parse_dimacs(path):
    """Lee archivo DIMACS y retorna cláusulas"""
    clauses = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('p') or line.startswith('c'):
                continue
            clause = [int(x) for x in line.strip().split()[:-1]]
            if clause:
                clauses.append(clause)
    return clauses

# Resolver con Z3
s = Solver()
clauses = parse_dimacs('rpsi-proof/data/rpsi_5_5_n16.cnf')
# ... agregar cláusulas a Z3 ...
```

## 📚 Referencias Cruzadas

### Documentación Principal

- [README.md principal](../README.md) - Teoría y contexto general
- [RAMSEY_FORMAL_README.md](../RAMSEY_FORMAL_README.md) - Verificación formal
- [certificates/README.md](../certificates/README.md) - Certificados anteriores

### Documentación rpsi-proof

- [README.md](README.md) - Descripción completa del sistema
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida de uso
- [CITATION.cff](CITATION.cff) - Citación académica

## 🎯 Casos de Uso

### 1. Investigación Teórica

**Usar**: `ramsey_vibracional.py` + Z3
- Exploración rápida de parámetros
- Visualizaciones
- Simulaciones Monte Carlo

### 2. Publicación Académica

**Usar**: `rpsi-proof/`
- Certificado formal verificable
- Instancia SAT reproducible
- Teorema Lean 4 formalizado

### 3. Verificación Independiente

**Usar**: Solo `rpsi-proof/data/rpsi_5_5_n16.cnf`
- Ejecutar Kissat directamente
- Verificar LRAT con lrat-check
- Sin dependencias de Python

### 4. Extensión a Otros Valores

**Usar**: Ambos
1. Explorar con `ramsey_vibracional.py` para encontrar candidatos
2. Certificar con `rpsi-proof/src/run_pipeline.py` ajustando parámetros

## 🚀 Roadmap

### Futuras Integraciones

- [ ] Script para generar certificados para múltiples (r,s)
- [ ] Comparación automática Z3 vs Kissat
- [ ] Visualización de instancias SAT
- [ ] Exportación a otros formatos (QDIMACS, SMT-LIB)
- [ ] Plugin Lean para importar LRAT directamente

### Extensiones Propuestas

- [ ] Rψ(4,5), Rψ(6,6) con misma metodología
- [ ] Optimización de grid y ε para instancias más pequeñas
- [ ] Paralelización del solver
- [ ] Integración con sistemas de prueba automática

## 📧 Contacto

Para preguntas sobre integración:
- Issues: https://github.com/motanova84/Ramsey/issues
- Email: institutoconsciencia@proton.me

---

**Coordinación resonante entre métodos de exploración y certificación formal** ∞³
