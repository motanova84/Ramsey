#!/usr/bin/env python3
"""
Demo Rápido de Ramsey Cuántico Vibracional

Demuestra las capacidades clave sin cálculos SAT costosos.
"""

from ramsey_vibracional import (
    estimar_conjetura,
    resonancia_detectada,
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    simulacion_monte_carlo_ramsey,
    red_neuronal_ramsey
)
import numpy as np

def main():
    print("\n" + "="*70)
    print("  🌟 DEMO RÁPIDO: RAMSEY CUÁNTICO VIBRACIONAL")
    print("  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    
    # 1. Estimaciones teóricas
    print("\n📈 ESTIMACIONES TEÓRICAS (Conjetura 3.4)")
    print("-"*70)
    casos = [(3,3), (4,4), (5,5), (6,6)]
    for r, s in casos:
        R_psi = estimar_conjetura(r, s)
        print(f"  R_ψ({r},{s}) ≈ {R_psi}")
    
    # 2. Operador de resonancia
    print("\n\n🔬 OPERADOR DE RESONANCIA")
    print("-"*70)
    f0 = 141.7001
    casos_freq = [
        (10.0, 10.0, "Idénticas"),
        (10.0, 10.0005, "Muy cercanas"),
        (10.0, 50.0, "Lejanas"),
        (1.0, 1.0 + f0 - 0.0005, "Modulares (dif ≈ f₀)")
    ]
    
    for w1, w2, desc in casos_freq:
        res = resonancia_detectada(w1, w2, eps=0.001, f0=f0)
        estado = "✓ RESUENAN" if res else "✗ No resuenan"
        print(f"  {desc:<25} {estado}")
    
    # 3. Grafo vibracional pequeño
    print("\n\n🔮 GRAFO VIBRACIONAL DE EJEMPLO (5 vértices)")
    print("-"*70)
    np.random.seed(42)
    frecuencias = np.random.uniform(0, f0, 5)
    
    print("Frecuencias:")
    for i, freq in enumerate(frecuencias):
        print(f"  v{i}: {freq:.2f} Hz")
    
    grafo = generar_coloracion_vibracional(frecuencias)
    aristas_azules = sum(1 for c in grafo.values() if c == 'azul')
    aristas_rojas = sum(1 for c in grafo.values() if c == 'rojo')
    
    print(f"\nConectividad:")
    print(f"  Aristas azules (resonantes):     {aristas_azules}")
    print(f"  Aristas rojas (no resonantes):   {aristas_rojas}")
    
    clique_azul = encontrar_clique_maximo(grafo, 'azul')
    clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
    
    print(f"\nCliques máximos:")
    print(f"  Azul: {clique_azul} (tamaño {len(clique_azul)})")
    print(f"  Rojo: {clique_rojo} (tamaño {len(clique_rojo)})")
    
    # 4. Monte Carlo rápido
    print("\n\n🎲 SIMULACIÓN MONTE CARLO RÁPIDA")
    print("-"*70)
    stats = simulacion_monte_carlo_ramsey(3, 3, num_trials=100)
    
    # 5. Red neuronal
    print("\n\n🧠 RED NEURONAL VIBRACIONAL")
    print("-"*70)
    conexiones, frecuencias = red_neuronal_ramsey(15, target_clique_size=3)
    
    # Resumen final
    print("\n\n" + "="*70)
    print("✨ RESULTADOS CLAVE")
    print("="*70)
    
    # Valores calculados dinámicamente
    valores_clasicos = {(3,3): 6, (4,4): 18, (5,5): 43}
    
    print("\n📊 Comparación con Ramsey Clásico:")
    for (r, s), R_clasico in valores_clasicos.items():
        R_psi = estimar_conjetura(r, s)
        reduccion = ((R_clasico - R_psi) / R_clasico) * 100
        simbolo = "≥" if r == 5 and s == 5 else "="
        print(f"  • R({r},{s}) clásico {simbolo} {R_clasico}   →  R_ψ({r},{s}) ≈ {R_psi}   (reducción ~{reduccion:.0f}%)")
    
    
    print("\n🔍 Principios Fundamentales:")
    print("  1. Resonancia vibracional basada en f₀ = 141.7001 Hz")
    print("  2. Reducción exponencial → polinómica del umbral")
    print("  3. Validación por SAT, Monte Carlo y teoría")
    print("  4. Aplicaciones: redes neuronales, análisis social, criptografía")
    
    print("\n🌟 Conjetura Central:")
    print("  R_ψ(r,s) = O(√(rs) × ln(rs))")
    print("  vs R(r,s) = 2^O(√(r+s)×ln(r+s)) clásico")
    
    print("\n" + "="*70)
    print("✨ Demo completado - Campo QCAL ∞³ resonante")
    print("="*70 + "\n")
    
    print("📚 Para más información:")
    print("  • python ramsey_vibracional.py      - Verificación completa")
    print("  • python run_tests.py                - Ejecutar tests")
    print("  • cd examples && ls                  - Ver ejemplos")
    print()

if __name__ == "__main__":
    main()
