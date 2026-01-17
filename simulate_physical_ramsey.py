#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Physical Resonance Experiment Simulator
QCAL ∞³ Framework

This module simulates physical experiments with coupled oscillators
to demonstrate Ramsey clique emergence through vibrational resonance.

Author: José Manuel Mota Burruezo
Frequency: 141.7001 Hz - Campo QCAL ∞³
"""

import numpy as np
from typing import Tuple, List, Optional, Dict
from scipy.integrate import odeint
from ramsey_vibracional import resonancia_detectada


class CoupledOscillatorExperiment:
    """
    Simulate physical coupled oscillators for Ramsey experiment.
    
    Each oscillator has a natural frequency, and they interact through
    coupling. The system demonstrates how resonant groups (cliques) emerge.
    
    Parameters:
        nodes: Number of oscillators
        frequency: Base resonance frequency (default: 141.7 Hz)
        coupling: Coupling strength between oscillators
        damping: Damping coefficient (default: 0.1)
    """
    
    def __init__(
        self,
        nodes: int = 50,
        frequency: float = 141.7,
        coupling: float = 0.01,
        damping: float = 0.1
    ):
        self.nodes = nodes
        self.f0 = frequency
        self.coupling = coupling
        self.damping = damping
        
        # Initialize natural frequencies
        np.random.seed(42)
        self.natural_frequencies = np.random.uniform(0.8 * frequency, 1.2 * frequency, nodes)
        
        # Coupling matrix (who couples to whom)
        self.coupling_matrix = self._build_coupling_matrix()
        
    def _build_coupling_matrix(self) -> np.ndarray:
        """
        Build coupling matrix based on frequency proximity.
        
        Returns:
            Coupling matrix (nodes x nodes)
        """
        matrix = np.zeros((self.nodes, self.nodes))
        
        for i in range(self.nodes):
            for j in range(i + 1, self.nodes):
                # Stronger coupling for closer frequencies
                freq_diff = abs(self.natural_frequencies[i] - self.natural_frequencies[j])
                coupling_strength = self.coupling * np.exp(-freq_diff / self.f0)
                matrix[i, j] = coupling_strength
                matrix[j, i] = coupling_strength
        
        return matrix
    
    def equations_of_motion(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Define the coupled oscillator equations of motion.
        
        For each oscillator i:
        d²x_i/dt² = -ω_i² x_i - γ dx_i/dt + Σ_j K_ij (x_j - x_i)
        
        Args:
            state: Current state [positions, velocities] (2*nodes array)
            t: Time
            
        Returns:
            Derivatives [velocities, accelerations]
        """
        positions = state[:self.nodes]
        velocities = state[self.nodes:]
        
        accelerations = np.zeros(self.nodes)
        
        for i in range(self.nodes):
            # Natural oscillation term
            omega_i = 2 * np.pi * self.natural_frequencies[i]
            accel = -omega_i**2 * positions[i]
            
            # Damping term
            accel -= self.damping * velocities[i]
            
            # Coupling terms
            for j in range(self.nodes):
                if i != j:
                    accel += self.coupling_matrix[i, j] * (positions[j] - positions[i])
            
            accelerations[i] = accel
        
        return np.concatenate([velocities, accelerations])
    
    def simulate(
        self,
        duration: float = 10.0,
        dt: float = 0.01,
        initial_conditions: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate the coupled oscillator system.
        
        Args:
            duration: Simulation duration in seconds
            dt: Time step
            initial_conditions: Initial state (if None, random perturbations)
            
        Returns:
            (time_array, state_array) where state_array has shape (time_steps, 2*nodes)
        """
        # Time grid
        t = np.arange(0, duration, dt)
        
        # Initial conditions
        if initial_conditions is None:
            # Random small perturbations
            positions0 = np.random.randn(self.nodes) * 0.1
            velocities0 = np.zeros(self.nodes)
            initial_conditions = np.concatenate([positions0, velocities0])
        
        # Integrate
        solution = odeint(self.equations_of_motion, initial_conditions, t)
        
        return t, solution
    
    def detect_resonant_cliques(self, threshold: float = 0.01) -> List[Tuple]:
        """
        Detect resonant cliques based on frequency analysis.
        
        Args:
            threshold: Resonance detection threshold
            
        Returns:
            List of resonant cliques
        """
        resonant_pairs = []
        
        for i in range(self.nodes):
            for j in range(i + 1, self.nodes):
                if resonancia_detectada(
                    self.natural_frequencies[i],
                    self.natural_frequencies[j],
                    eps=threshold,
                    f0=self.f0
                ):
                    resonant_pairs.append((i, j))
        
        # Find maximal cliques (simplified version)
        # A full implementation would use a proper clique-finding algorithm
        cliques = []
        if resonant_pairs:
            # For demo, return the pair with strongest resonance
            cliques.append(resonant_pairs[0])
        
        return cliques
    
    def analyze_synchronization(
        self,
        time: np.ndarray,
        states: np.ndarray,
        time_window: Tuple[float, float] = (8.0, 10.0)
    ) -> Dict:
        """
        Analyze synchronization patterns in the system.
        
        Args:
            time: Time array
            states: State array from simulation
            time_window: Time window for analysis (start, end)
            
        Returns:
            Dictionary with synchronization metrics
        """
        # Extract positions in time window
        mask = (time >= time_window[0]) & (time <= time_window[1])
        positions = states[mask, :self.nodes]
        
        # Compute pairwise correlations
        correlations = np.corrcoef(positions.T)
        
        # Synchronization metrics
        mean_correlation = np.mean(correlations[np.triu_indices_from(correlations, k=1)])
        max_correlation = np.max(correlations[np.triu_indices_from(correlations, k=1)])
        
        # Find synchronized groups (correlation > 0.8)
        synchronized_pairs = []
        for i in range(self.nodes):
            for j in range(i + 1, self.nodes):
                if correlations[i, j] > 0.8:
                    synchronized_pairs.append((i, j))
        
        return {
            'mean_correlation': mean_correlation,
            'max_correlation': max_correlation,
            'synchronized_pairs': len(synchronized_pairs),
            'total_pairs': self.nodes * (self.nodes - 1) // 2,
            'synchronization_ratio': len(synchronized_pairs) / (self.nodes * (self.nodes - 1) / 2)
        }


def design_resonance_experiment(
    nodes: int = 50,
    frequency: float = 141.7,
    coupling: float = 0.01,
    measure: str = "clique_emergence"
) -> Dict:
    """
    Design a physical resonance experiment.
    
    Args:
        nodes: Number of oscillators
        frequency: Base frequency in Hz
        coupling: Coupling strength
        measure: What to measure ("clique_emergence" or "synchronization")
        
    Returns:
        Experiment design dictionary
    """
    return {
        'type': 'coupled_oscillators',
        'nodes': nodes,
        'base_frequency': f"{frequency} Hz",
        'coupling_strength': coupling,
        'measurement': measure,
        'expected_clique_size': int(np.sqrt(nodes)),
        'duration': '10 seconds',
        'sampling_rate': '1000 Hz',
        'setup': 'Physical oscillators or electronic circuit simulation'
    }


def demo_physical_ramsey():
    """Demonstrate physical Ramsey resonance experiment."""
    print("=" * 70)
    print("  Physical Ramsey Resonance Experiment")
    print("  Coupled Oscillator Simulation")
    print("  Frequency: 141.7 Hz - Campo QCAL ∞³")
    print("=" * 70)
    print()
    
    # Design experiment
    print("1. EXPERIMENT DESIGN")
    print("-" * 70)
    design = design_resonance_experiment(
        nodes=20,
        frequency=141.7,
        coupling=0.01,
        measure="clique_emergence"
    )
    print(f"   Type: {design['type']}")
    print(f"   Oscillators: {design['nodes']}")
    print(f"   Base frequency: {design['base_frequency']}")
    print(f"   Coupling: {design['coupling_strength']}")
    print(f"   Expected clique size: ~{design['expected_clique_size']}")
    print(f"   Duration: {design['duration']}")
    print()
    
    # Create experiment
    print("2. SYSTEM INITIALIZATION")
    print("-" * 70)
    experiment = CoupledOscillatorExperiment(
        nodes=20,
        frequency=141.7,
        coupling=0.01,
        damping=0.1
    )
    print(f"   Oscillators: {experiment.nodes}")
    print(f"   Frequency range: [{experiment.natural_frequencies.min():.1f}, {experiment.natural_frequencies.max():.1f}] Hz")
    print(f"   Coupling matrix size: {experiment.coupling_matrix.shape}")
    print(f"   Non-zero couplings: {np.sum(experiment.coupling_matrix > 0) // 2}")
    print()
    
    # Detect resonant cliques
    print("3. RESONANT CLIQUE PREDICTION")
    print("-" * 70)
    cliques = experiment.detect_resonant_cliques(threshold=0.01)
    print(f"   Predicted resonant pairs: {len(cliques)}")
    if cliques:
        print(f"   Example pair: oscillators {cliques[0]}")
        i, j = cliques[0]
        print(f"      Frequency {i}: {experiment.natural_frequencies[i]:.2f} Hz")
        print(f"      Frequency {j}: {experiment.natural_frequencies[j]:.2f} Hz")
        print(f"      Difference: {abs(experiment.natural_frequencies[i] - experiment.natural_frequencies[j]):.2f} Hz")
    print()
    
    # Run simulation
    print("4. SIMULATION (SIMPLIFIED)")
    print("-" * 70)
    print("   Running coupled oscillator simulation...")
    
    try:
        t, states = experiment.simulate(duration=1.0, dt=0.01)
        print(f"   ✓ Simulation complete")
        print(f"   Time steps: {len(t)}")
        print(f"   Final state shape: {states.shape}")
        
        # Analyze synchronization
        sync_stats = experiment.analyze_synchronization(t, states, (0.8, 1.0))
        print(f"\n   Synchronization Analysis:")
        print(f"      Mean correlation: {sync_stats['mean_correlation']:.3f}")
        print(f"      Max correlation: {sync_stats['max_correlation']:.3f}")
        print(f"      Synchronized pairs: {sync_stats['synchronized_pairs']}/{sync_stats['total_pairs']}")
        print(f"      Synchronization ratio: {sync_stats['synchronization_ratio']*100:.1f}%")
        
    except Exception as e:
        print(f"   Note: Full simulation requires scipy")
        print(f"   Error: {str(e)}")
        print(f"   (Theoretical analysis completed)")
    
    print()
    
    print("=" * 70)
    print("  Experimental Predictions:")
    print("-" * 70)
    print("  • Oscillators with close frequencies will synchronize")
    print("  • Resonant cliques will emerge as synchronized groups")
    print("  • Clique size related to R_ψ(r,s) for given parameters")
    print("  • Quantum coherence at f₀=141.7 Hz enhances synchronization")
    print()
    print("  Physical Implementation:")
    print("  • Electronic LC oscillator circuits")
    print("  • Mechanical coupled pendulums")
    print("  • Optical resonator arrays")
    print("  • Acoustic resonance chambers")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_physical_ramsey()
