# Examples for Parameterized Ramsey Theory (R_Λ)

This directory contains example scripts demonstrating the parameterized Ramsey theory implementation.

## Overview

All examples use `ramsey_lambda.sage` to compute R_Λ(r,s) for various parameter combinations.

## Examples

### 1. Basic Examples (`example_basic.py`)

Demonstrates fundamental usage of the parameterized approach:
- Computing R_Λ for different (r,s) pairs
- Using different λ values
- Comparing with classical Ramsey numbers

**Run:**
```bash
python examples_lambda/example_basic.py
```

**What it shows:**
- R_Λ(3,3) with various λ values
- R_Λ(3,4) asymmetric case
- R_Λ(4,4) larger case
- How to interpret results

### 2. Threshold Behavior (`example_threshold.py`)

Explores Theorem B: the threshold behavior as μ(Λ) = λ varies.

**Run:**
```bash
python examples_lambda/example_threshold.py
```

**What it shows:**
- How R_Λ changes with λ ∈ (0,1)
- Comparison with theoretical bound C(λ)·√(rs)·log(rs)
- Optimal λ for minimal R_Λ
- Verification of Theorem A (R_Λ ≤ R)

**Sample Output:**
```
λ        μ(Λ)     R_Λ(r,s)     Theorem B    Classical
------------------------------------------------------------
0.01     0.01     5            652.1        6
0.05     0.05     5            130.4        6
0.10     0.10     5            65.2         6
0.20     0.20     5            32.6         6
0.50     0.50     6            13.0         6
```

## Direct Command-Line Usage

You can also use `ramsey_lambda.sage` directly:

### Basic Computation
```bash
python ramsey_lambda.sage --r=3 --s=3 --lam=0.1
```

### With Certificate Generation
```bash
python ramsey_lambda.sage --r=4 --s=4 --lam=0.05 --certify
```

### Adjust Precision and Search Range
```bash
python ramsey_lambda.sage --r=3 --s=4 --lam=0.1 --bits=18 --nmax=25
```

### Quiet Mode (Less Output)
```bash
python ramsey_lambda.sage --r=3 --s=3 --lam=0.1 --quiet
```

## Parameters Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--r` | Size of blue clique | `--r=3` |
| `--s` | Size of red clique | `--s=4` |
| `--lam` | Lambda (interval length) | `--lam=0.1` |
| `--certify` | Generate SMT2 certificate | `--certify` |
| `--bits` | Precision (bits) | `--bits=16` |
| `--nmax` | Max n to search | `--nmax=30` |
| `--quiet` | Suppress progress output | `--quiet` |

## Understanding the Output

### Main Result
```
RESULT: R_Λ(3,3) ≤ 5
        with Λ=[0,0.1), μ(Λ)=0.1
```

This means: For any assignment of frequencies ω_i ∈ [0,1) to 5 vertices,
there must exist either:
- A blue K_3 (triangle where all edges (i,j) satisfy (ω_i-ω_j) mod 1 ∈ [0,0.1))
- A red K_3 (triangle where no edge satisfies the above)

### Comparison with Theory
```
Conjectured bound (Theorem B): 65
Actual bound:                  5
Ratio:                         0.08
```

The theoretical bound from Theorem B provides an upper limit. The actual
computed bound is often much better, showing the bound is not tight.

### LaTeX Snippet
```latex
$\RL(3,3) \le 5$ \quad with \quad $\mu(\Lambda) = 0.1000$
```

Ready to include in papers, with proper formatting.

## Creating New Examples

To create a new example:

1. Import subprocess to call `ramsey_lambda.sage`
2. Parse output with regex: `r'R_Λ\((\d+),(\d+)\) ≤ (\d+)'`
3. Process and display results

Example template:
```python
import subprocess
import re

def compute(r, s, lam):
    cmd = ['python', 'ramsey_lambda.sage', 
           f'--r={r}', f'--s={s}', f'--lam={lam}', '--quiet']
    result = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r'R_Λ\((\d+),(\d+)\) ≤ (\d+)', result.stdout)
    return int(match.group(3)) if match else None

R_lambda = compute(3, 3, 0.1)
print(f"R_Λ(3,3) = {R_lambda}")
```

## Performance Notes

Computation time grows exponentially with n:
- (3,3): < 1 second
- (4,4): 2-5 seconds
- (5,5): 30-120 seconds (depending on λ)

For large (r,s), use:
- `--nmax` to limit search range
- Smaller `--bits` for faster but less precise computation
- Consider parallelizing multiple λ values

## Further Reading

- **Main Documentation**: See [RAMSEY_LAMBDA_README.md](../RAMSEY_LAMBDA_README.md)
- **Comparison**: See [COMPARISON.md](../COMPARISON.md)
- **Theory**: Problem statement in repository root

## Tips

1. **Start small**: Test with (3,3) or (3,4) first
2. **Use --quiet**: Reduces output for scripting
3. **Certificates**: Use `--certify` for important results
4. **Explore λ**: Different λ values can significantly affect bounds
5. **Be patient**: Larger cases (5,5) can take minutes

## Contributing

Have an interesting example? Submit a pull request with:
- Descriptive filename
- Clear comments
- Sample output in comments
- Entry in this README

---

**Questions?** See the main documentation or open an issue.
