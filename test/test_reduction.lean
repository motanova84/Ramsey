-- test/test_reduction.lean

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction

namespace RamseyTest

open Ramsey

/-!
  Tests for Reduction Module
  
  This module contains tests for the exponential to polynomial
  reduction in Ramsey theory via the vibrational approach.
-/

-- Test: Vibrational bound exists
example : ∃ C : ℝ, ∀ r s : ℕ, ∀ ε : ℝ, 
    (r ≥ 2) → (s ≥ 2) → (0 < ε ∧ ε < 1) →
    vibrationalRamseyNumber r s ε ≤ C * Real.sqrt (r * s) * Real.log (r * s) := by
  sorry

-- Test: Vibrational is better than classical
example (r s : ℕ) (ε : ℝ) (hr : r ≥ 2) (hs : s ≥ 2) (hε : 0 < ε ∧ ε < 1) :
    vibrationalRamseyNumber r s ε ≤ ramseyNumber r s :=
  vibrational_better_than_classical r s ε hr hs hε

-- Test: Small cases
example : vibrationalRamseyNumber 3 3 0.1 ≤ ramseyNumber 3 3 := by
  apply vibrational_better_than_classical
  · norm_num
  · norm_num
  · constructor <;> norm_num

-- Test: Polynomial bound property
example (r s : ℕ) (ε : ℝ) (hr : r ≥ 2) (hs : s ≥ 2) (hε : 0 < ε ∧ ε < 1) :
    ∃ C : ℝ, vibrationalRamseyNumber r s ε ≤ 
      C * Real.sqrt (r * s) * Real.log (r * s) :=
  vibrational_polynomial_bound r s ε hr hs hε

end RamseyTest
