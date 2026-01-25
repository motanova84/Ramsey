"""
SAT-based Ramsey Resonance Solver
Generates SAT instances for R_ψ(r,s) with resonant coloring
Uses Tseytin encoding for scalability
"""
import os
from itertools import combinations


def generate_rpsi_sat_instance_tseytin(
    n: int, r: int, s: int,
    f0: float = 141.7001, eps: float = 0.037, grid: int = 128
):
    """
    Generate SAT instance for R_ψ(r,s) ≤ n with Tseytin encoding.
    
    Parameters:
    -----------
    n : int
        Number of vertices
    r : int
        Size of blue (resonant) clique to avoid
    s : int
        Size of red (non-resonant) clique to avoid
    f0 : float
        Base frequency (default: 141.7001 Hz)
    eps : float
        Resonance threshold (default: 0.037)
    grid : int
        Number of discretization points for [0, f0) (default: 128)
    
    Returns:
    --------
    tuple : (clauses, num_vars, num_clauses)
        - clauses: list of clauses (each clause is a list of literals)
        - num_vars: total number of variables
        - num_clauses: total number of clauses
    """
    var_id = 1
    clauses = []

    # 1. Variables de frecuencia (one-hot por vértice)
    freq_var = [[0] * grid for _ in range(n)]
    for v in range(n):
        for k in range(grid):
            freq_var[v][k] = var_id
            var_id += 1
        # Exactly one frequency: at least one
        clauses.append([freq_var[v][k] for k in range(grid)])
        # At most one (pairwise exclusion)
        for i in range(grid):
            for j in range(i+1, grid):
                clauses.append([-freq_var[v][i], -freq_var[v][j]])

    # 2. Variables de resonancia por arista
    edge_res = {}  # (i,j) -> var
    for i in range(n):
        for j in range(i+1, n):
            edge_res[(i, j)] = var_id
            var_id += 1

    # Precomputar pares resonantes
    resonant_pairs = []
    for k1 in range(grid):
        for k2 in range(grid):
            w1 = k1 * f0 / grid
            w2 = k2 * f0 / grid
            diff = abs(w1 - w2)
            circular_diff = min(diff, f0 - diff)
            # Resonant if circular distance is close to 0
            # Using < (not <=) to match Lean specification
            if circular_diff < eps:
                resonant_pairs.append((k1, k2))

    # 3. Tseytin encoding: edge_res ↔ ∃ (k1,k2) resonant
    for i in range(n):
        for j in range(i+1, n):
            e = edge_res[(i, j)]
            aux_vars = []
            
            # For each resonant pair, create auxiliary variable
            for k1, k2 in resonant_pairs:
                aux = var_id
                var_id += 1
                aux_vars.append(aux)
                
                # aux → (freq_var[i][k1] ∧ freq_var[j][k2])
                clauses.append([-aux, freq_var[i][k1]])
                clauses.append([-aux, freq_var[j][k2]])
                
                # (freq_var[i][k1] ∧ freq_var[j][k2]) → aux
                clauses.append([-freq_var[i][k1], -freq_var[j][k2], aux])

            # edge_res ↔ OR(aux_vars)
            # edge_res → OR(aux_vars)
            clauses.append([-e] + aux_vars)
            
            # OR(aux_vars) → edge_res
            for aux in aux_vars:
                clauses.append([-aux, e])

    # 4. Prohibir K_r resonante (azul)
    for clique in combinations(range(n), r):
        clause = []
        for i, j in combinations(clique, 2):
            e = edge_res[(min(i, j), max(i, j))]
            clause.append(-e)  # al menos una arista NO resonante
        clauses.append(clause)

    # 5. Prohibir K_s no resonante (rojo)
    for clique in combinations(range(n), s):
        clause = []
        for i, j in combinations(clique, 2):
            e = edge_res[(min(i, j), max(i, j))]
            clause.append(e)  # al menos una arista resonante
        clauses.append(clause)

    return clauses, var_id - 1, len(clauses)


def generate_dimacs(n: int, r: int, s: int, 
                   f0: float = 141.7001, eps: float = 0.037, grid: int = 128,
                   output_file: str = None):
    """
    Generate DIMACS CNF file for R_ψ(r,s) ≤ n problem.
    
    Parameters:
    -----------
    n : int
        Number of vertices
    r : int
        Size of blue clique to avoid
    s : int
        Size of red clique to avoid
    f0 : float
        Base frequency
    eps : float
        Resonance threshold
    grid : int
        Discretization grid size
    output_file : str
        Output filename (default: data/rpsi_{r}_{s}_n{n}.cnf)
    
    Returns:
    --------
    str : Path to generated DIMACS file
    """
    if output_file is None:
        output_file = f"data/rpsi_{r}_{s}_n{n}.cnf"
    
    # Ensure the parent directory exists
    dir_name = os.path.dirname(output_file)
    if dir_name:  # Only create if dirname is non-empty
        os.makedirs(dir_name, exist_ok=True)
    
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n, r, s, f0, eps, grid
    )
    
    with open(output_file, 'w') as f:
        # Header
        f.write(f"c Ramsey Resonance SAT Instance\n")
        f.write(f"c R_ψ({r},{s}) ≤ {n}\n")
        f.write(f"c f0 = {f0} Hz, eps = {eps}, grid = {grid}\n")
        f.write(f"c Generated with Tseytin encoding\n")
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        
        # Clauses
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"Generated DIMACS file: {output_file}")
    print(f"  Variables: {num_vars}")
    print(f"  Clauses: {num_clauses}")
    
    return output_file


if __name__ == "__main__":
    import sys
    
    # Default: R_ψ(5,5) ≤ 16
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    s = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    print(f"\nGenerating SAT instance for R_ψ({r},{s}) ≤ {n}")
    print(f"Parameters: f0=141.7001 Hz, eps=0.037, grid=128\n")
    
    output_file = generate_dimacs(n, r, s)
    print(f"\nDone! File saved to: {output_file}")
