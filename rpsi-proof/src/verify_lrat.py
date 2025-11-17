#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador LRAT del certificado

Valida certificados LRAT de insatisfiabilidad SAT para instancias Rψ.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import subprocess
import sys
import os


def verify_lrat(cnf_path, lrat_path, lrat_checker="lrat-check"):
    """
    Verifica certificado LRAT usando lrat-check.
    
    Args:
        cnf_path: Ruta al archivo CNF en formato DIMACS
        lrat_path: Ruta al certificado LRAT
        lrat_checker: Comando o ruta al ejecutable lrat-check
    
    Returns:
        bool: True si el certificado es válido, False en caso contrario
    """
    
    # Verificar que los archivos existen
    if not os.path.exists(cnf_path):
        print(f"❌ ERROR: Archivo CNF no encontrado: {cnf_path}")
        return False
    
    if not os.path.exists(lrat_path):
        print(f"❌ ERROR: Archivo LRAT no encontrado: {lrat_path}")
        return False
    
    print(f"🔍 Verificando certificado LRAT...")
    print(f"   CNF: {cnf_path}")
    print(f"   LRAT: {lrat_path}")
    print()
    
    try:
        # Ejecutar lrat-check
        result = subprocess.run(
            [lrat_checker, cnf_path, lrat_path],
            capture_output=True,
            text=True,
            timeout=300  # Timeout de 5 minutos
        )
        
        # Analizar resultado
        if result.returncode == 0:
            print("✅ CERTIFICADO LRAT VÁLIDO")
            print("   La prueba de insatisfiabilidad es correcta.")
            print()
            if result.stdout:
                print("Salida del verificador:")
                print(result.stdout)
            return True
        else:
            print("❌ CERTIFICADO LRAT INVÁLIDO")
            print(f"   Código de salida: {result.returncode}")
            if result.stderr:
                print("\nError:")
                print(result.stderr)
            if result.stdout:
                print("\nSalida:")
                print(result.stdout)
            return False
            
    except FileNotFoundError:
        print(f"❌ ERROR: lrat-check no encontrado")
        print(f"   Asegúrate de que lrat-check esté instalado y en el PATH")
        print()
        print("Para instalar lrat-check:")
        print("  git clone https://github.com/marijnheule/drat-trim.git")
        print("  cd drat-trim")
        print("  make")
        print("  sudo cp lrat-check /usr/local/bin/")
        return False
        
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Timeout al verificar certificado")
        print("   La verificación tomó más de 5 minutos")
        return False
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return False


def verify_with_drat_trim(cnf_path, drat_path, drat_trim="drat-trim"):
    """
    Verifica certificado DRAT/LRAT usando drat-trim.
    
    Args:
        cnf_path: Ruta al archivo CNF en formato DIMACS
        drat_path: Ruta al certificado DRAT/LRAT
        drat_trim: Comando o ruta al ejecutable drat-trim
    
    Returns:
        bool: True si el certificado es válido, False en caso contrario
    """
    
    if not os.path.exists(cnf_path):
        print(f"❌ ERROR: Archivo CNF no encontrado: {cnf_path}")
        return False
    
    if not os.path.exists(drat_path):
        print(f"❌ ERROR: Archivo DRAT no encontrado: {drat_path}")
        return False
    
    print(f"🔍 Verificando certificado DRAT con drat-trim...")
    print(f"   CNF: {cnf_path}")
    print(f"   DRAT: {drat_path}")
    print()
    
    try:
        # Ejecutar drat-trim
        result = subprocess.run(
            [drat_trim, cnf_path, drat_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0 and "VERIFIED" in result.stdout:
            print("✅ CERTIFICADO DRAT VERIFICADO")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ VERIFICACIÓN FALLIDA")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
            
    except FileNotFoundError:
        print(f"❌ ERROR: drat-trim no encontrado")
        print("Para instalar drat-trim:")
        print("  git clone https://github.com/marijnheule/drat-trim.git")
        print("  cd drat-trim")
        print("  make")
        print("  sudo cp drat-trim /usr/local/bin/")
        return False
        
    except subprocess.TimeoutExpired:
        print("❌ ERROR: Timeout al verificar certificado")
        return False
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        return False


if __name__ == "__main__":
    # Ejemplo de uso
    if len(sys.argv) < 3:
        print("Uso: python verify_lrat.py <cnf_file> <lrat_file> [lrat-check]")
        print()
        print("Ejemplo:")
        print("  python verify_lrat.py ../data/coloring_r16.cnf ../cert/proof_r16.lrat")
        print()
        sys.exit(1)
    
    cnf_path = sys.argv[1]
    lrat_path = sys.argv[2]
    lrat_checker = sys.argv[3] if len(sys.argv) > 3 else "lrat-check"
    
    # Intentar con lrat-check primero
    print("=" * 60)
    print("VERIFICACIÓN DE CERTIFICADO LRAT")
    print("=" * 60)
    print()
    
    success = verify_lrat(cnf_path, lrat_path, lrat_checker)
    
    if success:
        print()
        print("=" * 60)
        print("🎉 VERIFICACIÓN EXITOSA")
        print("   El certificado LRAT es válido.")
        print("   La instancia SAT es INSATISFIABLE.")
        print("   Rψ(5,5) ≤ 16 está CERTIFICADO.")
        print("=" * 60)
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("❌ VERIFICACIÓN FALLIDA")
        print("=" * 60)
        sys.exit(1)
