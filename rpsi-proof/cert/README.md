# Certificates and Validation

⚠️ **IMPORTANT CORRECTION**: This directory originally documented validation of Rψ(5,5) ≤ 16, 
but the actual SAT result shows the instance is **SATISFIABLE**, not UNSAT.

This directory contains the actual SAT solver outputs showing that n=16 is insufficient.

## Files

### Kissat Solver Outputs

- **rpsi_5_5_n16_kissat_output.txt** - Raw Kissat solver output
  - Shows **SATISFIABLE** result (exit code 10)
  - Includes solver statistics
  - Generation metadata

- **rpsi_5_5_n16_result.md** - Human-readable summary
  - Mathematical interpretation of SATISFIABLE result
  - Key statistics
  - Implications for Rψ(5,5) bound

## Verification Result

The SAT solver (Kissat) found the instance to be **SATISFIABLE** (not UNSAT).

### What SATISFIABLE Means

The SAT (satisfiable) result means:

**There EXISTS a way to assign frequencies ω₀, ω₁, ..., ω₁₅ ∈ [0, f₀)** to the 16 vertices of K₁₆ such that:

1. Every subset of 5 vertices has at least one pair that is NOT resonant (no blue K₅)
2. Every subset of 5 vertices has at least one pair that IS resonant (no red K₅)

Since both constraints CAN be satisfied simultaneously, we conclude:

> **There exists a vibrational coloring of K₁₆ with NO monochromatic K₅**

Therefore: **Rψ(5,5) > 16** (not ≤ 16 as originally claimed)

## Implications

To find the exact value of Rψ(5,5), further testing is needed:
- Test n=17, 18, 19, ... until finding the first UNSAT instance
- That value will be Rψ(5,5)
