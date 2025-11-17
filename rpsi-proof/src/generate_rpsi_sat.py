#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Instancias SAT para Rψ(r,s) con Codificación Tseytin

Este módulo genera instancias SAT para verificar cotas superiores de números 
de Ramsey vibracionales usando codificación Tseytin para cláusulas compactas.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

from itertools import combinations
import numpy as np


def generate_rpsi_sat_instance_tseytin(n, r, s, eps=0.037, f0=141.7001, grid=128):
    """
    Genera instancia SAT para Rψ(r,s) ≤ n con codificación Tseytin + One-Hot + Resonancia
    
    Codificación:
    1. Variables de frecuencia: Cada vértice i tiene frecuencia ωᵢ = kᵢ * (f₀/grid)
       donde kᵢ ∈ [0, grid) se codifica en one-hot
    2. Variables de aristas: edge(i,j) = 1 si arista (i,j) es azul (resonante)
    3. Cláusulas Tseytin: Definen edge(i,j) según resonancia de ωᵢ, ωⱼ
    4. Cláusulas Ramsey: Prohiben K_r azul y K_s rojo
    
    Args:
        n: Número de vértices del grafo completo
        r: Tamaño del clique azul prohibido
        s: Tamaño del clique rojo prohibido
        eps: Umbral de resonancia (default: 0.037)
        f0: Frecuencia base (default: 141.7001 Hz)
        grid: Resolución de discretización (default: 128)
    
    Returns:
        tuple: (clauses, num_vars, num_clauses)
            clauses: Lista de cláusulas (cada cláusula es lista de literales)
            num_vars: Número total de variables
            num_clauses: Número total de cláusulas
    """
    
    # ===== ASIGNACIÓN DE VARIABLES =====
    var_counter = 1
    
    # 1. Variables k[i][j]: Vértice i tiene frecuencia j*f0/grid
    #    One-hot encoding: exactamente una de k[i][0], ..., k[i][grid-1] es true
    k_vars = {}
    for i in range(n):
        k_vars[i] = {}
        for j in range(grid):
            k_vars[i][j] = var_counter
            var_counter += 1
    
    # 2. Variables de aristas: edge[i][j] = 1 si (i,j) es azul (resonante)
    edge_vars = {}
    for i in range(n):
        for j in range(i + 1, n):
            edge_vars[(i, j)] = var_counter
            var_counter += 1
    
    # 3. Variables auxiliares para Tseytin (resonancia)
    #    res[i][j][ki][kj] = 1 si vértice i tiene freq ki Y vértice j tiene freq kj Y son resonantes
    res_vars = {}
    for i in range(n):
        for j in range(i + 1, n):
            res_vars[(i, j)] = {}
            for ki in range(grid):
                for kj in range(grid):
                    if is_resonant(ki, kj, grid, eps, f0):
                        res_vars[(i, j)][(ki, kj)] = var_counter
                        var_counter += 1
    
    num_vars = var_counter - 1
    clauses = []
    
    # ===== CLÁUSULAS =====
    
    # 1. ONE-HOT ENCODING: Cada vértice tiene exactamente una frecuencia
    for i in range(n):
        # Al menos una frecuencia
        clauses.append([k_vars[i][j] for j in range(grid)])
        
        # A lo más una frecuencia (pairwise)
        for j1 in range(grid):
            for j2 in range(j1 + 1, grid):
                clauses.append([-k_vars[i][j1], -k_vars[i][j2]])
    
    # 2. CODIFICACIÓN TSEYTIN DE RESONANCIA
    for i in range(n):
        for j in range(i + 1, n):
            edge = edge_vars[(i, j)]
            
            # edge(i,j) ⟺ ⋁_{(ki,kj) resonantes} (k[i][ki] ∧ k[j][kj])
            # Usando variables auxiliares res[(i,j)][(ki,kj)]
            
            resonant_pairs = []
            for ki in range(grid):
                for kj in range(grid):
                    if is_resonant(ki, kj, grid, eps, f0):
                        res_var = res_vars[(i, j)][(ki, kj)]
                        resonant_pairs.append(res_var)
                        
                        # res_var → k[i][ki]
                        clauses.append([-res_var, k_vars[i][ki]])
                        # res_var → k[j][kj]
                        clauses.append([-res_var, k_vars[j][kj]])
                        # k[i][ki] ∧ k[j][kj] → res_var
                        clauses.append([-k_vars[i][ki], -k_vars[j][kj], res_var])
            
            # edge ⟺ ⋁ res_var
            if resonant_pairs:
                # edge → ⋁ res_var
                clauses.append([-edge] + resonant_pairs)
                # res_var → edge (para cada res_var)
                for res_var in resonant_pairs:
                    clauses.append([-res_var, edge])
            else:
                # No hay pares resonantes → edge debe ser falso
                clauses.append([-edge])
    
    # 3. CLÁUSULAS RAMSEY: Prohibir K_r azul y K_s rojo
    
    # No K_r azul: Para cada r-subconjunto, al menos una arista NO es azul
    for clique in combinations(range(n), r):
        clause = []
        for i, j in combinations(clique, 2):
            if i > j:
                i, j = j, i
            clause.append(-edge_vars[(i, j)])
        clauses.append(clause)
    
    # No K_s rojo: Para cada s-subconjunto, al menos una arista ES azul
    for clique in combinations(range(n), s):
        clause = []
        for i, j in combinations(clique, 2):
            if i > j:
                i, j = j, i
            clause.append(edge_vars[(i, j)])
        clauses.append(clause)
    
    num_clauses = len(clauses)
    
    return clauses, num_vars, num_clauses


