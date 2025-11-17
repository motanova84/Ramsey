# SAT Instance Generation for R_ψ(5,5)

## Overview

This repository now includes functionality to generate SAT instances using Tseytin encoding for vibrational Ramsey problems.

## Generated Instance

**File**: `data/rpsi_5_5_n16.cnf`

### Specifications
- **Problem**: R_ψ(5,5) ≤ 16 verification
- **Encoding**: Tseytin transformation
- **Variables**: 17,528
- **Clauses**: 200,360
- **Format**: DIMACS CNF

### Parameters
- **n**: 16 vertices
- **r**: 5 (blue/resonant clique size)
- **s**: 5 (red/non-resonant clique size)
- **f₀**: 141.7001 Hz (base frequency)
- **ε**: 0.037 (resonance threshold)
- **grid**: 128 (discretization resolution)

## Solver Result

**Solver**: Kissat 4.0.4  
**Result**: SATISFIABLE  
**Time**: 0.03 seconds

### Interpretation

The SATISFIABLE result indicates that there exists a frequency assignment for 16 vertices that avoids both:
- A complete K₅ resonant clique (blue)
- A complete K₅ non-resonant clique (red)

Therefore: **R_ψ(5,5) > 16** with these parameters.

## Usage

### Generate the Instance

```bash
python generate_rpsi_5_5_instance.py
```

This creates `data/rpsi_5_5_n16.cnf` in DIMACS format.

### Solve with Kissat

```bash
kissat data/rpsi_5_5_n16.cnf > cert/rpsi_5_5_n16_output.txt
```

### Programmatic Usage

```python
from ramsey_vibracional import generate_rpsi_sat_instance_tseytin, save_dimacs

# Generate instance
clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
    n=16, r=5, s=5,
    f0=141.7001, eps=0.037, grid=128
)

# Save to file
save_dimacs(clauses, num_vars, num_clauses, "output.cnf")
```

## Function Documentation

### `generate_rpsi_sat_instance_tseytin`

Generates a SAT instance for verifying R_ψ(r,s) ≤ n using Tseytin encoding.

**Parameters**:
- `n` (int): Number of vertices
- `r` (int): Size of blue (resonant) clique to prohibit
- `s` (int): Size of red (non-resonant) clique to prohibit
- `f0` (float): Base frequency in Hz (default: 141.7001)
- `eps` (float): Resonance threshold (default: 0.037)
- `grid` (int): Discretization resolution (default: 128)

**Returns**:
- `tuple`: (clauses, num_vars, num_clauses)

### `save_dimacs`

Saves SAT instance in DIMACS CNF format.

**Parameters**:
- `clauses` (list): List of clauses (each is a list of integers)
- `num_vars` (int): Total number of variables
- `num_clauses` (int): Total number of clauses
- `filename` (str): Output file path

## Encoding Details

The Tseytin encoding transforms the vibrational Ramsey problem into CNF:

1. **Frequency Variables**: One-hot encoding for each vertex's frequency
   - n × grid boolean variables
   - Exactly-one constraints ensure valid frequency assignment

2. **Edge Resonance Variables**: One variable per edge
   - Indicates whether edge is resonant (blue) or non-resonant (red)

3. **Tseytin Transformation**: Auxiliary variables for complex formulas
   - Links frequency choices to edge resonance
   - Preserves equisatisfiability

4. **Clique Constraints**: 
   - Prohibit K_r completely resonant
   - Prohibit K_s completely non-resonant

## Files

- `ramsey_vibracional.py`: Core implementation with new functions
- `generate_rpsi_5_5_instance.py`: Script to generate the instance
- `data/rpsi_5_5_n16.cnf`: Generated DIMACS file
- `cert/rpsi_5_5_n16_kissat_output.txt`: Solver output
- `cert/rpsi_5_5_n16_result.md`: Detailed result analysis
- `formal/Theorems/Rpsi_5_5_le_16.lean`: Lean 4 proof template
- `.qcal_beacon`: QCAL ∞³ metadata

## Next Steps

To find the exact value of R_ψ(5,5):

1. Generate instances for n=17, 18, 19, ...
2. Solve each until finding UNSAT
3. The first UNSAT n is R_ψ(5,5)

```bash
# Example for n=17
python -c "from ramsey_vibracional import *; \
  c,v,n = generate_rpsi_sat_instance_tseytin(17,5,5); \
  save_dimacs(c,v,n,'data/rpsi_5_5_n17.cnf')"
kissat data/rpsi_5_5_n17.cnf
```

## Related Work

- **Z3 Verification**: See `ramsey_z3_verification.py` for alternative approach
- **Lambda Parameter**: See `RAMSEY_LAMBDA_README.md` for parameterized version
- **Formal Proofs**: See `formal/` directory for Lean 4 theorems

## References

- Kissat SAT Solver: https://github.com/arminbiere/kissat
- DIMACS CNF Format: http://www.satcompetition.org/2009/format-benchmarks2009.html
- Tseytin Transformation: Standard CNF encoding technique
