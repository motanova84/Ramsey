#!/usr/bin/env python3
"""
Ejemplo 1: Cálculo de Valores Exactos R_ψ(r,s)

Este script calcula valores exactos de la función de Ramsey vibracional
usando verificación SAT con el solver Z3.
"""

import sys
sys.path.insert(0, '..')

from ramsey_vibracional import calcular_Rpsi_exacto, estimar_conjetura

def main():
    print("="*70)
    print("  Ejemplo 1: Cálculo de Valores Exactos R_ψ(r,s)")
    print("  Frecuencia Base: 141.7001 Hz")
    print("="*70)
    print()
    
    # Lista de pares (r,s) para calcular
    casos = [
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 4),
        (4, 5),
        (5, 5)
    ]
    
    resultados = []
    
    for r, s in casos:
        print(f"\n{'='*70}")
        print(f"Calculando R_ψ({r},{s})")
        print(f"{'='*70}")
        
        # Calcular valor exacto
        R_psi_exacto = calcular_Rpsi_exacto(r, s, nmax=30, grid=64)
        
        # Estimación teórica
        R_psi_conjetura = estimar_conjetura(r, s)
        
        if R_psi_exacto:
            error = abs(R_psi_exacto - R_psi_conjetura) / R_psi_exacto * 100
            
            resultados.append({
                'r': r,
                's': s,
                'exacto': R_psi_exacto,
                'conjetura': R_psi_conjetura,
                'error': error
            })
            
            print(f"\n✨ Resultados para ({r},{s}):")
            print(f"   R_ψ exacto:     {R_psi_exacto}")
            print(f"   Conjetura:      {R_psi_conjetura}")
            print(f"   Error:          {error:.1f}%")
        else:
            print(f"\n⚠️  No se encontró valor en rango [1,30]")
    
    # Resumen final
    if resultados:
        print(f"\n\n{'='*70}")
        print("📊 RESUMEN DE RESULTADOS")
        print(f"{'='*70}\n")
        
        print(f"{'Par (r,s)':<12} {'R_ψ Exacto':<15} {'Conjetura':<15} {'Error %':<10}")
        print("-"*70)
        
        for res in resultados:
            print(f"({res['r']},{res['s']}){' '*8} {res['exacto']:<15} {res['conjetura']:<15} {res['error']:<10.1f}")
        
        error_promedio = sum(r['error'] for r in resultados) / len(resultados)
        print(f"\n{'='*70}")
        print(f"Error Promedio: {error_promedio:.1f}%")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
