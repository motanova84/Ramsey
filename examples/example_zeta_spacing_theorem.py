#!/usr/bin/env python3
"""
Example: Demonstrating the vibrational_Ramsey_implies_zeta_spacing theorem

This example shows how to use the theorem to predict relationships between
Ramsey number coherence and Riemann zeta zero spacing.

The theorem states:
    ∀ r s ε, R_ψ(r,s,ε) > N → ∃ t₁ t₂, |t₁ - t₂| < C·ε

Where:
    - R_ψ(r,s,ε) is the vibrational Ramsey number
    - N = 43 is the coherence threshold
    - C ≈ 2.017 is the spectral constant
    - ε is the resonance threshold
"""

import sys
sys.path.append('..')

from zeta_spacing_connection import (
    compute_spectral_constant,
    demonstrate_symbiotic_connection,
    predict_zeta_zero_proximity,
    estimate_zeta_zero_spacing,
    F0,
    N_THRESHOLD
)
import numpy as np


def example_1_basic_theorem():
    """Example 1: Basic usage of the theorem."""
    print("=" * 70)
    print("Example 1: Basic Theorem Usage")
    print("=" * 70)
    print()
    
    # Calculate spectral constant
    C = compute_spectral_constant()
    print(f"Spectral constant C = {C:.6f}")
    print(f"Universal frequency f₀ = {F0} Hz")
    print(f"Coherence threshold N = {N_THRESHOLD}")
    print()
    
    # Test with hypothetical R_ψ(8,8,0.001) = 45
    r, s = 8, 8
    epsilon = 0.001
    R_psi = 45  # Hypothetical value > 43
    
    print(f"Given: R_ψ({r},{s},{epsilon}) = {R_psi}")
    print()
    
    # Apply theorem
    result = demonstrate_symbiotic_connection(r, s, epsilon, R_psi)
    
    if result['coherence_condition']:
        print(f"✓ Theorem applies: R_ψ = {R_psi} > N = {N_THRESHOLD}")
        print(f"  Conclusion: ∃ t₁, t₂ such that |t₁ - t₂| < {result['zeta_spacing_bound']:.6f}")
        print()
        print("  Interpretation:")
        print("  Since the vibrational graph cannot avoid cliques,")
        print("  the zeta zeros cannot avoid spectral proximity.")
    else:
        print(f"✗ Theorem does not apply: R_ψ = {R_psi} ≤ N = {N_THRESHOLD}")
    
    print()


def example_2_compare_cases():
    """Example 2: Comparing cases where theorem applies vs doesn't apply."""
    print("=" * 70)
    print("Example 2: Comparing Different Cases")
    print("=" * 70)
    print()
    
    epsilon = 0.001
    
    # Case A: R_ψ(5,5) = 16 (below threshold)
    print("Case A: R_ψ(5,5,0.001) = 16")
    print("-" * 70)
    result_a = demonstrate_symbiotic_connection(5, 5, epsilon, 16)
    print(f"  Coherence condition: {result_a['coherence_condition']}")
    print(f"  R_ψ value: {result_a['R_psi_value']}")
    if not result_a['coherence_condition']:
        print("  → Theorem does NOT guarantee zeta zero proximity")
    print()
    
    # Case B: R_ψ(10,10) = 50 (above threshold)
    print("Case B: R_ψ(10,10,0.001) = 50 (hypothetical)")
    print("-" * 70)
    result_b = demonstrate_symbiotic_connection(10, 10, epsilon, 50)
    print(f"  Coherence condition: {result_b['coherence_condition']}")
    print(f"  R_ψ value: {result_b['R_psi_value']}")
    if result_b['coherence_condition']:
        print(f"  → Theorem GUARANTEES: |t₁ - t₂| < {result_b['zeta_spacing_bound']:.6f}")
    print()
    
    # Case C: Boundary case R_ψ = 43
    print("Case C: R_ψ(7,7,0.001) = 43 (boundary)")
    print("-" * 70)
    result_c = demonstrate_symbiotic_connection(7, 7, epsilon, 43)
    print(f"  Coherence condition: {result_c['coherence_condition']}")
    print(f"  R_ψ value: {result_c['R_psi_value']}")
    print(f"  → At boundary: theorem requires R_ψ > N (strict inequality)")
    print()


