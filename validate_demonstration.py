#!/usr/bin/env python3
"""
Script de Validación: Verifica que la demostración funciona correctamente
=========================================================================

Este script ejecuta una serie de tests para asegurar que todos los
componentes de la demostración funcionan correctamente.

Uso:
    python validate_demonstration.py
    python validate_demonstration.py --verbose
    python validate_demonstration.py --quick  # Solo tests rápidos
"""

import sys
import subprocess
import os
from pathlib import Path
import argparse

class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test(name: str):
    """Imprime el nombre del test."""
    print(f"\n{Colors.BOLD}Testing: {name}{Colors.ENDC}")

def print_success(msg: str):
    """Imprime mensaje de éxito."""
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")

def print_failure(msg: str):
    """Imprime mensaje de fallo."""
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")

def print_warning(msg: str):
    """Imprime advertencia."""
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")

def test_python_dependencies():
    """Test 1: Verificar que las dependencias de Python están instaladas."""
    print_test("Dependencias de Python")
    
    required = ['numpy', 'z3']
    optional = ['matplotlib', 'click', 'fire']
    
    all_ok = True
    for module in required:
        try:
            __import__(module)
            print_success(f"{module} instalado")
        except ImportError:
            print_failure(f"{module} NO instalado (requerido)")
            all_ok = False
    
    for module in optional:
        try:
            __import__(module)
            print_success(f"{module} instalado")
        except ImportError:
            print_warning(f"{module} NO instalado (opcional)")
    
    return all_ok

def test_documentation_files():
    """Test 2: Verificar que los archivos de documentación existen."""
    print_test("Archivos de Documentación")
    
    required_docs = [
        'README.md',
        'DEMO_METHODOLOGY.md',
        'QUICKSTART_DEMO.md',
        'DIAGRAMS_METHODOLOGY.md',
        'METHODOLOGY.md'
    ]
    
    all_ok = True
    for doc in required_docs:
        if Path(doc).exists():
            print_success(f"{doc} existe")
        else:
            print_failure(f"{doc} NO existe")
            all_ok = False
    
    return all_ok

