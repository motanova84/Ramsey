#!/usr/bin/env python3
"""
Example: Using AI-Ramsey-Formal for automated certification

This script demonstrates how to use the AI-Ramsey-Formal CLI tool
both from the command line and programmatically.
"""

from ai_ramsey_formal import certify
import json


def example_programmatic_usage():
    """
    Example of using the certify function directly in Python code
    """
    print("=" * 70)
    print("Example 1: Programmatic usage")
    print("=" * 70)
    
    # Certify R_psi(3,3)
    result = certify(
        r=3,
        s=3,
        lam=0.037,
        f0=141.7001,
        nmax=15,
        grid=64,
        output_dir="./certifications"
    )
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    return result


def example_multiple_certifications():
    """
    Example of certifying multiple Ramsey numbers
    """
    print("\n" + "=" * 70)
    print("Example 2: Multiple certifications")
    print("=" * 70)
    
    cases = [
        (3, 3),
        (3, 4),
        (4, 4),
    ]
    
    results = []
    for r, s in cases:
        print(f"\nCertifying R_psi({r},{s})...")
        result = certify(
            r=r,
            s=s,
            lam=0.037,
            f0=141.7001,
            nmax=20,
            grid=64,
            output_dir=f"./certifications/case_{r}_{s}"
        )
        
        if 'bound' in result:
            results.append({
                'r': r,
                's': s,
                'bound': result['bound']
            })
            print(f"✓ R_psi({r},{s}) <= {result['bound']}")
    
    print("\n" + "=" * 70)
    print("Summary of certifications:")
    print("=" * 70)
    for res in results:
        print(f"  R_psi({res['r']},{res['s']}) <= {res['bound']}")
    
    return results


def example_custom_parameters():
    """
    Example of using custom vibrational parameters
    """
    print("\n" + "=" * 70)
    print("Example 3: Custom vibrational parameters")
    print("=" * 70)
    
    # Use tighter coherence threshold
    result = certify(
        r=3,
        s=3,
        lam=0.001,  # Tighter coherence
        f0=141.7001,
        nmax=20,
        grid=128,  # Higher resolution
        output_dir="./certifications/tight_coherence"
    )
    
    if 'bound' in result:
        print(f"\n✓ With lambda=0.001: R_psi(3,3) <= {result['bound']}")
        print(f"  (Compare with lambda=0.037 which typically gives a smaller bound)")
    
    return result


def main():
    """
    Run all examples
    """
    print("\n" + "=" * 70)
    print("AI-Ramsey-Formal: Automated Certification Examples")
    print("=" * 70)
    
    print("\nThese examples show how to:")
    print("  1. Use the certify function programmatically")
    print("  2. Certify multiple Ramsey numbers in batch")
    print("  3. Customize vibrational parameters")
    print()
    
    input("Press Enter to start examples...")
    
    # Run examples
    example_programmatic_usage()
    
    example_multiple_certifications()
    
    example_custom_parameters()
    
    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
    print("\nGenerated files are in ./certifications/")
    print("\nTry from command line:")
    print("  python ai_ramsey_formal.py 5 5 --lam=0.037")


if __name__ == "__main__":
    main()
