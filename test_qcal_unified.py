#!/usr/bin/env python3
"""
Tests for QCAL Unified Framework
"""

import sys
import json
import numpy as np
from qcal_unified_framework import QCALUnifiedFramework
from cross_verification_protocol import CrossVerificationProtocol


def test_framework_initialization():
    """Test that framework initializes correctly."""
    print("Testing framework initialization...", end=" ")
    framework = QCALUnifiedFramework()
    
    assert len(framework.constants) == 8, "Should have 8 universal constants"
    assert len(framework.problems) == 7, "Should have 7 millennium problems"
    assert len(framework.operators) == 7, "Should have 7 operators"
    
    print("✓")


def test_universal_constants():
    """Test that universal constants have correct values."""
    print("Testing universal constants...", end=" ")
    framework = QCALUnifiedFramework()
    
    assert framework.constants['kappa_pi'] == 2.5773
    assert framework.constants['f0'] == 141.7001
    assert framework.constants['critical_line'] == 0.5
    assert abs(framework.constants['ramsey_ratio'] - 43/108) < 0.001
    assert framework.constants['navier_stokes_epsilon'] == 0.5772
    assert framework.constants['bsd_delta'] == 1.0
    
    print("✓")


def test_operators():
    """Test that all operators work."""
    print("Testing operators...", end=" ")
    framework = QCALUnifiedFramework()
    
    # Test P vs NP operator
    result = framework.D_PNP_operator({'treewidth': 10})
    assert isinstance(result, float)
    assert result > 0
    
    # Test Riemann operator
    result = framework.H_Psi_operator({'s': 0.5 + 14j})
    assert isinstance(result, complex)
    
    # Test BSD operator
    result = framework.L_E_operator({'rank': 0, 'omega': 1.0})
    assert isinstance(result, float)
    assert result > 0
    
    # Test Navier-Stokes operator
    result = framework.NS_operator({'viscosity': 1.0})
    assert isinstance(result, float)
    assert result > 0
    
    # Test Ramsey operator
    result = framework.R_operator({'m': 5, 'n': 5})
    assert isinstance(result, int)
    assert result > 0
    
    print("✓")


def test_problem_connections():
    """Test that problem connections are computed correctly."""
    print("Testing problem connections...", end=" ")
    framework = QCALUnifiedFramework()
    
    # P vs NP should connect to Ramsey
    connections = framework.find_connections('p_vs_np')
    assert 'ramsey' in connections
    
    # Riemann should connect to several problems
    connections = framework.find_connections('riemann')
    assert len(connections) > 0
    
    # All problems should have a connections entry
    all_connections = framework.get_all_connections()
    assert len(all_connections) == len(framework.problems)
    
    print("✓")


def test_unify_problem():
    """Test problem unification."""
    print("Testing problem unification...", end=" ")
    framework = QCALUnifiedFramework()
    
    # Test P vs NP unification
    result = framework.unify_problem('p_vs_np', {'treewidth': 10})
    assert 'problem' in result
    assert 'eigenvalue' in result
    assert 'universal_constant' in result
    assert result['problem'] == 'P vs NP'
    
    # Test invalid problem
    result = framework.unify_problem('invalid', {})
    assert 'error' in result
    
    print("✓")


def test_framework_coherence():
    """Test framework coherence calculation."""
    print("Testing framework coherence...", end=" ")
    framework = QCALUnifiedFramework()
    
    coherence = framework.calculate_coherence()
    assert isinstance(coherence, float)
    assert 0 <= coherence <= 1, "Coherence should be between 0 and 1"
    
    print("✓")


def test_demonstration():
    """Test full framework demonstration."""
    print("Testing framework demonstration...", end=" ")
    framework = QCALUnifiedFramework()
    
    results = framework.demonstrate_unification()
    assert len(results) == len(framework.problems)
    
    for problem_key, result in results.items():
        assert 'problem' in result
        assert 'eigenvalue' in result
        assert 'constant' in result
        assert 'verification_status' in result
    
    print("✓")


def test_export_framework():
    """Test framework export."""
    print("Testing framework export...", end=" ")
    framework = QCALUnifiedFramework()
    
    filename = '/tmp/test_qcal_framework.json'
    exported = framework.export_framework(filename)
    assert exported == filename
    
    # Verify file exists and is valid JSON
    with open(filename, 'r') as f:
        data = json.load(f)
    
    assert 'constants' in data
    assert 'problems' in data
    assert 'coherence' in data
    
    print("✓")


def test_verification_protocol():
    """Test cross-verification protocol."""
    print("Testing verification protocol...", end=" ")
    protocol = CrossVerificationProtocol()
    
    # Test individual verifiers
    result = protocol.verify_p_vs_np()
    assert 'status' in result
    assert 'accuracy' in result
    
    result = protocol.verify_riemann()
    assert 'status' in result
    assert 'accuracy' in result
    
    result = protocol.verify_ramsey()
    assert 'status' in result
    assert 'accuracy' in result
    
    print("✓")


def test_cross_verification():
    """Test full cross-verification."""
    print("Testing cross-verification...", end=" ")
    protocol = CrossVerificationProtocol()
    
    results = protocol.run_cross_verification()
    
    assert 'individual_results' in results
    assert 'consistency_matrix' in results
    assert 'qcal_coherence' in results
    assert 'unified_status' in results
    
    # Check coherence
    coherence = results['qcal_coherence']
    assert 'overall_coherence' in coherence
    assert 'is_coherent' in coherence
    
    print("✓")


def test_consistency_matrix():
    """Test consistency matrix construction."""
    print("Testing consistency matrix...", end=" ")
    protocol = CrossVerificationProtocol()
    
    # Get complete results for all problems
    results = {}
    for problem in protocol.framework.problems.keys():
        results[problem] = {'accuracy': 1.0, 'status': 'verified'}
    
    matrix = protocol.build_consistency_matrix(results)
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape[0] == matrix.shape[1]
    assert matrix.shape[0] == len(protocol.framework.problems)
    
    print("✓")


def test_verification_export():
    """Test verification report export."""
    print("Testing verification export...", end=" ")
    protocol = CrossVerificationProtocol()
    
    results = protocol.run_cross_verification()
    filename = '/tmp/test_verification_report.json'
    exported = protocol.export_verification_report(results, filename)
    
    assert exported == filename
    
    # Verify file exists and is valid JSON
    with open(filename, 'r') as f:
        data = json.load(f)
    
    assert 'individual_results' in data
    assert 'qcal_coherence' in data
    
    print("✓")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("QCAL UNIFIED FRAMEWORK TESTS")
    print("=" * 70)
    print()
    
    tests = [
        test_framework_initialization,
        test_universal_constants,
        test_operators,
        test_problem_connections,
        test_unify_problem,
        test_framework_coherence,
        test_demonstration,
        test_export_framework,
        test_verification_protocol,
        test_cross_verification,
        test_consistency_matrix,
        test_verification_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ - {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ - Unexpected error: {str(e)}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
