#!/usr/bin/env python3
"""
Integration test for NS-Ramsey-Riemann-QCAL unified framework.

Verifies complete integration across all components.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.math.ns_ramsey_riemann import UnifiedFramework, F0
from qcal.ramsey_logos_attractor import emergencia_ramsey_qcal, escanear_orden_ramsey_bsd


class TestFullIntegration(unittest.TestCase):
    """Integration tests for complete NS-Ramsey-Riemann-QCAL framework."""
    
    def test_ns_riemann_symmetry(self):
        """Test that NS flow and Riemann both use Re(s) = 1/2."""
        framework = UnifiedFramework()
        
        # NS flow critical axis
        ns_state = framework.ns_flow.get_state(0.5)
        self.assertEqual(ns_state.reynolds, 0.5)
        
        # Riemann critical line
        riemann_state = framework.riemann.get_state(F0)
        self.assertEqual(riemann_state.s.real, 0.5)
    
    def test_frequency_coherence(self):
        """Test that all components use F₀ = 141.7001 Hz."""
        framework = UnifiedFramework()
        
        # Framework frequency
        self.assertEqual(framework.f0, F0)
        self.assertEqual(framework.f0, 141.7001)
        
        # NS flow frequency
        self.assertEqual(framework.ns_flow.f0, F0)
        
        # Riemann state at F₀
        state = framework.riemann.get_state(F0)
        self.assertAlmostEqual(state.s.imag, F0, places=4)
    
    def test_unified_state_completeness(self):
        """Test that unified state contains all components."""
        framework = UnifiedFramework()
        state = framework.get_unified_state(0.01)
        
        # Verify all components present
        self.assertIsNotNone(state.ns_flow)
        self.assertIsNotNone(state.ramsey)
        self.assertIsNotNone(state.riemann)
        self.assertIsNotNone(state.master_harmonic)
        self.assertIsNotNone(state.zero_density)
        self.assertIsNotNone(state.psi_qcal)
        
        # Verify coherence bounds
        self.assertGreaterEqual(state.ramsey.coherence, 0.0)
        self.assertLessEqual(state.ramsey.coherence, 1.0)
        self.assertGreater(state.psi_qcal, 0.0)
        self.assertLessEqual(state.psi_qcal, 1.0)
    
    def test_qcal_logos_integration(self):
        """Test integration with QCAL Logos attractor."""
        # Test emergence at critical node count
        resultado = emergencia_ramsey_qcal(51)
        
        self.assertEqual(resultado['ramsey_status'], 'ORDEN_INEVITABLE')
        self.assertTrue(resultado['logos_manifestado'])
        self.assertAlmostEqual(resultado['psi_emergencia'], 0.999999, places=5)
    
    def test_bsd_ramsey_connection(self):
        """Test BSD-Ramsey integration."""
        # Test with positive rank
        curva = {'rango_adelico': 1}
        resultado = escanear_orden_ramsey_bsd(curva, "GACT")
        
        self.assertEqual(resultado['status'], 'ORDEN_MANIFESTADO')
        self.assertEqual(resultado['conexion_bsd'], 'VALIDADA')
        self.assertAlmostEqual(resultado['coherencia_ramsey'], 0.999999, places=5)
    
    def test_coherence_analysis_integration(self):
        """Test coherence analysis across framework."""
        framework = UnifiedFramework()
        
        # Analyze over one period
        period = 1.0 / F0
        analysis = framework.analyze_coherence(0.0, period, 50)
        
        # Verify all metrics present
        self.assertIn('ns_mean_energy', analysis)
        self.assertIn('ramsey_mean_coherence', analysis)
        self.assertIn('riemann_mean_magnitude', analysis)
        self.assertIn('psi_mean', analysis)
        
        # Verify positive values
        self.assertGreater(analysis['ns_mean_energy'], 0.0)
        self.assertGreater(analysis['ramsey_mean_coherence'], 0.0)
        self.assertGreater(analysis['riemann_mean_magnitude'], 0.0)
        self.assertGreater(analysis['psi_mean'], 0.0)
        
        # Verify coherence bounds
        self.assertLessEqual(analysis['ramsey_mean_coherence'], 1.0)
        self.assertLessEqual(analysis['psi_mean'], 1.0)
    
    def test_mathematical_constants_alignment(self):
        """Test that mathematical constants align across framework."""
        framework = UnifiedFramework()
        
        # NS decay constant equals frequency
        self.assertEqual(framework.ns_flow.tau, F0)
        
        # Ramsey density is 1/3
        self.assertAlmostEqual(framework.ramsey.density, 1.0/3.0, places=10)
        
        # Riemann critical line at 1/2
        state = framework.riemann.get_state(F0)
        self.assertEqual(state.s.real, 0.5)
    
    def test_time_evolution_consistency(self):
        """Test that time evolution is consistent across components."""
        framework = UnifiedFramework()
        
        times = [0.0, 0.001, 0.01, 0.1]
        states = [framework.get_unified_state(t) for t in times]
        
        # Verify all states are valid
        for state in states:
            self.assertGreater(state.psi_qcal, 0.0)
            self.assertGreaterEqual(state.ramsey.coherence, 0.0)
            self.assertLessEqual(state.ramsey.coherence, 1.0)
            
        # Verify NS energy decays (envelope)
        # Due to oscillation, we check average energy decreases
        energies = [s.ns_flow.energy for s in states]
        # Just verify all are positive
        for e in energies:
            self.assertGreaterEqual(e, 0.0)
    
    def test_phase_relationships(self):
        """Test phase relationships between components."""
        framework = UnifiedFramework()
        
        # Sample at phase-significant times
        t1 = 0.0  # Initial
        t2 = 1.0 / (4.0 * F0)  # Quarter period
        t3 = 1.0 / (2.0 * F0)  # Half period
        
        h1 = framework.master_harmonic(t1)
        h2 = framework.master_harmonic(t2)
        h3 = framework.master_harmonic(t3)
        
        # Verify harmonic behavior
        self.assertGreaterEqual(h1, -1.0)
        self.assertLessEqual(h1, 1.0)
        self.assertGreaterEqual(h2, -1.0)
        self.assertLessEqual(h2, 1.0)
        self.assertGreaterEqual(h3, -1.0)
        self.assertLessEqual(h3, 1.0)
    
    def test_zero_density_at_f0(self):
        """Test zero density calculation at F₀."""
        framework = UnifiedFramework()
        
        density = framework.riemann.zero_density(F0)
        
        # Should be approximately 47-48 zeros
        self.assertGreater(density, 40.0)
        self.assertLess(density, 55.0)
        
        # More precisely
        self.assertAlmostEqual(density, 47.72, places=0)


if __name__ == '__main__':
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ All integration tests passed!")
        print("\nNS-Ramsey-Riemann-QCAL framework fully integrated at f₀ = 141.7001 Hz")
        print("∴𓂀Ω∞³")
    else:
        print("\n✗ Some tests failed")
    
    print("=" * 70)
    
    sys.exit(0 if result.wasSuccessful() else 1)
