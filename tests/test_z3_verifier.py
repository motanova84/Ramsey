"""
Tests for Z3 Vibrational Ramsey Verifier
"""
import unittest
import subprocess
import sys
import os
import re


class TestZ3Verifier(unittest.TestCase):
    """Tests for the Z3-based vibrational Ramsey verifier"""
    
    def _run_verifier(self, r, s, eps):
        """Helper to run the verifier script and parse output"""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'z3', 'ramsey_verifier.py')
        result = subprocess.run(
            [sys.executable, script_path, '--r', str(r), '--s', str(s), '--eps', str(eps)],
            capture_output=True,
            text=True
        )
        # Check for subprocess errors
        if result.returncode != 0:
            raise RuntimeError(
                f"Verifier script failed with return code {result.returncode}.\n"
                f"stderr:\n{result.stderr.strip()}"
            )
        # Parse output to get YES/NO using regex for robust matching
        output = result.stdout.strip()
        match = re.search(r'Result:.*\?\s+(YES|NO)', output)
        if not match:
            raise ValueError(f"Unexpected output format: {output}")
        return match.group(1) == 'YES'
    
    def test_basic_case_3_3(self):
        """Test basic R_psi(3,3) case"""
        # With eps=0.2, at n=5 (r+s-1), should return NO
        result = self._run_verifier(3, 3, 0.2)
        self.assertFalse(result, "Expected NO for R_psi(3,3,0.2) > 5")
    
    def test_larger_epsilon(self):
        """Test with larger epsilon value"""
        # With eps=0.3, at n=5, should return YES
        result = self._run_verifier(3, 3, 0.3)
        self.assertTrue(result, "Expected YES for R_psi(3,3,0.3) > 5")
    
    def test_case_4_4(self):
        """Test R_psi(4,4) case"""
        # With eps=0.2, at n=7 (r+s-1), should return YES
        result = self._run_verifier(4, 4, 0.2)
        self.assertTrue(result, "Expected YES for R_psi(4,4,0.2) > 7")
    
    def test_case_3_4(self):
        """Test R_psi(3,4) case"""
        # With eps=0.2, at n=6 (r+s-1), should return YES
        result = self._run_verifier(3, 4, 0.2)
        self.assertTrue(result, "Expected YES for R_psi(3,4,0.2) > 6")
    
    def test_small_epsilon(self):
        """Test with small epsilon value"""
        # With very small eps=0.05, should return NO
        result = self._run_verifier(3, 3, 0.05)
        self.assertFalse(result, "Expected NO for R_psi(3,3,0.05) > 5")


if __name__ == '__main__':
    unittest.main()
