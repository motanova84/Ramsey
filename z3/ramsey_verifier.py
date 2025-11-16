#!/usr/bin/env python3
"""
Ramsey Verifier - Z3-based verification tool for Vibrational Ramsey Theory

This script provides Z3-based verification of the vibrational Ramsey numbers R_psi(r,s,eps).
It uses SMT solving to compute exact values and validate theoretical predictions.

Usage:
    python ramsey_verifier.py --r 3 --s 3 --M 1000 --eps 0.2
    python ramsey_verifier.py --r 3 --s 4 --nmax 30 --grid 128
    
Author: José Manuel Mota Burruezo
License: MIT
"""

import argparse
import sys
from z3 import *
from itertools import combinations


def vibrational_ramsey_unsat(n, r, s, eps=0.001, f0=141.7001, grid=128):
    """
    Verify if n >= R_psi(r,s,eps) using Z3 SAT solver.
    
    Returns True if UNSAT (no valid frequency assignment exists),
    meaning n is at least R_psi(r,s,eps).
    
    Args:
        n: Number of vertices
        r: Target size for blue clique
        s: Target size for red clique
        eps: Coherence threshold (default: 0.001 Hz)
        f0: Base frequency (default: 141.7001 Hz)
        grid: Discretization resolution (default: 128)
        
    Returns:
        bool: True if UNSAT (n >= R_psi(r,s,eps)), False if SAT
    """
    solver = Solver()
    
    # Discretized frequency variables: omega_i = k_i * (f0/grid) where k_i in [0, grid)
    k = [Int(f"k_{i}") for i in range(n)]
    
    # Constraint: all k_i values in valid range
    for ki in k:
        solver.add(And(ki >= 0, ki < grid))
    
    # Symmetry breaking: order frequencies
    for i in range(n-1):
        solver.add(k[i] <= k[i+1])
    
    # Frequency expressions
    omega = [(f0 * ki) / grid for ki in k]
    
    def is_blue_resonant(i, j):
        """
        Resonance predicate: |omega_i - omega_j| mod f0 <= eps
        
        Handles modular arithmetic with three cases:
        - Direct difference: omega_j - omega_i in [-eps, eps]
        - Upper wrap: (omega_j - omega_i) - f0 in [-eps, eps]
        - Lower wrap: (omega_j - omega_i) + f0 in [-eps, eps]
        """
        dij = omega[j] - omega[i]
        eps_grid = (eps * grid) / f0  # eps in grid units
        
        return Or(
            And(dij >= -eps_grid, dij <= eps_grid),        # Direct case
            And(dij - grid >= -eps_grid, dij - grid <= eps_grid),  # Wrap +
            And(dij + grid >= -eps_grid, dij + grid <= eps_grid)   # Wrap -
        )
    
    # ABSENCE of K_r blue: for each r-subset, at least one edge is NOT resonant
    for S in combinations(range(n), r):
        edges = [(S[i], S[j]) for i in range(r) for j in range(i+1, r)]
        # Negate: NOT all edges are blue
        solver.add(Or([Not(is_blue_resonant(i, j)) for (i, j) in edges]))
    
    # ABSENCE of K_s red: for each s-subset, at least one edge IS resonant
    # (because red = non-blue = non-resonant)
    for T in combinations(range(n), s):
        edges = [(T[i], T[j]) for i in range(s) for j in range(i+1, s)]
        # Negate: NOT all edges are red (i.e., at least one is blue)
        solver.add(Or([is_blue_resonant(i, j) for (i, j) in edges]))
    
    # Check satisfiability
    result = solver.check()
    return result == unsat


def compute_R_psi(r, s, eps=0.001, f0=141.7001, nmax=25, grid=128, verbose=True):
    """
    Compute R_psi(r,s,eps) exactly via SAT search.
    
    Args:
        r: Blue clique size
        s: Red clique size
        eps: Coherence threshold
        f0: Base frequency (141.7001 Hz)
        nmax: Maximum n to check
        grid: Discretization resolution
        verbose: Print progress messages
        
    Returns:
        int: R_psi(r,s,eps) if found, None otherwise
    """
    if verbose:
        print(f"Computing R_psi({r},{s},{eps}) with f0={f0} Hz, grid={grid}")
    
    for n in range(max(r, s), nmax + 1):
        if verbose:
            print(f"  Testing n={n}...", end=" ", flush=True)
        
        if vibrational_ramsey_unsat(n, r, s, eps, f0, grid):
            if verbose:
                print(f"UNSAT -> R_psi({r},{s}) = {n}")
            return n
        else:
            if verbose:
                print("SAT (counterexample exists)")
    
    if verbose:
        print(f"Not found in range [1,{nmax}]")
    return None


