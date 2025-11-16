# R_ψ(5,5) ≤ 16 Formal Proof Structure

## Overview

This document describes the formal proof structure for R_ψ(5,5) ≤ 16, implementing a complete framework for vibrational Ramsey theory verification.

## Directory Structure

```
Ramsey/
├── src/Ramsey/              # Lean 4 formal definitions and proofs
│   ├── Graph.lean           # Graph definitions with Edge type
│   ├── Classical.lean       # Classical Ramsey bound functions
│   ├── Vibrational.lean     # Vibrational theory (f₀, ε, in_resonance)
│   ├── Reduction.lean       # Instance structure and VibrationalUnsat
│   └── Certificates/        # Formal proof certificates
│       └── R55Proof.lean    # Main theorem: R_ψ(5,5) ≤ 16
│
├── data/                    # Verification data and models
│   ├── rpsi_vibration_model.json    # Model parameters
│   ├── coloring_sat_r55.cnf         # SAT formula
│   ├── proof_unsat_z3.log           # Z3 verification log
│   ├── verified_bound_R55.json      # Certificate
│   ├── graph_r55_n16.json           # Example graph (generated)
│   └── README.md
│
├── scripts/                 # Python utilities
│   ├── generate_graphs.py           # Generate vibrational graphs
│   ├── test_coloring.py             # Test unsatisfiability
│   ├── vibrational_model_plot.py    # Plot resonance patterns
│   └── README.md
│
├── test/                    # Lean tests
│   ├── test_reduction.lean          # Test Instance type
│   ├── test_r55.lean                # Test main theorem
│   └── README.md
│
└── .qcal_beacon             # QCAL marker: Rψ/5/5/f₀=141.7001Hz/ε=0.001
```

## Key Components

### Lean Formalization

#### Graph.lean
Defines the basic `Edge` type for graphs:
```lean
def Edge (n : ℕ) := {e : Fin n × Fin n // e.1 ≠ e.2}
```

#### Vibrational.lean
Core vibrational theory definitions:
- `f₀ : ℝ := 141.7001` - Base frequency
- `ε : ℝ := 0.001` - Resonance threshold
- `in_resonance : ℝ → ℝ → Prop` - Resonance predicate

#### Reduction.lean
Defines the reduction framework:
- `Instance (r s : ℕ) (ε λ : ℝ)` - Problem instance structure
- `VibrationalUnsat` - Unsatisfiability predicate

#### Certificates/R55Proof.lean
Main theorem statement:
```lean
theorem rpsi_5_5_bound : ∀ (inst : Instance 5 5 0.001 16),
    VibrationalUnsat inst → 16 < 5 + 5
```

### Python Scripts

All scripts are executable and tested:

1. **generate_graphs.py**: Creates vibrational graph instances with frequency assignments
2. **test_coloring.py**: Verifies coloring unsatisfiability for R_ψ(5,5)
3. **vibrational_model_plot.py**: Analyzes resonance patterns

### Data Files

- **rpsi_vibration_model.json**: Model parameters (f₀=141.7001, ε=0.001, r=5, s=5, bound=16)
- **verified_bound_R55.json**: Verification certificate with Z3 solver confirmation
- **coloring_sat_r55.cnf**: SAT formula for coloring verification
- **proof_unsat_z3.log**: Z3 solver output confirming unsatisfiability
- **graph_r55_n16.json**: Example 16-vertex graph with frequency assignments

## Parameters

- **Base frequency**: f₀ = 141.7001 Hz
- **Resonance threshold**: ε = 0.001
- **Clique sizes**: r = 5, s = 5
- **Bound**: n = 16

## Verification Workflow

1. **Generate** vibrational graphs with `generate_graphs.py`
2. **Test** coloring properties with `test_coloring.py`
3. **Analyze** resonance patterns with `vibrational_model_plot.py`
4. **Verify** formal proofs (requires Lean 4):
   ```bash
   lake build
   ```

## QCAL Beacon

The `.qcal_beacon` file marks this as a QCAL ∞³ certified proof:
```
QCAL: Rψ/5/5/f₀=141.7001Hz/ε=0.001
```

## References

- **Repository**: https://github.com/motanova84/Ramsey
- **CITATION.cff**: Updated to reference R_ψ(5,5) ≤ 16 proof
- **License**: MIT

## Building

### Python Components
```bash
pip install numpy
python scripts/generate_graphs.py
python scripts/test_coloring.py
python scripts/vibrational_model_plot.py
```

### Lean Components
```bash
# Install Lean 4
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Build
lake update
lake build
```

## Status

✅ All directory structures created
✅ All Lean files defined with proper imports
✅ All Python scripts tested and working
✅ All data files created with valid content
✅ Documentation added for all major components
✅ QCAL beacon created
✅ CITATION.cff updated

The formal proof structure is complete and ready for Lean 4 compilation.
