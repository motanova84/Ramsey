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

-- Test library configuration
lean_lib RamseyTest where
  srcDir := "test"
  globs := #[.andSubmodules `test_r55, .andSubmodules `test_reduction, .andSubmodules `test_hamiltonian]

-- Dependencia para certificados SAT
require «aesop» from git
  "https://github.com/leanprover-community/aesop" @ "master"
