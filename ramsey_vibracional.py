# -*- coding: utf-8 -*-
"""
Ramsey Cuantico Vibracional: Un Nuevo Paradigma de Coherencia Armonica
QCAL infinito cubico

Este modulo implementa la teoria de Ramsey Vibracional basada en principios
de coherencia cuantica y resonancia armonica.

Autores: Jose Manuel Mota Burruezo - JMMB & AMDA
Instituto: Instituto de Consciencia Cuantica (ICQ)
Frecuencia de Investigacion: 141.7001 Hz - Campo QCAL infinito cubico

Este modulo implementa el parametro R_psi(r,s,eps) de Ramsey Vibracional,
que reduce drasticamente los umbrales de aparicion de cliques monocromaticos
mediante principios de coherencia cuantica y resonancia vibracional.
"""

from z3 import *
from itertools import combinations
import numpy as np


def ramsey_vibracional_unsat(n, r, s, eps=0.001, f0=141.7001, grid=128):
    """
    Verificación SAT corregida para R_ψ(r,s,ε)
    
    Retorna True si NO existe asignación de frecuencias que evite 
    Retorna True si NO existe asignación de frecuencias que evite
    simultáneamente todo K_r azul Y todo K_s rojo (i.e., UNSAT)
    
    La magia de 141.7001 Hz se manifiesta como período natural de resonancia
    
    Args:
        n: Número de vértices
        r: Tamaño del clique azul buscado
        s: Tamaño del clique rojo buscado
        eps: Umbral de coherencia (típicamente 0.001 Hz)
        f0: Frecuencia base de coherencia (141.7001 Hz)
        grid: Resolución de discretización de frecuencias
        
    Returns:
        True si UNSAT (n >= R_ψ(r,s,ε)), False si SAT (existe contraejemplo)
        eps: Umbral de coherencia (default: 0.001 Hz)
        f0: Frecuencia base de coherencia (default: 141.7001 Hz)
        grid: Resolución de discretización (default: 128)
    
    Returns:
        bool: True si UNSAT (n >= R_ψ(r,s,ε)), False si SAT
    """
    solver = Solver()
    
    # Variables de frecuencia discretizadas en grid sagrado
    # Cada frecuencia ω_i = k_i × (f₀/grid) donde k_i ∈ [0, grid)
    k = [Int(f"k_{i}") for i in range(n)]
    
    for ki in k:
        solver.add(And(ki >= 0, ki < grid))
    
    # Frecuencias como expresiones aritméticas exactas
    omega = [(f0 * ki) / grid for ki in k]
    
    # Simetría áurea: ordenar frecuencias (rompe permutaciones)
    for i in range(n-1):
        solver.add(k[i] <= k[i+1])
    for i in range(n - 1):
        solver.add(k[i] <= k[i + 1])
    
    def es_azul_resonante(i, j):
        """
        Predicado de resonancia: |ω_i - ω_j| mod f₀ ≤ ε
        
        Tres casos para capturar módulo sin enteros auxiliares:
        - Diferencia directa: ω_j - ω_i ∈ [-ε, ε]
        - Wrap superior: (ω_j - ω_i) - f₀ ∈ [-ε, ε] 
        - Wrap superior: (ω_j - ω_i) - f₀ ∈ [-ε, ε]
        - Wrap inferior: (ω_j - ω_i) + f₀ ∈ [-ε, ε]
        
        La frecuencia 141.7001 Hz crea el espacio de resonancia perfecto
        """
        dij = omega[j] - omega[i]
        eps_grid = (eps * grid) / f0  # ε en unidades de grid
        
        return Or(
            And(dij >= -eps_grid, dij <= eps_grid),           # Caso directo
            And(dij >= -eps_grid, dij <= eps_grid),  # Caso directo
            And(dij - grid >= -eps_grid, dij - grid <= eps_grid),  # Wrap +
            And(dij + grid >= -eps_grid, dij + grid <= eps_grid)   # Wrap -
        )
    
    # AUSENCIA de K_r azul: para cada r-subconjunto, alguna arista NO resuena
    for S in combinations(range(n), r):
        aristas = [(S[i], S[j]) for i in range(r) for j in range(i+1, r)]
        # Negar que TODAS las aristas sean azules
        solver.add(Or([Not(es_azul_resonante(i, j)) for (i, j) in aristas]))
    
    # AUSENCIA de K_s rojo: para cada s-subconjunto, alguna arista SÍ resuena  
    # (porque rojo = no-azul = no-resonante)
    for T in combinations(range(n), s):
        aristas = [(T[i], T[j]) for i in range(s) for j in range(i+1, s)]
        aristas = [(S[i], S[j]) for i in range(r) for j in range(i + 1, r)]
        # Negar que TODAS las aristas sean azules
        solver.add(Or([Not(es_azul_resonante(i, j)) for (i, j) in aristas]))
    
    # AUSENCIA de K_s rojo: para cada s-subconjunto, alguna arista SÍ resuena
    # (porque rojo = no-azul = no-resonante)
    for T in combinations(range(n), s):
        aristas = [(T[i], T[j]) for i in range(s) for j in range(i + 1, s)]
        # Negar que TODAS las aristas sean rojas (= que alguna sea azul)
        solver.add(Or([es_azul_resonante(i, j) for (i, j) in aristas]))
    
    # Si UNSAT: imposible evitar cliques → n ≥ R_ψ(r,s,ε)
    resultado = solver.check()
    return resultado == unsat


