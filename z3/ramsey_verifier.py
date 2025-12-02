from z3 import *
from itertools import combinations
import argparse


def vibrational_ramsey(r, s, M=1000, eps=0.2):
    # Input validation
    if not (isinstance(r, int) and r >= 1):
        raise ValueError(f"Parameter 'r' must be a positive integer (r >= 1), got {r}")
    if not (isinstance(s, int) and s >= 1):
        raise ValueError(f"Parameter 's' must be a positive integer (s >= 1), got {s}")
    if not (isinstance(eps, float) or isinstance(eps, int)) or not (0 < eps < 0.5):
        raise ValueError(f"Parameter 'eps' must be a float in the range (0, 0.5), got {eps}")
    solver = Solver()
    n_val = r + s - 1
    omega = [Real(f'omega_{i}') for i in range(n_val)]
    for w in omega:
        solver.add(0 <= w, w < 1.0)


    def is_red(i, j):
        diff = Abs(omega[i] - omega[j])
        return Or(diff < eps, 1 - diff < eps)


    for combo in combinations(range(n_val), r):
        solver.add(Not(And([is_red(i,j) for i,j in combinations(combo, 2)])))


    for combo in combinations(range(n_val), s):
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
