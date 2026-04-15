#!/usr/bin/env python3
"""
Tests for Riemann-Adelic Module: Hilbert-Pólya Operator & Weil Trace Formula

Validates:
1. Berry-Keating operator construction and diagonalization
2. Weil trace formula computation
3. Spectral determinant function
4. Montgomery-Odlyzko GUE correlation
5. Weil scanner zero extraction
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.math.riemann_adelic import (
    BerryKeatingOperator,
    WeilTraceFormula,
    SpectralDeterminant,
    MontgomeryCorrelation,
    WeilScanner,
    create_hilbert_polya_system
)


class TestBerryKeatingOperator(unittest.TestCase):
    """Test Berry-Keating quantum scaling operator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.n_modes = 64  # Small size for fast tests
        self.f0 = 141.7001
        self.operator = BerryKeatingOperator(n_modes=self.n_modes, f0=self.f0)
    
    def test_operator_initialization(self):
        """Test operator initialization."""
        self.assertEqual(self.operator.n_modes, self.n_modes)
        self.assertEqual(self.operator.f0, self.f0)
        self.assertIsNone(self.operator.H_matrix)
        self.assertIsNone(self.operator.eigenvalues)
    
    def test_operator_construction(self):
        """Test operator matrix construction."""
        H = self.operator.construct_operator()
        
        # Check dimensions
        self.assertEqual(H.shape, (self.n_modes, self.n_modes))
        
        # Check Hermiticity
        self.assertTrue(np.allclose(H, H.T))
        
        # Check not all zeros
        self.assertTrue(np.any(H != 0))
    
    def test_operator_diagonalization(self):
        """Test operator diagonalization."""
        eigenvals, eigenvecs = self.operator.diagonalize()
        
        # Check dimensions
        self.assertEqual(len(eigenvals), self.n_modes)
        self.assertEqual(eigenvecs.shape, (self.n_modes, self.n_modes))
        
        # Check eigenvalues are real (Hermitian operator)
        self.assertTrue(np.all(np.isreal(eigenvals)))
        
        # Check eigenvalues are sorted
        self.assertTrue(np.all(eigenvals[:-1] <= eigenvals[1:]))
    
    def test_weyl_law_density(self):
        """Test Weyl law spectral density computation."""
        # Test at positive energy
        density = self.operator.weyl_law_density(100.0)
        self.assertIsInstance(density, float)
        self.assertTrue(density > 0)
        
        # Test at zero energy
        density_zero = self.operator.weyl_law_density(0.0)
        self.assertEqual(density_zero, 0.0)
        
        # Test at negative energy
        density_neg = self.operator.weyl_law_density(-10.0)
        self.assertEqual(density_neg, 0.0)


