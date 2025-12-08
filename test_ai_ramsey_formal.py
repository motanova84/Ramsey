"""
Tests for AI-Ramsey-Formal CLI tool

Verifies the CLI functionality without requiring OpenAI API key.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_ramsey_formal import certify, lean_theorem, generate_qcal_beacon


def test_certify_basic():
    """Test basic certification flow"""
    print("\n=== Test: Basic certification (3,3) ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=3,
            s=3,
            lam=0.037,
            f0=141.7001,
            nmax=10,
            grid=32,
            output_dir=tmpdir
        )
        
        # Check result structure
        assert 'r' in result, "Result should contain 'r'"
        assert 'bound' in result, "Result should contain 'bound'"
        assert result['r'] == 3, f"Expected r=3, got {result['r']}"
        assert result['s'] == 3, f"Expected s=3, got {result['s']}"
        assert result['bound'] >= 3, f"Bound should be >= 3, got {result['bound']}"
        
        # Check files were created
        lean_file = Path(result['theorem_file'])
        cert_file = Path(tmpdir) / f"Rpsi_{result['r']}_{result['s']}_certification.json"
        
        assert lean_file.exists(), f"Lean file should exist: {lean_file}"
        assert cert_file.exists(), f"Certification JSON should exist: {cert_file}"
        
        # Verify Lean file content
        lean_content = lean_file.read_text()
        assert 'import Mathlib.Combinatorics.Ramsey' in lean_content, "Lean file should import Mathlib"
        assert f'R_psi_{result["r"]}_{result["s"]}_le_{result["bound"]}' in lean_content, "Lean file should define theorem"
        
        # Verify certification JSON
        with open(cert_file) as f:
            cert_data = json.load(f)
        assert cert_data['r'] == 3, "Certification should have r=3"
        assert cert_data['s'] == 3, "Certification should have s=3"
        assert 'timestamp' in cert_data, "Certification should have timestamp"
        
        print(f"✓ Test passed: Found bound R_psi(3,3) <= {result['bound']}")


def test_certify_asymmetric():
    """Test asymmetric case (3,4)"""
    print("\n=== Test: Asymmetric certification (3,4) ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=3,
            s=4,
            lam=0.037,
            f0=141.7001,
            nmax=15,
            grid=32,
            output_dir=tmpdir
        )
        
        assert result['r'] == 3, f"Expected r=3, got {result['r']}"
        assert result['s'] == 4, f"Expected s=4, got {result['s']}"
        assert result['bound'] >= max(3, 4), f"Bound should be >= max(r,s)"
        
        # Check theorem file was created
        lean_file = Path(result['theorem_file'])
        assert lean_file.exists(), "Lean file should be created"
        
        print(f"✓ Test passed: Found bound R_psi(3,4) <= {result['bound']}")


def test_no_bound_found():
    """Test when no bound is found in range"""
    print("\n=== Test: No bound found in range ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use very small nmax so no bound is found
        result = certify(
            r=5,
            s=5,
            lam=0.037,
            f0=141.7001,
            nmax=6,  # Too small to find bound
            grid=32,
            output_dir=tmpdir
        )
        
        assert result['success'] == False, "Should fail when no bound found"
        assert 'error' in result, "Should contain error message"
        
        print("✓ Test passed: Correctly handles no bound found")


def test_lean_theorem_generation():
    """Test Lean theorem generation"""
    print("\n=== Test: Lean theorem generation ===")
    
    lean_code = lean_theorem(r=3, s=3, n=6, lam=0.001, f0=141.7001)
    
    assert 'import Mathlib.Combinatorics.Ramsey' in lean_code, "Should import Mathlib"
    assert 'theorem R_psi_3_3_le_6' in lean_code, "Should define theorem with correct name"
    assert 'vibrational_unsat_tac' in lean_code, "Should use vibrational_unsat_tac"
    assert '0.001' in lean_code, "Should include lam parameter"
    assert '141.7001' in lean_code, "Should include f0 parameter"
    
    print("✓ Test passed: Lean theorem generated correctly")


def test_qcal_beacon_generation():
    """Test QCAL beacon generation"""
    print("\n=== Test: QCAL beacon generation ===")
    
    beacon = generate_qcal_beacon(r=4, s=4, n=12, lam=0.05, f0=141.7001, coherence_mode=True)
    
    assert 'R(4,4)=12' in beacon, "Should mention R(4,4)=12"
    assert '12' in beacon, "Should mention bound value"
    assert 'f0 = 141.7001' in beacon, "Should mention f0 parameter"
    assert 'lambda = 0.05' in beacon, "Should mention lambda parameter"
    assert 'coherence = MAX' in beacon, "Should mention coherence mode"
    
    print("✓ Test passed: QCAL beacon generated correctly")


def test_output_directory_creation():
    """Test that output directory is created if it doesn't exist"""
    print("\n=== Test: Output directory creation ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "nested" / "directory"
        assert not output_dir.exists(), "Output directory should not exist initially"
        
        result = certify(
            r=3,
            s=3,
            lam=0.037,
            f0=141.7001,
            nmax=10,
            grid=32,
            output_dir=str(output_dir)
        )
        
        assert output_dir.exists(), "Output directory should be created"
        lean_file = Path(result['theorem_file'])
        assert lean_file.exists(), "Lean file should be in created directory"
        
        print("✓ Test passed: Output directory created successfully")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running AI-Ramsey-Formal CLI Tests")
    print("=" * 70)
    
    tests = [
        test_certify_basic,
        test_certify_asymmetric,
        test_no_bound_found,
        test_lean_theorem_generation,
        test_qcal_beacon_generation,
        test_output_directory_creation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
