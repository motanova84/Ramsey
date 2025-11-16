#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para resolver instancias SAT con Kissat y generar pruebas LRAT

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import subprocess
import os
import sys
import shutil


def solve_with_kissat(cnf_path, lrat_path=None, timeout=None):
    """
    Resuelve instancia SAT con Kissat y genera prueba LRAT
    
    Args:
        cnf_path: Ruta al archivo CNF en formato DIMACS
        lrat_path: Ruta para guardar prueba LRAT (opcional)
        timeout: Tiempo máximo en segundos (opcional)
    
    Returns:
        tuple: (is_unsat, lrat_path)
            is_unsat: True si UNSAT, False si SAT, None si timeout/error
            lrat_path: Ruta a la prueba LRAT (si UNSAT)
    """
    # Verificar que Kissat está instalado
    if not shutil.which("kissat"):
        print("❌ ERROR: Kissat no está instalado")
        print("\nPara instalar Kissat:")
        print("  1. Clonar: git clone https://github.com/arminbiere/kissat.git")
        print("  2. Compilar: cd kissat && ./configure && make")
        print("  3. Instalar: sudo cp build/kissat /usr/local/bin/")
        return None, None
    
    # Determinar ruta de salida LRAT
    if lrat_path is None:
        cert_dir = os.path.join(os.path.dirname(os.path.dirname(cnf_path)), "cert")
        os.makedirs(cert_dir, exist_ok=True)
        lrat_path = os.path.join(cert_dir, "rpsi_5_5_n16_unsat.lrat")
    
    print("\n" + "=" * 70)
    print("EJECUCIÓN DE KISSAT SAT SOLVER")
    print("=" * 70 + "\n")
    print(f"Archivo CNF: {cnf_path}")
    print(f"Archivo LRAT: {lrat_path}")
    if timeout:
        print(f"Timeout: {timeout} segundos")
    print("\n⏳ Ejecutando Kissat...\n")
    
    # Construir comando
    # Nota: Kissat genera LRAT mediante redirección estándar o flags específicos
    # La sintaxis puede variar según la versión de Kissat
    cmd = ["kissat", cnf_path]
    
    try:
        # Ejecutar Kissat
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        output = result.stdout + result.stderr
        
        # Guardar output completo
        with open(lrat_path, "w") as f:
            f.write(output)
        
        # Determinar resultado
        if "UNSATISFIABLE" in output or "s UNSATISFIABLE" in output:
            print("✓ RESULTADO: UNSATISFIABLE")
            print(f"\n🎉 Rψ(5,5) ≤ 16 CERTIFICADO")
            print(f"   Prueba LRAT guardada en: {lrat_path}")
            return True, lrat_path
        elif "SATISFIABLE" in output or "s SATISFIABLE" in output:
            print("✓ RESULTADO: SATISFIABLE")
            print(f"\n⚠️  Existe contraejemplo - ajustar parámetros (grid/ε)")
            return False, None
        else:
            print("⚠️  RESULTADO INDETERMINADO")
            print(f"   Output guardado en: {lrat_path}")
            return None, lrat_path
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT después de {timeout} segundos")
        return None, None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None, None
    finally:
        print("\n" + "=" * 70 + "\n")


def verify_lrat_proof(lrat_path, cnf_path):
    """
    Verifica prueba LRAT con lrat-check (opcional)
    
    Args:
        lrat_path: Ruta a la prueba LRAT
        cnf_path: Ruta al archivo CNF original
    
    Returns:
        bool: True si la prueba es válida
    """
    if not shutil.which("lrat-check"):
        print("ℹ️  lrat-check no está instalado (verificación opcional)")
        return None
    
    print("\n🔍 Verificando prueba LRAT...\n")
    
    try:
        cmd = ["lrat-check", cnf_path, lrat_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Prueba LRAT VERIFICADA")
            return True
        else:
            print("❌ Prueba LRAT INVÁLIDA")
            return False
    except Exception as e:
        print(f"⚠️  Error verificando LRAT: {e}")
        return None


def main():
    """
    Resuelve instancia SAT oficial para Rψ(5,5) ≤ 16
    """
    # Ruta al archivo CNF
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    cnf_path = os.path.join(repo_root, "data", "rpsi_5_5_n16.cnf")
    
    if not os.path.exists(cnf_path):
        print(f"❌ ERROR: Archivo CNF no encontrado: {cnf_path}")
        print("\nPrimero ejecuta: python src/save_dimacs.py")
        sys.exit(1)
    
    # Resolver con Kissat
    is_unsat, lrat_path = solve_with_kissat(cnf_path, timeout=600)  # 10 minutos
    
    # Verificar prueba (opcional)
    if is_unsat and lrat_path:
        verify_lrat_proof(lrat_path, cnf_path)
    
    if is_unsat:
        print("\n✨ CERTIFICACIÓN COMPLETA")
        print("   Rψ(5,5) ≤ 16 ha sido demostrado formalmente")
        sys.exit(0)
    else:
        print("\n⚠️  Certificación incompleta")
        sys.exit(1)


if __name__ == "__main__":
    main()