class TestWeilTraceFormula(unittest.TestCase):
    """Test Weil trace formula implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.n_modes = 64
        self.operator = BerryKeatingOperator(n_modes=self.n_modes)
        self.operator.diagonalize()
        self.weil = WeilTraceFormula(self.operator)
    
    def test_test_function(self):
        """Test the test function h(x)."""
        # Test symmetry
        self.assertAlmostEqual(self.weil.test_function(5.0), 
                              self.weil.test_function(-5.0))
        
        # Test decay
        self.assertTrue(self.weil.test_function(0.0) > self.weil.test_function(10.0))
        
        # Test positivity
        self.assertTrue(self.weil.test_function(3.0) > 0)
    
    def test_spectral_side(self):
        """Test spectral side computation."""
        spectral = self.weil.spectral_side()
        
        self.assertIsInstance(spectral, (int, float))
        self.assertTrue(spectral > 0)
    
    def test_geometric_term(self):
        """Test geometric term computation."""
        geom = self.weil.geometric_term()
        
        self.assertIsInstance(geom, (int, float))
        self.assertTrue(geom > 0)
    
    def test_gamma_integral_term(self):
        """Test Γ-function integral term."""
        integral = self.weil.gamma_integral_term()
        
        self.assertIsInstance(integral, (int, float))
    
    def test_prime_sum_term(self):
        """Test prime sum term computation."""
        prime_sum = self.weil.prime_sum_term(max_prime=50, max_m=3)
        
        self.assertIsInstance(prime_sum, (int, float))
        self.assertTrue(prime_sum > 0)
    
    def test_arithmetic_side(self):
        """Test arithmetic side computation."""
        arithmetic = self.weil.arithmetic_side()
        
        self.assertIsInstance(arithmetic, (int, float))
    
    def test_weil_residue(self):
        """Test Weil residue computation."""
        result = self.weil.weil_residue()
        
        # Check all required keys present
        self.assertIn('spectral_side', result)
        self.assertIn('arithmetic_side', result)
        self.assertIn('residue', result)
        self.assertIn('relative_residue', result)
        self.assertIn('is_valid', result)
        
        # Check types
        self.assertIsInstance(result['spectral_side'], (int, float))
        self.assertIsInstance(result['arithmetic_side'], (int, float))
        self.assertIsInstance(result['residue'], (int, float))
        self.assertIsInstance(result['is_valid'], bool)
        
        # Check residue is non-negative
        self.assertTrue(result['residue'] >= 0)


class TestSpectralDeterminant(unittest.TestCase):
    """Test spectral determinant function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.n_modes = 32
        self.operator = BerryKeatingOperator(n_modes=self.n_modes)
        self.operator.diagonalize()
        self.det = SpectralDeterminant(self.operator)
    
    def test_compute_determinant(self):
        """Test determinant computation."""
        # Test at t = 0
        det_0 = self.det.compute_determinant(0.0)
        self.assertIsInstance(det_0, complex)
        
        # Test at non-zero t
        det_5 = self.det.compute_determinant(5.0)
        self.assertIsInstance(det_5, complex)
        
        # Test magnitude is finite
        self.assertTrue(np.isfinite(abs(det_5)))
    
    def test_riemann_xi_approximation(self):
        """Test Riemann ξ-function approximation."""
        xi_approx = self.det.riemann_xi_approximation(14.134725)
        
        self.assertIsInstance(xi_approx, (int, float))
        self.assertTrue(xi_approx > 0)
        self.assertTrue(np.isfinite(xi_approx))


