# Z3 Verification Examples

This directory contains example scripts demonstrating the Z3-based verification system for vibrational Ramsey numbers.

## Examples

### 1. Basic Usage (`example_basic.py`)

Demonstrates fundamental verification operations:
- Basic SAT/UNSAT checks
- Calculating exact R_psi values
- Epsilon sensitivity analysis

**Run:**
```bash
python example_basic.py
```

**Time:** ~1-2 minutes

### 2. Parameter Explorer (`example_explorer.py`)

Shows how to use the automatic parameter explorer:
- Small parameter space exploration
- Epsilon range scanning
- Systematic (r,s) combinations
- Results export to CSV

**Run:**
```bash
python example_explorer.py
```

**Time:** ~2-5 minutes (depending on selected example)

### 3. Visualization (`example_visualization.py`)

Generates visualizations from exploration results:
- Heatmaps of R_psi values
- Epsilon sensitivity plots
- Computation time analysis

**Run:**
```bash
# First run explorer to generate data
python example_explorer.py

# Then generate visualizations
python example_visualization.py
```

**Time:** ~1 minute

## Quick Start

Run all basic examples:

```bash
cd examples_z3
python example_basic.py
```

For a complete workflow:

```bash
# 1. Explore parameters
python example_explorer.py

# 2. Generate visualizations
python example_visualization.py

# 3. Check output files
ls -l *.csv *.png
```

## Output Files

After running the examples, you'll find:

- `results_*.csv`: Computed R_psi values in CSV format
- `*.png`: Visualization plots (if matplotlib is installed)
- Console output with detailed computation logs

## Customization

### Modify Parameters

Edit the example files to test your own parameter ranges:

```python
results = explore_parameters(
    r_values=[3, 4, 5],      # Your r values
    s_values=[3, 4, 5],      # Your s values
    eps_values=[0.2, 0.3],   # Your epsilon values
    M=1000,                  # Modular base
    nmax=20                  # Maximum n to test
)
```

### Add Custom Examples

Create your own example script:

```python
import sys
sys.path.insert(0, '..')

from ramsey_z3_verification import calculate_ramsey_vibrational

# Your custom exploration code
result = calculate_ramsey_vibrational(r=5, s=5, eps=0.2, nmax=25)
print(f"R_psi(5,5,0.2) = {result}")
```

## Performance Tips

1. **Start small**: Use `nmax=12` for initial tests
2. **Parallel processing**: Run multiple parameter sets separately
3. **Save intermediate results**: Use CSV export to avoid recomputation
4. **Monitor memory**: Large r,s values require significant RAM

## Troubleshooting

### Z3 takes too long

- Reduce `nmax` parameter
- Test smaller r,s values first
- Use larger epsilon values (computations are faster)

### Out of memory

- Reduce the number of parameter combinations
- Run examples sequentially instead of all at once
- Close other applications

### No visualizations

- Install matplotlib: `pip install matplotlib`
- Check that CSV files were generated
- Verify image files are created in current directory

## Next Steps

After running these examples:

1. **Analyze results**: Open CSV files in Excel or pandas
2. **Compare with theory**: Check against known Ramsey numbers
3. **Extend exploration**: Add more parameter combinations
4. **Formalize proofs**: Use results to guide formal verification

## References

- Main documentation: `../RAMSEY_Z3_README.md`
- Core implementation: `../ramsey_z3_verification.py`
- Visualization: `../ramsey_visualization.py`
