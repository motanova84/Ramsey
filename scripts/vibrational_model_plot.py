#!/usr/bin/env python3
"""
vibrational_model_plot.py - Visualize vibrational Ramsey structures

Creates plots showing:
1. Frequency distribution on unit circle
2. Edge coloring based on resonance
3. Network structure with harmonic connections
4. Comparison of classical vs vibrational bounds
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from generate_graphs import generate_frequencies, vibrational_coloring


def plot_frequency_circle(frequencies, f0=141.7001, epsilon=0.001, 
                         filename='frequency_circle.png'):
    """
    Plot frequencies on unit circle with resonance bands.
    
    Args:
        frequencies: Array of frequencies
        f0: Base frequency
        epsilon: Resonance threshold
        filename: Output file
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Normalize frequencies to [0, 2π) for circular plot
    angles = 2 * np.pi * frequencies / f0
    
    # Plot unit circle
    circle = Circle((0, 0), 1, fill=False, color='black', linewidth=2)
    ax.add_patch(circle)
    
    # Plot frequency points
    x = np.cos(angles)
    y = np.sin(angles)
    ax.scatter(x, y, s=100, c='blue', alpha=0.7, zorder=3)
    
    # Add resonance bands (epsilon regions)
    eps_angle = 2 * np.pi * epsilon / f0
    for angle in angles:
        # Draw small arc showing resonance region
        arc_angles = np.linspace(angle - eps_angle, angle + eps_angle, 20)
        arc_x = 1.05 * np.cos(arc_angles)
        arc_y = 1.05 * np.sin(arc_angles)
        ax.plot(arc_x, arc_y, 'r-', alpha=0.3, linewidth=2)
    
    # Labels
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Vibrational Frequencies on Unit Circle\nf₀ = {f0} Hz, ε = {epsilon} Hz', 
                 fontsize=14)
    ax.set_xlabel('cos(2πω/f₀)', fontsize=12)
    ax.set_ylabel('sin(2πω/f₀)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {filename}")


def plot_network_structure(n, coloring, filename='network_structure.png'):
    """
    Plot network with colored edges.
    
    Args:
        n: Number of vertices
        coloring: Edge coloring dictionary
        filename: Output file
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Position vertices in circle
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    
    # Draw edges
    for (i, j), color in coloring.items():
        x = [pos[i][0], pos[j][0]]
        y = [pos[i][1], pos[j][1]]
        edge_color = 'red' if color else 'blue'
        edge_alpha = 0.3 if color else 0.1
        ax.plot(x, y, color=edge_color, alpha=edge_alpha, linewidth=0.5, zorder=1)
    
    # Draw vertices
    for i, (x, y) in pos.items():
        ax.scatter(x, y, s=200, c='yellow', edgecolors='black', 
                  linewidths=2, zorder=2)
        ax.text(x * 1.1, y * 1.1, str(i), fontsize=8, ha='center', va='center')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Vibrational Network Structure (n={n})\nRed = Resonant, Blue = Non-resonant',
                fontsize=14)
    
    # Add legend
    red_count = sum(1 for c in coloring.values() if c)
    blue_count = len(coloring) - red_count
    ax.text(0, -1.4, f'Red edges: {red_count} | Blue edges: {blue_count}',
           ha='center', fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat'))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {filename}")


def plot_bounds_comparison(filename='bounds_comparison.png'):
    """
    Plot comparison of classical vs vibrational Ramsey bounds.
    
    Args:
        filename: Output file
    """
    # Known values
    cases = ['(3,3)', '(3,4)', '(4,4)', '(3,5)', '(4,5)', '(5,5)']
    r_vals = [3, 3, 4, 3, 4, 5]
    s_vals = [3, 4, 4, 5, 5, 5]
    classical = [6, 9, 18, 14, 25, 43]
    vibrational = [6, 8, 11, 9, 13, 16]  # From table in README
    
    x = np.arange(len(cases))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars1 = ax.bar(x - width/2, classical, width, label='Classical R(r,s)',
                   color='steelblue', alpha=0.8)
    bars2 = ax.bar(x + width/2, vibrational, width, label='Vibrational Rψ(r,s)',
                   color='coral', alpha=0.8)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)
    
    ax.set_xlabel('Ramsey Parameters', fontsize=12)
    ax.set_ylabel('Bound Value', fontsize=12)
    ax.set_title('Classical vs Vibrational Ramsey Bounds\nf₀ = 141.7001 Hz',
                fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(cases)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add improvement percentages
    for i, (c, v) in enumerate(zip(classical, vibrational)):
        if c > v:
            improvement = (c - v) / c * 100
            ax.text(i, max(c, v) + 1, f'-{improvement:.0f}%',
                   ha='center', fontsize=9, color='green', weight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {filename}")


def plot_f0_resonance(filename='f0_resonance.png'):
    """
    Plot the role of f₀ = 141.7001 Hz in the model.
    
    Args:
        filename: Output file
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left plot: f₀ spectrum
    f0 = 141.7001
    freq_range = np.linspace(0, f0, 1000)
    resonance = np.exp(-((freq_range - f0/2)**2) / (f0/10)**2)
    
    ax1.plot(freq_range, resonance, 'b-', linewidth=2)
    ax1.axvline(f0/2, color='red', linestyle='--', label=f'f₀/2 = {f0/2:.1f} Hz')
    ax1.axvline(f0, color='green', linestyle='--', label=f'f₀ = {f0} Hz')
    ax1.fill_between(freq_range, 0, resonance, alpha=0.3)
    ax1.set_xlabel('Frequency (Hz)', fontsize=12)
    ax1.set_ylabel('Resonance Amplitude', fontsize=12)
    ax1.set_title('Harmonic Structure at f₀ = 141.7001 Hz', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    
    # Right plot: Growth comparison
    rs = np.arange(2, 10)
    classical_growth = 2**(rs/2)  # Exponential
    vibrational_growth = np.sqrt(rs) * np.log(rs + 1)  # Polynomial
    
    ax2.semilogy(rs, classical_growth, 'b-o', label='Classical: 2^(r/2)', linewidth=2)
    ax2.semilogy(rs, vibrational_growth, 'r-s', label='Vibrational: √r ln r', linewidth=2)
    ax2.set_xlabel('Clique size r', fontsize=12)
    ax2.set_ylabel('Ramsey bound (log scale)', fontsize=12)
    ax2.set_title('Growth Rate Comparison', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved: {filename}")


def main():
    """Generate all visualizations."""
    print("Vibrational Ramsey Model Visualization")
    print("=" * 50)
    
    # Example with n=20 vertices
    n = 20
    f0 = 141.7001
    epsilon = 0.001
    
    print(f"\nGenerating visualizations for n={n}, f₀={f0} Hz")
    
    # Generate data
    frequencies = generate_frequencies(n, f0, seed=42)
    coloring = vibrational_coloring(frequencies, epsilon, f0)
    
    # Create plots
    print("\nCreating plots...")
    plot_frequency_circle(frequencies, f0, epsilon)
    plot_network_structure(n, coloring)
    plot_bounds_comparison()
    plot_f0_resonance()
    
    print("\n✓ All visualizations generated")
    print("\nOutput files:")
    print("  - frequency_circle.png")
    print("  - network_structure.png")
    print("  - bounds_comparison.png")
    print("  - f0_resonance.png")


if __name__ == "__main__":
    main()
