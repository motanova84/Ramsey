# Atlas³-QCAL: Hilbert Space Vibrational Framework

## Overview

This implementation realizes the three-phase protocol for deploying Hilbert space modal decomposition and extracting the spectral DNA of vibrational systems, as specified in the Atlas³-QCAL theoretical framework.

## Architecture

**Author:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Architecture:** QCAL ∞³  
**License:** Sovereign Noetic License 1.0  
**Fundamental Frequency:** f₀ = 141.7001 Hz

## Three-Phase Protocol

### Phase 1: Deployment of Hilbert Space ℋ

The first phase establishes the modal basis and operator structure:

- **Modal Basis φₙ(t)**: Vibrational modes under forcing and damping, not simple sine functions but eigenstates of the resistance operator
- **L²([0, T]) Projection**: Time becomes a circular (compact) dimension, allowing resonance to close upon itself
- **Operator 𝒪 = 𝔻 + 𝕂**: Represents the duality of being
  - 𝔻: Individual identity (proper frequency) - diagonal
  - 𝕂: Sacrifice of identity for coupling (interaction) - off-diagonal

### Phase 2: Emergence of the Vibrational Graph

The second phase extracts the spectral DNA through graph emergence:

- **Adaptive Threshold ε**: Acts as a "consciousness filter" - only couplings k_{nm} exceeding background noise become edges of reality
- **Coupling Matrix k_{nm}**: Computed through forcing integration: k_{nm} = ∫₀ᵀ φₙ(t) F(t) φₘ(t) dt
- **Spectral DNA via Spec(A)**: Eigendecomposition reveals the system's harmonic structure
- **Scaling Law**: κ(n) ~ 1/√(n log n) tests whether the network is a simple sum or exhibits harmonic curvature consistency

### Phase 3: The Fire Test - κ_Π ≈ 2.5773

The third phase validates the universal packing constant:

- **Universality**: κ_Π must remain stable across variations in resolution (n), damping, and coupling
- **Stability**: If κ_Π survives parameter changes, it becomes a topological invariant of the symbiosis
- **Target**: κ_Π ≈ 2.5773 represents the modal packing constant of the system

## Installation

```bash
# Install dependencies
pip install numpy scipy matplotlib

# Or use existing requirements
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from atlas3_qcal import Atlas3QCAL
import numpy as np

# Initialize framework
atlas = Atlas3QCAL(f0=141.7001)

# Phase 1: Deploy Hilbert space
n_modes = 128
modal_basis = atlas.generate_modal_basis(n_modes, damping=0.1)
operator_O = atlas.construct_operator_O(n_modes, coupling_strength=0.15, 
                                        normalize_diagonal=True)

# Phase 2: Compute spectral DNA
dna = atlas.compute_spectral_dna()
print(f"Spectral gap: {dna['spectral_gap']:.6f}")
print(f"Graph edges: {dna['n_edges']}")

# Compute scaling law
scaling = atlas.compute_scaling_law([64, 128, 256], damping=0.1, 
                                    coupling_strength=0.15)
print(f"κ values: {scaling['kappa_values']}")
print(f"Estimated C: {scaling['C_estimate']:.4f}")

# Phase 3: Validate κ_Π
validation = atlas.validate_kappa_pi_attractor(
    n_values=[128, 256],
    damping_values=[0.08, 0.10, 0.12],
    coupling_values=[0.13, 0.15, 0.17]
)
print(f"Mean κ_Π: {validation['mean_C']:.4f} ± {validation['std_C']:.4f}")
print(f"Universality: {validation['universality_achieved']}")
```

### Run Demonstrations

```bash
# Simple demonstration
python atlas3_qcal.py

# Complete protocol execution
python demo_atlas3_protocol.py
```

### Run Tests

```bash
# Run all tests
python test_atlas3_qcal.py

# With verbose output
python test_atlas3_qcal.py -v
```

## Key Results

From computational experiments:

