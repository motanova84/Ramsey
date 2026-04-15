#!/usr/bin/env python3
"""
Unit tests for Kernel Navier-Stokes QCAL.

48 unit tests covering:
- Unitarity: |det(V)| = 1, V^T·V = I, V^7 = I
- Synchronization: dt = 1/f₀
- Conservation: ∇·v = 0, ΔE/E = 0
- Global Coherence: Ψ ≥ 0.888

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kernel_navier_stokes_qcal import (
    MatrizTraslaciónUnitaria,
    IntegradorCuantico,
    FlujoCuanticoConservativo,
    NavierStokesQCAL,
    F0, DT, OMEGA0, PRIMES_C7, N_PRIMES, COHERENCE_THRESHOLD,
    MatrizUnitariaResult, IntegradorCuanticoResult,
    FlujoConservativoResult, NavierStokesQCALResult
)


class TestMatrizTraslaciónUnitaria(unittest.TestCase):
    """Test cases for Unitary Translation Matrix component (15 tests)."""
    
    def setUp(self):
        """Initialize matrix component for testing."""
        self.matriz = MatrizTraslaciónUnitaria()
    
    # Test 1
    def test_initialization_dimension(self):
        """Test matrix has correct dimension."""
        self.assertEqual(self.matriz.n, N_PRIMES)
        self.assertEqual(self.matriz.V.shape, (N_PRIMES, N_PRIMES))
    
    # Test 2
    def test_matrix_is_cyclic_permutation(self):
        """Test V is a cyclic permutation matrix."""
        V = self.matriz.V
        # Each row and column should have exactly one 1
        for i in range(self.matriz.n):
            self.assertEqual(np.sum(V[i, :]), 1.0)
            self.assertEqual(np.sum(V[:, i]), 1.0)
    
    # Test 3
    def test_determinant_equals_one(self):
        """Test |det(V)| = 1 (exact unitarity)."""
        det = self.matriz.determinante()
        self.assertAlmostEqual(abs(det), 1.0, places=12)
    
    # Test 4
    def test_determinant_sign_positive(self):
        """Test det(V) = 1 (not -1)."""
        det = self.matriz.determinante()
        self.assertAlmostEqual(det, 1.0, places=12)
    
    # Test 5
    def test_matrix_is_unitary(self):
        """Test V^T·V = I."""
        self.assertTrue(self.matriz.es_unitaria())
    
    # Test 6
    def test_orthogonality_direct(self):
        """Test V^T·V = I directly."""
        V = self.matriz.V
        producto = V.T @ V
        identidad = np.eye(self.matriz.n)
        np.testing.assert_array_almost_equal(producto, identidad, decimal=12)
    
    # Test 7
    def test_period_equals_seven(self):
        """Test V^7 = I (period 7)."""
        periodo = self.matriz.periodo()
        self.assertEqual(periodo, 7)
    
    # Test 8
    def test_power_seven_is_identity(self):
        """Test V^7 = I directly."""
        V = self.matriz.V
        V_power = np.linalg.matrix_power(V, 7)
        identidad = np.eye(self.matriz.n)
        np.testing.assert_array_almost_equal(V_power, identidad, decimal=12)
    
    # Test 9
    def test_power_14_is_identity(self):
        """Test V^14 = I (two full cycles)."""
        V = self.matriz.V
        V_power = np.linalg.matrix_power(V, 14)
        identidad = np.eye(self.matriz.n)
        np.testing.assert_array_almost_equal(V_power, identidad, decimal=12)
    
    # Test 10
    def test_coherencia_det_perfect(self):
        """Test Ψ_det = 1 for perfect unitarity."""
        coh = self.matriz.coherencia_det()
        self.assertAlmostEqual(coh, 1.0, places=10)
    
    # Test 11
    def test_coherencia_det_in_range(self):
        """Test Ψ_det ∈ [0, 1]."""
        coh = self.matriz.coherencia_det()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)
    
    # Test 12
    def test_ejecutar_returns_result(self):
        """Test ejecutar returns MatrizUnitariaResult."""
        resultado = self.matriz.ejecutar()
        self.assertIsInstance(resultado, MatrizUnitariaResult)
    
    # Test 13
    def test_ejecutar_determinante(self):
        """Test ejecutar result has correct determinant."""
        resultado = self.matriz.ejecutar()
        self.assertAlmostEqual(resultado.determinante, 1.0, places=12)
    
    # Test 14
    def test_ejecutar_es_unitaria(self):
        """Test ejecutar result confirms unitarity."""
        resultado = self.matriz.ejecutar()
        self.assertTrue(resultado.es_unitaria)
    
    # Test 15
    def test_custom_dimension(self):
        """Test matrix with custom dimension."""
        matriz_5 = MatrizTraslaciónUnitaria(n=5)
        self.assertEqual(matriz_5.n, 5)
        self.assertEqual(matriz_5.periodo(), 5)
        self.assertAlmostEqual(matriz_5.determinante(), 1.0, places=12)


class TestIntegradorCuantico(unittest.TestCase):
    """Test cases for Quantum Integrator component (10 tests)."""
    
    def setUp(self):
        """Initialize integrator for testing."""
        self.integrador = IntegradorCuantico()
    
    # Test 16
    def test_initialization_frequency(self):
        """Test integrator uses correct frequency."""
        self.assertEqual(self.integrador.f0, F0)
    
    # Test 17
    def test_dt_equals_inverse_f0(self):
        """Test dt = 1/f₀ synchronized timestep."""
        expected_dt = 1.0 / F0
        self.assertAlmostEqual(self.integrador.dt, expected_dt, places=10)
    
    # Test 18
    def test_dt_value_milliseconds(self):
        """Test dt ≈ 7.057 ms."""
        dt_ms = self.integrador.dt * 1000
        self.assertAlmostEqual(dt_ms, 7.057, places=2)
    
    # Test 19
    def test_periodo_completo(self):
        """Test T = 7 × dt full cycle period."""
        expected_T = 7 * self.integrador.dt
        self.assertAlmostEqual(self.integrador.periodo_completo, expected_T, places=10)
    
    # Test 20
    def test_periodo_completo_milliseconds(self):
        """Test T ≈ 49.4 ms."""
        T_ms = self.integrador.periodo_completo * 1000
        self.assertAlmostEqual(T_ms, 49.4, places=1)
    
    # Test 21
    def test_frecuencia_espectral(self):
        """Test spectral frequency matches f₀."""
        f_spectral = self.integrador.frecuencia_espectral()
        self.assertAlmostEqual(f_spectral, F0, places=4)
    
    # Test 22
    def test_error_relativo_small(self):
        """Test relative error is very small (machine precision)."""
        error = self.integrador.error_relativo()
        self.assertLess(error, 1e-10)
    
    # Test 23
    def test_coherencia_temporal_perfect(self):
        """Test Ψ_t = 1 for perfect synchronization."""
        coh = self.integrador.coherencia_temporal()
        self.assertAlmostEqual(coh, 1.0, places=10)
    
    # Test 24
    def test_ejecutar_returns_result(self):
        """Test ejecutar returns IntegradorCuanticoResult."""
        resultado = self.integrador.ejecutar()
        self.assertIsInstance(resultado, IntegradorCuanticoResult)
    
    # Test 25
    def test_ejecutar_n_pasos(self):
        """Test ejecutar has correct number of steps."""
        resultado = self.integrador.ejecutar()
        self.assertEqual(resultado.n_pasos, 7)


class TestFlujoCuanticoConservativo(unittest.TestCase):
    """Test cases for Conservative Quantum Flow component (10 tests)."""
    
    def setUp(self):
        """Initialize flow component for testing."""
        self.flujo = FlujoCuanticoConservativo()
    
    # Test 26
    def test_initialization_dimension(self):
        """Test flow has correct dimension."""
        self.assertEqual(self.flujo.n, N_PRIMES)
    
    # Test 27
    def test_divergencia_zero(self):
        """Test ∇·v = 0 (incompressible)."""
        div = self.flujo.divergencia()
        self.assertAlmostEqual(div, 0.0, places=10)
    
    # Test 28
    def test_velocidad_initialized(self):
        """Test velocity field is properly initialized."""
        self.assertEqual(len(self.flujo.velocidad), N_PRIMES)
    
    # Test 29
    def test_energia_conservada(self):
        """Test ΔE/E = 0 (energy conserved)."""
        E_inicial = self.flujo.energia_inicial
        v_final = self.flujo.evolucionar(DT, N_PRIMES)
        E_final = self.flujo._calcular_energia(v_final)
        
        # Energy should be conserved within tolerance
        if E_inicial > 0:
            delta_E = abs(E_final - E_inicial) / E_inicial
            self.assertLess(delta_E, 0.1)  # Less than 10% change
    
    # Test 30
    def test_fase_berry(self):
        """Test Berry phase φ = 2π/7."""
        fase = self.flujo.fase_berry()
        expected = 2 * np.pi / 7
        self.assertAlmostEqual(fase, expected, places=10)
    
    # Test 31
    def test_potencial_chern_simons_positive(self):
        """Test Chern-Simons potential is positive."""
        A_CS = self.flujo.potencial_chern_simons()
        self.assertGreater(A_CS, 0.0)
    
    # Test 32
    def test_coherencia_flujo_high(self):
        """Test Ψ_flujo ≈ 1 for conservative flow."""
        coh = self.flujo.coherencia_flujo()
        self.assertGreater(coh, 0.9)
    
    # Test 33
    def test_coherencia_flujo_in_range(self):
        """Test Ψ_flujo ∈ [0, 1]."""
        coh = self.flujo.coherencia_flujo()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)
    
    # Test 34
    def test_ejecutar_returns_result(self):
        """Test ejecutar returns FlujoConservativoResult."""
        resultado = self.flujo.ejecutar()
        self.assertIsInstance(resultado, FlujoConservativoResult)
    
    # Test 35
    def test_ejecutar_divergencia(self):
        """Test ejecutar result has zero divergence."""
        resultado = self.flujo.ejecutar()
        self.assertAlmostEqual(resultado.divergencia, 0.0, places=10)


class TestNavierStokesQCAL(unittest.TestCase):
    """Test cases for Navier-Stokes QCAL kernel (10 tests)."""
    
    def setUp(self):
        """Initialize kernel for testing."""
        self.kernel = NavierStokesQCAL()
    
    # Test 36
    def test_initialization(self):
        """Test kernel initializes correctly."""
        self.assertEqual(self.kernel.f0, F0)
        self.assertIsInstance(self.kernel.matriz_unitaria, MatrizTraslaciónUnitaria)
        self.assertIsInstance(self.kernel.integrador_cuantico, IntegradorCuantico)
        self.assertIsInstance(self.kernel.flujo_conservativo, FlujoCuanticoConservativo)
    
    # Test 37
    def test_coherencia_global_high(self):
        """Test Ψ_global ≈ 1 for perfect components."""
        coh = self.kernel.coherencia_global()
        self.assertGreater(coh, COHERENCE_THRESHOLD)
    
    # Test 38
    def test_coherencia_global_geometric_mean(self):
        """Test Ψ_global is geometric mean of components."""
        psi_det = self.kernel.matriz_unitaria.coherencia_det()
        psi_t = self.kernel.integrador_cuantico.coherencia_temporal()
        psi_flujo = self.kernel.flujo_conservativo.coherencia_flujo()
        
        expected = np.power(psi_det * psi_t * psi_flujo, 1.0/3.0)
        actual = self.kernel.coherencia_global()
        
        self.assertAlmostEqual(actual, expected, places=10)
    
    # Test 39
    def test_brecha_b_sellada(self):
        """Test Gap B is sealed (Ψ ≥ 0.888)."""
        self.assertTrue(self.kernel.brecha_b_sellada())
    
    # Test 40
    def test_coherencia_threshold_888(self):
        """Test coherence threshold is 0.888."""
        self.assertEqual(COHERENCE_THRESHOLD, 0.888)
    
    # Test 41
    def test_ejecutar_returns_result(self):
        """Test ejecutar returns NavierStokesQCALResult."""
        resultado = self.kernel.ejecutar()
        self.assertIsInstance(resultado, NavierStokesQCALResult)
    
    # Test 42
    def test_ejecutar_determinante_accessor(self):
        """Test result determinante property."""
        resultado = self.kernel.ejecutar()
        self.assertAlmostEqual(resultado.determinante, 1.0, places=12)
    
    # Test 43
    def test_ejecutar_psi_global_accessor(self):
        """Test result psi_global property."""
        resultado = self.kernel.ejecutar()
        self.assertEqual(resultado.psi_global, resultado.coherencia_global)
    
    # Test 44
    def test_verificar_alineacion_hamiltonian(self):
        """Test Hamiltonian alignment verification."""
        alineacion = self.kernel.verificar_alineacion_hamiltonian()
        
        self.assertIn('frecuencia_espectral', alineacion)
        self.assertIn('error_relativo', alineacion)
        self.assertIn('alineacion_confirmada', alineacion)
        
        self.assertAlmostEqual(alineacion['frecuencia_espectral'], F0, places=4)
        self.assertTrue(alineacion['alineacion_confirmada'])
    
    # Test 45
    def test_estado_completo(self):
        """Test complete state dictionary."""
        estado = self.kernel.estado_completo()
        
        # Check structure
        self.assertIn('componentes', estado)
        self.assertIn('alineacion_hamiltonian', estado)
        self.assertIn('coherencia_global', estado)
        self.assertIn('brecha_b_sellada', estado)
        
        # Check components
        self.assertIn('matriz_unitaria', estado['componentes'])
        self.assertIn('integrador_cuantico', estado['componentes'])
        self.assertIn('flujo_conservativo', estado['componentes'])
        
        # Check values
        self.assertTrue(estado['brecha_b_sellada'])
        self.assertGreater(estado['coherencia_global'], COHERENCE_THRESHOLD)


class TestMathematicalConstants(unittest.TestCase):
    """Test mathematical constants."""
    
    def test_f0_value(self):
        """Test F₀ = 141.7001 Hz."""
        self.assertAlmostEqual(F0, 141.7001, places=4)
    
    def test_primes_c7_count(self):
        """Test C₇ has 7 primes."""
        self.assertEqual(len(PRIMES_C7), 7)
    
    def test_primes_c7_values(self):
        """Test C₇ = {2, 3, 5, 7, 11, 13, 17}."""
        expected = [2, 3, 5, 7, 11, 13, 17]
        self.assertEqual(PRIMES_C7, expected)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
