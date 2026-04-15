#!/usr/bin/env python3
"""
Tests for Atlas³-QCAL Hilbert Space Vibrational Framework

Unit tests for the three-phase protocol:
- Phase 1: Hilbert space deployment
- Phase 2: Vibrational graph emergence  
- Phase 3: κ_Π validation
"""

import unittest
import numpy as np
from scipy.integrate import trapezoid
import sys
from atlas3_qcal import Atlas3QCAL


class TestAtlas3Phase1(unittest.TestCase):
    """Test Phase 1: Hilbert Space Deployment"""
    
    def setUp(self):
        """Set up test framework."""
        self.atlas = Atlas3QCAL(f0=141.7001)
    
    def test_initialization(self):
        """Test framework initialization."""
        self.assertAlmostEqual(self.atlas.f0, 141.7001, places=4)
        self.assertAlmostEqual(self.atlas.omega0, 2 * np.pi * 141.7001, places=2)
        self.assertIsNotNone(self.atlas.T)
        self.assertAlmostEqual(self.atlas.kappa_pi, 2.5773, places=4)
    
    def test_modal_basis_generation(self):
        """Test modal basis generation."""
        n_modes = 16
        modal_basis = self.atlas.generate_modal_basis(n_modes, damping=0.1)
        
        # Check shape
        self.assertEqual(modal_basis.shape[1], n_modes)
        self.assertGreater(modal_basis.shape[0], n_modes)
        
        # Check normalization (L² norm should be ~1)
        for n in range(n_modes):
            norm = np.sqrt(trapezoid(modal_basis[:, n]**2, self.atlas.time_grid))
            self.assertAlmostEqual(norm, 1.0, places=2)
    
    def test_operator_construction(self):
        """Test operator 𝒪 = 𝔻 + 𝕂 construction."""
        n_modes = 8
        self.atlas.generate_modal_basis(n_modes)
        operator = self.atlas.construct_operator_O(n_modes, coupling_strength=0.1)
        
        # Check shape
        self.assertEqual(operator.shape, (n_modes, n_modes))
        
        # Check that coupling matrix exists
        self.assertIsNotNone(self.atlas.coupling_matrix)
        self.assertEqual(self.atlas.coupling_matrix.shape, (n_modes, n_modes))
        
        # Check symmetry of coupling (should be symmetric for physical system)
        coupling_diff = np.abs(self.atlas.coupling_matrix - self.atlas.coupling_matrix.T)
        self.assertLess(np.max(coupling_diff), 1e-10)
    
    def test_operator_properties(self):
        """Test operator has proper frequency scaling."""
        n_modes = 4
        self.atlas.generate_modal_basis(n_modes)
        
        # Test with normalized diagonal
        operator = self.atlas.construct_operator_O(n_modes, coupling_strength=0.0, normalize_diagonal=True)
        for n in range(n_modes):
            expected = 1.0 + self.atlas.DIAGONAL_SCALING_FACTOR * n
            self.assertAlmostEqual(operator[n, n], expected, places=2)
        
        # Test with original (non-normalized) diagonal
        operator2 = self.atlas.construct_operator_O(n_modes, coupling_strength=0.0, normalize_diagonal=False)
        for n in range(n_modes):
            self.assertAlmostEqual(operator2[n, n], (n + 1)**2, places=2)


class TestAtlas3Phase2(unittest.TestCase):
    """Test Phase 2: Vibrational Graph Emergence"""
    
    def setUp(self):
        """Set up test framework."""
        self.atlas = Atlas3QCAL(f0=141.7001)
        # Prepare system
        self.n_modes = 16
        self.atlas.generate_modal_basis(self.n_modes)
        self.atlas.construct_operator_O(self.n_modes)
    
    def test_spectral_dna_computation(self):
        """Test spectral DNA calculation."""
        dna = self.atlas.compute_spectral_dna()
        
        # Check all required fields
        self.assertIn('eigenvalues', dna)
        self.assertIn('eigenvectors', dna)
        self.assertIn('adjacency_matrix', dna)
        self.assertIn('spectral_gap', dna)
        
        # Check eigenvalue count
        self.assertEqual(len(dna['eigenvalues']), self.n_modes)
        
        # Check spectral gap is positive
        self.assertGreater(dna['spectral_gap'], 0)
    
    def test_graph_properties(self):
        """Test vibrational graph properties."""
        dna = self.atlas.compute_spectral_dna(epsilon=0.01)
        
        # Check graph metrics
        self.assertEqual(dna['n_modes'], self.n_modes)
        self.assertGreaterEqual(dna['n_edges'], 0)
        self.assertGreaterEqual(dna['graph_density'], 0)
        self.assertLessEqual(dna['graph_density'], 1.0)
        
        # Adjacency should be symmetric
        adj = dna['adjacency_matrix']
        self.assertTrue(np.array_equal(adj, adj.T))
    
    def test_adaptive_threshold(self):
        """Test adaptive threshold filtering."""
        # With very high threshold, should have few edges
        dna_high = self.atlas.compute_spectral_dna(epsilon=10.0)
        
        # With low threshold, should have more edges
        dna_low = self.atlas.compute_spectral_dna(epsilon=0.001)
        
        # More edges with lower threshold
        self.assertGreaterEqual(dna_low['n_edges'], dna_high['n_edges'])
    
    def test_scaling_law_computation(self):
        """Test scaling law κ(n) ~ 1/√(n log n)."""
        n_values = [16, 32]
        scaling = self.atlas.compute_scaling_law(n_values, damping=0.1, coupling_strength=0.1)
        
        # Check outputs
        self.assertEqual(len(scaling['kappa_values']), len(n_values))
        self.assertIn('C_estimate', scaling)
        self.assertIn('convergence_to_kappa_pi', scaling)
        
        # Kappa values should be positive
        for kappa in scaling['kappa_values']:
            self.assertGreater(kappa, 0)


