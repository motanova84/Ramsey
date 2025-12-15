# Vibrational to Classical Reduction

## Overview

This module implements a bridge between vibrational (frequency-based) graph coloring and classical discrete graph coloring. The key insight is that frequency assignments with sufficient separation can be discretized into valid colorings.

## Main Concepts

### Frequency Assignment
- Each vertex is assigned a non-negative real frequency
- Frequencies represent vibrational states or harmonic modes
- Type: `FreqAssignment V := V → Frequency` where `Frequency = {f : ℝ // 0 ≤ f}`

### Resonance Condition
- Adjacent vertices must have frequencies separated by at least δ (minimum separation)
- `Resonant G f δ` means: for all adjacent vertices v, w: |f(v) - f(w)| ≥ δ
- This ensures no "interference" between neighboring vertices

### Classical Coloring
- Discrete assignment of colors from a finite set
- Type: `VertexColoring r V := V → Fin r` (r colors)
- Adjacent vertices must have different colors
- Note: This is different from `Coloring` in Graph.lean which colors edges

## Main Theorems

### `vibrational_to_classical`
If there exists a resonant frequency assignment (with separation ≥ δ), then there exists a valid classical coloring.

**Proof Sketch:**
1. Given a resonant frequency assignment f
2. Discretize frequencies into bins of size ε = δ/10
3. Map each frequency to a color based on its bin
4. Adjacent vertices have frequencies separated by ≥ δ
5. Therefore they fall into different bins (different colors)
6. This gives a valid coloring with no monochromatic edges

### Connection to Ramsey Theory

This reduction is crucial for proving R(5,5) ≤ 43:
- If the vibrational model (with SAT solver) proves UNSAT for n=43
- Then no valid frequency assignment exists
- By contrapositive of our theorem, no valid coloring exists
- Therefore R(5,5) ≤ 43

## Parameters

- **δ = 0.01**: Minimum frequency separation (can be tuned)
- **ε = δ/10**: Discretization granularity for binning

## Usage

```lean
import Ramsey.VibrationalReduction

open Ramsey.VibrationalReduction

-- Prove a graph has a valid coloring from a resonant frequency assignment
example {r : ℕ} {V : Type*} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V) (hr : 0 < r)
  (f : FreqAssignment V) (hf : Resonant G f δ) :
  ∃ c : VertexColoring r V, ∀ ⦃v w⦄, G.Adj v w → c v ≠ c w :=
vibrational_to_classical G hr f hf
```

## References

- Main paper: RAMSEY-JMMB.pdf
- Related: Vibrational.lean, Reduction.lean
- Test: test/test_vibrational_reduction.lean
