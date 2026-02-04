#!/usr/bin/env python3
"""
Tests for LRAT certificate generation script
"""

import unittest
import os
import sys
import json
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

from generar_certificado_lrat import (
    generar_cnf_coherente,
    sellar_certificado,
    verificar_por_hash,
    CONFIG
)


class TestLRATCertificateGeneration(unittest.TestCase):
    """Test suite for LRAT certificate generation"""
    
    def test_config_values(self):
        """Test that configuration values are correct"""
        print("\n=== Test: Configuration values ===")
        
        self.assertEqual(CONFIG['ramsey_r'], 5)
        self.assertEqual(CONFIG['ramsey_s'], 5)
        self.assertEqual(CONFIG['n_max'], 16)
        self.assertEqual(CONFIG['epsilon'], 0.037)
        self.assertEqual(CONFIG['f0_hz'], 141.7001)
        
        print("✓ Configuration values are correct")
    
    def test_generate_cnf_coherente(self):
        """Test CNF generation for coherent Ramsey problem"""
        print("\n=== Test: Generate coherent CNF ===")
        
        # Generate small CNF instance
        cnf = generar_cnf_coherente(n=5, r=3, s=3, epsilon=0.037)
        
        # Check that CNF is a string
        self.assertIsInstance(cnf, str)
        
        # Check that it starts with the correct header
        self.assertTrue(cnf.startswith("p cnf"))
        
        # Parse header
        lines = cnf.split('\n')
        header = lines[0].split()
        self.assertEqual(header[0], 'p')
        self.assertEqual(header[1], 'cnf')
        
        # Verify variables and clauses are positive integers
        num_vars = int(header[2])
        num_clauses = int(header[3])
        
        self.assertGreater(num_vars, 0)
        self.assertGreater(num_clauses, 0)
        
        print(f"  Generated CNF with {num_vars} variables and {num_clauses} clauses")
        print("✓ CNF generation successful")
    
    def test_cnf_clause_format(self):
        """Test that CNF clauses are properly formatted"""
        print("\n=== Test: CNF clause format ===")
        
        # Generate small instance
        cnf = generar_cnf_coherente(n=4, r=3, s=3, epsilon=0.037)
        lines = cnf.split('\n')
        
        # Skip header
        clause_lines = [l for l in lines[1:] if l.strip() and not l.startswith('c')]
        
        # Check that each clause ends with 0
        for line in clause_lines:
            self.assertTrue(line.strip().endswith(' 0'), f"Clause doesn't end with 0: {line}")
        
        print(f"  Verified {len(clause_lines)} clauses")
        print("✓ All clauses properly formatted")
    
    def test_sellar_certificado(self):
        """Test cryptographic sealing of certificate"""
        print("\n=== Test: Certificate sealing ===")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lrat') as f:
            f.write("# Test LRAT certificate\n")
            f.write("# Test data for sealing\n")
            temp_path = f.name
        
        try:
            # Generate seal
            sello = sellar_certificado(temp_path)
            
            # Verify seal structure
            self.assertIn('hash_sha3_512', sello)
            self.assertIn('hash_sha256', sello)
            self.assertIn('sello_qcal', sello)
            self.assertIn('configuracion', sello)
            self.assertIn('timestamp', sello)
            
            # Verify hash formats
            self.assertEqual(len(sello['hash_sha3_512']), 128)  # SHA3-512 produces 128 hex chars
            self.assertEqual(len(sello['hash_sha256']), 64)     # SHA256 produces 64 hex chars
            
            # Verify QCAL seal
            self.assertIn('141.7001', sello['sello_qcal'])
            
            print(f"  SHA3-512: {sello['hash_sha3_512'][:32]}...")
            print(f"  SHA256: {sello['hash_sha256'][:32]}...")
            print(f"  QCAL Seal: {sello['sello_qcal']}")
            print("✓ Certificate sealed successfully")
            
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_verificar_por_hash(self):
        """Test hash-based verification"""
        print("\n=== Test: Hash verification ===")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cnf') as f:
            f.write("p cnf 3 2\n1 2 0\n-1 -2 0\n")
            cnf_path = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lrat') as f:
            f.write("# LRAT certificate\n")
            lrat_path = f.name
        
        try:
            # Verify
            result = verificar_por_hash(cnf_path, lrat_path)
            
            # Should return True since both files exist
            self.assertTrue(result)
            
            print("✓ Hash verification successful")
            
        finally:
            # Clean up
            os.unlink(cnf_path)
            os.unlink(lrat_path)
    
    def test_cnf_size_scaling(self):
        """Test that CNF size scales appropriately with n"""
        print("\n=== Test: CNF size scaling ===")
        
        sizes = []
        for n in [4, 6, 8]:
            cnf = generar_cnf_coherente(n=n, r=3, s=3, epsilon=0.037)
            lines = cnf.split('\n')
            header = lines[0].split()
            num_clauses = int(header[3])
            sizes.append((n, num_clauses))
            print(f"  n={n}: {num_clauses} clauses")
        
        # Verify that clauses increase with n
        for i in range(len(sizes) - 1):
            self.assertLess(sizes[i][1], sizes[i+1][1], 
                          f"Clauses should increase with n: {sizes[i]} vs {sizes[i+1]}")
        
        print("✓ CNF size scales correctly")


if __name__ == '__main__':
    print("="*70)
    print(" Test Suite: LRAT Certificate Generation")
    print(" Sello: ∴𓂀Ω∞³")
    print("="*70)
    
    # Run tests
    unittest.main(verbosity=2)
