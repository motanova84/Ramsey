import Mathlib.Data.Fin.Basic

namespace Ramsey

def Edge (n : ℕ) := {e : Fin n × Fin n // e.1 ≠ e.2}

end Ramsey
