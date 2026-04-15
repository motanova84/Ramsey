#!/usr/bin/env python3
"""
Tests for Universal Coherence Mode and Infinite Prediction features
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_universal_coherence_mode():
    """Test universal coherence mode with direct positional arguments"""
    print("\n=== Test: Universal Coherence Mode ===")
    
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "3", "3", "--universal-coherence", 
         "--lam", "0.037", "--nmax", "10", "--grid", "64"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=30
    )
    
    output = result.stdout + result.stderr
    
    # Check for key output elements
    assert "AI-Ramsey-Formal v1.3.0" in output, "Should show version"
    assert "QCAL ∞³ COHERENCIA UNIVERSAL" in output, "Should show coherence mode"
    assert "Campo unificado" in output, "Should show phase 1"
    assert "RESULTADO UNIVERSAL" in output, "Should show results"
    assert "TABLA QCAL ∞³" in output, "Should show table"
    assert "ETERNALLY CERTIFIED" in output, "Should show certification"
    assert result.returncode == 0, f"Should succeed, got return code {result.returncode}"
    
    print("✓ Test passed: Universal coherence mode works correctly")
    return True


def test_predict_infinite_mode():
    """Test infinite prediction mode"""
    print("\n=== Test: Infinite Prediction Mode ===")
    
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "--max-r", "25", "--predict-infinite"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=10
    )
    
    output = result.stdout + result.stderr
    
    # Check for key output elements
    assert "AI-Ramsey-Formal v1.4.0" in output, "Should show version"
    assert "COHERENCIA INFINITA" in output, "Should show infinite mode"
    assert "Extrapolación áurea" in output, "Should show phase 1"
    assert "LÍMITE MÁXIMO" in output, "Should show limit"
    assert "R(15,15)" in output, "Should show R(15,15)"
    assert "R(20,20)" in output, "Should show R(20,20)"
    assert "R(25,25)" in output, "Should show R(25,25)"
    assert "POLINOMIAL" in output, "Should mention polynomial growth"
    assert result.returncode == 0, f"Should succeed, got return code {result.returncode}"
    
    print("✓ Test passed: Infinite prediction mode works correctly")
    return True


def test_script_generation():
    """Test demo script generation"""
    print("\n=== Test: Script Generation ===")
    
    # Clean up any existing scripts
    for script in ["r1010_demo.py", "ramsey_infinite.py"]:
        script_path = Path(script)
        if script_path.exists():
            script_path.unlink()
    
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "--generate-scripts"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=10
    )
    
    output = result.stdout + result.stderr
    
    # Check files were created
    assert Path("r1010_demo.py").exists(), "r1010_demo.py should be created"
    assert Path("ramsey_infinite.py").exists(), "ramsey_infinite.py should be created"
    assert "Generated: r1010_demo.py" in output, "Should show r1010_demo.py generated"
    assert "Generated: ramsey_infinite.py" in output, "Should show ramsey_infinite.py generated"
    assert result.returncode == 0, f"Should succeed, got return code {result.returncode}"
    
    # Verify scripts are executable
    result_r1010 = subprocess.run(
        ["python", "ramsey_infinite.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert "LÍMITE CÓSMICO" in result_r1010.stdout, "ramsey_infinite.py should run"
    assert "R(5,5)" in result_r1010.stdout, "Should compute R(5,5)"
    assert result_r1010.returncode == 0, "ramsey_infinite.py should succeed"
    
    print("✓ Test passed: Script generation works correctly")
    return True


def test_combined_modes():
    """Test combining flags"""
    print("\n=== Test: Combined Modes ===")
    
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "--max-r", "20", "--predict-infinite", "--generate-scripts"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=10
    )
    
    output = result.stdout + result.stderr
    
    # Check both modes worked
    assert "COHERENCIA INFINITA" in output, "Should show infinite mode"
    assert "Generated: r1010_demo.py" in output or Path("r1010_demo.py").exists(), "Should generate scripts"
    assert result.returncode == 0, f"Should succeed, got return code {result.returncode}"
    
    print("✓ Test passed: Combined modes work correctly")
    return True


def test_backward_compatibility():
    """Test that old certify command still works"""
    print("\n=== Test: Backward Compatibility ===")
    
    result = subprocess.run(
        ["python", "ai_ramsey_formal.py", "certify", "3", "3", 
         "--lam", "0.037", "--nmax", "10", "--grid", "64"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True,
        timeout=30
    )
    
    output = result.stdout + result.stderr
    
    # Check for certify command output
    assert "Certifying R_ψ(3,3)" in output or "Computing exact bound" in output, "Should run certify"
    assert result.returncode == 0, f"Should succeed, got return code {result.returncode}"
    
    print("✓ Test passed: Backward compatibility maintained")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Universal Coherence Mode Tests")
    print("=" * 70)
    
    tests = [
        test_universal_coherence_mode,
        test_predict_infinite_mode,
        test_script_generation,
        test_combined_modes,
        test_backward_compatibility,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
