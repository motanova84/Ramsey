-- example_vibrational_reduction.lean
-- Concrete examples demonstrating the vibrational to classical reduction

import Ramsey.VibrationalReduction
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic

namespace VibrationalReductionExamples

open VibrationalReduction
open Classical

/-!
## Example 1: Triangle Graph (K₃)

We show that a triangle graph with 3 colors can be properly colored
if we have a resonant frequency assignment.
-/

-- Define a triangle graph on 3 vertices
def triangleGraph : SimpleGraph (Fin 3) where
  Adj i j := i ≠ j
  symm := fun _ _ h => h.symm
  loopless := fun _ h => h rfl

-- Example frequency assignment for the triangle
-- Vertices at frequencies 0, 0.05, 0.10 (well-separated)
noncomputable def triangleFreq : FreqAssignment (Fin 3) :=
  fun i => match i with
  | 0 => ⟨0.00, by norm_num⟩
  | 1 => ⟨0.05, by norm_num⟩
  | 2 => ⟨0.10, by norm_num⟩

-- Verify this assignment is resonant with δ = 0.01
lemma triangle_resonant : Resonant triangleGraph triangleFreq δ := by
  intro v w adj
  -- Unfold definitions
  unfold δ triangleFreq
  -- Check all pairs
  fin_cases v <;> fin_cases w <;> simp [triangleGraph] at adj ⊢
  all_goals (try norm_num; done)

-- Apply the reduction theorem
example : ∃ c : Coloring 3 (Fin 3), ∀ ⦃v w⦄, triangleGraph.Adj v w → c v ≠ c w := by
  apply vibrational_to_classical triangleGraph (by norm_num) triangleFreq
  exact triangle_resonant

/-!
## Example 2: Path Graph

A simple path graph: 0 -- 1 -- 2
This requires only 2 colors classically.
-/

def pathGraph : SimpleGraph (Fin 3) where
  Adj i j := (i = 0 ∧ j = 1) ∨ (i = 1 ∧ j = 0) ∨ (i = 1 ∧ j = 2) ∨ (i = 2 ∧ j = 1)
  symm := by
    intro i j h
    cases h with
    | inl h => cases h; right; left; constructor <;> assumption
    | inr h => 
      cases h with
      | inl h => cases h; left; constructor <;> assumption
      | inr h =>
        cases h with
        | inl h => cases h; right; right; right; constructor <;> assumption
        | inr h => cases h; right; right; left; constructor <;> assumption
  loopless := by
    intro i h
    cases h with
    | inl h => cases h; omega
    | inr h =>
      cases h with
      | inl h => cases h; omega
      | inr h =>
        cases h with
        | inl h => cases h; omega
        | inr h => cases h; omega

-- Frequency assignment for path: 0, 0.02, 0
-- Note: endpoints can have the same frequency since they're not adjacent
noncomputable def pathFreq : FreqAssignment (Fin 3) :=
  fun i => match i with
  | 0 => ⟨0.00, by norm_num⟩
  | 1 => ⟨0.02, by norm_num⟩
  | 2 => ⟨0.00, by norm_num⟩

lemma path_resonant : Resonant pathGraph pathFreq δ := by
  intro v w adj
  unfold δ pathFreq pathGraph at *
  fin_cases v <;> fin_cases w <;> simp at adj ⊢
  all_goals (
    try { cases adj <;> norm_num }
    done
  )

example : ∃ c : Coloring 2 (Fin 3), ∀ ⦃v w⦄, pathGraph.Adj v w → c v ≠ c w := by
  apply vibrational_to_classical pathGraph (by norm_num) pathFreq
  exact path_resonant

/-!
## Documentation

These examples demonstrate:
1. How to define simple graphs using SimpleGraph
2. How to construct frequency assignments
3. How to prove resonance conditions
4. How to apply the vibrational_to_classical theorem

The key insight: if frequencies are well-separated (≥ δ), 
discretization produces a valid coloring.
-/

end VibrationalReductionExamples
