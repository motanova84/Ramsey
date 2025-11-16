#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Instancia Rψ(5,5) para n vértices

Genera instancias CNF para verificar Rψ(5,5) ≤ n mediante codificación
de coloración vibracional con restricciones de resonancia.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

from itertools import combinations
import numpy as np


def generate_rpsi_instance(n, f0=141.7001, eps=0.015, grid=128):
    """
    Genera instancia CNF para Rψ(5,5) ≤ n con coloración vibracional.
    
    Codifica un grafo completo Kₙ en formato CNF con reglas de coloración vibracional:
    - Cada vértice i tiene frecuencia ωᵢ ∈ [0, f₀)
    - Frecuencias discretizadas en 'grid' valores
    - Arista (i,j) es roja ↔ |ωᵢ - ωⱼ| mod f₀ ≥ ε
    - Arista (i,j) es azul ↔ |ωᵢ - ωⱼ| mod f₀ < ε (resonante)
    
    Args:
        n: Número de vértices del grafo completo Kₙ
        f0: Frecuencia base de coherencia (default: 141.7001 Hz)
        eps: Umbral de resonancia (default: 0.015)
        grid: Resolución de discretización (default: 128)
    
    Returns:
        tuple: (clauses, num_vars, num_clauses)
            clauses: Lista de cláusulas CNF (cada cláusula es lista de literales)
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
    
    # 3. Variables auxiliares para codificación Tseytin (resonancia)
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
    
    # 2. CODIFICACIÓN DE RESONANCIA (Tseytin)
    for i in range(n):
        for j in range(i + 1, n):
            edge = edge_vars[(i, j)]
            
            # edge(i,j) ⟺ ⋁_{(ki,kj) resonantes} (k[i][ki] ∧ k[j][kj])
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
    
    # 3. CLÁUSULAS RAMSEY: Prohibir K₅ azul (resonante)
    r = 5  # Tamaño de clique azul prohibido
    for clique in combinations(range(n), r):
        clause = []
        for i, j in combinations(clique, 2):
            if i > j:
                i, j = j, i
            clause.append(-edge_vars[(i, j)])
        clauses.append(clause)
    
    # 4. CLÁUSULAS RAMSEY: Prohibir K₅ rojo (no-resonante)
    s = 5  # Tamaño de clique rojo prohibido
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
    Determina si dos índices de frecuencia ki, kj son resonantes.
    
    ωᵢ = ki * f0/grid, ωⱼ = kj * f0/grid
    Resonantes si |ωᵢ - ωⱼ| mod f0 < eps
    
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
    return diff_mod < eps_grid


def save_dimacs(clauses, num_vars, num_clauses, path):
    """
    Guarda instancia SAT en formato DIMACS CNF.
    
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


if __name__ == "__main__":
    # Genera instancia para Rψ(5,5) con n=16
    print("\n🔬 GENERANDO INSTANCIA Rψ(5,5) para K₁₆\n")
    
    n = 16
    f0 = 141.7001
    eps = 0.015
    grid = 128
    
    print(f"Parámetros:")
    print(f"  n = {n} vértices")
    print(f"  f₀ = {f0} Hz")
    print(f"  ε = {eps}")
    print(f"  grid = {grid}\n")
    
    clauses, num_vars, num_clauses = generate_rpsi_instance(n, f0, eps, grid)
    
    print(f"\nInstancia generada:")
    print(f"  Variables: {num_vars:,}")
    print(f"  Cláusulas: {num_clauses:,}")
    
    # Guardar en formato DIMACS
    output_path = "../data/coloring_r16.cnf"
    save_dimacs(clauses, num_vars, num_clauses, output_path)
    
    print("\n✨ GENERACIÓN COMPLETADA\n")
