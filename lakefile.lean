import Lake
open Lake DSL

package «ramsey-vibracional» {
  -- add package configuration options here
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «RamseyVibracional» {
  -- add library configuration options here
}

@[default_target]
lean_lib «Certificates» {
  roots := #[`Certificates]
  -- Certificate files
}
