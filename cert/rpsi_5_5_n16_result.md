# Resultado SAT para R_ψ(5,5) ≤ 16

## Instancia Generada

- **Archivo**: `data/rpsi_5_5_n16.cnf`
- **Variables**: 17,528
- **Cláusulas**: 200,360
- **Método**: Codificación Tseytin con resonancia vibracional
- **Parámetros**:
  - Frecuencia base: f₀ = 141.7001 Hz
  - Umbral de resonancia: ε = 0.037
  - Grid de discretización: 128 puntos

## Resultado del Solver

**Solver**: Kissat 4.0.4  
**Tiempo de ejecución**: 0.03 segundos  
**Resultado**: **SATISFIABLE** ✓

## Interpretación

El resultado SATISFIABLE significa que:

1. **Existe** una asignación de frecuencias para 16 vértices que evita:
   - Un K₅ completamente resonante (azul)
   - Un K₅ completamente no-resonante (rojo)

2. Por lo tanto: **R_ψ(5,5) > 16**

3. El grafo encontrado por el solver es un contra-ejemplo que demuestra que n=16 es insuficiente.

## Implicaciones

La conjetura original de que R_ψ(5,5) ≤ 16 no es correcta según esta verificación SAT.

Para encontrar el valor exacto de R_ψ(5,5), sería necesario:
- Probar con n=17, 18, 19, ... hasta encontrar el primer n donde la instancia sea UNSAT
- Ese valor sería R_ψ(5,5)

## Frecuencias del Contra-ejemplo

El solver encontró una asignación satisfactoria. Las variables positivas en la salida indican:
- Variable 16764 → TRUE (frecuencia para algún vértice)
- Variable 16892 → TRUE (frecuencia para algún vértice)
- Variable 17020 → TRUE (frecuencia para algún vértice)
- Variable 17148 → TRUE (frecuencia para algún vértice)
- Variable 17276 → TRUE (frecuencia para algún vértice)
- Variable 17404 → TRUE (frecuencia para algún vértice)

Estas variables corresponden a las elecciones de frecuencia en el grid de 128 puntos para los 16 vértices.

## Próximos Pasos

1. Generar instancias para n=17, 18, 19, etc.
2. Ejecutar Kissat hasta encontrar UNSAT
3. Ese n será el valor correcto de R_ψ(5,5) con estos parámetros
