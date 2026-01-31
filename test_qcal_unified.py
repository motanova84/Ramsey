#!/usr/bin/env python3
"""
Tests for QCAL Unified Framework
=================================

Unit tests for the unified framework components.
"""

import sys
import unittest
from qcal_unified_framework import QCALUnifiedFramework, CrossVerificationProtocol


class TestQCALUnifiedFramework(unittest.TestCase):
    """Test cases for QCAL unified framework."""
    
    def setUp(self):
        """Set up test framework."""
        self.framework = QCALUnifiedFramework()
        self.protocol = CrossVerificationProtocol()
    
    def test_constants_exist(self):
        """Test that all universal constants are defined."""
        required_constants = [
            'kappa_pi', 'f0', 'critical_line',
            'ramsey_ratio', 'navier_stokes_epsilon', 'bsd_delta'
        ]
        for const in required_constants:
            self.assertIn(const, self.framework.constants)
            self.assertIsNotNone(self.framework.constants[const])
    
    def test_constant_values(self):
        """Test that constants have expected values."""
        self.assertAlmostEqual(self.framework.constants['kappa_pi'], 2.5773, places=4)
        self.assertAlmostEqual(self.framework.constants['f0'], 141.7001, places=4)
        self.assertAlmostEqual(self.framework.constants['critical_line'], 0.5, places=10)
        self.assertAlmostEqual(self.framework.constants['ramsey_ratio'], 43/108, places=10)
        self.assertAlmostEqual(self.framework.constants['bsd_delta'], 1.0, places=10)
    
    def test_operators_exist(self):
        """Test that all operators are defined."""
        required_operators = [
            'p_vs_np', 'riemann', 'bsd', 'navier_stokes', 'ramsey'
        ]
        for op in required_operators:
            self.assertIn(op, self.framework.operators)
            self.assertTrue(callable(self.framework.operators[op]))
    
    def test_p_vs_np_operator(self):
        """Test P vs NP operator."""
        result = self.framework.D_PNP_operator({'treewidth': 10})
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_riemann_operator(self):
        """Test Riemann Hypothesis operator."""
        result = self.framework.H_Psi_operator({})
        self.assertIsInstance(result, complex)
        self.assertAlmostEqual(result.real, 0.5, places=10)
    
    def test_bsd_operator(self):
        """Test BSD operator."""
        result = self.framework.L_E_operator({'s': 1.0})
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_navier_stokes_operator(self):
        """Test Navier-Stokes operator."""
        result = self.framework.NS_operator({'viscosity': 1.0, 'wavenumber': 1.0})
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_ramsey_operator(self):
        """Test Ramsey operator."""
        # Test known values
        result_33 = self.framework.R_operator({'r': 3, 's': 3})
        self.assertIsInstance(result_33, int)
        self.assertGreaterEqual(result_33, 3)  # R(3,3) >= 3
        
        result_55 = self.framework.R_operator({'r': 5, 's': 5})
        self.assertIsInstance(result_55, int)
        self.assertGreaterEqual(result_55, 5)  # R(5,5) >= 5
    
    def test_constant_coherence(self):
        """Test constant coherence verification."""
        coherence = self.framework.verify_constant_coherence()
        
        # All tests should pass
        self.assertTrue(coherence['critical_line_bsd'])
        self.assertTrue(coherence['f0_positive'])
        self.assertTrue(coherence['kappa_pi_range'])
        self.assertTrue(coherence['ramsey_ratio_rational'])
        self.assertTrue(coherence['euler_mascheroni'])
    
    def test_demonstrate_unification(self):
        """Test unification demonstration."""
        results = self.framework.demonstrate_unification()
        
        # Should have results for all problems
        self.assertGreater(len(results), 0)
        
        # Each result should have expected keys
        for problem, data in results.items():
            if 'error' not in data:
                self.assertIn('eigenvalue', data)
                self.assertIn('connected_via', data)
                self.assertIn('verification_status', data)
    
    def test_find_connections(self):
        """Test problem connection finding."""
        connections = self.framework._find_connections('ramsey')
        self.assertIsInstance(connections, list)
        self.assertGreater(len(connections), 0)
    
    def test_verify_problem(self):
        """Test problem verification."""
        status = self.framework._verify_problem('ramsey')
        self.assertIsInstance(status, str)
        self.assertGreater(len(status), 0)
    
    def test_unified_equation(self):
        """Test unified equation generation."""
        equation = self.framework.get_unified_equation()
        self.assertIsInstance(equation, str)
        self.assertIn('f₀', equation)
        self.assertIn('141.7001', equation)
    
    def test_summary_table(self):
        """Test summary table generation."""
        table = self.framework.generate_summary_table()
        self.assertIsInstance(table, str)
        self.assertIn('QCAL', table)
        self.assertIn('P vs NP', table)
        self.assertIn('Riemann', table)


class TestCrossVerificationProtocol(unittest.TestCase):
    """Test cases for cross-verification protocol."""
    
    def setUp(self):
        """Set up test protocol."""
        self.protocol = CrossVerificationProtocol()
    
    def test_verification_methods_exist(self):
        """Test that verification methods exist."""
        required_methods = [
            'verify_p_vs_np', 'verify_riemann', 'verify_bsd',
            'verify_navier_stokes', 'verify_ramsey'
        ]
        for method in required_methods:
            self.assertTrue(hasattr(self.protocol, method))
    
    def test_verify_ramsey(self):
        """Test Ramsey verification."""
        result = self.protocol.verify_ramsey()
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('verified', result)
        # Ramsey should be verified
        self.assertTrue(result['verified'])
    
    def test_run_cross_verification(self):
        """Test complete cross-verification."""
        results = self.protocol.run_cross_verification()
        
        # Check structure
        self.assertIn('individual_results', results)
        self.assertIn('consistency_matrix', results)
        self.assertIn('qcal_coherence', results)
        self.assertIn('unified_status', results)
        
        # Consistency matrix should be present
        self.assertIsNotNone(results['consistency_matrix'])
        
        # QCAL coherence should pass
        self.assertIsInstance(results['qcal_coherence'], dict)
        self.assertTrue(results['qcal_coherence']['constants_coherent'])
    
    def test_consistency_matrix(self):
        """Test consistency matrix building."""
        results = self.protocol.run_cross_verification()
        matrix = results['consistency_matrix']
        
        # Should be square
        self.assertEqual(matrix.shape[0], matrix.shape[1])
        
        # Diagonal should be ones
        import numpy as np
        self.assertTrue(np.allclose(np.diag(matrix), 1.0))
        
        # Should be symmetric
        self.assertTrue(np.allclose(matrix, matrix.T))


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQCALUnifiedFramework))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossVerificationProtocol))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
