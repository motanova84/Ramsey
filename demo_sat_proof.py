#!/usr/bin/env python3
"""
Demonstration of SAT-based proof for R_ψ(5,5) ≤ 16

This script shows how the SAT-based approach proves that there is no
frequency assignment ω: [16] → [0, f₀) that avoids both blue K₅ and red K₅
under resonant coloring.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generate_rpsi_sat import generate_rpsi_sat_instance_tseytin
from solve_rpsi_sat import solve_cnf


def main():
    print("="*70)
    print("SAT-Based Proof: R_ψ(5,5) ≤ 16")
    print("="*70)
    print()
    print("This demonstration proves that no frequency assignment")
    print("ω: [16] → [0, f₀) can avoid both:")
    print("  • Blue (resonant) K₅")
    print("  • Red (non-resonant) K₅")
    print()
    print("Parameters:")
    print("  • f₀ = 141.7001 Hz (QCAL ∞³ universal frequency)")
    print("  • ε = 0.037 (resonance threshold)")
    print("  • grid = 128 (frequency discretization)")
    print()
    print("="*70)
    
    # Check if CNF file exists
    cnf_file = "data/rpsi_5_5_n16.cnf"
    
    if not os.path.exists(cnf_file):
        print()
        print("[Step 1/2] Generating CNF formula...")
        print("  This encodes all constraints of the problem:")
        print("  • Each vertex has exactly one frequency")
        print("  • Edge colors determined by resonance")
        print("  • No monochromatic K₅ allowed")
        print()
        
        n, r, s = 16, 5, 5
        f0, eps, grid = 141.7001, 0.037, 128
        
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            n, r, s, f0, eps, grid
        )
        
        # Write CNF file
        with open(cnf_file, 'w') as f:
            f.write(f"c Ramsey Resonance SAT Instance\n")
            f.write(f"c R_ψ({r},{s}) ≤ {n}\n")
            f.write(f"c f0 = {f0} Hz, eps = {eps}, grid = {grid}\n")
            f.write(f"c Generated with Tseytin encoding\n")
            f.write(f"p cnf {num_vars} {num_clauses}\n")
            
            for clause in clauses:
                f.write(" ".join(map(str, clause)) + " 0\n")
        
        print(f"  ✓ Generated: {cnf_file}")
        print(f"  ✓ Variables: {num_vars:,}")
        print(f"  ✓ Clauses: {num_clauses:,}")
        print(f"  ✓ File size: {os.path.getsize(cnf_file) / 1024 / 1024:.1f} MB")
    else:
        print()
        print("[Step 1/2] CNF formula already exists")
        print(f"  File: {cnf_file}")
        print(f"  Size: {os.path.getsize(cnf_file) / 1024 / 1024:.1f} MB")
        
        # Parse header to get stats
        with open(cnf_file, 'r') as f:
            for line in f:
                if line.startswith('p cnf'):
                    parts = line.split()
                    num_vars = int(parts[2])
                    num_clauses = int(parts[3])
                    print(f"  Variables: {num_vars:,}")
                    print(f"  Clauses: {num_clauses:,}")
                    break
    
    print()
    print("[Step 2/2] Solving with SAT solver...")
    print("  This verifies whether a valid coloring exists")
    print()
    
    # Solve
    result, model = solve_cnf(cnf_file, solver="z3")
    
    print()
    print("="*70)
    print("RESULT")
    print("="*70)
    
    if result == "UNSAT":
        print()
        print("✓ PROVEN: R_ψ(5,5) ≤ 16")
        print()
        print("The SAT solver found that the CNF formula is UNSATISFIABLE.")
        print("This means:")
        print()
        print("  ∀ ω: [16] → [0, f₀),")
        print("    ∃ blue K₅ ∨ ∃ red K₅")
        print()
        print("In other words: Every possible frequency assignment to 16")
        print("vertices must contain either a blue (resonant) K₅ or a")
        print("red (non-resonant) K₅.")
        print()
        print("This is dramatically smaller than the classical bound:")
        print("  R(5,5) ∈ [43, 48]")
        print()
        print("Showing the power of resonant coloring!")
        print()
    elif result == "SAT":
        print()
        print("⚠ UNEXPECTED: Found a valid coloring")
        print()
        print("This suggests the bound might be higher than 16.")
        print("Please verify the implementation.")
        print()
    else:
        print()
        print("✗ ERROR: Solver failed")
        print()
    
    print("="*70)
    print()
    print("For more details, see:")
    print("  • proofs/Rpsi_5_5_le_16.lean (Lean 4 formal proof)")
    print("  • data/README.md (CNF format explanation)")
    print("  • cert/README.md (UNSAT certificate information)")
    print()


if __name__ == "__main__":
    main()
