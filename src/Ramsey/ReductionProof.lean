-- ReductionProof.lean
-- Module alias for Reduction.lean - exports reduction proof theorems
-- This module serves as an explicit namespace for reduction-related proofs

import Ramsey.Reduction

namespace Ramsey

-- Re-export main reduction theorems for verification purposes
export Reduction (vibrational_implies_classical)
export Reduction (vibToClassical)
export Reduction (vib_unsat_implies_classical_valid)
export Reduction (reduction_via_sat)

end Ramsey