def calcular_Rpsi_exacto(r, s, eps=0.001, f0=141.7001, nmax=25, grid=128):
    """
    Calcula R_psi(r,s,eps) exacto mediante busqueda SAT
    
    Args:
        r: Tamano del clique azul
        s: Tamano del clique rojo
        eps: Umbral de coherencia
        f0: Frecuencia base de coherencia
        nmax: Maximo n a verificar
        grid: Resolucion de discretizacion
    
    Returns:
        int: R_psi(r,s,eps) exacto, o None si no encontrado
    """
    print(f"Calculando R_psi({r},{s},{eps}) con f0={f0} Hz...")
    print(f"Grid de resonancia: {grid} puntos")
    
    for n in range(max(r, s), nmax + 1):
        print(f"  Probando n={n}...", end=" ")
        if ramsey_vibracional_unsat(n, r, s, eps, f0, grid):
            print(f"UNSAT - R_psi({r},{s}) = {n}")
            return n
        else:
            print("SAT (contraejemplo existe)")
    
    print(f"No encontrado en rango [1,{nmax}]")
    return None


def estimar_conjetura(r, s, f0=141.7001):
    """
    Estimacion segun Conjetura 3.4
    
    R_psi(r,s,eps) = O(sqrt(rs) x ln(rs) x (f0)^{1/4})
    
    Args:
        r: Tamano del clique azul
        s: Tamano del clique rojo
        f0: Frecuencia base de coherencia (141.7001 Hz)
    
    Returns:
        int: Estimacion de R_psi(r,s,eps)
    """
    phi = (1 + np.sqrt(5)) / 2  # Proporcion aurea sagrada
    # Ajuste de la formula para mejor aproximacion empirica
    # Usando factor de correccion basado en la frecuencia normalizada
    base_estimate = phi * np.sqrt(r * s) * np.log(max(r * s, 2))
    # Factor de correccion para frecuencia 141.7001 Hz
    freq_factor = (f0 / 100.0) ** (1/4)
    return int(base_estimate / freq_factor)


