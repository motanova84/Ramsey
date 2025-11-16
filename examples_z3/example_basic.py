"""
Basic Example: Z3 Verification of Vibrational Ramsey Numbers

This example demonstrates basic usage of the Z3 verification system.
"""

import sys
sys.path.insert(0, '..')

from ramsey_z3_verification import vibrational_ramsey, calculate_ramsey_vibrational


def example_1_basic_check():
    """Example 1: Check if specific n satisfies Ramsey property"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Verification")
    print("=" * 70)
    print("\nChecking if (3,3) holds for different n values with epsilon=0.2:\n")
    
    for n in [4, 5, 6, 7]:
        # Test for specific n by passing it to vibrational_ramsey
        result = vibrational_ramsey(3, 3, n=n, eps=0.2)
        status = "SAT (counterexample exists)" if result else "UNSAT (no valid assignment)"
        print(f"  n={n}: {status}")
    
    print("\nInterpretation:")
    print("  - SAT means a valid frequency assignment exists (n < R_psi)")
    print("  - UNSAT means no valid assignment exists (n >= R_psi)")


def example_2_calculate_exact():
    """Example 2: Calculate exact Ramsey number"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Calculate Exact R_psi")
    print("=" * 70)
    
    cases = [
        (3, 3, 0.2),
        (3, 4, 0.2),
        (4, 4, 0.2),
    ]
    
    print("\nCalculating exact vibrational Ramsey numbers:\n")
    
    for r, s, eps in cases:
        print(f"\nCase: R_psi({r},{s},{eps})")
        print("-" * 50)
        result = calculate_ramsey_vibrational(r, s, eps=eps, nmax=12)
        
        if result:
            print(f"✓ R_psi({r},{s},{eps}) = {result}")
        else:
            print(f"✗ R_psi({r},{s},{eps}) not found (needs larger nmax)")


def example_3_epsilon_variation():
    """Example 3: How epsilon affects R_psi"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Epsilon Sensitivity")
    print("=" * 70)
    print("\nTesting how epsilon affects R_psi(3,3):\n")
    
    epsilon_values = [0.15, 0.2, 0.25, 0.3]
    
    print(f"{'Epsilon':<10} {'R_psi(3,3)':<15}")
    print("-" * 30)
    
    for eps in epsilon_values:
        result = calculate_ramsey_vibrational(3, 3, eps=eps, nmax=12)
        result_str = str(result) if result else "N/A"
        print(f"{eps:<10.2f} {result_str:<15}")
    
    print("\nObservation:")
    print("  Larger epsilon typically leads to smaller R_psi values")
    print("  (More edges are considered 'red', making cliques easier to form)")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RAMSEY Z3 VERIFICATION: BASIC EXAMPLES")
    print("=" * 70)
    
    # Run examples
    example_1_basic_check()
    example_2_calculate_exact()
    example_3_epsilon_variation()
    
    print("\n" + "=" * 70)
    print("✓ All basic examples completed!")
    print("=" * 70 + "\n")
