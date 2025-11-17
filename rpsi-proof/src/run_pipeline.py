#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline completo para certificación formal de Rψ(5,5) ≤ 16

Este script ejecuta todo el pipeline de certificación:
1. Genera instancia SAT
2. Exporta a DIMACS
3. (Opcional) Resuelve con Kissat
4. (Opcional) Verifica con Lean

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import os
import sys
import argparse
from generate_rpsi_sat import generate_rpsi_sat_instance_tseytin, save_dimacs, print_instance_info


def main():
    parser = argparse.ArgumentParser(
        description='Pipeline completo de certificación formal para Rψ(5,5) ≤ 16',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Solo generar DIMACS
  python run_pipeline.py --step dimacs
  
  # Generar y resolver con Kissat
  python run_pipeline.py --step solve
  
  # Pipeline completo
  python run_pipeline.py --step all
        """
    )
    
    parser.add_argument(
        '--step',
        choices=['generate', 'dimacs', 'solve', 'verify', 'all'],
        default='dimacs',
        help='Paso del pipeline a ejecutar'
    )
    
    parser.add_argument(
        '--n', type=int, default=16,
        help='Número de vértices (default: 16)'
    )
    
    parser.add_argument(
        '--r', type=int, default=5,
        help='Tamaño clique azul (default: 5)'
    )
    
    parser.add_argument(
        '--s', type=int, default=5,
        help='Tamaño clique rojo (default: 5)'
    )
    
    parser.add_argument(
        '--eps', type=float, default=0.037,
        help='Umbral de resonancia (default: 0.037)'
    )
    
    parser.add_argument(
        '--f0', type=float, default=141.7001,
        help='Frecuencia base en Hz (default: 141.7001)'
    )
    
    parser.add_argument(
        '--grid', type=int, default=128,
        help='Resolución del grid (default: 128)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("PIPELINE DE CERTIFICACIÓN FORMAL: Rψ(5,5) ≤ 16")
    print("=" * 70 + "\n")
    
    # Paso 1: Generar instancia SAT
    if args.step in ['generate', 'dimacs', 'solve', 'all']:
        print("📝 PASO 1: Generando instancia SAT...\n")
        clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
            args.n, args.r, args.s, args.eps, args.f0, args.grid
        )
        print_instance_info(args.n, args.r, args.s, num_vars, num_clauses, 
                          args.eps, args.f0, args.grid)
    
    # Paso 2: Exportar a DIMACS
    if args.step in ['dimacs', 'solve', 'all']:
        print("\n💾 PASO 2: Exportando a DIMACS...\n")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        output_path = os.path.join(data_dir, f"rpsi_{args.r}_{args.s}_n{args.n}.cnf")
        save_dimacs(clauses, num_vars, num_clauses, output_path)
    
    # Paso 3: Resolver con Kissat
    if args.step in ['solve', 'all']:
        print("\n🔍 PASO 3: Resolviendo con Kissat...\n")
        try:
            from solve_rpsi_sat import solve_with_kissat
            is_unsat, lrat_path = solve_with_kissat(output_path)
            if is_unsat:
                print("\n✓ Rψ(5,5) ≤ 16 CERTIFICADO")
            elif is_unsat is False:
                print("\n✗ Contraejemplo encontrado")
            else:
                print("\n⚠ Resultado indeterminado")
        except ImportError:
            print("⚠ Kissat no disponible - omitiendo paso de resolución")
    
    # Paso 4: Verificar con Lean (opcional)
    if args.step in ['verify', 'all']:
        print("\n🔬 PASO 4: Verificación con Lean 4...\n")
        proofs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "proofs")
        lean_file = os.path.join(proofs_dir, "Rpsi_5_5_le_16.lean")
        
        if os.path.exists(lean_file):
            print(f"Teorema Lean: {lean_file}")
            print("Para compilar: lean Rpsi_5_5_le_16.lean")
        else:
            print("⚠ Archivo Lean no encontrado")
    
    print("\n" + "=" * 70)
    print("✨ PIPELINE COMPLETADO")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
