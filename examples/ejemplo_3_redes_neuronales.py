#!/usr/bin/env python3
"""
Ejemplo 3: Aplicación a Redes Neuronales

Este script demuestra cómo usar Ramsey vibracional para diseñar
redes neuronales con conectividad optimizada.
"""

import sys
sys.path.insert(0, '..')

from ramsey_vibracional import red_neuronal_ramsey, estimar_conjetura
import numpy as np

def analizar_red(conexiones, frecuencias):
    """Analiza las propiedades de la red neuronal"""
    n = len(frecuencias)
    
    # Grado de cada neurona
    grados = {i: 0 for i in range(n)}
    for i, j in conexiones:
        grados[i] += 1
        grados[j] += 1
    
    grado_promedio = np.mean(list(grados.values()))
    grado_max = max(grados.values()) if grados else 0
    
    return {
        'grado_promedio': grado_promedio,
        'grado_max': grado_max,
        'densidad': len(conexiones) / (n * (n - 1) / 2) if n > 1 else 0
    }

def main():
    print("="*70)
    print("  Ejemplo 3: Redes Neuronales Vibracionalmente Optimizadas")
    print("  Frecuencia Base: 141.7001 Hz")
    print("="*70)
    print()
    
    # Diferentes configuraciones de redes
    configuraciones = [
        {'neuronas': 10, 'clique_size': 3},
        {'neuronas': 20, 'clique_size': 4},
        {'neuronas': 30, 'clique_size': 4},
        {'neuronas': 50, 'clique_size': 5},
    ]
    
    for i, config in enumerate(configuraciones, 1):
        print(f"\n{'='*70}")
        print(f"Configuración {i}: {config['neuronas']} neuronas, cliques de {config['clique_size']}")
        print(f"{'='*70}\n")
        
        conexiones, frecuencias = red_neuronal_ramsey(
            num_neuronas=config['neuronas'],
            target_clique_size=config['clique_size']
        )
        
        # Analizar propiedades
        stats = analizar_red(conexiones, frecuencias)
        
        print(f"\n📊 Análisis de la Red:")
        print(f"   • Conexiones totales: {len(conexiones)}")
        print(f"   • Grado promedio: {stats['grado_promedio']:.2f}")
        print(f"   • Grado máximo: {stats['grado_max']}")
        print(f"   • Densidad de red: {stats['densidad']*100:.1f}%")
        
        # Mostrar algunas frecuencias de ejemplo
        print(f"\n🎵 Frecuencias de Neuronas (primeras 5):")
        for idx in range(min(5, len(frecuencias))):
            print(f"   Neurona {idx}: {frecuencias[idx]:.4f} Hz")
    
    # Análisis teórico
    print(f"\n\n{'='*70}")
    print("📈 ANÁLISIS TEÓRICO")
    print(f"{'='*70}\n")
    
    print("Requisitos mínimos de neuronas para garantizar cliques:\n")
    print(f"{'Tamaño Clique':<20} {'R_ψ(k,k) Estimado':<20} {'Neuronas Requeridas':<20}")
    print("-"*70)
    
    for k in [3, 4, 5, 6, 7]:
        R_psi = estimar_conjetura(k, k)
        print(f"{k:<20} {R_psi:<20} ≥ {R_psi}")
    
    print(f"\n{'='*70}")
    print("🔍 Conclusión:")
    print("-"*70)
    print("• Las redes pequeñas (<20 neuronas) tienen baja conectividad")
    print("• Redes más grandes garantizan cliques de procesamiento robusto")
    print("• La resonancia vibracional optimiza la arquitectura de red")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