class TestMontgomeryCorrelation(unittest.TestCase):
    """Test Montgomery-Odlyzko GUE correlation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.n_modes = 128
        self.operator = BerryKeatingOperator(n_modes=self.n_modes)
        self.operator.diagonalize()
        self.montgomery = MontgomeryCorrelation(self.operator)
    
    def test_normalized_spacings(self):
        """Test normalized spacing computation."""
        spacings = self.montgomery.normalized_spacings()
        
        # Check we have spacings
        self.assertTrue(len(spacings) > 0)
        
        # Check all spacings are positive
        self.assertTrue(np.all(spacings > 0))
        
        # Check mean is approximately 1 (normalized)
        self.assertAlmostEqual(np.mean(spacings), 1.0, places=1)
    
    def test_pair_correlation(self):
        """Test pair correlation function computation."""
        r_vals, R2 = self.montgomery.pair_correlation()
        
        # Check dimensions match
        self.assertEqual(len(r_vals), len(R2))
        
        # Check R2 is non-negative
        self.assertTrue(np.all(R2 >= 0))
    
    def test_gue_prediction(self):
        """Test GUE theoretical prediction."""
        # Test at r = 0
        gue_0 = self.montgomery.gue_prediction(0.0)
        self.assertAlmostEqual(gue_0, 0.0, places=5)
        
        # Test at r = 1
        gue_1 = self.montgomery.gue_prediction(1.0)
        self.assertTrue(0 <= gue_1 <= 1)
        
        # Test at large r (should approach 1)
        gue_large = self.montgomery.gue_prediction(10.0)
        self.assertAlmostEqual(gue_large, 1.0, places=2)
    
    def test_validate_gue(self):
        """Test GUE validation."""
        result = self.montgomery.validate_gue()
        
        # Check all required keys
        self.assertIn('r_values', result)
        self.assertIn('empirical', result)
        self.assertIn('theoretical', result)
        self.assertIn('mse', result)
        self.assertIn('is_gue', result)
        
        # Check types
        self.assertIsInstance(result['mse'], (int, float))
        self.assertIsInstance(result['is_gue'], bool)
        
        # Check MSE is non-negative
        self.assertTrue(result['mse'] >= 0)


class TestWeilScanner(unittest.TestCase):
    """Test Weil scanner for zero extraction."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.n_modes = 256
        self.operator = BerryKeatingOperator(n_modes=self.n_modes)
        self.operator.diagonalize()
        self.scanner = WeilScanner(self.operator)
    
    def test_extract_zeros(self):
        """Test zero extraction."""
        zeros = self.scanner.extract_zeros(n_zeros=10)
        
        # Check we got some zeros
        self.assertTrue(len(zeros) > 0)
        
        # Check all zeros are positive
        self.assertTrue(np.all(zeros > 0))
        
        # Check zeros are sorted
        self.assertTrue(np.all(zeros[:-1] <= zeros[1:]))
    
    def test_odlyzko_zeros_present(self):
        """Test that Odlyzko reference zeros are available."""
        self.assertTrue(len(self.scanner.odlyzko_zeros) > 0)
        
        # Check first zero is correct (approximately)
        self.assertAlmostEqual(self.scanner.odlyzko_zeros[0], 14.134725, places=5)
    
    def test_compare_with_odlyzko(self):
        """Test comparison with Odlyzko tables."""
        result = self.scanner.compare_with_odlyzko(n_compare=10)
        
        # Check all required keys
        self.assertIn('n_compared', result)
        self.assertIn('extracted', result)
        self.assertIn('extracted_scaled', result)
        self.assertIn('odlyzko', result)
        self.assertIn('scale_factor', result)
        self.assertIn('differences', result)
        self.assertIn('mean_error', result)
        self.assertIn('max_error', result)
        self.assertIn('relative_error', result)
        
        # Check types
        self.assertIsInstance(result['n_compared'], int)
        self.assertIsInstance(result['scale_factor'], (int, float))
        self.assertIsInstance(result['mean_error'], (int, float))
        
        # Check scale factor is positive
        self.assertTrue(result['scale_factor'] > 0)
    
    def test_validate_isomorphism(self):
        """Test isomorphism validation."""
        result = self.scanner.validate_isomorphism()
        
        # Check all required keys
        self.assertIn('comparison', result)
        self.assertIn('is_valid_isomorphism', result)
        self.assertIn('quality', result)
        
        # Check types
        self.assertIsInstance(result['is_valid_isomorphism'], bool)
        self.assertIsInstance(result['quality'], str)
        
        # Check quality is one of expected values
        self.assertIn(result['quality'], ['EXCELLENT', 'GOOD', 'FAIR', 'POOR'])


class TestSystemIntegration(unittest.TestCase):
    """Test integrated system functionality."""
    
    def test_create_hilbert_polya_system(self):
        """Test complete system creation."""
        system = create_hilbert_polya_system(n_modes=64)
        
        # Check all components present
        self.assertIn('operator', system)
        self.assertIn('weil_trace', system)
        self.assertIn('spectral_determinant', system)
        self.assertIn('montgomery_correlation', system)
        self.assertIn('weil_scanner', system)
        
        # Check types
        self.assertIsInstance(system['operator'], BerryKeatingOperator)
        self.assertIsInstance(system['weil_trace'], WeilTraceFormula)
        self.assertIsInstance(system['spectral_determinant'], SpectralDeterminant)
        self.assertIsInstance(system['montgomery_correlation'], MontgomeryCorrelation)
        self.assertIsInstance(system['weil_scanner'], WeilScanner)
        
        # Check operator is already diagonalized
        self.assertIsNotNone(system['operator'].eigenvalues)
        self.assertIsNotNone(system['operator'].eigenvectors)


if __name__ == '__main__':
    unittest.main()
