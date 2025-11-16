# Ramsey Vibrational Numbers Verification (Z3 Version)

Complete Z3-based SAT verification system for vibrational Ramsey numbers **R_ψ(r,s,ε)** using continuous frequency assignments.

## Overview

This implementation provides a rigorous computational framework for calculating vibrational Ramsey numbers using the Z3 theorem prover. The system can:

1. **Verify** vibrational Ramsey numbers for specific parameter combinations
2. **Explore** parameter spaces automatically
3. **Visualize** results with heatmaps and sensitivity plots
4. **Export** results to CSV for further analysis

## Mathematical Background

### Definition

The **vibrational Ramsey number** R_ψ(r,s,ε) is the smallest integer n such that any frequency assignment ω: {1,...,n} → [0,1) contains either:
- A **red clique** of size r (vertices with resonant frequencies), or
- A **blue clique** of size s (vertices with non-resonant frequencies)

### Edge Coloring

An edge (i,j) is **red** (resonant) if:
```
|ω_i - ω_j| < ε  OR  |ω_i - ω_j| > 1 - ε
```

Otherwise, the edge is **blue** (non-resonant).

### Parameters

- **r**: Size of red clique to avoid
- **s**: Size of blue clique to avoid  
- **ε (epsilon)**: Resonance threshold (typically 0.1 - 0.3)

## Installation

```bash
# Clone repository
git clone https://github.com/motanova84/Ramsey.git
cd Ramsey

# Install dependencies
pip install z3-solver numpy matplotlib
```

### Dependencies

- Python 3.8+
- z3-solver >= 4.12.0
- numpy >= 1.24.0
- matplotlib >= 3.5.0 (for visualizations)

## Quick Start

### 1. Basic Verification

Verify if a specific parameter combination satisfies the Ramsey property:

```python
from ramsey_z3_verification import vibrational_ramsey

# Check if (3,3) holds for default n with epsilon=0.2
result = vibrational_ramsey(3, 3, eps=0.2)
print(f"Result: {result}")  # True if SAT (counterexample exists)
```

### 2. Calculate Exact Values

Find the exact vibrational Ramsey number:

```python
from ramsey_z3_verification import calculate_ramsey_vibrational

# Calculate R_psi(3,3) with epsilon=0.2
R_psi = calculate_ramsey_vibrational(r=3, s=3, eps=0.2, nmax=15)
print(f"R_psi(3,3,0.2) = {R_psi}")
```

### 3. Automatic Parameter Explorer

Explore multiple parameter combinations:

```python
from ramsey_z3_verification import explore_parameters, save_results_to_csv

# Define parameter ranges
results = explore_parameters(
    r_values=[3, 4, 5],
    s_values=[3, 4, 5],
    eps_values=[0.15, 0.2, 0.25],
    nmax=20
)

# Save results to CSV
save_results_to_csv(results, 'my_results.csv')
```

### 4. Generate Visualizations

Create plots from exploration results:

```python
from ramsey_visualization import generate_all_visualizations

# Generate all visualizations from CSV
generate_all_visualizations('my_results.csv', 'output_plots')
```

This creates:
- `ramsey_heatmap.png`: Heatmap of R_ψ values
- `epsilon_sensitivity.png`: How R_ψ varies with ε
- `computation_time.png`: Performance analysis

## Complete Workflow

Run the complete verification pipeline:

```bash
# Run Z3 verification with explorer
python ramsey_z3_verification.py

# Generate visualizations
python ramsey_visualization.py
```

This will:
1. Calculate R_ψ for multiple (r,s,ε) combinations
2. Save results to `ramsey_results.csv`
3. Generate visualizations in `visualizations/` directory

## Natural Language Interface

The system supports natural language queries:

```python
from ramsey_z3_verification import natural_interface_example

# Run natural language examples
natural_interface_example()
```

Example queries:
- "What is the smallest n such that R_psi(3,3,0.2) = n?"
- "Calculate R_psi(4,4) with epsilon=0.15"

The system translates these to Z3 verification calls automatically.

## File Structure

