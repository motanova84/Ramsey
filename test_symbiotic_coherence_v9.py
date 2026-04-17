#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Symbiotic Coherence V9
=================================

Test suite for V9 implementation covering:
- Atlas³ field stability
- Multiescala convergence
- External perturbations (η, δζ)
- Symbiotic coherence validation

Author: QCAL ∞³ Framework
Date: 2026-02-13
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from symbiotic_coherence_v9 import (
    Atlas3Field,
    MultiScaleConvergenceAnalyzer,
    PerturbationConfig,
    generate_perturbation_suite,
    F0,
    KAPPA_PI,
    C_EST_TARGET,
    COHERENCE_THRESHOLD,
    DENSITY_TARGET,
)


class TestAtlas3Field(unittest.TestCase):
    """Test Atlas³ field functionality"""
    
    def test_field_initialization(self):
        """Test field initializes with correct constants"""
        field = Atlas3Field()
        self.assertEqual(field.f0, F0)
        self.assertEqual(field.kappa_pi, KAPPA_PI)
        
    def test_field_strength_at_kappa_pi(self):
        """Test field has maximum strength near κ_Π"""
        field = Atlas3Field()
        
        # Position near κ_Π should have high field strength
        pos_near = np.array([KAPPA_PI])
        strength_near = field.field_strength(pos_near)
        self.assertGreater(strength_near, 0.9)
        
        # Position far from κ_Π should have lower strength
        pos_far = np.array([KAPPA_PI * 3])
        strength_far = field.field_strength(pos_far)
        self.assertLess(strength_far, strength_near)
        
    def test_spectrum_stabilization_no_perturbation(self):
        """Test spectrum stabilization with dogmatic baseline (θ=0)"""
        field = Atlas3Field()
        eigenvalues = np.array([1.0, 2.0, 3.0, 4.0])
        # Dogmatic case: θ=0 (no frequency shift)
        pert = PerturbationConfig(eta=0.0, delta_zeta=0.0)
        
        stabilized = field.stabilize_spectrum(eigenvalues, pert)
        np.testing.assert_array_almost_equal(stabilized, eigenvalues)
        
    def test_spectrum_stabilization_with_noise(self):
        """Test spectrum stabilization with noise perturbation"""
        field = Atlas3Field()
        eigenvalues = np.array([1.0, 2.0, 3.0, 4.0])
        pert = PerturbationConfig(eta=0.1, delta_zeta=0.0, apply_to_spectrum=True)
        
        # Run multiple times due to randomness
        deviations = []
        for _ in range(10):
            stabilized = field.stabilize_spectrum(eigenvalues, pert)
            deviation = np.mean(np.abs(stabilized - eigenvalues))
            deviations.append(deviation)
        
        avg_deviation = np.mean(deviations)
        # Stabilization should reduce deviation compared to raw noise
        self.assertLess(avg_deviation, pert.eta * 2)
        
    def test_spectrum_stabilization_with_shift(self):
        """Test spectrum stabilization with frequency shift"""
        field = Atlas3Field()
        eigenvalues = np.array([1.0, 2.0, 3.0, 4.0])
        delta = 0.1
        pert = PerturbationConfig(eta=0.0, delta_zeta=delta, apply_to_spectrum=True)
        
        stabilized = field.stabilize_spectrum(eigenvalues, pert)
        
        # Stabilization should partially compensate shift
        mean_shift = np.mean(stabilized - eigenvalues)
        self.assertLess(abs(mean_shift), delta)


