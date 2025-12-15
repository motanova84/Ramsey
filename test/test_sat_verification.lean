-- test/test_sat_verification.lean
-- Tests for SAT certificate verification module

import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Reduction
import Ramsey.R55Proof
import Ramsey.SATVerification

namespace RamseyTest

open Ramsey

-- Test that the certificate path is defined correctly
example : r55_certificate_path = "data/proof_unsat_z3.log" := rfl

-- Test that the R55_unsat_proof theorem is available
-- This theorem states that no vibrational configuration of 43 vertices
-- can avoid both a red 5-clique and a blue 5-clique
example : ∀ (inst : Instance 5 5 ε_55 N_55), ¬VibrationalUnsat inst := 
  R55_unsat_proof

-- Verify that both theorems can be used interchangeably
example (inst : Instance 5 5 ε_55 N_55) : ¬VibrationalUnsat inst :=
  R55_unsat_proof inst

example (inst : Instance 5 5 ε_55 N_55) : ¬VibrationalUnsat inst :=
  sat_verified_unsat_43 inst

-- Test that the LRATCertificate structure can be constructed
example : LRATCertificate := {
  formula_hash := "test_hash"
  proof_steps := ["step1", "step2", "step3"]
  verified_by := "Kissat+LRAT"
}

-- Test with default verified_by field
example : LRATCertificate := {
  formula_hash := "hash"
  proof_steps := []
}

end RamseyTest
