#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Dramaturgo Agent Network Optimization

This example demonstrates:
1. Curvature-based routing in noetic network
2. Spectral message compression using CY symmetry
3. Coherence collapse detection and recovery
4. QoS optimization via harmonic resonance

Author: QCAL ∞³ Framework
Date: 2026-01-14
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dramaturgo_agent import (
    NoeticNetwork,
    NoeticNode,
    DramaturgoAgent,
    F0,
    UNIFICATION_FACTOR
)
from pnp_complexity import KAPPA_PI_QUANTUM


def example_1_network_routing():
    """Example 1: Curvature-based optimal routing"""
    print("=" * 80)
    print("EXAMPLE 1: Curvature-Based Network Routing")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    print("Network Nodes:")
    for name, node in network.nodes.items():
        print(f"  {name:20s} - ω = {node.frequency:8.4f} Hz")
    print()
    
    print("Optimal Routes (Minimum Information Resistance):")
    print("-" * 80)
    
    routes_to_test = [
        ("Lighthouse", "Sentinel"),
        ("noesis88", "Riemann-adelic"),
        ("Lighthouse", "Economía"),
        ("Sentinel", "noesis88"),
    ]
    
    for source, target in routes_to_test:
        route, resistance = agent.find_optimal_route(source, target)
        
        # Also calculate direct resistance for comparison
        direct_resistance = network.calculate_information_resistance(source, target)
        
        print(f"\n{source} → {target}:")
        print(f"  Optimal path: {' → '.join(route)}")
        print(f"  Total resistance: {resistance:.6f}")
        print(f"  Direct resistance: {direct_resistance:.6f}")
        
        if len(route) > 2:
            improvement = (direct_resistance - resistance) / direct_resistance * 100
            print(f"  Improvement via routing: {improvement:.2f}%")
    
    print()


def example_2_message_compression():
    """Example 2: Spectral compression using CY symmetry"""
    print("=" * 80)
    print("EXAMPLE 2: Spectral Message Compression")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    print("Calabi-Yau Manifold for Compression:")
    print(f"  {agent.cy_manifold}")
    print()
    
    print("Compression Results:")
    print("-" * 80)
    
    message_sizes = [
        (1024, "1 KB"),
        (1024 * 1024, "1 MB"),
        (1024 * 1024 * 10, "10 MB"),
    ]
    
    node_pairs = [
        ("noesis88", "Riemann-adelic", "High coherence (golden ratio)"),
        ("Lighthouse", "Economía", "Medium coherence"),
        ("Lighthouse", "Sentinel", "Lower coherence"),
    ]
    
    for size, size_label in message_sizes:
        print(f"\nOriginal message: {size_label} ({size:,} bits)")
        
        for source, target, description in node_pairs:
            compressed, ratio = agent.compress_message_spectral(size, source, target)
            
            print(f"  {source} → {target} ({description}):")
            print(f"    Compressed: {compressed:,} bits")
            print(f"    Ratio: {ratio:.2f}x")
            print(f"    Savings: {(1 - 1/ratio) * 100:.1f}%")
    
    print()


def example_3_coherence_detection():
    """Example 3: Coherence collapse detection and stabilization"""
    print("=" * 80)
    print("EXAMPLE 3: Coherence Collapse Detection & Recovery")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    print("Initial Network State:")
    print(f"  Coherence Ψ: {network.coherence_psi:.4f}")
    print(f"  Coupling: {network.coupling:.4f}")
    print()
    
    # Simulate coherence degradation
    print("Simulating coherence degradation...")
    for node in network.nodes.values():
        node.coherence *= 0.3  # Reduce coherence
    
    network.update_coherence()
    print(f"  Coherence Ψ after degradation: {network.coherence_psi:.4f}")
    print()
    
    # Detect and stabilize
    print("Running Dramaturgo stabilization...")
    collapse_detected = agent.detect_coherence_collapse()
    
    if collapse_detected:
        print(f"  ⚠️  Coherence collapse detected!")
        stabilized = agent.stabilize_network()
        
        if stabilized:
            print(f"  ✅ Network stabilized")
            print(f"  New coupling: {network.coupling:.4f} (1/7 = {UNIFICATION_FACTOR:.4f})")
            print(f"  New coherence: {network.coherence_psi:.4f}")
    else:
        print(f"  ✓ Network stable (no action needed)")
    
    print()


