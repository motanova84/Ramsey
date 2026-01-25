#!/usr/bin/env python
"""
Basic Examples of Parameterized Ramsey Theory (R_Λ)

This script demonstrates how to use the ramsey_lambda.sage module
to compute Ramsey numbers with different Lambda parameters.
"""

import subprocess
import sys


def run_example(name, r, s, lam, extra_args=None):
    """Run an example computation"""
    print("\n" + "=" * 70)
    print(f"Example: {name}")
    print("=" * 70)
    
    cmd = ['python', 'ramsey_lambda.sage', 
           f'--r={r}', f'--s={s}', f'--lam={lam}']
    
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("Parameterized Ramsey Theory - Basic Examples")
    print("=" * 70)
    print("\nThese examples demonstrate R_Λ(r,s) computation with")
    print("different Lambda parameters Λ = [0,λ) ⊂ [0,1)")
    print()
    
    examples = [
        {
            "name": "Small Case - R_Λ(3,3)",
            "description": "Classical R(3,3) = 6, let's see if R_Λ < 6",
            "r": 3, "s": 3, "lam": 0.1
        },
        {
            "name": "Asymmetric Case - R_Λ(3,4)",
            "description": "Classical R(3,4) = 9",
            "r": 3, "s": 4, "lam": 0.1
        },
        {
            "name": "Larger Case - R_Λ(4,4)",
            "description": "Classical R(4,4) = 18, expect significant reduction",
            "r": 4, "s": 4, "lam": 0.05
        },
        {
            "name": "Different Lambda - R_Λ(3,3) with λ=0.05",
            "description": "Testing smaller lambda value",
            "r": 3, "s": 3, "lam": 0.05
        },
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"Example {i}/{len(examples)}: {ex['name']}")
        print(f"Description: {ex['description']}")
        print(f"{'='*70}")
        
        input("\nPress Enter to run this example...")
        
        returncode = run_example(
            ex['name'],
            ex['r'], ex['s'], ex['lam']
        )
        
        if returncode != 0:
            print(f"\nWarning: Example failed with return code {returncode}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "=" * 70)
    print("Examples Complete")
    print("=" * 70)
    print("\nKey Observations:")
    print("1. R_Λ(r,s) ≤ R(r,s) for all lambda (Theorem A)")
    print("2. Smaller lambda generally gives better bounds")
    print("3. Results are deterministic and reproducible")
    print("4. Certificates can be generated with --certify flag")
    print("\nFor more options, run:")
    print("  python ramsey_lambda.sage --help")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
        sys.exit(0)
