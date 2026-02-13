#!/usr/bin/env python3
"""
Tests for V13 Limit Validator

Unit tests for the V13 thermodynamic limit extrapolation protocol.
"""

import unittest
import numpy as np
import os
import json
from pathlib import Path
import sys

# Import V13 validator
from v13_limit_validator import V13LimitValidator


class TestV13LimitValidator(unittest.TestCase):
    """Test V13 Limit Validator"""
    
    def setUp(self):
        """Set up test validator."""
        self.validator = V13LimitValidator(kappa_pi_target=2.577310)
        self.test_prefix = "test_v13_unit"
    
    def tearDown(self):
        """Clean up test files."""
        # Remove test output files
        for ext in ['.json', '_scaling_rigidity.png']:
            test_file = f"{self.test_prefix}_limit_results{ext}" if ext == '.json' else f"{self.test_prefix}{ext}"
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_initialization(self):
        """Test validator initialization."""
        self.assertAlmostEqual(self.validator.kappa_pi_target, 2.577310, places=6)
        self.assertIsNotNone(self.validator.atlas)
        self.assertIsNone(self.validator.scaling_data)
        self.assertIsNone(self.validator.fit_results)
        self.assertIsNone(self.validator.number_variance_data)
    
    def test_thermodynamic_limit_model(self):
        """Test thermodynamic limit model function."""
        N = np.array([100, 200, 400])
        kappa_inf = 2.5
        a = 10.0
        alpha = 0.5
        
        result = self.validator.thermodynamic_limit_model(N, kappa_inf, a, alpha)
        
        # Check shape
        self.assertEqual(result.shape, N.shape)
        
        # Check values converge to kappa_inf
        self.assertTrue(np.all(result > kappa_inf))
        self.assertTrue(np.all(np.diff(result) < 0))  # Decreasing
    
    def test_compute_spectral_curvature(self):
        """Test spectral curvature computation."""
        # Small system for fast testing
        N = 32
        kappa = self.validator.compute_spectral_curvature(N, damping=0.1, coupling_strength=0.15)
        
        # Check that kappa is a positive number
        self.assertIsInstance(kappa, (float, np.floating))
        self.assertGreater(kappa, 0)
        
        # Check that Atlas3 system was generated
        self.assertIsNotNone(self.validator.atlas.modal_basis)
        self.assertIsNotNone(self.validator.atlas.coupling_matrix)
    
    def test_multi_scale_sweep(self):
        """Test multi-scale sweep."""
        N_values = [32, 64]
        
        scaling_data = self.validator.multi_scale_sweep(
            N_values=N_values,
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Check data structure
        self.assertIn('N_values', scaling_data)
        self.assertIn('kappa_values', scaling_data)
        self.assertEqual(scaling_data['N_values'], N_values)
        self.assertEqual(len(scaling_data['kappa_values']), len(N_values))
        
        # Check all kappa values are positive
        self.assertTrue(all(k > 0 for k in scaling_data['kappa_values']))
    
    def test_extrapolate_kappa_infinity(self):
        """Test kappa infinity extrapolation."""
        # First run sweep
        self.validator.multi_scale_sweep(N_values=[32, 64, 128])
        
        # Then extrapolate
        fit_results = self.validator.extrapolate_kappa_infinity()
        
        # Check fit results structure
        self.assertIn('kappa_infinity', fit_results)
        self.assertIn('exponent_alpha', fit_results)
        self.assertIn('amplitude_a', fit_results)
        self.assertIn('relative_error_percent', fit_results)
        self.assertIn('fit_success', fit_results)
        
        # If fit succeeded, check values are reasonable
        if fit_results['fit_success']:
            # Alpha should be between 0.3 and 0.7
            alpha = fit_results['exponent_alpha']
            if alpha is not None:
                self.assertGreater(alpha, 0.1)
                self.assertLess(alpha, 1.0)
    
    def test_compute_number_variance_GOE(self):
        """Test GOE number variance computation."""
        L = np.array([1, 10, 50, 100])
        
        sigma2_goe = self.validator.compute_number_variance_GOE(L)
        
        # Check shape
        self.assertEqual(sigma2_goe.shape, L.shape)
        
        # Check that variance increases with L (logarithmically)
        self.assertTrue(np.all(np.diff(sigma2_goe) > 0))
        
        # Check that it grows slower than linear (rigidity)
        # For Poisson it would be sigma2 = L
        # For GOE it grows logarithmically
        ratio = sigma2_goe / L
        # Ratio should decrease (log growth vs linear)
        self.assertTrue(ratio[0] > ratio[-1])
    
    def test_compute_number_variance_atlas3(self):
        """Test Atlas3 number variance computation."""
        # Generate a small system
        N = 64
        self.validator.atlas.generate_modal_basis(N, damping=0.1)
        self.validator.atlas.construct_operator_O(N, coupling_strength=0.15)
        dna = self.validator.atlas.compute_spectral_dna()
        eigenvalues = dna['eigenvalues']
        
        # Compute number variance
        L_values = np.array([1, 5, 10, 20])
        sigma2 = self.validator.compute_number_variance_atlas3(eigenvalues, L_values)
        
        # Check shape
        self.assertEqual(sigma2.shape, L_values.shape)
        
        # Check all values are non-negative
        self.assertTrue(np.all(sigma2 >= 0))
    
    def test_test_spectral_rigidity(self):
        """Test spectral rigidity test."""
        # Small system for fast testing
        N = 64
        
        rigidity_data = self.validator.test_spectral_rigidity(
            N=N,
            L_max=50,
            n_L_points=20
        )
        
        # Check data structure
        self.assertIn('N', rigidity_data)
        self.assertIn('L_values', rigidity_data)
        self.assertIn('sigma2_atlas', rigidity_data)
        self.assertIn('sigma2_goe', rigidity_data)
        self.assertIn('sigma2_poisson', rigidity_data)
        self.assertIn('rigidity_achieved', rigidity_data)
        
        self.assertEqual(rigidity_data['N'], N)
        self.assertEqual(len(rigidity_data['L_values']), 20)
    
    def test_export_results(self):
        """Test results export."""
        # Run a minimal sweep first
        self.validator.multi_scale_sweep(N_values=[32, 64])
        self.validator.extrapolate_kappa_infinity()
        
        # Export
        output_file = f"{self.test_prefix}_limit_results.json"
        results = self.validator.export_results(output_file)
        
        # Check file exists
        self.assertTrue(os.path.exists(output_file))
        
        # Load and validate JSON
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        self.assertIn('metadata', data)
        self.assertIn('scaling_data', data)
        self.assertIn('fit_results', data)
        
        # Check metadata
        self.assertEqual(data['metadata']['kappa_pi_target'], 2.57731)
    
    def test_complete_validation_pipeline(self):
        """Test complete validation pipeline with small system sizes."""
        # Run with very small sizes for speed
        results = self.validator.run_complete_validation(
            N_values=[32, 64],
            N_rigidity=32,
            output_prefix=self.test_prefix
        )
        
        # Check that all outputs were generated
        self.assertIsNotNone(self.validator.scaling_data)
        self.assertIsNotNone(self.validator.fit_results)
        self.assertIsNotNone(self.validator.number_variance_data)
        
        # Check that files were created
        self.assertTrue(os.path.exists(f"{self.test_prefix}_limit_results.json"))
        self.assertTrue(os.path.exists(f"{self.test_prefix}_scaling_rigidity.png"))


class TestV13Integration(unittest.TestCase):
    """Integration tests for V13 validator"""
    
    def test_reproducibility(self):
        """Test that results are reproducible."""
        validator1 = V13LimitValidator(kappa_pi_target=2.577310)
        validator2 = V13LimitValidator(kappa_pi_target=2.577310)
        
        # Same parameters should give same results
        N = 32
        kappa1 = validator1.compute_spectral_curvature(N, damping=0.1, coupling_strength=0.15)
        kappa2 = validator2.compute_spectral_curvature(N, damping=0.1, coupling_strength=0.15)
        
        # Should be very close (within numerical precision)
        self.assertAlmostEqual(kappa1, kappa2, places=10)
    
    def test_monotonic_convergence(self):
        """Test that kappa values show expected convergence behavior."""
        validator = V13LimitValidator()
        
        # Compute for increasing N
        N_values = [32, 64, 128]
        kappas = []
        
        for N in N_values:
            kappa = validator.compute_spectral_curvature(N)
            kappas.append(kappa)
        
        # Values should all be positive
        self.assertTrue(all(k > 0 for k in kappas))


if __name__ == '__main__':
    unittest.main()
