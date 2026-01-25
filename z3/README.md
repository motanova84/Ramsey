# Vibrational Ramsey Z3 Verifier (Rψ)

Este módulo implementa un verificador formal basado en Z3 para números de Ramsey vibracionales:

Rψ(r, s, ε)

Donde:
- Se asignan frecuencias reales ω_i ∈ [0,1)
- Los bordes se colorean según condición de resonancia:
  |ω_i - ω_j| < ε  → borde rojo  
  |ω_i - ω_j| ≥ ε → borde azul  

El verificador determina:

- SAT → Existe coloración sin K_r roja ni K_s azul → Rψ > n  
- UNSAT → Toda coloración induce una camarilla → Rψ ≤ n

Uso:

```bash
python z3/ramsey_verifier.py --r 3 --s 3 --eps 0.2
```

Resultados típicos:

Rψ(3,3,0.2) > 5? → NO

Rψ(4,4,0.2) > 7? → SÍ (SAT)
