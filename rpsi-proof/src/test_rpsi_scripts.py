#!/usr/bin/env python3
"""
Tests for rpsi-proof scripts (generate_instance.py and verify_lrat.py)
"""

import unittest
import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_instance import generate_rpsi_instance, save_dimacs, is_resonant


class TestRpsiScripts(unittest.TestCase):
    """Test suite for rpsi-proof scripts"""
    
    def test_is_resonant(self):
        """Test resonance predicate"""
        print("\n=== Test: is_resonant function ===")
        
        # Test with known parameters
        f0 = 141.7001
        eps = 0.015
        grid = 128
        
        # Same frequency should always be resonant
        self.assertTrue(is_resonant(10, 10, grid, eps, f0))
        self.assertTrue(is_resonant(0, 0, grid, eps, f0))
        
        # Far apart frequencies should not be resonant
        self.assertFalse(is_resonant(0, 64, grid, eps, f0))
        self.assertFalse(is_resonant(10, 100, grid, eps, f0))
        
        # With small epsilon and large grid, adjacent points are not resonant
        # eps_grid = (0.015 * 128) / 141.7001 ≈ 0.0135 < 1
        self.assertFalse(is_resonant(0, 1, grid, eps, f0))
        
        # Test with larger epsilon where adjacent points would be resonant
        large_eps = 2.0
        self.assertTrue(is_resonant(0, 1, grid, large_eps, f0))
        
        print("✓ Test passed")
    
    def test_generate_small_instance(self):
        """Test generation of small Rψ instance"""
        print("\n=== Test: Generate small instance ===")
        
        # Generate a small instance (n=5, grid=16)
        clauses, num_vars, num_clauses = generate_rpsi_instance(
            n=5, f0=141.7001, eps=0.015, grid=16
        )
        
        print(f"Small instance (n=5, grid=16):")
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
            self.assertGreater(len(clause), 0)  # No empty clauses
            for lit in clause:
                self.assertIsInstance(lit, int)
                self.assertNotEqual(lit, 0)  # No zero literals
                self.assertGreater(abs(lit), 0)
                self.assertLessEqual(abs(lit), num_vars)
        
        print("✓ Test passed")
    
    def test_generate_r16_instance(self):
        """Test generation of K₁₆ instance (actual target)"""
        print("\n=== Test: Generate K₁₆ instance ===")
        
        # Generate the actual Rψ(5,5) instance for n=16
        clauses, num_vars, num_clauses = generate_rpsi_instance(
            n=16, f0=141.7001, eps=0.015, grid=128
        )
        
        print(f"K₁₆ instance (n=16, grid=128):")
        print(f"  Variables: {num_vars:,}")
        print(f"  Clauses: {num_clauses:,}")
        
        # Sanity checks
        self.assertIsInstance(clauses, list)
        self.assertGreater(num_vars, 0)
        self.assertGreater(num_clauses, 0)
        self.assertEqual(len(clauses), num_clauses)
        
        # Expected: at least 16*128 = 2048 variables for vertex frequencies
        self.assertGreaterEqual(num_vars, 2048)
        
        # Should have many clauses (one-hot, resonance, Ramsey constraints)
        self.assertGreater(num_clauses, 1000)
        
        print("✓ Test passed")
    
    def test_save_dimacs(self):
        """Test saving instance to DIMACS format"""
        print("\n=== Test: Save DIMACS ===")
        
        # Generate small instance
        clauses, num_vars, num_clauses = generate_rpsi_instance(
            n=4, f0=141.7001, eps=0.015, grid=8
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
            tmpfile = f.name
        
        try:
            save_dimacs(clauses, num_vars, num_clauses, tmpfile)
            
            # Verify file exists and has content
            self.assertTrue(os.path.exists(tmpfile))
            self.assertGreater(os.path.getsize(tmpfile), 0)
            
            # Read and verify DIMACS header
            with open(tmpfile, 'r') as f:
                first_line = f.readline().strip()
                self.assertTrue(first_line.startswith('p cnf'))
                
                # Parse header
                parts = first_line.split()
                self.assertEqual(parts[0], 'p')
                self.assertEqual(parts[1], 'cnf')
                self.assertEqual(int(parts[2]), num_vars)
                self.assertEqual(int(parts[3]), num_clauses)
                
                # Count clauses (lines ending with 0)
                f.seek(0)
                clause_count = sum(1 for line in f if line.strip().endswith('0') and not line.startswith('c'))
                self.assertEqual(clause_count, num_clauses)
            
            print(f"  Saved to: {tmpfile}")
            print(f"  Size: {os.path.getsize(tmpfile)} bytes")
            print("✓ Test passed")
            
        finally:
            # Clean up
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)


if __name__ == '__main__':
    unittest.main(verbosity=2)
