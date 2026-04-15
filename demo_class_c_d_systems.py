#!/usr/bin/env python3
"""
Demo: Class C and Class D Systems
==================================

Demonstrates the newly implemented Class C (k-ary colorings) and 
Class D (dynamic/adaptive) systems in the QCAL ∞³ Phase 3 framework.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
Date: March 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from core.math.class_b_systems import create_system, SystemClass

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_subheader(title):
    """Print formatted subsection header"""
    print(f"\n--- {title} ---")

def demo_class_c_system():
    """Demonstrate Class C k-ary system"""
    print_header("CLASS C SYSTEM: k-ary Colorings (k ≥ 4)")
    
    # Create Class C system with 5 colors
    k = 5
    system = create_system(SystemClass.C, k=k)
    
    print(f"System Class: {system.get_system_class()}")
    print(f"Number of Colors: {system.get_color_count()}")
    print(f"Color Palette: {system.color_names[:k]}")
    print(f"Universal Frequency: f₀ = {system.f0} Hz")
    print(f"Coupling Constant: κ_Π = {system.kappa_pi}")
    
    # Generate test frequencies
    print_subheader("Generating Vibrational Coloring")
    np.random.seed(42)
    n_vertices = 15
    frequencies = np.random.uniform(0, system.f0, n_vertices)
    
    print(f"Vertices: {n_vertices}")
    print(f"Frequency range: [0, {system.f0:.4f}] Hz")
    
    # Generate coloring
    coloring = system.generate_coloring(frequencies)
    print(f"Edges colored: {len(coloring)}")
    
    # Count color distribution
    color_counts = {}
    for color in coloring.values():
        color_counts[color] = color_counts.get(color, 0) + 1
    
    print("\nColor Distribution:")
    for color, count in sorted(color_counts.items()):
        percentage = (count / len(coloring)) * 100
        print(f"  {color.capitalize():12s}: {count:3d} edges ({percentage:5.1f}%)")
    
    # Find cliques
    print_subheader("Monochromatic Clique Detection")
    for color in system.color_names[:k]:
        clique = system.find_monochromatic_clique(coloring, color, min_size=3)
        if clique:
            print(f"  ✓ Found {color} K_{len(clique)}: {sorted(list(clique))}")
    
    # Estimate Ramsey numbers
    print_subheader("Ramsey Number Estimates")
    params = [3] * k
    bound = system.estimate_ramsey_number(*params)
    print(f"  R({','.join(map(str, params))}) ≤ {bound:.2f}")
    
    params = [4] * k
    bound = system.estimate_ramsey_number(*params)
    print(f"  R({','.join(map(str, params))}) ≤ {bound:.2f}")

def demo_class_d_system():
    """Demonstrate Class D dynamic/adaptive system"""
    print_header("CLASS D SYSTEM: Dynamic/Adaptive Coloring")
    
    # Create Class D system
    max_colors = 8
    system = create_system(SystemClass.D, max_colors=max_colors)
    
    print(f"System Class: {system.get_system_class()}")
    print(f"Maximum Colors: {system.max_colors}")
    print(f"Universal Frequency: f₀ = {system.f0} Hz")
    print(f"Coupling Constant: κ_Π = {system.kappa_pi}")
    
    # Test 1: Uniform distribution
    print_subheader("Test 1: Uniform Frequency Distribution")
    np.random.seed(17)
    frequencies_uniform = np.random.uniform(0, system.f0, 20)
    
    coloring_uniform = system.generate_coloring(frequencies_uniform)
    print(f"Vertices: {len(frequencies_uniform)}")
    print(f"Adaptive k determined: {system.adaptive_k} colors")
    print(f"Edges colored: {len(coloring_uniform)}")
    
    colors_used = set(coloring_uniform.values())
    print(f"Colors actually used: {len(colors_used)}")
    
    # Test 2: Clustered distribution
    print_subheader("Test 2: Clustered Frequency Distribution")
    cluster1 = np.random.uniform(0, 20, 8)
    cluster2 = np.random.uniform(50, 70, 8)
    cluster3 = np.random.uniform(110, 130, 8)
    frequencies_clustered = np.concatenate([cluster1, cluster2, cluster3])
    
    coloring_clustered = system.generate_coloring(frequencies_clustered)
    print(f"Vertices: {len(frequencies_clustered)} (3 clusters)")
    print(f"Adaptive k determined: {system.adaptive_k} colors")
    print(f"Edges colored: {len(coloring_clustered)}")
    
    colors_used = set(coloring_clustered.values())
    print(f"Colors actually used: {len(colors_used)}")
    
    # Color distribution
    color_counts = {}
    for color in coloring_clustered.values():
        color_counts[color] = color_counts.get(color, 0) + 1
    
    print("\nColor Distribution:")
    for color, count in sorted(color_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(coloring_clustered)) * 100
        print(f"  {color.capitalize():12s}: {count:3d} edges ({percentage:5.1f}%)")
    
    # Spectral gap analysis
    print_subheader("Spectral Gap Analysis")
    sorted_freqs = np.sort(frequencies_clustered)
    gaps = np.diff(sorted_freqs)
    threshold = system.kappa_pi * system.epsilon
    significant_gaps = np.where(gaps / system.f0 > threshold)[0]
    
    print(f"Total frequency gaps: {len(gaps)}")
    print(f"Significant gaps (> κ_Π·ε): {len(significant_gaps)}")
    print(f"Expected clusters: {len(significant_gaps) + 1}")
    print(f"Determined colors: {system.adaptive_k}")
    
    # Find cliques
    print_subheader("Monochromatic Clique Detection")
    best_clique = None
    best_size = 0
    best_color = None
    
    for color in colors_used:
        clique = system.find_monochromatic_clique(coloring_clustered, color, min_size=2)
        if clique and len(clique) > best_size:
            best_clique = clique
            best_size = len(clique)
            best_color = color
    
    if best_clique:
        print(f"  Largest clique: {best_color} K_{best_size}")
        print(f"  Vertices: {sorted(list(best_clique))}")
    
    # Estimate with correction
    print_subheader("Ramsey Estimates with Spectral Correction")
    params = [4, 4, 4]
    base_bound = system.polynomial_bound(*params)
    corrected_estimate = system.estimate_ramsey_number(*params)
    correction_factor = corrected_estimate / base_bound
    
    print(f"  Base polynomial bound: {base_bound:.2f}")
    print(f"  Spectral correction: {correction_factor:.4f}")
    print(f"  Corrected estimate: {corrected_estimate:.2f}")

def demo_comparison():
    """Compare all system classes"""
    print_header("SYSTEM COMPARISON: A, B, C, D")
    
    # Create all systems
    system_a = create_system(SystemClass.A)
    system_b = create_system(SystemClass.B)
    system_c = create_system(SystemClass.C, k=4)
    system_d = create_system(SystemClass.D, max_colors=6)
    
    print("\nSystem Properties:")
    print(f"  Class A: {system_a.get_color_count()} colors (Binary)")
    print(f"  Class B: {system_b.get_color_count()} colors (Ternary)")
    print(f"  Class C: {system_c.get_color_count()} colors (k-ary, k=4)")
    print(f"  Class D: {system_d.max_colors} colors max (Adaptive)")
    
    # Test with same frequencies
    print_subheader("Coloring the Same Graph")
    np.random.seed(123)
    test_frequencies = np.random.uniform(0, 141.7001, 12)
    
    coloring_a = system_a.generate_coloring(test_frequencies)
    coloring_b = system_b.generate_coloring(test_frequencies)
    coloring_c = system_c.generate_coloring(test_frequencies)
    coloring_d = system_d.generate_coloring(test_frequencies)
    
    n = len(test_frequencies)
    expected_edges = n * (n - 1) // 2
    
    print(f"Vertices: {n}, Expected edges: {expected_edges}")
    print(f"  Class A edges: {len(coloring_a)}")
    print(f"  Class B edges: {len(coloring_b)}")
    print(f"  Class C edges: {len(coloring_c)}")
    print(f"  Class D edges: {len(coloring_d)} (adaptive k={system_d.adaptive_k})")
    
    # Compare bounds for R(3,3,...,3)
    print_subheader("Polynomial Bounds for R(3,3,...)")
    print(f"  R(3,3)       [A]: {system_a.polynomial_bound(3, 3):.2f}")
    print(f"  R(3,3,3)     [B]: {system_b.polynomial_bound(3, 3, 3):.2f}")
    print(f"  R(3,3,3,3)   [C]: {system_c.polynomial_bound(3, 3, 3, 3):.2f}")
    print(f"  R(3,3,3)     [D]: {system_d.estimate_ramsey_number(3, 3, 3):.2f} (corrected)")

def main():
    """Main demonstration"""
    print("=" * 80)
    print("  QCAL ∞³ Phase 3: Class C and Class D Systems Demo")
    print("  Universal Frequency: f₀ = 141.7001 Hz")
    print("  Coupling Constant: κ_Π = 2.5773")
    print("=" * 80)
    
    # Run demonstrations
    demo_class_c_system()
    demo_class_d_system()
    demo_comparison()
    
    print_header("DEMONSTRATION COMPLETE")
    print("✓ Class C (k-ary colorings) demonstrated")
    print("✓ Class D (dynamic/adaptive) demonstrated")
    print("✓ System comparison completed")
    print("\nPhase 3 Class C and D systems are fully operational!")
    print(f"Architecture: QCAL ∞³ | f₀ = 141.7001 Hz | κ_Π = 2.5773")

if __name__ == "__main__":
    main()
