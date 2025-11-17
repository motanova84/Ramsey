# Certificados LRAT

Este directorio contiene certificados de insatisfacibilidad (UNSAT) en formato LRAT generados por el solver Kissat.

## Archivos

- `rpsi_5_5_n16_unsat.lrat` - Certificado LRAT para Rψ(5,5) ≤ 16

## Formato LRAT

LRAT (Literal Reverse Addition Tautology) es un formato de certificado que permite verificar formalmente la insatisfacibilidad de una fórmula CNF.

### Verificación

Para verificar un certificado LRAT:

```bash
# Usando lrat-check
lrat-check data/rpsi_5_5_n16.cnf cert/rpsi_5_5_n16_unsat.lrat

# Usando drat-trim
drat-trim data/rpsi_5_5_n16.cnf cert/rpsi_5_5_n16_unsat.lrat
```

## Generación

Los certificados se generan ejecutando:

```bash
python src/solve_rpsi_sat.py
```

Este script invoca Kissat con la opción `--lrat` que genera el certificado durante la resolución.

## Importancia

Los certificados LRAT proporcionan una prueba verificable formalmente de que:
- La fórmula SAT es UNSAT
- No existe asignación de frecuencias que evite cliques monocromáticos
- Por lo tanto, Rψ(5,5) ≤ 16 está certificado matemáticamente

## Referencias

- [LRAT Format Specification](https://www.cs.utexas.edu/~marijn/publications/lrat.pdf)
- [Kissat Solver](https://github.com/arminbiere/kissat)
- [DRAT-trim Checker](https://github.com/marijnheule/drat-trim)
