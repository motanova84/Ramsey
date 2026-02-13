#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V9 Visualization - Convergence Graphs
======================================

Optional visualization module for V9 convergence analysis.
Generates publication-quality plots of C_est vs N_MODES.

Requires: matplotlib (optional dependency)

Author: QCAL ∞³ Framework
Date: 2026-02-13
"""

import sys
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ matplotlib not available. Install with: pip install matplotlib")

import numpy as np
from symbiotic_coherence_v9 import (
    MultiScaleConvergenceAnalyzer,
    PerturbationConfig,
    KAPPA_PI,
    C_EST_TARGET,
)


def plot_convergence_multiescale(results, filename='v9_convergence.png'):
    """
    Generate convergence plot: C_est vs N_MODES
    
    Args:
        results: List of ConvergenceResult objects
        filename: Output filename
    """
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Cannot generate plot: matplotlib not installed")
        return
    
    # Extract data
    n_modes = [r.n_modes for r in results]
    c_est_values = [r.c_est for r in results]
    errors = [r.relative_error * 100 for r in results]
    densities = [r.density * 100 for r in results]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: C_est vs N_MODES
    ax1.plot(n_modes, c_est_values, 'o-', linewidth=2, markersize=8, 
             label='C_est (empírico)', color='#2E86AB')
    ax1.axhline(y=KAPPA_PI, color='#A23B72', linestyle='--', linewidth=2,
                label=f'κ_Π = {KAPPA_PI} (teórico)')
    ax1.axhline(y=C_EST_TARGET, color='#F18F01', linestyle=':', linewidth=2,
                label=f'C_est objetivo ≈ {C_EST_TARGET}')
    
    # Shaded region for coherence
    ax1.fill_between(n_modes, 
                     KAPPA_PI * (1 - 0.05), 
                     KAPPA_PI * (1 + 0.05),
                     alpha=0.2, color='green', 
                     label='Banda de coherencia (±5%)')
    
    ax1.set_xlabel('N_MODES', fontsize=14, fontweight='bold')
    ax1.set_ylabel('C_est', fontsize=14, fontweight='bold')
    ax1.set_title('Convergencia Multiescala: C_est → κ_Π', 
                  fontsize=16, fontweight='bold')
    ax1.legend(loc='best', fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Plot 2: Relative Error and Density
    ax2_twin = ax2.twinx()
    
    line1 = ax2.plot(n_modes, errors, 's-', linewidth=2, markersize=7,
                     label='Error relativo (%)', color='#C73E1D')
    ax2.axhline(y=5.0, color='red', linestyle='--', linewidth=1.5,
                alpha=0.5, label='Umbral coherencia (5%)')
    
    line2 = ax2_twin.plot(n_modes, densities, '^-', linewidth=2, markersize=7,
                          label='Densidad grafo (%)', color='#6A994E')
    ax2_twin.axhline(y=18.0, color='green', linestyle='--', linewidth=1.5,
                     alpha=0.5, label='Objetivo densidad (18%)')
    
    ax2.set_xlabel('N_MODES', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Error Relativo (%)', fontsize=14, fontweight='bold', color='#C73E1D')
    ax2_twin.set_ylabel('Densidad Grafo (%)', fontsize=14, fontweight='bold', color='#6A994E')
    ax2.set_title('Métricas de Calidad: Error y Densidad',
                  fontsize=16, fontweight='bold')
    
    ax2.tick_params(axis='y', labelcolor='#C73E1D')
    ax2_twin.tick_params(axis='y', labelcolor='#6A994E')
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper left', fontsize=11)
    
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f'✅ Convergence plot saved: {filename}')
    
    return filename


def plot_perturbation_coherence(report, filename='v9_coherence.png'):
    """
    Generate perturbation coherence plot
    
    Args:
        report: Coherence report dictionary
        filename: Output filename
    """
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Cannot generate plot: matplotlib not installed")
        return
    
    results = report['results']
    n = len(results)
    
    # Extract data
    labels = []
    c_est_values = []
    errors = []
    colors = []
    
    for r in results:
        pert = r['perturbation']
        label = f"η={pert.eta:.2f}\nδζ={pert.delta_zeta:.2f}"
        labels.append(label)
        c_est_values.append(r['c_est'])
        errors.append(r['relative_error'] * 100)
        colors.append('green' if r['coherent'] else 'red')
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: C_est values
    x = np.arange(n)
    bars1 = ax1.bar(x, c_est_values, color=colors, alpha=0.7, edgecolor='black')
    ax1.axhline(y=KAPPA_PI, color='blue', linestyle='--', linewidth=2,
                label=f'κ_Π = {KAPPA_PI}')
    ax1.axhline(y=KAPPA_PI * 1.05, color='red', linestyle=':', linewidth=1,
                alpha=0.5)
    ax1.axhline(y=KAPPA_PI * 0.95, color='red', linestyle=':', linewidth=1,
                alpha=0.5, label='Banda coherencia (±5%)')
    
    ax1.set_xlabel('Configuración de Perturbación', fontsize=14, fontweight='bold')
    ax1.set_ylabel('C_est', fontsize=14, fontweight='bold')
    ax1.set_title('Test de Coherencia Simbiótica\nC_est bajo Perturbaciones',
                  fontsize=16, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9, rotation=45, ha='right')
    ax1.legend(loc='best', fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Error percentages
    bars2 = ax2.bar(x, errors, color=colors, alpha=0.7, edgecolor='black')
    ax2.axhline(y=5.0, color='red', linestyle='--', linewidth=2,
                label='Umbral coherencia (5%)')
    
    ax2.set_xlabel('Configuración de Perturbación', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Error Relativo (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Error Relativo bajo Perturbaciones',
                  fontsize=16, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9, rotation=45, ha='right')
    ax2.legend(loc='best', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add status text
    status_text = f"Status: {report['status']}\n"
    status_text += f"Tasa coherencia: {report['coherence_rate']:.1%}\n"
    status_text += f"C_est promedio: {report['avg_c_est']:.6f}"
    
    fig.text(0.5, 0.02, status_text, ha='center', fontsize=12,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f'✅ Coherence plot saved: {filename}')
    
    return filename


def generate_all_plots():
    """Generate all V9 visualization plots"""
    if not MATPLOTLIB_AVAILABLE:
        print("=" * 80)
        print("  MATPLOTLIB NOT AVAILABLE")
        print("=" * 80)
        print()
        print("To generate plots, install matplotlib:")
        print("  pip install matplotlib")
        print()
        return False
    
    print("=" * 80)
    print("  V9 VISUALIZATION - GENERATING PLOTS")
    print("=" * 80)
    print()
    
    # Generate convergence analysis
    print("Generating convergence analysis...")
    analyzer = MultiScaleConvergenceAnalyzer()
    n_modes_range = [10, 25, 50, 100, 200, 500, 1000]
    conv_results = analyzer.run_convergence_analysis(n_modes_range, num_samples=10)
    
    plot_convergence_multiescale(conv_results, 'v9_convergence_multiescala.png')
    
    # Generate perturbation coherence
    print("Generating perturbation coherence analysis...")
    from symbiotic_coherence_v9 import generate_perturbation_suite
    perturbations = generate_perturbation_suite()
    coherence_report = analyzer.test_symbiotic_coherence(perturbations, n_modes=100)
    
    plot_perturbation_coherence(coherence_report, 'v9_coherence_perturbations.png')
    
    print()
    print("=" * 80)
    print("  VISUALIZATION COMPLETE ✅")
    print("=" * 80)
    print()
    print("Generated files:")
    print("  • v9_convergence_multiescala.png")
    print("  • v9_coherence_perturbations.png")
    print()
    
    return True


if __name__ == "__main__":
    success = generate_all_plots()
    sys.exit(0 if success else 1)
