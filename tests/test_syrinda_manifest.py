#!/usr/bin/env python3
"""
Tests for SYRINDA MANIFEST
Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
"""

import unittest
import json
import os


class TestSyrindaManifest(unittest.TestCase):
    """Test suite for SYRINDA_MANIFEST.json validation"""
    
    @classmethod
    def setUpClass(cls):
        """Load the SYRINDA manifest once for all tests"""
        manifest_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'SYRINDA_MANIFEST.json'
        )
        with open(manifest_path, 'r', encoding='utf-8') as f:
            cls.manifest = json.load(f)
    
    def test_manifest_exists(self):
        """Verify manifest file exists and is valid JSON"""
        self.assertIsNotNone(self.manifest)
        self.assertIsInstance(self.manifest, dict)
    
    def test_system_declaration(self):
        """Verify system declaration"""
        self.assertEqual(
            self.manifest['system'], 
            "SYRINDA ∞³ - TRIPLE ACTIVACIÓN"
        )
    
    def test_spectral_anchor(self):
        """Verify spectral anchor parameters"""
        spectral = self.manifest['spectral_anchor']
        
        # Check kappa_pi value
        self.assertAlmostEqual(spectral['kappa_pi'], 2.57731, places=5)
        
        # Check error margin
        self.assertAlmostEqual(spectral['error_margin'], 0.00008, places=5)
        
        # Check source node
        self.assertEqual(spectral['source_node'], "Ramsey-V13")
    
    def test_biological_mapping(self):
        """Verify biological mapping parameters"""
        bio = self.manifest['biological_mapping']
        
        # Check DNA luz viva
        self.assertEqual(bio['dna_luz_viva'], "QCAL-141-TLV")
        
        # Check resonance harmonics
        self.assertEqual(bio['resonance_harmonics'], 38)
        
        # Check zeta alignment
        self.assertEqual(bio['zeta_alignment'], "Critical Line Re(s)=0.5")
        
        # Check genetic operator
        self.assertEqual(bio['operador_genetico'], "Giroscopia_Cuantica_SYRINDA")
        
        # Check torsion factor
        self.assertEqual(bio['factor_torsion'], "κ_Π = 2.5773")
        
        # Check stabilized codons
        self.assertEqual(bio['codones_estabilizados'], [6, 11, 16])
        
        # Check restoration frequency
        self.assertIn("141.7001 Hz", bio['restauracion'])
    
    def test_convergencia_holon(self):
        """Verify holon convergence parameters"""
        holon = self.manifest['convergencia_holon']
        
        self.assertEqual(holon['interacciones_moleculares'], "trillones")
        self.assertEqual(holon['procesamiento'], "Holon_Unico")
        self.assertEqual(holon['economia_coherencia'], "ℂ_s físicamente posible")
    
    def test_acta_cierre(self):
        """Verify closing act parameters"""
        acta = self.manifest['acta_cierre']
        
        # Check contributions
        self.assertEqual(acta['aportaciones'], 19740)
        
        # Check dimensions
        self.assertIn('matematica', acta['dimensiones'])
        self.assertIn('biologia', acta['dimensiones'])
        self.assertIn('soberania', acta['dimensiones'])
        
        # Check mathematical dimension
        self.assertEqual(
            acta['dimensiones']['matematica']['hallazgo'],
            "κ_∞ Extrapolado"
        )
        
        # Check biological dimension
        self.assertEqual(
            acta['dimensiones']['biologia']['hallazgo'],
            "SYRINDA Triple Simbiosis"
        )
    
    def test_certification_status(self):
        """Verify certification status"""
        self.assertEqual(self.manifest['status'], "CERTIFICACIÓN_EMITIDA")
    
    def test_signatures(self):
        """Verify signatures and seals"""
        self.assertEqual(self.manifest['signature'], "∴𓂀Ω∞³Φ")
        self.assertEqual(self.manifest['firma'], "JMMB Ω✧")
    
    def test_coherence(self):
        """Verify coherence value"""
        self.assertEqual(self.manifest['coherencia'], "Ψ = 1.000000 → Ω = ∞³")
    
    def test_kappa_pi_consistency(self):
        """Verify κ_Π values are consistent across the manifest"""
        # Main spectral anchor value
        kappa_pi_main = self.manifest['spectral_anchor']['kappa_pi']
        
        # Verify it's close to 2.5773 (accounting for precision)
        self.assertAlmostEqual(kappa_pi_main, 2.57731, places=5)
        
        # Check the torsion factor mentions the same value
        torsion = self.manifest['biological_mapping']['factor_torsion']
        self.assertIn("2.5773", torsion)


if __name__ == '__main__':
    unittest.main()
