-- test/test_reduction_proof.lean
-- Tests for ReductionProof.lean module

import Ramsey.Instance
import Ramsey.ReductionProof

namespace RamseyTest

open Ramsey

-- Test that segment_width is positive
example : 0 < segment_width := segment_width_pos

-- Test that round_to_grid is well-defined for values in range
example (x : ℝ) (hx : 0 ≤ x) (hx' : x < f₀_55) : 
    ∃ y, y = round_to_grid x := by
  use round_to_grid x

-- Test the round_error_bound lemma
example (x : ℝ) (hx : 0 ≤ x) (hx' : x < f₀_55) :
    |x - round_to_grid x| < ε_55 / 2 := 
  round_error_bound x hx hx'

-- Test that frequencies_from_coloring is well-defined
example {n : ℕ} (c : Fin n → Fin 2) (i : Fin n) :
    ∃ f : ℝ, f = frequencies_from_coloring c i := by
  use frequencies_from_coloring c i

-- Test the main reduction theorem type
example (r s N : ℕ) :
    (∀ (inst : Instance r s ε_55 N), ¬VibrationalUnsat inst) →
    Classical.R r s ≤ N := 
  vibrational_implies_classical_reduction r s N

end RamseyTest
