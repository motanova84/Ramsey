"""
SAT Solver for Ramsey Resonance Problems
Uses external SAT solvers or Python-based solvers
"""
import os
import sys


def solve_with_pysat(cnf_file: str):
    """
    Solve CNF using PySAT library.
    
    Parameters:
    -----------
    cnf_file : str
        Path to DIMACS CNF file
    
    Returns:
    --------
    tuple : (result, model)
        - result: "SAT" or "UNSAT"
        - model: list of variable assignments (if SAT) or None
    """
    try:
        from pysat.solvers import Glucose3
        from pysat.formula import CNF
    except ImportError:
        print("PySAT not available. Install with: pip install python-sat")
        return None, None
    
    cnf = CNF(from_file=cnf_file)
    solver = Glucose3()
    solver.append_formula(cnf)
    
    result = solver.solve()
    
    if result:
        model = solver.get_model()
        solver.delete()
        return "SAT", model
    else:
        solver.delete()
        return "UNSAT", None


def solve_with_z3(cnf_file: str):
    """
    Solve CNF using Z3 solver.
    
    Parameters:
    -----------
    cnf_file : str
        Path to DIMACS CNF file
    
    Returns:
    --------
    tuple : (result, model)
        - result: "SAT" or "UNSAT"
        - model: dict of variable assignments (if SAT) or None
    """
    try:
        from z3 import Bool, Solver, sat, Or, Not
    except ImportError:
        print("Z3 not available. Install with: pip install z3-solver")
        return None, None
    
    # Parse DIMACS file
    clauses = []
    num_vars = 0
    
    with open(cnf_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                # Skip empty lines
                continue
            if line.startswith('c'):
                continue
            elif line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
            else:
                parts = line.split()
                # In DIMACS, a line containing only '0' represents an empty clause,
                # which makes the whole CNF UNSAT.
                if len(parts) == 1 and parts[0] == '0':
                    return "UNSAT", None
                clause = [int(x) for x in parts if x != '0']
                if clause:
                    clauses.append(clause)
    
    # Create Z3 variables
    vars_z3 = {i: Bool(f'v{i}') for i in range(1, num_vars + 1)}
    
    # Create solver and add clauses
    solver = Solver()
    for clause in clauses:
        z3_clause = []
        for lit in clause:
            if lit > 0:
                z3_clause.append(vars_z3[lit])
            else:
                z3_clause.append(Not(vars_z3[-lit]))
        solver.add(z3_clause[0] if len(z3_clause) == 1 else Or(*z3_clause))
    
    # Solve
    result = solver.check()
    
    if result == sat:
        model = solver.model()
        model_dict = {}
        for i in range(1, num_vars + 1):
            val = model.eval(vars_z3[i], model_completion=True)
            # Use Z3's is_true() to properly evaluate boolean values
            from z3 import is_true
            model_dict[i] = is_true(val)
        return "SAT", model_dict
    else:
        return "UNSAT", None


def solve_cnf(cnf_file: str, solver: str = "z3"):
    """
    Solve CNF file using specified solver.
    
    Parameters:
    -----------
    cnf_file : str
        Path to DIMACS CNF file
    solver : str
        Solver to use: "z3", "pysat", or "external"
    
    Returns:
    --------
    tuple : (result, model)
        - result: "SAT" or "UNSAT"
        - model: variable assignments (if SAT) or None
    """
    print(f"Solving {cnf_file} with {solver}...")
    
    if solver == "z3":
        return solve_with_z3(cnf_file)
    elif solver == "pysat":
        return solve_with_pysat(cnf_file)
    else:
        print(f"Unknown solver: {solver}")
        return None, None


def analyze_result(result: str, n: int, r: int, s: int):
    """
    Analyze and report SAT result.
    
    Parameters:
    -----------
    result : str
        "SAT" or "UNSAT"
    n : int
        Number of vertices
    r : int
        Blue clique size
    s : int
        Red clique size
    """
    print("\n" + "="*60)
    if result == "UNSAT":
        print(f"RESULT: UNSAT")
        print(f"CONCLUSION: R_ψ({r},{s}) ≤ {n}")
        print(f"\nThis proves that any resonant coloring of K_{n}")
        print(f"must contain either:")
        print(f"  - A blue (resonant) K_{r}, or")
        print(f"  - A red (non-resonant) K_{s}")
    elif result == "SAT":
        print(f"RESULT: SAT")
        print(f"CONCLUSION: There exists a valid coloring for {n} vertices")
        print(f"This means R_ψ({r},{s}) > {n}")
    else:
        print(f"RESULT: Unknown (solver error)")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Solve Ramsey Resonance SAT instances"
    )
    parser.add_argument(
        "cnf_file",
        nargs="?",
        default="data/rpsi_5_5_n16.cnf",
        help="Path to DIMACS CNF file (default: data/rpsi_5_5_n16.cnf)"
    )
    parser.add_argument(
        "--solver",
        default="z3",
        choices=["z3", "pysat"],
        help="SAT solver to use (default: z3)"
    )
    parser.add_argument(
        "--n", type=int, default=16,
        help="Number of vertices (for reporting)"
    )
    parser.add_argument(
        "--r", type=int, default=5,
        help="Blue clique size (for reporting)"
    )
    parser.add_argument(
        "--s", type=int, default=5,
        help="Red clique size (for reporting)"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.cnf_file):
        print(f"Error: File not found: {args.cnf_file}")
        print(f"Generate it first with: python src/generate_rpsi_sat.py")
        sys.exit(1)
    
    result, model = solve_cnf(args.cnf_file, args.solver)
    
    if result:
        analyze_result(result, args.n, args.r, args.s)
    else:
        print("Error: Failed to solve CNF")
        sys.exit(1)
