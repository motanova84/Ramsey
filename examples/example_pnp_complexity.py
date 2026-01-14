#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: P-NP Complexity Analysis via Treewidth and κ_Π

This example demonstrates:
1. Treewidth calculation for different graph structures
2. Complexity classification using κ_Π threshold
3. Connection to Ramsey number problems
4. Spectral curvature analysis

Author: QCAL ∞³ Framework
Date: 2026-01-14
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pnp_complexity import (
    CalabiYauManifold,
    TreewidthAnalyzer,
    ComplexityMetrics,
    analyze_ramsey_complexity,
    is_problem_tractable,
    KAPPA_PI_QUANTUM,
    RESONANCE_CY
)


def example_1_basic_treewidth():
    """Example 1: Basic treewidth calculation"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Treewidth Calculation")
    print("=" * 80)
    print()
    
    # Create a simple path graph: 0-1-2-3
    # Path graphs have treewidth = 1
    print("Graph 1: Path graph (0-1-2-3)")
    path_graph = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ])
    
    analyzer = TreewidthAnalyzer(path_graph)
    tw = analyzer.estimate_treewidth_greedy()
    complexity = analyzer.complexity_class()
    curvature = analyzer.spectral_curvature()
    
    print(f"  Treewidth: {tw}")
    print(f"  Complexity class: {complexity}")
    print(f"  Spectral curvature: {curvature:.4f}")
    print(f"  κ_Π threshold: {KAPPA_PI_QUANTUM:.4f}")
    print(f"  Tractable: {tw <= KAPPA_PI_QUANTUM}")
    print()
    
    # Create a complete graph K4
    # Complete graphs have treewidth = n-1
    print("Graph 2: Complete graph K4")
    complete_graph = np.array([
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0]
    ])
    
    analyzer2 = TreewidthAnalyzer(complete_graph)
    tw2 = analyzer2.estimate_treewidth_greedy()
    complexity2 = analyzer2.complexity_class()
    curvature2 = analyzer2.spectral_curvature()
    
    print(f"  Treewidth: {tw2}")
    print(f"  Complexity class: {complexity2}")
    print(f"  Spectral curvature: {curvature2:.4f}")
    print(f"  κ_Π threshold: {KAPPA_PI_QUANTUM:.4f}")
    print(f"  Tractable: {tw2 <= KAPPA_PI_QUANTUM}")
    print()


def example_2_calabi_yau_manifolds():
    """Example 2: Calabi-Yau manifold properties"""
    print("=" * 80)
    print("EXAMPLE 2: Calabi-Yau Manifolds and κ_Π")
    print("=" * 80)
    print()
    
    print("Resonance Manifold (N=13):")
    print(f"  {RESONANCE_CY}")
    print(f"  h^{{1,1}} = {RESONANCE_CY.h11}")
    print(f"  h^{{2,1}} = {RESONANCE_CY.h21}")
    print(f"  Total moduli: {RESONANCE_CY.total_moduli}")
    print(f"  Euler characteristic: {RESONANCE_CY.euler_characteristic}")
    print(f"  κ_Π = ln({RESONANCE_CY.total_moduli}) = {RESONANCE_CY.kappa_pi:.6f}")
    print()
    
    # Create other example manifolds
    print("Other Example Manifolds:")
    manifolds = [
        CalabiYauManifold(h11=1, h21=101),  # Quintic threefold
        CalabiYauManifold(h11=19, h21=19),  # Self-mirror
        CalabiYauManifold(h11=11, h21=11),  # Self-mirror
    ]
    
    for i, cy in enumerate(manifolds, 1):
        print(f"  Manifold {i}: {cy}")
    print()


def example_3_ramsey_complexity():
    """Example 3: Ramsey number complexity analysis"""
    print("=" * 80)
    print("EXAMPLE 3: Ramsey Number Complexity Analysis")
    print("=" * 80)
    print()
    
    ramsey_pairs = [
        (3, 3, "Classical: 6"),
        (4, 4, "Classical: 18"),
        (5, 5, "Proven: 43"),
        (6, 6, "Proven: 108"),
        (3, 4, "Classical: 9"),
    ]
    
    for r, s, note in ramsey_pairs:
        print(f"R({r},{s}) - {note}")
        print("-" * 80)
        
        result = analyze_ramsey_complexity(r, s)
        
        print(f"  Classical bound: {result['classical_bound']}")
        print(f"  Vibrational bound: {result['vibrational_bound']}")
        print(f"  Estimated treewidth: {result['treewidth']}")
        print(f"  Spectral curvature: {result['spectral_curvature']:.4f}")
        print(f"  Complexity class: {result['complexity_class']}")
        print(f"  Tractable within κ_Π: {result['tractable']}")
        
        if result['reduction_factor'] > 1:
            print(f"  Reduction factor: {result['reduction_factor']:.2f}x improvement")
        
        print()


def example_4_complexity_metrics():
    """Example 4: Advanced complexity metrics"""
    print("=" * 80)
    print("EXAMPLE 4: Noetic Curvature and Information Resistance")
    print("=" * 80)
    print()
    
    # Create a test graph
    test_graph = np.array([
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0]
    ])
    
    print("Test Graph (5 vertices):")
    print(test_graph)
    print()
    
    # Calculate noetic curvature
    noetic_curv = ComplexityMetrics.noetic_curvature(test_graph)
    print(f"Noetic Curvature: {noetic_curv:.6f}")
    print()
    
    # Information resistance between frequencies
    print("Information Resistance Examples:")
    print("-" * 80)
    
    f0 = 141.7001
    freq_pairs = [
        (0.0 * f0, 0.618 * f0, "Reference -> Golden ratio"),
        (0.25 * f0, 0.5 * f0, "Quadrature -> Opposition"),
        (0.618 * f0, 0.382 * f0, "Golden ratio -> Conjugate"),
    ]
    
    for f1, f2, description in freq_pairs:
        resistance = ComplexityMetrics.information_resistance(f1, f2, f0)
        print(f"  {description}")
        print(f"    Frequencies: {f1:.2f} Hz, {f2:.2f} Hz")
        print(f"    Resistance: {resistance:.6f}")
        print()
    
    # Effective growth rate
    print("Effective Growth Rates:")
    print("-" * 80)
    for n in [10, 50, 100, 500]:
        rate = ComplexityMetrics.effective_growth_rate(n)
        print(f"  n={n:3d}: N_eff = {rate:.4f}")
    print()


def example_5_problem_classification():
    """Example 5: Automatic problem classification"""
    print("=" * 80)
    print("EXAMPLE 5: Automatic Problem Classification")
    print("=" * 80)
    print()
    
    problems = [
        ("Small cycle", np.array([
            [0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0]
        ])),
        ("Dense graph", np.random.randint(0, 2, (10, 10))),
        ("Sparse graph", np.eye(8, k=1) + np.eye(8, k=-1)),
    ]
    
    # Symmetrize random graphs
    problems[1] = (problems[1][0], 
                   (problems[1][1] + problems[1][1].T) // 2)
    np.fill_diagonal(problems[1][1], 0)
    
    for name, graph in problems:
        print(f"Problem: {name}")
        print("-" * 80)
        
        tractable = is_problem_tractable(graph)
        analyzer = TreewidthAnalyzer(graph)
        tw = analyzer.estimate_treewidth_greedy()
        complexity = analyzer.complexity_class()
        
        print(f"  Size: {len(graph)} vertices")
        print(f"  Edges: {np.sum(graph) // 2}")
        print(f"  Treewidth: {tw}")
        print(f"  Complexity: {complexity}")
        print(f"  Tractable: {'✓ Yes' if tractable else '✗ No'}")
        print()


def main():
    """Run all examples"""
    print()
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "P-NP COMPLEXITY EXAMPLES" + " " * 34 + "█")
    print("█" + " " * 15 + "Calabi-Yau Geometry & Treewidth" + " " * 32 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print()
    print(f"Framework: QCAL ∞³")
    print(f"κ_Π = {KAPPA_PI_QUANTUM:.6f}")
    print(f"f₀ = 141.7001 Hz")
    print()
    
    examples = [
        example_1_basic_treewidth,
        example_2_calabi_yau_manifolds,
        example_3_ramsey_complexity,
        example_4_complexity_metrics,
        example_5_problem_classification,
    ]
    
    for i, example_func in enumerate(examples, 1):
        example_func()
        if i < len(examples):
            print()
    
    print("=" * 80)
    print(" " * 25 + "ALL EXAMPLES COMPLETED")
    print(" " * 20 + "Framework Status: ✅ OPERATIONAL")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
