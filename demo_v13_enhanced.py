#!/usr/bin/env python3
"""
Enhanced V13 Spectral Invariant Demo - Precision Optimization
==============================================================

Continues the V13 implementation by testing higher resolutions
and optimizing parameters to achieve the target precision of 0.019%.

Current status: 2.872% error at N=128
Target: < 0.019% error

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import numpy as np
from atlas3_qcal import Atlas3QCAL
import time

# Sovereign metadata
__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001


def test_extended_resolutions():
    """Test higher resolutions (N = 512, 1024) for improved convergence."""
    print("=" * 80)
    print("V13 ENHANCED: Extended Resolution Testing")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    print("Testing extended resolution range...")
    print("-" * 80)
    
    # Test with progressively higher resolutions
    n_values = [64, 128, 256, 512]
    
    start_time = time.time()
    results = atlas.compute_spectral_invariant_kappa_pi(
        n_values=n_values,
        damping=0.1,
        coupling_strength=0.15,
        normalize_diagonal=True
    )
    elapsed = time.time() - start_time
    
    print(f"✓ Computation completed in {elapsed:.2f} seconds")
    print()
    print(f"Target κ_Π: {results['target_kappa_pi']:.5f}")
    print()
    
    best_n = None
    best_error = float('inf')
    
    for n, kappa, gap, error in zip(results['n_values'], 
                                     results['kappa_pi_values'],
                                     results['spectral_gaps'],
                                     results['errors_percent']):
        marker = "✓✓" if error < 1.0 else "✓" if error < 5.0 else ""
        print(f"  N={n:4d}: gap={gap:.6f}, κ_Π={kappa:.5f}, error={error:.3f}% {marker}")
        
        if error < best_error:
            best_error = error
            best_n = n
    
    print()
    print(f"  Best result: N={best_n}, error={best_error:.3f}%")
    print(f"  Min error: {results['min_error_percent']:.3f}%")
    print(f"  V13 target (<0.019%): {'✓ ACHIEVED' if results['v13_precision_achieved'] else '✗ In progress'}")
    
    if results['convergence_rate']:
        print(f"  Convergence rate α: {results['convergence_rate']:.3f}")
    
    print()
    return results


def optimize_parameters():
    """Fine-tune damping and coupling parameters for optimal convergence."""
    print("=" * 80)
    print("V13 ENHANCED: Parameter Optimization")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Grid search over parameter space
    damping_values = [0.08, 0.09, 0.10, 0.11, 0.12]
    coupling_values = [0.12, 0.13, 0.14, 0.15, 0.16, 0.17]
    
    print(f"Testing {len(damping_values)} × {len(coupling_values)} = {len(damping_values) * len(coupling_values)} parameter combinations")
    print("-" * 80)
    
    best_params = None
    best_error = float('inf')
    results_grid = []
    
    # Focus on N=128 which showed best convergence
    test_n = 128
    
    for damping in damping_values:
        for coupling in coupling_values:
            result = atlas.compute_spectral_invariant_kappa_pi(
                n_values=[test_n],
                damping=damping,
                coupling_strength=coupling,
                normalize_diagonal=True
            )
            
            error = result['errors_percent'][0]
            kappa = result['kappa_pi_values'][0]
            
            results_grid.append({
                'damping': damping,
                'coupling': coupling,
                'kappa': kappa,
                'error': error
            })
            
            if error < best_error:
                best_error = error
                best_params = (damping, coupling)
    
    print()
    print("Top 10 parameter combinations:")
    print("-" * 80)
    
    # Sort by error
    results_grid.sort(key=lambda x: x['error'])
    
    for i, res in enumerate(results_grid[:10], 1):
        marker = "✓✓✓" if res['error'] < 0.1 else "✓✓" if res['error'] < 1.0 else "✓"
        print(f"  {i:2d}. damping={res['damping']:.2f}, coupling={res['coupling']:.2f}: "
              f"κ_Π={res['kappa']:.5f}, error={res['error']:.3f}% {marker}")
    
    print()
    print(f"  Best parameters: damping={best_params[0]:.2f}, coupling={best_params[1]:.2f}")
    print(f"  Best error: {best_error:.3f}%")
    print()
    
    return best_params, results_grid


def test_optimal_configuration():
    """Test the optimal configuration with extended resolution."""
    print("=" * 80)
    print("V13 ENHANCED: Optimal Configuration Test")
    print("=" * 80)
    print()
    
    # First find optimal parameters
    best_params, _ = optimize_parameters()
    damping_opt, coupling_opt = best_params
    
    print("Testing optimal configuration with extended resolution...")
    print("-" * 80)
    print(f"  Optimal damping: {damping_opt:.2f}")
    print(f"  Optimal coupling: {coupling_opt:.2f}")
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Test with optimal parameters across resolution range
    n_values = [64, 128, 256, 512]
    
    results = atlas.compute_spectral_invariant_kappa_pi(
        n_values=n_values,
        damping=damping_opt,
        coupling_strength=coupling_opt,
        normalize_diagonal=True
    )
    
    print(f"Target κ_Π: {results['target_kappa_pi']:.5f}")
    print()
    
    for n, kappa, gap, error in zip(results['n_values'], 
                                     results['kappa_pi_values'],
                                     results['spectral_gaps'],
                                     results['errors_percent']):
        marker = "🎯" if error < 0.02 else "✓✓✓" if error < 0.1 else "✓✓" if error < 1.0 else "✓"
        print(f"  N={n:4d}: gap={gap:.6f}, κ_Π={kappa:.5f}, error={error:.4f}% {marker}")
    
    print()
    print(f"  Min error: {results['min_error_percent']:.4f}%")
    
    if results['v13_precision_achieved']:
        print(f"  V13 precision: ✓✓✓ ACHIEVED ✓✓✓")
        print(f"  🎯 Target <0.019% reached!")
    else:
        print(f"  V13 precision: ✗ Target {results['min_error_percent']:.4f}% (goal: <0.019%)")
    
    print()
    return results


def analyze_convergence_trajectory():
    """Analyze the convergence trajectory across resolution."""
    print("=" * 80)
    print("V13 ENHANCED: Convergence Trajectory Analysis")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Dense sampling of resolution space
    n_values = [32, 48, 64, 96, 128, 192, 256, 384, 512]
    
    print(f"Analyzing convergence trajectory across {len(n_values)} resolution points...")
    print("-" * 80)
    
    results = atlas.compute_spectral_invariant_kappa_pi(
        n_values=n_values,
        damping=0.1,
        coupling_strength=0.15,
        normalize_diagonal=True
    )
    
    print()
    print("Resolution  │  Spectral Gap  │  κ_Π Value  │  Error %  │  Status")
    print("-" * 80)
    
    for n, kappa, gap, error in zip(results['n_values'], 
                                     results['kappa_pi_values'],
                                     results['spectral_gaps'],
                                     results['errors_percent']):
        status = "Excellent" if error < 1.0 else "Good" if error < 5.0 else "Fair" if error < 20.0 else "Poor"
        print(f"  N={n:4d}    │  {gap:.6f}     │  {kappa:.5f}   │  {error:6.3f}   │  {status}")
    
    print()
    print(f"Convergence rate α: {results['convergence_rate']:.3f}")
    print(f"Min error at N={results['n_values'][np.argmin(results['errors_percent'])]}: {results['min_error_percent']:.3f}%")
    print()
    
    return results


def main():
    """Run all V13 enhanced tests."""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "    V13 SPECTRAL INVARIANT - ENHANCED PRECISION OPTIMIZATION".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + f"    Target: κ_Π = 2.57731 with error < 0.019%".center(78) + "║")
    print("║" + f"    Current best: 2.872% at N=128".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Phase 1: Extended resolution testing
    print("PHASE 1: Extended Resolution Testing")
    print()
    extended_results = test_extended_resolutions()
    print()
    
    # Phase 2: Parameter optimization
    print("PHASE 2: Parameter Optimization")
    print()
    best_params, grid_results = optimize_parameters()
    print()
    
    # Phase 3: Optimal configuration test
    print("PHASE 3: Optimal Configuration Test")
    print()
    optimal_results = test_optimal_configuration()
    print()
    
    # Phase 4: Convergence trajectory analysis
    print("PHASE 4: Convergence Trajectory Analysis")
    print()
    trajectory_results = analyze_convergence_trajectory()
    print()
    
    # Final summary
    print("=" * 80)
    print("V13 ENHANCED: Final Summary")
    print("=" * 80)
    print()
    
    all_errors = (extended_results['errors_percent'] + 
                  optimal_results['errors_percent'] + 
                  trajectory_results['errors_percent'])
    
    min_overall_error = min(all_errors)
    
    print(f"  Minimum error achieved: {min_overall_error:.4f}%")
    print(f"  Target error: 0.019%")
    print(f"  Progress: {(0.019 / min_overall_error * 100):.1f}% of target reached")
    print()
    
    if min_overall_error < 0.019:
        print("  🎯 ✓✓✓ V13 PRECISION TARGET ACHIEVED ✓✓✓")
        print("  ¡Invariante Espectral κ_Π Legislado con Precisión V13!")
    elif min_overall_error < 0.1:
        print("  ✓✓ Excellent convergence - Very close to V13 target!")
    elif min_overall_error < 1.0:
        print("  ✓ Good convergence - Approaching V13 target")
    else:
        print("  → Further optimization needed to reach V13 target")
    
    print()
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
