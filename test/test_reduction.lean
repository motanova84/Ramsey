-- test_reduction.lean
-- Tests for the reduction theorem Rψ → R

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction

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

end RamseyTest
