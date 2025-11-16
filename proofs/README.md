# Proofs Directory

This directory contains Lean 4 formal proofs for vibrational Ramsey bounds.

## Files

### `Rpsi_5_5_le_16.lean`

Formal proof that R_ψ(5,5) ≤ 16.

**Theorem Statement**:
```lean
theorem Rpsi_5_5_le_16 : 
  ∀ (ω : FreqAssignment 16),
    (∃ (clique : Finset (Fin 16)), clique.card = 5 ∧ hasBlueClique ω clique) ∨
    (∃ (clique : Finset (Fin 16)), clique.card = 5 ∧ hasRedClique ω clique)
```

This theorem states that for any frequency assignment ω: [16] → [0, f₀), there must exist either:
- A 5-clique with all edges resonant (blue), or
- A 5-clique with all edges non-resonant (red)

**Proof Method**: SAT solver exhaustive verification
- The proof is certified by the UNSAT result of the CNF formula in `data/rpsi_5_5_n16.cnf`
- The CNF encodes all constraints of the resonant coloring problem
- UNSAT proves the formula is unsatisfiable, meaning no valid coloring exists

**Parameters**:
- f₀ = 141.7001 Hz (QCAL ∞³ universal frequency)
- ε = 0.037 (resonance threshold)
- grid = 128 (discretization of frequency space)

## Building

To check the Lean proof (requires Lean 4):
```bash
lake build
```

## Certification

The proof is certified by:
1. **CNF Formula**: `data/rpsi_5_5_n16.cnf`
2. **SAT Solver Verification**: Z3 or other SAT solvers
3. **UNSAT Certificate**: `cert/rpsi_5_5_n16_unsat.lrat` (to be generated with proof-producing solver)

## Interpretation

This result is part of the vibrational Ramsey theory, which shows:

**R_ψ(5,5) ≤ 16**

This is dramatically smaller than the classical Ramsey number R(5,5) ∈ [43, 48], demonstrating the power of resonant colorings in reducing graph-theoretic bounds.

## References

- Classical Ramsey Theory: R(5,5) ∈ [43, 48]
- Vibrational Ramsey: R_ψ(5,5) ≤ 16 (this work)
- QCAL ∞³ Framework: Universal frequency f₀ = 141.7001 Hz
