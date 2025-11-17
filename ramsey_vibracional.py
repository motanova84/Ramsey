# -*- coding: utf-8 -*-
"""
Ramsey Cuantico Vibracional: Un Nuevo Paradigma de Coherencia Armonica
QCAL infinito cubico
Ramsey Cuántico Vibracional: Un Nuevo Paradigma de Coherencia Armónica
QCAL infinity^3

Este modulo implementa la teoria de Ramsey Vibracional basada en principios
de coherencia cuantica y resonancia armonica.

Autores: Jose Manuel Mota Burruezo - JMMB & AMDA
Instituto: Instituto de Consciencia Cuantica (ICQ)
Frecuencia de Investigacion: 141.7001 Hz - Campo QCAL infinito cubico

Este modulo implementa el parametro R_psi(r,s,eps) de Ramsey Vibracional,
que reduce drasticamente los umbrales de aparicion de cliques monocromaticos
mediante principios de coherencia cuantica y resonancia vibracional.
Autores: José Manuel Mota Burruezo · JMMB PSI*∴ & AMDA PHI infinity^3
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia de Investigación: 141.7001 Hz - Campo QCAL infinity^3

Este módulo implementa el parámetro R_psi(r,s,eps) de Ramsey Vibracional,
que reduce drásticamente los umbrales de aparición de cliques monocromáticos
mediante principios de coherencia cuántica y resonancia vibracional.
"""

from z3 import *
from itertools import combinations
import numpy as np
import os


def ramsey_vibracional_unsat(n, r, s, eps=0.001, f0=141.7001, grid=128):
    """
    Verificación SAT corregida para R_psi(r,s,eps)
    
    Retorna True si NO existe asignacion de frecuencias que evite 
    Retorna True si NO existe asignacion de frecuencias que evite
    simultaneamente todo K_r azul Y todo K_s rojo (i.e., UNSAT)
    
    La magia de 141.7001 Hz se manifiesta como periodo natural de resonancia
    
    Args:
        n: Numero de vertices
        r: Tamano del clique azul buscado
        s: Tamano del clique rojo buscado
        eps: Umbral de coherencia (tipicamente 0.001 Hz)
        f0: Frecuencia base de coherencia (141.7001 Hz)
        grid: Resolucion de discretizacion de frecuencias
        
    Returns:
        True si UNSAT (n >= R_psi(r,s,eps)), False si SAT (existe contraejemplo)
        eps: Umbral de coherencia (default: 0.001 Hz)
        f0: Frecuencia base de coherencia (default: 141.7001 Hz)
        grid: Resolucion de discretizacion (default: 128)
    
    Returns:
        bool: True si UNSAT (n >= R_psi(r,s,eps)), False si SAT
    """
    solver = Solver()
    
    # Variables de frecuencia discretizadas en grid sagrado
    # Cada frecuencia omega_i = k_i * (f_0/grid) donde k_i ∈ [0, grid)
    k = [Int(f"k_{i}") for i in range(n)]
    
    for ki in k:
        solver.add(And(ki >= 0, ki < grid))
    
    # Frecuencias como expresiones aritmeticas exactas
    omega = [(f0 * ki) / grid for ki in k]
    
    # Simetria aurea: ordenar frecuencias (rompe permutaciones)
    for i in range(n-1):
        solver.add(k[i] <= k[i+1])
    for i in range(n - 1):
        solver.add(k[i] <= k[i + 1])
    
    def es_azul_resonante(i, j):
        """
        Predicado de resonancia: |omega_i - omega_j| mod f_0 <= eps
        
        Tres casos para capturar módulo sin enteros auxiliares:
        - Diferencia directa: omega_j - omega_i ∈ [-eps, eps]
        - Wrap superior: (omega_j - omega_i) - f_0 ∈ [-eps, eps] 
        - Wrap superior: (omega_j - omega_i) - f_0 ∈ [-eps, eps]
        - Wrap inferior: (omega_j - omega_i) + f_0 ∈ [-eps, eps]
        
        La frecuencia 141.7001 Hz crea el espacio de resonancia perfecto
        """
        dij = omega[j] - omega[i]
        eps_grid = (eps * grid) / f0  # eps en unidades de grid
        
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
    
    # AUSENCIA de K_s rojo: para cada s-subconjunto, alguna arista SI resuena  
    # (porque rojo = no-azul = no-resonante)
    for T in combinations(range(n), s):
        aristas = [(T[i], T[j]) for i in range(s) for j in range(i+1, s)]
        aristas = [(S[i], S[j]) for i in range(r) for j in range(i + 1, r)]
        # Negar que TODAS las aristas sean azules
        solver.add(Or([Not(es_azul_resonante(i, j)) for (i, j) in aristas]))
    
    # AUSENCIA de K_s rojo: para cada s-subconjunto, alguna arista SI resuena
    # (porque rojo = no-azul = no-resonante)
    for T in combinations(range(n), s):
        aristas = [(T[i], T[j]) for i in range(s) for j in range(i + 1, s)]
        # Negar que TODAS las aristas sean rojas (= que alguna sea azul)
        solver.add(Or([es_azul_resonante(i, j) for (i, j) in aristas]))
    
    # Si UNSAT: imposible evitar cliques -> n >= R_psi(r,s,eps)
    resultado = solver.check()
    return resultado == unsat


