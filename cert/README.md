# Certificados SAT para R_ψ(5,5)

Este directorio contiene los resultados de la verificación SAT para R_ψ(5,5).

## Archivos

- `rpsi_5_5_n16_kissat_output.txt` - Salida completa del solver Kissat para n=16
- `rpsi_5_5_n16_result.md` - Análisis e interpretación del resultado SAT

## Resultado IMPORTANTE

**El solver Kissat encontró que la instancia para n=16 es SATISFIABLE** (exit code 10).

Esto significa:
- **SÍ existe** una asignación de frecuencias para 16 vértices que evita ambos:
  - Un K₅ completamente resonante (azul)
  - Un K₅ completamente no-resonante (rojo)
- Por lo tanto: **R_ψ(5,5) > 16**, NO R_ψ(5,5) ≤ 16

## Implicaciones

El resultado SATISFIABLE demuestra que n=16 es insuficiente. Para encontrar el valor exacto
de R_ψ(5,5), es necesario probar con n=17, 18, 19, ... hasta encontrar el primer n donde
la instancia sea UNSAT. Ese valor será R_ψ(5,5).

## Verificación

Para reproducir el resultado:

```bash
# Generar la instancia CNF
python generate_rpsi_5_5_instance.py --n=16

# Resolver con Kissat
kissat data/rpsi_5_5_n16.cnf
# Resultado esperado: exit code 10 (SATISFIABLE)
```

## Importancia

Este resultado SAT demuestra que:
- La instancia para n=16 es SATISFIABLE
- Existe una asignación de frecuencias que evita cliques monocromáticos
- Por lo tanto, R_ψ(5,5) > 16 está certificado computacionalmente

## Referencias

- [LRAT Format Specification](https://www.cs.utexas.edu/~marijn/publications/lrat.pdf)
- [Kissat Solver](https://github.com/arminbiere/kissat)
- [DRAT-trim Checker](https://github.com/marijnheule/drat-trim)
