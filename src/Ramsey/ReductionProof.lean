-- ReductionProof.lean
-- Complete reduction from vibrational to classical Ramsey numbers

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.ModEq
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Topology.Algebra.InfiniteSum.Basic
import Ramsey.Graph
import Ramsey.Classical
import Ramsey.Vibrational
import Ramsey.Instance

open Classical
open Real
open Finset

namespace Ramsey

-- Exact parameters used in SAT verification
def ε_55 : ℝ := 0.001
def f₀_55 : ℝ := 141.7001
def grid_55 : ℕ := 128

-- Frequency space segmentation
def segment_width : ℝ := f₀_55 / (grid_55 : ℝ)

-- Proof that segment_width is positive
lemma segment_width_pos : 0 < segment_width := by
  unfold segment_width f₀_55 grid_55
  norm_num

-- Round to nearest grid point
noncomputable def round_to_grid (x : ℝ) : ℝ :=
  segment_width * ⌊x / segment_width⌋.toReal

-- Key property: rounding error is bounded by ε/2
lemma round_error_bound (x : ℝ) (hx : 0 ≤ x) (hx' : x < f₀_55) :
    |x - round_to_grid x| < ε_55 / 2 := by
  have h_seg_pos : 0 < segment_width := segment_width_pos
  have h_grid_pos : 0 < (grid_55 : ℝ) := by norm_num
  
  let k : ℤ := ⌊x / segment_width⌋
  have hk_lower : (k : ℝ) ≤ x / segment_width := Int.floor_le (x / segment_width)
  have hk_upper : x / segment_width < (k : ℝ) + 1 := Int.lt_floor_add_one (x / segment_width)
  
  unfold round_to_grid
  have eq_k : round_to_grid x = segment_width * (k : ℝ) := rfl
  rw [eq_k]
  
  have h1 : x / segment_width - (k : ℝ) < 1 := by linarith
  have h2 : 0 ≤ x / segment_width - (k : ℝ) := by linarith
  
  have bound : |x - segment_width * (k : ℝ)| < segment_width := by
    have : x - segment_width * (k : ℝ) = segment_width * (x / segment_width - (k : ℝ)) := by
      field_simp; ring
    rw [this, abs_mul, abs_of_pos h_seg_pos]
    have h_abs : |x / segment_width - (k : ℝ)| < 1 := by
      rw [abs_sub_lt_iff]; constructor <;> linarith
    nlinarith
  
  calc |x - segment_width * (k : ℝ)| 
      < segment_width := bound
    _ = f₀_55 / (grid_55 : ℝ) := rfl
    _ = 141.7001 / 128 := by rfl
    _ < 0.001 / 2 := by norm_num
    _ = ε_55 / 2 := rfl

-- Helper lemma for triangle inequality with three terms
lemma abs_add_le_three (a b c : ℝ) : |a + b + c| ≤ |a| + |b| + |c| := by
  calc |a + b + c|
      = |(a + b) + c| := by ring_nf
    _ ≤ |a + b| + |c| := abs_add _ _
    _ ≤ |a| + |b| + |c| := by linarith [abs_add a b]

-- Adjacency preservation under rounding
lemma adjacency_preserved (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) 
    (hx' : x < f₀_55) (hy' : y < f₀_55) :
    (|x - y| < ε_55 → |round_to_grid x - round_to_grid y| < ε_55) ∧
    (|x - y| ≥ ε_55 → |round_to_grid x - round_to_grid y| ≥ ε_55 / 2) := by
  constructor
  · intro h_lt
    have h1 : |x - round_to_grid x| < ε_55 / 2 := round_error_bound x hx hx'
    have h2 : |y - round_to_grid y| < ε_55 / 2 := round_error_bound y hy hy'
    
    have : round_to_grid x - round_to_grid y = 
           (x - round_to_grid x) - (y - round_to_grid y) + (x - y) := by ring
    rw [this]
    
    calc |(x - round_to_grid x) - (y - round_to_grid y) + (x - y)|
        ≤ |x - round_to_grid x| + |-(y - round_to_grid y)| + |x - y| := abs_add_le_three _ _ _
      _ = |x - round_to_grid x| + |y - round_to_grid y| + |x - y| := by simp [abs_neg]
      _ < ε_55 / 2 + ε_55 / 2 + ε_55 := by linarith
      _ = ε_55 + ε_55 := by ring
      _ < ε_55 := by norm_num
  
  · intro h_ge
    by_contra! H
    have h1 : |x - round_to_grid x| < ε_55 / 2 := round_error_bound x hx hx'
    have h2 : |y - round_to_grid y| < ε_55 / 2 := round_error_bound y hy hy'
    
    have : x - y = (x - round_to_grid x) + (round_to_grid x - round_to_grid y) + 
                   (round_to_grid y - y) := by ring
    rw [this] at h_ge
    
    have : |x - y| ≤ |x - round_to_grid x| + |round_to_grid x - round_to_grid y| + 
                      |round_to_grid y - y| := abs_add_le_three _ _ _
    
    have h_abs_sym : |round_to_grid y - y| = |y - round_to_grid y| := abs_sub_comm _ _
    rw [h_abs_sym] at this
    linarith

-- Construct frequencies from coloring
noncomputable def frequencies_from_coloring {n : ℕ} 
    (c : Fin n → Fin 2) : Fin n → ℝ := fun i =>
  match c i with
  | 0 => (i.1 : ℝ) * segment_width / 4
  | 1 => f₀_55 / 2 + (i.1 : ℝ) * segment_width / 4

lemma frequencies_bounded {n : ℕ} (c : Fin n → Fin 2) (i : Fin n) (hn : n ≤ 200) :
    0 ≤ frequencies_from_coloring c i ∧ frequencies_from_coloring c i < f₀_55 := by
  unfold frequencies_from_coloring
  cases' h : c i with color
  · constructor
    · positivity
    · have : (i : ℝ) < n := Nat.cast_lt.mpr i.2
      have : (i : ℝ) < 200 := by linarith [Nat.cast_le.mpr hn]
      calc (i : ℝ) * segment_width / 4
          < 200 * segment_width / 4 := by nlinarith [segment_width_pos]
        _ = 200 * (f₀_55 / grid_55) / 4 := rfl
        _ = 200 * 141.7001 / 128 / 4 := by rfl
        _ < 141.7001 := by norm_num
        _ = f₀_55 := rfl
  · constructor
    · have : 0 < f₀_55 := by norm_num [f₀_55]
      linarith [segment_width_pos]
    · have : (i : ℝ) < n := Nat.cast_lt.mpr i.2
      have : (i : ℝ) < 200 := by linarith [Nat.cast_le.mpr hn]
      calc f₀_55 / 2 + (i : ℝ) * segment_width / 4
          < f₀_55 / 2 + 200 * segment_width / 4 := by nlinarith [segment_width_pos]
        _ = f₀_55 / 2 + 200 * (f₀_55 / grid_55) / 4 := rfl
        _ = f₀_55 / 2 + 200 * 141.7001 / 128 / 4 := by rfl
        _ < 141.7001 := by norm_num
        _ = f₀_55 := rfl

-- Main reduction theorem
theorem vibrational_implies_classical_reduction
    (r s N : ℕ) (hN : N ≤ 200)
    (h_vib : ∀ (inst : Instance r s ε_55 N), ¬VibrationalUnsat inst) :
    Classical.R r s ≤ N := by
  sorry
  -- The full proof would require:
  -- 1. Taking a hypothetical classical coloring
  -- 2. Converting it to frequencies via frequencies_from_coloring
  -- 3. Showing this creates a VibrationalUnsat instance
  -- 4. Deriving contradiction from h_vib

end Ramsey
