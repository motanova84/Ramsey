#!/usr/bin/env python3
"""
Visualización de Resultados de Ramsey Vibracional

Este script genera visualizaciones ASCII de los resultados del modelo.
"""

import sys
sys.path.insert(0, '..')

from ramsey_vibracional import (
    calcular_Rpsi_exacto,
    estimar_conjetura,
    generar_coloracion_vibracional,
    encontrar_clique_maximo
)
import numpy as np


def grafico_barras_ascii(valores, etiquetas, titulo="", max_ancho=50):
    """Genera un gráfico de barras ASCII"""
    print(f"\n{titulo}")
    print("=" * (max_ancho + 20))
    
    if not valores:
        print("Sin datos para mostrar")
        return
    
    max_val = max(valores)
    
    for i, (val, label) in enumerate(zip(valores, etiquetas)):
        ancho = int((val / max_val) * max_ancho) if max_val > 0 else 0
        barra = "█" * ancho
        print(f"{label:<10} {barra} {val}")
    
    print()


def comparacion_ramsey_clasico_vs_vibracional():
    """Compara R(r,s) clásico vs R_ψ(r,s) vibracional"""
    
    print("\n" + "="*70)
    print("📊 COMPARACIÓN: R(r,s) CLÁSICO vs R_ψ(r,s) VIBRACIONAL")
    print("="*70)
    
    # Valores conocidos de Ramsey clásico
    valores_clasicos = {
        (3, 3): 6,
        (3, 4): 9,
        (4, 4): 18,
        (3, 5): 14,
        (4, 5): 25,
    }
    
    print("\nCalculando R_ψ con SAT (puede tomar unos segundos)...\n")
    
    etiquetas = []
    clasicos = []
    vibracionales = []
    reducciones = []
    
    for (r, s), R_clasico in valores_clasicos.items():
        R_psi = calcular_Rpsi_exacto(r, s, nmax=30, grid=64)
        
        if R_psi:
            etiquetas.append(f"({r},{s})")
            clasicos.append(R_clasico)
            vibracionales.append(R_psi)
            reduccion = ((R_clasico - R_psi) / R_clasico) * 100
            reducciones.append(reduccion)
    
    # Gráfico de comparación
    grafico_barras_ascii(
        clasicos,
        etiquetas,
        titulo="📈 R(r,s) CLÁSICO"
    )
    
    grafico_barras_ascii(
        vibracionales,
        etiquetas,
        titulo="🌟 R_ψ(r,s) VIBRACIONAL"
    )
    
    # Tabla de reducciones
    print("\n" + "="*70)
    print("🎯 REDUCCIÓN PORCENTUAL")
    print("="*70 + "\n")
    
    print(f"{'Par':<10} {'R(r,s)':<12} {'R_ψ(r,s)':<12} {'Reducción':<15}")
    print("-"*70)
    
    for i, label in enumerate(etiquetas):
        print(f"{label:<10} {clasicos[i]:<12} {vibracionales[i]:<12} {reducciones[i]:.1f}%")
    
    if reducciones:
        reduccion_promedio = np.mean(reducciones)
        print(f"\n{'Promedio':<10} {'':<12} {'':<12} {reduccion_promedio:.1f}%")
    
    print("\n" + "="*70)


def visualizar_grafo_vibracional(n=8):
    """Visualiza un grafo vibracional pequeño"""
    
    print("\n" + "="*70)
    print(f"🔮 GRAFO VIBRACIONAL ({n} vértices)")
    print("="*70 + "\n")
    
    # Generar frecuencias
    np.random.seed(42)
    frecuencias = np.random.uniform(0, 141.7001, n)
    
    print("🎵 Frecuencias de vértices:")
    for i, freq in enumerate(frecuencias):
        print(f"   v{i}: {freq:.4f} Hz")
    
    # Generar coloración
    grafo = generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001)
    
    # Contar aristas por color
    aristas_azules = sum(1 for c in grafo.values() if c == 'azul')
    aristas_rojas = sum(1 for c in grafo.values() if c == 'rojo')
    
    print(f"\n📊 Estadísticas:")
    print(f"   Total de aristas: {len(grafo)}")
    print(f"   Aristas azules (resonantes): {aristas_azules}")
    print(f"   Aristas rojas (no resonantes): {aristas_rojas}")
    
    # Matriz de adyacencia visual
    print(f"\n🔷 Matriz de Adyacencia:")
    print("   (⚫ = azul/resonante, • = rojo/no resonante)\n")
    
    print("    ", end="")
    for i in range(n):
        print(f"v{i} ", end="")
    print()
    
    for i in range(n):
        print(f"v{i}  ", end="")
        for j in range(n):
            if i == j:
                print(" - ", end=" ")
            elif i < j:
                color = grafo.get((i, j), 'rojo')
                simbolo = "⚫" if color == 'azul' else "•"
                print(f" {simbolo} ", end=" ")
            else:
                color = grafo.get((j, i), 'rojo')
                simbolo = "⚫" if color == 'azul' else "•"
                print(f" {simbolo} ", end=" ")
        print()
    
    # Encontrar cliques
    clique_azul = encontrar_clique_maximo(grafo, 'azul')
    clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
    
    print(f"\n🔍 Cliques Detectados:")
    print(f"   Clique azul máximo: {clique_azul} (tamaño {len(clique_azul)})")
    print(f"   Clique rojo máximo: {clique_rojo} (tamaño {len(clique_rojo)})")
    
    print("\n" + "="*70)


def curva_crecimiento():
    """Muestra curva de crecimiento de R_ψ vs conjetura"""
    
    print("\n" + "="*70)
    print("📈 CURVA DE CRECIMIENTO R_ψ(k,k)")
    print("="*70 + "\n")
    
    valores_k = range(3, 8)
    conjeturas = [estimar_conjetura(k, k) for k in valores_k]
    
    print(f"{'k':<10} {'R_ψ(k,k) Conjetura':<25} {'Visualización':<30}")
    print("-"*70)
    
    max_val = max(conjeturas)
    
    for k, conj in zip(valores_k, conjeturas):
        ancho = int((conj / max_val) * 30)
        barra = "█" * ancho
        print(f"{k:<10} {conj:<25} {barra}")
    
    print("\n🔍 Observaciones:")
    print("   • Crecimiento sub-exponencial (polinómico)")
    print("   • Patrón O(√(k²) × ln(k²)) = O(k × ln(k))")
    print("   • Contrasta con R(k,k) = 2^O(k×ln(k)) clásico")
    
    print("\n" + "="*70)


def main():
    print("\n" + "="*70)
    print("  🌟 VISUALIZACIÓN DE RAMSEY CUÁNTICO VIBRACIONAL 🌟")
    print("  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    
    # 1. Comparación con Ramsey clásico
    comparacion_ramsey_clasico_vs_vibracional()
    
    # 2. Visualización de grafo
    visualizar_grafo_vibracional(n=6)
    
    # 3. Curva de crecimiento
    curva_crecimiento()
    
    print("\n" + "="*70)
    print("✨ Visualización completada - Campo QCAL ∞³ resonante")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
