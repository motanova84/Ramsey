-- Graph.lean
-- Basic definitions for graphs, colorings, and cliques

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace Ramsey

/-- A simple graph on n vertices -/
structure Graph (n : ℕ) where
  edge : Fin n → Fin n → Prop
  symm : ∀ i j, edge i j → edge j i
  irrefl : ∀ i, ¬ edge i i

/-- A coloring of edges with two colors (red/blue) -/
def Coloring (n : ℕ) := Fin n → Fin n → Bool

/-- Check if a set forms a monochromatic clique of given color -/
def isMonochromaticClique {n : ℕ} (c : Coloring n) (color : Bool) (S : Finset (Fin n)) : Prop :=
  ∀ i j ∈ S, i < j → c i j = color

/-- A clique in a graph -/
def isClique {n : ℕ} (g : Graph n) (S : Finset (Fin n)) : Prop :=
  ∀ i j ∈ S, i ≠ j → g.edge i j

/-- The complete graph on n vertices -/
def completeGraph (n : ℕ) : Graph n where
  edge i j := i ≠ j
  symm := fun i j h => Ne.symm h
  irrefl := fun i => id

/-- Check if coloring contains a red clique of size r -/
def hasRedClique {n : ℕ} (c : Coloring n) (r : ℕ) : Prop :=
  ∃ S : Finset (Fin n), S.card = r ∧ isMonochromaticClique c true S

/-- Check if coloring contains a blue clique of size s -/
def hasBlueClique {n : ℕ} (c : Coloring n) (s : ℕ) : Prop :=
  ∃ S : Finset (Fin n), S.card = s ∧ isMonochromaticClique c false S

/-- A valid Ramsey coloring avoids both red r-clique and blue s-clique -/
def isValidRamseyColoring {n : ℕ} (c : Coloring n) (r s : ℕ) : Prop :=
  ¬ hasRedClique c r ∧ ¬ hasBlueClique c s

end Ramsey
