#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración: Dogma vs Humildad Epistemológica
==============================================

Este script demuestra la diferencia entre:
- θ = 0 (dogma): Afirmar sin medición, universo cerrado y estéril
- θ ≈ 0.052463 rad (medición): Humildad epistemológica basada en observación

Autor: QCAL ∞³ Framework (JMMB Ψ)
Fecha: 2026-04-17
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from symbiotic_coherence_v9 import (
    MultiScaleConvergenceAnalyzer,
    PerturbationConfig,
    KAPPA_PI,
    C_EST_TARGET,
)


def print_header():
    """Imprime el encabezado del demo"""
    print()
    print("=" * 80)
    print("  DOGMA vs HUMILDAD EPISTEMOLÓGICA")
    print("  θ = 0 (afirmación) vs θ ≈ 0.052463 rad (medición)")
    print("=" * 80)
    print()
    print("Cita: 'Afirmar θ = 0 es dogma (universo cerrado, estéril).'")
    print("      'Medir θ ≈ 0.052463 rad es humildad epistemológica.'")
    print("                                                    — JMMB Ψ")
    print()


def compare_approaches():
    """Compara el enfoque dogmático vs epistemológico"""
    analyzer = MultiScaleConvergenceAnalyzer()
    
    # Configuraciones a comparar
    configs = [
        {
            'name': 'Dogmático (θ=0)',
            'config': PerturbationConfig(eta=0.0, delta_zeta=0.0),
            'description': 'Afirmación sin medición - universo cerrado'
        },
        {
            'name': 'Epistemológico (θ≈0.052463 rad)',
            'config': PerturbationConfig(),  # Usa el default con delta_zeta=0.052463
            'description': 'Medición empírica - apertura al ajuste'
        }
    ]
    
    print()
    print("-" * 80)
    print("COMPARACIÓN DE ENFOQUES")
    print("-" * 80)
    print()
    
    results = []
    
    for cfg in configs:
        print(f"🔬 {cfg['name']}")
        print(f"   {cfg['description']}")
        print()
        
        # Calcular C_est con cada configuración
        n_modes = 100
        c_est, density = analyzer.compute_c_est(n_modes, cfg['config'])
        
        # Calcular métricas
        error_rel = abs(c_est - KAPPA_PI) / KAPPA_PI * 100
        coherent = error_rel < 5.0
        
        results.append({
            'name': cfg['name'],
            'c_est': c_est,
            'error': error_rel,
            'coherent': coherent,
            'config': cfg['config']
        })
        
        print(f"   C_est calculado: {c_est:.6f}")
        print(f"   κ_Π (teórico):   {KAPPA_PI:.6f}")
        print(f"   Error relativo:  {error_rel:.4f}%")
        print(f"   Estado:          {'✅ Coherente' if coherent else '❌ Incoherente'}")
        print()
    
    # Resumen comparativo
    print()
    print("=" * 80)
    print("RESUMEN COMPARATIVO")
    print("=" * 80)
    print()
    
    dogmatic = results[0]
    epistemic = results[1]
    
    print(f"{'Métrica':<30} {'Dogmático':<20} {'Epistemológico':<20}")
    print("-" * 80)
    print(f"{'θ (despl. frecuencial)':<30} {dogmatic['config'].delta_zeta:<20.6f} {epistemic['config'].delta_zeta:<20.6f}")
    print(f"{'C_est':<30} {dogmatic['c_est']:<20.6f} {epistemic['c_est']:<20.6f}")
    print(f"{'Error relativo (%)':<30} {dogmatic['error']:<20.4f} {epistemic['error']:<20.4f}")
    print(f"{'Coherencia':<30} {'✅' if dogmatic['coherent'] else '❌':<20} {'✅' if epistemic['coherent'] else '❌':<20}")
    print()
    
    # Conclusión
    print()
    print("=" * 80)
    print("CONCLUSIÓN")
    print("=" * 80)
    print()
    print("El enfoque epistemológico (θ ≈ 0.052463 rad) representa:")
    print()
    print("  ✓ Medición empírica basada en observación")
    print("  ✓ Apertura a revisión y ajuste")
    print("  ✓ Humildad epistemológica ante la incertidumbre")
    print("  ✓ Reconocimiento del contexto experimental")
    print()
    print("Mientras que el enfoque dogmático (θ = 0) implica:")
    print()
    print("  ✗ Afirmación sin evidencia experimental")
    print("  ✗ Universo cerrado sin posibilidad de ajuste")
    print("  ✗ Rigidez ante nueva información")
    print("  ✗ Certeza absoluta sin base empírica")
    print()
    print("La ciencia avanza con mediciones, no con dogmas.")
    print()


def main():
    """Función principal"""
    print_header()
    compare_approaches()
    print()
    print("=" * 80)
    print("  Fin de la demostración")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
