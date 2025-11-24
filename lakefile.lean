import Lake
open Lake DSL

package «ramsey-formal» where
  -- Ramsey formal verification project
  -- Proves R(5,5) = 43 via vibrational reduction

lean_lib «Ramsey» where
  -- Library containing all Ramsey theory modules
  globs := #[.submodules `Ramsey]

@[default_target]
lean_exe «ramsey-formal» where
  root := `Main

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
