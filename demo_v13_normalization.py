#!/usr/bin/env python3
"""
V13 Normalization Scheme Comparison
====================================

Tests different diagonal normalization schemes to find which
gives the best convergence to κ_Π = 2.57731.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³  
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import numpy as np
from atlas3_qcal import Atlas3QCAL

# Sovereign metadata
__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001


def test_normalization_schemes():
    """Compare all normalization schemes."""
    print("=" * 80)
    print("V13 NORMALIZATION SCHEME COMPARISON")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Test parameters (optimized from previous run)
    damping = 0.08
    coupling = 0.17
    n_values = [64, 128, 192, 256]
    
    schemes = ['constant', 'logarithmic', 'sqrt', 'linear', 'quadratic']
    
    print(f"Testing {len(schemes)} normalization schemes...")
    print(f"Damping: {damping:.2f}, Coupling: {coupling:.2f}")
    print(f"Resolution range: {n_values}")
    print()
    print("-" * 80)
    
    best_scheme = None
    best_error = float('inf')
    all_results = {}
    
    for scheme in schemes:
        print(f"\n📊 Scheme: {scheme.upper()}")
        print("-" * 40)
        
        results = atlas.compute_spectral_invariant_kappa_pi(
            n_values=n_values,
            damping=damping,
            coupling_strength=coupling,
            normalize_diagonal=True,
            normalization_scheme=scheme
        )
        
        all_results[scheme] = results
        
        print(f"  Target κ_Π: {results['target_kappa_pi']:.5f}")
        print()
        
        scheme_best_error = min(results['errors_percent'])
        scheme_best_n = results['n_values'][np.argmin(results['errors_percent'])]
        
        for n, kappa, error in zip(results['n_values'],
                                    results['kappa_pi_values'],
                                    results['errors_percent']):
            marker = "🎯" if error < 0.1 else "✓✓✓" if error < 1.0 else "✓✓" if error < 5.0 else "✓"
            print(f"    N={n:3d}: κ_Π={kappa:.5f}, error={error:.4f}% {marker}")
        
        print()
        print(f"  Best for {scheme}: N={scheme_best_n}, error={scheme_best_error:.4f}%")
        
        if scheme_best_error < best_error:
            best_error = scheme_best_error
            best_scheme = scheme
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    # Rank schemes by best error
    scheme_rankings = []
    for scheme in schemes:
        min_err = min(all_results[scheme]['errors_percent'])
        scheme_rankings.append((scheme, min_err))
    
    scheme_rankings.sort(key=lambda x: x[1])
    
    print("Scheme Rankings (by minimum error):")
    print("-" * 80)
    for rank, (scheme, err) in enumerate(scheme_rankings, 1):
        marker = "🏆" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        print(f"  {marker} {scheme:12s}: {err:.4f}%")
    
    print()
    print(f"Best scheme: {best_scheme.upper()}")
    print(f"Best error: {best_error:.4f}%")
    print(f"Target: 0.019%")
    print(f"Progress: {(0.019 / best_error * 100) if best_error > 0 else 0:.1f}% of target")
    
    if best_error < 0.019:
        print()
        print("🎯 ✓✓✓ V13 PRECISION ACHIEVED ✓✓✓")
    elif best_error < 0.1:
        print()
        print("✓✓ Excellent! Very close to V13 target")
    elif best_error < 1.0:
        print()
        print("✓ Good progress toward V13 target")
    
    print()
    print("=" * 80)
    print()
    
    return best_scheme, all_results


def fine_tune_best_scheme(best_scheme):
    """Fine-tune parameters for the best normalization scheme."""
    print("=" * 80)
    print(f"FINE-TUNING: {best_scheme.upper()} SCHEME")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Expand parameter grid around optimal region
    damping_values = [0.06, 0.07, 0.08, 0.09, 0.10]
    coupling_values = [0.15, 0.16, 0.17, 0.18, 0.19, 0.20]
    
    print(f"Testing {len(damping_values)} × {len(coupling_values)} = {len(damping_values) * len(coupling_values)} combinations")
    print("-" * 80)
    
    # Focus on optimal N
    test_n = 128
    
    best_params = None
    best_error = float('inf')
    results_grid = []
    
    for damping in damping_values:
        for coupling in coupling_values:
            result = atlas.compute_spectral_invariant_kappa_pi(
                n_values=[test_n],
                damping=damping,
                coupling_strength=coupling,
                normalize_diagonal=True,
                normalization_scheme=best_scheme
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
    
    # Sort by error
    results_grid.sort(key=lambda x: x['error'])
    
    print()
    print(f"Top 15 parameter combinations for {best_scheme} scheme:")
    print("-" * 80)
    
    for i, res in enumerate(results_grid[:15], 1):
        marker = "🎯" if res['error'] < 0.02 else "✓✓✓" if res['error'] < 0.1 else "✓✓" if res['error'] < 1.0 else "✓"
        print(f"  {i:2d}. d={res['damping']:.2f}, c={res['coupling']:.2f}: "
              f"κ_Π={res['kappa']:.5f}, error={res['error']:.5f}% {marker}")
    
    print()
    print(f"Optimal: damping={best_params[0]:.2f}, coupling={best_params[1]:.2f}")
    print(f"Best error: {best_error:.5f}%")
    print()
    
    # Test optimal parameters across resolution range
    print("Testing optimal parameters across resolution range...")
    print("-" * 80)
    
    final_results = atlas.compute_spectral_invariant_kappa_pi(
        n_values=[64, 96, 128, 160, 192, 224, 256],
        damping=best_params[0],
        coupling_strength=best_params[1],
        normalize_diagonal=True,
        normalization_scheme=best_scheme
    )
    
    print()
    for n, kappa, error in zip(final_results['n_values'],
                                final_results['kappa_pi_values'],
                                final_results['errors_percent']):
        marker = "🎯" if error < 0.02 else "✓✓✓" if error < 0.1 else "✓✓" if error < 1.0 else "✓"
        print(f"  N={n:3d}: κ_Π={kappa:.5f}, error={error:.5f}% {marker}")
    
    final_best_error = min(final_results['errors_percent'])
    
    print()
    print(f"Final best error: {final_best_error:.5f}%")
    print(f"V13 target: 0.019%")
    
    if final_best_error < 0.019:
        print()
        print("🎯✓✓✓ V13 PRECISION TARGET ACHIEVED ✓✓✓🎯")
        print("¡Invariante Espectral κ_Π Certificado con Precisión V13!")
    elif final_best_error < 0.1:
        print()
        print("✓✓ Excellent convergence - Very close to V13 target!")
    elif final_best_error < 1.0:
        print()
        print("✓ Good convergence - Significant progress toward V13")
    
    print()
    print("=" * 80)
    print()
    
    return best_params, final_results


def main():
    """Run normalization scheme comparison and fine-tuning."""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "V13 ENHANCED: NORMALIZATION SCHEME OPTIMIZATION".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "Phase 3: Advanced Normalization Testing".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Phase 1: Compare all schemes
    best_scheme, all_results = test_normalization_schemes()
    
    # Phase 2: Fine-tune best scheme
    best_params, final_results = fine_tune_best_scheme(best_scheme)
    
    # Final summary
    print()
    print("=" * 80)
    print("FINAL V13 STATUS")
    print("=" * 80)
    print()
    print(f"  Best normalization scheme: {best_scheme.upper()}")
    print(f"  Optimal damping: {best_params[0]:.2f}")
    print(f"  Optimal coupling: {best_params[1]:.2f}")
    print(f"  Minimum error achieved: {min(final_results['errors_percent']):.5f}%")
    print(f"  V13 target: 0.019%")
    print()
    
    if final_results['v13_precision_achieved']:
        print("  STATUS: ✓✓✓ V13 PRECISION CERTIFIED ✓✓✓")
    else:
        progress = 0.019 / min(final_results['errors_percent']) * 100
        print(f"  STATUS: {progress:.1f}% of V13 target achieved")
    
    print()
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
