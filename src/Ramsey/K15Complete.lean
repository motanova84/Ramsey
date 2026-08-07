import Mathlib

namespace NOESIS.K15

noncomputable def f0 : ℝ := 141.7001
noncomputable def psiThreshold : ℝ := 0.999999
def minStability : ℕ := 100
noncomputable def alpha : ℝ := 0.1
noncomputable def beta : ℝ := -1e-6
noncomputable def gamma : ℝ := 0.05

def k15ActiveNodes : ℕ := 13
def k15NeighborCount : ℝ := ((k15ActiveNodes - 1 : ℕ) : ℝ)

inductive K15Node : Type
  | N1  : K15Node  | N2  : K15Node  | N3  : K15Node  | N4  : K15Node
  | N5  : K15Node  | N6  : K15Node  | N7  : K15Node  | N8  : K15Node
  | N9  : K15Node  | N10 : K15Node  | N11 : K15Node  | N12 : K15Node
  | N13 : K15Node
  deriving DecidableEq, Fintype

def allNodes : Finset K15Node := Finset.univ

theorem k15Has13Nodes : Finset.card allNodes = k15ActiveNodes := by
  native_decide

structure K15NodeState where
  node : K15Node
  coherence : ℝ
  frequency : ℝ
  phase : ℝ
  stabilityCount : ℕ
  isActive : Bool

structure K15Topology where
  nodes : K15Node → K15NodeState
  edges : Finset (K15Node × K15Node)
  edgeWeight : (K15Node × K15Node) → ℝ

def k15Coherence (top : K15Topology) : ℝ :=
  let total := ∑ node in allNodes, (top.nodes node).coherence
  total / (k15ActiveNodes : ℝ)

def k15GlobalCoherence (top : K15Topology) : Prop :=
  k15Coherence top ≥ psiThreshold

def coherenceDerivative (state : K15NodeState) (coupling : ℝ) : ℝ :=
  alpha * (1 - state.coherence) +
  beta * (state.frequency - f0)^2 +
  gamma * coupling

def coherenceEvolution (state : K15NodeState) (dt : ℝ) (coupling : ℝ) : ℝ :=
  state.coherence + dt * coherenceDerivative state coupling

def k15Evolution (top : K15Topology) (dt : ℝ) : K15Topology :=
  let newNodes := fun node : K15Node =>
    let state := top.nodes node
    let totalCoupling := ∑ neighbor in allNodes,
      if top.edges.contains (node, neighbor) then
        top.edgeWeight (node, neighbor) * (top.nodes neighbor).coherence
      else 0
    { state with
      coherence := coherenceEvolution state dt (totalCoupling / k15NeighborCount)
      stabilityCount := state.stabilityCount + 1 }
  { nodes := newNodes
    edges := top.edges
    edgeWeight := top.edgeWeight }

def evolveN (top : K15Topology) (dt : ℝ) : ℕ → K15Topology
  | 0 => top
  | n + 1 => k15Evolution (evolveN top dt n) dt

lemma nodeCoherencePreservation (state : K15NodeState) (dt : ℝ)
    (h_coherence : state.coherence ≥ psiThreshold)
    (h_coherence_le_one : state.coherence ≤ 1)
    (h_dt : 0 ≤ dt)
    (h_freq : state.frequency = f0) :
    coherenceEvolution state dt 0 ≥ psiThreshold := by
  dsimp [coherenceEvolution, coherenceDerivative]
  have h_alpha_term : alpha * (1 - state.coherence) ≥ 0 := by
    have h_nonneg : 0 ≤ 1 - state.coherence := by linarith
    exact mul_nonneg (by norm_num [alpha]) h_nonneg
  have h_deriv_nonneg : alpha * (1 - state.coherence) + beta * (state.frequency - f0) ^ 2 + gamma * 0 ≥ 0 := by
    rw [h_freq]
    simp [beta, gamma]
    exact h_alpha_term
  have h_inc : dt * (alpha * (1 - state.coherence) + beta * (state.frequency - f0) ^ 2 + gamma * 0) ≥ 0 :=
    mul_nonneg h_dt h_deriv_nonneg
  linarith

def k15InitialState : K15Topology :=
  let nodes := fun node : K15Node =>
    { node := node
      coherence := 1
      frequency := f0
      phase := 0
      stabilityCount := minStability
      isActive := true }
  { nodes := nodes
    edges := (allNodes.product allNodes).filter (fun e => e.1 ≠ e.2)
    edgeWeight := fun _ => 0 }

