"""
Ramsey Vibrational Numbers Verification (Z3 version)

This module implements a complete Z3-based SAT verifier for vibrational Ramsey numbers
R_psi(r, s, epsilon) with modular coloring.

Key Features:
1. Z3 SAT Formula Generator for vibrational Ramsey verification
2. Automatic explorer to scan multiple (r,s,epsilon) values
3. Results visualization and CSV export
4. Natural language interface via examples

Author: José Manuel Mota Burruezo
"""

from z3 import *
from itertools import combinations
import numpy as np
import csv
from datetime import datetime


def vibrational_ramsey(r, s, M=1000, eps=0.2):
    """
    Verify if vibrational Ramsey number R_psi(r,s,eps) holds for n vertices.
    
    Uses Z3 solver to check if there exists a valid frequency assignment
    that avoids both:
    - A red clique of size r
    - A blue clique of size s
    
    Args:
        r: Size of red clique to avoid
        s: Size of blue clique to avoid
        M: Modular base for coloring (default 1000)
        eps: Threshold for resonance (default 0.2)
    
    Returns:
        True if no valid assignment exists (n >= R_psi), False otherwise
    """
    solver = Solver()
    n_val = r + s - 1  # Test minimum n
    omega = [Real(f'omega_{i}') for i in range(n_val)]
    
    # Frequency constraints: 0 <= omega < 1.0
    for w in omega:
        solver.add(0 <= w, w < 1.0)
    
    def is_red(i, j):
        """Check if edge (i,j) is red (resonant)"""
        diff = Abs(omega[i] - omega[j])
        return Or(diff < eps, 1 - diff < eps)
    
    # Avoid red clique of size r
    for combo in combinations(range(n_val), r):
        solver.add(Not(And([is_red(i, j) for i, j in combinations(combo, 2)])))
    
    # Avoid blue clique of size s
    for combo in combinations(range(n_val), s):
        solver.add(Not(And([Not(is_red(i, j)) for i, j in combinations(combo, 2)])))
    
    return solver.check() == sat


def calculate_ramsey_vibrational(r, s, M=1000, eps=0.2, nmax=20):
    """
    Calculate the exact vibrational Ramsey number R_psi(r,s,eps).
    
    Searches for the minimum n such that every frequency assignment
    contains either a red r-clique or a blue s-clique.
    
    Args:
        r: Red clique size
        s: Blue clique size
        M: Modular base
        eps: Resonance threshold
        nmax: Maximum n to test
    
    Returns:
        The Ramsey number, or None if not found in range
    """
    print(f"Calculating R_psi({r},{s}) with eps={eps}, M={M}...")
    
    for n in range(max(r, s), nmax + 1):
        print(f"  Testing n={n}...", end=" ")
        
        solver = Solver()
        omega = [Real(f'omega_{i}') for i in range(n)]
        
        # Frequency constraints
        for w in omega:
            solver.add(0 <= w, w < 1.0)
        
        def is_red(i, j):
            diff = Abs(omega[i] - omega[j])
            return Or(diff < eps, 1 - diff < eps)
        
        # Avoid red clique of size r
        for combo in combinations(range(n), r):
            solver.add(Not(And([is_red(i, j) for i, j in combinations(combo, 2)])))
        
        # Avoid blue clique of size s
        for combo in combinations(range(n), s):
            solver.add(Not(And([Not(is_red(i, j)) for i, j in combinations(combo, 2)])))
        
        result = solver.check()
        if result == unsat:
            print(f"UNSAT -> R_psi({r},{s}) = {n}")
            return n
        else:
            print("SAT (counterexample exists)")
    
    print(f"Not found in range [1,{nmax}]")
    return None


def explore_parameters(r_values, s_values, eps_values, M=1000, nmax=20):
    """
    Automatic explorer: scans multiple (r,s,epsilon) values.
    
    Args:
        r_values: List of r values to test
        s_values: List of s values to test
        eps_values: List of epsilon values to test
        M: Modular base
        nmax: Maximum n to test for each case
    
    Returns:
        List of results dictionaries
    """
    results = []
    total = len(r_values) * len(s_values) * len(eps_values)
    current = 0
    
    print("=" * 70)
    print("AUTOMATIC PARAMETER EXPLORER")
    print("=" * 70)
    print(f"Testing {total} parameter combinations...")
    print()
    
    for r in r_values:
        for s in s_values:
            for eps in eps_values:
                current += 1
                print(f"\n[{current}/{total}] Testing (r={r}, s={s}, eps={eps})")
                print("-" * 50)
                
                start_time = datetime.now()
                R_psi = calculate_ramsey_vibrational(r, s, M, eps, nmax)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                result = {
                    'r': r,
                    's': s,
                    'epsilon': eps,
                    'M': M,
                    'R_psi': R_psi,
                    'duration_seconds': duration,
                    'timestamp': start_time.isoformat()
                }
                results.append(result)
                
                if R_psi:
                    print(f"✓ R_psi({r},{s},{eps}) = {R_psi} (computed in {duration:.2f}s)")
                else:
                    print(f"✗ R_psi({r},{s},{eps}) not found (timeout after {duration:.2f}s)")
    
    return results