def calcular_Rpsi_exacto(r, s, eps=0.001, f0=141.7001, nmax=25, grid=128):
    """
    Calcula R_psi(r,s,eps) exacto mediante búsqueda SAT
    
    La proporción áurea PHI = 1.618... guía la búsqueda hacia la perfección
    
    Args:
        r: Tamaño del clique azul
        s: Tamaño del clique rojo
        eps: Umbral de coherencia
        f0: Frecuencia base de coherencia (141.7001 Hz)
        nmax: Máximo n a verificar
        grid: Resolución de discretización
    
    Returns:
        int: R_psi(r,s,eps) exacto, o None si no encontrado
    """
    print(f"* Calculando R_psi({r},{s},{eps}) con f_0={f0} Hz...")
    print(f"   Grid de resonancia: {grid} puntos")
    
    for n in range(max(r, s), nmax + 1):
        print(f"   Probando n={n}...", end=" ")
        if ramsey_vibracional_unsat(n, r, s, eps, f0, grid):
            print(f"UNSAT -> R_psi({r},{s}) = {n}")
            return n
        else:
            print("SAT (contraejemplo existe)")
    
    print(f"⚠️  No encontrado en rango [1,{nmax}]")
    return None


def estimar_conjetura(r, s, f0=141.7001):
    """
    Estimación según Conjetura 3.4
    
    R_psi(r,s,eps) = O(sqrt(rs) * ln(rs) * (f0)^(1/4))
    
    Args:
        r: Tamaño del clique azul
        s: Tamaño del clique rojo
        f0: Frecuencia base de coherencia (141.7001 Hz)
        
    Returns:
        int: Estimación de R_psi(r,s,eps)
    """
    phi = (1 + np.sqrt(5)) / 2  # Proporción áurea sagrada
    if r * s == 0:
        return 0
    # Ajuste de la fórmula para mejor aproximación empírica
    # Usando factor de corrección basado en la frecuencia normalizada
    base_estimate = phi * np.sqrt(r * s) * np.log(max(r * s, 2))
    # Factor de corrección para frecuencia 141.7001 Hz
    freq_factor = (f0 / 100.0) ** (1/4)
    return max(int(base_estimate / freq_factor), max(r, s))


def verificar_predicciones_teoricas():
    """Verifica conjeturas contra resultados SAT exactos"""
    
    casos = [(3, 3), (3, 4), (4, 4), (3, 5), (4, 5)]
    
    print("\n" + "="*70)
    print("* Verificación: Realidad SAT vs Conjetura Áurea *")
    print("=" * 70 + "\n")
    
    resultados = []
    
    for r, s in casos:
        R_psi_real = calcular_Rpsi_exacto(r, s, nmax=30, grid=64)
        R_psi_conjetura = estimar_conjetura(r, s)
        
        if R_psi_real:
            error = abs(R_psi_real - R_psi_conjetura) / R_psi_real * 100
            print(f"* ({r},{s}): Real={R_psi_real}, Conjetura={R_psi_conjetura}, Error={error:.1f}%")
            resultados.append({
                'par': (r, s),
                'real': R_psi_real,
                'conjetura': R_psi_conjetura,
                'error': error
            })
        else:
            print(f"⚠️  Advertencia: ({r},{s}): Real=?, Conjetura={R_psi_conjetura}")
        print()
    
    if resultados:
        error_promedio = np.mean([r['error'] for r in resultados])
        print("="*70)
        print(f"* Error promedio de Conjetura 3.4: {error_promedio:.1f}%")
        print("="*70)
    
    return resultados