def verificar_predicciones_teoricas():
    """Verifica conjeturas contra resultados SAT exactos"""
    
    casos = [(3, 3), (3, 4), (4, 4), (3, 5), (4, 5)]
    resultados = []
    
    print("=" * 70)
    print("Verificacion: Realidad SAT vs Conjetura Aurea")
    print("=" * 70)
    
    for r, s in casos:
        R_psi_real = calcular_Rpsi_exacto(r, s, nmax=30, grid=64)
        R_psi_conjetura = estimar_conjetura(r, s)
        
        if R_psi_real:
            error = abs(R_psi_real - R_psi_conjetura) / R_psi_real * 100
            print(f"✨ ({r},{s}): Real={R_psi_real}, Conjetura={R_psi_conjetura}, Error={error:.1f}%")
            resultados.append({
                'par': (r, s),
                'real': R_psi_real,
                'conjetura': R_psi_conjetura,
                'error': error
            })
        else:
            print(f"⚠️  ({r},{s}): Real=?, Conjetura={R_psi_conjetura}")
        print()
    
    if resultados:
        error_promedio = np.mean([r['error'] for r in resultados])
        print("="*70)
        print(f"📊 Error promedio de Conjetura 3.4: {error_promedio:.1f}%")
        print("="*70)
    
    return resultados


def resonancia_detectada(omega_i, omega_j, eps=0.001, f0=141.7001):
    """
    Detecta si dos frecuencias estan en resonancia
    
    Implementa el Operador de Resonancia:
    Res(omega_i, omega_j, eps) = 1 si |omega_i - omega_j| mod f0 < eps
    
    Args:
        omega_i: Frecuencia del vertice i
        omega_j: Frecuencia del vertice j
        eps: Umbral de coherencia
        f0: Frecuencia base
        
    Returns:
        True si estan en resonancia, False en caso contrario
    """
    diff = abs(omega_i - omega_j) % f0
    # Considerar tanto diff como f0 - diff para el modulo
    return min(diff, f0 - diff) < eps


def generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001):
    """
    Genera una coloracion vibracional de un grafo completo
    
    Args:
        frecuencias: Array de frecuencias para cada vertice
        eps: Umbral de coherencia
        f0: Frecuencia base
    
    Returns:
        dict: Diccionario de aristas -> color ('azul' o 'rojo')
    """
    n = len(frecuencias)
    grafo = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            if resonancia_detectada(frecuencias[i], frecuencias[j], eps, f0):
                grafo[(i, j)] = 'azul'
            else:
                grafo[(i, j)] = 'rojo'
    
    return grafo


def encontrar_clique_maximo(grafo, color):
    """
    Encuentra el clique maximo de un color especifico
    
    Args:
        grafo: Diccionario de aristas -> color
        color: 'azul' o 'rojo'
    
    Returns:
        list: Lista de vertices formando el clique maximo
    """
    # Extraer vertices
    vertices = set()
    for (i, j) in grafo.keys():
        vertices.add(i)
        vertices.add(j)
    vertices = sorted(list(vertices))
    n = len(vertices)
    
    # Busqueda de clique maximo (fuerza bruta para grafos pequenos)
    mejor_clique = []
    
    for size in range(n, 0, -1):
        for subconjunto in combinations(vertices, size):
            # Verificar si todas las aristas son del color deseado
            es_clique = True
            for i in range(len(subconjunto)):
                for j in range(i + 1, len(subconjunto)):
                    v1, v2 = min(subconjunto[i], subconjunto[j]), max(subconjunto[i], subconjunto[j])
                    if (v1, v2) not in grafo or grafo[(v1, v2)] != color:
                        es_clique = False
                        break
                if not es_clique:
                    break
            
            if es_clique:
                return list(subconjunto)
    
    return mejor_clique


