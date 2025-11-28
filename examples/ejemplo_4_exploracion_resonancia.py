#!/usr/bin/env python3
"""
Ejemplo 4: Exploración de Resonancia Vibracional

Este script explora cómo diferentes frecuencias y umbrales afectan
la formación de cliques en grafos vibracionales.
"""

import sys
sys.path.insert(0, '..')

from ramsey_vibracional import (
    resonancia_detectada, 
    generar_coloracion_vibracional,
    encontrar_clique_maximo
)
import numpy as np

def explorar_umbrales(frecuencias, f0=141.7001):
    """Explora diferentes umbrales de resonancia"""
    
    umbrales = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]
    
    print(f"\n🔬 Explorando Umbrales de Resonancia")
    print(f"   Frecuencias de prueba: {len(frecuencias)} vértices")
    print(f"   Frecuencia base f₀: {f0} Hz\n")
    
    print(f"{'Umbral ε (Hz)':<20} {'Aristas Azules':<20} {'Aristas Rojas':<20} {'Clique ⚫ max':<15} {'Clique 🔴 max':<15}")
    print("-"*90)
    
    for eps in umbrales:
        grafo = generar_coloracion_vibracional(frecuencias, eps=eps, f0=f0)
        
        aristas_azules = sum(1 for color in grafo.values() if color == 'azul')
        aristas_rojas = sum(1 for color in grafo.values() if color == 'rojo')
        
        clique_azul = encontrar_clique_maximo(grafo, 'azul')
        clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
        
        print(f"{eps:<20} {aristas_azules:<20} {aristas_rojas:<20} "
              f"{len(clique_azul):<15} {len(clique_rojo):<15}")

def explorar_distribucion_frecuencias(n=10, f0=141.7001):
    """Explora diferentes distribuciones de frecuencias"""
    
    print(f"\n\n🎵 Explorando Distribuciones de Frecuencias")
    print(f"   Número de vértices: {n}")
    print(f"   Frecuencia base f₀: {f0} Hz\n")
    
    distribuciones = {
        'Uniforme': np.random.uniform(0, f0, n),
        'Normal': np.abs(np.random.normal(f0/2, f0/6, n)) % f0,
        'Exponencial': (np.random.exponential(f0/3, n)) % f0,
        'Armónica': [f0 * i / n for i in range(n)],
        'Fibonacci': [(f0 * (1.618**i)) % f0 for i in range(n)]
    }
    
    eps = 0.001  # Umbral fijo
    
    print(f"{'Distribución':<20} {'Aristas ⚫':<15} {'Aristas 🔴':<15} {'Clique ⚫':<15} {'Clique 🔴':<15}")
    print("-"*80)
    
    for nombre, freqs in distribuciones.items():
        grafo = generar_coloracion_vibracional(freqs, eps=eps, f0=f0)
        
        aristas_azules = sum(1 for color in grafo.values() if color == 'azul')
        aristas_rojas = sum(1 for color in grafo.values() if color == 'rojo')
        
        clique_azul = encontrar_clique_maximo(grafo, 'azul')
        clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
        
        print(f"{nombre:<20} {aristas_azules:<15} {aristas_rojas:<15} "
              f"{len(clique_azul):<15} {len(clique_rojo):<15}")

def matriz_resonancia(frecuencias, eps=0.001, f0=141.7001):
    """Muestra matriz de resonancia entre vértices"""
    
    n = len(frecuencias)
    print(f"\n\n🔮 Matriz de Resonancia ({n}x{n})")
    print(f"   ⚫ = Resonancia (azul), • = No resonancia (rojo)")
    print(f"   Umbral ε = {eps} Hz\n")
    
    # Encabezado
    print("    ", end="")
    for i in range(n):
        print(f"{i:3}", end=" ")
    print()
    
    # Matriz
    for i in range(n):
        print(f"{i:3} ", end="")
        for j in range(n):
            if i == j:
                print(" - ", end=" ")
            elif resonancia_detectada(frecuencias[i], frecuencias[j], eps, f0):
                print(" ⚫ ", end=" ")
            else:
                print(" • ", end=" ")
        print()

def main():
    print("="*90)
    print("  Ejemplo 4: Exploración de Resonancia Vibracional")
    print("  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*90)
    
    # Generar frecuencias de prueba
    np.random.seed(42)  # Para reproducibilidad
    frecuencias = np.random.uniform(0, 141.7001, 10)
    
    # Explorar umbrales
    explorar_umbrales(frecuencias)
    
    # Explorar distribuciones
    explorar_distribucion_frecuencias(n=12)
    
    # Matriz de resonancia (ejemplo pequeño)
    frecuencias_pequeño = np.random.uniform(0, 141.7001, 6)
    matriz_resonancia(frecuencias_pequeño)
    
    print(f"\n{'='*90}")
    print("🔍 Observaciones Clave:")
    print("-"*90)
    print("• Umbral más pequeño → menos resonancias → más aristas rojas")
    print("• Umbral más grande → más resonancias → más aristas azules")
    print("• Distribuciones armónicas favorecen patrones coherentes")
    print("• La proporción áurea (Fibonacci) genera estructuras especiales")
    print(f"{'='*90}\n")

if __name__ == "__main__":
    main()
