# Certificados de Prueba

Este directorio contiene los certificados de insatisfacibilidad (UNSAT) o satisfacibilidad (SAT) generados por los SAT solvers.

## Formato de Certificados

### JSON Certificate (`.json`)
Certificado estructurado con metadata:
```json
{
  "timestamp": "2025-11-16T...",
  "cnf_file": "../data/rpsi_5_5_n16.cnf",
  "solver": "z3",
  "status": "UNSAT",
  "time_seconds": 1234.56,
  "num_vars": 120,
  "num_clauses": 8736,
  "frequency": "141.7001 Hz",
  "field": "QCAL ∞³"
}
```

### DRAT Proof (`.drat`)
Certificado de resolución estándar SAT competition.

### LRAT Proof (`.lrat`)
Certificado de resolución con justificación de cada paso.

## Generar Certificado

```bash
cd ../src
python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3 --cert ../cert/proof_rpsi_5_5_16.json
```

## Verificar Certificado

Para verificar certificados DRAT/LRAT, usar herramientas estándar:
- `drat-trim` - DRAT verifier
- `lrat-check` - LRAT verifier

## Estado Actual

- [ ] Certificado para Rψ(5,5) ≤ 16
- [ ] Certificado para Rψ(4,4) ≤ 10
- [ ] Certificado para Rψ(3,3) ≤ 5

Los certificados se generarán cuando se ejecuten los SAT solvers sobre las instancias correspondientes.
