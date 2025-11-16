#!/usr/bin/env python3
"""
Vibrational Model Plotting

This script visualizes the vibrational Ramsey model, including
frequency assignments, colorings, and graph structures.

Usage:
    python vibrational_model_plot.py --input=data/rpsi_vibration_model.json
"""

import sys
import os
import argparse
import json
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib")


def plot_frequency_distribution(frequencies, output_path='frequency_dist.png'):
    """Plot the distribution of frequencies on the unit circle."""
    if not HAS_MATPLOTLIB:
        print("Skipping plot: matplotlib not available")
        return
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Convert frequencies to angles (0 to 2π)
    f0 = max(frequencies) if frequencies else 141.7001
    angles = [2 * np.pi * f / f0 for f in frequencies]
    
    # Plot points on circle
    radii = [1.0] * len(angles)
    ax.scatter(angles, radii, c='blue', s=100, alpha=0.6, edgecolors='black')
    
    # Add labels
    for i, (angle, r) in enumerate(zip(angles, radii)):
        ax.text(angle, r + 0.1, f'v{i}', ha='center', va='center')
    
    ax.set_ylim(0, 1.3)
    ax.set_title('Vibrational Ramsey Frequency Distribution', pad=20)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Frequency distribution plot saved to: {output_path}")


def plot_coloring_graph(n, coloring, output_path='coloring_graph.png'):
    """Plot the graph with edge coloring."""
    if not HAS_MATPLOTLIB:
        print("Skipping plot: matplotlib not available")
        return
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Position vertices in a circle
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    positions = [(np.cos(a), np.sin(a)) for a in angles]
    
    # Draw edges
    for (i, j), color in coloring.items():
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        edge_color = 'red' if color == 'rojo' else 'blue'
        ax.plot([x1, x2], [y1, y2], color=edge_color, alpha=0.3, linewidth=0.5)
    
    # Draw vertices
    for i, (x, y) in enumerate(positions):
        circle = Circle((x, y), 0.05, color='black', zorder=10)
        ax.add_patch(circle)
        ax.text(x, y, f'{i}', ha='center', va='center', 
                color='white', fontsize=8, zorder=11)
    
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Vibrational Ramsey Graph Coloring', fontsize=16)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=2, label='Red (resonant)'),
        Line2D([0], [0], color='blue', linewidth=2, label='Blue (non-resonant)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Coloring graph plot saved to: {output_path}")


def plot_from_model(model_path, output_dir='.'):
    """Create plots from a vibrational model JSON file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    with open(model_path, 'r') as f:
        model = json.load(f)
    
    frequencies = model.get('frequency_assignment', {}).get('frequencies', [])
    n = model.get('frequency_assignment', {}).get('n', len(frequencies))
    
    print(f"Loaded model: {model.get('model', 'unknown')}")
    print(f"Vertices: {n}")
    print(f"Parameters: r={model['parameters']['r']}, s={model['parameters']['s']}")
    
    # Plot frequency distribution
    if frequencies:
        plot_frequency_distribution(
            frequencies, 
            output_dir / 'frequency_distribution.png'
        )
    
    # Note: Actual coloring would need to be computed or loaded
    print("\nNote: To plot the full graph coloring, run generate_graphs.py first")


def main():
    parser = argparse.ArgumentParser(
        description='Visualize vibrational Ramsey models'
    )
    parser.add_argument('--input', type=str, 
                        default='../data/rpsi_vibration_model.json',
                        help='Input model JSON file')
    parser.add_argument('--output', type=str, default='.',
                        help='Output directory for plots')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    plot_from_model(input_path, args.output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
