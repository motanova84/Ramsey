#!/usr/bin/env python3
"""
Test script for SAT-based Ramsey resonance implementation
Tests small instances to verify correctness
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generate_rpsi_sat import generate_rpsi_sat_instance_tseytin, generate_dimacs
from solve_rpsi_sat import solve_cnf


def test_small_instance():
    """Test R_ψ(3,3) ≤ 6"""
    print("="*60)
    print("Test 1: R_ψ(3,3) ≤ 6")
    print("="*60)
    
    # Generate CNF
    print("\n[1/3] Generating CNF...")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n=6, r=3, s=3, f0=141.7001, eps=0.037, grid=128
    )
    print(f"  Variables: {num_vars}")
    print(f"  Clauses: {num_clauses}")
    
    # Write to file
    cnf_file = "data/test_rpsi_3_3_n6.cnf"
    with open(cnf_file, 'w') as f:
        f.write(f"c Test: R_ψ(3,3) ≤ 6\n")
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"  Saved to: {cnf_file}")
    
    # Solve
    print("\n[2/3] Solving with Z3...")
    result, model = solve_cnf(cnf_file, solver="z3")
    
    print(f"\n[3/3] Result: {result}")
    
    # Verify
    if result == "UNSAT":
        print("  ✓ PASS: R_ψ(3,3) ≤ 6 is proven!")
        return True
    else:
        print("  ✗ FAIL: Expected UNSAT but got", result)
        return False


def test_trivial_sat():
    """Test that R_ψ(3,3) > 3 (should be SAT)"""
    print("\n" + "="*60)
    print("Test 2: R_ψ(3,3) > 3 (should find valid coloring)")
    print("="*60)
    
    # Generate CNF for n=3
    print("\n[1/3] Generating CNF for n=3...")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n=3, r=3, s=3, f0=141.7001, eps=0.037, grid=128
    )
    print(f"  Variables: {num_vars}")
    print(f"  Clauses: {num_clauses}")
    
    # Write to file
    cnf_file = "data/test_rpsi_3_3_n3.cnf"
    with open(cnf_file, 'w') as f:
        f.write(f"c Test: R_ψ(3,3) > 3\n")
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"  Saved to: {cnf_file}")
    
    # Solve
    print("\n[2/3] Solving with Z3...")
    result, model = solve_cnf(cnf_file, solver="z3")
    
    print(f"\n[3/3] Result: {result}")
    
    # Verify
    if result == "SAT":
        print("  ✓ PASS: Found valid coloring for n=3!")
        return True
    else:
        print("  ✗ FAIL: Expected SAT but got", result)
        return False


def test_consistency():
    """Test that generated CNF has correct structure"""
    print("\n" + "="*60)
    print("Test 3: CNF Structure Consistency")
    print("="*60)
    
    n, r, s = 5, 3, 3
    grid = 128
    
    print(f"\n[1/2] Generating CNF for n={n}, r={r}, s={s}...")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n, r, s, f0=141.7001, eps=0.037, grid=grid
    )
    
    # Check variable count
    expected_min_vars = n * grid  # At least frequency variables
    if num_vars < expected_min_vars:
        print(f"  ✗ FAIL: Too few variables: {num_vars} < {expected_min_vars}")
        return False
    
    print(f"  Variables: {num_vars} (≥ {expected_min_vars}) ✓")
    
    # Check clause count
    expected_min_clauses = n  # At least one clause per vertex (at least one freq)
    if num_clauses < expected_min_clauses:
        print(f"  ✗ FAIL: Too few clauses: {num_clauses} < {expected_min_clauses}")
        return False
    
    print(f"  Clauses: {num_clauses} (≥ {expected_min_clauses}) ✓")
    
    # Check all clauses are valid
    print("\n[2/2] Validating clause structure...")
    invalid_clauses = 0
    for i, clause in enumerate(clauses):
        # Check no zero literals (except line terminator)
        if 0 in clause:
            invalid_clauses += 1
        # Check all literals are in valid range
        for lit in clause:
            if abs(lit) > num_vars:
                print(f"  ✗ Clause {i}: Literal {lit} exceeds num_vars {num_vars}")
                invalid_clauses += 1
    
    if invalid_clauses > 0:
        print(f"  ✗ FAIL: Found {invalid_clauses} invalid clauses")
        return False
    
    print(f"  All {num_clauses} clauses are valid ✓")
    print("  ✓ PASS: CNF structure is consistent!")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SAT-Based Ramsey Resonance Implementation Tests")
    print("="*60 + "\n")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    results = []
    
    # Run tests
    try:
        results.append(("Structure Consistency", test_consistency()))
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results.append(("Structure Consistency", False))
    
    try:
        results.append(("R_ψ(3,3) ≤ 6 (UNSAT)", test_small_instance()))
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results.append(("R_ψ(3,3) ≤ 6 (UNSAT)", False))
    
    try:
        results.append(("R_ψ(3,3) > 3 (SAT)", test_trivial_sat()))
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results.append(("R_ψ(3,3) > 3 (SAT)", False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