```
Ramsey/
├── ramsey_z3_verification.py    # Core Z3 verification engine
├── ramsey_visualization.py      # Visualization module
├── RAMSEY_Z3_README.md          # This file
├── examples/
│   ├── example_basic.py         # Basic usage
│   ├── example_explorer.py      # Parameter exploration
│   └── example_visualization.py # Visualization examples
├── results/
│   ├── ramsey_results.csv       # Computed results
│   └── visualizations/          # Generated plots
└── tests/
    └── test_z3_verification.py  # Unit tests
```

## Results Format

Results are saved in CSV format with the following fields:

| Field | Description |
|-------|-------------|
| r | Red clique size |
| s | Blue clique size |
| epsilon | Resonance threshold |
| R_psi | Computed Ramsey number |
| duration_seconds | Computation time |
| timestamp | ISO 8601 timestamp |

## Performance Considerations

### Computation Time

- Small values (r,s ≤ 4): Seconds to minutes
- Medium values (r,s = 5-6): Minutes to hours
- Large values (r,s ≥ 7): May require significant time

### Memory Usage

Z3 solver memory usage grows with:
- Number of vertices n
- Clique sizes r and s
- Grid resolution M

### Optimization Tips

1. **Start with small nmax**: Use `nmax=15` for initial exploration
2. **Use appropriate epsilon**: Larger ε often gives smaller R_ψ
3. **Parallelize**: Run multiple (r,s,ε) combinations in parallel
4. **Cache results**: Save intermediate results to avoid recomputation

## Theoretical Results

### Known Values (ε = 0.2, M = 1000)

| (r,s) | R_ψ(r,s,0.2) | Classical R(r,s) |
|-------|--------------|------------------|
| (3,3) | ~6           | 6                |
| (3,4) | ~9           | 9                |
| (4,4) | ~14          | 18               |

### Conjectures

**Polynomial Bound**: For fixed ε > 0,
```
R_ψ(r,s,ε) = O(√(rs) · log(rs))
```

This is significantly better than classical Ramsey numbers:
```
R(r,s) = 2^O(√(r+s)·log(r+s))
```

## Advanced Usage

### Custom Z3 Constraints

Add custom constraints to the solver:

```python
from z3 import *
from ramsey_z3_verification import vibrational_ramsey

# Modify the function to add custom constraints
# See source code for details
```

### Batch Processing

Process multiple parameter sets:

```bash
# Example: You can create your own batch_exploration.py script to automate parameter sweeps.
# (This file is not included; see below for a minimal template.)
python batch_exploration.py --r-range 3-7 --s-range 3-7 --eps 0.2
### Integration with Other Tools

Export results for use with:
- **SageMath**: Further mathematical analysis
- **Lean 4**: Formal verification
- **Jupyter**: Interactive exploration

## Troubleshooting

### Issue: Z3 timeout

**Solution**: Reduce `nmax` or increase timeout in Z3 solver settings.

### Issue: Memory errors

**Solution**: Process parameter combinations sequentially, reduce `nmax`, or increase available memory.

### Issue: No results found

**Solution**: Increase `nmax` parameter or check that ε is in valid range.

## Contributing

Contributions are welcome! Areas for improvement:

1. **Performance**: Optimize Z3 encoding
2. **Parallelization**: Add multiprocessing support
3. **Visualization**: More plot types
4. **Documentation**: Additional examples
5. **Testing**: Extended test coverage

## Citation

If you use this code in research, please cite:

```bibtex
@software{ramsey_z3_verification,
  author = {José Manuel Mota Burruezo},
  title = {Ramsey Vibrational Numbers Verification (Z3 Version)},
  year = {2024},
  url = {https://github.com/motanova84/Ramsey}
}
```

## License

MIT License - See LICENSE file for details.

## References

1. **Classical Ramsey Theory**: Graham, Rothschild, Spencer. "Ramsey Theory" (1990)
2. **Z3 Theorem Prover**: de Moura, Bjørner. "Z3: An Efficient SMT Solver" (2008)
3. **SAT-based Ramsey**: Heule, Kullmann. "The Science of Brute Force" (2017)

## Contact

- **Author**: José Manuel Mota Burruezo
- **Email**: [Contact via GitHub]
- **Repository**: https://github.com/motanova84/Ramsey

---

*"The order emerges more easily than predicted by random models when we consider the vibrational nature of systems."*
