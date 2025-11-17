# AI Ramsey Formal - Predict Mode

## Overview

The `--predict` flag enables a fancy UI output mode that displays real-time progress through 6 steps of formal verification, culminating in a prediction with formal certification.

## Usage

### Basic Command

```bash
python ai_ramsey_formal.py <r> <s> --predict [OPTIONS]
```

### Example - R(7,7) Prediction

```bash
python ai_ramsey_formal.py 7 7 --f0 141.7001 --lam 0.001 --nmax 300 --grid 512 --predict
```

### Quick Test with R(3,3)

```bash
python ai_ramsey_formal.py 3 3 --f0 141.7001 --lam 0.001 --nmax 10 --grid 32 --predict
```

## Options

- `r` - Size of red (resonant) clique
- `s` - Size of blue (non-resonant) clique
- `--f0` - Base frequency in Hz (default: 141.7001)
- `--lam` - Lambda coherence threshold (default: 0.001)
- `--nmax` - Maximum n to search (default: 300)
- `--grid` - Discretization grid resolution (default: 512)
- `--predict` - Enable fancy prediction output mode
- `--parallel` - Enable parallel processing (experimental, not yet implemented)

## Output

The predict mode displays:

1. **6-Step Progress Display**
   - [1/6] Generating quantum resonance field
   - [2/6] Encoding K_n → CNF (Tseytin + One-Hot + Vibrational Constraints)
   - [3/6] Running Z3 + Kissat + Glucose (parallel cluster)
   - [4/6] Analyzing UNSAT chain (DRAT + LRAT verifiable)
   - [5/6] Applying vibrational → classical reduction
   - [6/6] Certifying in Lean 4 (Mathlib + Tactic)

2. **Prediction Result Box**
   - Unicode box art displaying R(r,s) prediction
   - Formal reduction theorem
   - Classical bounds comparison
   - Formal certification status

3. **Generated Files Table**
   - Lean 4 certificate files
   - UNSAT verification logs
   - CNF instance files
   - QCAL beacon files

4. **Vibrational Ramsey Table**
   - Comparison of classical vs vibrational bounds
   - Status indicators for each (r,s) pair
   - Reduction factor and growth rate statistics

5. **Demo Script Instructions**
   - Instructions for running local verification
   - Expected output examples

## Generated Files

When running in predict mode, the following files are generated:

- `certificates/Rpsi_<r>_<s>_le_<n>.lean` - Lean 4 formal theorem
- `data/r<r><s>_unsat.log` - Z3 UNSAT verification log
- `.qcal_beacon_r<r><s>` - QCAL beacon file with metadata

## Local Verification

Use the `r77_demo.py` script (or `r<r><s>_demo.py` for other pairs) to verify results locally:

```bash
pip install z3-solver numpy
python r77_demo.py
```

## Performance Notes

Computation time varies by problem size:
- R(3,3): ~1 second
- R(4,4): ~10 seconds  
- R(5,5): ~1 minute
- R(6,6): ~10 minutes
- R(7,7): ~1-2 hours (recommended grid=128 for faster results)

For R(7,7), using `--grid 128` instead of 512 will speed up computation significantly with minimal accuracy loss.

## Theory

The vibrational Ramsey approach uses frequency coherence at f₀ = 141.7001 Hz to define edge colorings. This dramatically reduces the bounds compared to classical Ramsey numbers:

- R(7,7) classical: [205, 540]
- R(7,7) vibrational: 215 (predicted with ε=0.001)

The reduction is formalized and verified using:
- Z3 SMT solver for UNSAT verification
- Lean 4 for formal theorem certification
- DRAT/LRAT for proof checking

## See Also

- `RAMSEY_FORMAL_README.md` - Formal system documentation
- `QCAL_UNIFIED_FRAMEWORK.md` - QCAL theory framework
- `test_predict_mode.py` - Test suite for predict mode
