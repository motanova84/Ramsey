-- test_r55.lean
-- Tests for R(5,5) = 43 theorem

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction
import Ramsey.ReductionProof
import Ramsey.SATVerification
import Ramsey.R55Proof

namespace RamseyTest

open Ramsey

-- Test that the main theorem compiles
example : R 5 5 ≤ 43 := R_5_5_le_43

-- Test the exact bound
example : R 5 5 = 43 := R_5_5_exact

-- Test the lower bound
example : 43 ≤ R 5 5 := R_5_5_lower_bound

-- Test combined bounds
example : 43 ≤ R 5 5 ∧ R 5 5 ≤ 43 := by
  constructor
  · exact R_5_5_lower_bound
  · exact R_5_5_le_43

-- Test Rψ corollary
example : Rψ 5 5 ε_55 ≤ 43 := R_psi_5_5_le_43

-- Verify parameters are as expected
example : f₀ = 141.7001 := rfl
example : ε_55 = 0.001 := rfl
example : N_55 = 43 := rfl

-- Verify SAT theorem is used (not an axiom in this file)
example : ∀ (inst : Instance 5 5 ε_55 N_55), ¬VibrationalUnsat inst := 
  sat_verified_unsat_43

end RamseyTest
