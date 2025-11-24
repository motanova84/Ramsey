#!/usr/bin/env python3
"""
Compute and display table of R_ψ(r,s) values with theoretical predictions

Generates comprehensive table for r,s ≤ 10 comparing:
- Theoretical bound: ceil(√(r·s) · log(r·s))
- Classical R(r,s) when known
- Computed R_ψ(r,s) values

Usage:
    python compute_rpsi_table.py
    python compute_rpsi_table.py --max-size=6 --output=table.csv
"""

import argparse
import math
import csv
from typing import Dict, Tuple, Optional


# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

# Universal coherence frequency
F0 = 141.7001  # Hz

# Known classical Ramsey numbers R(r,s)
CLASSICAL_RAMSEY = {
    (2, 2): 2,
    (2, 3): 3,
    (2, 4): 4,
    (2, 5): 5,
    (2, 6): 6,
    (2, 7): 7,
    (2, 8): 8,
    (2, 9): 9,
    (2, 10): 10,
    (3, 3): 6,
    (3, 4): 9,
    (3, 5): 14,
    (3, 6): 18,
    (3, 7): 23,
    (3, 8): 28,
    (3, 9): 36,
    (4, 4): 18,
    (4, 5): 25,
    (5, 5): 48,  # Upper bound; lower bound is 43
}


def theoretical_bound(r: int, s: int) -> int:
    """
    Compute theoretical bound for R_ψ(r,s)
    
    Formula: R_ψ(r,s) ≈ φ × √(r·s) · log(r·s) / (f₀/100)^(1/4)
    
    This is Conjecture 3.4 from the theory.
    """
    if r * s == 0:
        return 0
    if r * s == 1:
        return 1
    
    # Base estimate using golden ratio
    product = r * s
    base_estimate = PHI * math.sqrt(product) * math.log(max(product, 2))
    
    # Frequency correction factor
    freq_factor = (F0 / 100.0) ** (1/4)
    
    # Adjusted estimate
    estimate = base_estimate / freq_factor
    
    return max(math.ceil(estimate), max(r, s))


def simple_bound(r: int, s: int) -> int:
    """
    Simple polynomial bound: ceil(√(r·s) · log(r·s))
    """
    if r * s == 0:
        return 0
    if r * s == 1:
        return 1
    
    product = r * s
    bound = math.sqrt(product) * math.log(max(product, 2))
    return max(math.ceil(bound), max(r, s))


# Known computed R_ψ values (from SAT solving and certificates)
COMPUTED_RPSI = {
    (3, 3): 6,
    (3, 4): 8,
    (4, 4): 11,
    (3, 5): 9,
    (4, 5): 13,
    (5, 5): 16,
}


def get_rpsi(r: int, s: int) -> Optional[int]:
    """Get computed R_ψ(r,s) if available"""
    # Check both (r,s) and (s,r) due to symmetry
    if (r, s) in COMPUTED_RPSI:
        return COMPUTED_RPSI[(r, s)]
    elif (s, r) in COMPUTED_RPSI:
        return COMPUTED_RPSI[(s, r)]
    else:
        return None


def get_classical(r: int, s: int) -> Optional[int]:
    """Get classical R(r,s) if known"""
    # R(r,s) = R(s,r), so check both
    if (r, s) in CLASSICAL_RAMSEY:
        return CLASSICAL_RAMSEY[(r, s)]
    elif (s, r) in CLASSICAL_RAMSEY:
        return CLASSICAL_RAMSEY[(s, r)]
    else:
        return None


def compute_improvement(classical: Optional[int], vibrational: Optional[int]) -> Optional[float]:
    """Compute percentage improvement of R_ψ over R"""
    if classical and vibrational and classical > 0:
        return 100 * (classical - vibrational) / classical
    return None


def generate_table(max_size: int = 10) -> list:
    """Generate comprehensive table of R_ψ values"""
    
    table = []
    
    for r in range(2, max_size + 1):
        for s in range(r, max_size + 1):  # Only upper triangle due to symmetry
            # Get values
            rpsi = get_rpsi(r, s)
            classical = get_classical(r, s)
            theory_bound = theoretical_bound(r, s)
            simple = simple_bound(r, s)
            improvement = compute_improvement(classical, rpsi)
            
            # Compute error if we have both theoretical and computed
            theory_error = None
            if rpsi and theory_bound:
                theory_error = 100 * abs(theory_bound - rpsi) / rpsi
            
            # Build row
            row = {
                'r': r,
                's': s,
                'R_classical': classical if classical else '?',
                'R_psi_computed': rpsi if rpsi else '?',
                'R_psi_theory': theory_bound,
                'Simple_bound': simple,
                'Improvement_%': f"{improvement:.1f}%" if improvement else '-',
                'Theory_error_%': f"{theory_error:.1f}%" if theory_error is not None else '-',
            }
            
            table.append(row)
    
    return table