def example_3_epsilon_scaling():
    """Example 3: How zeta spacing bound scales with epsilon."""
    print("=" * 70)
    print("Example 3: Scaling with Epsilon")
    print("=" * 70)
    print()
    
    r, s = 10, 10
    R_psi = 50  # Above threshold
    
    epsilons = [0.0001, 0.001, 0.01, 0.1]
    
    print(f"For R_ψ({r},{s},ε) = {R_psi} > {N_THRESHOLD}:")
    print()
    print(f"{'ε':>10} | {'C·ε':>12} | {'Interpretation':>30}")
    print("-" * 70)
    
    for eps in epsilons:
        bound, C = predict_zeta_zero_proximity(eps)
        interpretation = "Very tight spacing" if bound < 0.01 else \
                        "Tight spacing" if bound < 0.1 else \
                        "Moderate spacing"
        print(f"{eps:>10.4f} | {bound:>12.6f} | {interpretation:>30}")
    
    print()
    print("Observation: The bound scales linearly with ε")
    print("            → Tighter resonance (smaller ε) implies tighter zero spacing")
    print()


def example_4_spectral_analysis():
    """Example 4: Analyzing spectral properties at different heights."""
    print("=" * 70)
    print("Example 4: Spectral Analysis at Different Heights")
    print("=" * 70)
    print()
    
    heights = [F0, F0 * 2, F0 * 5, F0 * 10]
    
    print(f"Average zero spacing Δ(T) at different heights T:")
    print()
    print(f"{'Height T':>12} | {'Δ(T)':>12} | {'Relative to f₀':>20}")
    print("-" * 70)
    
    for T in heights:
        spacing = estimate_zeta_zero_spacing(T)
        ratio = T / F0
        print(f"{T:>12.2f} | {spacing:>12.6f} | {ratio:>20.2f}×f₀")
    
    print()
    print("Observation: As height increases, zero spacing decreases")
    print("            → This is the Montgomery-Odlyzko law")
    print()


def example_5_philosophical_interpretation():
    """Example 5: Philosophical/noetic interpretation of the theorem."""
    print("=" * 70)
    print("Example 5: Philosophical Interpretation")
    print("=" * 70)
    print()
    
    print("The theorem reveals a deep connection between two domains:")
    print()
    
    print("1. GRAPH THEORY (Ramsey):")
    print("   - Vibrational graphs with frequency-based resonance")
    print("   - Emergence of monochromatic cliques under coherence")
    print("   - Governed by f₀ = 141.7001 Hz")
    print()
    
    print("2. ANALYTIC NUMBER THEORY (Riemann):")
    print("   - Zeros of zeta function on critical line Re(s) = 1/2")
    print("   - Spectral spacing following GUE distribution")
    print("   - Also connected to f₀ = 141.7001 Hz")
    print()
    
    print("SYMBIOTIC PRINCIPLE:")
    print("   'If a graph cannot avoid a clique under coherence,")
    print("    then the zeros of ζ(s) cannot avoid spectral proximity.'")
    print()
    
    print("This suggests that f₀ is a UNIVERSAL CONSTANT governing:")
    print("  • Coherence in graphs (combinatorial domain)")
    print("  • Coherence in spectra (analytic domain)")
    print("  • Coherence in consciousness (noetic domain)")
    print()
    
    # Show concrete example
    r, s, epsilon = 10, 10, 0.001
    R_psi = 50
    
    result = demonstrate_symbiotic_connection(r, s, epsilon, R_psi)
    bound = result['zeta_spacing_bound']
    
    print(f"Concrete example:")
    print(f"  R_ψ({r},{s},{epsilon}) = {R_psi} > {N_THRESHOLD}")
    print(f"  → |t₁ - t₂| < {bound:.6f}")
    print()
    print(f"The same coherence threshold that forces cliques in graphs")
    print(f"also forces proximity in zeta zeros!")
    print()


def main():
    """Run all examples."""
    examples = [
        example_1_basic_theorem,
        example_2_compare_cases,
        example_3_epsilon_scaling,
        example_4_spectral_analysis,
        example_5_philosophical_interpretation
    ]
    
    for i, example_func in enumerate(examples, 1):
        example_func()
        if i < len(examples):
            print("\n" + "█" * 70 + "\n")
    
    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
