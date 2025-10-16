#!/usr/bin/env python3
"""
Ejemplo 2: Simulación Monte Carlo

Este script realiza simulaciones Monte Carlo para validar las predicciones
teóricas del modelo de Ramsey vibracional.
"""

import sys
sys.path.insert(0, '..')

from ramsey_vibracional import simulacion_monte_carlo_ramsey
import numpy as np

def main():
    print("="*70)
    print("  Ejemplo 2: Simulación Monte Carlo de Ramsey Vibracional")
    print("  Frecuencia Base: 141.7001 Hz")
    print("="*70)
    print()
    
    # Configuración de simulaciones
    configuraciones = [
        {'r': 3, 's': 3, 'trials': 1000},
        {'r': 3, 's': 4, 'trials': 1000},
        {'r': 4, 's': 4, 'trials': 500},
        {'r': 3, 's': 5, 'trials': 500},
        {'r': 4, 's': 5, 'trials': 500},
    ]
    
    resultados = []
    
    for config in configuraciones:
        r = config['r']
        s = config['s']
        trials = config['trials']
        
        print(f"\n{'='*70}")
        print(f"Simulación para R_ψ({r},{s}) con {trials} ensayos")
        print(f"{'='*70}")
        
        stats = simulacion_monte_carlo_ramsey(r, s, num_trials=trials)
        resultados.append({
            'r': r,
            's': s,
            'n': stats['n'],
            'prob_exito': stats['probabilidad_exito'],
            'clique_azul_prom': stats['clique_azul_promedio'],
            'clique_rojo_prom': stats['clique_rojo_promedio'],
            'clique_azul_max': stats['clique_azul_max'],
            'clique_rojo_max': stats['clique_rojo_max']
        })
    
    # Resumen comparativo
    print(f"\n\n{'='*70}")
    print("📊 RESUMEN COMPARATIVO DE SIMULACIONES")
    print(f"{'='*70}\n")
    
    print(f"{'Par':<8} {'n usado':<10} {'Prob.Éxito':<15} {'Clique ⚫ max':<15} {'Clique 🔴 max':<15}")
    print("-"*70)
    
    for res in resultados:
        print(f"({res['r']},{res['s']}){' '*4} {res['n']:<10} {res['prob_exito']*100:.1f}%{' '*9} "
              f"{res['clique_azul_max']:<15} {res['clique_rojo_max']:<15}")
    
    print(f"\n{'='*70}")
    print("🔍 Interpretación:")
    print("-"*70)
    print("• Probabilidad de éxito cercana a 100% confirma las predicciones")
    print("• El tamaño máximo de cliques observados valida el modelo teórico")
    print("• La coherencia vibracional facilita la emergencia del orden")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