def estimate_conjecture(r, s, f0=141.7001):
    """
    Theoretical estimate based on Conjecture 3.4.
    
    R_psi(r,s,eps) = O(sqrt(rs) * ln(rs))
    
    Uses the golden ratio phi = 1.618... as empirical constant.
    
    Args:
        r: Blue clique size
        s: Red clique size
        f0: Base frequency
        
    Returns:
        int: Estimated R_psi(r,s)
    """
    import math
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    if r * s == 0:
        return 0
    # Empirically calibrated formula
    value = 0.5 * phi * math.sqrt(r * s) * math.log(max(r * s, 2))
    return max(int(value), max(r, s))


def verify_table(cases, eps=0.001, f0=141.7001, grid=128):
    """
    Verify a table of (r,s) cases.
    
    Args:
        cases: List of (r,s) tuples to verify
        eps: Coherence threshold
        f0: Base frequency
        grid: Resolution
        
    Returns:
        dict: Results dictionary with computed values
    """
    results = {}
    
    print("\n" + "="*70)
    print("Verification: SAT Reality vs Theoretical Conjecture")
    print("="*70 + "\n")
    
    for r, s in cases:
        R_psi_real = compute_R_psi(r, s, eps, f0, nmax=30, grid=grid, verbose=True)
        R_psi_theory = estimate_conjecture(r, s, f0)
        
        if R_psi_real:
            error = abs(R_psi_real - R_psi_theory) / R_psi_real * 100
            print(f"  ({r},{s}): Real={R_psi_real}, Theory={R_psi_theory}, Error={error:.1f}%\n")
            results[(r, s)] = {
                'real': R_psi_real,
                'theory': R_psi_theory,
                'error': error
            }
        else:
            print(f"  ({r},{s}): Real=?, Theory={R_psi_theory}\n")
            results[(r, s)] = {
                'real': None,
                'theory': R_psi_theory,
                'error': None
            }
    
    # Compute average error
    errors = [res['error'] for res in results.values() if res['error'] is not None]
    if errors:
        avg_error = sum(errors) / len(errors)
        print("="*70)
        print(f"Average error of Conjecture 3.4: {avg_error:.1f}%")
        print("="*70 + "\n")
    
    return results


def main():
    """Main entry point for the verifier."""
    parser = argparse.ArgumentParser(
        description='Vibrational Ramsey Verifier - Z3-based exact computation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compute R_psi(3,3) with default parameters
  python ramsey_verifier.py --r 3 --s 3
  
  # High-precision computation with custom threshold
  python ramsey_verifier.py --r 3 --s 4 --M 1000 --eps 0.2 --grid 256
  
  # Verify multiple cases
  python ramsey_verifier.py --verify-table
        """
    )
    
    parser.add_argument('--r', type=int, help='Blue clique size')
    parser.add_argument('--s', type=int, help='Red clique size')
    parser.add_argument('--M', '--nmax', type=int, default=25, dest='nmax',
                       help='Maximum n to search (default: 25)')
    parser.add_argument('--eps', type=float, default=0.001,
                       help='Coherence threshold (default: 0.001)')
    parser.add_argument('--f0', type=float, default=141.7001,
                       help='Base frequency in Hz (default: 141.7001)')
    parser.add_argument('--grid', type=int, default=128,
                       help='Discretization resolution (default: 128)')
    parser.add_argument('--verify-table', action='store_true',
                       help='Verify standard table of values')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress messages')
    
    args = parser.parse_args()
    
    # Handle table verification mode
    if args.verify_table:
        cases = [(3,3), (3,4), (4,4), (3,5), (4,5)]
        verify_table(cases, args.eps, args.f0, args.grid)
        return 0
    
    # Require r and s for single computation
    if args.r is None or args.s is None:
        parser.print_help()
        print("\nError: --r and --s are required (or use --verify-table)")
        return 1
    
    # Compute single value
    result = compute_R_psi(
        args.r, args.s,
        eps=args.eps,
        f0=args.f0,
        nmax=args.nmax,
        grid=args.grid,
        verbose=not args.quiet
    )
    
    if result:
        print(f"\nResult: R_psi({args.r},{args.s}) = {result}")
        theory = estimate_conjecture(args.r, args.s, args.f0)
        error = abs(result - theory) / result * 100
        print(f"Theoretical estimate: {theory} (error: {error:.1f}%)")
        return 0
    else:
        print(f"\nR_psi({args.r},{args.s}) not found in range [1,{args.nmax}]")
        print("Try increasing --M (nmax) parameter")
        return 1


if __name__ == "__main__":
    sys.exit(main())
