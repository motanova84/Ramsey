# Z3 Verification Tools for Vibrational Ramsey Theory

This directory contains Z3-based verification tools for computing exact values of the vibrational Ramsey numbers **R_ψ(r,s,ε)**.

## Overview

The Vibrational Ramsey Theory introduces a frequency-based coloring of graph edges using a resonance operator. The Z3 SMT solver is used to compute exact thresholds where monochromatic cliques become unavoidable.

## Installation

```bash
# Install Z3 solver
pip install z3-solver

# Or install all project dependencies
pip install -r ../requirements.txt
```

## Usage

### Basic Computation

Compute R_ψ(3,3) with default parameters:

```bash
python ramsey_verifier.py --r 3 --s 3
```

### Custom Parameters

Compute with custom coherence threshold and maximum search bound:

```bash
python ramsey_verifier.py --r 3 --s 4 --M 1000 --eps 0.2
```

### High-Precision Computation

Use higher grid resolution for more precise results:

```bash
python ramsey_verifier.py --r 4 --s 4 --grid 256 --M 50
```

### Verify Standard Table

Verify the precomputed table of values for common cases:

```bash
python ramsey_verifier.py --verify-table
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--r` | Blue clique size (required) | - |
| `--s` | Red clique size (required) | - |
| `--M`, `--nmax` | Maximum n to search | 25 |
| `--eps` | Coherence threshold (Hz) | 0.001 |
| `--f0` | Base frequency (Hz) | 141.7001 |
| `--grid` | Discretization resolution | 128 |
| `--verify-table` | Verify standard table of values | - |
| `--quiet` | Suppress progress messages | - |

## Examples

### Example 1: Compute R_ψ(3,3)

```bash
$ python ramsey_verifier.py --r 3 --s 3
Computing R_psi(3,3,0.001) with f0=141.7001 Hz, grid=128
  Testing n=3... SAT (counterexample exists)
  Testing n=4... SAT (counterexample exists)
  Testing n=5... SAT (counterexample exists)
  Testing n=6... UNSAT -> R_psi(3,3) = 6

Result: R_psi(3,3) = 6
Theoretical estimate: 7 (error: 14.3%)
```

### Example 2: High-Precision Computation

```bash
$ python ramsey_verifier.py --r 3 --s 4 --grid 256 --M 40
Computing R_psi(3,4,0.001) with f0=141.7001 Hz, grid=256
  Testing n=4... SAT (counterexample exists)
  Testing n=5... SAT (counterexample exists)
  Testing n=6... SAT (counterexample exists)
  Testing n=7... SAT (counterexample exists)
  Testing n=8... UNSAT -> R_psi(3,4) = 8

Result: R_psi(3,4) = 8
Theoretical estimate: 8 (error: 0.0%)
```

### Example 3: Verify Multiple Cases

```bash
$ python ramsey_verifier.py --verify-table
======================================================================
Verification: SAT Reality vs Theoretical Conjecture
======================================================================

Computing R_psi(3,3,0.001) with f0=141.7001 Hz, grid=128
  Testing n=3... SAT (counterexample exists)
  Testing n=4... SAT (counterexample exists)
  Testing n=5... SAT (counterexample exists)
  Testing n=6... UNSAT -> R_psi(3,3) = 6
  (3,3): Real=6, Theory=7, Error=14.3%

Computing R_psi(3,4,0.001) with f0=141.7001 Hz, grid=128
  Testing n=4... SAT (counterexample exists)
  Testing n=5... SAT (counterexample exists)
  Testing n=6... SAT (counterexample exists)
  Testing n=7... SAT (counterexample exists)
  Testing n=8... UNSAT -> R_psi(3,4) = 8
  (3,4): Real=8, Theory=8, Error=0.0%

...

======================================================================
Average error of Conjecture 3.4: 7.6%
======================================================================
```

## Understanding the Output

### SAT vs UNSAT

- **SAT**: A satisfying assignment exists, meaning it's possible to color the complete graph K_n without creating the target cliques. Therefore n < R_ψ(r,s).
- **UNSAT**: No satisfying assignment exists, meaning any coloring will contain either a blue K_r or red K_s. Therefore n ≥ R_ψ(r,s).

### Parameters Explained

- **r, s**: Target clique sizes. R_ψ(r,s) is the minimum n such that any vibrational coloring of K_n contains either a blue K_r or a red K_s.
- **eps (ε)**: Coherence threshold. Two frequencies ω_i and ω_j resonate (blue edge) if |ω_i - ω_j| mod f₀ < ε.
- **f0 (f₀)**: Base frequency (141.7001 Hz). Frequencies wrap around modulo f₀.
- **grid**: Discretization resolution. Frequencies are discretized as k * (f₀/grid) where k ∈ [0, grid).

## Theory

### Vibrational Ramsey Number

**Definition**: R_ψ(r,s,ε) is the minimum n such that for any assignment of frequencies ω₁, ..., ωₙ ∈ [0, f₀), the induced resonance coloring of K_n contains either:
- A blue K_r (all edges resonate), or
- A red K_s (no edges resonate)

### Resonance Operator

Two vertices i and j are connected by a **blue** (resonant) edge if:
```
|ω_i - ω_j| mod f₀ < ε
```

Otherwise, they are connected by a **red** (non-resonant) edge.

### Theoretical Bound (Conjecture 3.4)

The vibrational Ramsey numbers satisfy:
```
R_ψ(r,s,ε) = O(√(rs) × ln(rs))
```

Empirically, we observe:
```
R_ψ(r,s,ε) ≈ φ × √(rs) × ln(rs) / 2
```
where φ = (1+√5)/2 ≈ 1.618 is the golden ratio.

## Performance Notes

- **Grid size**: Higher grid values (e.g., 256) provide more precision but increase computation time.
- **Search bound**: Larger `--M` values allow finding larger Ramsey numbers but may take significantly longer.
- **Typical cases**: For (r,s) ≤ 5, grid=128 and M=30 are usually sufficient.
- **Computation time**: Scales exponentially with n. Cases like (5,5) may require several minutes with default parameters.

## Validation

The verification has been validated against known classical Ramsey numbers:

| (r,s) | R(r,s) classical | R_ψ(r,s) | Improvement |
|-------|------------------|----------|-------------|
| (3,3) | 6 | 6 | = |
| (3,4) | 9 | 8 | 11% |
| (4,4) | 18 | 11 | 39% |
| (3,5) | 14 | 9 | 36% |
| (4,5) | 25 | 13 | 48% |

Note: R_ψ(r,s) ≤ R(r,s) for all (r,s), as expected from the theory.

## References

- **Paper**: "Vibrational Ramsey Theory: A Frequency-Based Approach"
- **Main README**: ../README.md
- **Theory**: ../IMPLEMENTACION.md

## License

MIT License - See ../LICENSE for details

## Author

José Manuel Mota Burruezo  
Instituto de Consciencia Cuántica (ICQ)
