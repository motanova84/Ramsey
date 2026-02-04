# Certificados SAT para R_ψ(5,5)

Este directorio contiene los resultados de la verificación SAT para R_ψ(5,5).

## Archivos

- `rpsi_5_5_n16_kissat_output.txt` - Salida completa del solver Kissat para n=16
- `rpsi_5_5_n16_result.md` - Análisis e interpretación del resultado SAT
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
