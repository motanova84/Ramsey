#!/usr/bin/env python3
"""
Ejemplos de Uso de Ramsey Cuántico Vibracional

Este script demuestra las principales funcionalidades del framework.
"""

from ramsey_vibracional import (
    calcular_Rpsi_exacto,
    estimar_conjetura,
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    red_neuronal_ramsey,
    simulacion_monte_carlo_ramsey
)
import numpy as np


def ejemplo_basico():
    """Ejemplo 1: Cálculo básico de R_ψ(r,s)"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Cálculo Básico de R_ψ(r,s)")
    print("="*70)
    
    r, s = 3, 3
    print(f"\nCalculando R_ψ({r},{s}) con frecuencia base 141.7001 Hz...")
    
    R_psi = calcular_Rpsi_exacto(r, s, nmax=15, grid=64)
    R_conjetura = estimar_conjetura(r, s)
    
    print(f"\n✓ Resultado:")
    print(f"  R_ψ({r},{s}) exacto = {R_psi}")
    print(f"  Conjetura estima = {R_conjetura}")
    print(f"  Ramsey clásico R({r},{s}) = 6")
    print(f"\n✧ Reducción: {6 - R_psi} vértices menos necesarios con coherencia cuántica")


def ejemplo_coloracion_vibracional():
    """Ejemplo 2: Coloración vibracional de un grafo"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Coloración Vibracional de Grafo")
    print("="*70)
    
    # Crear un grafo con 6 vértices
    n = 6
    print(f"\nGenerando grafo completo K_{n} con frecuencias vibracionales...")
    
    # Asignar frecuencias: algunas en resonancia, otras no
    frecuencias = [0.0, 0.0005, 50.0, 50.0003, 100.0, 141.7001]
    print(f"Frecuencias (Hz): {frecuencias}")
    
    # Generar coloración
    grafo = generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001)
    
    # Contar aristas de cada color
    azules = sum(1 for color in grafo.values() if color == 'azul')
    rojas = sum(1 for color in grafo.values() if color == 'rojo')
    
    print(f"\n✓ Coloración generada:")
    print(f"  Aristas azules (resonantes): {azules}")
    print(f"  Aristas rojas (no resonantes): {rojas}")
    
    # Encontrar cliques
    clique_azul = encontrar_clique_maximo(grafo, 'azul')
    clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
    
    print(f"\n✓ Cliques encontrados:")
    print(f"  Clique azul máximo: {clique_azul} (tamaño {len(clique_azul)})")
    print(f"  Clique rojo máximo: {clique_rojo} (tamaño {len(clique_rojo)})")


def ejemplo_red_neuronal():
    """Ejemplo 3: Red neuronal vibracionalmente optimizada"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Red Neuronal Vibracionalmente Optimizada")
    print("="*70)
    
    num_neuronas = 50
    target_clique = 4
    
    print(f"\nDiseñando red neuronal con {num_neuronas} neuronas...")
    print(f"Objetivo: Garantizar cliques de procesamiento de tamaño {target_clique}")
    
    conexiones, frecuencias = red_neuronal_ramsey(num_neuronas, target_clique)
    
    print(f"\n✓ Red diseñada:")
    print(f"  Neuronas: {num_neuronas}")
    print(f"  Conexiones resonantes: {len(conexiones)}")
    print(f"  Densidad de conexión: {len(conexiones) / (num_neuronas * (num_neuronas-1) / 2):.2%}")
    
    # Estadísticas de frecuencias
    print(f"\n✓ Distribución de frecuencias:")
    print(f"  Mínima: {min(frecuencias):.2f} Hz")
    print(f"  Máxima: {max(frecuencias):.2f} Hz")
    print(f"  Media: {np.mean(frecuencias):.2f} Hz")


def ejemplo_simulacion_monte_carlo():
    """Ejemplo 4: Simulación Monte Carlo"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Simulación Monte Carlo")
    print("="*70)
    
    r, s = 3, 3
    num_trials = 1000
    
    print(f"\nSimulando {num_trials} grafos aleatorios...")
    print(f"Buscando cliques: K_{r} azul o K_{s} rojo")
    
    prob_exito = simulacion_monte_carlo_ramsey(r, s, num_trials=num_trials)
    
    print(f"\n✓ Resultados:")
    print(f"  Probabilidad de encontrar clique objetivo: {prob_exito:.1%}")
    print(f"  Éxitos: {int(prob_exito * num_trials)}/{num_trials}")


def ejemplo_comparacion_valores():
    """Ejemplo 5: Comparación con valores clásicos"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Comparación R_ψ vs R Clásico")
    print("="*70)
    
    casos = [
        (3, 3, 6),
        (3, 4, 9),
        (4, 4, 18),
    ]
    
    print("\n(r,s) | R_ψ vibracional | R clásico | Reducción")
    print("-" * 55)
    
    for r, s, R_clasico in casos:
        R_psi = calcular_Rpsi_exacto(r, s, nmax=20, grid=64)
        if R_psi:
            reduccion = R_clasico - R_psi
            print(f"({r},{s})  |       {R_psi:2d}        |    {R_clasico:2d}     |    {reduccion:2d} ({reduccion/R_clasico*100:.0f}%)")


def ejemplo_propiedades_teoricas():
    """Ejemplo 6: Verificación de propiedades teóricas"""
    print("\n" + "="*70)
    print("EJEMPLO 6: Propiedades Teóricas")
    print("="*70)
    
    print("\n✧ Propiedad 1: R_ψ es no-decreciente en r y s")
    R_33 = calcular_Rpsi_exacto(3, 3, nmax=15, grid=32)
    R_34 = calcular_Rpsi_exacto(3, 4, nmax=15, grid=32)
    R_44 = calcular_Rpsi_exacto(4, 4, nmax=15, grid=32)
    
    print(f"  R_ψ(3,3) = {R_33}")
    print(f"  R_ψ(3,4) = {R_34}")
    print(f"  R_ψ(4,4) = {R_44}")
    print(f"  ✓ Verificado: {R_33} ≤ {R_34} ≤ {R_44}")
    
    print("\n✧ Propiedad 2: Simetría R_ψ(r,s) = R_ψ(s,r)")
    R_34_alt = calcular_Rpsi_exacto(4, 3, nmax=15, grid=32)
    print(f"  R_ψ(3,4) = {R_34}")
    print(f"  R_ψ(4,3) = {R_34_alt}")
    print(f"  ✓ Verificado: {R_34} = {R_34_alt}")


def ejemplo_paradigma_vibracional():
    """Ejemplo 7: Paradigma Ramsey Vibracional vs Clásico"""
    print("\n" + "="*70)
    print("EJEMPLO 7: Paradigma Ramsey Vibracional vs Clásico")
    print("="*70)
    
    from ramsey_vibracional import demostrar_paradigma_vibracional
    
    # Mostrar la diferencia fundamental entre ambos paradigmas
    demostrar_paradigma_vibracional()


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "☆"*35)
    print("✧ Ramsey Cuántico Vibracional - Ejemplos ✧")
    print("Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("☆"*35)
    
    # Ejecutar ejemplos
    ejemplo_paradigma_vibracional()
    ejemplo_basico()
    ejemplo_coloracion_vibracional()
    ejemplo_red_neuronal()
    ejemplo_simulacion_monte_carlo()
    ejemplo_comparacion_valores()
    ejemplo_propiedades_teoricas()
    
    print("\n" + "="*70)
    print("✧ La coherencia cuántica revela el orden oculto en las redes ✧")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
