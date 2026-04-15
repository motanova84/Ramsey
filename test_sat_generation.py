#!/usr/bin/env python3
"""
Tests for SAT instance generation using Tseytin encoding
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ramsey_vibracional import generate_rpsi_sat_instance_tseytin, save_dimacs
import tempfile


class TestSATGeneration(unittest.TestCase):
    """Test suite for SAT instance generation"""
    
    def test_generate_small_instance(self):
        """Test generation of small SAT instance"""
        print("\n=== Test: Generate small instance ===")
        
        # Generate a small instance (3 vertices, K_2 vs K_2)
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n=3, r=2, s=2, f0=141.7001, eps=0.037, grid=4
        )
        
        print(f"Small instance (n=3, r=2, s=2, grid=4):")
        print(f"  Variables: {num_vars}")
        print(f"  Clauses: {num_clauses}")
        
        # Basic sanity checks
        self.assertIsInstance(clauses, list)
        self.assertGreater(num_vars, 0)
        self.assertGreater(num_clauses, 0)
        self.assertEqual(len(clauses), num_clauses)
        
        # Check clause structure
        for clause in clauses:
            self.assertIsInstance(clause, list)
            for lit in clause:
                self.assertIsInstance(lit, int)
                self.assertGreater(abs(lit), 0)
                self.assertLessEqual(abs(lit), num_vars)
        
        print("✓ Test passed")
    
    def test_generate_medium_instance(self):
        """Test generation of medium SAT instance"""
        print("\n=== Test: Generate medium instance ===")
        
        # Generate medium instance (5 vertices, K_3 vs K_3)
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n=5, r=3, s=3, f0=141.7001, eps=0.037, grid=8
        )
        
        print(f"Medium instance (n=5, r=3, s=3, grid=8):")
        print(f"  Variables: {num_vars}")
        print(f"  Clauses: {num_clauses}")
        
        # Sanity checks
        self.assertGreater(num_vars, 100)  # Should have at least n*grid variables
        self.assertGreater(num_clauses, 100)
        
        print("✓ Test passed")
    
    def test_dimacs_format(self):
        """Test DIMACS file format output"""
        print("\n=== Test: DIMACS format ===")
        
        # Generate small instance
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n=3, r=2, s=2, f0=141.7001, eps=0.037, grid=4
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
            temp_path = f.name
        
        try:
            save_dimacs(clauses, num_vars, num_clauses, temp_path)
            
            # Read and verify format
            with open(temp_path, 'r') as f:
                lines = f.readlines()
            
            # Check header
            self.assertTrue(lines[0].startswith('p cnf'))
            header_parts = lines[0].split()
            self.assertEqual(header_parts[0], 'p')
            self.assertEqual(header_parts[1], 'cnf')
            self.assertEqual(int(header_parts[2]), num_vars)
            self.assertEqual(int(header_parts[3]), num_clauses)
            
            # Check clauses
            clause_lines = [l for l in lines[1:] if l.strip()]
            self.assertEqual(len(clause_lines), num_clauses)
            
            for line in clause_lines:
                self.assertTrue(line.strip().endswith(' 0'))
            
            print(f"DIMACS file created: {temp_path}")
            print(f"  Header: {lines[0].strip()}")
            print(f"  Clauses: {len(clause_lines)}")
            print("✓ Test passed")
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_parameter_validation(self):
        """Test that generated instance has expected properties"""
        print("\n=== Test: Parameter validation ===")
        
        n, r, s, grid = 4, 2, 2, 8
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n=n, r=r, s=s, f0=141.7001, eps=0.037, grid=grid
        )
        
        # Expected minimum number of frequency variables: n * grid
        min_freq_vars = n * grid
        print(f"Expected at least {min_freq_vars} frequency variables")
        self.assertGreaterEqual(num_vars, min_freq_vars)
        
        # Expected edge variables: n*(n-1)/2
        num_edges = n * (n - 1) // 2
        print(f"Expected {num_edges} edge variables")
        
        # Total should include frequency vars + edge vars + auxiliary vars
        print(f"Total variables: {num_vars}")
        self.assertGreater(num_vars, min_freq_vars + num_edges)
        
        print("✓ Test passed")
    
    def test_rpsi_5_5_n16_properties(self):
        """Test properties of the R_ψ(5,5) n=16 instance"""
        print("\n=== Test: R_ψ(5,5) n=16 instance properties ===")
        
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n=16, r=5, s=5, f0=141.7001, eps=0.037, grid=128
        )
        
        print(f"R_ψ(5,5) instance (n=16, grid=128):")
        print(f"  Variables: {num_vars:,}")
        print(f"  Clauses: {num_clauses:,}")
        
        # Verify expected values from problem statement
        self.assertEqual(num_vars, 17528)
        self.assertEqual(num_clauses, 200360)
        
        print("✓ Values match problem statement")
        print("✓ Test passed")


if __name__ == '__main__':
    print("="*70)
    print("  Tests for SAT Instance Generation")
    print("  Tseytin Encoding - Vibrational Ramsey")
    print("="*70)
    
    unittest.main(verbosity=2)
