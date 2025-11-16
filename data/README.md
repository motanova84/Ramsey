# Data Directory

This directory contains DIMACS CNF files for Ramsey resonance SAT instances.

## Files

### `rpsi_5_5_n16.cnf`
- **Theorem**: R_ψ(5,5) ≤ 16
- **Variables**: 17,528
- **Clauses**: 200,360
- **Size**: ~3.1 MB
- **Parameters**:
  - f₀ = 141.7001 Hz (universal frequency)
  - ε = 0.037 (resonance threshold)
  - grid = 128 (discretization points)
- **Encoding**: Tseytin transformation for scalability

### `rpsi_3_3_n6.cnf`
- **Theorem**: R_ψ(3,3) ≤ 6
- **Variables**: 2,703
- **Clauses**: 56,509
- **Purpose**: Testing and validation

## Format

All files use standard DIMACS CNF format:
```
c <comment lines>
p cnf <num_vars> <num_clauses>
<clause_1> 0
<clause_2> 0
...
```

## Generation

Files are generated using:
```bash
python src/generate_rpsi_sat.py <n> <r> <s>
```

Where:
- `n`: number of vertices
- `r`: size of blue (resonant) clique to avoid
- `s`: size of red (non-resonant) clique to avoid

## Solving

To verify UNSAT (proving the bound):
```bash
python src/solve_rpsi_sat.py data/rpsi_5_5_n16.cnf --n 16 --r 5 --s 5
```

## Interpretation

If the SAT solver returns:
- **UNSAT**: The bound is proven (no valid frequency assignment exists)
- **SAT**: The bound is not tight (a valid coloring exists)

For R_ψ(5,5) ≤ 16, UNSAT proves that any assignment ω: [16] → [0, f₀) must contain either a blue K₅ or red K₅.
