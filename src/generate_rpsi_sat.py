# src/generate_rpsi_sat.py
from itertools import combinations
from pathlib import Path

def generate_rpsi_sat_instance_tseytin(
    n: int, r: int, s: int,
    f0: float = 141.7001, eps: float = 0.037, grid: int = 128,
    output_path: str = "data/rpsi_5_5_n16.cnf"
):
    var_id = 1
    clauses = []

    # 1. Variables de frecuencia (one-hot por vértice)
    freq_var = [[0] * grid for _ in range(n)]
    for v in range(n):
        for k in range(grid):
            freq_var[v][k] = var_id
            var_id += 1
        # exactly one frequency
        clauses.append([freq_var[v][k] for k in range(grid)])  # at least one
        for i in range(grid):
            for j in range(i+1, grid):
                clauses.append([-freq_var[v][i], -freq_var[v][j]])  # at most one

    # 2. Variables de resonancia por arista
    edge_res = {}
    for i in range(n):
        for j in range(i+1, n):
            edge_res[(i,j)] = var_id
            var_id += 1

    # Precomputar pares resonantes
    resonant_pairs = []
    for k1 in range(grid):
        for k2 in range(grid):
            w1 = k1 * f0 / grid
            w2 = k2 * f0 / grid
            diff = min(abs(w1 - w2) % f0, f0 - abs(w1 - w2) % f0)
            if diff <= eps:
                resonant_pairs.append((k1, k2))

    # 3. Tseytin: edge_res ↔ ∃ k1,k2 resonant
    for i in range(n):
        for j in range(i+1, n):
            e = edge_res[(i,j)]
            lits = []
            for k1, k2 in resonant_pairs:
                aux_lit = var_id
                var_id += 1
                clauses.append([-aux_lit, freq_var[i][k1]])
                clauses.append([-aux_lit, freq_var[j][k2]])
                clauses.append([aux_lit, -freq_var[i][k1], -freq_var[j][k2]])
                lits.append(aux_lit)
            # edge_res → OR(lits)
            clauses.append([-e] + lits)
            # NOT edge_res → AND(NOT lit)
            for lit in lits:
                clauses.append([e, -lit])

    # 4. Prohibir K_r resonante (azul)
    for clique in combinations(range(n), r):
        clause = [-edge_res[(min(i,j), max(i,j))] for i, j in combinations(clique, 2)]
        clauses.append(clause)

    # 5. Prohibir K_s no resonante (rojo)
    for clique in combinations(range(n), s):
        clause = [edge_res[(min(i,j), max(i,j))] for i, j in combinations(clique, 2)]
        clauses.append(clause)

    # Guardar en DIMACS
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(f"p cnf {var_id-1} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"Instancia SAT guardada: {output_path}")
    print(f"Variables: {var_id-1} | Cláusulas: {len(clauses)}")
    return var_id-1, len(clauses)

# Generar para Rψ(5,5) ≤ 16
if __name__ == "__main__":
    generate_rpsi_sat_instance_tseytin(16, 5, 5)