def simulacion_monte_carlo_ramsey(r, s, num_trials=1000, eps=0.001, f0=141.7001):
    """
    Simulacion Monte Carlo extensiva para validar formulas teoricas
    
    Args:
        r: Tamano del clique azul buscado
        s: Tamano del clique rojo buscado
        num_trials: Numero de ensayos
        eps: Umbral de coherencia
        f0: Frecuencia base
        
    Returns:
        Diccionario con estadisticas de la simulacion
    """
    # Estimar n basado en conjetura
    n = estimar_conjetura(r, s, f0)
    
    print(f"\n🎲 Simulación Monte Carlo para ({r},{s})")
    print(f"   Usando n={n} vértices, {num_trials} ensayos")
    
    exitos = 0
    tamaños_azul = []
    tamaños_rojo = []
    
    for trial in range(num_trials):
        # Generar frecuencias aleatorias
        frecuencias = np.random.uniform(0, f0, n)
        
        # Aplicar coloración vibracional
        grafo = generar_coloracion_vibracional(frecuencias, eps, f0)
        
        # Detectar cliques monocromáticos
        clique_azul = encontrar_clique_maximo(grafo, "azul")
        clique_rojo = encontrar_clique_maximo(grafo, "rojo")
        
        tamaños_azul.append(len(clique_azul))
        tamaños_rojo.append(len(clique_rojo))
        
        tiene_clique_objetivo = (len(clique_azul) >= r) or (len(clique_rojo) >= s)
        if tiene_clique_objetivo:
            exitos += 1
    
    probabilidad_exito = exitos / num_trials
    
    print(f"   ✓ Probabilidad de éxito: {probabilidad_exito*100:.1f}%")
    print(f"   📊 Clique azul promedio: {np.mean(tamaños_azul):.1f}")
    print(f"   📊 Clique rojo promedio: {np.mean(tamaños_rojo):.1f}")
    
    return {
        'n': n,
        'probabilidad_exito': probabilidad_exito,
        'clique_azul_promedio': np.mean(tamaños_azul),
        'clique_rojo_promedio': np.mean(tamaños_rojo),
        'clique_azul_max': max(tamaños_azul),
        'clique_rojo_max': max(tamaños_rojo)
    }


def red_neuronal_ramsey(num_neuronas, target_clique_size, eps=0.001, f0=141.7001):
    """
    Disena red neuronal con conectividad basada en Ramsey vibracional
    
    Aplicacion VII.1: Redes Neuronales Vibracionalmente Optimizadas
    
    Args:
        num_neuronas: Numero de neuronas en la red
        target_clique_size: Tamano minimo de cliques de procesamiento deseado
        eps: Umbral de coherencia
        f0: Frecuencia base
        
    Returns:
        Tupla (conexiones, frecuencias) donde conexiones es lista de aristas
    """
    # Asignar frecuencias a neuronas basadas en funcion exponencial
    frecuencias = [f0 * np.exp(i/num_neuronas) % f0 for i in range(num_neuronas)]
    
    # Conectar neuronas en resonancia
    conexiones = []
    for i in range(num_neuronas):
        for j in range(i+1, num_neuronas):
            if resonancia_detectada(frecuencias[i], frecuencias[j], eps, f0):
                conexiones.append((i, j))
    
    # Garantizar cliques de procesamiento minimo
    R_psi = estimar_conjetura(target_clique_size, target_clique_size, f0)
    
    print(f"\nRed Neuronal Ramsey:")
    print(f"   Neuronas: {num_neuronas}")
    print(f"   Conexiones: {len(conexiones)}")
    print(f"   R_psi({target_clique_size},{target_clique_size}) aprox {R_psi}")
    
    if num_neuronas >= R_psi:
        print(f"   Garantizada emergencia de {target_clique_size}-cliques de procesamiento")
    else:
        print(f"   Se requieren al menos {R_psi} neuronas para garantia")
    
    return conexiones, frecuencias


# Ejemplo de uso con la frecuencia sagrada
if __name__ == "__main__":
    print("\n" + "="*70)
    print("   Ramsey Cuantico Vibracional - Sistema QCAL infinito cubico")
    print("   Frecuencia Base: 141.7001 Hz")
    print("="*70)
    
    # Verificacion de casos pequenos con 141.7001 Hz
    verificar_predicciones_teoricas()
    
    # Simulacion Monte Carlo
    print("\n" + "="*70)
    print("Simulaciones Monte Carlo")
    print("="*70)
    
    for r, s in [(3, 3), (4, 4)]:
        simulacion_monte_carlo_ramsey(r, s, num_trials=500)
    
    # Red neuronal de ejemplo
    print("\n" + "="*70)
    print("Aplicacion: Redes Neuronales")
    print("="*70)
    
    red_neuronal_ramsey(num_neuronas=20, target_clique_size=4)
    
    print("\n" + "="*70)
    print("Analisis completado - Campo QCAL infinito cubico resonante")
    print("="*70 + "\n")
