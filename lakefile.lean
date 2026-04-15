-- lakefile.lean
import Lake
open Lake DSL

package Ramsey where
  -- more package configuration options go here

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib Ramsey where
  -- add library configuration options here
  globs := #[.submodules "Ramsey"]

-- Verification script
lean_exe verify_all where
  root := `scripts.verify_all
