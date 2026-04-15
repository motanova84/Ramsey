#!/usr/bin/env python3
"""
V13 Ultra-Fine Parameter Tuning
================================

Performs ultra-fine parameter optimization around the optimal region
(damping=0.06, coupling=0.20) to push toward the V13 target of 0.019%.

Current best: 0.619% error at N=128

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


def ultra_fine_grid_search():
    """Ultra-fine grid search around optimal parameters."""
    print("=" * 80)
    print("V13 ULTRA-FINE PARAMETER TUNING")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    # Ultra-fine grid around optimal region
    # Center: damping=0.06, coupling=0.20
    damping_values = np.linspace(0.050, 0.070, 21)  # 21 points
    coupling_values = np.linspace(0.190, 0.210, 21)  # 21 points
    
    print(f"Testing {len(damping_values)} × {len(coupling_values)} = {len(damping_values) * len(coupling_values)} combinations")
    print(f"Damping range: [{damping_values[0]:.3f}, {damping_values[-1]:.3f}]")
    print(f"Coupling range: [{coupling_values[0]:.3f}, {coupling_values[-1]:.3f}]")
    print("-" * 80)
    
    # Focus on optimal N
    test_n = 128
    
    best_params = None
    best_error = float('inf')
    results_grid = []
    
    total_combinations = len(damping_values) * len(coupling_values)
    count = 0
    
    for damping in damping_values:
        for coupling in coupling_values:
            count += 1
            if count % 50 == 0:
                print(f"  Progress: {count}/{total_combinations} ({100*count/total_combinations:.1f}%)")
            
            result = atlas.compute_spectral_invariant_kappa_pi(
                n_values=[test_n],
                damping=damping,
                coupling_strength=coupling,
                normalize_diagonal=True,
                normalization_scheme='linear'
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
    
    print(f"  Progress: {total_combinations}/{total_combinations} (100.0%)")
    print()
    
    # Sort by error
    results_grid.sort(key=lambda x: x['error'])
    
    print()
    print("Top 20 parameter combinations:")
    print("-" * 80)
    
    for i, res in enumerate(results_grid[:20], 1):
        marker = "🎯" if res['error'] < 0.02 else "✓✓✓" if res['error'] < 0.1 else "✓✓" if res['error'] < 0.5 else "✓"
        print(f"  {i:2d}. d={res['damping']:.4f}, c={res['coupling']:.4f}: "
              f"κ_Π={res['kappa']:.6f}, error={res['error']:.6f}% {marker}")
    
    print()
    print(f"Optimal: damping={best_params[0]:.4f}, coupling={best_params[1]:.4f}")
    print(f"Best error: {best_error:.6f}%")
    print(f"V13 target: 0.019%")
    
    if best_error < 0.019:
        print()
        print("🎯✓✓✓ V13 PRECISION TARGET ACHIEVED ✓✓✓🎯")
    elif best_error < 0.05:
        print()
        print("✓✓✓ Excellent! Very close to V13 target")
    elif best_error < 0.1:
        print()
        print("✓✓ Great progress! Approaching V13 target")
    
    print()
    print("=" * 80)
    print()
    
    return best_params, results_grid


def test_resolution_sweep(damping, coupling):
    """Test optimal parameters across extended resolution range."""
    print("=" * 80)
    print("RESOLUTION SWEEP WITH OPTIMAL PARAMETERS")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    print(f"Parameters: damping={damping:.4f}, coupling={coupling:.4f}")
    print()
    
    # Dense resolution sampling around optimal
    n_values = [64, 80, 96, 112, 128, 144, 160, 176, 192]
    
    results = atlas.compute_spectral_invariant_kappa_pi(
        n_values=n_values,
        damping=damping,
        coupling_strength=coupling,
        normalize_diagonal=True,
        normalization_scheme='linear'
    )
    
    print("Resolution sweep results:")
    print("-" * 80)
    print()
    
    for n, kappa, gap, error in zip(results['n_values'],
                                     results['kappa_pi_values'],
                                     results['spectral_gaps'],
                                     results['errors_percent']):
        marker = "🎯" if error < 0.02 else "✓✓✓" if error < 0.1 else "✓✓" if error < 0.5 else "✓"
        print(f"  N={n:3d}: gap={gap:.6f}, κ_Π={kappa:.6f}, error={error:.6f}% {marker}")
    
    best_error = min(results['errors_percent'])
    best_n = results['n_values'][np.argmin(results['errors_percent'])]
    
    print()
    print(f"Best resolution: N={best_n}")
    print(f"Best error: {best_error:.6f}%")
    print(f"Convergence rate α: {results['convergence_rate']:.3f}")
    print()
    print("=" * 80)
    print()
    
    return results


def adaptive_refinement(initial_damping, initial_coupling, n_iterations=5):
    """Adaptive parameter refinement using gradient descent."""
    print("=" * 80)
    print("ADAPTIVE PARAMETER REFINEMENT")
    print("=" * 80)
    print()
    
    atlas = Atlas3QCAL(f0=141.7001)
    
    damping = initial_damping
    coupling = initial_coupling
    test_n = 128
    
    print(f"Starting from: d={damping:.4f}, c={coupling:.4f}")
    print(f"Iterations: {n_iterations}")
    print()
    print("-" * 80)
    
    history = []
    
    for iteration in range(n_iterations):
        print(f"\nIteration {iteration + 1}/{n_iterations}:")
        print(f"  Current: d={damping:.4f}, c={coupling:.4f}")
        
        # Evaluate current point
        result = atlas.compute_spectral_invariant_kappa_pi(
            n_values=[test_n],
            damping=damping,
            coupling_strength=coupling,
            normalize_diagonal=True,
            normalization_scheme='linear'
        )
        
        current_error = result['errors_percent'][0]
        current_kappa = result['kappa_pi_values'][0]
        
        print(f"  Error: {current_error:.6f}%")
        print(f"  κ_Π: {current_kappa:.6f}")
        
        history.append({
            'iteration': iteration + 1,
            'damping': damping,
            'coupling': coupling,
            'error': current_error,
            'kappa': current_kappa
        })
        
        # Estimate gradient by finite differences
        delta = 0.001
        
        # Damping gradient
        result_d_plus = atlas.compute_spectral_invariant_kappa_pi(
            n_values=[test_n],
            damping=damping + delta,
            coupling_strength=coupling,
            normalize_diagonal=True,
            normalization_scheme='linear'
        )
        
        grad_damping = (result_d_plus['errors_percent'][0] - current_error) / delta
        
        # Coupling gradient
        result_c_plus = atlas.compute_spectral_invariant_kappa_pi(
            n_values=[test_n],
            damping=damping,
            coupling_strength=coupling + delta,
            normalize_diagonal=True,
            normalization_scheme='linear'
        )
        
        grad_coupling = (result_c_plus['errors_percent'][0] - current_error) / delta
        
        # Adaptive step size
        step_size = 0.002 / (1 + iteration)
        
        # Gradient descent step
        damping_new = damping - step_size * grad_damping
        coupling_new = coupling - step_size * grad_coupling
        
        # Bounds
        damping_new = np.clip(damping_new, 0.01, 0.15)
        coupling_new = np.clip(coupling_new, 0.10, 0.30)
        
        print(f"  Gradient: ∇d={grad_damping:.4f}, ∇c={grad_coupling:.4f}")
        print(f"  Step: Δd={damping_new - damping:.6f}, Δc={coupling_new - coupling:.6f}")
        
        damping = damping_new
        coupling = coupling_new
    
    # Final evaluation
    print()
    print("-" * 80)
    print("Final evaluation:")
    
    final_result = atlas.compute_spectral_invariant_kappa_pi(
        n_values=[test_n],
        damping=damping,
        coupling_strength=coupling,
        normalize_diagonal=True,
        normalization_scheme='linear'
    )
    
    final_error = final_result['errors_percent'][0]
    final_kappa = final_result['kappa_pi_values'][0]
    
    print(f"  Final: d={damping:.4f}, c={coupling:.4f}")
    print(f"  Error: {final_error:.6f}%")
    print(f"  κ_Π: {final_kappa:.6f}")
    
    history.append({
        'iteration': n_iterations + 1,
        'damping': damping,
        'coupling': coupling,
        'error': final_error,
        'kappa': final_kappa
    })
    
    print()
    print("Improvement: {:.6f}% → {:.6f}% ({:.2f}x)".format(
        history[0]['error'],
        final_error,
        history[0]['error'] / final_error if final_error > 0 else float('inf')
    ))
    
    print()
    print("=" * 80)
    print()
    
    return (damping, coupling), history


def main():
    """Run ultra-fine parameter tuning."""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "V13 ULTRA-FINE PARAMETER TUNING".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "Phase 4: Pushing Toward 0.019% Target".center(78) + "║")
    print("║" + "Current: 0.619% → Target: 0.019%".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Phase 1: Ultra-fine grid search
    print("PHASE 1: Ultra-Fine Grid Search")
    print()
    best_params, grid_results = ultra_fine_grid_search()
    print()
    
    # Phase 2: Resolution sweep with optimal parameters
    print("PHASE 2: Resolution Sweep")
    print()
    resolution_results = test_resolution_sweep(best_params[0], best_params[1])
    print()
    
    # Phase 3: Adaptive refinement
    print("PHASE 3: Adaptive Refinement")
    print()
    refined_params, history = adaptive_refinement(best_params[0], best_params[1], n_iterations=5)
    print()
    
    # Final summary
    print()
    print("=" * 80)
    print("FINAL V13 STATUS")
    print("=" * 80)
    print()
    
    best_grid_error = grid_results[0]['error']
    best_resolution_error = min(resolution_results['errors_percent'])
    best_adaptive_error = history[-1]['error']
    
    overall_best_error = min(best_grid_error, best_resolution_error, best_adaptive_error)
    
    print(f"  Best from grid search: {best_grid_error:.6f}%")
    print(f"  Best from resolution sweep: {best_resolution_error:.6f}%")
    print(f"  Best from adaptive refinement: {best_adaptive_error:.6f}%")
    print()
    print(f"  Overall best error: {overall_best_error:.6f}%")
    print(f"  V13 target: 0.019%")
    print(f"  Progress: {(0.019 / overall_best_error * 100):.1f}% of target")
    print()
    
    if overall_best_error < 0.019:
        print("  🎯✓✓✓ V13 PRECISION TARGET ACHIEVED ✓✓✓🎯")
        print("  ¡Invariante Espectral κ_Π Legislado con Precisión V13!")
    elif overall_best_error < 0.05:
        print("  ✓✓✓ Excellent! Very close to V13 target")
    elif overall_best_error < 0.1:
        print("  ✓✓ Great progress! Approaching V13 target")
    elif overall_best_error < 0.5:
        print("  ✓ Good progress toward V13 target")
    
    print()
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()