def is_resonant(ki, kj, grid, eps, f0):
    """
    Determina si dos índices de frecuencia ki, kj son resonantes
    
    ωᵢ = ki * f0/grid, ωⱼ = kj * f0/grid
    Resonantes si |ωᵢ - ωⱼ| mod f0 ≤ eps
    
    En términos de índices: |ki - kj| mod grid ≤ eps_grid
    donde eps_grid = eps * grid / f0
    
    Args:
        ki, kj: Índices de frecuencia [0, grid)
        grid: Tamaño del grid
        eps: Umbral de resonancia
        f0: Frecuencia base
    
    Returns:
        bool: True si son resonantes
    """
    eps_grid = (eps * grid) / f0
    diff = abs(ki - kj)
    # Considerar wrap-around modular
    diff_mod = min(diff, grid - diff)
    return diff_mod <= eps_grid


def save_dimacs(clauses, num_vars, num_clauses, path):
    """
    Guarda instancia SAT en formato DIMACS CNF
    
    Args:
        clauses: Lista de cláusulas
        num_vars: Número de variables
        num_clauses: Número de cláusulas
        path: Ruta del archivo de salida
    """
    with open(path, "w") as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    size_mb = len(clauses) * 20 / (1024 * 1024)  # Estimación aproximada
    print(f"✓ Guardado: {path}")
    print(f"  Variables: {num_vars:,}")
    print(f"  Cláusulas: {num_clauses:,}")
    print(f"  Tamaño estimado: ~{size_mb:.1f} MB")


def print_instance_info(n, r, s, num_vars, num_clauses, eps, f0, grid):
    """
    Imprime información sobre la instancia SAT generada
    """
    print("=" * 60)
    print(f"INSTANCIA SAT PARA Rψ({r},{s}) ≤ {n}")
    print("=" * 60)
    print(f"Métrica                    Valor")
    print(f"------------------------   ----------")
    print(f"Variables                  {num_vars:,}")
    print(f"Cláusulas                  {num_clauses:,}")
    print(f"Tamaño estimado (DIMACS)   ~{num_clauses * 20 / (1024**2):.1f} MB")
    print(f"Codificación               Tseytin + One-Hot + Resonancia")
    print(f"f₀                         {f0} Hz")
    print(f"ε                          {eps}")
    print(f"Grid                       {grid}")
    print("=" * 60)


if __name__ == "__main__":
    # RESULTADO OFICIAL: Rψ(5,5) ≤ 16
    print("\n🔬 GENERANDO INSTANCIA SAT OFICIAL\n")
    
    n, r, s = 16, 5, 5
    eps = 0.037
    f0 = 141.7001
    grid = 128
    
    print(f"Generando Rψ({r},{s}) ≤ {n}...\n")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(n, r, s, eps, f0, grid)
    
    print_instance_info(n, r, s, num_vars, num_clauses, eps, f0, grid)
    print("\n✨ INSTANCIA GENERADA EXITOSAMENTE")
    print("   Usar save_dimacs() para exportar a DIMACS\n")
