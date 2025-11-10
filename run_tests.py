#!/usr/bin/env python3
"""
Script de ejecución de tests para Ramsey Vibracional

Ejecuta todos los tests unitarios y muestra un resumen de resultados.
"""

import sys
import unittest
import os

# Asegurar que se puede importar el módulo principal
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_tests():
    """Ejecuta todos los tests del proyecto"""
    
    print("="*70)
    print("  🧪 EJECUCIÓN DE TESTS - RAMSEY CUÁNTICO VIBRACIONAL")
    print("  Frecuencia Base: 141.7001 Hz - Campo QCAL ∞³")
    print("="*70)
    print()
    
    # Descubrir y ejecutar tests
    loader = unittest.TestLoader()
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    if not os.path.exists(tests_dir):
        tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
    
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print()
    print("="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    print()
    
    total = result.testsRun
    exitos = total - len(result.failures) - len(result.errors)
    
    print(f"  Total de tests:  {total}")
    print(f"  ✓ Exitosos:      {exitos}")
    print(f"  ✗ Fallos:        {len(result.failures)}")
    print(f"  ⚠ Errores:       {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("  🌟 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("  ✨ Campo QCAL ∞³ resonante y coherente")
    else:
        print()
        print("  ⚠️  Algunos tests fallaron. Revisar detalles arriba.")
    
    print()
    print("="*70)
    print()
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