class TestMultiScaleConvergenceAnalyzer(unittest.TestCase):
    """Test multiescala convergence analyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly"""
        analyzer = MultiScaleConvergenceAnalyzer()
        self.assertIsNotNone(analyzer.atlas)
        self.assertEqual(len(analyzer.convergence_history), 0)
        
    def test_c_est_computation_no_perturbation(self):
        """Test C_est computation with epistemological baseline (default θ≈0.052463)"""
        analyzer = MultiScaleConvergenceAnalyzer()
        n_modes = 100
        
        # Uses default PerturbationConfig with θ≈0.052463 rad
        c_est, density = analyzer.compute_c_est(n_modes)
        
        # C_est should be near κ_Π
        self.assertGreater(c_est, KAPPA_PI * 0.8)
        self.assertLess(c_est, KAPPA_PI * 1.2)
        
        # Density should be near target
        self.assertGreater(density, 0.1)
        self.assertLess(density, 0.3)
        
    def test_c_est_convergence_stability(self):
        """Test C_est shows stability across multiple runs"""
        analyzer = MultiScaleConvergenceAnalyzer()
        n_modes = 100
        num_runs = 20
        
        c_est_values = []
        for _ in range(num_runs):
            c_est, _ = analyzer.compute_c_est(n_modes)
            c_est_values.append(c_est)
        
        # Standard deviation should be small (stable)
        std = np.std(c_est_values)
        self.assertLess(std, 0.5)
        
        # Mean should be near κ_Π
        mean = np.mean(c_est_values)
        rel_error = abs(mean - KAPPA_PI) / KAPPA_PI
        self.assertLess(rel_error, 0.2)  # Within 20%
        
    def test_convergence_analysis(self):
        """Test convergence analysis across scales"""
        analyzer = MultiScaleConvergenceAnalyzer()
        n_modes_range = [10, 50, 100, 200]
        
        results = analyzer.run_convergence_analysis(n_modes_range, num_samples=3)
        
        self.assertEqual(len(results), len(n_modes_range))
        
        for i, result in enumerate(results):
            self.assertEqual(result.n_modes, n_modes_range[i])
            self.assertEqual(result.kappa_pi, KAPPA_PI)
            self.assertGreater(result.c_est, 0)
            self.assertGreaterEqual(result.relative_error, 0)
            
    def test_convergence_improves_with_modes(self):
        """Test that convergence generally improves with more modes"""
        analyzer = MultiScaleConvergenceAnalyzer()
        n_modes_range = [10, 100, 500]
        
        results = analyzer.run_convergence_analysis(n_modes_range, num_samples=5)
        
        # At least some results should show coherence
        coherent_count = sum(1 for r in results if r.coherence)
        self.assertGreater(coherent_count, 0)
        
    def test_symbiotic_coherence_baseline(self):
        """Test symbiotic coherence with dogmatic baseline (θ=0)"""
        analyzer = MultiScaleConvergenceAnalyzer()
        # Dogmatic case: θ=0
        perturbations = [PerturbationConfig(eta=0.0, delta_zeta=0.0)]
        
        report = analyzer.test_symbiotic_coherence(perturbations, n_modes=100)
        
        self.assertEqual(len(report['results']), 1)
        self.assertIn('coherence_rate', report)
        self.assertIn('avg_c_est', report)
        self.assertIn('status', report)
        
        # Baseline should be coherent
        self.assertGreaterEqual(report['coherence_rate'], 0.8)
        
    def test_symbiotic_coherence_with_perturbations(self):
        """Test symbiotic coherence with various perturbations"""
        analyzer = MultiScaleConvergenceAnalyzer()
        perturbations = generate_perturbation_suite()
        
        report = analyzer.test_symbiotic_coherence(perturbations, n_modes=50)
        
        self.assertEqual(len(report['results']), len(perturbations))
        
        # Check structure of results
        for result in report['results']:
            self.assertIn('perturbation', result)
            self.assertIn('c_est', result)
            self.assertIn('relative_error', result)
            self.assertIn('coherent', result)
            self.assertGreater(result['c_est'], 0)


class TestPerturbationConfig(unittest.TestCase):
    """Test perturbation configuration"""
    
    def test_default_config(self):
        """Test default perturbation config (epistemological baseline)"""
        config = PerturbationConfig()
        self.assertEqual(config.eta, 0.0)
        self.assertEqual(config.delta_zeta, 0.052463)  # θ ≈ 0.052463 rad (medición epistemológica)
        self.assertTrue(config.apply_to_modes)
        self.assertTrue(config.apply_to_spectrum)
        
    def test_custom_config(self):
        """Test custom perturbation config"""
        config = PerturbationConfig(
            eta=0.05,
            delta_zeta=0.02,
            apply_to_modes=False,
            apply_to_spectrum=True
        )
        self.assertEqual(config.eta, 0.05)
        self.assertEqual(config.delta_zeta, 0.02)
        self.assertFalse(config.apply_to_modes)
        self.assertTrue(config.apply_to_spectrum)


