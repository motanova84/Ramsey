"""
Tests para Ramsey Cuántico Vibracional

Verifica la correctitud de las implementaciones y predicciones teóricas.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ramsey_vibracional import (
    ramsey_vibracional_unsat,
    calcular_Rpsi_exacto,
    estimar_conjetura,
    generar_coloracion_vibracional,
    encontrar_clique_maximo
)
import numpy as np


def test_ramsey_vibracional_unsat_basic():
    """Test básico de verificación SAT"""
    print("\n=== Test: ramsey_vibracional_unsat básico ===")
    
    # Para n pequeño (menor que R_ψ(3,3)), debe ser SAT (False)
    # Con grid=32, R_ψ(3,3) = 5, entonces n=4 debe ser SAT
    result = ramsey_vibracional_unsat(n=4, r=3, s=3, grid=32)
    print(f"n=4, r=3, s=3: {'UNSAT' if result else 'SAT'} (esperado: SAT)")
    assert not result, "Debería ser SAT para n=4, r=3, s=3"
    
    # Para n >= R_ψ(3,3), debe ser UNSAT (True)
    result = ramsey_vibracional_unsat(n=5, r=3, s=3, grid=32)
    print(f"n=5, r=3, s=3: {'UNSAT' if result else 'SAT'} (esperado: UNSAT)")
    assert result, "Debería ser UNSAT para n=5, r=3, s=3"
    
    print("✓ Test pasado")


def test_calcular_Rpsi_exacto():
    """Test de cálculo exacto de R_ψ"""
    print("\n=== Test: calcular_Rpsi_exacto ===")
    
    # R_ψ(3,3) con grid=32 debería ser 5
    R_psi_33 = calcular_Rpsi_exacto(3, 3, nmax=10, grid=32)
    print(f"R_ψ(3,3) = {R_psi_33} (con grid=32)")
    assert R_psi_33 == 5, f"R_ψ(3,3) con grid=32 debería ser 5, obtuvimos {R_psi_33}"
    
    print("✓ Test pasado")


def test_estimar_conjetura():
    """Test de estimación según conjetura"""
    print("\n=== Test: estimar_conjetura ===")
    
    # Verificar que las estimaciones estén en el rango esperado
    # Los valores dependen de la fórmula ajustada
    casos = [
        (3, 3, 5, 12),   # Conjetura para (3,3) en rango [5, 12]
        (3, 4, 6, 15),   # Conjetura para (3,4) en rango [6, 15]
        (4, 4, 8, 20),   # Conjetura para (4,4) en rango [8, 20]
    ]
    
    for r, s, min_esperado, max_esperado in casos:
        estimacion = estimar_conjetura(r, s)
        print(f"Conjetura({r},{s}) = {estimacion} (esperado entre {min_esperado} y {max_esperado})")
        # Verificar que esté en el rango razonable
        assert min_esperado <= estimacion <= max_esperado, \
            f"Estimación para ({r},{s}) fuera de rango: {estimacion} no está entre [{min_esperado}, {max_esperado}]"
    
    print("✓ Test pasado")


def test_generar_coloracion_vibracional():
    """Test de generación de coloración vibracional"""
    print("\n=== Test: generar_coloracion_vibracional ===")
    
    # Crear frecuencias de prueba
    frecuencias = [0.0, 0.0005, 141.7001, 141.7005]
    grafo = generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001)
    
    # Verificar que genera aristas
    assert len(grafo) == 6, f"Debe generar 6 aristas para 4 vértices, obtuvimos {len(grafo)}"
    
    # Verificar colores
    # (0,1) debe ser azul (diferencia 0.0005 < 0.001)
    assert grafo[(0, 1)] == 'azul', "Arista (0,1) debe ser azul"
    
    # (2,3) debe ser azul (diferencia 0.0005 < 0.001)
    assert grafo[(2, 3)] == 'azul', "Arista (2,3) debe ser azul"
    
    print("✓ Test pasado")


def test_encontrar_clique_maximo():
    """Test de búsqueda de clique máximo"""
    print("\n=== Test: encontrar_clique_maximo ===")
    
    # Crear un grafo simple con clique azul conocido
    grafo = {
        (0, 1): 'azul',
        (0, 2): 'azul',
        (1, 2): 'azul',
        (0, 3): 'rojo',
        (1, 3): 'rojo',
        (2, 3): 'rojo',
    }
    
    clique_azul = encontrar_clique_maximo(grafo, 'azul')
    print(f"Clique azul encontrado: {clique_azul}")
    assert len(clique_azul) == 3, f"Debe encontrar clique de tamaño 3, encontró {len(clique_azul)}"
    
    # Verificar que es un clique válido
    for i in range(len(clique_azul)):
        for j in range(i + 1, len(clique_azul)):
            v1, v2 = min(clique_azul[i], clique_azul[j]), max(clique_azul[i], clique_azul[j])
            assert grafo[(v1, v2)] == 'azul', f"Arista ({v1},{v2}) debe ser azul"
    
    print("✓ Test pasado")


def test_relacion_con_ramsey_clasico():
    """Test de relación R_ψ ≤ R"""
    print("\n=== Test: R_ψ ≤ R (relación con Ramsey clásico) ===")
    
    # Valores conocidos de Ramsey clásico
    valores_clasicos = {
        (3, 3): 6,
        (3, 4): 9,
        (4, 4): 18,
    }
    
    for (r, s), R_clasico in valores_clasicos.items():
        R_psi = calcular_Rpsi_exacto(r, s, nmax=20, grid=32)
        if R_psi:
            print(f"R_ψ({r},{s}) = {R_psi} ≤ R({r},{s}) = {R_clasico}")
            assert R_psi <= R_clasico, \
                f"Debe cumplirse R_ψ({r},{s}) ≤ R({r},{s}): {R_psi} > {R_clasico}"
        else:
            print(f"No se pudo calcular R_ψ({r},{s})")
    
    print("✓ Test pasado")


def test_monotonicidad_n():
    """Test de monotonicidad: si n1 < n2, UNSAT(n1)=True => UNSAT(n2)=True"""
    print("\n=== Test: Monotonicidad respecto a n ===")
    
    r, s = 3, 3
    
    # Si n=5 es UNSAT, entonces n=6 también debe ser UNSAT
    result_5 = ramsey_vibracional_unsat(5, r, s, grid=32)
    result_6 = ramsey_vibracional_unsat(6, r, s, grid=32)
    
    print(f"n=5: {'UNSAT' if result_5 else 'SAT'}")
    print(f"n=6: {'UNSAT' if result_6 else 'SAT'}")
    
    if result_5:
        assert result_6, "Si n=5 es UNSAT, n=6 también debe serlo"
    
    print("✓ Test pasado")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("✧ Ejecutando Tests de Ramsey Cuántico Vibracional ✧")
    print("=" * 70)
    
    tests = [
        test_ramsey_vibracional_unsat_basic,
        test_calcular_Rpsi_exacto,
        test_estimar_conjetura,
        test_generar_coloracion_vibracional,
        test_encontrar_clique_maximo,
        test_relacion_con_ramsey_clasico,
        test_monotonicidad_n,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ Test falló: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Resultados: {passed} pasados, {failed} fallidos")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
