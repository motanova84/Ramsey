#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para validar la generación de instancias SAT

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import os
import sys
from generate_rpsi_sat import (
    generate_rpsi_sat_instance_tseytin,
    is_resonant,
    save_dimacs
)


def test_is_resonant():
    """Test del predicado de resonancia"""
    print("Test 1: Predicado de resonancia...")
    
    grid = 128
    eps = 0.037
    f0 = 141.7001
    eps_grid = (eps * grid) / f0  # ~0.033
    
    # Caso 1: Misma frecuencia (debe ser resonante)
    assert is_resonant(10, 10, grid, eps, f0) == True, "Misma frecuencia debe resonar"
    
    # Caso 2: Frecuencias idénticas o muy cercanas (diff=0 debe resonar)
    assert is_resonant(0, 0, grid, eps, f0) == True, "Frecuencias idénticas deben resonar"
    
    # Caso 3: Frecuencias distantes (no debe resonar)
    assert is_resonant(10, 64, grid, eps, f0) == False, "Frecuencias distantes no deben resonar"
    
    # Caso 4: Frecuencias separadas pero no resonantes (diff > eps_grid)
    # Con eps_grid ~0.033, diff=1 no resuena
    assert is_resonant(10, 11, grid, eps, f0) == False, "Frecuencias con diff=1 no deben resonar (eps_grid < 1)"
    
    # Caso 5: Wrap-around modular
    # Índices cerca de 0 y cerca de 127 (diff_mod = 1) no deben resonar con eps_grid < 1
    assert is_resonant(0, 127, grid, eps, f0) == False, "Wrap-around con diff=1 no debe resonar"
    
    print(f"  ✓ Todos los tests de resonancia pasaron (eps_grid={eps_grid:.3f})\n")


def test_sat_instance_structure():
    """Test de la estructura de la instancia SAT"""
    print("Test 2: Estructura de instancia SAT...")
    
    n, r, s = 4, 3, 3  # Caso pequeño para testing
    eps = 0.037
    f0 = 141.7001
    grid = 16  # Grid pequeño para testing
    
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n, r, s, eps, f0, grid
    )
    
    # Verificar que se generaron cláusulas
    assert num_clauses > 0, "Deben generarse cláusulas"
    assert len(clauses) == num_clauses, "Número de cláusulas debe coincidir"
    
    # Verificar que todas las cláusulas terminan en 0 conceptualmente
    # (en nuestra representación interna no tienen 0 al final)
    for clause in clauses:
        assert len(clause) > 0, "Cláusulas no deben estar vacías"
        assert all(isinstance(lit, int) for lit in clause), "Literales deben ser enteros"
    
    # Verificar rango de variables
    max_var = max(max(abs(lit) for lit in clause) for clause in clauses)
    assert max_var <= num_vars, f"Variable {max_var} excede num_vars {num_vars}"
    
    print(f"  ✓ Instancia generada correctamente:")
    print(f"    - n={n}, r={r}, s={s}")
    print(f"    - Variables: {num_vars}")
    print(f"    - Cláusulas: {num_clauses}")
    print()


def test_official_instance():
    """Test de la instancia oficial Rψ(5,5) ≤ 16"""
    print("Test 3: Instancia oficial Rψ(5,5) ≤ 16...")
    
    n, r, s = 16, 5, 5
    eps = 0.037
    f0 = 141.7001
    grid = 128
    
    print(f"  Generando instancia oficial...")
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n, r, s, eps, f0, grid
    )
    
    # Verificar métricas esperadas
    print(f"  ✓ Instancia oficial generada:")
    print(f"    - Variables: {num_vars:,} (esperado: ~17,528)")
    print(f"    - Cláusulas: {num_clauses:,} (esperado: ~200,360)")
    
    # Verificar que las métricas están en el rango esperado
    assert 15000 <= num_vars <= 20000, f"Variables fuera de rango: {num_vars}"
    assert 180000 <= num_clauses <= 220000, f"Cláusulas fuera de rango: {num_clauses}"
    
    print()


def test_dimacs_export():
    """Test de exportación a DIMACS"""
    print("Test 4: Exportación DIMACS...")
    
    n, r, s = 4, 3, 3
    eps = 0.037
    f0 = 141.7001
    grid = 16
    
    clauses, num_vars, num_clauses = generate_rpsi_sat_instance_tseytin(
        n, r, s, eps, f0, grid
    )
    
    # Crear archivo temporal
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cnf', delete=False) as f:
        temp_path = f.name
    
    try:
        # Exportar a DIMACS
        save_dimacs(clauses, num_vars, num_clauses, temp_path)
        
        # Verificar que el archivo existe
        assert os.path.exists(temp_path), "Archivo DIMACS no fue creado"
        
        # Verificar formato DIMACS
        with open(temp_path, 'r') as f:
            lines = f.readlines()
        
        # Primera línea debe ser "p cnf num_vars num_clauses"
        first_line = lines[0].strip()
        assert first_line.startswith('p cnf'), f"Primera línea inválida: {first_line}"
        
        parts = first_line.split()
        assert int(parts[2]) == num_vars, "num_vars no coincide en DIMACS"
        assert int(parts[3]) == num_clauses, "num_clauses no coincide en DIMACS"
        
        # Verificar que cada cláusula termina en 0
        for i, line in enumerate(lines[1:], 1):
            if line.strip():
                assert line.strip().endswith(' 0'), f"Línea {i+1} no termina en 0"
        
        print(f"  ✓ Archivo DIMACS generado correctamente:")
        print(f"    - Ruta: {temp_path}")
        print(f"    - Tamaño: {os.path.getsize(temp_path)} bytes")
        print()
    
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 70)
    print("TESTS DE VALIDACIÓN: Generación de Instancias SAT")
    print("=" * 70 + "\n")
    
    try:
        test_is_resonant()
        test_sat_instance_structure()
        test_official_instance()
        test_dimacs_export()
        
        print("=" * 70)
        print("✨ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 70 + "\n")
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FALLÓ: {e}\n")
        return 1
    
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
