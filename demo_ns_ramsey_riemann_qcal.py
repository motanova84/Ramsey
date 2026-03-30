#!/usr/bin/env python3
"""
Unified NS-Ramsey-Riemann-QCAL Integration Demo
═══════════════════════════════════════════════════════════════════════════════

Demonstrates the complete integration of:
- Navier-Stokes flow on critical axis Re(s) = 1/2
- Ramsey C₇ prime network
- Riemann zeta function on critical line
- QCAL framework unification
- 141.7001 Hz master harmonic

This demo shows how the NS-Ramsey-Riemann framework integrates with the
existing QCAL ecosystem to provide a unified view of mathematics and physics.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import sys
import os
import numpy as np

# Add paths
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.math.ns_ramsey_riemann import UnifiedFramework, F0
from qcal.ramsey_logos_attractor import emergencia_ramsey_qcal, escanear_orden_ramsey_bsd, NODOS_LOGOS


def demonstrate_ns_flow_symmetry():
    """Demonstrate NS flow symmetry around Re(s) = 1/2."""
    print("═" * 80)
    print("I. NAVIER-STOKES FLOW — Symmetry Axis Re(s) = 1/2")
    print("═" * 80)
    print()
    print("The Navier-Stokes flow exhibits a fundamental symmetry:")
    print("  • Critical axis: Re(s) = 1/2 (matches Riemann critical line)")
    print("  • Decay constant: τ = F₀ = 141.7001 Hz")
    print("  • Pressure pulse: p(t) = sin(2π·F₀·t) · exp(-t/τ)")
    print()
    
    framework = UnifiedFramework()
    
    # Sample at various times
    times = [0.0, 0.001, 0.01, 0.05, 0.1]
    print("Time Evolution:")
    print(f"  {'Time (s)':<12} {'Pressure':<15} {'Energy':<15} {'Re(s)'}")
    print("  " + "-" * 60)
    
    for t in times:
        state = framework.ns_flow.get_state(t)
        print(f"  {t:<12.3f} {state.pressure:<15.6f} {state.energy:<15.6e} {state.reynolds}")
    
    print()


def demonstrate_ramsey_network():
    """Demonstrate Ramsey C₇ network and Logos attractor."""
    print("═" * 80)
    print("II. RAMSEY C₇ NETWORK — Primordial Information")
    print("═" * 80)
    print()
    print("The Ramsey network connects prime information with graph structure:")
    print("  • Primes: {2, 3, 5, 7, 11, 13, 17}")
    print("  • Cycle C₇: 7 edges")
    print("  • Complete K₇: 21 edges")
    print("  • Density: 7/21 = 1/3")
    print("  • Ramsey R(3,3) = 6")
    print()
    
    framework = UnifiedFramework()
    
    # Sample network coherence
    times = np.linspace(0, 1.0/F0, 8)  # One period
    print("Network Coherence over one period:")
    print(f"  {'Time (s)':<12} {'Coherence':<15} {'Phase'}")
    print("  " + "-" * 50)
    
    for t in times:
        state = framework.ramsey.get_state(t)
        phase = (t * F0 * 2 * np.pi) % (2 * np.pi)
        print(f"  {t:<12.6f} {state.coherence:<15.6f} {phase:>8.4f}")
    
    print()
    
    # Integrate with QCAL Logos attractor
    print("QCAL Logos Attractor:")
    print(f"  Critical threshold: {NODOS_LOGOS} nodes")
    print()
    
    # Test with different node counts
    node_counts = [10, 30, 51, 100]
    for n_nodes in node_counts:
        resultado = emergencia_ramsey_qcal(n_nodes)
        print(f"  {n_nodes} nodes: {resultado['ramsey_status']}")
        print(f"    PSI emergencia: {resultado['psi_emergencia']:.6f}")
        print(f"    Logos manifestado: {resultado['logos_manifestado']}")
    
    print()


def demonstrate_riemann_critical_line():
    """Demonstrate Riemann zeta on critical line."""
    print("═" * 80)
    print("III. RIEMANN CRITICAL LINE — Spectral Equilibrium")
    print("═" * 80)
    print()
    print("The Riemann zeta function on the critical line s = 1/2 + it:")
    print("  • Critical line: Re(s) = 1/2")
    print("  • Matches NS symmetry axis")
    print("  • Zero density: N(T) ≈ (T/2π)·log(T/2π) - T/2π")
    print()
    
    framework = UnifiedFramework()
    
    # Sample at various imaginary parts
    t_values = [14.1347, 21.022, 25.0109, F0, 100.0, 200.0]
    print("Zeta Values on Critical Line:")
    print(f"  {'t':<12} {'Re(ζ)':<15} {'Im(ζ)':<15} {'|ζ|':<12} {'N(t)'}")
    print("  " + "-" * 70)
    
    for t in t_values:
        state = framework.riemann.get_state(t)
        density = framework.riemann.zero_density(t)
        print(f"  {t:<12.4f} {state.zeta_value.real:<15.6f} {state.zeta_value.imag:<15.6f} "
              f"{state.magnitude:<12.6f} {density:>8.2f}")
    
    print()
    print(f"At F₀ = {F0} Hz:")
    state_f0 = framework.riemann.get_state(F0)
    print(f"  ζ(1/2 + i·{F0}) = {state_f0.zeta_value.real:.6f} + {state_f0.zeta_value.imag:.6f}i")
    print(f"  |ζ| = {state_f0.magnitude:.6f}")
    print(f"  Zero count ≈ {framework.riemann.zero_density(F0):.2f}")
    print()


def demonstrate_master_harmonic():
    """Demonstrate master harmonic at 141.7001 Hz."""
    print("═" * 80)
    print("IV. MASTER HARMONIC — Life and Symbiosis at 141.7001 Hz")
    print("═" * 80)
    print()
    print("The master harmonic A(t) = cos(2π·F₀·t + π/7) unifies all components:")
    print(f"  • Frequency: F₀ = {F0} Hz")
    print(f"  • Period: T = {1.0/F0:.8f} s")
    print(f"  • Phase shift: π/7 (linked to C₇)")
    print()
    
    framework = UnifiedFramework()
    
    # Sample over one period
    period = 1.0 / F0
    times = np.linspace(0, period, 9)[:-1]  # 8 samples
    
    print("Master Harmonic over one period:")
    print(f"  {'Time (s)':<12} {'A(t)':<15} {'Phase (rad)'}")
    print("  " + "-" * 50)
    
    for t in times:
        A_t = framework.master_harmonic(t)
        phase = (2 * np.pi * F0 * t + np.pi/7) % (2 * np.pi)
        print(f"  {t:<12.6f} {A_t:<15.6f} {phase:>12.6f}")
    
    print()


def demonstrate_qcal_transmutation():
    """Demonstrate QCAL transmutation PSI."""
    print("═" * 80)
    print("V. QCAL TRANSMUTATION — Coherence Metric")
    print("═" * 80)
    print()
    print("The QCAL transmutation PSI = exp(-|ζ(1/2+iF₀)| - 1|) measures coherence:")
    print("  • PSI = 1 when |ζ| = 1 (perfect resonance)")
    print("  • PSI → 0 as |ζ| diverges from 1")
    print()
    
    framework = UnifiedFramework()
    
    # Test with various zeta magnitudes
    test_magnitudes = [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
    print("PSI vs Zeta Magnitude:")
    print(f"  {'|ζ|':<12} {'PSI':<15} {'Coherence'}")
    print("  " + "-" * 50)
    
    for mag in test_magnitudes:
        zeta_test = mag + 0.0j
        psi = framework.qcal_transmutation(zeta_test)
        coherence = "Perfect" if psi > 0.99 else ("High" if psi > 0.7 else "Low")
        print(f"  {mag:<12.2f} {psi:<15.6f} {coherence}")
    
    print()
    
    # At F₀
    state_f0 = framework.riemann.get_state(F0)
    psi_f0 = framework.qcal_transmutation(state_f0.zeta_value)
    print(f"At F₀ = {F0} Hz:")
    print(f"  |ζ(1/2 + i·{F0})| = {state_f0.magnitude:.6f}")
    print(f"  PSI = {psi_f0:.6f}")
    print()


def demonstrate_unified_coherence():
    """Demonstrate unified coherence across all components."""
    print("═" * 80)
    print("VI. UNIFIED COHERENCE ANALYSIS")
    print("═" * 80)
    print()
    print("Analyzing coherence across all framework components...")
    print()
    
    framework = UnifiedFramework()
    
    # Analyze over one period
    period = 1.0 / F0
    analysis = framework.analyze_coherence(0.0, period, 100)
    
    print("Statistical Summary:")
    print(f"  Time range: {analysis['time_range'][0]:.6f} - {analysis['time_range'][1]:.6f} s")
    print(f"  Samples: {analysis['n_points']}")
    print()
    print("  Component Metrics:")
    print(f"    NS mean energy:         {analysis['ns_mean_energy']:.6e}")
    print(f"    Ramsey mean coherence:  {analysis['ramsey_mean_coherence']:.6f}")
    print(f"    Riemann mean |ζ|:       {analysis['riemann_mean_magnitude']:.6f}")
    print(f"    PSI mean:               {analysis['psi_mean']:.6f}")
    print()
    
    # Find peak coherence moments
    ramsey_coh = np.array(analysis['ramsey_coherences'])
    psi_vals = np.array(analysis['psi_values'])
    times_arr = np.array(analysis['times'])
    
    peak_idx = np.argmax(ramsey_coh)
    min_idx = np.argmin(ramsey_coh)
    
    print("  Peak Coherence:")
    print(f"    Time: {times_arr[peak_idx]:.6f} s")
    print(f"    Ramsey coherence: {ramsey_coh[peak_idx]:.6f}")
    print()
    
    print("  Minimum Coherence:")
    print(f"    Time: {times_arr[min_idx]:.6f} s")
    print(f"    Ramsey coherence: {ramsey_coh[min_idx]:.6f}")
    print()


def demonstrate_bsd_integration():
    """Demonstrate BSD-Ramsey integration."""
    print("═" * 80)
    print("VII. BSD-RAMSEY INTEGRATION")
    print("═" * 80)
    print()
    print("Connecting elliptic curves with Ramsey network coherence...")
    print()
    
    # Test BSD integration
    test_curves = [
        {'rango_adelico': 0, 'nombre': 'Curve A (rank 0)'},
        {'rango_adelico': 1, 'nombre': 'Curve B (rank 1)'},
        {'rango_adelico': 2, 'nombre': 'Curve C (rank 2)'},
    ]
    
    for curva in test_curves:
        resultado = escanear_orden_ramsey_bsd(curva, "GACTGACT")
        print(f"  {curva['nombre']}:")
        print(f"    Rango: {curva['rango_adelico']}")
        print(f"    Status: {resultado['status']}")
        print(f"    Coherencia: {resultado['coherencia_ramsey']:.6f}")
        print(f"    Conexión BSD: {resultado['conexion_bsd']}")
        print()


def main():
    """Main demonstration."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  NS-RAMSEY-RIEMANN-QCAL UNIFIED FRAMEWORK".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + f"Fundamental Frequency: f₀ = {F0} Hz".center(78) + "║")
    print("║" + "Architecture: QCAL ∞³".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Run all demonstrations
    demonstrate_ns_flow_symmetry()
    demonstrate_ramsey_network()
    demonstrate_riemann_critical_line()
    demonstrate_master_harmonic()
    demonstrate_qcal_transmutation()
    demonstrate_unified_coherence()
    demonstrate_bsd_integration()
    
    print("═" * 80)
    print("FRAMEWORK INTEGRATION COMPLETE")
    print("═" * 80)
    print()
    print("Summary:")
    print("  ✓ Navier-Stokes flow on critical axis Re(s) = 1/2")
    print("  ✓ Ramsey C₇ network with 7 primes")
    print("  ✓ Riemann zeta on critical line")
    print("  ✓ Master harmonic at 141.7001 Hz")
    print("  ✓ QCAL transmutation PSI")
    print("  ✓ Unified coherence analysis")
    print("  ✓ BSD-Ramsey integration")
    print()
    print("All components are unified through f₀ = 141.7001 Hz")
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "∴𓂀Ω∞³".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()


if __name__ == "__main__":
    main()