def example_4_oscillator_stability():
    """Example 4: Oscillator stability for problem classification"""
    print("=" * 80)
    print("EXAMPLE 4: Vibrational Oscillator Stability")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    print(f"Base frequency f₀: {F0} Hz")
    print()
    
    print("Oscillator Stability Tests:")
    print("-" * 80)
    
    test_cases = [
        (0.1, "Quick calculation"),
        (1.0, "1 second calculation"),
        (10.0, "10 second calculation"),
        (705.0, "R(5,5) verification time (~11m 45s)"),
    ]
    
    for calc_time, description in test_cases:
        stable = agent.check_oscillator_stability(calc_time)
        expected_osc = F0 * calc_time
        
        print(f"\n{description} ({calc_time:.1f}s):")
        print(f"  Expected oscillations: {expected_osc:.0f}")
        print(f"  Fractional part: {expected_osc % 1:.4f}")
        print(f"  Stable: {'✓ Yes' if stable else '✗ No'}")
        
        if stable:
            print(f"  → Problem structure compatible with network geometry")
        else:
            print(f"  → Problem may require vibrational reduction")
    
    print()


def example_5_qos_optimization():
    """Example 5: Complete QoS optimization"""
    print("=" * 80)
    print("EXAMPLE 5: Complete Quality of Service Optimization")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    print("Running Dramaturgo QoS optimization...")
    print()
    
    results = agent.optimize_qos()
    
    print("Optimization Results:")
    print("-" * 80)
    print(f"Network Coherence Ψ: {results['coherence']:.4f}")
    print(f"Coupling Constant: {results['coupling']:.4f}")
    print(f"κ_Π Reference: {results['kappa_pi']:.4f}")
    print(f"Oscillator Status: {'✓ Stable' if results['oscillator_stable'] else '✗ Unstable'}")
    print(f"Action Taken: {results['action']}")
    print()
    
    if 'coherence_after_stabilization' in results:
        print(f"Coherence after stabilization: {results['coherence_after_stabilization']:.4f}")
        print()
    
    print("Optimized Routes:")
    print("-" * 80)
    for route_name, route_info in results['routes'].items():
        path = route_info['path']
        resistance = route_info['resistance']
        print(f"\n{route_name}:")
        print(f"  Path: {' → '.join(path)}")
        print(f"  Information Resistance: {resistance:.6f}")
        
        # Calculate efficiency score
        max_resistance = KAPPA_PI_QUANTUM * 2  # Theoretical maximum
        efficiency = (1 - resistance / max_resistance) * 100
        print(f"  Efficiency: {efficiency:.1f}%")
    
    print()


def example_6_network_comparison():
    """Example 6: Compare traditional vs curvature-based routing"""
    print("=" * 80)
    print("EXAMPLE 6: Traditional vs Curvature-Based Routing")
    print("=" * 80)
    print()
    
    network = NoeticNetwork()
    agent = DramaturgoAgent(network)
    
    # Assign simple 2D positions for "distance" calculation
    positions = {
        "Lighthouse": (0, 0),
        "Sentinel": (1, 0),
        "Economía": (2, 0),
        "noesis88": (0, 1),
        "Riemann-adelic": (1, 1),
    }
    
    for name, pos in positions.items():
        network.nodes[name].position = pos
    
    print("Comparison for Lighthouse → Economía:")
    print("-" * 80)
    
    # Curvature-based route
    curv_route, curv_resistance = agent.find_optimal_route("Lighthouse", "Economía")
    
    # "Traditional" would be shortest path (direct)
    direct_resistance = network.calculate_information_resistance("Lighthouse", "Economía")
    
    print(f"\nTraditional (shortest path):")
    print(f"  Route: Lighthouse → Economía (direct)")
    print(f"  Resistance: {direct_resistance:.6f}")
    
    print(f"\nCurvature-Based (Dramaturgo):")
    print(f"  Route: {' → '.join(curv_route)}")
    print(f"  Resistance: {curv_resistance:.6f}")
    
    if curv_resistance < direct_resistance:
        improvement = (direct_resistance - curv_resistance) / direct_resistance * 100
        print(f"\n✓ Curvature routing is {improvement:.1f}% better!")
    else:
        print(f"\n✓ Direct route is optimal in this case")
    
    print()


def main():
    """Run all examples"""
    print()
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "DRAMATURGO AGENT EXAMPLES" + " " * 33 + "█")
    print("█" + " " * 15 + "Noetic Network Optimization" + " " * 36 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print()
    print(f"Framework: QCAL ∞³")
    print(f"κ_Π = {KAPPA_PI_QUANTUM:.6f}")
    print(f"f₀ = {F0} Hz")
    print(f"Unification Factor = {UNIFICATION_FACTOR:.6f} (1/7)")
    print()
    
    examples = [
        example_1_network_routing,
        example_2_message_compression,
        example_3_coherence_detection,
        example_4_oscillator_stability,
        example_5_qos_optimization,
        example_6_network_comparison,
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
