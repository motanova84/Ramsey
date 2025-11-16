import Lake
open Lake DSL

package «ramsey-vibracional» where
  -- add package configuration options here

lean_lib «RamseyVibracional» where
  -- add library configuration options here

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «VibrationalRamsey» where
  globs := #[.submodules `VibrationalRamsey]
