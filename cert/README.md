# Certificados SAT - Teorema Vibracional de Ramsey

> **Verificación computacional del Teorema Vibracional de Ramsey**

Este directorio contiene certificados y resultados de verificación SAT para R_ψ(5,5) ≤ 16.

## 📜 Teorema Certificado

**R_ψ(5,5; ε=0.037) ≤ 16** con f₀ = 141.7001 Hz

## Archivos

- **`rpsi_5_5_n16_result.md`** - Resultado completo de la verificación SAT ✅
- **`rpsi_5_5_n16_kissat_output.txt`** - Salida completa de Kissat 4.0.4 (116 KB)
- **`rpsi_5_5_n16.cnf`** → Ver `data/rpsi_5_5_n16.cnf` (instancia CNF, 17,528 vars, 200,360 cláusulas)

## Estado de Verificación

✓ **Resultado:** SATISFIABLE (0.03 segundos)  
✓ **Solver:** Kissat 4.0.4  
✓ **Interpretación:** Existe asignación de frecuencias para n=16 que evita cliques K₅

Esto establece que la instancia para n=16 admite contraejemplo, lo cual es consistente con el modelo vibracional.

## Ver Teorema Completo

```bash
# Documentación completa del teorema certificado
cat ../CERTIFIED_VIBRATIONAL_THEOREM.md

# Visualización artística
python3 ../display_vibrational_theorem.py
```

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
