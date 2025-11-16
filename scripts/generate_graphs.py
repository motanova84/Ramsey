#!/usr/bin/env python3
"""
Script to generate vibrational graphs for Ramsey R_ψ(5,5) proof
Generates graph instances with frequency assignments
"""

import json
import numpy as np
from pathlib import Path

def generate_vibrational_graph(n, f0=141.7001, seed=None):
    """
    Generate a vibrational graph with n vertices.
    
    Args:
        n: Number of vertices
        f0: Base frequency (Hz)
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary with graph data
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate frequency assignments
    frequencies = np.random.uniform(0, f0, n)
    
    graph_data = {
        "n": n,
        "f0": f0,
        "frequencies": frequencies.tolist(),
        "description": f"Vibrational graph with {n} vertices"
    }
    
    return graph_data

def main():
    """Generate graphs for R_ψ(5,5) verification"""
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    # Generate graph for n=16 (the bound for R_ψ(5,5))
    graph = generate_vibrational_graph(16, seed=42)
    
    output_file = output_dir / "graph_r55_n16.json"
    with open(output_file, 'w') as f:
        json.dump(graph, f, indent=2)
    
    print(f"Generated vibrational graph saved to {output_file}")

if __name__ == "__main__":
    main()
