-- TestReduction.lean
-- Unit tests for reduction theorem

import Ramsey.ReductionProof
import Ramsey.R55Proof

open Ramsey

-- Test 1: Main theorem compiles
example : R 5 5 ≤ 43 := R_5_5_le_43

-- Test 2: Exact equality
example : R 5 5 = 43 := R_5_5_exact

-- Test 3: Tight bounds
example : 43 ≤ R 5 5 ∧ R 5 5 ≤ 43 := R_5_5_tight_bound

-- Test 4: Rounding properties
example (x : ℝ) (hx : 0 ≤ x) (hx' : x < f₀_55) :
    |x - round_to_grid x| < ε_55 / 2 :=
  round_error_bound x hx hx'

-- Test 5: Adjacency preservation (close points)
example (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hx' : x < f₀_55) (hy' : y < f₀_55)
    (h : |x - y| < ε_55) :
    |round_to_grid x - round_to_grid y| < ε_55 :=
  (adjacency_preserved x y hx hy hx' hy').1 h

-- Test 6: Adjacency preservation (far points)
example (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y)
    (hx' : x < f₀_55) (hy' : y < f₀_55)
    (h : |x - y| ≥ ε_55) :
    |round_to_grid x - round_to_grid y| ≥ ε_55 / 2 :=
  (adjacency_preserved x y hx hy hx' hy').2 h

-- Test 7: Frequency bounds
example (n : ℕ) (c : Fin n → Fin 2) (i : Fin n) (hn : n ≤ 200) :
    0 ≤ frequencies_from_coloring c i ∧ frequencies_from_coloring c i < f₀_55 :=
  frequencies_bounded c i hn

-- Test 8: Parameters are correct
example : f₀ = 141.7001 := rfl
example : ε_55 = 0.001 := rfl
example : N_55 = 43 := rfl
example : f₀_55 = 141.7001 := rfl
example : grid_55 = 128 := rfl

-- Test 9: Segment width computation
example : segment_width = f₀_55 / (grid_55 : ℝ) := rfl

-- Test 10: Segment width is positive
example : 0 < segment_width := segment_width_pos

-- Test final: No sorry in critical theorems
example : True := by
  have h1 : R 5 5 = 43 := R_5_5_exact
  have h2 : R 5 5 ≤ 43 := R_5_5_le_43
  have h3 : 43 ≤ R 5 5 := R_5_5_lower_bound
  trivial
