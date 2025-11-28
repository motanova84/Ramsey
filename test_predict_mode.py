"""
Tests for the --predict mode of ai_ramsey_formal.py

Tests the fancy output and certificate generation.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_predict_mode_basic():
    """Test basic predict mode with small example"""
    print("\n=== Test: Predict mode with R(3,3) ===")
    
    # Run the predict command
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "3", "3", 
         "--f0", "141.7001", "--lam", "0.001", "--nmax", "10", "--grid", "32", "--predict"],
        capture_output=True,
        text=True,
        cwd="/home/runner/work/Ramsey/Ramsey"
    )
    
    # Check that it ran successfully
    assert result.returncode == 0, f"Command failed with error:\n{result.stderr}"
    
    # Check for expected output strings
    output = result.stdout
    assert "RESULTADO EN TIEMPO REAL" in output, "Missing header"
    assert "AI-Ramsey-Formal v1.0.0" in output, "Missing version"
    assert "QCAL ∞³" in output, "Missing QCAL"
    assert "[1/6]" in output, "Missing step 1"
    assert "[2/6]" in output, "Missing step 2"
    assert "[3/6]" in output, "Missing step 3"
    assert "[4/6]" in output, "Missing step 4"
    assert "[5/6]" in output, "Missing step 5"
    assert "[6/6]" in output, "Missing step 6"
    assert "PREDICCIÓN FINAL" in output, "Missing prediction header"
    assert "FORMALLY CERTIFIED" in output, "Missing certification"
    assert "TABLA ACTUALIZADA" in output, "Missing table"
    assert "r77_demo.py" in output or "r33_demo.py" in output, "Missing demo script mention"
    
    # Check that certificate files were created
    assert Path("certificates/Rpsi_3_3_le_5.lean").exists() or \
           Path("certificates/Rpsi_3_3_le_6.lean").exists(), \
           "Certificate file not created"
    
    assert Path(".qcal_beacon_r33").exists(), "Beacon file not created"
    assert Path("data/r33_unsat.log").exists(), "UNSAT log not created"
    
    print("✓ Test passed: Predict mode works correctly")


def test_demo_script_exists():
    """Test that r77_demo.py exists and is executable"""
    print("\n=== Test: Demo script exists ===")
    
    demo_script = Path("/home/runner/work/Ramsey/Ramsey/r77_demo.py")
    assert demo_script.exists(), "r77_demo.py does not exist"
    assert os.access(demo_script, os.X_OK), "r77_demo.py is not executable"
    
    # Check that it has proper shebang
    with open(demo_script) as f:
        first_line = f.readline().strip()
        assert first_line.startswith("#!"), "Missing shebang"
        assert "python" in first_line.lower(), "Shebang doesn't mention python"
    
    print("✓ Test passed: Demo script exists and is executable")


def test_parallel_flag():
    """Test that --parallel flag is accepted"""
    print("\n=== Test: --parallel flag ===")
    
    # Run help to check if flag is accepted
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "--help"],
        capture_output=True,
        text=True,
        cwd="/home/runner/work/Ramsey/Ramsey"
    )
    
    assert "--parallel" in result.stdout, "--parallel flag not in help"
    
    print("✓ Test passed: --parallel flag is accepted")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Predict Mode Tests")
    print("=" * 70)
    
    tests = [
        test_predict_mode_basic,
        test_demo_script_exists,
        test_parallel_flag,
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
