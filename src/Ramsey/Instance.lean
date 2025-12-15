-- Instance.lean
-- Vibrational instance structure with proper bounds and properties

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace Ramsey

/-- A vibrational instance with r, s parameters, epsilon threshold, and n vertices -/
structure Instance (r s : ℕ) (ε : ℝ) (N : ℕ) where
  n : ℕ
  vertices : Finset (Fin n)
  edges : Fin n → Fin n → Bool
  freq : Fin n → ℝ
  freq_bound : ∀ i, 0 ≤ freq i ∧ freq i < 141.7001  -- f₀_55
  edge_property : ∀ i j, i ≠ j → 
    (edges i j = true ↔ |freq i - freq j| < ε)

/-- Two vertices are resonant if their frequency difference is small -/
def resonant {r s : ℕ} {ε : ℝ} {N : ℕ} (inst : Instance r s ε N) (i j : Fin inst.n) : Prop :=
  |inst.freq i - inst.freq j| < ε

/-- A set forms a resonant clique (all pairs resonant) -/
def hasResonantClique {r s : ℕ} {ε : ℝ} {N : ℕ} (inst : Instance r s ε N) 
    (vertices : Finset (Fin inst.n)) : Prop :=
  ∀ i j ∈ vertices, i ≠ j → resonant inst i j

/-- A set forms a non-resonant clique (all pairs non-resonant) -/
def hasNonResonantClique {r s : ℕ} {ε : ℝ} {N : ℕ} (inst : Instance r s ε N) 
    (vertices : Finset (Fin inst.n)) : Prop :=
  ∀ i j ∈ vertices, i ≠ j → ¬resonant inst i j

/-- An instance is UNSAT if it avoids both resonant r-clique and non-resonant s-clique -/
def VibrationalUnsat {r s : ℕ} {ε : ℝ} {N : ℕ} (inst : Instance r s ε N) : Prop :=
  inst.n = N ∧ 
  (¬∃ vertices : Finset (Fin inst.n), vertices.card = r ∧ hasResonantClique inst vertices) ∧
  (¬∃ vertices : Finset (Fin inst.n), vertices.card = s ∧ hasNonResonantClique inst vertices)

end Ramsey
