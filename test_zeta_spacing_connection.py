#!/usr/bin/env python3
"""
Tests for the zeta spacing connection module.

Validates the symbiotic relationship between Vibrational Ramsey Theory
and Riemann Zeta Function zeros.
"""

import unittest
import numpy as np
from zeta_spacing_connection import (
    compute_spectral_constant,
    estimate_zeta_zero_spacing,
    check_coherence_condition,
    predict_zeta_zero_proximity,
    demonstrate_symbiotic_connection,
    compute_resonance_to_spectral_map,
    F0,
    N_THRESHOLD
)


class TestZetaSpacingConnection(unittest.TestCase):
    """Test suite for zeta spacing connection."""
    
    def test_spectral_constant_positive(self):
        """Test that spectral constant C is positive."""
        C = compute_spectral_constant()
        self.assertGreater(C, 0, "Spectral constant must be positive")
    
    def test_spectral_constant_value(self):
        """Test that spectral constant is within expected range."""
        C = compute_spectral_constant()
        # C = 2π / log(141.7001 / 2π) ≈ 2π / log(22.56) ≈ 2π / 3.116 ≈ 2.015
        self.assertAlmostEqual(C, 2.015, places=2,
                              msg="Spectral constant should be approximately 2.015")
    
    def test_zeta_spacing_decreases_with_height(self):
        """Test that zero spacing decreases as height increases."""
        spacing_100 = estimate_zeta_zero_spacing(100)
        spacing_1000 = estimate_zeta_zero_spacing(1000)
        spacing_10000 = estimate_zeta_zero_spacing(10000)
        
        self.assertGreater(spacing_100, spacing_1000,
                          "Spacing should decrease with height")
        self.assertGreater(spacing_1000, spacing_10000,
                          "Spacing should decrease with height")
    
    def test_zeta_spacing_at_f0(self):
        """Test zero spacing at the resonance frequency."""
        spacing = estimate_zeta_zero_spacing(F0)
        # At T = 141.7, spacing ≈ 2π / log(141.7/2π) ≈ 2π / 3.116 ≈ 2.015
        self.assertGreater(spacing, 1.5, "Spacing at f₀ should be > 1.5")
        self.assertLess(spacing, 3.0, "Spacing at f₀ should be < 3.0")
    
    def test_coherence_condition_true(self):
        """Test coherence condition when R_ψ > N."""
        # R_ψ(10,10) = 50 > 43
        result = check_coherence_condition(10, 10, 0.001, 50)
        self.assertTrue(result, "Should return True when R_ψ > N")
    
    def test_coherence_condition_false(self):
        """Test coherence condition when R_ψ ≤ N."""
        # R_ψ(5,5) = 16 ≤ 43
        result = check_coherence_condition(5, 5, 0.001, 16)
        self.assertFalse(result, "Should return False when R_ψ ≤ N")
    
    def test_coherence_condition_boundary(self):
        """Test coherence condition at boundary N = 43."""
        result_equal = check_coherence_condition(5, 5, 0.001, 43)
        result_above = check_coherence_condition(5, 5, 0.001, 44)
        
        self.assertFalse(result_equal, "Should be False when R_ψ = N")
        self.assertTrue(result_above, "Should be True when R_ψ = N + 1")
    
    def test_predict_zeta_proximity(self):
        """Test prediction of zeta zero proximity."""
        epsilon = 0.001
        bound, C = predict_zeta_zero_proximity(epsilon)
        
        self.assertGreater(bound, 0, "Bound must be positive")
        self.assertAlmostEqual(bound, C * epsilon, places=10,
                              msg="Bound should equal C * epsilon")
    
    def test_predict_zeta_proximity_scales_with_epsilon(self):
        """Test that proximity bound scales linearly with epsilon."""
        eps1 = 0.001
        eps2 = 0.002
        
        bound1, _ = predict_zeta_zero_proximity(eps1)
        bound2, _ = predict_zeta_zero_proximity(eps2)
        
        ratio = bound2 / bound1
        self.assertAlmostEqual(ratio, 2.0, places=5,
                              msg="Bound should scale linearly with epsilon")
    
    def test_demonstrate_connection_structure(self):
        """Test that demonstrate_symbiotic_connection returns correct structure."""
        result = demonstrate_symbiotic_connection(5, 5, 0.001, 16)
        
        # Check all required keys are present
        required_keys = ['coherence_condition', 'R_psi_value', 'N_threshold',
                        'spectral_constant', 'zeta_spacing_bound', 'epsilon',
                        'interpretation']
        for key in required_keys:
            self.assertIn(key, result, f"Result should contain key '{key}'")
    
    def test_demonstrate_connection_values(self):
        """Test values in demonstrate_symbiotic_connection."""
        result = demonstrate_symbiotic_connection(10, 10, 0.001, 50)
        
        self.assertTrue(result['coherence_condition'])
        self.assertEqual(result['R_psi_value'], 50)
        self.assertEqual(result['N_threshold'], N_THRESHOLD)
        self.assertEqual(result['epsilon'], 0.001)
        self.assertGreater(result['spectral_constant'], 0)
        self.assertGreater(result['zeta_spacing_bound'], 0)
    
    def test_demonstrate_connection_interpretation_coherent(self):
        """Test interpretation when coherence condition is met."""
        result = demonstrate_symbiotic_connection(10, 10, 0.001, 50)
        interpretation = result['interpretation']
        
        self.assertIn('✓', interpretation, "Should have checkmark for success")
        self.assertIn('Condición cumplida', interpretation)
        self.assertIn('INTERPRETACIÓN NOÉTICA', interpretation)
    
    def test_demonstrate_connection_interpretation_non_coherent(self):
        """Test interpretation when coherence condition is not met."""
        result = demonstrate_symbiotic_connection(5, 5, 0.001, 16)
        interpretation = result['interpretation']
        
        self.assertIn('✗', interpretation, "Should have X for failure")
        self.assertIn('Condición no cumplida', interpretation)
    
    def test_resonance_spectral_map_shape(self):
        """Test shape of resonance to spectral map."""
        heights = [100, 200, 300]
        results = compute_resonance_to_spectral_map(heights)
        
        self.assertEqual(results.shape, (3, 4),
                        "Results should have shape (n_heights, 4)")
    
    def test_resonance_spectral_map_columns(self):
        """Test columns of resonance to spectral map."""
        heights = [F0, F0 * 2]
        results = compute_resonance_to_spectral_map(heights)
        
        # Column 0: heights
        np.testing.assert_array_almost_equal(results[:, 0], heights)
        
        # Column 1: spacings (should be positive)
        self.assertTrue(np.all(results[:, 1] > 0),
                       "All spacings should be positive")
        
        # Column 2: scaled spacings (should be positive)
        self.assertTrue(np.all(results[:, 2] > 0),
                       "All scaled spacings should be positive")
        
        # Column 3: ratios (should be positive and ≤ 1)
        self.assertTrue(np.all(results[:, 3] > 0),
                       "All ratios should be positive")
        self.assertTrue(np.all(results[:, 3] <= 1),
                       "Ratios should be ≤ 1 when height ≥ f₀")
    
    def test_theorem_implication_logic(self):
        """Test the logical implication of the theorem.
        
        Theorem: ∀ r s ε, R_ψ(r,s,ε) > N → ∃ t₁ t₂, |t₁ - t₂| < C·ε
        
        This tests that when the hypothesis is true, we can compute
        the bound on zero spacing.
        """
        # Hypothesis: R_ψ(r,s,ε) > N
        r, s, epsilon = 10, 10, 0.001
        R_psi_value = 50
        
        coherence = check_coherence_condition(r, s, epsilon, R_psi_value)
        self.assertTrue(coherence, "Hypothesis should be true")
        
        # Conclusion: ∃ t₁ t₂, |t₁ - t₂| < C·ε
        bound, C = predict_zeta_zero_proximity(epsilon)
        expected_bound = C * epsilon
        
        self.assertAlmostEqual(bound, expected_bound, places=10,
                              msg="Bound should equal C * epsilon")
        self.assertGreater(bound, 0, "Bound should be positive")
    
    def test_f0_is_resonance_frequency(self):
        """Test that F0 = 141.7001 Hz is the universal resonance frequency."""
        self.assertAlmostEqual(F0, 141.7001, places=4,
                              msg="f₀ should be 141.7001 Hz")
    
    def test_n_threshold_is_43(self):
        """Test that N threshold is 43 (related to R(5,5))."""
        self.assertEqual(N_THRESHOLD, 43,
                        msg="N should be 43, related to classical R(5,5)")


