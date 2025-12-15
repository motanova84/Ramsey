-- Instance.lean
-- Vibrational instance structure with explicit SAT-compatible definitions

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace Ramsey

/-- A vibrational instance for SAT encoding
    This structure is designed to be compatible with SAT solver verification -/
structure Instance (r s : ℕ) (ε : ℝ) (N : ℕ) where
  /-- The actual number of vertices (typically N+1 for counterexample) -/
  n : ℕ
  /-- Set of vertices -/
  vertices : Finset (Fin n)
  /-- Edge relation: true if resonant (red), false if non-resonant (blue) -/
  edges : Fin n → Fin n → Bool
  /-- Frequency assignment to each vertex -/
  freq : Fin n → ℝ
  /-- Frequencies are bounded in [0, f₀) -/
  freq_bound : ∀ i, 0 ≤ freq i ∧ freq i < 141.7001
  /-- Edge coloring must respect frequency resonance -/
  edge_property : ∀ i j, i ≠ j → 
    (edges i j = true ↔ |freq i - freq j| < ε)

/-- An instance is UNSAT if it avoids both red and blue cliques -/
def VibrationalUnsat {r s : ℕ} {ε : ℝ} {N : ℕ} (inst : Instance r s ε N) : Prop :=
  inst.n = N + 1 ∧
  (∀ (S : Finset (Fin inst.n)), S.card = r → 
    ∃ i j ∈ S, i ≠ j ∧ inst.edges i j = false) ∧
  (∀ (S : Finset (Fin inst.n)), S.card = s → 
    ∃ i j ∈ S, i ≠ j ∧ inst.edges i j = true)

end Ramsey
