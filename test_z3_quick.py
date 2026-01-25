"""
Quick test script for Z3 verification with minimal parameters
"""

from ramsey_z3_verification import vibrational_ramsey, calculate_ramsey_vibrational

print("\n" + "=" * 70)
print("QUICK TEST: Z3 Vibrational Ramsey Verification")
print("=" * 70)

# Test 1: Basic verification with (3,3)
print("\nTest 1: Basic verification (3,3) with eps=0.2")
print("-" * 50)
result = vibrational_ramsey(3, 3, eps=0.2)
print(f"Result for n=5: {result} (SAT means counterexample exists)")

# Test 2: Calculate with smaller nmax
print("\nTest 2: Calculate R_psi(3,3) with eps=0.3 (larger epsilon for faster computation)")
print("-" * 50)
result = calculate_ramsey_vibrational(3, 3, eps=0.3, nmax=10)
print(f"\nFinal: R_psi(3,3,0.3) = {result}")

print("\n" + "=" * 70)
print("✓ Quick test completed!")
print("=" * 70 + "\n")
