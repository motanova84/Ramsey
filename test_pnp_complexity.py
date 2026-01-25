#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for P-NP Complexity Framework

Tests cover:
- Calabi-Yau manifold properties
- κ_Π constant calculation
- Treewidth estimation
- Complexity classification
- Ramsey complexity analysis

Author: QCAL ∞³ Framework
Date: 2026-01-14
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pnp_complexity import (
    CalabiYauManifold,
    TreewidthAnalyzer,
    ComplexityMetrics,
    analyze_ramsey_complexity,
    is_problem_tractable,
    get_kappa_pi_exact,
    get_kappa_pi_quantum_corrected,
    KAPPA_PI,
    KAPPA_PI_QUANTUM,
    RESONANCE_CY
)


class TestCalabiYauManifold(unittest.TestCase):
    """Test Calabi-Yau manifold calculations"""
    
    def test_resonance_manifold(self):
        """Test resonance manifold with N=13"""
        self.assertEqual(RESONANCE_CY.h11, 8)
        self.assertEqual(RESONANCE_CY.h21, 5)
        self.assertEqual(RESONANCE_CY.total_moduli, 13)
        
    def test_euler_characteristic(self):
        """Test Euler characteristic calculation"""
        cy = CalabiYauManifold(h11=8, h21=5)
        # χ = 2(h^{1,1} - h^{2,1}) = 2(8-5) = 6
        self.assertEqual(cy.euler_characteristic, 6)
        
    def test_kappa_pi_calculation(self):
        """Test κ_Π = ln(h^{1,1} + h^{2,1})"""
        cy = CalabiYauManifold(h11=8, h21=5)
        expected = np.log(13)
        self.assertAlmostEqual(cy.kappa_pi, expected, places=6)
        
    def test_quintic_manifold(self):
        """Test quintic threefold (classic example)"""
        quintic = CalabiYauManifold(h11=1, h21=101)
        self.assertEqual(quintic.total_moduli, 102)
        self.assertEqual(quintic.euler_characteristic, -200)


class TestKappaPi(unittest.TestCase):
    """Test κ_Π constant"""
    
    def test_exact_value(self):
        """Test exact κ_Π = ln(13)"""
        expected = np.log(13)
        self.assertAlmostEqual(get_kappa_pi_exact(), expected, places=6)
        self.assertAlmostEqual(KAPPA_PI, expected, places=6)
        
    def test_quantum_correction(self):
        """Test quantum-corrected κ_Π"""
        kappa_quantum = get_kappa_pi_quantum_corrected()
        # Should be slightly larger than exact value
        self.assertGreater(kappa_quantum, KAPPA_PI)
        # Should be close to 2.5773
        self.assertAlmostEqual(kappa_quantum, 2.5773, places=2)


class TestTreewidthAnalyzer(unittest.TestCase):
    """Test treewidth analysis"""
    
    def test_path_graph(self):
        """Test path graph has treewidth 1"""
        # Path: 0-1-2-3
        path = np.array([
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]
        ])
        
        analyzer = TreewidthAnalyzer(path)
        tw = analyzer.estimate_treewidth_greedy()
        self.assertEqual(tw, 1)
        
    def test_complete_graph(self):
        """Test complete graph K_n has treewidth n-1"""
        # K4
        k4 = np.ones((4, 4)) - np.eye(4)
        
        analyzer = TreewidthAnalyzer(k4)
        tw = analyzer.estimate_treewidth_greedy()
        self.assertEqual(tw, 3)  # n-1 = 4-1 = 3
        
    def test_cycle_graph(self):
        """Test cycle graph"""
        # Cycle: 0-1-2-3-0
        cycle = np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ])
        
        analyzer = TreewidthAnalyzer(cycle)
        tw = analyzer.estimate_treewidth_greedy()
        self.assertEqual(tw, 2)
        
    def test_complexity_classification(self):
        """Test P vs NP classification"""
        # Small graph (should be P)
        small_graph = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ])
        
        analyzer = TreewidthAnalyzer(small_graph)
        complexity = analyzer.complexity_class()
        self.assertEqual(complexity, "P")
        
    def test_spectral_curvature(self):
        """Test spectral curvature calculation"""
        graph = np.array([
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]
        ])
        
        analyzer = TreewidthAnalyzer(graph)
        curvature = analyzer.spectral_curvature()
        
        # Curvature should be positive
        self.assertGreater(curvature, 0)


