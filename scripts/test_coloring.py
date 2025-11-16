#!/usr/bin/env python3
"""
Test Vibrational Coloring

This script tests vibrational colorings to verify they satisfy
the required properties (no monochromatic cliques).

Usage:
    python test_coloring.py --n=15 --r=5 --s=5
"""

import sys
import os
import argparse
from pathlib import Path
from itertools import combinations

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from ramsey_vibracional import (
        resonancia_detectada,
        generar_coloracion_vibracional,
        encontrar_clique_maximo
    )
except ImportError:
    print("Warning: ramsey_vibracional module not found. Using dummy functions.")
    def resonancia_detectada(f1, f2, eps=0.001, f0=141.7001):
        return abs(f1 - f2) < eps
    def generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001):
        n = len(frecuencias)
        grafo = {}
        for i in range(n):
            for j in range(i+1, n):
                es_rojo = resonancia_detectada(frecuencias[i], frecuencias[j], eps, f0)
                grafo[(i, j)] = 'rojo' if es_rojo else 'azul'
        return grafo
    def encontrar_clique_maximo(grafo, color):
        return set()


def has_monochromatic_clique(coloring, n, k, color):
    """
    Check if there exists a monochromatic clique of size k.
    
    Args:
        coloring: Edge coloring dictionary
        n: Number of vertices
        k: Clique size to check
        color: Color to check ('rojo' or 'azul')
        
    Returns:
        tuple: (has_clique, clique_vertices) or (False, None)
    """
    for subset in combinations(range(n), k):
        is_clique = True
        for i in range(len(subset)):
            for j in range(i+1, len(subset)):
                edge = (subset[i], subset[j])
                if edge not in coloring or coloring[edge] != color:
                    is_clique = False
                    break
            if not is_clique:
                break
        
        if is_clique:
            return True, subset
    
    return False, None


def test_coloring(n, r, s, epsilon=0.05, f0=141.7001):
    """
    Test a vibrational coloring for R_ψ(r,s).
    
    Args:
        n: Number of vertices
        r: Red clique size to avoid
        s: Blue clique size to avoid
        epsilon: Resonance threshold
        f0: Base frequency
        
    Returns:
        dict: Test results
    """
    # Generate frequency assignment
    frequencies = [f0 * i / 128 for i in range(n)]
    
    # Generate coloring
    coloring = generar_coloracion_vibracional(frequencies, eps=epsilon, f0=f0)
    
    # Check for red K_r
    has_red_kr, red_clique = has_monochromatic_clique(coloring, n, r, 'rojo')
    
    # Check for blue K_s
    has_blue_ks, blue_clique = has_monochromatic_clique(coloring, n, s, 'azul')
    
    results = {
        "n": n,
        "r": r,
        "s": s,
        "epsilon": epsilon,
        "f0": f0,
        "has_red_clique": has_red_kr,
        "red_clique": red_clique if has_red_kr else None,
        "has_blue_clique": has_blue_ks,
        "blue_clique": blue_clique if has_blue_ks else None,
        "is_valid": not (has_red_kr or has_blue_ks),
        "num_edges": len(coloring),
        "num_red_edges": sum(1 for c in coloring.values() if c == 'rojo'),
        "num_blue_edges": sum(1 for c in coloring.values() if c == 'azul')
    }
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Test vibrational colorings'
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
    
    args = parser.parse_args()
    
    print(f"Testing vibrational coloring...")
    print(f"Parameters: n={args.n}, r={args.r}, s={args.s}, ε={args.epsilon}")
    print()
    
    results = test_coloring(args.n, args.r, args.s, args.epsilon, args.f0)
    
    print(f"Results:")
    print(f"  Total edges: {results['num_edges']}")
    print(f"  Red edges: {results['num_red_edges']}")
    print(f"  Blue edges: {results['num_blue_edges']}")
    print(f"  Has red K_{args.r}: {results['has_red_clique']}")
    if results['has_red_clique']:
        print(f"    Found at: {results['red_clique']}")
    print(f"  Has blue K_{args.s}: {results['has_blue_clique']}")
    if results['has_blue_clique']:
        print(f"    Found at: {results['blue_clique']}")
    print()
    print(f"Valid coloring (no monochromatic cliques): {results['is_valid']}")
    
    return 0 if results['is_valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