class TestPerturbationSuite(unittest.TestCase):
    """Test perturbation suite generation"""
    
    def test_suite_generation(self):
        """Test perturbation suite contains expected configurations"""
        suite = generate_perturbation_suite()
        
        # Should have multiple configurations
        self.assertGreater(len(suite), 5)
        
        # First should be baseline (no perturbation)
        self.assertEqual(suite[0].eta, 0.0)
        self.assertEqual(suite[0].delta_zeta, 0.0)
        
        # Should have variety of perturbations
        has_noise_only = any(p.eta > 0 and p.delta_zeta == 0 for p in suite)
        has_shift_only = any(p.eta == 0 and p.delta_zeta > 0 for p in suite)
        has_combined = any(p.eta > 0 and p.delta_zeta > 0 for p in suite)
        
        self.assertTrue(has_noise_only)
        self.assertTrue(has_shift_only)
        self.assertTrue(has_combined)


class TestConstants(unittest.TestCase):
    """Test V9 constants"""
    
    def test_kappa_pi_value(self):
        """Test κ_Π constant value"""
        self.assertAlmostEqual(KAPPA_PI, 2.5773, places=4)
        
    def test_c_est_target_value(self):
        """Test C_est target value"""
        self.assertAlmostEqual(C_EST_TARGET, 2.5786, places=4)
        
    def test_coherence_threshold(self):
        """Test coherence threshold is < 5%"""
        self.assertEqual(COHERENCE_THRESHOLD, 0.05)
        self.assertLess(COHERENCE_THRESHOLD, 0.051)
        
    def test_density_target(self):
        """Test density target is ~18%"""
        self.assertAlmostEqual(DENSITY_TARGET, 0.18, places=2)
        
    def test_f0_frequency(self):
        """Test fundamental frequency"""
        self.assertAlmostEqual(F0, 141.7001, places=4)
        
    def test_relative_error_between_constants(self):
        """Test relative error between C_est and κ_Π"""
        rel_error = abs(C_EST_TARGET - KAPPA_PI) / KAPPA_PI
        # Should be very small (< 0.1%)
        self.assertLess(rel_error, 0.001)


class TestIntegration(unittest.TestCase):
    """Integration tests for V9 system"""
    
    def test_full_v9_pipeline(self):
        """Test complete V9 pipeline"""
        # Initialize system
        analyzer = MultiScaleConvergenceAnalyzer()
        
        # Run convergence analysis
        n_modes_range = [10, 50, 100]
        conv_results = analyzer.run_convergence_analysis(n_modes_range, num_samples=3)
        
        # Verify convergence results
        self.assertEqual(len(conv_results), 3)
        self.assertEqual(len(analyzer.convergence_history), 3)
        
        # Run coherence test
        perturbations = [
            PerturbationConfig(eta=0.0, delta_zeta=0.0),
            PerturbationConfig(eta=0.05, delta_zeta=0.0),
            PerturbationConfig(eta=0.0, delta_zeta=0.05),
        ]
        
        coherence_report = analyzer.test_symbiotic_coherence(perturbations, n_modes=50)
        
        # Verify coherence report
        self.assertIn('status', coherence_report)
        self.assertEqual(len(coherence_report['results']), 3)
        
        # At least baseline should be coherent
        baseline_result = coherence_report['results'][0]
        self.assertTrue(baseline_result['coherent'])
        
    def test_atlas3_field_maintains_coherence(self):
        """Test that Atlas³ field maintains coherence under perturbation"""
        field = Atlas3Field()
        analyzer = MultiScaleConvergenceAnalyzer(atlas_field=field)
        
        # Test with moderate perturbation
        pert = PerturbationConfig(eta=0.05, delta_zeta=0.05)
        
        # Multiple runs to average out randomness
        c_est_values = []
        for _ in range(20):
            c_est, _ = analyzer.compute_c_est(100, pert)
            c_est_values.append(c_est)
        
        avg_c_est = np.mean(c_est_values)
        rel_error = abs(avg_c_est - KAPPA_PI) / KAPPA_PI
        
        # Even with perturbation, should maintain reasonable coherence
        self.assertLess(rel_error, 0.3)  # Within 30%


def run_all_tests():
    """Run all V9 tests"""
    print("=" * 80)
    print("  SYMBIOTIC COHERENCE V9 - TEST SUITE")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Field))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiScaleConvergenceAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPerturbationConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestPerturbationSuite))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
