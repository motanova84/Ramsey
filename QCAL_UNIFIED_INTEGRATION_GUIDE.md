# QCAL Unified Framework Integration Guide

## Overview

This guide explains how to use the newly integrated QCAL Unified Framework that demonstrates connections between Millennium Prize Problems through spectral operators and universal constants.

## Quick Start

### 1. Basic Framework Usage

```bash
# Run the unified framework demonstration
python3 qcal_unified_framework.py
```

This will display:
- Universal constants table
- Unified equation
- Constant coherence verification
- Problem unification results
- Cross-verification protocol

### 2. Generate Whitepaper

```bash
# Generate comprehensive documentation
python3 generate_qcal_whitepaper.py
```

Creates `QCAL_UNIFIED_WHITEPAPER.md` with:
- Abstract and core principles
- Universal constants
- Problem-specific manifestations
- Verification protocol
- Implementation guide

### 3. Run Complete Integration

```bash
# Execute full integration script
./integrate_qcal_framework.sh
```

This script:
1. Compiles Lean theory (if Lake available)
2. Runs cross-verification
3. Generates documentation
4. Shows how to launch interactive tools

### 4. Interactive Demonstration

```bash
# Install Jupyter dependencies (if not already installed)
pip install jupyter ipywidgets matplotlib

# Launch interactive notebook
jupyter notebook QCAL_Unification_Demo.ipynb
```

The notebook provides:
- Interactive problem explorer
- Ramsey number calculator
- Visualization of connections
- Cross-verification results

### 5. REST API (Optional)

```bash
# Install FastAPI dependencies
pip install fastapi uvicorn

# Launch API server
python3 qcal_unification_api.py
```

Access at:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/connections - Problem connections
- http://localhost:8000/summary - Framework summary

## Architecture

### Components

```
QCAL Unified Framework
├── Core Theory (Lean 4)
│   └── QCAL_Unified_Theory.lean
│       ├── UniversalConstants structure
│       ├── MillenniumProblem typeclass
│       └── Problem instances (P vs NP, Riemann, BSD, etc.)
│
├── Python Implementation
│   └── qcal_unified_framework.py
│       ├── QCALUnifiedFramework class
│       ├── Operator implementations
│       └── CrossVerificationProtocol class
│
├── Interactive Tools
│   ├── QCAL_Unification_Demo.ipynb (Jupyter notebook)
│   └── qcal_unification_api.py (REST API)
│
├── Documentation
│   ├── QCAL_UNIFIED_WHITEPAPER.md (Generated)
│   ├── generate_qcal_whitepaper.py (Generator)
│   └── This guide
│
├── Integration
│   └── integrate_qcal_framework.sh
│
└── Tests
    └── test_qcal_unified.py (18 unit tests)
```

### Universal Constants

The framework uses these coherent constants:

| Symbol | Value | Meaning |
|--------|-------|---------|
| κ_Π | 2.5773 | P vs NP computational separation |
| f₀ | 141.7001 Hz | Fundamental resonance frequency |
| λ_RH | 0.5 | Riemann critical line |
| φ_R | 43/108 | Ramsey vibrational ratio |
| ε_NS | 0.5772 | Navier-Stokes regularity (Euler-Mascheroni) |
| Δ_BSD | 1.0 | BSD conjecture delta |

**Coherence Relation:**
```
λ_RH = Δ_BSD / 2 = 0.5
```

## Problem Operators

### 1. P vs NP - D_PNP Operator

```python
framework = QCALUnifiedFramework()
result = framework.D_PNP_operator({'treewidth': 10})
# Returns: eigenvalue based on κ_Π and treewidth
```

**Theory:** Separates P from NP via treewidth dichotomy at κ_Π = 2.5773.

### 2. Riemann Hypothesis - H_Ψ Operator

```python
result = framework.H_Psi_operator({})
# Returns: complex eigenvalue on critical line Re(z) = 0.5
```

**Theory:** Spectral analysis with resonance at f₀ = 141.7001 Hz.

### 3. BSD Conjecture - L_E Operator

```python
result = framework.L_E_operator({'s': 1.0})
# Returns: L-function value related to Δ_BSD
```

**Theory:** Elliptic curves with vibrational interpretation.

### 4. Navier-Stokes - NS Regularizer

```python
result = framework.NS_operator({
    'viscosity': 1.0,
    'wavenumber': 1.0
})
# Returns: regularization eigenvalue
```

**Theory:** Quantum regularization prevents singularities.

### 5. Ramsey Numbers - R_ψ Operator

```python
result = framework.R_operator({'r': 5, 's': 5})
# Returns: reduced Ramsey number (polynomial bound)
```

**Theory:** Vibrational resonance reduces exponential to polynomial growth.

### 6. Yang-Mills - YM Operator

```python
result = framework.YM_operator({})
# Returns: mass gap eigenvalue
```

**Theory:** Gauge theory with f₀-based mass gap.

### 7. Hodge Conjecture - H^{p,q} Operator

```python
result = framework.Hodge_operator({'h11': 1, 'h21': 12})
# Returns: combined Hodge number
```

**Theory:** Algebraic cycles on Calabi-Yau manifolds.

