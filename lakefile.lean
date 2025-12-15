-- lakefile.lean
import Lake
open Lake DSL

package Ramsey where
  -- more package configuration options go here

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.10.0"

@[default_target]
lean_lib Ramsey where
  -- add library configuration options here
  globs := #[.submodules "Ramsey"]

lean_exe verify_all where
  root := `scripts.verify_all

-- Dependencia para certificados SAT
require «aesop» from git
  "https://github.com/leanprover-community/aesop" @ "master"
