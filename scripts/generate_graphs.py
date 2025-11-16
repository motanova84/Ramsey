#!/usr/bin/env python3
"""
Generate Vibrational Ramsey Graphs

This script generates graph structures for vibrational Ramsey theory,
computing frequency assignments and colorings based on the resonance model.

Usage:
    python generate_graphs.py --n=15 --r=5 --s=5 --epsilon=0.05
"""

import sys
import os
import argparse
import json
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from ramsey_vibracional import (
        ramsey_vibracional_unsat,
        generar_coloracion_vibracional,
        encontrar_clique_maximo
    )
except ImportError:
    print("Warning: ramsey_vibracional module not found. Using dummy functions.")
    def ramsey_vibracional_unsat(n, r, s, eps=0.001, f0=141.7001, grid=128):
        return False
    def generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001):
        return {}
    def encontrar_clique_maximo(grafo, color):
        return set()


def generate_frequency_assignment(n, f0=141.7001, grid=128):
    """Generate uniform frequency assignment for n vertices."""
    return [f0 * i / grid for i in range(n)]


def generate_vibrational_graph(n, r, s, epsilon=0.05, f0=141.7001, grid=128):
    """
    Generate a vibrational Ramsey graph.
    
    Args:
        n: Number of vertices
        r: Red clique size to avoid
        s: Blue clique size to avoid
        epsilon: Resonance threshold
        f0: Base frequency (Hz)
        grid: Frequency grid resolution
        
    Returns:
        dict: Graph data including vertices, edges, and coloring
    """
    frequencies = generate_frequency_assignment(n, f0, grid)
    
    # Generate coloring based on resonance
    coloring = generar_coloracion_vibracional(frequencies, eps=epsilon, f0=f0)
    
    # Check if configuration is UNSAT
    is_unsat = ramsey_vibracional_unsat(n, r, s, eps=epsilon, f0=f0, grid=grid)
    
    graph_data = {
        "vertices": n,
        "parameters": {
            "r": r,
            "s": s,
            "epsilon": epsilon,
            "f0": f0,
            "grid": grid
        },
        "frequencies": frequencies,
        "coloring": coloring,
        "is_unsat": is_unsat,
        "properties": {
            "no_red_Kr": is_unsat,
            "no_blue_Ks": is_unsat
        }
    }
    
    return graph_data


def main():
    parser = argparse.ArgumentParser(
        description='Generate vibrational Ramsey graphs'
    )
    parser.add_argument('--n', type=int, default=15,
                        help='Number of vertices (default: 15)')
    parser.add_argument('--r', type=int, default=5,
                        help='Red clique size (default: 5)')
    parser.add_argument('--s', type=int, default=5,
                        help='Blue clique size (default: 5)')
    parser.add_argument('--epsilon', type=float, default=0.05,
                        help='Resonance threshold (default: 0.05)')
    parser.add_argument('--f0', type=float, default=141.7001,
                        help='Base frequency in Hz (default: 141.7001)')
    parser.add_argument('--grid', type=int, default=128,
                        help='Frequency grid resolution (default: 128)')
    parser.add_argument('--output', type=str, default='graph_data.json',
                        help='Output file path (default: graph_data.json)')
    
    args = parser.parse_args()
    
    print(f"Generating vibrational Ramsey graph...")
    print(f"Parameters: n={args.n}, r={args.r}, s={args.s}, ε={args.epsilon}")
    
    graph_data = generate_vibrational_graph(
        args.n, args.r, args.s, args.epsilon, args.f0, args.grid
    )
    
    # Save to file
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"Graph data saved to: {output_path}")
    print(f"Is UNSAT: {graph_data['is_unsat']}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
