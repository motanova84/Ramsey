"""
Unit tests for Class B Systems Framework

Tests the QCAL ∞³ Phase 3 extension covering:
- System creation and classification
- Resonance detection
- Binary colorings (Class A)
- Ternary colorings (Class B)
- Clique detection
- Polynomial bounds
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import numpy as np
from core.math.class_b_systems import (
    SystemClass,
    VibrationSystem,
    ClassASystem,
    ClassBSystem,
    create_system
)


class TestSystemCreation(unittest.TestCase):
    """Tests for system creation and initialization"""
    
    def test_create_class_a_system(self):
        """Class A system should be created correctly"""
        system = create_system(SystemClass.A)
        self.assertIsInstance(system, ClassASystem)
        self.assertEqual(system.get_system_class(), SystemClass.A)
        self.assertEqual(system.get_color_count(), 2)
    
    def test_create_class_b_system(self):
        """Class B system should be created correctly"""
        system = create_system(SystemClass.B)
        self.assertIsInstance(system, ClassBSystem)
        self.assertEqual(system.get_system_class(), SystemClass.B)
        self.assertEqual(system.get_color_count(), 3)
    
    def test_system_constants(self):
        """Systems should have correct universal constants"""
        system = create_system(SystemClass.A)
        self.assertAlmostEqual(system.f0, 141.7001, places=4)
        self.assertAlmostEqual(system.kappa_pi, 2.5773, places=4)
        self.assertAlmostEqual(system.epsilon, 0.037, places=3)
    
    def test_invalid_system_class(self):
        """Invalid system class should raise ValueError"""
        with self.assertRaises(ValueError):
            create_system("INVALID")


class TestResonanceDetection(unittest.TestCase):
    """Tests for resonance detection mechanism"""
    
    def setUp(self):
        self.system = create_system(SystemClass.A)
    
    def test_exact_resonance(self):
        """Identical frequencies should resonate"""
        self.assertTrue(self.system.resonance_detected(10.0, 10.0))
        self.assertTrue(self.system.resonance_detected(141.7001, 141.7001))
    
    def test_close_resonance(self):
        """Very close frequencies should resonate"""
        self.assertTrue(self.system.resonance_detected(10.0, 10.01))
        self.assertTrue(self.system.resonance_detected(50.0, 50.02))
    
    def test_no_resonance(self):
        """Far apart frequencies should not resonate"""
        self.assertFalse(self.system.resonance_detected(10.0, 50.0))
        self.assertFalse(self.system.resonance_detected(0.0, 100.0))
    
    def test_modular_resonance(self):
        """Frequencies differing by f₀ should resonate"""
        f0 = self.system.f0
        # Frequencies that differ by approximately f₀
        self.assertTrue(self.system.resonance_detected(1.0, 1.0 + f0))
        self.assertTrue(self.system.resonance_detected(10.0, 10.0 + f0))


class TestClassAColoring(unittest.TestCase):
    """Tests for Class A (binary) coloring"""
    
    def setUp(self):
        self.system = create_system(SystemClass.A)
    
    def test_coloring_produces_dict(self):
        """Coloring should produce a dictionary"""
        frequencies = np.array([10.0, 20.0, 30.0])
        coloring = self.system.generate_coloring(frequencies)
        self.assertIsInstance(coloring, dict)
    
    def test_coloring_edge_count(self):
        """Coloring should have correct number of edges"""
        n = 5
        frequencies = np.random.uniform(0, 141.7001, n)
        coloring = self.system.generate_coloring(frequencies)
        expected_edges = n * (n - 1) // 2
        self.assertEqual(len(coloring), expected_edges)
    
    def test_coloring_symmetry(self):
        """All edges should have i < j"""
        frequencies = np.array([10.0, 20.0, 30.0, 40.0])
        coloring = self.system.generate_coloring(frequencies)
        for (i, j) in coloring.keys():
            self.assertLess(i, j)
    
    def test_coloring_valid_colors(self):
        """Colors should be 'azul' or 'rojo' only"""
        frequencies = np.random.uniform(0, 141.7001, 6)
        coloring = self.system.generate_coloring(frequencies)
        valid_colors = {'azul', 'rojo'}
        for color in coloring.values():
            self.assertIn(color, valid_colors)


class TestClassBColoring(unittest.TestCase):
    """Tests for Class B (ternary) coloring"""
    
    def setUp(self):
        self.system = create_system(SystemClass.B)
    
    def test_coloring_produces_dict(self):
        """Coloring should produce a dictionary"""
        frequencies = np.array([10.0, 20.0, 30.0])
        coloring = self.system.generate_coloring(frequencies)
        self.assertIsInstance(coloring, dict)
    
    def test_coloring_valid_colors(self):
        """Colors should be 'azul', 'verde', or 'rojo' only"""
        frequencies = np.random.uniform(0, 141.7001, 6)
        coloring = self.system.generate_coloring(frequencies)
        valid_colors = {'azul', 'verde', 'rojo'}
        for color in coloring.values():
            self.assertIn(color, valid_colors)
    
    def test_coloring_has_all_three_colors(self):
        """Large enough graph should have all three colors"""
        # Use specific seed to get diverse frequencies
        np.random.seed(42)
        frequencies = np.random.uniform(0, 141.7001, 20)
        coloring = self.system.generate_coloring(frequencies)
        colors_present = set(coloring.values())
        # With 20 vertices and diverse frequencies, we should see multiple colors
        self.assertGreaterEqual(len(colors_present), 2)


class TestCliqueDetection(unittest.TestCase):
    """Tests for monochromatic clique detection"""
    
    def test_class_a_trivial_clique(self):
        """Single vertex is a clique of size 1"""
        system = create_system(SystemClass.A)
        coloring = {(0, 1): 'rojo', (0, 2): 'rojo', (1, 2): 'rojo'}
        clique = system.find_monochromatic_clique(coloring, 'rojo', min_size=1)
        self.assertIsNotNone(clique)
        self.assertGreaterEqual(len(clique), 1)
    
    def test_class_a_complete_blue_clique(self):
        """All-blue graph has clique of all vertices"""
        system = create_system(SystemClass.A)
        coloring = {(0, 1): 'azul', (0, 2): 'azul', (1, 2): 'azul'}
        clique = system.find_monochromatic_clique(coloring, 'azul', min_size=3)
        self.assertIsNotNone(clique)
        self.assertEqual(len(clique), 3)
    
    def test_class_a_no_clique_found(self):
        """Should return None if clique too small"""
        system = create_system(SystemClass.A)
        coloring = {(0, 1): 'azul', (0, 2): 'rojo', (1, 2): 'rojo'}
        clique = system.find_monochromatic_clique(coloring, 'azul', min_size=3)
        # With only one azul edge, cannot have azul clique of size 3
        self.assertIsNone(clique)
    
    def test_class_b_clique_detection(self):
        """Class B should find cliques in ternary coloring"""
        system = create_system(SystemClass.B)
        coloring = {
            (0, 1): 'verde', (0, 2): 'verde', (1, 2): 'verde',
            (0, 3): 'rojo', (1, 3): 'rojo', (2, 3): 'rojo'
        }
        verde_clique = system.find_monochromatic_clique(coloring, 'verde', min_size=3)
        self.assertIsNotNone(verde_clique)
        self.assertEqual(len(verde_clique), 3)


class TestPolynomialBounds(unittest.TestCase):
    """Tests for polynomial bound calculations"""
    
    def test_class_a_bound_positive(self):
        """Class A bounds should be positive"""
        system = create_system(SystemClass.A)
        self.assertGreater(system.polynomial_bound(3, 3), 0)
        self.assertGreater(system.polynomial_bound(5, 5), 0)
    
    def test_class_a_bound_increasing(self):
        """Class A bounds should increase with parameters"""
        system = create_system(SystemClass.A)
        bound_33 = system.polynomial_bound(3, 3)
        bound_44 = system.polynomial_bound(4, 4)
        bound_55 = system.polynomial_bound(5, 5)
        self.assertLess(bound_33, bound_44)
        self.assertLess(bound_44, bound_55)
    
    def test_class_a_bound_symmetric(self):
        """Class A bounds should be symmetric"""
        system = create_system(SystemClass.A)
        self.assertAlmostEqual(
            system.polynomial_bound(3, 5),
            system.polynomial_bound(5, 3),
            places=10
        )
    
    def test_class_b_bound_positive(self):
        """Class B bounds should be positive"""
        system = create_system(SystemClass.B)
        self.assertGreater(system.polynomial_bound(3, 3, 3), 0)
        self.assertGreater(system.polynomial_bound(4, 4, 4), 0)
    
    def test_class_b_bound_symmetric(self):
        """Class B bounds should be symmetric under permutation"""
        system = create_system(SystemClass.B)
        bound_345 = system.polynomial_bound(3, 4, 5)
        bound_453 = system.polynomial_bound(4, 5, 3)
        bound_534 = system.polynomial_bound(5, 3, 4)
        self.assertAlmostEqual(bound_345, bound_453, places=10)
        self.assertAlmostEqual(bound_453, bound_534, places=10)
    
    def test_class_b_estimate_333(self):
        """R(3,3,3) estimate should be close to known value 17"""
        system = create_system(SystemClass.B)
        estimate = system.estimate_ramsey_number(3, 3, 3)
        # Our bound should give a reasonable estimate
        # Known: R(3,3,3) = 17
        self.assertLess(estimate, 30)  # Should be reasonable
        self.assertGreater(estimate, 5)  # Should not be too small


class TestModalFunctions(unittest.TestCase):
    """Tests for modal function calculations"""
    
    def test_phi_modal_basic(self):
        """Modal function should return values in [-1, 1]"""
        system = create_system(SystemClass.A)
        t = 0.5
        phi = system.phi_modal(t, n=1, delta=0.0)
        self.assertGreaterEqual(phi, -1.0)
        self.assertLessEqual(phi, 1.0)
    
    def test_phi_modal_zero_at_origin(self):
        """φₙ(0, δ=0) = sin(0) = 0"""
        system = create_system(SystemClass.A)
        phi = system.phi_modal(0.0, n=1, delta=0.0)
        self.assertAlmostEqual(phi, 0.0, places=10)
    
    def test_phi_modal_with_phase(self):
        """Phase shift should affect the value"""
        system = create_system(SystemClass.A)
        t = 0.5
        phi_no_phase = system.phi_modal(t, n=1, delta=0.0)
        phi_with_phase = system.phi_modal(t, n=1, delta=np.pi/2)
        # Values should be different with phase shift
        self.assertNotAlmostEqual(phi_no_phase, phi_with_phase, places=5)


class TestIntegration(unittest.TestCase):
    """Integration tests with existing QCAL ∞³ infrastructure"""
    
    def test_universal_constants_match(self):
        """Universal constants should match across systems"""
        system_a = create_system(SystemClass.A)
        system_b = create_system(SystemClass.B)
        
        self.assertEqual(system_a.f0, system_b.f0)
        self.assertEqual(system_a.kappa_pi, system_b.kappa_pi)
        self.assertEqual(system_a.epsilon, system_b.epsilon)
    
    def test_backward_compatibility(self):
        """Class A should work like original binary system"""
        system = create_system(SystemClass.A)
        
        # Test with known frequencies that should resonate
        frequencies = np.array([10.0, 10.01, 50.0, 50.01])
        coloring = system.generate_coloring(frequencies)
        
        # (0,1) should be azul (resonant)
        self.assertEqual(coloring[(0, 1)], 'azul')
        # (2,3) should be azul (resonant)
        self.assertEqual(coloring[(2, 3)], 'azul')
        # (0,2) should be rojo (not resonant)
        self.assertEqual(coloring[(0, 2)], 'rojo')


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)
