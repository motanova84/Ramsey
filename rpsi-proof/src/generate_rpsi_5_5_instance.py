#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Rψ(5,5) SAT Instance for n=16

This is a convenience wrapper script that generates the SAT instance for
proving Rψ(5,5) ≤ 16. It uses the main generate_rpsi_sat.py module with
specific parameters optimized for the (5,5) case.

Usage:
    python generate_rpsi_5_5_instance.py --n=16
    python generate_rpsi_5_5_instance.py --n=16 --epsilon=0.037 --grid=128

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import argparse
import sys
import os

# Add parent directory to path to import generate_rpsi_sat
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_rpsi_sat import generate_rpsi_sat_instance_tseytin
from save_dimacs import save_dimacs


def main():
    parser = argparse.ArgumentParser(
        description='Generate SAT instance for Rψ(5,5) ≤ n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_rpsi_5_5_instance.py --n=16
  python generate_rpsi_5_5_instance.py --n=16 --epsilon=0.037 --grid=128
  python generate_rpsi_5_5_instance.py --n=15 --output=../data/rpsi_5_5_n15.cnf

This script generates a SAT instance encoding the constraint that every
vibrational coloring of K_n contains either a blue K_5 or a red K_5.
        """
    )
    
    parser.add_argument(
        '--n',
        type=int,
        default=16,
        help='Number of vertices (default: 16)'
    )
    
    parser.add_argument(
        '--epsilon',
        type=float,
        default=0.037,
        help='Resonance threshold (default: 0.037)'
    )
    
    parser.add_argument(
        '--f0',
        type=float,
        default=141.7001,
        help='Base frequency in Hz (default: 141.7001)'
    )
    
    parser.add_argument(
        '--grid',
        type=int,
        default=128,
        help='Grid resolution for frequency discretization (default: 128)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output CNF file path (default: ../data/rpsi_5_5_n{n}.cnf)'
    )
    
    args = parser.parse_args()
    
    # Generate SAT instance
    print(f"Generating SAT instance for Rψ(5,5) ≤ {args.n}")
    print(f"Parameters:")
    print(f"  f₀ = {args.f0} Hz")
    print(f"  ε = {args.epsilon}")
    print(f"  grid = {args.grid}")
    print()
    
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n=args.n,
        r=5,
        s=5,
        eps=args.epsilon,
        f0=args.f0,
        grid=args.grid
    )
    
    print(f"Generated SAT instance:")
    print(f"  Variables: {num_vars:,}")
    print(f"  Clauses: {num_clauses:,}")
    print()
    
    # Determine output path
    if args.output is None:
        output_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            f'rpsi_5_5_n{args.n}.cnf'
        )
    else:
        output_path = args.output
    
    # Save to DIMACS format
    output_path = os.path.abspath(output_path)
    save_dimacs(clauses, num_vars, output_path)
    
    print(f"✓ Saved to: {output_path}")
    print(f"  File size: ~{os.path.getsize(output_path) / (1024*1024):.1f} MB")
    print()
    print("Next steps:")
    print(f"  1. Verify with SAT solver: z3 {output_path}")
    print(f"  2. Or use Kissat: kissat {output_path}")


if __name__ == '__main__':
    main()