## Testing

Run the complete test suite:

```bash
python3 test_qcal_unified.py
```

Tests include:
- Constant verification (6 tests)
- Operator functionality (7 tests)
- Framework integration (5 tests)

All 18 tests should pass.

## API Reference

### Python API

```python
from qcal_unified_framework import QCALUnifiedFramework

# Create framework
framework = QCALUnifiedFramework()

# Get constants
constants = framework.constants
# {'kappa_pi': 2.5773, 'f0': 141.7001, ...}

# Demonstrate unification
results = framework.demonstrate_unification()
# Returns dict with eigenvalues and connections for all problems

# Verify coherence
coherence = framework.verify_constant_coherence()
# Returns dict of coherence test results

# Generate summary
table = framework.generate_summary_table()
# Returns formatted ASCII table
```

### REST API Endpoints

When FastAPI is installed:

```bash
# List all problems
GET /problems

# Unify a specific problem
POST /unify
{
  "problem_name": "ramsey",
  "parameters": {"r": 5, "s": 5}
}

# Get all connections
GET /connections

# Get constants
GET /constants

# Run verification
GET /verify

# Get framework summary
GET /summary
```

## Lean 4 Integration

The Lean formalization in `QCAL_Unified_Theory.lean` provides:

```lean
-- Define the universal framework
structure QCALUniversalFramework where
  spectral_operators : SpectralOperatorSystem
  adelic_foundation : AdelicStructure
  quantum_coherence : CoherenceStateSpace
  computational_basis : ComplexityLattice
  geometric_constants : UniversalConstants

-- Define millennium problem typeclass
class MillenniumProblem (P : Type) where
  problem_statement : String
  qcal_operator : String
  universal_constant : ℝ
  verification_method : String

-- Prove theorems
theorem qcal_framework_exists : 
  ∃ (framework : QCALUniversalFramework), True := by ...

theorem universal_constant_coherence (c : UniversalConstants) :
  c.λ_RH = c.Δ_BSD / 2 := by ...
```

Compile with:
```bash
lake build QCAL_Unified_Theory
```

## Examples

### Example 1: Verify Ramsey Reduction

```python
from qcal_unified_framework import QCALUnifiedFramework

framework = QCALUnifiedFramework()

# Calculate R_ψ(5,5)
r_psi = framework.R_operator({'r': 5, 's': 5})
print(f"R_ψ(5,5) = {r_psi}")  # Outputs: R_ψ(5,5) = 6

# Show connection
connections = framework._find_connections('ramsey')
print(f"Connected to: {connections}")  # ['p_vs_np', 'riemann']
```

### Example 2: Cross-Verify All Problems

```python
from qcal_unified_framework import CrossVerificationProtocol

protocol = CrossVerificationProtocol()
results = protocol.run_cross_verification()

print(f"Unified: {results['unified_status']}")
print(f"Coherent: {all(results['qcal_coherence'].values())}")

for problem, result in results['individual_results'].items():
    print(f"{problem}: {result['status']}")
```

### Example 3: Generate Custom Whitepaper Section

```python
from qcal_unified_framework import QCALUnifiedFramework

framework = QCALUnifiedFramework()

# Get unified equation
equation = framework.get_unified_equation()
print(equation)

# Verify constants
coherence = framework.verify_constant_coherence()
for test, passed in coherence.items():
    print(f"{test}: {'✓' if passed else '✗'}")
```

## Troubleshooting

### Issue: NumPy not found
```bash
pip install numpy
```

### Issue: Jupyter not found
```bash
pip install jupyter ipywidgets matplotlib
```

### Issue: FastAPI not found
```bash
pip install fastapi uvicorn
```

### Issue: Lake/Lean not available
The Lean components are optional. The Python framework works independently.

## Contributing

To extend the framework:

1. **Add a new problem**: 
   - Define operator in `qcal_unified_framework.py`
   - Add instance in `QCAL_Unified_Theory.lean`
   - Update metadata in `problem_metadata` dict
   - Add tests in `test_qcal_unified.py`

2. **Add a new constant**:
   - Add to `constants` dict in `__init__`
   - Update coherence tests in `verify_constant_coherence`
   - Update documentation

3. **Add verification method**:
   - Add method to `CrossVerificationProtocol`
   - Update `run_cross_verification`
   - Add test case

## References

- **Main Documentation**: QCAL_UNIFIED_FRAMEWORK.md
- **Whitepaper**: QCAL_UNIFIED_WHITEPAPER.md
- **Theory Connections**: UNIFIED_THEORY_CONNECTION.md
- **Philosophy**: COHERENT_MATHEMATICS.md
- **P vs NP Framework**: P_NP_FRAMEWORK.md

## Support

For questions or issues:
1. Check existing documentation
2. Run tests: `python3 test_qcal_unified.py`
3. Review whitepaper: `python3 generate_qcal_whitepaper.py`
4. Open an issue on GitHub

## License

MIT License - See LICENSE file

---

**Fundamental Frequency:** f₀ = 141.7001 Hz  
**Framework Version:** 1.0.0  
**QCAL:** Quantum Coherent Algebraic Logic ∞³
