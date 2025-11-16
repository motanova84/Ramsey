import Ramsey.Vibrational
import Ramsey.Graph

namespace Ramsey

structure Instance (r s : ℕ) (ε λ : ℝ) where
  n : ℕ
  ω : Fin n → ℝ

def VibrationalUnsat {r s : ℕ} {ε λ : ℝ} (inst : Instance r s ε λ) : Prop :=
  ¬∃ (S : Finset (Fin inst.n)), S.card = r ∧
    ∀ i j, i ∈ S → j ∈ S → i ≠ j → in_resonance (inst.ω i) (inst.ω j)

end Ramsey
