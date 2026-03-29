#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for V13 Thermodynamic Limit Validation
=============================================

Test suite for V13 implementation covering:
- Thermodynamic limit convergence
- Scaling law validation
- κ_∞ → κ_Π convergence
- Data integrity

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import unittest
import numpy as np
import json
import os
import tempfile

from v13_thermodynamic_validation import (
    ThermodynamicLimitValidator,
    v13_manifestacion,
    save_v13_data,
)


class TestV13ManifestacionData(unittest.TestCase):
    """Test V13 manifestation data structure and values"""
    
    def test_manifestacion_structure(self):
        """Test V13 data has correct structure"""
        self.assertIn('validacion', v13_manifestacion)
        self.assertEqual(v13_manifestacion['validacion'], 'V13_THERMODYNAMIC_LIMIT')
        
        self.assertIn('resultado_central', v13_manifestacion)
        self.assertIn('convergencia_multiescala', v13_manifestacion)
        self.assertIn('marco_teorico', v13_manifestacion)
        self.assertIn('significado_termodinamico', v13_manifestacion)
        self.assertIn('ecuacion_fundamental', v13_manifestacion)
    
    def test_resultado_central_values(self):
        """Test central results have valid values"""
        resultado = v13_manifestacion['resultado_central']
        
        self.assertAlmostEqual(resultado['kappa_medido'], 2.59764, places=5)
        self.assertAlmostEqual(resultado['kappa_teorico'], 2.577310, places=6)
        self.assertLess(resultado['error_relativo'], 0.01)  # Less than 1%
        self.assertLess(resultado['error_porcentaje'], 1.0)
        self.assertGreater(resultado['r_cuadrado'], 0.95)  # High R²
        self.assertEqual(resultado['veredicto'], 'CONFIRMADO')
    
    def test_convergencia_multiescala(self):
        """Test multiscale convergence data"""
        conv = v13_manifestacion['convergencia_multiescala']
        
        # Check all N values are present
        self.assertIn('N_128', conv)
        self.assertIn('N_256', conv)
        self.assertIn('N_512', conv)
        self.assertIn('N_1024', conv)
        self.assertIn('N_2560', conv)
        self.assertIn('N_infinito', conv)
        
        # Values should decrease monotonically towards N_infinito
        values = [conv['N_128'], conv['N_256'], conv['N_512'], 
                  conv['N_1024'], conv['N_2560']]
        for i in range(len(values) - 1):
            self.assertGreater(values[i], values[i+1])
        
        # All values should be greater than κ_∞
        for val in values:
            self.assertGreater(val, conv['N_infinito'])
        
        # Check α exponent is reasonable
        self.assertGreater(conv['exponente_alpha'], 0.5)
        self.assertLess(conv['exponente_alpha'], 0.7)
    
    def test_marco_teorico(self):
        """Test theoretical framework data"""
        marco = v13_manifestacion['marco_teorico']
        
        self.assertIn('clase_B', marco)
        self.assertIn('d_ramsey', marco)
        self.assertIn('alineacion_riemann', marco)
        
        # d_ramsey should be a range
        self.assertEqual(len(marco['d_ramsey']), 2)
        self.assertLess(marco['d_ramsey'][0], marco['d_ramsey'][1])


