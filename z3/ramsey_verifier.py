from z3 import *
from itertools import combinations
import argparse


def vibrational_ramsey(r, s, M=1000, eps=0.2):
    """
    Verifies the existence of a vibrational Ramsey coloring for given parameters.

    This function encodes a Ramsey-type property using Z3 SMT solver. It attempts to find a coloring
    of n = r + s - 1 points on a circle such that:
        - No subset of r points forms a "red" clique (all pairwise distances < eps or > 1 - eps).
        - No subset of s points forms a "blue" clique (all pairwise distances >= eps and <= 1 - eps).

    Parameters:
        r (int): Size of the red clique to avoid.
        s (int): Size of the blue clique to avoid.
        M (int, optional): Discretization parameter (unused in current implementation, reserved for future use).
        eps (float, optional): Resonance threshold for determining "red" edges.

    Returns:
        bool: True if a valid coloring exists (SAT), False otherwise (UNSAT).
              SAT means Rψ(r, s, eps) > r + s - 1.

    Logic:
        - Each point is assigned a real value in [0, 1).
        - An edge is "red" if the distance between two points is less than eps or greater than 1 - eps.
        - The solver checks that no r-clique is fully red and no s-clique is fully blue.
        - Returns True if the constraints are satisfiable, False otherwise.
    """
    # Input validation
    if not (isinstance(r, int) and r >= 1):
        raise ValueError(f"Parameter 'r' must be a positive integer (r >= 1), got {r}")
    if not (isinstance(s, int) and s >= 1):
        raise ValueError(f"Parameter 's' must be a positive integer (s >= 1), got {s}")
    if not (isinstance(eps, float) or isinstance(eps, int)) or not (0 < eps < 0.5):
        raise ValueError(f"Parameter 'eps' must be a float in the range (0, 0.5), got {eps}")
    solver = Solver()
    n = r + s - 1
    omega = [Real(f'omega_{i}') for i in range(n)]
    for w in omega:
        solver.add(0 <= w, w < 1.0)


    def is_red(i, j):
        diff = Abs(omega[i] - omega[j])
        return Or(diff < eps, 1 - diff < eps)


    for combo in combinations(range(n), r):
        solver.add(Not(And([is_red(i,j) for i,j in combinations(combo, 2)])))


    for combo in combinations(range(n), s):
        solver.add(Not(And([Not(is_red(i,j)) for i,j in combinations(combo, 2)])))


    return solver.check() == sat


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vibrational Ramsey Verifier")
    parser.add_argument("--r", type=int, required=True, help="Red clique size")
    parser.add_argument("--s", type=int, required=True, help="Blue clique size")
    parser.add_argument("--M", type=int, default=1000, help="Discretization parameter")
    parser.add_argument("--eps", type=float, default=0.2, help="Resonance threshold")
    args = parser.parse_args()


    result = vibrational_ramsey(args.r, args.s, args.M, args.eps)
    print(f"Result: Rψ({args.r},{args.s},{args.eps}) > {args.r + args.s - 1}? {'YES' if result else 'NO'}")