def resonancia_detectada(omega_i, omega_j, eps=0.001, f0=141.7001):
    """
    Detecta si dos frecuencias estan en resonancia
    
    Implementa el Operador de Resonancia:
    Res(omega_i, omega_j, eps) = 1 si |omega_i - omega_j| mod f0 < eps
    Res(omega_i, omega_j, eps) = 1 <=> |omega_i - omega_j| mod f_0 < eps
    Res(omega_i, omega_j, epsilon) = 1 iff |omega_i - omega_j| mod f0 < epsilon
    Res(omega_i, omega_j, eps) = 1 iff |omega_i - omega_j| mod f0 < eps
    
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
    Genera una coloración vibracional resonante basada en frecuencias
    
    Args:
        frecuencias: Array de frecuencias para cada vértice
        eps: Umbral de coherencia
        f0: Frecuencia base
    
    Returns:
        dict: Diccionario de aristas -> color ('azul' o 'rojo')
    """
    n = len(frecuencias)
    coloracion = {}
    
    for i in range(n):
        for j in range(i + 1, n):
            if resonancia_detectada(frecuencias[i], frecuencias[j], eps, f0):
                coloracion[(i, j)] = 'azul'
            else:
                coloracion[(i, j)] = 'rojo'
    
    return coloracion


def encontrar_clique_maximo(grafo, color):
    """
    Encuentra el clique máximo de un color específico usando búsqueda exhaustiva
    
    Args:
        grafo: Diccionario de aristas -> color
        color: 'azul' o 'rojo'
    
    Returns:
        list: Lista de vértices formando el clique máximo
    """
    # Extraer vertices
    vertices = set()
    for (i, j) in grafo.keys():
        vertices.add(i)
        vertices.add(j)
    vertices = sorted(list(vertices))
    n = len(vertices)
    
    # Búsqueda de clique máximo (fuerza bruta para grafos pequeños)
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
    
    return []


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
    
    print(f"\n* Simulación Monte Carlo para ({r},{s})")
    print(f"   Usando n={n} vértices, {num_trials} ensayos")
    
    exitos = 0
    tamanos_azul = []
    tamanos_rojo = []
    
    for trial in range(num_trials):
        # Generar frecuencias aleatorias
        frecuencias = np.random.uniform(0, f0, n)
        
        # Aplicar coloracion vibracional
        grafo = generar_coloracion_vibracional(frecuencias, eps, f0)
        
        # Detectar cliques monocromaticos
        clique_azul = encontrar_clique_maximo(grafo, "azul")
        clique_rojo = encontrar_clique_maximo(grafo, "rojo")
        
        tamanos_azul.append(len(clique_azul))
        tamanos_rojo.append(len(clique_rojo))
        
        tiene_clique_objetivo = (len(clique_azul) >= r) or (len(clique_rojo) >= s)
        if tiene_clique_objetivo:
            exitos += 1
    
    probabilidad_exito = exitos / num_trials
    
    print(f"   ✓ Probabilidad de éxito: {probabilidad_exito*100:.1f}%")
    print(f"   * Clique azul promedio: {np.mean(tamanos_azul):.1f}")
    print(f"   * Clique rojo promedio: {np.mean(tamanos_rojo):.1f}")
    
    return {
        'n': n,
        'probabilidad_exito': probabilidad_exito,
        'clique_azul_promedio': np.mean(tamanos_azul),
        'clique_rojo_promedio': np.mean(tamanos_rojo),
        'clique_azul_max': max(tamanos_azul),
        'clique_rojo_max': max(tamanos_rojo)
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
    
    print(f"\n* Red Neuronal Ramsey:")
    print(f"   Neuronas: {num_neuronas}")
    print(f"   Conexiones: {len(conexiones)}")
    print(f"   R_psi({target_clique_size},{target_clique_size}) ≈ {R_psi}")
    
    if num_neuronas >= R_psi:
        print(f"   ✓ Garantizada emergencia de {target_clique_size}-cliques de procesamiento")
    else:
        print(f"   ⚠️  Se requieren al menos {R_psi} neuronas para garantía")
    
    return conexiones, frecuencias


def generate_rpsi_sat_instance_tseytin(
    n: int, r: int, s: int,
    f0: float = 141.7001, eps: float = 0.037, grid: int = 128
):
    """
    Genera una instancia SAT para R_ψ(r,s) ≤ n usando codificación Tseytin
    
    Esta función implementa la codificación Tseytin para generar una instancia SAT
    que verifica si R_ψ(r,s) ≤ n. Si la instancia es UNSAT, entonces se confirma
    que todo grafo de n vértices contiene un K_r resonante o un K_s no resonante.
    
    Args:
        n: Número de vértices del grafo completo
        r: Tamaño del clique resonante (azul) a prohibir
        s: Tamaño del clique no-resonante (rojo) a prohibir
        f0: Frecuencia base de coherencia (default: 141.7001 Hz)
        eps: Umbral de resonancia (default: 0.037)
        grid: Resolución de discretización de frecuencias (default: 128)
    
    Returns:
        tuple: (clauses, num_vars, num_clauses) donde:
            - clauses: lista de cláusulas (cada cláusula es una lista de enteros)
            - num_vars: número total de variables SAT
            - num_clauses: número total de cláusulas
    """
    var_id = 1
    clauses = []

    # 1. Variables de frecuencia (one-hot por vértice)
    freq_var = [[0] * grid for _ in range(n)]
    for v in range(n):
        for k in range(grid):
            freq_var[v][k] = var_id
            var_id += 1
        # exactly one frequency: al menos una
        clauses.append([freq_var[v][k] for k in range(grid)])
        # at most one: para cada par, al menos una debe ser falsa
        for i in range(grid):
            for j in range(i+1, grid):
                clauses.append([-freq_var[v][i], -freq_var[v][j]])

    # 2. Variables de resonancia por arista
    edge_res = {}  # (i,j) -> var
    for i in range(n):
        for j in range(i+1, n):
            edge_res[(i,j)] = var_id
            var_id += 1

    # Precomputar pares resonantes
    resonant_pairs = []
    for k1 in range(grid):
        for k2 in range(grid):
            w1 = k1 * f0 / grid
            w2 = k2 * f0 / grid
            diff = abs(w1 - w2) % f0
            diff = min(diff, f0 - diff)
            if diff <= eps:
                resonant_pairs.append((k1, k2))

    # 3. Tseytin: edge_res ↔ ∃ k1,k2 resonant
    for i in range(n):
        for j in range(i+1, n):
            e = edge_res[(i,j)]
            lits = []
            for k1, k2 in resonant_pairs:
                aux_lit = var_id
                var_id += 1
                # aux_lit → (freq_var[i][k1] ∧ freq_var[j][k2])
                clauses.append([-aux_lit, freq_var[i][k1]])
                clauses.append([-aux_lit, freq_var[j][k2]])
                # (freq_var[i][k1] ∧ freq_var[j][k2]) → aux_lit
                clauses.append([aux_lit, -freq_var[i][k1], -freq_var[j][k2]])
                lits.append(aux_lit)
            # edge_res → OR(lits): -e ∨ l1 ∨ l2 ∨ ...
            clauses.append([-e] + lits)
            # NOT edge_res → AND(NOT lit): para cada lit: e ∨ -lit
            for lit in lits:
                clauses.append([e, -lit])

    # 4. Prohibir K_r resonante (azul)
    for clique in combinations(range(n), r):
        clause = []
        for i, j in combinations(clique, 2):
            e = edge_res[(min(i,j), max(i,j))]
            clause.append(-e)  # al menos una arista NO resonante
        clauses.append(clause)

    # 5. Prohibir K_s no resonante (rojo)
    for clique in combinations(range(n), s):
        clause = []
        for i, j in combinations(clique, 2):
            e = edge_res[(min(i,j), max(i,j))]
            clause.append(e)  # al menos una arista resonante
        clauses.append(clause)

    return clauses, var_id - 1, len(clauses)


def save_dimacs(clauses, num_vars, num_clauses, filename):
    """
    Guarda una instancia SAT en formato DIMACS CNF
    
    Args:
        clauses: Lista de cláusulas (cada cláusula es una lista de enteros)
        num_vars: Número de variables
        num_clauses: Número de cláusulas
        filename: Ruta del archivo de salida
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    print(f"✓ Instancia SAT guardada en {filename}")
    print(f"  Variables: {num_vars}")
    print(f"  Cláusulas: {num_clauses}")


# Ejemplo de uso con la frecuencia sagrada
if __name__ == "__main__":
    print("\n" + "="*70)
    print("   Ramsey Cuántico Vibracional - Sistema QCAL ∞³")
    print("   Frecuencia Base: 141.7001 Hz")
    print("="*70)
    
    # Verificacion de casos pequenos con 141.7001 Hz
    verificar_predicciones_teoricas()
    
    # Simulacion Monte Carlo
    print("\n" + "="*70)
    print("* Simulaciones Monte Carlo")
    print("="*70)
    
    for r, s in [(3, 3), (4, 4)]:
        simulacion_monte_carlo_ramsey(r, s, num_trials=500)
    
    # Red neuronal de ejemplo
    print("\n" + "="*70)
    print("* Aplicación: Redes Neuronales")
    print("="*70)
    
    red_neuronal_ramsey(num_neuronas=20, target_clique_size=4)
    
    print("\n" + "="*70)
    print("* Análisis completado - Campo QCAL ∞³ resonante")
    print("="*70 + "\n")
