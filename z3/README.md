# Z3 Vibrational Ramsey Verifier

This module provides a Z3-based formal verification tool for Vibrational Ramsey Theory.

## Overview

The verifier uses the Z3 SMT solver to formally verify properties of vibrational Ramsey numbers Rψ(r,s,ε). It checks whether for a given graph with `n = r + s - 1` vertices, it's possible to assign frequencies to vertices such that both a red clique of size r and a blue clique of size s can be avoided.

## Usage

### Command Line

```bash
python z3/ramsey_verifier.py --r 3 --s 3 --eps 0.2
```

### Arguments

- `--r`: Red clique size (required)
- `--s`: Blue clique size (required)
- `--M`: Discretization parameter (default: 1000, currently not used)
- `--eps`: Resonance threshold (default: 0.2)

### Example Output

```
Result: Rψ(3,3,0.2) > 5? NO
```

This means that for ε=0.2, we cannot avoid both cliques with 5 vertices, so Rψ(3,3,0.2) ≤ 5.

## How It Works

1. Creates n = r + s - 1 vertices with real-valued frequency assignments in [0, 1)
2. Defines edges as "red" if their frequency difference is less than ε or greater than 1-ε (resonance)
3. Adds constraints to avoid:
   - Any complete red clique of size r
   - Any complete blue (non-red) clique of size s
4. Checks satisfiability:
   - **SAT**: A counterexample exists → Rψ(r,s,ε) > n → Output: YES
   - **UNSAT**: No counterexample → Rψ(r,s,ε) ≤ n → Output: NO

## Examples

```bash
# Test different parameter combinations
python z3/ramsey_verifier.py --r 3 --s 3 --eps 0.2
# Output: Result: Rψ(3,3,0.2) > 5? NO

python z3/ramsey_verifier.py --r 3 --s 3 --eps 0.3
# Output: Result: Rψ(3,3,0.3) > 5? YES

python z3/ramsey_verifier.py --r 4 --s 4 --eps 0.2
# Output: Result: Rψ(4,4,0.2) > 7? YES

python z3/ramsey_verifier.py --r 3 --s 4 --eps 0.2
# Output: Result: Rψ(3,4,0.2) > 6? YES
```

## Theory

In Vibrational Ramsey Theory, edges are colored based on frequency resonance:
- **Red edge**: |ω_i - ω_j| < ε or |ω_i - ω_j| > 1 - ε (frequencies are resonant)
- **Blue edge**: Otherwise (frequencies are not resonant)

The Ramsey number Rψ(r,s,ε) is the smallest n such that any frequency assignment to n vertices must contain either a red clique of size r or a blue clique of size s.

## Testing

Tests are located in `tests/test_z3_verifier.py`. Run them with:

```bash
python -m unittest tests.test_z3_verifier -v
```

## Dependencies

- z3-solver >= 4.12.0
- Python 3.8+
