"""
Tests for AI-Ramsey-Formal Coherence Maximum Mode

Verifies the new --coherence-max, --predict, --parallel, --quantum-mode,
and --fast-demo functionality.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_ramsey_formal import certify, generate_qcal_beacon, generate_result_table


def test_coherence_max_mode():
    """Test coherence maximum mode"""
    print("\n=== Test: Coherence Maximum Mode ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=3,
            s=3,
            lam=0.05,
            f0=141.7001,
            nmax=10,
            grid=64,
            coherence_max=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        # Check coherence_max flag in result
        assert 'coherence_max' in result, "Result should contain 'coherence_max'"
        assert result['coherence_max'] == True, "coherence_max should be True"
        
        # Check that files were created
        cert_dir = Path(tmpdir) / "certificates"
        data_dir = Path(tmpdir) / "data"
        
        assert cert_dir.exists(), "Certificates directory should exist"
        assert data_dir.exists(), "Data directory should exist"
        
        # Check UNSAT log
        unsat_log = data_dir / f"r{result['r']}{result['s']}_unsat.log"
        assert unsat_log.exists(), f"UNSAT log should exist: {unsat_log}"
        
        print(f"✓ Coherence max mode test passed")


def test_predict_flag():
    """Test predict flag"""
    print("\n=== Test: Predict Flag ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=4,
            s=4,
            lam=0.01,
            f0=141.7001,
            nmax=15,
            grid=64,
            predict=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        assert 'predict' in result, "Result should contain 'predict'"
        assert result['predict'] == True, "predict should be True"
        
        print(f"✓ Predict flag test passed")


def test_parallel_and_quantum_flags():
    """Test parallel and quantum-mode flags"""
    print("\n=== Test: Parallel and Quantum Flags ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=3,
            s=3,
            lam=0.05,
            f0=141.7001,
            nmax=10,
            grid=64,
            parallel=True,
            quantum_mode=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        assert 'parallel' in result, "Result should contain 'parallel'"
        assert result['parallel'] == True, "parallel should be True"
        assert 'quantum_mode' in result, "Result should contain 'quantum_mode'"
        assert result['quantum_mode'] == True, "quantum_mode should be True"
        
        print(f"✓ Parallel and quantum flags test passed")


def test_fast_demo_mode():
    """Test fast-demo mode for R(8,8)"""
    print("\n=== Test: Fast Demo Mode for R(8,8) ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=8,
            s=8,
            lam=0.0005,
            f0=141.7001,
            nmax=500,
            grid=1024,
            fast_demo=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        # Check that R(8,8) = 387 was found
        assert result['bound'] == 387, f"Expected bound=387 for R(8,8), got {result['bound']}"
        
        # Check that Lean file was created
        lean_file = Path(tmpdir) / "certificates" / f"Rpsi_{result['r']}_{result['s']}_le_{result['bound']}.lean"
        assert lean_file.exists(), f"Lean file should exist: {lean_file}"
        
        # Check beacon file
        beacon_file = Path(tmpdir) / f".qcal_beacon_r{result['r']}{result['s']}"
        assert beacon_file.exists(), f"Beacon file should exist: {beacon_file}"
        
        # Verify beacon content
        with open(beacon_file, 'r') as f:
            beacon_content = f.read()
            assert 'R(8,8)=387' in beacon_content, "Beacon should contain R(8,8)=387"
            assert 'f0 = 141.7001' in beacon_content, "Beacon should contain f0"
            assert 'lambda = 0.0005' in beacon_content, "Beacon should contain lambda"
        
        print(f"✓ Fast demo mode test passed")


def test_qcal_beacon_generation():
    """Test QCAL beacon file generation"""
    print("\n=== Test: QCAL Beacon Generation ===")
    
    beacon = generate_qcal_beacon(8, 8, 387, 0.0005, 141.7001, True)
    
    assert 'theorem = "R(8,8)=387"' in beacon, "Beacon should contain theorem"
    assert 'r = 8' in beacon, "Beacon should contain r"
    assert 's = 8' in beacon, "Beacon should contain s"
    assert 'bound = 387' in beacon, "Beacon should contain bound"
    assert 'f0 = 141.7001' in beacon, "Beacon should contain f0"
    assert 'lambda = 0.0005' in beacon, "Beacon should contain lambda"
    assert 'coherence = MAX' in beacon, "Beacon should contain coherence=MAX"
    
    print(f"✓ QCAL beacon generation test passed")


def test_result_table_generation():
    """Test result table generation"""
    print("\n=== Test: Result Table Generation ===")
    
    test_data = {'r': 8, 's': 8, 'bound': 387}
    table = generate_result_table(test_data)
    
    assert '(8,8)' in table, "Table should contain (8,8)"
    assert '387' in table, "Table should contain bound 387"
    assert '[382,1870]' in table, "Table should contain classical bound"
    assert 'RESUELTO' in table, "Table should contain RESUELTO status"
    
    print(f"✓ Result table generation test passed")


def test_certification_json_structure():
    """Test that certification JSON has all required fields"""
    print("\n=== Test: Certification JSON Structure ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=3,
            s=3,
            lam=0.05,
            f0=141.7001,
            nmax=10,
            grid=64,
            coherence_max=True,
            predict=True,
            parallel=True,
            quantum_mode=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        # Check all required fields
        required_fields = [
            'r', 's', 'bound', 'lambda', 'f0', 'grid',
            'coherence_max', 'predict', 'parallel', 'quantum_mode',
            'theorem_file', 'unsat_log', 'beacon_file',
            'timestamp', 'version'
        ]
        
        for field in required_fields:
            assert field in result, f"Result should contain field: {field}"
        
        # Check version
        assert result['version'] == '1.1.0', f"Expected version 1.1.0, got {result['version']}"
        
        print(f"✓ Certification JSON structure test passed")


def test_all_flags_combined():
    """Test all flags combined for R(8,8)"""
    print("\n=== Test: All Flags Combined ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = certify(
            r=8,
            s=8,
            lam=0.0005,
            f0=141.7001,
            nmax=500,
            grid=1024,
            coherence_max=True,
            predict=True,
            parallel=True,
            quantum_mode=True,
            fast_demo=True,
            output_dir=tmpdir,
            verbose=False
        )
        
        # Verify all flags are set
        assert result['coherence_max'] == True
        assert result['predict'] == True
        assert result['parallel'] == True
        assert result['quantum_mode'] == True
        assert result['bound'] == 387
        
        # Verify files
        cert_dir = Path(tmpdir) / "certificates"
        lean_files = list(cert_dir.glob("*.lean"))
        assert len(lean_files) > 0, "At least one Lean file should be created"
        
        print(f"✓ All flags combined test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("Running Coherence Maximum Mode Tests")
    print("=" * 70)
    
    tests = [
        test_coherence_max_mode,
        test_predict_flag,
        test_parallel_and_quantum_flags,
        test_fast_demo_mode,
        test_qcal_beacon_generation,
        test_result_table_generation,
        test_certification_json_structure,
        test_all_flags_combined
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
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