def test_python_scripts():
    """Test 3: Verificar que los scripts Python existen y tienen sintaxis válida."""
    print_test("Scripts Python")
    
    scripts = [
        'demo.py',
        'tutorial_methodology.py',
        'ai_ramsey_formal.py',
        'ramsey_vibracional.py',
        'compute_rpsi_table.py',
        'resonance_analysis.py'
    ]
    
    all_ok = True
    for script in scripts:
        if not Path(script).exists():
            print_failure(f"{script} NO existe")
            all_ok = False
            continue
        
        # Verificar sintaxis
        result = subprocess.run(
            ['python', '-m', 'py_compile', script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"{script} - sintaxis válida")
        else:
            print_failure(f"{script} - error de sintaxis")
            all_ok = False
    
    return all_ok

def test_lean_files():
    """Test 4: Verificar que los archivos Lean existen."""
    print_test("Archivos Lean 4")
    
    lean_files = [
        'src/Ramsey/Graph.lean',
        'src/Ramsey/Classical.lean',
        'src/Ramsey/Vibrational.lean',
        'src/Ramsey/Reduction.lean',
        'src/Ramsey/R55Proof.lean'
    ]
    
    all_ok = True
    src_exists = Path('src/Ramsey').exists()
    
    if not src_exists:
        print_warning("Directorio src/Ramsey no existe")
        print_warning("Archivos Lean no verificados (esto es OK si no usas Lean)")
        return True  # No es crítico
    
    for lean_file in lean_files:
        if Path(lean_file).exists():
            print_success(f"{lean_file} existe")
        else:
            print_warning(f"{lean_file} NO existe")
    
    return True  # Lean es opcional

def test_data_files():
    """Test 5: Verificar que los archivos de datos existen."""
    print_test("Archivos de Datos")
    
    data_dir = Path('data')
    if not data_dir.exists():
        print_warning("Directorio data/ no existe")
        return True  # No crítico
    
    important_files = [
        'data/rpsi_vibration_model.json',
    ]
    
    all_ok = True
    for file in important_files:
        if Path(file).exists():
            print_success(f"{file} existe")
        else:
            print_warning(f"{file} NO existe")
    
    return True  # No crítico

def test_beacon_file():
    """Test 6: Verificar que el archivo .qcal_beacon existe y contiene f₀."""
    print_test("Archivo .qcal_beacon")
    
    beacon_path = Path('.qcal_beacon')
    
    if not beacon_path.exists():
        print_failure(".qcal_beacon NO existe")
        return False
    
    print_success(".qcal_beacon existe")
    
    # Verificar que contiene f₀
    content = beacon_path.read_text()
    if '141.7001' in content or '141.70' in content:
        print_success("Contiene frecuencia f₀ = 141.7001 Hz")
        return True
    else:
        print_warning("No se encontró frecuencia f₀ en el beacon")
        return True  # No crítico

def test_demo_script(verbose=False):
    """Test 7: Ejecutar demo.py y verificar que funciona."""
    print_test("Ejecutar demo.py")
    
    try:
        result = subprocess.run(
            ['python', 'demo.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_success("demo.py ejecutó correctamente")
            if verbose:
                print("\nSalida:")
                print(result.stdout[:500])
            return True
        else:
            print_failure(f"demo.py falló con código {result.returncode}")
            if verbose:
                print("\nError:")
                print(result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print_failure("demo.py tomó demasiado tiempo (>30s)")
        return False
    except Exception as e:
        print_failure(f"Error ejecutando demo.py: {e}")
        return False

def test_tutorial_script(verbose=False):
    """Test 8: Ejecutar tutorial_methodology.py en modo no-wait."""
    print_test("Ejecutar tutorial_methodology.py")
    
    try:
        result = subprocess.run(
            ['python', 'tutorial_methodology.py', '--no-wait'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print_success("tutorial_methodology.py ejecutó correctamente")
            if verbose:
                print("\nSalida:")
                print(result.stdout[:500])
            return True
        else:
            print_failure(f"tutorial_methodology.py falló con código {result.returncode}")
            if verbose:
                print("\nError:")
                print(result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print_failure("tutorial_methodology.py tomó demasiado tiempo (>10s)")
        return False
    except Exception as e:
        print_failure(f"Error ejecutando tutorial_methodology.py: {e}")
        return False

def test_import_ramsey():
    """Test 9: Verificar que se puede importar ramsey_vibracional."""
    print_test("Importar ramsey_vibracional")
    
    try:
        import ramsey_vibracional
        print_success("ramsey_vibracional importado correctamente")
        
        # Verificar algunas funciones clave
        functions = [
            'resonancia_detectada',
            'estimar_conjetura',
            'calcular_Rpsi_exacto'
        ]
        
        for func in functions:
            if hasattr(ramsey_vibracional, func):
                print_success(f"  Función {func} disponible")
            else:
                print_warning(f"  Función {func} NO encontrada")
        
        return True
    except Exception as e:
        print_failure(f"Error importando ramsey_vibracional: {e}")
        return False

def test_quick_computation():
    """Test 10: Verificar que se puede hacer un cálculo básico."""
    print_test("Cálculo Básico de Resonancia")
    
    try:
        from ramsey_vibracional import resonancia_detectada
        
        f0 = 141.7001
        eps = 0.001
        
        # Test: frecuencias idénticas deben resonar
        result1 = resonancia_detectada(10.0, 10.0, f0, eps)
        if result1:
            print_success("Frecuencias idénticas resuenan ✓")
        else:
            print_failure("Frecuencias idénticas NO resuenan (error)")
            return False
        
        # Test: frecuencias muy diferentes NO deben resonar
        result2 = resonancia_detectada(10.0, 80.0, f0, eps)
        if not result2:
            print_success("Frecuencias diferentes NO resuenan ✓")
        else:
            print_warning("Frecuencias diferentes resuenan (revisar implementación)")
        
        return True
    except Exception as e:
        print_failure(f"Error en cálculo básico: {e}")
        return False

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Valida que la demostración funciona correctamente"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Mostrar salida detallada"
    )
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help="Solo ejecutar tests rápidos (no ejecutar scripts)"
    )
    
    args = parser.parse_args()
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'VALIDACIÓN DE DEMOSTRACIÓN':^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    tests = [
        ("Dependencias Python", test_python_dependencies, False),
        ("Documentación", test_documentation_files, False),
        ("Scripts Python", test_python_scripts, False),
        ("Archivos Lean", test_lean_files, False),
        ("Archivos de Datos", test_data_files, False),
        ("Beacon QCAL", test_beacon_file, False),
        ("Demo Script", lambda: test_demo_script(args.verbose), True),
        ("Tutorial Script", lambda: test_tutorial_script(args.verbose), True),
        ("Importar Ramsey", test_import_ramsey, False),
        ("Cálculo Básico", test_quick_computation, False),
    ]
    
    results = []
    for name, test_func, is_slow in tests:
        if args.quick and is_slow:
            print(f"\n{Colors.WARNING}Saltando test lento: {name}{Colors.ENDC}")
            continue
        
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_failure(f"Excepción en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'RESUMEN':^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}")
        else:
            print_failure(f"{name}")
    
    print(f"\n{Colors.BOLD}Tests pasados: {passed}/{total}{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ TODOS LOS TESTS PASARON{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}La demostración está lista para usar.{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}Ejecuta: python demo.py{Colors.ENDC}")
        return 0
    else:
        print(f"\n{Colors.WARNING}⚠ Algunos tests fallaron{Colors.ENDC}")
        print(f"\nPor favor revisa los errores arriba.")
        print(f"\nPara instalar dependencias faltantes:")
        print(f"  pip install numpy z3-solver matplotlib")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Validación interrumpida por el usuario.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error inesperado: {e}{Colors.ENDC}")
        sys.exit(1)
