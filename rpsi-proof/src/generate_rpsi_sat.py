#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Instancias SAT para Rψ(r,s) ≤ n

Este script genera instancias SAT en formato DIMACS CNF para verificar
si R_ψ(r,s) ≤ n mediante codificación simbiótica Rψ basada en resonancia vibracional.

La codificación está basada en SAT estándar para problemas de Ramsey:
- Cada arista del grafo completo K_n es una variable booleana
- TRUE = arista roja (no-resonante)
- FALSE = arista azul (resonante)

Para cada subconjunto de r nodos: al menos una arista NO debe ser roja (evitar K_r rojo)
Para cada subconjunto de s nodos: al menos una arista NO debe ser azul (evitar K_s azul)

Autores: José Manuel Mota Burruezo - JMMB Ψ✧∴
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³
"""

from itertools import combinations
from typing import List, Tuple, Dict
import argparse


def generate_rpsi_sat_instance(n: int, r: int, s: int) -> Tuple[Dict[Tuple[int, int], int], List[List[int]]]:
    """
    Genera la instancia SAT de Rψ(r,s) ≤ n como CNF.
    
    Args:
        n: número total de nodos (vértices del grafo completo K_n)
        r: tamaño del clique monocromático rojo prohibido
        s: tamaño del clique monocromático azul prohibido
    
    Returns:
        edge_vars: Diccionario que mapea aristas (i,j) a variables booleanas
        clauses: Lista de cláusulas CNF (cada cláusula es una lista de literales)
    """
    edge_vars = {}
    var_id = 1
    clauses = []

    # Asignamos un número a cada arista del grafo completo K_n
    for (i, j) in combinations(range(1, n + 1), 2):
        edge_vars[(i, j)] = var_id
        var_id += 1

    def get_var(i, j):
        """Obtiene el ID de variable para la arista (i,j)"""
        return edge_vars[(i, j)] if (i, j) in edge_vars else edge_vars[(j, i)]

    # Prohibir cliques monocromáticos rojos (todos rojos)
    # Para cada subconjunto de r nodos, al menos una arista debe NO ser roja
    for clique in combinations(range(1, n + 1), r):
        # Para evitar K_r rojo: al menos una arista debe ser azul (negada)
        clause = [-get_var(i, j) for (i, j) in combinations(clique, 2)]
        clauses.append(clause)
    
    # Prohibir cliques monocromáticos azules (todos azules)
    # Para cada subconjunto de s nodos, al menos una arista debe NO ser azul
    for clique in combinations(range(1, n + 1), s):
        # Para evitar K_s azul: al menos una arista debe ser roja (positiva)
        clause = [get_var(i, j) for (i, j) in combinations(clique, 2)]
        clauses.append(clause)

    return edge_vars, clauses


def write_dimacs_cnf(edge_vars: Dict[Tuple[int, int], int], clauses: List[List[int]], 
                     output_file: str, r: int, s: int, n: int):
    """
    Escribe la instancia SAT en formato DIMACS CNF.
    
    Args:
        edge_vars: Diccionario de variables
        clauses: Lista de cláusulas
        output_file: Ruta del archivo de salida
        r, s, n: Parámetros del problema Rψ(r,s) ≤ n
    """
    num_vars = len(edge_vars)
    num_clauses = len(clauses)
    
    with open(output_file, 'w') as f:
        # Comentarios con información del problema
        f.write(f"c Instancia SAT para Rψ({r},{s}) ≤ {n}\n")
        f.write(f"c Codificación simbiótica basada en resonancia vibracional\n")
        f.write(f"c Frecuencia base: 141.7001 Hz - Campo QCAL ∞³\n")
        f.write(f"c\n")
        f.write(f"c Grafo: K_{n} (grafo completo con {n} vértices)\n")
        f.write(f"c Variables booleanas (aristas): {num_vars}\n")
        f.write(f"c Cláusulas CNF: {num_clauses}\n")
        f.write(f"c\n")
        f.write(f"c Variable x_ij = TRUE  => arista (i,j) es ROJA (no-resonante)\n")
        f.write(f"c Variable x_ij = FALSE => arista (i,j) es AZUL (resonante)\n")
        f.write(f"c\n")
        f.write(f"c Objetivo: verificar si existe coloración que evita:\n")
        f.write(f"c   - K_{r} rojo (clique rojo de tamaño {r})\n")
        f.write(f"c   - K_{s} azul (clique azul de tamaño {s})\n")
        f.write(f"c\n")
        f.write(f"c Si UNSAT => Rψ({r},{s}) ≤ {n} está certificado\n")
        f.write(f"c Si SAT   => Existe contraejemplo (coloración válida)\n")
        f.write(f"c\n")
        
        # Línea de formato DIMACS
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        
        # Escribir cláusulas
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"✓ Instancia SAT generada: {output_file}")
    print(f"  Variables: {num_vars}")
    print(f"  Cláusulas: {num_clauses}")


def main():
    """Función principal para generar instancias SAT desde línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Generador de Instancias SAT para Rψ(r,s) ≤ n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Generar instancia para Rψ(5,5) ≤ 16
  python generate_rpsi_sat.py -n 16 -r 5 -s 5 -o ../data/rpsi_5_5_n16.cnf
  
  # Generar instancia para Rψ(4,4) ≤ 10
  python generate_rpsi_sat.py -n 10 -r 4 -s 4 -o ../data/rpsi_4_4_n10.cnf

Formato de salida: DIMACS CNF (estándar para SAT solvers)
        """
    )
    
    parser.add_argument('-n', '--nodes', type=int, required=True,
                       help='Número de nodos (vértices) en el grafo completo K_n')
    parser.add_argument('-r', '--red-clique', type=int, required=True,
                       help='Tamaño del clique rojo monocromático prohibido')
    parser.add_argument('-s', '--blue-clique', type=int, required=True,
                       help='Tamaño del clique azul monocromático prohibido')
    parser.add_argument('-o', '--output', type=str, required=True,
                       help='Archivo de salida (formato DIMACS CNF)')
    
    args = parser.parse_args()
    
    print("="*70)
    print("  Generador de Instancias SAT - Ramsey Vibracional")
    print(f"  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    print(f"\nGenerando instancia para Rψ({args.red_clique},{args.blue_clique}) ≤ {args.nodes}...")
    
    # Generar instancia
    edge_map, cnf_clauses = generate_rpsi_sat_instance(args.nodes, args.red_clique, args.blue_clique)
    
    # Escribir a archivo
    write_dimacs_cnf(edge_map, cnf_clauses, args.output, args.red_clique, args.blue_clique, args.nodes)
    
    print(f"\n✓ Instancia SAT generada exitosamente")
    print(f"  Archivo: {args.output}")
    print("\nPara resolver con un SAT solver (ej. Kissat, CaDiCaL):")
    print(f"  kissat {args.output}")
    print("="*70)


if __name__ == "__main__":
    main()
