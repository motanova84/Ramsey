#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resonant Neural Networks using Ramsey Vibrational Connectivity
QCAL ∞³ Framework

This module implements neural networks with connectivity optimized
using vibrational Ramsey theory principles.

The network connectivity is based on resonance at f₀=141.7001 Hz,
ensuring emergence of processing cliques for information integration.

Author: José Manuel Mota Burruezo
Frequency: 141.7001 Hz - Campo QCAL ∞³
"""

import numpy as np
from typing import Tuple, List, Optional, Callable
from ramsey_vibracional import (
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    resonancia_detectada,
    estimar_conjetura
)


class ResonantNeuralNetwork:
    """
    Neural network with vibrational resonance-based connectivity.
    
    Instead of traditional fully-connected or convolutional layers,
    this network uses Ramsey-inspired connectivity where neurons
    connect based on frequency resonance.
    
    Parameters:
        neurons: Number of neurons in the network
        resonance_freq: Base resonance frequency (default: 141.7 Hz)
        clique_size: Minimum clique size for information processing
        epsilon: Resonance threshold (default: 0.001)
        learning_rate: Learning rate for weight updates (default: 0.01)
    """
    
    def __init__(
        self, 
        neurons: int = 1000,
        resonance_freq: float = 141.7,
        clique_size: int = 10,
        epsilon: float = 0.001,
        learning_rate: float = 0.01
    ):
        self.neurons = neurons
        self.f0 = resonance_freq
        self.clique_size = clique_size
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        
        # Initialize neuron frequencies
        np.random.seed(42)  # For reproducibility
        self.frequencies = np.random.uniform(0, self.f0, neurons)
        
        # Build connectivity based on resonance
        self.adjacency = self._build_connectivity()
        
        # Initialize weights for resonant connections
        self.weights = self._initialize_weights()
        
        # Neuron states
        self.states = np.zeros(neurons)
        
    def _build_connectivity(self) -> np.ndarray:
        """
        Build connectivity matrix based on vibrational resonance.
        
        Returns:
            Binary adjacency matrix (1 = connected, 0 = not connected)
        """
        adjacency = np.zeros((self.neurons, self.neurons), dtype=int)
        
        for i in range(self.neurons):
            for j in range(i + 1, self.neurons):
                if resonancia_detectada(
                    self.frequencies[i], 
                    self.frequencies[j], 
                    eps=self.epsilon, 
                    f0=self.f0
                ):
                    adjacency[i, j] = 1
                    adjacency[j, i] = 1
        
        return adjacency
    
    def _initialize_weights(self) -> np.ndarray:
        """
        Initialize connection weights.
        
        Weights are initialized based on frequency similarity,
        with stronger connections for closer resonances.
        
        Returns:
            Weight matrix
        """
        weights = np.zeros((self.neurons, self.neurons))
        
        for i in range(self.neurons):
            for j in range(self.neurons):
                if self.adjacency[i, j] == 1:
                    # Weight based on frequency similarity
                    freq_diff = abs(self.frequencies[i] - self.frequencies[j])
                    # Closer frequencies = stronger initial connection
                    weights[i, j] = np.exp(-freq_diff / self.f0)
        
        return weights
    
    def forward(self, input_vector: np.ndarray, activation: str = 'relu') -> np.ndarray:
        """
        Forward pass through the network.
        
        Args:
            input_vector: Input signal (length must match number of neurons)
            activation: Activation function ('relu', 'sigmoid', or 'tanh')
            
        Returns:
            Output states of all neurons
        """
        if len(input_vector) != self.neurons:
            raise ValueError(f"Input vector size {len(input_vector)} must match neurons {self.neurons}")
        
        # Set initial states from input
        self.states = input_vector.copy()
        
        # Propagate through resonant connections
        # Each neuron receives weighted sum from resonant neighbors
        new_states = np.zeros(self.neurons)
        
        for i in range(self.neurons):
            # Sum weighted inputs from connected neurons
            weighted_sum = np.sum(self.weights[i, :] * self.states)
            new_states[i] = weighted_sum
        
        # Apply activation function
        if activation == 'relu':
            self.states = np.maximum(0, new_states)
        elif activation == 'sigmoid':
            self.states = 1 / (1 + np.exp(-new_states))
        elif activation == 'tanh':
            self.states = np.tanh(new_states)
        else:
            self.states = new_states
        
        return self.states
    
    def find_processing_cliques(self, color: str = 'azul') -> List[Tuple]:
        """
        Find processing cliques in the network.
        
        Processing cliques are groups of strongly connected neurons
        that can integrate information coherently.
        
        Args:
            color: 'azul' for resonant (connected) or 'rojo' for non-resonant
            
        Returns:
            List of cliques (tuples of neuron indices)
        """
        # Build graph representation for clique finding
        grafo = {}
        for i in range(self.neurons):
            for j in range(i + 1, self.neurons):
                if self.adjacency[i, j] == 1:
                    grafo[(i, j)] = 'azul'
                else:
                    grafo[(i, j)] = 'rojo'
        
        # Find maximum clique
        max_clique = encontrar_clique_maximo(grafo, color)
        
        return [max_clique] if max_clique else []
    
    def get_network_stats(self) -> dict:
        """
        Get statistics about the network connectivity.
        
        Returns:
            Dictionary with network statistics
        """
        connections = np.sum(self.adjacency) // 2
        density = connections / (self.neurons * (self.neurons - 1) / 2)
        
        # Find processing cliques
        cliques = self.find_processing_cliques('azul')
        max_clique_size = len(cliques[0]) if cliques and cliques[0] else 0
        
        return {
            'neurons': self.neurons,
            'connections': connections,
            'density': density,
            'base_frequency': f"{self.f0} Hz",
            'max_clique_size': max_clique_size,
            'theoretical_rpsi': estimar_conjetura(self.clique_size, self.clique_size)
        }
    
    def visualize_connectivity(self, save_path: Optional[str] = None):
        """
        Visualize the network connectivity pattern.
        
        Args:
            save_path: Optional path to save the visualization
        """
        try:
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Plot 1: Adjacency matrix
            im = axes[0].imshow(self.adjacency, cmap='RdBu', interpolation='nearest')
            axes[0].set_title('Network Connectivity Matrix')
            axes[0].set_xlabel('Neuron Index')
            axes[0].set_ylabel('Neuron Index')
            plt.colorbar(im, ax=axes[0])
            
            # Plot 2: Frequency distribution
            axes[1].hist(self.frequencies, bins=50, color='purple', alpha=0.7)
            axes[1].set_title(f'Neuron Frequency Distribution (f₀={self.f0} Hz)')
            axes[1].set_xlabel('Frequency (Hz)')
            axes[1].set_ylabel('Count')
            axes[1].axvline(self.f0, color='red', linestyle='--', label='f₀')
            axes[1].legend()
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"   Visualization saved to {save_path}")
            else:
                plt.show()
            
        except ImportError:
            print("   Matplotlib not available for visualization")


def demo_resonant_neural_network():
    """Demonstrate the resonant neural network."""
    print("=" * 70)
    print("  Resonant Neural Network Demo")
    print("  Connectivity based on Ramsey Vibrational Theory")
    print("  Frequency: 141.7001 Hz - Campo QCAL ∞³")
    print("=" * 70)
    print()
    
    # Create network
    print("1. NETWORK INITIALIZATION")
    print("-" * 70)
    rnn = ResonantNeuralNetwork(
        neurons=100,
        resonance_freq=141.7,
        clique_size=5,
        epsilon=0.001
    )
    
    stats = rnn.get_network_stats()
    print(f"   Neurons: {stats['neurons']}")
    print(f"   Connections: {stats['connections']}")
    print(f"   Connection density: {stats['density']:.4f}")
    print(f"   Base frequency: {stats['base_frequency']}")
    print(f"   Maximum processing clique: {stats['max_clique_size']} neurons")
    print(f"   Theoretical R_ψ({rnn.clique_size},{rnn.clique_size}): ~{stats['theoretical_rpsi']}")
    print()
    
    # Test forward pass
    print("2. FORWARD PROPAGATION TEST")
    print("-" * 70)
    input_signal = np.random.randn(100)
    print(f"   Input signal: {input_signal.shape}")
    
    output = rnn.forward(input_signal, activation='relu')
    print(f"   Output signal: {output.shape}")
    print(f"   Active neurons: {np.sum(output > 0)}")
    print(f"   Mean activation: {np.mean(output):.4f}")
    print(f"   Max activation: {np.max(output):.4f}")
    print()
    
    # Analyze processing cliques
    print("3. PROCESSING CLIQUE ANALYSIS")
    print("-" * 70)
    cliques = rnn.find_processing_cliques('azul')
    
    if cliques and cliques[0]:
        print(f"   Found {len(cliques)} processing clique(s)")
        print(f"   Maximum clique size: {len(cliques[0])}")
        print(f"   Clique neurons: {cliques[0][:10]}..." if len(cliques[0]) > 10 else f"   Clique neurons: {cliques[0]}")
    else:
        print("   No large processing cliques found")
    print()
    
    # Comparison with traditional networks
    print("4. COMPARISON WITH TRADITIONAL NETWORKS")
    print("-" * 70)
    traditional_connections = 100 * 99 / 2  # Fully connected
    sparse_connections = 100 * 10  # Sparse network
    
    print(f"   Fully connected: {int(traditional_connections)} connections")
    print(f"   Sparse network: {int(sparse_connections)} connections")
    print(f"   Resonant network: {stats['connections']} connections")
    print(f"   Reduction vs. fully connected: {(1 - stats['connections']/traditional_connections)*100:.1f}%")
    print()
    
    print("=" * 70)
    print("  Advantages of Resonant Networks:")
    print("-" * 70)
    print("  • Optimal connectivity based on frequency resonance")
    print("  • Natural emergence of processing cliques")
    print("  • Reduced connections while maintaining information flow")
    print("  • Quantum coherence at f₀=141.7 Hz for enhanced processing")
    print("  • Biologically-inspired oscillatory dynamics")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_resonant_neural_network()
