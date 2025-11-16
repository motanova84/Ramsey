#!/usr/bin/env python3
"""
Cross-validation script for SAT solver verification
Tests CNF formulas across multiple solvers (Z3, MiniSAT, CaDiCaL, PySAT)

Usage:
    python validate_sat.py --solver=z3 --file=certificates/rpsi_3_3_le_6.smt2
    python validate_sat.py --solver=all --r=3 --s=3 --n=6
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

try:
    from z3 import *
except ImportError:
    print("Warning: z3-solver not installed. Install with: pip install z3-solver")
    Solver = None


def verify_z3(smt2_file):
    """Verify using Z3 SMT solver"""
    print(f"\n=== Testing with Z3 ===")
    
    if not os.path.exists(smt2_file):
        print(f"Error: File {smt2_file} not found")
        return None
    
    try:
        # Try using z3 command line
        result = subprocess.run(
            ['z3', smt2_file],
            capture_output=True,
            text=True,
            timeout=300
        )
        output = result.stdout.strip()
        print(f"Z3 result: {output}")
        
        if 'unsat' in output.lower():
            return 'UNSAT'
        elif 'sat' in output.lower() and 'unsat' not in output.lower():
            return 'SAT'
        else:
            return 'UNKNOWN'
    except FileNotFoundError:
        print("z3 command not found. Trying Python API...")
        if Solver is None:
            print("Z3 Python API not available")
            return None
        
        # Try using Python API
        try:
            solver = Solver()
            solver.from_file(smt2_file)
            result = solver.check()
            print(f"Z3 result: {result}")
            return str(result)
        except Exception as e:
            print(f"Error using Z3 Python API: {e}")
            return None
    except subprocess.TimeoutExpired:
        print("Z3 timed out after 300 seconds")
        return 'TIMEOUT'
    except Exception as e:
        print(f"Error running Z3: {e}")
        return None


def verify_minisat(cnf_file):
    """Verify using MiniSAT solver"""
    print(f"\n=== Testing with MiniSAT ===")
    
    try:
        # Check if minisat is available
        result = subprocess.run(
            ['minisat', '--help'],
            capture_output=True,
            timeout=5
        )
        if result.returncode not in [0, 1]:  # minisat returns 1 for --help
            print("MiniSAT not found. Install with: apt-get install minisat")
            return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("MiniSAT not found. Install with: apt-get install minisat")
        return None
    
    if not os.path.exists(cnf_file):
        print(f"Error: File {cnf_file} not found")
        print("Note: MiniSAT requires CNF format. Convert SMT2 to CNF first.")
        return None
    
    try:
        # Create output file for minisat
        output_file = cnf_file + '.out'
        result = subprocess.run(
            ['minisat', cnf_file, output_file],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Check result
        if 'UNSATISFIABLE' in result.stdout:
            print("MiniSAT result: UNSAT")
            return 'UNSAT'
        elif 'SATISFIABLE' in result.stdout:
            print("MiniSAT result: SAT")
            return 'SAT'
        else:
            print(f"MiniSAT output: {result.stdout}")
            return 'UNKNOWN'
    except subprocess.TimeoutExpired:
        print("MiniSAT timed out after 300 seconds")
        return 'TIMEOUT'
    except Exception as e:
        print(f"Error running MiniSAT: {e}")
        return None


def verify_cadical(cnf_file):
    """Verify using CaDiCaL solver"""
    print(f"\n=== Testing with CaDiCaL ===")
    
    try:
        # Check if cadical is available
        result = subprocess.run(
            ['cadical', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode not in [0, 1]:
            print("CaDiCaL not found. Install from: https://github.com/arminbiere/cadical")
            return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("CaDiCaL not found. Install from: https://github.com/arminbiere/cadical")
        return None
    
    if not os.path.exists(cnf_file):
        print(f"Error: File {cnf_file} not found")
        return None
    
    try:
        result = subprocess.run(
            ['cadical', cnf_file],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if 's UNSATISFIABLE' in result.stdout:
            print("CaDiCaL result: UNSAT")
            return 'UNSAT'
        elif 's SATISFIABLE' in result.stdout:
            print("CaDiCaL result: SAT")
            return 'SAT'
        else:
            print(f"CaDiCaL output: {result.stdout[:200]}")
            return 'UNKNOWN'
    except subprocess.TimeoutExpired:
        print("CaDiCaL timed out after 300 seconds")
        return 'TIMEOUT'
    except Exception as e:
        print(f"Error running CaDiCaL: {e}")
        return None


def verify_pysat(cnf_file):
    """Verify using PySAT library"""
    print(f"\n=== Testing with PySAT ===")
    
    try:
        from pysat.solvers import Glucose3
        from pysat.formula import CNF
    except ImportError:
        print("PySAT not installed. Install with: pip install python-sat")
        return None
    
    if not os.path.exists(cnf_file):
        print(f"Error: File {cnf_file} not found")
        return None
    
    try:
        # Read CNF file
        cnf = CNF(from_file=cnf_file)
        
        # Create solver
        solver = Glucose3()
        for clause in cnf.clauses:
            solver.add_clause(clause)
        
        # Solve
        result = solver.solve()
        
        if result:
            print("PySAT result: SAT")
            return 'SAT'
        else:
            print("PySAT result: UNSAT")
            return 'UNSAT'
    except Exception as e:
        print(f"Error using PySAT: {e}")
        return None


def convert_smt2_to_cnf(smt2_file, cnf_file):
    """Convert SMT2 file to CNF format (simplified conversion)"""
    print(f"\nConverting {smt2_file} to {cnf_file}...")
    print("Note: Full SMT2 to CNF conversion is complex. Using Z3 for conversion.")
    
    # This is a placeholder - full conversion requires sophisticated tools
    print("For production use, consider tools like:")
    print("  - Z3's tactic framework")
    print("  - SMT-LIB benchmarks")
    print("  - Boolector or other SMT solvers with CNF export")
    
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Cross-validate SAT formulas across multiple solvers'
    )
    parser.add_argument(
        '--solver',
        choices=['z3', 'minisat', 'cadical', 'pysat', 'all'],
        default='z3',
        help='Which solver(s) to use'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to SMT2 or CNF file'
    )
    parser.add_argument(
        '--r',
        type=int,
        help='Clique size r (if generating formula)'
    )
    parser.add_argument(
        '--s',
        type=int,
        help='Clique size s (if generating formula)'
    )
    parser.add_argument(
        '--n',
        type=int,
        help='Number of vertices n (if generating formula)'
    )
    
    args = parser.parse_args()
    
    # Determine file to test
    if args.file:
        test_file = args.file
    elif args.r and args.s and args.n:
        # Look for pre-generated certificate
        test_file = f"certificates/rpsi_{args.r}_{args.s}_le_{args.n}.smt2"
        if not os.path.exists(test_file):
            test_file = f"smt2/rpsi_{args.r}_{args.s}_n{args.n}.smt2"
        if not os.path.exists(test_file):
            print(f"Error: No certificate found for R_ψ({args.r},{args.s}) with n={args.n}")
            print(f"Looked for: {test_file}")
            sys.exit(1)
    else:
        print("Error: Must specify either --file or --r, --s, --n")
        parser.print_help()
        sys.exit(1)
    
    print(f"Testing file: {test_file}")
    print("="*70)
    
    results = {}
    
    # Test with requested solver(s)
    if args.solver in ['z3', 'all']:
        results['Z3'] = verify_z3(test_file)
    
    # For other solvers, need CNF format
    cnf_file = test_file.replace('.smt2', '.cnf')
    if args.solver in ['minisat', 'cadical', 'pysat', 'all']:
        if not os.path.exists(cnf_file):
            print(f"\nCNF file not found: {cnf_file}")
            print("Attempting to convert from SMT2...")
            convert_smt2_to_cnf(test_file, cnf_file)
        
        if os.path.exists(cnf_file):
            if args.solver in ['minisat', 'all']:
                results['MiniSAT'] = verify_minisat(cnf_file)
            if args.solver in ['cadical', 'all']:
                results['CaDiCaL'] = verify_cadical(cnf_file)
            if args.solver in ['pysat', 'all']:
                results['PySAT'] = verify_pysat(cnf_file)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF RESULTS:")
    print("="*70)
    for solver, result in results.items():
        if result:
            print(f"  {solver:12s}: {result}")
        else:
            print(f"  {solver:12s}: NOT AVAILABLE")
    
    # Check consistency
    valid_results = [r for r in results.values() if r and r != 'UNKNOWN']
    if len(set(valid_results)) > 1:
        print("\n⚠️  WARNING: Inconsistent results across solvers!")
        sys.exit(1)
    elif valid_results:
        print(f"\n✓ All solvers agree: {valid_results[0]}")
    else:
        print("\n⚠️  No solvers available or all returned UNKNOWN")
    
    print("="*70)


if __name__ == '__main__':
    main()
