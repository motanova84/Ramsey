#!/usr/bin/env python3
"""
Demo del Sistema Formal AI-Ramsey-Formal

Este script demuestra cómo usar el sistema de certificación formal.
"""

import os
import sys

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def main():
    print_header("🎓 Demo: Sistema de Certificación Formal AI-Ramsey-Formal")
    
    print("Este demo muestra las capacidades del sistema de certificación formal")
    print("para Ramsey Vibracional.\n")
    
    # 1. Listar certificados existentes
    print_header("📜 Paso 1: Listar Certificados Existentes")
    os.system("python ai_ramsey_formal.py list")
    
    # 2. Mostrar un certificado Lean 4
    print_header("📖 Paso 2: Visualizar un Certificado Lean 4")
    
    cert_file = "certificates/Rpsi_3_3_le_5.lean"
    if os.path.exists(cert_file):
        print(f"Contenido de {cert_file}:\n")
        with open(cert_file, 'r') as f:
            content = f.read()
            # Mostrar primeras 30 líneas
            lines = content.split('\n')[:30]
            print('\n'.join(lines))
            if len(content.split('\n')) > 30:
                print("\n... (archivo completo disponible en certificates/)")
    else:
        print(f"❌ Certificado no encontrado: {cert_file}")
    
    # 3. Mostrar certificado SMT2
    print_header("📋 Paso 3: Visualizar un Certificado SMT2")
    
    smt2_file = "certificates/Rpsi_3_3_le_5.smt2"
    if os.path.exists(smt2_file):
        print(f"Contenido de {smt2_file}:\n")
        with open(smt2_file, 'r') as f:
            content = f.read()
            print(content)
    else:
        print(f"❌ Certificado no encontrado: {smt2_file}")
    
    # 4. Explicar cómo generar nuevos certificados
    print_header("🔨 Paso 4: Cómo Generar Nuevos Certificados")
    
    print("Para generar un nuevo certificado, usa el comando:")
    print("\n  python ai_ramsey_formal.py certify <r> <s> [opciones]\n")
    print("Ejemplos:")
    print("  • python ai_ramsey_formal.py certify 3 3 --lam 0.1")
    print("  • python ai_ramsey_formal.py certify 4 4 --lam 0.062 --grid 32")
    print("  • python ai_ramsey_formal.py certify 3 4 --lam 0.08 --nmax 15\n")
    
    # 5. Información sobre el paper
    print_header("📄 Paso 5: Paper LaTeX")
    
    print("El paper formal está en paper/main.tex")
    print("\nPara compilar:")
    print("  cd paper")
    print("  pdflatex main.tex")
    print("  pdflatex main.tex  # Segunda pasada para referencias\n")
    print("El paper incluye:")
    print("  • Definiciones formales")
    print("  • Teoremas principales")
    print("  • Tabla de resultados certificados")
    print("  • Listo para arXiv\n")
    
    # 6. Información sobre CI/CD
    print_header("🚀 Paso 6: CI/CD con GitHub Actions")
    
    print("El proyecto incluye CI/CD automático en .github/workflows/lean-ci.yml")
    print("\nEl workflow ejecuta:")
    print("  1. Build de Lean 4 (verifica certificados)")
    print("  2. Tests de Python")
    print("  3. Benchmark de verificación\n")
    print("Cada push/PR ejecuta verificación automática.\n")
    
    # 7. Resumen
    print_header("✨ Resumen del Sistema Formal")
    
    print("✅ Certificados formales en Lean 4 + SMT2")
    print("✅ CLI automatizado (ai-ramsey-formal)")
    print("✅ Paper LaTeX listo para arXiv")
    print("✅ CI/CD con GitHub Actions")
    print("✅ Documentación completa (FORMAL_SYSTEM.md)")
    print("\n📚 Para más información:")
    print("  • README.md - Guía de uso general")
    print("  • FORMAL_SYSTEM.md - Sistema de certificación")
    print("  • paper/main.tex - Paper formal")
    
    print_header("🎉 Demo Completado")
    print("El sistema AI-Ramsey-Formal está listo para uso.\n")

if __name__ == "__main__":
    main()
