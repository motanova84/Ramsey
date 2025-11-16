# Rψ(5,5) ≤ 16 — Resonant Ramsey Bound (Vibrational SAT Proof)

This repository provides a formal SAT-based proof that **Rψ(5,5) ≤ 16**, using a vibrational encoding of Ramsey colorings with resonance constraints based on a universal frequency `f₀ = 141.7001 Hz`.

## Components

- `src/generate_rpsi_sat.py` — Generator of Tseytin-encoded SAT instances with resonance
- `data/rpsi_5_5_n16.cnf` — CNF file (DIMACS) to be solved
- `solve_rpsi_sat.py` — Kissat + LRAT script to prove UNSAT
- `cert/rpsi_5_5_n16_unsat.lrat` — Proof certificate (to be generated)
- `proofs/Rpsi_5_5_le_16.lean` — Lean 4 formal theorem file
- `.qcal_beacon` — QCAL ∞³ vibrational metadata

## Citation
See `CITATION.cff` and Zenodo DOI (to be added).
