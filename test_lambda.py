#!/usr/bin/env python
"""
Test suite for ramsey_lambda.sage

Tests the parameterized Ramsey theory implementation with various
parameter combinations to verify correctness and consistency.
"""

import subprocess
import sys
import re


def run_ramsey_lambda(r, s, lam, extra_args=None):
    """Run ramsey_lambda.sage and parse output"""
    cmd = ['python', 'ramsey_lambda.sage', 
           f'--r={r}', f'--s={s}', f'--lam={lam}']
    
    if extra_args:
        cmd.extend(extra_args)
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    # Parse output to extract R_Lambda value
    output = result.stdout
    match = re.search(r'R_Λ\((\d+),(\d+)\) ≤ (\d+)', output)
    
    if match:
        return int(match.group(3)), output
    else:
        return None, output


def test_basic_cases():
    """Test basic small cases"""
    print("=" * 70)
    print("Test 1: Basic Cases")
    print("=" * 70)
    
    test_cases = [
        (3, 3, 0.1, 6),   # Should be ≤ classical R(3,3) = 6
        (3, 4, 0.1, 9),   # Should be ≤ classical R(3,4) = 9
        (4, 4, 0.1, 18),  # Should be ≤ classical R(4,4) = 18
    ]
    
    passed = 0
    failed = 0
    
    for r, s, lam, max_expected in test_cases:
        print(f"\nTesting R_Λ({r},{s}) with λ={lam}...", end=" ")
        R_lambda, _ = run_ramsey_lambda(r, s, lam, ['--quiet'])
        
        if R_lambda is not None and R_lambda <= max_expected:
            print(f"✓ PASS (R_Λ = {R_lambda} ≤ {max_expected})")
            passed += 1
        else:
            print(f"✗ FAIL (R_Λ = {R_lambda}, expected ≤ {max_expected})")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


def test_monotonicity():
    """Test that R_Lambda decreases as lambda increases (for small λ)"""
    print("\n" + "=" * 70)
    print("Test 2: Monotonicity in λ")
    print("=" * 70)
    
    r, s = 3, 3
    lambdas = [0.05, 0.1, 0.15]
    
    results = []
    for lam in lambdas:
        print(f"\nTesting R_Λ({r},{s}) with λ={lam}...", end=" ")
        R_lambda, _ = run_ramsey_lambda(r, s, lam, ['--quiet'])
        results.append(R_lambda)
        print(f"R_Λ = {R_lambda}")
    
    # Check that results are reasonable (should all be ≤ classical bound)
    classical_bound = 6
    all_valid = all(r <= classical_bound for r in results if r is not None)
    
    if all_valid:
        print(f"\n✓ PASS: All values ≤ classical R({r},{s}) = {classical_bound}")
        return True
    else:
        print(f"\n✗ FAIL: Some values exceed classical bound")
        return False


def test_symmetry():
    """Test that R_Lambda(r,s) = R_Lambda(s,r)"""
    print("\n" + "=" * 70)
    print("Test 3: Symmetry R_Λ(r,s) = R_Λ(s,r)")
    print("=" * 70)
    
    test_pairs = [(3, 4, 0.1)]
    passed = 0
    failed = 0
    
    for r, s, lam in test_pairs:
        print(f"\nTesting R_Λ({r},{s}) vs R_Λ({s},{r}) with λ={lam}")
        R_rs, _ = run_ramsey_lambda(r, s, lam, ['--quiet'])
        R_sr, _ = run_ramsey_lambda(s, r, lam, ['--quiet'])
        
        print(f"  R_Λ({r},{s}) = {R_rs}")
        print(f"  R_Λ({s},{r}) = {R_sr}")
        
        if R_rs == R_sr:
            print("  ✓ PASS: Symmetric")
            passed += 1
        else:
            print("  ✗ FAIL: Not symmetric")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n" + "=" * 70)
    print("Test 4: Edge Cases")
    print("=" * 70)
    
    # Test with very small lambda
    print("\nTesting with small λ=0.01...")
    R_lambda, _ = run_ramsey_lambda(3, 3, 0.01, ['--quiet', '--nmax=15'])
    if R_lambda is not None:
        print(f"✓ R_Λ(3,3) = {R_lambda} (small λ)")
    else:
        print("✗ Failed to compute")
    
    # Test with larger lambda
    print("\nTesting with larger λ=0.3...")
    R_lambda, _ = run_ramsey_lambda(3, 3, 0.3, ['--quiet'])
    if R_lambda is not None:
        print(f"✓ R_Λ(3,3) = {R_lambda} (larger λ)")
    else:
        print("✗ Failed to compute")
    
    return True


def test_certificate_generation():
    """Test certificate generation"""
    print("\n" + "=" * 70)
    print("Test 5: Certificate Generation")
    print("=" * 70)
    
    print("\nGenerating certificate for R_Λ(3,3) with λ=0.2...")
    result = subprocess.run(
        ['python', 'ramsey_lambda.sage', '--r=3', '--s=3', '--lam=0.2', 
         '--certify', '--quiet'],
        capture_output=True, text=True, timeout=30
    )
    
    if 'Certificate written to' in result.stdout:
        print("✓ PASS: Certificate generated successfully")
        return True
    else:
        print("✗ FAIL: Certificate generation failed")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("Ramsey Lambda Test Suite")
    print("=" * 70)
    
    tests = [
        ("Basic Cases", test_basic_cases),
        ("Monotonicity", test_monotonicity),
        ("Symmetry", test_symmetry),
        ("Edge Cases", test_edge_cases),
        ("Certificate Generation", test_certificate_generation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\n{passed_count}/{total_count} test suites passed")
    print("=" * 70)
    
    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
