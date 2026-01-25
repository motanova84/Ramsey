#!/usr/bin/env python3
"""
generate_graphs.py - Generate graph colorings and CNF formulas for Ramsey verification

This script generates:
1. Random vibrational frequency assignments
2. Corresponding edge colorings
3. CNF formulas for SAT solving
4. Verification data structures
"""

import numpy as np
import json
from itertools import combinations
from typing import List, Tuple, Dict


def generate_frequencies(n: int, f0: float = 141.7001, seed: int = None) -> np.ndarray:
    """
    Generate random frequency assignments for n vertices.
    
    Args:
        n: Number of vertices
        f0: Base frequency (Hz)
        seed: Random seed for reproducibility
    
    Returns:
        Array of n frequencies in [0, f0)
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.uniform(0, f0, n)


def vibrational_coloring(frequencies: np.ndarray, epsilon: float = 0.001, 
                         f0: float = 141.7001) -> Dict[Tuple[int, int], bool]:
    """
    Compute edge coloring based on vibrational resonance.
    
    Args:
        frequencies: Frequency for each vertex
        epsilon: Resonance threshold
        f0: Base frequency
    
    Returns:
        Dictionary mapping (i,j) -> color (True=Red/resonant, False=Blue)
    """
    n = len(frequencies)
    coloring = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            # Compute frequency difference with modular arithmetic
            diff = abs(frequencies[i] - frequencies[j])
            # Check resonance condition
            is_resonant = (diff < epsilon) or (f0 - diff < epsilon)
            coloring[(i, j)] = is_resonant
    
    return coloring


def generate_cnf_formula(n: int, r: int, s: int, 
                         output_file: str = None) -> Tuple[List[List[int]], int]:
    """
    Generate CNF formula for Ramsey R(r,s) on K_n.
    
    Variables: edge(i,j) for i < j encoded as integers 1..num_edges
    Clauses:
        - For each r-subset: at least one edge is not red (avoids red r-clique)
        - For each s-subset: at least one edge is red (avoids blue s-clique)
    
    Args:
        n: Number of vertices
        r: Red clique size to avoid
        s: Blue clique size to avoid
        output_file: Optional file to write CNF
    
    Returns:
        (clauses, num_variables)
    """
    # Create edge to variable mapping
    edge_to_var = {}
    var_num = 1
    for i in range(n):
        for j in range(i + 1, n):
            edge_to_var[(i, j)] = var_num
            var_num += 1
    
    num_vars = len(edge_to_var)
    clauses = []
    
    # For each r-subset, forbid all-red (at least one blue edge)
    for subset in combinations(range(n), r):
        clause = []
        for i, j in combinations(subset, 2):
            edge = (min(i, j), max(i, j))
            # Negative literal means edge must be blue
            clause.append(-edge_to_var[edge])
        clauses.append(clause)
    
    # For each s-subset, forbid all-blue (at least one red edge)
    for subset in combinations(range(n), s):
        clause = []
        for i, j in combinations(subset, 2):
            edge = (min(i, j), max(i, j))
            # Positive literal means edge must be red
            clause.append(edge_to_var[edge])
        clauses.append(clause)
    
    # Write to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"p cnf {num_vars} {len(clauses)}\n")
            for clause in clauses:
                f.write(" ".join(map(str, clause)) + " 0\n")
    
    return clauses, num_vars


def check_cliques(coloring: Dict[Tuple[int, int], bool], n: int, 
                  r: int, s: int) -> Dict[str, any]:
    """
    Check if coloring contains monochromatic cliques.
    
    Args:
        coloring: Edge coloring dictionary
        n: Number of vertices
        r: Red clique size to check
        s: Blue clique size to check
    
    Returns:
        Dictionary with results
    """
    # Check for red r-cliques
    red_clique_found = False
    for subset in combinations(range(n), r):
        all_red = True
        for i, j in combinations(subset, 2):
            edge = (min(i, j), max(i, j))
            if not coloring.get(edge, False):
                all_red = False
                break
        if all_red:
            red_clique_found = True
            break
    
    # Check for blue s-cliques
    blue_clique_found = False
    for subset in combinations(range(n), s):
        all_blue = True
        for i, j in combinations(subset, 2):
            edge = (min(i, j), max(i, j))
            if coloring.get(edge, False):
                all_blue = False
                break
        if all_blue:
            blue_clique_found = True
            break
    
    return {
        'has_red_clique': red_clique_found,
        'has_blue_clique': blue_clique_found,
        'is_valid': not (red_clique_found or blue_clique_found)
    }


def main():
    """Example usage and testing."""
    print("Ramsey Graph Generation Tool")
    print("=" * 50)
    
    # Example: R(5,5) with n=43
    n, r, s = 43, 5, 5
    f0 = 141.7001
    epsilon = 0.001
    
    print(f"\nGenerating for R({r},{s}) with n={n}")
    print(f"Parameters: f₀={f0} Hz, ε={epsilon}")
    
    # Generate frequencies
    frequencies = generate_frequencies(n, f0, seed=42)
    print(f"\nGenerated {n} frequencies")
    print(f"Sample: {frequencies[:5]}")
    
    # Compute coloring
    coloring = vibrational_coloring(frequencies, epsilon, f0)
    red_edges = sum(1 for c in coloring.values() if c)
    blue_edges = len(coloring) - red_edges
    print(f"\nColoring: {red_edges} red edges, {blue_edges} blue edges")
    
    # Check for cliques
    result = check_cliques(coloring, n, r, s)
    print(f"\nClique check:")
    print(f"  Red {r}-clique: {result['has_red_clique']}")
    print(f"  Blue {s}-clique: {result['has_blue_clique']}")
    print(f"  Valid coloring: {result['is_valid']}")
    
    # Generate CNF (small example)
    print(f"\nGenerating CNF for R(3,3) with n=5 (example)...")
    clauses, num_vars = generate_cnf_formula(5, 3, 3)
    print(f"  Variables: {num_vars}")
    print(f"  Clauses: {len(clauses)}")
    
    print("\n✓ Graph generation complete")


if __name__ == "__main__":
    main()
