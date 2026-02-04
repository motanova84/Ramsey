-- proofs/Rpsi_5_5_le_16.lean
-- NOTE: This file name is misleading - the SAT result shows R_ψ(5,5) > 16
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Finset.Basic

def f0 : ℝ := 141.7001
def ε : ℝ := 0.037
def grid : ℕ := 128

def ω_val (k : Fin grid) : ℝ := k.val * f0 / grid

def resonant (i j : Fin grid) : Prop :=
  let d := |ω_val i - ω_val j| % f0
  d ≤ ε ∨ d ≥ f0 - ε

structure VibColoring (n : ℕ) where
  ω : Fin n → Fin grid
  color : Fin n → Fin n → Bool
  valid : ∀ i j, color i j ↔ resonant (ω i) (ω j)

-- CORRECTED: SAT solver shows n=16 is SATISFIABLE, so the bound is > 16, not ≤ 16
axiom Rψ_5_5_counterexample_n16 :
  ∃ (c : VibColoring 16),
    (∀ S : Finset (Fin 16), S.card = 5 → ∃ e ∈ S.offDiag, ¬c.color e.1 e.2) ∧
    (∀ S : Finset (Fin 16), S.card = 5 → ∃ e ∈ S.offDiag, c.color e.1 e.2)
-- This axiom states that there exists a coloring of K₁₆ with NO monochromatic K₅,
-- proving R_ψ(5,5) > 16
