#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para guardar instancias SAT en formato DIMACS

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import os
import sys
from generate_rpsi_sat import generate_rpsi_sat_instance_tseytin, save_dimacs, print_instance_info


def main():
    """
    Genera y guarda instancia SAT para Rψ(5,5) ≤ 16
    """
    print("\n" + "=" * 70)
    print("GENERACIÓN DE ARCHIVO DIMACS PARA Rψ(5,5) ≤ 16")
    print("=" * 70 + "\n")
    
    # Parámetros oficiales
    n, r, s = 16, 5, 5
    eps = 0.037
    f0 = 141.7001
    grid = 128
    
    print(f"Parámetros:")
    print(f"  n = {n} (número de vértices)")
    print(f"  r = {r} (tamaño clique azul)")
    print(f"  s = {s} (tamaño clique rojo)")
    print(f"  ε = {eps}")
    print(f"  f₀ = {f0} Hz")
    print(f"  grid = {grid}")
    print("\n⏳ Generando instancia SAT...\n")
    
    # Generar instancia
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(n, r, s, eps, f0, grid)
    
    # Mostrar información
    print_instance_info(n, r, s, num_vars, num_clauses, eps, f0, grid)
    
    # Crear directorio data si no existe
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Guardar archivo DIMACS
    output_path = os.path.join(data_dir, "rpsi_5_5_n16.cnf")
    print(f"\n💾 Guardando archivo DIMACS...\n")
    save_dimacs(clauses, num_vars, num_clauses, output_path)
    
    print(f"\n✨ ¡ARCHIVO LISTO PARA KISSAT!")
    print(f"\nPara resolver con Kissat:")
    print(f"  kissat --lrat {output_path}")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
