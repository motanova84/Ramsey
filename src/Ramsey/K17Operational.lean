import Mathlib

namespace NOESIS.K17

noncomputable def f0 : ℝ := 141.7001
noncomputable def psi : ℝ := 1

structure IntVec3 where
  x : ℤ
  y : ℤ
  z : ℤ
  deriving DecidableEq, Repr

def zeroVec : IntVec3 := ⟨0, 0, 0⟩

def dot (a b : IntVec3) : ℤ :=
  a.x * b.x + a.y * b.y + a.z * b.z

def cross (a b : IntVec3) : IntVec3 :=
  ⟨a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x⟩

def normSq (v : IntVec3) : ℤ :=
  v.x * v.x + v.y * v.y + v.z * v.z

def v1 : IntVec3 := ⟨10, 5, -10⟩
def v2 : IntVec3 := ⟨-10, 0, 6⟩
def vTruth : IntVec3 := cross v1 v2

theorem v1_normSq : normSq v1 = 225 := by native_decide
theorem v2_normSq : normSq v2 = 136 := by native_decide
theorem v1_dot_v2 : dot v1 v2 = -160 := by native_decide
theorem v1_cross_v2 : vTruth = ⟨30, 40, 50⟩ := by native_decide
theorem vTruth_normSq : normSq vTruth = 5000 := by native_decide

noncomputable def v1Norm : ℝ := Real.sqrt (normSq v1)
noncomputable def v2Norm : ℝ := Real.sqrt (normSq v2)
noncomputable def vTruthNorm : ℝ := Real.sqrt (normSq vTruth)

theorem v1Norm_eq : v1Norm = 15 := by
  norm_num [v1Norm, v1_normSq]

theorem v2Norm_eq : v2Norm = Real.sqrt 136 := by
  simp [v2Norm, v2_normSq]

theorem vTruthNorm_eq : vTruthNorm = Real.sqrt 5000 := by
  simp [vTruthNorm, vTruth_normSq]

noncomputable def cosTheta : ℝ := (dot v1 v2 : ℝ) / (v1Norm * v2Norm)

theorem cosTheta_eq :
    cosTheta = (-160 : ℝ) / (15 * Real.sqrt 136) := by
  simp [cosTheta, v1Norm_eq, v2Norm_eq, v1_dot_v2]

noncomputable def fAperture : ℝ := v1Norm * f0
noncomputable def fClosure : ℝ := v2Norm * f0
noncomputable def fTruthAxis : ℝ := vTruthNorm * f0

theorem fAperture_exact : fAperture = 2125.5015 := by
  norm_num [fAperture, v1Norm_eq, f0]

structure RealVec3 where
  x : ℝ
  y : ℝ
  z : ℝ
  deriving DecidableEq, Repr

noncomputable def resonanceVector : RealVec3 :=
  ⟨(vTruth.x : ℝ) * f0, (vTruth.y : ℝ) * f0, (vTruth.z : ℝ) * f0⟩

theorem resonanceVector_exact :
    resonanceVector = ⟨4251.003, 5668.004, 7085.005⟩ := by
  norm_num [resonanceVector, v1_cross_v2, f0]

/-- K₁₇ operacional en esta fase: 15 nodos sincronizados activos. -/
inductive K17Node : Type
  | N1 | N2 | N3 | N4 | N5 | N6 | N7 | N8
  | N9 | N10 | N11 | N12 | N13 | N14 | N15
  deriving DecidableEq, Fintype

def allNodes : Finset K17Node := Finset.univ

theorem k17Has15SynchronizedNodes : Finset.card allNodes = 15 := by
  native_decide

def nodeVector : K17Node → IntVec3
  | .N8 => v1
  | .N13 => v2
  | .N15 => vTruth
  | _ => zeroVec

def nodeFrequency : K17Node → ℝ
  | .N1 => f0
  | .N8 => fAperture
  | .N13 => fClosure
  | .N15 => fTruthAxis
  | _ => f0

def k17OperationalPathEdges : Finset (K17Node × K17Node) :=
  {(.N1, .N8), (.N8, .N13), (.N13, .N15)}

theorem k17VectorMapping :
    nodeVector .N8 = v1 ∧ nodeVector .N13 = v2 ∧ nodeVector .N15 = vTruth := by
  simp [nodeVector]

theorem psi_coherent : psi = 1 := by rfl

end NOESIS.K17