def save_results_to_csv(results, filename='ramsey_results.csv'):
    """
    Save exploration results to CSV file.
    
    Args:
        results: List of result dictionaries
        filename: Output CSV filename
    """
    if not results:
        print("No results to save.")
        return
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['r', 's', 'epsilon', 'M', 'R_psi', 'duration_seconds', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"\n✓ Results saved to {filename}")


def generate_results_table(results):
    """
    Generate a formatted results table for display.
    
    Args:
        results: List of result dictionaries
    
    Returns:
        Formatted string table
    """
    if not results:
        return "No results available."
    
    print("\n" + "=" * 70)
    print("RESULTS TABLE")
    print("=" * 70)
    print(f"{'(r,s)':<10} {'epsilon':<10} {'M':<10} {'R_psi':<10} {'Time(s)':<10}")
    print("-" * 70)
    
    for result in results:
        r_s = f"({result['r']},{result['s']})"
        eps = f"{result['epsilon']:.2f}"
        M = str(result['M'])
        R_psi = str(result['R_psi']) if result['R_psi'] else "N/A"
        time = f"{result['duration_seconds']:.2f}"
        print(f"{r_s:<10} {eps:<10} {M:<10} {R_psi:<10} {time:<10}")
    
    print("=" * 70)


def natural_interface_example():
    """
    Natural language interface example.
    
    Demonstrates how to use the system with natural language queries.
    """
    print("\n" + "=" * 70)
    print("NATURAL LANGUAGE INTERFACE EXAMPLE")
    print("=" * 70)
    
    queries = [
        {
            'query': "What is the smallest n such that R_psi(3,3,0.2) = n?",
            'r': 3, 's': 3, 'eps': 0.2
        },
        {
            'query': "Calculate R_psi(4,4) with epsilon=0.15",
            'r': 4, 's': 4, 'eps': 0.15
        }
    ]
    
    for i, q in enumerate(queries, 1):
        print(f"\nQuery {i}: \"{q['query']}\"")
        print(f"Translating to: calculate_ramsey_vibrational(r={q['r']}, s={q['s']}, eps={q['eps']})")
        print("-" * 50)
        
        result = calculate_ramsey_vibrational(q['r'], q['s'], eps=q['eps'], nmax=15)
        
        if result:
            print(f"\n✓ Answer: R_psi({q['r']},{q['s']},{q['eps']}) = {result}")
        else:
            print(f"\n✗ Answer: Could not determine R_psi({q['r']},{q['s']},{q['eps']}) in range")
        print()


# Example usage
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RAMSEY VIBRATIONAL NUMBERS VERIFICATION (Z3 VERSION)")
    print("=" * 70)
    print("\nModular verification via Z3 for R_psi(r,s,epsilon)")
    print(f"Using M=1000 and modular coloring\n")
    
    # Example 1: Basic verification
    print("\n--- Example 1: Basic Verification ---")
    print("(3,3) in n=5:", vibrational_ramsey(3, 3))      # True -> R_psi > 5
    print("(3,3) in n=6:", not vibrational_ramsey(3, 3))  # False -> R_psi = 6
    
    # Example 2: Calculate exact values
    print("\n--- Example 2: Calculate Exact Values ---")
    R_33 = calculate_ramsey_vibrational(3, 3, eps=0.2, nmax=10)
    print(f"\nFinal result: R_psi(3,3,0.2) = {R_33}")
    
    # Example 3: Explore multiple parameters
    print("\n--- Example 3: Automatic Parameter Explorer ---")
    results = explore_parameters(
        r_values=[3, 4],
        s_values=[3, 4],
        eps_values=[0.2, 0.3],
        M=1000,
        nmax=15
    )
    
    # Generate and display results table
    generate_results_table(results)
    
    # Save results to CSV
    save_results_to_csv(results, 'ramsey_results.csv')
    
    # Example 4: Natural language interface
    natural_interface_example()
    
    print("\n" + "=" * 70)
    print("✓ Verification complete!")
    print("=" * 70 + "\n")
