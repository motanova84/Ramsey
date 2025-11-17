"""
Tests for RPSI SAT generator and solver
"""
import unittest
import os
from pathlib import Path
from src.generate_rpsi_sat import generate_rpsi_sat_instance_tseytin

class TestRPSISAT(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path("data/test")
        self.test_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test files"""
        if self.test_dir.exists():
            for f in self.test_dir.glob("*.cnf"):
                f.unlink()
    
    def test_generate_small_instance(self):
        """Test generation of small SAT instance"""
        output_path = self.test_dir / "test_small.cnf"
        vars_count, clauses_count = generate_rpsi_sat_instance_tseytin(
            n=3, r=2, s=2,
            f0=141.7001, eps=0.037, grid=16,
            output_path=str(output_path)
        )
        
        # Check file was created
        self.assertTrue(output_path.exists())
        
        # Check file has content
        self.assertGreater(output_path.stat().st_size, 0)
        
        # Verify DIMACS header
        with open(output_path, 'r') as f:
            header = f.readline().strip()
            self.assertTrue(header.startswith('p cnf'))
            parts = header.split()
            self.assertEqual(int(parts[2]), vars_count)
            self.assertEqual(int(parts[3]), clauses_count)
    
    def test_main_instance_exists(self):
        """Test that main instance file was created"""
        main_cnf = Path("data/rpsi_5_5_n16.cnf")
        self.assertTrue(main_cnf.exists(), "Main CNF file should exist")
        
        # Check it's not empty
        self.assertGreater(main_cnf.stat().st_size, 1000000, 
                          "CNF file should be at least 1MB")
        
        # Verify header
        with open(main_cnf, 'r') as f:
            header = f.readline().strip()
            self.assertEqual(header, "p cnf 17528 200360")
    
    def test_cnf_format(self):
        """Test that generated CNF follows DIMACS format"""
        output_path = self.test_dir / "test_format.cnf"
        generate_rpsi_sat_instance_tseytin(
            n=4, r=3, s=3,
            f0=141.7001, eps=0.037, grid=32,
            output_path=str(output_path)
        )
        
        with open(output_path, 'r') as f:
            lines = f.readlines()
            
            # First line should be header
            self.assertTrue(lines[0].startswith('p cnf'))
            
            # All clause lines should end with ' 0\n'
            for i, line in enumerate(lines[1:11]):  # Check first 10 clauses
                self.assertTrue(line.strip().endswith('0'), 
                               f"Clause {i+1} should end with 0")
    
    def test_parameter_validation(self):
        """Test that different parameters produce different results"""
        output1 = self.test_dir / "test1.cnf"
        output2 = self.test_dir / "test2.cnf"
        
        # Generate with different grid sizes
        vars1, clauses1 = generate_rpsi_sat_instance_tseytin(
            n=3, r=2, s=2, grid=8, output_path=str(output1)
        )
        vars2, clauses2 = generate_rpsi_sat_instance_tseytin(
            n=3, r=2, s=2, grid=16, output_path=str(output2)
        )
        
        # Different grid sizes should produce different number of variables
        self.assertNotEqual(vars1, vars2)
    
    def test_lean_proof_exists(self):
        """Test that Lean proof file was created"""
        lean_file = Path("proofs/Rpsi_5_5_le_16.lean")
        self.assertTrue(lean_file.exists(), "Lean proof file should exist")
        
        # Check it contains required definitions
        content = lean_file.read_text()
        self.assertIn("def f0", content)
        self.assertIn("def ε", content)
        self.assertIn("def grid", content)
        self.assertIn("theorem Rψ_5_5_le_16", content)

if __name__ == '__main__':
    unittest.main()