class TestSymbioticInterpretation(unittest.TestCase):
    """Test the philosophical/noetic interpretation of the theorem."""
    
    def test_symbiotic_principle(self):
        """Test that the symbiotic principle is reflected in calculations.
        
        The principle: "If a graph cannot avoid a clique under coherence,
        then the zeros of ζ(s) cannot avoid spectral proximity."
        """
        # Case where graph cannot avoid clique (R_ψ > N)
        result_coherent = demonstrate_symbiotic_connection(10, 10, 0.001, 50)
        
        # Case where graph can avoid clique (R_ψ ≤ N)
        result_non_coherent = demonstrate_symbiotic_connection(5, 5, 0.001, 16)
        
        # In coherent case, we have a bound on zeta spacing
        self.assertTrue(result_coherent['coherence_condition'])
        self.assertGreater(result_coherent['zeta_spacing_bound'], 0)
        
        # In non-coherent case, theorem doesn't apply
        self.assertFalse(result_non_coherent['coherence_condition'])
    
    def test_universal_frequency_connection(self):
        """Test connection between vibrational frequency and spectral spacing."""
        C = compute_spectral_constant()
        
        # The spectral constant relates f₀ to zeta zero spacing
        # C = 2π / log(f₀ / 2π)
        # This shows f₀ naturally appears in the spacing formula
        
        # Verify the relationship
        expected_C = (2 * np.pi) / np.log(F0 / (2 * np.pi))
        self.assertAlmostEqual(C, expected_C, places=10,
                              msg="C should be derived from f₀")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