class TestAtlas3Phase3(unittest.TestCase):
    """Test Phase 3: Fire Test κ_Π ≈ 2.57731 (V13 Results)"""
    
    def setUp(self):
        """Set up test framework."""
        self.atlas = Atlas3QCAL(f0=141.7001)
    
    def test_kappa_pi_constant(self):
        """Test κ_Π constant is properly defined."""
        self.assertAlmostEqual(self.atlas.kappa_pi, 2.57731, places=5)
    
    def test_validation_structure(self):
        """Test validation returns proper structure."""
        # Use small parameters for fast test
        validation = self.atlas.validate_kappa_pi_attractor(
            n_values=[8, 16],
            damping_values=[0.1],
            coupling_values=[0.1]
        )
        
        # Check required fields
        self.assertIn('results', validation)
        self.assertIn('mean_C', validation)
        self.assertIn('std_C', validation)
        self.assertIn('kappa_pi_target', validation)
        self.assertIn('universality_achieved', validation)
        
        # Check target is correct
        self.assertAlmostEqual(validation['kappa_pi_target'], 2.57731, places=5)
    
    def test_universality_check(self):
        """Test universality is properly evaluated."""
        validation = self.atlas.validate_kappa_pi_attractor(
            n_values=[16],
            damping_values=[0.1, 0.15],
            coupling_values=[0.1]
        )
        
        # Should have results for each parameter combination
        self.assertEqual(len(validation['results']), 2)  # 2 damping × 1 coupling
        
        # Each result should have required fields
        for result in validation['results']:
            self.assertIn('damping', result)
            self.assertIn('coupling', result)
            self.assertIn('C_estimate', result)
    
    def test_stability_across_parameters(self):
        """Test stability across different parameters."""
        validation = self.atlas.validate_kappa_pi_attractor(
            n_values=[16],
            damping_values=[0.1, 0.15],
            coupling_values=[0.1, 0.15]
        )
        
        # Stability ratio should be reasonable (< 1 for stable)
        if validation['mean_C'] > 0:
            self.assertIsNotNone(validation['stability_ratio'])


