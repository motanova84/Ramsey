#!/usr/bin/env python3
"""
Script to plot resonance patterns for vibrational Ramsey graphs
Visualizes frequency distributions and resonance structure
"""

import json
import numpy as np
from pathlib import Path

def plot_resonance_pattern(frequencies, f0=141.7001, epsilon=0.001):
    """
    Plot the resonance pattern for a set of frequencies.
    
    Args:
        frequencies: List of vertex frequencies
        f0: Base frequency
        epsilon: Resonance threshold
    """
    print("Resonance Pattern Analysis")
    print(f"Base frequency f₀ = {f0} Hz")
    print(f"Resonance threshold ε = {epsilon}")
    print(f"Number of vertices: {len(frequencies)}")
    
    # Count resonant pairs
    resonant_count = 0
    total_pairs = len(frequencies) * (len(frequencies) - 1) // 2
    
    for i in range(len(frequencies)):
        for j in range(i + 1, len(frequencies)):
            diff = abs(frequencies[i] - frequencies[j])
            if diff < epsilon or (f0 - diff) < epsilon:
                resonant_count += 1
    
    print(f"Resonant pairs: {resonant_count} / {total_pairs}")
    print(f"Resonance density: {resonant_count / total_pairs:.2%}")
    
    return resonant_count, total_pairs

def main():
    """Generate resonance plots"""
    print("Vibrational Model Plotting Tool")
    print("=" * 50)
    
    # Example: Plot for n=16 vertices
    np.random.seed(42)
    frequencies = np.random.uniform(0, 141.7001, 16)
    
    plot_resonance_pattern(frequencies)
    
    print("\n✓ Resonance analysis complete")
    print("  (Note: Full visualization requires matplotlib)")

if __name__ == "__main__":
    main()
