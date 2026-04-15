-- test_reduction.lean
-- Tests for the reduction theorem Rψ → R

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction
import Ramsey.ReductionProof

namespace RamseyTest

open Ramsey

-- Test that vibrational coloring induces classical coloring
example {n r s : ℕ} {ε : ℝ} (inst : Instance r s ε n) :
    ∃ c : Coloring n, c = vibToClassical inst := by
  use vibToClassical inst

-- Test basic properties of reduction
example (r s N : ℕ) (ε : ℝ) (hε : 0 < ε) (hε_small : ε < 1) :
    (∀ (inst : Instance r s ε N), ¬VibrationalUnsat inst) →
    R r s ≤ N := by
  intro h
  exact vibrational_implies_classical r s N ε hε hε_small h
  exact vibrational_implies_classical r s N ε h

-- Test that vibrational unsat implies classical valid coloring
example {n r s : ℕ} {ε : ℝ} (inst : Instance r s ε n) 
    (h : VibrationalUnsat inst) :
    isValidRamseyColoring (vibToClassical inst) r s := by
  exact vib_unsat_implies_classical_valid inst h

-- Test vibrational to classical coloring transformation
example {n r s : ℕ} {ε : ℝ} (inst : Instance r s ε n) :
    ∃ c : Coloring n, ∀ i j, c i j = (if isRed inst.ω i j then true else false) := by
  use vibrational_to_classical_coloring inst
  intro i j
  rfl

-- Test alternative formulation of reduction
example (r s N : ℕ) (ε : ℝ)
    (h : ∀ (inst : Instance r s ε N), ¬VibrationalUnsat inst) 
    (inst : Instance r s ε N) :
    hasRedClique (vibrational_to_classical_coloring inst) r ∨
    hasBlueClique (vibrational_to_classical_coloring inst) s := by
  exact vibrational_unsat_implies_ramsey_property r s N ε h inst

end RamseyTest
