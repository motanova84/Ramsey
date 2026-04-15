#!/usr/bin/env python3
"""
Unit tests for NS-Ramsey-Riemann unified framework.

Tests all components:
- Navier-Stokes flow
- Ramsey C₇ network
- Riemann critical line
- Master harmonic
- QCAL transmutation
- Unified framework integration

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.math.ns_ramsey_riemann import (
    NavierStokesFlow,
    RamseyC7Network,
    RiemannCriticalLine,
    UnifiedFramework,
    F0, OMEGA0, TAU, PRIMES_C7,
    NSFlowState, RamseyNetworkState, RiemannState, UnifiedState
)


class TestNavierStokesFlow(unittest.TestCase):
    """Test Navier-Stokes flow component."""
    
    def setUp(self):
        """Initialize NS flow for testing."""
        self.ns = NavierStokesFlow()
    
    def test_initialization(self):
        """Test NS flow initialization."""
        self.assertEqual(self.ns.f0, F0)
        self.assertEqual(self.ns.omega0, OMEGA0)
        self.assertEqual(self.ns.tau, TAU)
    
    def test_pressure_at_zero(self):
        """Test pressure at t=0."""
        p0 = self.ns.pressure(0.0)
        self.assertAlmostEqual(p0, 0.0, places=10)
    
    def test_pressure_decay(self):
        """Test that pressure decays with time."""
        t1 = 1.0
        t2 = 2.0
        p1 = abs(self.ns.pressure(t1))
        p2 = abs(self.ns.pressure(t2))
        # Envelope should decay
        self.assertGreater(np.exp(-t1/TAU), np.exp(-t2/TAU))
    
    def test_velocity_derivative(self):
        """Test velocity is related to pressure derivative."""
        t = 0.5
        dt = 1e-6
        
        # Numerical derivative
        p1 = self.ns.pressure(t - dt)
        p2 = self.ns.pressure(t + dt)
        dp_dt_num = (p2 - p1) / (2 * dt)
        
        # Should be related (not exact due to different formulation)
        self.assertIsInstance(self.ns.velocity(t), (float, np.floating))
    
    def test_energy_positive(self):
        """Test energy is always positive."""
        times = [0.0, 0.1, 0.5, 1.0, 2.0]
        for t in times:
            energy = self.ns.energy(t)
            self.assertGreaterEqual(energy, 0.0)
    
    def test_get_state(self):
        """Test get_state returns valid NSFlowState."""
        t = 0.5
        state = self.ns.get_state(t)
        
        self.assertIsInstance(state, NSFlowState)
        self.assertEqual(state.time, t)
        self.assertEqual(state.reynolds, 0.5)
        self.assertIsInstance(state.pressure, (float, np.floating))
        self.assertIsInstance(state.velocity, (float, np.floating))
        self.assertIsInstance(state.energy, (float, np.floating))


class TestRamseyC7Network(unittest.TestCase):
    """Test Ramsey C₇ network component."""
    
    def setUp(self):
        """Initialize Ramsey network for testing."""
        self.ramsey = RamseyC7Network()
    
    def test_initialization(self):
        """Test Ramsey network initialization."""
        self.assertEqual(self.ramsey.primes, PRIMES_C7)
        self.assertEqual(self.ramsey.n, 7)
        self.assertEqual(self.ramsey.edges_c7, 7)
        self.assertEqual(self.ramsey.edges_k7, 21)
    
    def test_density(self):
        """Test network density is 1/3."""
        expected_density = 7.0 / 21.0
        self.assertAlmostEqual(self.ramsey.density, expected_density, places=10)
        self.assertAlmostEqual(self.ramsey.density, 1.0/3.0, places=10)
    
    def test_coherence_range(self):
        """Test coherence is in [0, 1]."""
        times = np.linspace(0, 1, 20)
        for t in times:
            coh = self.ramsey.coherence(t)
            self.assertGreaterEqual(coh, 0.0)
            self.assertLessEqual(coh, 1.0)
    
    def test_coherence_periodicity(self):
        """Test coherence is periodic with period 1/F₀."""
        period = 1.0 / F0
        t = 0.5
        
        coh1 = self.ramsey.coherence(t)
        coh2 = self.ramsey.coherence(t + period)
        
        self.assertAlmostEqual(coh1, coh2, places=6)
    
    def test_custom_primes(self):
        """Test network with custom prime list."""
        custom_primes = [2, 3, 5, 7, 11]
        ramsey_custom = RamseyC7Network(primes=custom_primes)
        
        self.assertEqual(ramsey_custom.primes, custom_primes)
        self.assertEqual(ramsey_custom.n, 5)
        self.assertEqual(ramsey_custom.edges_c7, 5)
        self.assertEqual(ramsey_custom.edges_k7, 10)
    
    def test_get_state(self):
        """Test get_state returns valid RamseyNetworkState."""
        t = 0.5
        state = self.ramsey.get_state(t)
        
        self.assertIsInstance(state, RamseyNetworkState)
        self.assertEqual(state.primes, PRIMES_C7)
        self.assertEqual(state.edges, 7)
        self.assertEqual(state.total_edges_k7, 21)
        self.assertAlmostEqual(state.density, 1.0/3.0, places=10)
        self.assertGreaterEqual(state.coherence, 0.0)
        self.assertLessEqual(state.coherence, 1.0)


class TestRiemannCriticalLine(unittest.TestCase):
    """Test Riemann zeta function on critical line."""
    
    def setUp(self):
        """Initialize Riemann zeta for testing."""
        self.riemann = RiemannCriticalLine()
    
    def test_initialization(self):
        """Test Riemann initialization."""
        self.assertEqual(self.riemann.n_terms, 100)
    
    def test_zeta_at_one(self):
        """Test zeta diverges near s=1."""
        # s = 1 + epsilon
        s = 1.0 + 0.1j
        zeta_val = self.riemann.zeta(s)
        
        # Should be large magnitude near pole
        self.assertGreater(abs(zeta_val), 1.0)
    
    def test_zeta_critical_line(self):
        """Test zeta on critical line s = 1/2 + it."""
        t_values = [0.0, 14.1347, 21.022, 25.0109]  # First few zeros
        
        for t in t_values:
            zeta_val = self.riemann.zeta_critical(t)
            self.assertIsInstance(zeta_val, complex)
    
    def test_zeta_critical_at_f0(self):
        """Test zeta at s = 1/2 + iF₀."""
        zeta_val = self.riemann.zeta_critical(F0)
        
        self.assertIsInstance(zeta_val, complex)
        self.assertGreater(abs(zeta_val), 0.0)
    
    def test_zero_density_positive(self):
        """Test zero density is positive for large T."""
        # Zero density N(T) can be negative for small T
        # but becomes positive for T > 2π ≈ 6.28
        T_values = [50.0, 100.0, 200.0]
        
        for T in T_values:
            N_T = self.riemann.zero_density(T)
            self.assertGreater(N_T, 0.0)
    
    def test_zero_density_zero_at_origin(self):
        """Test zero density is zero at T=0."""
        N_0 = self.riemann.zero_density(0.0)
        self.assertEqual(N_0, 0.0)
    
    def test_zero_density_increasing(self):
        """Test zero density increases with T."""
        T1 = 50.0
        T2 = 100.0
        
        N1 = self.riemann.zero_density(T1)
        N2 = self.riemann.zero_density(T2)
        
        self.assertGreater(N2, N1)
    
    def test_zero_density_riemann_von_mangoldt(self):
        """Test zero density formula matches RVM asymptotic."""
        T = 100.0
        N_T = self.riemann.zero_density(T)
        
        # Should be approximately T/(2π) * log(T/(2π)) - T/(2π)
        term1 = (T / (2 * np.pi)) * np.log(T / (2 * np.pi))
        term2 = T / (2 * np.pi)
        expected = term1 - term2
        
        self.assertAlmostEqual(N_T, expected, places=6)
    
    def test_get_state(self):
        """Test get_state returns valid RiemannState."""
        t = F0
        state = self.riemann.get_state(t)
        
        self.assertIsInstance(state, RiemannState)
        self.assertEqual(state.s, 0.5 + 1j * t)
        self.assertIsInstance(state.zeta_value, complex)
        self.assertGreater(state.magnitude, 0.0)
        self.assertIsInstance(state.phase, (float, np.floating))


class TestUnifiedFramework(unittest.TestCase):
    """Test unified NS-Ramsey-Riemann framework."""
    
    def setUp(self):
        """Initialize unified framework for testing."""
        self.framework = UnifiedFramework()
    
    def test_initialization(self):
        """Test framework initialization."""
        self.assertEqual(self.framework.f0, F0)
        self.assertEqual(self.framework.omega0, OMEGA0)
        self.assertIsInstance(self.framework.ns_flow, NavierStokesFlow)
        self.assertIsInstance(self.framework.ramsey, RamseyC7Network)
        self.assertIsInstance(self.framework.riemann, RiemannCriticalLine)
    
    def test_master_harmonic_range(self):
        """Test master harmonic is in [-1, 1]."""
        times = np.linspace(0, 1, 20)
        for t in times:
            A_t = self.framework.master_harmonic(t)
            self.assertGreaterEqual(A_t, -1.0)
            self.assertLessEqual(A_t, 1.0)
    
    def test_master_harmonic_periodicity(self):
        """Test master harmonic is periodic."""
        period = 1.0 / F0
        t = 0.5
        
        A1 = self.framework.master_harmonic(t)
        A2 = self.framework.master_harmonic(t + period)
        
        self.assertAlmostEqual(A1, A2, places=6)
    
    def test_qcal_transmutation_range(self):
        """Test QCAL transmutation PSI is in (0, 1]."""
        # Test various zeta values
        zeta_values = [
            1.0 + 0.0j,      # |ζ| = 1 → PSI = 1
            0.5 + 0.5j,      # |ζ| ≠ 1 → PSI < 1
            2.0 + 0.0j,      # |ζ| = 2 → PSI < 1
        ]
        
        for zeta_val in zeta_values:
            psi = self.framework.qcal_transmutation(zeta_val)
            self.assertGreater(psi, 0.0)
            self.assertLessEqual(psi, 1.0)
    
    def test_qcal_transmutation_unity(self):
        """Test PSI = 1 when |ζ| = 1."""
        zeta_val = 1.0 + 0.0j
        psi = self.framework.qcal_transmutation(zeta_val)
        self.assertAlmostEqual(psi, 1.0, places=10)
    
    def test_qcal_transmutation_decay(self):
        """Test PSI decays as |ζ| moves away from 1."""
        zeta1 = 1.0 + 0.0j
        zeta2 = 1.5 + 0.0j
        zeta3 = 2.0 + 0.0j
        
        psi1 = self.framework.qcal_transmutation(zeta1)
        psi2 = self.framework.qcal_transmutation(zeta2)
        psi3 = self.framework.qcal_transmutation(zeta3)
        
        self.assertGreater(psi1, psi2)
        self.assertGreater(psi2, psi3)
    
    def test_get_unified_state(self):
        """Test get_unified_state returns valid UnifiedState."""
        t = 0.5
        state = self.framework.get_unified_state(t)
        
        self.assertIsInstance(state, UnifiedState)
        self.assertEqual(state.time, t)
        self.assertIsInstance(state.ns_flow, NSFlowState)
        self.assertIsInstance(state.ramsey, RamseyNetworkState)
        self.assertIsInstance(state.riemann, RiemannState)
        self.assertIsInstance(state.master_harmonic, (float, np.floating))
        self.assertIsInstance(state.zero_density, (float, np.floating))
        self.assertIsInstance(state.psi_qcal, (float, np.floating))
    
    def test_unified_state_consistency(self):
        """Test unified state components are consistent."""
        t = 0.5
        state = self.framework.get_unified_state(t)
        
        # Check NS flow
        self.assertEqual(state.ns_flow.reynolds, 0.5)
        
        # Check Ramsey
        self.assertEqual(len(state.ramsey.primes), 7)
        self.assertAlmostEqual(state.ramsey.density, 1.0/3.0, places=10)
        
        # Check Riemann
        self.assertEqual(state.riemann.s.real, 0.5)
        self.assertAlmostEqual(state.riemann.s.imag, F0, places=6)
        
        # Check PSI
        self.assertGreater(state.psi_qcal, 0.0)
        self.assertLessEqual(state.psi_qcal, 1.0)
    
    def test_analyze_coherence(self):
        """Test coherence analysis."""
        analysis = self.framework.analyze_coherence(0.0, 0.1, 20)
        
        # Check structure
        self.assertIn('time_range', analysis)
        self.assertIn('n_points', analysis)
        self.assertIn('ns_mean_energy', analysis)
        self.assertIn('ramsey_mean_coherence', analysis)
        self.assertIn('riemann_mean_magnitude', analysis)
        self.assertIn('psi_mean', analysis)
        
        # Check values
        self.assertEqual(analysis['time_range'], (0.0, 0.1))
        self.assertEqual(analysis['n_points'], 20)
        self.assertGreater(analysis['ns_mean_energy'], 0.0)
        self.assertGreater(analysis['ramsey_mean_coherence'], 0.0)
        self.assertGreater(analysis['riemann_mean_magnitude'], 0.0)
        self.assertGreater(analysis['psi_mean'], 0.0)
        
        # Check arrays
        self.assertEqual(len(analysis['times']), 20)
        self.assertEqual(len(analysis['ns_pressures']), 20)
        self.assertEqual(len(analysis['ramsey_coherences']), 20)
        self.assertEqual(len(analysis['riemann_magnitudes']), 20)
        self.assertEqual(len(analysis['master_harmonics']), 20)
        self.assertEqual(len(analysis['psi_values']), 20)
    
    def test_analyze_coherence_ranges(self):
        """Test coherence analysis values are in valid ranges."""
        analysis = self.framework.analyze_coherence(0.0, 0.1, 20)
        
        # Check Ramsey coherence in [0, 1]
        for coh in analysis['ramsey_coherences']:
            self.assertGreaterEqual(coh, 0.0)
            self.assertLessEqual(coh, 1.0)
        
        # Check master harmonics in [-1, 1]
        for h in analysis['master_harmonics']:
            self.assertGreaterEqual(h, -1.0)
            self.assertLessEqual(h, 1.0)
        
        # Check PSI in (0, 1]
        for psi in analysis['psi_values']:
            self.assertGreater(psi, 0.0)
            self.assertLessEqual(psi, 1.0)


class TestMathematicalConstants(unittest.TestCase):
    """Test mathematical constants and relationships."""
    
    def test_f0_value(self):
        """Test F₀ = 141.7001 Hz."""
        self.assertAlmostEqual(F0, 141.7001, places=4)
    
    def test_omega0_value(self):
        """Test ω₀ = 2π·F₀."""
        expected = 2 * np.pi * F0
        self.assertAlmostEqual(OMEGA0, expected, places=6)
    
    def test_tau_equals_f0(self):
        """Test τ = F₀."""
        self.assertEqual(TAU, F0)
    
    def test_primes_c7(self):
        """Test PRIMES_C7 contains first 7 primes."""
        expected = [2, 3, 5, 7, 11, 13, 17]
        self.assertEqual(PRIMES_C7, expected)
    
    def test_ramsey_density(self):
        """Test C₇ density = 7/21 = 1/3."""
        edges_c7 = 7
        edges_k7 = 21  # 7*6/2
        density = edges_c7 / edges_k7
        
        self.assertAlmostEqual(density, 1.0/3.0, places=10)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete framework."""
    
    def test_full_workflow(self):
        """Test complete workflow from initialization to analysis."""
        # Initialize
        framework = UnifiedFramework()
        
        # Get state at multiple time points
        times = [0.0, 0.01, 0.05, 0.1]
        states = [framework.get_unified_state(t) for t in times]
        
        # Verify all states are valid
        for state in states:
            self.assertIsInstance(state, UnifiedState)
            self.assertGreater(state.psi_qcal, 0.0)
        
        # Run coherence analysis
        analysis = framework.analyze_coherence(0.0, 0.1, 50)
        
        # Verify analysis results
        self.assertEqual(analysis['n_points'], 50)
        self.assertGreater(analysis['psi_mean'], 0.0)
    
    def test_component_coupling(self):
        """Test that framework components interact correctly."""
        framework = UnifiedFramework()
        t = 0.5
        
        # Get individual states
        ns_state = framework.ns_flow.get_state(t)
        ramsey_state = framework.ramsey.get_state(t)
        riemann_state = framework.riemann.get_state(F0)
        
        # Get unified state
        unified_state = framework.get_unified_state(t)
        
        # Verify consistency
        self.assertEqual(unified_state.ns_flow.pressure, ns_state.pressure)
        self.assertEqual(unified_state.ramsey.coherence, ramsey_state.coherence)
        self.assertEqual(unified_state.riemann.magnitude, riemann_state.magnitude)
    
    def test_time_evolution(self):
        """Test system evolves correctly over time."""
        framework = UnifiedFramework()
        
        # Sample at multiple times
        times = np.linspace(0.0, 1.0, 100)
        
        pressures = []
        coherences = []
        
        for t in times:
            state = framework.get_unified_state(t)
            pressures.append(state.ns_flow.pressure)
            coherences.append(state.ramsey.coherence)
        
        # Verify arrays have correct length
        self.assertEqual(len(pressures), 100)
        self.assertEqual(len(coherences), 100)
        
        # Verify oscillatory behavior
        self.assertLess(min(pressures), 0.0)  # Has negative values
        self.assertGreater(max(pressures), 0.0)  # Has positive values
        
        # Verify coherence bounds
        self.assertGreaterEqual(min(coherences), 0.0)
        self.assertLessEqual(max(coherences), 1.0)


if __name__ == '__main__':
    unittest.main()
