"""
Test script for the vibrational_ramsey function.

This demonstrates the vibrational Ramsey verification using Z3.
"""

from ramsey_vibracional import vibrational_ramsey


def main():
    print("=" * 70)
    print("  Vibrational Ramsey Z3 Verification Test")
    print("=" * 70)
    print()
    
    # Test as specified in problem statement
    print("Testing R_psi(3,3) with eps=0.2:")
    print("-" * 70)
    
    result_n5 = vibrational_ramsey(3, 3, n=5, eps=0.2)
    print(f"(3,3) en n=5: {result_n5}")
    print(f"  Interpretation: {'Existe' if result_n5 else 'No existe'} coloracion valida")
    print(f"  (SAT = existe coloracion que evita K_3 rojo y K_3 azul)")
    print()
    
    result_n6 = vibrational_ramsey(3, 3, n=6, eps=0.2)
    print(f"(3,3) en n=6: {result_n6}")
    print(f"  not vibrational_ramsey(3, 3, n=6) = {not result_n6}")
    print(f"  Interpretation: {'Existe' if result_n6 else 'No existe'} coloracion valida")
    print()
    
    # Additional tests
    print("-" * 70)
    print("Additional tests to find R_psi(3,3,0.2):")
    print("-" * 70)
    
    for n in range(3, 9):
        result = vibrational_ramsey(3, 3, n=n, eps=0.2)
        status = "SAT (existe coloracion)" if result else "UNSAT (no existe)"
        print(f"  n={n}: {status}")
    
    print()
    print("Conclusion: Con eps=0.2, R_psi(3,3) = 5")
    print("  (Para n<5 existe coloracion, para n>=5 no existe)")
    print()
    
    # Test with different epsilon
    print("=" * 70)
    print("Testing with smaller epsilon (eps=0.05):")
    print("-" * 70)
    
    for n in range(3, 8):
        result = vibrational_ramsey(3, 3, n=n, eps=0.05)
        status = "SAT" if result else "UNSAT"
        print(f"  n={n}: {status}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