class TestComplexityMetrics(unittest.TestCase):
    """Test complexity metrics"""
    
    def test_noetic_curvature(self):
        """Test noetic curvature calculation"""
        graph = np.array([
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]
        ])
        
        curvature = ComplexityMetrics.noetic_curvature(graph)
        
        # Should be non-negative
        self.assertGreaterEqual(curvature, 0)
        
    def test_information_resistance(self):
        """Test information resistance calculation"""
        f0 = 141.7001
        
        # Same frequency -> zero resistance
        r1 = ComplexityMetrics.information_resistance(0.0, 0.0, f0)
        self.assertEqual(r1, 0.0)
        
        # Opposite frequencies -> maximum resistance
        r2 = ComplexityMetrics.information_resistance(0.0, f0/2, f0)
        
        # Adjacent frequencies -> small resistance
        r3 = ComplexityMetrics.information_resistance(0.0, 1.0, f0)
        
        self.assertGreater(r2, r3)
        
    def test_effective_growth_rate(self):
        """Test effective growth rate"""
        rate_10 = ComplexityMetrics.effective_growth_rate(10)
        rate_100 = ComplexityMetrics.effective_growth_rate(100)
        
        # Should increase with problem size
        self.assertGreater(rate_100, rate_10)


class TestRamseyComplexity(unittest.TestCase):
    """Test Ramsey number complexity analysis"""
    
    def test_ramsey_3_3(self):
        """Test R(3,3) analysis"""
        result = analyze_ramsey_complexity(3, 3)
        
        self.assertEqual(result['r'], 3)
        self.assertEqual(result['s'], 3)
        self.assertIn('classical_bound', result)
        self.assertIn('vibrational_bound', result)
        self.assertIn('treewidth', result)
        self.assertIn('complexity_class', result)
        
    def test_ramsey_5_5(self):
        """Test R(5,5) analysis"""
        result = analyze_ramsey_complexity(5, 5)
        
        self.assertEqual(result['r'], 5)
        self.assertEqual(result['s'], 5)
        
        # Vibrational bound should be much smaller than classical
        self.assertLess(result['vibrational_bound'], result['classical_bound'])
        
        # Should have significant reduction factor
        self.assertGreater(result['reduction_factor'], 1.0)
        
    def test_kappa_pi_in_results(self):
        """Test that κ_Π is included in results"""
        result = analyze_ramsey_complexity(4, 4)
        
        self.assertIn('kappa_pi', result)
        self.assertAlmostEqual(result['kappa_pi'], KAPPA_PI_QUANTUM, places=4)


class TestTractability(unittest.TestCase):
    """Test problem tractability classification"""
    
    def test_small_tractable_graph(self):
        """Test small graph is tractable"""
        small_graph = np.array([
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
        ])
        
        self.assertTrue(is_problem_tractable(small_graph))
        
    def test_path_is_tractable(self):
        """Test path graph is tractable"""
        path = np.zeros((10, 10))
        for i in range(9):
            path[i, i+1] = path[i+1, i] = 1
        
        self.assertTrue(is_problem_tractable(path))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_empty_graph(self):
        """Test empty graph"""
        empty = np.array([[]])
        
        # Should handle gracefully
        curvature = ComplexityMetrics.noetic_curvature(empty)
        self.assertEqual(curvature, 0.0)
        
    def test_single_vertex(self):
        """Test single vertex graph"""
        single = np.array([[0]])
        
        analyzer = TreewidthAnalyzer(single)
        tw = analyzer.estimate_treewidth_greedy()
        
        # Single vertex has treewidth 0
        self.assertEqual(tw, 0)


def run_tests():
    """Run all tests"""
    print("=" * 80)
    print(" " * 20 + "P-NP COMPLEXITY FRAMEWORK TESTS")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCalabiYauManifold))
    suite.addTests(loader.loadTestsFromTestCase(TestKappaPi))
    suite.addTests(loader.loadTestsFromTestCase(TestTreewidthAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexityMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestRamseyComplexity))
    suite.addTests(loader.loadTestsFromTestCase(TestTractability))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("✅ ALL TESTS PASSED")
    else:
        print()
        print("❌ SOME TESTS FAILED")
    
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