lemma k15InitialNodeCoherenceOne (node : K15Node) :
    (k15InitialState.nodes node).coherence = 1 := by
  simp [k15InitialState]

lemma k15InitialNodeFrequency (node : K15Node) :
    (k15InitialState.nodes node).frequency = f0 := by
  simp [k15InitialState]

lemma k15InitialCouplingZero (top : K15Topology)
    (h_weights : ∀ e, top.edgeWeight e = 0) (node : K15Node) :
    (∑ neighbor in allNodes,
      if top.edges.contains (node, neighbor) then
        top.edgeWeight (node, neighbor) * (top.nodes neighbor).coherence
      else 0) = 0 := by
  apply Finset.sum_eq_zero
  intro neighbor hneighbor
  by_cases hEdge : top.edges.contains (node, neighbor)
  · simp [hEdge, h_weights]
  · simp [hEdge]

theorem k15InitialCoherence : k15GlobalCoherence k15InitialState := by
  dsimp [k15GlobalCoherence, k15Coherence]
  have h_sum : (∑ node in allNodes, (k15InitialState.nodes node).coherence) = (k15ActiveNodes : ℝ) := by
    simp [allNodes, k15InitialState, k15ActiveNodes]
  rw [h_sum]
  field_simp [k15ActiveNodes]
  norm_num [psiThreshold]

lemma evolveN_initial_nodes_one (dt : ℝ) :
    ∀ n node, ((evolveN k15InitialState dt n).nodes node).coherence = 1 := by
  intro n
  induction n with
  | zero =>
      intro node
      simp [evolveN, k15InitialState]
  | succ n ih =>
      intro node
      have h_prev : ((evolveN k15InitialState dt n).nodes node).coherence = 1 := ih node
      have h_prev_freq : ((evolveN k15InitialState dt n).nodes node).frequency = f0 := by
        induction n with
        | zero => simp [evolveN, k15InitialState]
        | succ n ihFreq =>
            simp [evolveN, k15Evolution, ihFreq]
      have h_coupling_zero :
          (∑ neighbor in allNodes,
            if (evolveN k15InitialState dt n).edges.contains (node, neighbor) then
              (evolveN k15InitialState dt n).edgeWeight (node, neighbor) *
                ((evolveN k15InitialState dt n).nodes neighbor).coherence
            else 0) = 0 := by
        refine k15InitialCouplingZero (evolveN k15InitialState dt n) ?_ node
        intro e
        induction n with
        | zero => simp [evolveN, k15InitialState]
        | succ n ihWeights => simp [evolveN, k15Evolution, ihWeights]
      simp [evolveN, k15Evolution, h_prev, h_prev_freq, h_coupling_zero, coherenceEvolution, coherenceDerivative, alpha, beta, gamma, k15NeighborCount]

theorem k15CoherencePreservation (dt : ℝ) (h_dt : 0 ≤ dt) :
    k15GlobalCoherence (k15Evolution k15InitialState dt) := by
  dsimp [k15GlobalCoherence, k15Coherence, k15Evolution]
  have h_nodes : ∀ node, (k15Evolution k15InitialState dt).nodes node |>.coherence = 1 := by
    intro node
    have h0 := evolveN_initial_nodes_one dt 1 node
    simpa [evolveN] using h0
  have h_sum : (∑ node in allNodes, (k15Evolution k15InitialState dt).nodes node |>.coherence) = (k15ActiveNodes : ℝ) := by
    apply Finset.sum_eq_card_nsmul
    intro node hnode
    simpa using h_nodes node
  rw [h_sum]
  field_simp [k15ActiveNodes]
  norm_num [psiThreshold]

theorem k15PerpetualCoherence (dt : ℝ) (h_dt : 0 ≤ dt) (n : ℕ) :
    k15GlobalCoherence (evolveN k15InitialState dt n) := by
  dsimp [k15GlobalCoherence, k15Coherence]
  have h_nodes : ∀ node, ((evolveN k15InitialState dt n).nodes node).coherence = 1 :=
    evolveN_initial_nodes_one dt n
  have h_sum : (∑ node in allNodes, ((evolveN k15InitialState dt n).nodes node).coherence) = (k15ActiveNodes : ℝ) := by
    apply Finset.sum_eq_card_nsmul
    intro node hnode
    simpa using h_nodes node
  rw [h_sum]
  field_simp [k15ActiveNodes]
  norm_num [psiThreshold]

end NOESIS.K15
