#!/usr/bin/env python3
"""
Script to generate SAT instance for R_ψ(5,5) ≤ 16

This script generates the SAT instance in DIMACS format that can be solved
with Kissat to obtain an UNSAT certificate proving R_ψ(5,5) ≤ 16.
"""

from ramsey_vibracional import generate_rpsi_sat_instance_tseytin, save_dimacs

def main():
    print("="*70)
    print("  Generación de Instancia SAT para R_ψ(5,5) ≤ 16")
    print("  Codificación Tseytin con resonancia vibracional")
    print("  Frecuencia base: f₀ = 141.7001 Hz")
    print("  Umbral de resonancia: ε = 0.037")
    print("  Grid de discretización: 128 puntos")
    print("="*70)
    print()
    
    # Generar instancia SAT
    print("🔧 Generando instancia SAT para R_ψ(5,5) ≤ 16...")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n=16, r=5, s=5,
        f0=141.7001, eps=0.037, grid=128
    )
    
    print()
    print("✅ Instancia SAT generada exitosamente:")
    print(f"   Número total de variables: {num_vars:,}")
    print(f"   Número total de cláusulas: {num_clauses:,}")
    print()
    
    # Guardar en formato DIMACS
    output_file = "data/rpsi_5_5_n16.cnf"
    save_dimacs(clauses, num_vars, num_clauses, output_file)
    print()
    
    print("="*70)
    print("  Próximos pasos para certificación formal:")
    print("="*70)
    print()
    print("1. Resolver con Kissat SAT solver:")
    print("   $ kissat --lrat data/rpsi_5_5_n16.cnf > cert/rpsi_5_5_n16_unsat.lrat")
    print()
    print("2. Si resultado es UNSAT:")
    print("   → R_ψ(5,5) ≤ 16 formalmente verificado ✓")
    print()
    print("3. Formalizar en Lean 4:")
    print("   → Archivo: proofs/Rpsi_5_5_le_16.lean")
    print("   → Conectar con certificado LRAT")
    print()
    print("="*70)

if __name__ == "__main__":
    main()
