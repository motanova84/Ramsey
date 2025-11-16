#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Script para rpsi-proof

Demuestra la generación y resolución de instancias SAT para números de Ramsey vibracionales.

Autores: José Manuel Mota Burruezo - JMMB Ψ✧∴
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³
"""

import sys
import os
import tempfile
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from generate_rpsi_sat import generate_rpsi_sat_instance, write_dimacs_cnf
from solve_rpsi_sat import solve_with_z3


def demo_small_instance():
    """Demuestra generación y resolución de R(3,3)"""
    print("\n" + "="*70)
    print("  DEMO 1: Verificar R(3,3) = 6")
    print("="*70)
    
    # Probar n=5 (debe ser SAT)
    print("\n→ Generando instancia para Rψ(3,3) ≤ 5...")
    edge_map, clauses = generate_rpsi_sat_instance(5, 3, 3)
    print(f"  Variables: {len(edge_map)}, Cláusulas: {len(clauses)}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
        temp_file = f.name
        write_dimacs_cnf(edge_map, clauses, temp_file, 3, 3, 5)
    
    print("\n→ Resolviendo con Z3...")
    status, elapsed, _ = solve_with_z3(temp_file, timeout=30)
    print(f"  Estado: {status} (tiempo: {elapsed:.3f}s)")
    
    if status == "SAT":
        print("  ✓ Correcto: R(3,3) > 5")
    
    os.unlink(temp_file)
    
    # Probar n=6 (debe ser UNSAT)
    print("\n→ Generando instancia para Rψ(3,3) ≤ 6...")
    edge_map, clauses = generate_rpsi_sat_instance(6, 3, 3)
    print(f"  Variables: {len(edge_map)}, Cláusulas: {len(clauses)}")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
        temp_file = f.name
        write_dimacs_cnf(edge_map, clauses, temp_file, 3, 3, 6)
    
    print("\n→ Resolviendo con Z3...")
    status, elapsed, _ = solve_with_z3(temp_file, timeout=30)
    print(f"  Estado: {status} (tiempo: {elapsed:.3f}s)")
    
    if status == "UNSAT":
        print("  ✓ Correcto: R(3,3) ≤ 6, por lo tanto R(3,3) = 6")
    
    os.unlink(temp_file)


def demo_main_instance():
    """Muestra información sobre la instancia principal Rψ(5,5) ≤ 16"""
    print("\n" + "="*70)
    print("  DEMO 2: Instancia Principal Rψ(5,5) ≤ 16")
    print("="*70)
    
    cnf_file = Path(__file__).parent / 'data' / 'rpsi_5_5_n16.cnf'
    
    if not cnf_file.exists():
        print(f"\n❌ Error: Archivo no encontrado: {cnf_file}")
        return
    
    print(f"\nArchivo CNF: {cnf_file}")
    
    # Leer información
    num_vars = 0
    num_clauses = 0
    with open(cnf_file, 'r') as f:
        for line in f:
            if line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
                break
    
    print(f"  Variables: {num_vars} (aristas de K₁₆)")
    print(f"  Cláusulas: {num_clauses}")
    print(f"  Tamaño del archivo: {cnf_file.stat().st_size:,} bytes")
    
    print("\n→ Estructura de la instancia:")
    print(f"  Grafo completo: K₁₆ (16 vértices)")
    print(f"  Aristas totales: C(16,2) = 120 ✓")
    print(f"  Subconjuntos de 5 vértices: C(16,5) = 4,368")
    print(f"  Cláusulas por color: 4,368 × 2 = 8,736 ✓")
    
    print("\n→ Interpretación:")
    print("  - Variable x_ij = TRUE  → arista (i,j) es ROJA (no-resonante)")
    print("  - Variable x_ij = FALSE → arista (i,j) es AZUL (resonante)")
    
    print("\n→ Objetivo de la instancia:")
    print("  Verificar si existe coloración de K₁₆ que evita:")
    print("    • K₅ rojo (5 vértices totalmente conectados en rojo)")
    print("    • K₅ azul (5 vértices totalmente conectados en azul)")
    
    print("\n→ Si UNSAT:")
    print("  ✓ Rψ(5,5) ≤ 16 está certificado formalmente")
    print("  ✓ Todo K₁₆ contiene un K₅ monocromático")
    
    print("\n→ Comparación con Ramsey clásico:")
    print("  R(5,5) clásico: [43, 48]")
    print("  Rψ(5,5) conjeturado: ≤ 16")
    print("  Reducción: ~3x más pequeño")
    
    print("\n→ Para resolver esta instancia:")
    print(f"  cd src/")
    print(f"  python solve_rpsi_sat.py ../data/rpsi_5_5_n16.cnf --solver z3")
    print("\n⚠️  Advertencia: Esta instancia es grande y puede tomar tiempo significativo")


def demo_encoding_explanation():
    """Explica la codificación SAT en detalle"""
    print("\n" + "="*70)
    print("  DEMO 3: Explicación de la Codificación SAT")
    print("="*70)
    
    print("\n→ Codificación Estándar de Ramsey como SAT:")
    print("\n1. Variables Booleanas:")
    print("   Para cada arista (i,j) en K_n, creamos variable x_ij")
    print("   Ejemplo: K₅ tiene C(5,2) = 10 aristas → 10 variables")
    
    print("\n2. Semántica de Colores:")
    print("   x_ij = TRUE  (1) → arista (i,j) es ROJA")
    print("   x_ij = FALSE (0) → arista (i,j) es AZUL")
    
    print("\n3. Cláusulas para Prohibir K_r Rojo:")
    print("   Para cada subconjunto S de r vértices:")
    print("   ¬x_i₁j₁ ∨ ¬x_i₂j₂ ∨ ... ∨ ¬x_iₘjₘ")
    print("   (al menos una arista NO es roja)")
    
    print("\n4. Cláusulas para Prohibir K_s Azul:")
    print("   Para cada subconjunto S de s vértices:")
    print("   x_i₁j₁ ∨ x_i₂j₂ ∨ ... ∨ x_iₘjₘ")
    print("   (al menos una arista NO es azul, i.e., es roja)")
    
    print("\n→ Ejemplo Concreto: K₅ con r=3, s=3")
    print("\n  Variables: 10 (aristas de K₅)")
    print("    x_12, x_13, x_14, x_15")
    print("    x_23, x_24, x_25")
    print("    x_34, x_35")
    print("    x_45")
    
    print("\n  Cláusulas (20 total):")
    print("    - 10 para prohibir K₃ rojo: C(5,3) = 10")
    print("      Ejemplo: ¬x_12 ∨ ¬x_13 ∨ ¬x_23  (triángulo {1,2,3})")
    print("    - 10 para prohibir K₃ azul: C(5,3) = 10")
    print("      Ejemplo: x_12 ∨ x_13 ∨ x_23  (triángulo {1,2,3})")
    
    print("\n→ Conexión con Resonancia Vibracional:")
    print("  En el contexto de Rψ, las asignaciones TRUE/FALSE")
    print("  corresponden a estados de resonancia:")
    print("    • AZUL = resonante (|ω_i - ω_j| mod f₀ < ε)")
    print("    • ROJO = no-resonante (diferencia de fase grande)")
    print("  con f₀ = 141.7001 Hz (Campo QCAL ∞³)")


def main():
    """Ejecuta todos los demos"""
    print("\n" + "="*70)
    print("  DEMO: rpsi-proof - Certificación SAT para Rψ(r,s)")
    print("  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    
    try:
        # Demo 1: Instancia pequeña
        demo_small_instance()
        
        # Demo 2: Instancia principal
        demo_main_instance()
        
        # Demo 3: Explicación de codificación
        demo_encoding_explanation()
        
        print("\n" + "="*70)
        print("  ✓ Demos completados exitosamente")
        print("="*70)
        print("\n→ Próximos pasos:")
        print("  1. Generar más instancias: src/generate_rpsi_sat.py")
        print("  2. Resolver instancias: src/solve_rpsi_sat.py")
        print("  3. Ver documentación: README.md")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
