import Lake
open Lake DSL

package «ramsey-formal» where
  -- add package configuration options here

lean_lib «Ramsey» where
  -- add library configuration options here

@[default_target]
lean_exe «ramsey-formal» where
  root := `Main

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