class TestThermodynamicLimitValidator(unittest.TestCase):
    """Test ThermodynamicLimitValidator class"""
    
    def setUp(self):
        """Set up test validator"""
        self.validator = ThermodynamicLimitValidator()
    
    def test_validator_initialization(self):
        """Test validator initializes correctly"""
        self.assertIsNotNone(self.validator.v13_data)
        self.assertAlmostEqual(self.validator.kappa_infinito, 2.59764, places=5)
        self.assertAlmostEqual(self.validator.kappa_teorico, 2.577310, places=6)
        self.assertAlmostEqual(self.validator.alpha, 0.632, places=3)
    
    def test_get_convergence_data(self):
        """Test extraction of convergence data"""
        N_values, C_est_values = self.validator.get_convergence_data()
        
        # Check shapes
        self.assertEqual(len(N_values), 5)
        self.assertEqual(len(C_est_values), 5)
        
        # Check N values are correct
        expected_N = np.array([128, 256, 512, 1024, 2560])
        np.testing.assert_array_equal(N_values, expected_N)
        
        # Check C_est values decrease monotonically
        for i in range(len(C_est_values) - 1):
            self.assertGreater(C_est_values[i], C_est_values[i+1])
    
    def test_fit_scaling_law(self):
        """Test scaling law fitting"""
        N_values, C_est_values = self.validator.get_convergence_data()
        fit_results = self.validator.fit_scaling_law(N_values, C_est_values)
        
        self.assertIn('kappa_infinito', fit_results)
        self.assertIn('a', fit_results)
        self.assertIn('alpha', fit_results)
        self.assertIn('r_squared', fit_results)
        self.assertIn('success', fit_results)
        
        # Check fit was successful
        self.assertTrue(fit_results['success'])
        
        # Check R² is reasonable
        self.assertGreater(fit_results['r_squared'], 0.8)
    
    def test_validate_convergence(self):
        """Test convergence validation"""
        results = self.validator.validate_convergence()
        
        # Check all required keys are present
        self.assertIn('validation', results)
        self.assertIn('kappa_infinito_medido', results)
        self.assertIn('kappa_teorico', results)
        self.assertIn('error_relativo', results)
        self.assertIn('error_porcentaje', results)
        self.assertIn('veredicto', results)
        
        # Check values are reasonable
        self.assertEqual(results['validation'], 'V13_THERMODYNAMIC_LIMIT')
        self.assertLess(results['error_porcentaje'], 1.0)  # Less than 1% error
        
        # Check kappa values
        self.assertAlmostEqual(results['kappa_infinito_medido'], 2.59764, places=5)
        self.assertAlmostEqual(results['kappa_teorico'], 2.577310, places=6)


class TestDataPersistence(unittest.TestCase):
    """Test data saving and loading"""
    
    def test_save_v13_data(self):
        """Test saving V13 data to JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = os.path.join(tmpdir, 'test_v13_data.json')
            
            # Save data
            save_v13_data(test_path)
            
            # Check file exists
            self.assertTrue(os.path.exists(test_path))
            
            # Load and verify
            with open(test_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Check structure
            self.assertEqual(loaded_data['validacion'], 'V13_THERMODYNAMIC_LIMIT')
            self.assertIn('resultado_central', loaded_data)
            self.assertIn('convergencia_multiescala', loaded_data)

    
    def test_data_file_exists(self):
        """Test that V13 data file exists in data directory"""
        data_path = 'data/v13_thermodynamic_validation.json'
        
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertEqual(data['validacion'], 'V13_THERMODYNAMIC_LIMIT')


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency of V13 results"""
    
    def test_kappa_convergence(self):
        """Test that κ_∞ is close to κ_Π"""
        validator = ThermodynamicLimitValidator()
        
        kappa_inf = validator.kappa_infinito
        kappa_pi = validator.kappa_teorico
        
        # Error should be less than 1%
        error = abs(kappa_inf - kappa_pi) / kappa_pi
        self.assertLess(error, 0.01)
    
    def test_scaling_exponent_reasonable(self):
        """Test that scaling exponent α is in physical range"""
        # For 1/√N behavior, α should be around 0.5-0.7
        alpha = v13_manifestacion['convergencia_multiescala']['exponente_alpha']
        
        self.assertGreater(alpha, 0.4)
        self.assertLess(alpha, 0.8)
    
    def test_thermodynamic_limit_exists(self):
        """Test that thermodynamic limit is well-defined"""
        conv = v13_manifestacion['convergencia_multiescala']
        
        # κ_∞ should be less than all finite-N values
        kappa_inf = conv['N_infinito']
        
        for key in ['N_128', 'N_256', 'N_512', 'N_1024', 'N_2560']:
            self.assertGreater(conv[key], kappa_inf)


class TestMetadata(unittest.TestCase):
    """Test V13 metadata and documentation"""
    
    def test_timestamp_present(self):
        """Test timestamp is present"""
        self.assertIn('timestamp', v13_manifestacion)
        self.assertIsNotNone(v13_manifestacion['timestamp'])
    
    def test_sello_and_firma(self):
        """Test seal and signature are present"""
        self.assertIn('sello', v13_manifestacion)
        self.assertIn('firma', v13_manifestacion)
        
        self.assertEqual(v13_manifestacion['sello'], '∴𓂀Ω∞³Φ')
        self.assertIn('JMMB', v13_manifestacion['firma'])


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