def print_table(table: list, format_type: str = 'markdown'):
    """Print table in requested format"""
    
    if format_type == 'markdown':
        print("\n## Table: Vibrational Ramsey Numbers R_ψ(r,s)")
        print("\n| (r,s) | R(r,s) | R_ψ computed | R_ψ theory | Simple | Improvement | Error |")
        print("|-------|--------|--------------|------------|--------|-------------|-------|")
        
        for row in table:
            r, s = row['r'], row['s']
            print(f"| ({r},{s}) | {row['R_classical']} | {row['R_psi_computed']} | "
                  f"{row['R_psi_theory']} | {row['Simple_bound']} | "
                  f"{row['Improvement_%']} | {row['Theory_error_%']} |")
    
    elif format_type == 'csv':
        print("r,s,R_classical,R_psi_computed,R_psi_theory,Simple_bound,Improvement_%,Theory_error_%")
        for row in table:
            print(f"{row['r']},{row['s']},{row['R_classical']},{row['R_psi_computed']},"
                  f"{row['R_psi_theory']},{row['Simple_bound']},{row['Improvement_%']},{row['Theory_error_%']}")
    
    elif format_type == 'latex':
        print("\\begin{tabular}{|c|c|c|c|c|c|}")
        print("\\hline")
        print("$(r,s)$ & $R(r,s)$ & $R_\\psi$ computed & $R_\\psi$ theory & Improvement & Error \\\\")
        print("\\hline")
        
        for row in table:
            r, s = row['r'], row['s']
            print(f"$({r},{s})$ & {row['R_classical']} & {row['R_psi_computed']} & "
                  f"{row['R_psi_theory']} & {row['Improvement_%']} & {row['Theory_error_%']} \\\\")
        
        print("\\hline")
        print("\\end{tabular}")
    
    else:  # plain text
        print("\nVibrational Ramsey Numbers R_ψ(r,s)")
        print("="*90)
        print(f"{'(r,s)':<8} {'R(r,s)':<10} {'R_ψ(comp)':<12} {'R_ψ(theory)':<12} "
              f"{'Improvement':<14} {'Error':<10}")
        print("-"*90)
        
        for row in table:
            r, s = row['r'], row['s']
            print(f"({r},{s}){'':<4} {str(row['R_classical']):<10} "
                  f"{str(row['R_psi_computed']):<12} {row['R_psi_theory']:<12} "
                  f"{row['Improvement_%']:<14} {row['Theory_error_%']:<10}")
        
        print("="*90)


def print_statistics(table: list):
    """Print summary statistics"""
    
    # Count available computed values
    computed_count = sum(1 for row in table if row['R_psi_computed'] != '?')
    total_count = len(table)
    
    # Average improvement
    improvements = [
        float(row['Improvement_%'].rstrip('%')) 
        for row in table 
        if row['Improvement_%'] != '-'
    ]
    avg_improvement = sum(improvements) / len(improvements) if improvements else 0
    
    # Average theory error
    errors = [
        float(row['Theory_error_%'].rstrip('%'))
        for row in table
        if row['Theory_error_%'] != '-'
    ]
    avg_error = sum(errors) / len(errors) if errors else 0
    
    print("\n## Summary Statistics")
    print(f"\n- Total entries: {total_count}")
    print(f"- Computed values: {computed_count} ({100*computed_count/total_count:.1f}%)")
    print(f"- Average improvement over classical: {avg_improvement:.1f}%")
    print(f"- Average theory error: {avg_error:.1f}%")
    
    # Highlight best results
    if computed_count > 0:
        best = max(
            (row for row in table if row['Improvement_%'] != '-'),
            key=lambda r: float(r['Improvement_%'].rstrip('%'))
        )
        print(f"\n- Best improvement: R_ψ({best['r']},{best['s']}) = {best['R_psi_computed']} "
              f"vs R({best['r']},{best['s']}) = {best['R_classical']} "
              f"({best['Improvement_%']} reduction)")


def save_csv(table: list, filename: str):
    """Save table to CSV file"""
    
    with open(filename, 'w', newline='') as f:
        if table:
            writer = csv.DictWriter(f, fieldnames=table[0].keys())
            writer.writeheader()
            writer.writerows(table)
    
    print(f"\n✓ Table saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Compute table of R_ψ(r,s) values with predictions'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        default=10,
        help='Maximum r,s value to compute (default: 10)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'markdown', 'csv', 'latex'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Save to CSV file (optional)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show summary statistics'
    )
    
    args = parser.parse_args()
    
    # Generate table
    print(f"\nComputing R_ψ(r,s) table for r,s ≤ {args.max_size}...")
    table = generate_table(args.max_size)
    
    # Display table
    print_table(table, args.format)
    
    # Show statistics if requested
    if args.stats or args.format != 'csv':
        print_statistics(table)
    
    # Save to file if requested
    if args.output:
        save_csv(table, args.output)
    
    print()


if __name__ == '__main__':
    main()
