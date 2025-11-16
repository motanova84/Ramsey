import Lake
open Lake DSL

package ramsey where
  leanOptions := #[]
  moreLeanArgs := #[]

lean_lib Ramsey

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_exe «ramsey-formal» where
  root := `Main