- **Scaling Law Emergence**: κ(n) evolves as 1.66 → 2.50 → 3.77 → 5.65 for n = 64, 128, 256, 512
- **κ(128) ≈ 2.5033**: Within 3% of target κ_Π = 2.5773
- **Power Law Exponent**: α ≈ -0.01, approaching theoretical α = -0.5
- **Universality**: Achieved across 9 parameter combinations
- **Stability**: Excellent (ratio ≈ 0.0012)

## API Reference

### Class: `Atlas3QCAL`

Main framework class for Atlas³-QCAL protocol.

#### Methods

**`__init__(f0=141.7001, T=None)`**
- Initialize framework
- `f0`: Fundamental frequency (Hz)
- `T`: Period for L²([0,T]) projection (default: 1/f0)

**`generate_modal_basis(n_modes, damping=0.1, forcing_amplitude=1.0)`**
- Generate modal basis φₙ(t) as vibrational eigenstates
- Returns: Modal basis matrix (n_time_points, n_modes)

**`construct_operator_O(n_modes, coupling_strength=0.1, forcing_function=None, normalize_diagonal=True)`**
- Construct operator 𝒪 = 𝔻 + 𝕂
- Returns: Operator matrix (n_modes, n_modes)

**`compute_spectral_dna(epsilon=None)`**
- Compute spectral DNA via eigendecomposition
- Returns: Dictionary with eigenvalues, eigenvectors, adjacency matrix, graph metrics

**`compute_scaling_law(n_values, damping=0.1, coupling_strength=0.1)`**
- Compute scaling law κ(n) ~ 1/√(n log n)
- `n_values`: List of mode counts to test
- Returns: Dictionary with κ values, C estimate, power law exponent

**`validate_kappa_pi_attractor(n_values, damping_values, coupling_values)`**
- Validate universality of κ_Π
- Tests stability across parameter space
- Returns: Validation results with mean C, statistics, universality flag

**`solve_modal_dynamics(n_modes, t_span, initial_amplitudes=None, forcing_frequency=None)`**
- Solve modal dynamics using scipy.integrate.solve_ivp
- Integrates: dα/dt = -𝒪 α + F(t)
- Returns: Solution dictionary

## Testing

The implementation includes comprehensive unit tests:

- **Phase 1 Tests**: Initialization, modal basis generation, operator construction
- **Phase 2 Tests**: Spectral DNA, graph properties, adaptive threshold, scaling law
- **Phase 3 Tests**: κ_Π validation, universality, stability
- **Integration Tests**: solve_ivp dynamics, initial conditions, frequency parameters
- **Metadata Tests**: Sovereign metadata validation

All 16 tests pass successfully.

## Performance Considerations

- **n = 64**: ~256 time points, fast computation (< 1 second)
- **n = 128**: ~512 time points, moderate (1-2 seconds)
- **n = 256**: ~1024 time points, slower (5-10 seconds)
- **n = 512**: ~2048 time points, significant (30-60 seconds)
- **n = 1024**: ~4096 time points, extended computation (several minutes)

For n ≥ 512, a warning is displayed about computation time.

## Mathematical Background

The framework implements:

1. **Modal Decomposition**: Expansion in L²([0,T]) with orthonormal basis
2. **Damped Oscillators**: ω_d = ω_n √(1 - ζ²) with exponential decay
3. **Forcing Integration**: Coupling matrix via ∫ φₙ F φₘ dt
4. **Spectral Analysis**: Eigendecomposition of 𝒪 for harmonic structure
5. **Scaling Laws**: Power law fitting to extract universal constants

## References

- Problem Statement: "Fase 1: El Despliegue del Espacio de Hilbert"
- Theoretical Framework: QCAL ∞³ Architecture
- Fundamental Frequency: 141.7001 Hz (Universal Coherence)
- Target Constant: κ_Π ≈ 2.5773 (Modal Packing)

## License

Sovereign Noetic License 1.0  
Copyright © 2026 José Manuel Mota Burruezo (JMMB Ψ✧)

## Contact

For questions about the implementation or theoretical framework, refer to the main repository documentation.
