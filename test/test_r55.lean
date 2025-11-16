-- test_r55.lean
-- Tests for R(5,5) = 43 theorem

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction
import Ramsey.R55Proof

namespace RamseyTest

open Ramsey

-- Test that the main theorem compiles
example : R 5 5 ≤ 43 := R_5_5_le_43

-- Test the exact bound
example : R 5 5 = 43 := R_5_5_exact

-- Test the tight bounds
example : 43 ≤ R 5 5 ∧ R 5 5 ≤ 43 := R_5_5_tight_bound

-- Verify parameters are as expected
example : f₀ = 141.7001 := rfl
example : ε_55 = 0.001 := rfl
example : N_55 = 43 := rfl

end RamseyTest