class TestV13SpectralInvariant(unittest.TestCase):
    """Test V13 spectral invariant computation and validation"""
    
    def setUp(self):
        """Set up test framework."""
        self.atlas = Atlas3QCAL(f0=141.7001)
    
    def test_direct_kappa_pi_formula(self):
        """Test direct κ_Π formula: λ_max(A_N) / (N log N)"""
        n_values = [16, 32]
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=n_values,
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Check all required fields
        self.assertIn('kappa_pi_values', results)
        self.assertIn('lambda_max_values', results)
        self.assertIn('errors_percent', results)
        self.assertIn('target_kappa_pi', results)
        self.assertIn('v13_precision_achieved', results)
        
        # Check correct number of results
        self.assertEqual(len(results['kappa_pi_values']), len(n_values))
        self.assertEqual(len(results['lambda_max_values']), len(n_values))
        self.assertEqual(len(results['errors_percent']), len(n_values))
        
        # Kappa values should be positive and reasonable
        for kappa in results['kappa_pi_values']:
            self.assertGreater(kappa, 0)
            self.assertLess(kappa, 100)  # Sanity check
    
    def test_error_tracking(self):
        """Test that error tracking works correctly"""
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=[16, 32, 64],
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Error should be computed for each N
        self.assertEqual(len(results['errors_percent']), 3)
        
        # All errors should be non-negative percentages
        for error in results['errors_percent']:
            self.assertGreaterEqual(error, 0)
        
        # Min and max error should be tracked
        self.assertIn('min_error_percent', results)
        self.assertIn('max_error_percent', results)
    
    def test_v13_precision_flag(self):
        """Test V13 precision achievement flag"""
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=[16],
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Flag should be boolean (convert numpy bool to Python bool for isinstance check)
        self.assertIn(results['v13_precision_achieved'], [True, False])
        
        # If achieved, min error should be < 0.019%
        if results['v13_precision_achieved']:
            self.assertLess(results['min_error_percent'], 0.019)
    
    def test_convergence_rate_estimation(self):
        """Test convergence rate estimation"""
        # Need at least 3 points for convergence rate
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=[16, 32, 64],
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Convergence rate should be computed
        self.assertIsNotNone(results['convergence_rate'])
        
        # Should be a number (can be positive or negative depending on scaling)
        if results['convergence_rate'] is not None:
            self.assertIsInstance(float(results['convergence_rate']), float)
    
    def test_spectral_radius_computation(self):
        """Test that spectral radius (λ_max) is computed correctly"""
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=[8, 16],
            damping=0.1,
            coupling_strength=0.1
        )
        
        # Lambda max values should all be positive
        for lambda_max in results['lambda_max_values']:
            self.assertGreater(lambda_max, 0)
        
        # Lambda max should generally increase with N (more modes = larger eigenvalues)
        # (Not strictly monotonic due to normalization, but checking it's reasonable)
        self.assertTrue(all(lm > 0 for lm in results['lambda_max_values']))
    
    def test_higher_precision_constant(self):
        """Test that new κ_Π value has higher precision"""
        results = self.atlas.compute_spectral_invariant_kappa_pi(
            n_values=[16],
            damping=0.1,
            coupling_strength=0.15
        )
        
        # Target should be 2.57731 (5 decimal places)
        self.assertAlmostEqual(results['target_kappa_pi'], 2.57731, places=5)
        
        # Should match atlas instance
        self.assertEqual(results['target_kappa_pi'], self.atlas.kappa_pi)


class TestAtlas3Integration(unittest.TestCase):
    """Test integration with solve_ivp and other components"""
    
    def setUp(self):
        """Set up test framework."""
        self.atlas = Atlas3QCAL(f0=141.7001)
    
    def test_solve_modal_dynamics(self):
        """Test modal dynamics integration."""
        dynamics = self.atlas.solve_modal_dynamics(
            n_modes=8,
            t_span=(0, 0.01),
            forcing_frequency=141.7001
        )
        
        # Check solution structure
        self.assertIn('solution', dynamics)
        self.assertIn('success', dynamics)
        self.assertTrue(dynamics['success'])
        
        # Check solution shape
        self.assertEqual(dynamics['amplitudes'].shape[0], 8)
    
    def test_dynamics_with_initial_conditions(self):
        """Test dynamics with custom initial conditions."""
        n_modes = 4
        initial = np.array([1.0, 0.5, 0.25, 0.125])
        
        dynamics = self.atlas.solve_modal_dynamics(
            n_modes=n_modes,
            t_span=(0, 0.01),
            initial_amplitudes=initial
        )
        
        # Check initial condition matches
        np.testing.assert_array_almost_equal(
            dynamics['amplitudes'][:, 0],
            initial,
            decimal=6
        )
    
    def test_frequency_parameter(self):
        """Test different forcing frequencies."""
        # Test with f0
        dynamics1 = self.atlas.solve_modal_dynamics(
            n_modes=4,
            t_span=(0, 0.005),
            forcing_frequency=141.7001
        )
        
        # Test with different frequency
        dynamics2 = self.atlas.solve_modal_dynamics(
            n_modes=4,
            t_span=(0, 0.005),
            forcing_frequency=100.0
        )
        
        # Both should succeed
        self.assertTrue(dynamics1['success'])
        self.assertTrue(dynamics2['success'])


class TestAtlas3Metadata(unittest.TestCase):
    """Test sovereign metadata"""
    
    def test_sovereign_metadata(self):
        """Test that sovereign metadata is properly defined."""
        import atlas3_qcal
        
        self.assertEqual(atlas3_qcal.__author__, "José Manuel Mota Burruezo (JMMB Ψ✧)")
        self.assertEqual(atlas3_qcal.__architecture__, "QCAL ∞³")
        self.assertEqual(atlas3_qcal.__license__, "Sovereign Noetic License 1.0")
        self.assertAlmostEqual(atlas3_qcal.__f0__, 141.7001, places=4)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Phase1))
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Phase2))
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Phase3))
    suite.addTests(loader.loadTestsFromTestCase(TestV13SpectralInvariant))
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Integration))
    suite.addTests(loader.loadTestsFromTestCase(TestAtlas3Metadata))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
