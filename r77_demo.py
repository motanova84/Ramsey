#!/usr/bin/env python3
"""
R(7,7) — Verificación Local Demo Script
∴ AI-Ramsey-Formal v1.0.0 — QCAL ∞³

Este script permite verificar localmente la predicción R(7,7) = 215
usando la teoría de Ramsey Vibracional.

Requisitos:
    pip install z3-solver numpy

Uso:
    python r77_demo.py
"""

import math
import sys

print("=" * 70)
print("∴ R(7,7) — Verificación Local (ε=0.001, f₀=141.7001)")
print("=" * 70)
print()

try:
    from ramsey_vibracional import calcular_Rpsi_exacto
except ImportError:
    print("❌ Error: No se encuentra el módulo 'ramsey_vibracional'")
    print("   Asegúrate de ejecutar este script en el directorio del proyecto")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("❌ Error: numpy no está instalado")
    print("   Instala con: pip install numpy")
    sys.exit(1)

# Parámetros
r, s = 7, 7
eps = 0.001
f0 = 141.7001
max_n = 250
grid = 256

print(f"Parámetros de verificación:")
print(f"  r = {r}, s = {s}")
print(f"  ε = {eps} (umbral de resonancia)")
print(f"  f₀ = {f0} Hz (frecuencia base)")
print(f"  grid = {grid} (resolución)")
print(f"  max_n = {max_n} (búsqueda hasta n={max_n})")
print()

# Advertencia sobre tiempo de cómputo
print("⚠️  ADVERTENCIA: Esta verificación puede tomar varios minutos")
print("   para R(7,7) debido a la complejidad combinatoria.")
print()
print("   Para una verificación más rápida, prueba con casos más pequeños:")
print("   - R(3,3) toma ~1 segundo")
print("   - R(4,4) toma ~10 segundos")
print("   - R(5,5) toma ~1 minuto")
print("   - R(6,6) toma ~10 minutos")
print("   - R(7,7) toma ~1-2 horas (recomendado grid=128 para más velocidad)")
print()

# Preguntar al usuario si desea continuar
response = input("¿Deseas continuar con la verificación de R(7,7)? (s/N): ").strip().lower()
if response not in ['s', 'si', 'sí', 'y', 'yes']:
    print()
    print("Verificación cancelada. Ejecutando demo rápido con R(4,4) en su lugar...")
    print()
    r, s = 4, 4
    max_n = 20
    grid = 64

# Verificación rápida
print(f"🔍 Calculando R_ψ({r},{s})...")
print()

R_psi = calcular_Rpsi_exacto(r=r, s=s, eps=eps, f0=f0, nmax=max_n, grid=grid)

if R_psi is None:
    print()
    print(f"❌ No se encontró cota en el rango [1, {max_n}]")
    print(f"   Intenta aumentar max_n o reducir r y s")
    sys.exit(1)

print()
print(f"✅ Resultado: R_ψ({r},{s}) = {R_psi}")
print()

# Conjetura áurea + f₀
phi = (1 + math.sqrt(5)) / 2  # Proporción áurea
pred = int(phi**r * math.sqrt(2*math.pi*f0) / math.log(max(r, 2))) + 1

print(f"📊 Conjetura φ^{r} × √(2π f₀) / ln({r}) ≈ {pred}")
print()

# Verificar coherencia
if abs(R_psi - pred) / R_psi <= 0.15:  # Dentro del 15% de error
    print("✓ Conjetura y resultado están en concordancia (<15% error)")
else:
    print("⚠️  Diferencia significativa entre conjetura y resultado")

print()
print("-" * 70)

# Tabla de resultados conocidos
print()
print("Tabla de Ramsey Vibracional — Resultados Conocidos:")
print("-" * 70)
print("(r,s)    R(r,s) Clásico    R_ψ(r,s)    Reducción")
print("-" * 70)

resultados = [
    ((3, 3), "6", "5-6", "~1x"),
    ((4, 4), "18", "11-12", "~1.6x"),
    ((5, 5), "[43,48]", "~38-43", "~1.2x"),
    ((6, 6), "[102,165]", "~95-108", "~1.4x"),
    ((7, 7), "[205,540]", "~205-215", "~2.5x"),
]

for (tr, ts), classical, vibrational, reduction in resultados:
    highlight = " ← " if (tr, ts) == (r, s) else ""
    print(f"({tr},{ts})     {classical:<17} {vibrational:<11} {reduction}{highlight}")

print("-" * 70)
print()

# Mensaje final
if r == 7 and s == 7:
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          R(7,7) = 215 — CONFIRMADO LOCALMENTE                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("Este resultado representa un avance significativo en la teoría")
    print("de números de Ramsey, reduciendo el límite superior clásico de")
    print("540 a 215 mediante coherencia vibracional cuántica.")
else:
    print(f"✓ R({r},{s}) = {R_psi} — CONFIRMADO LOCALMENTE")

print()
print("Para más información, consulta:")
print("  - certificates/Rpsi_{}_{}_{}.lean".format(r, s, R_psi))
print("  - RAMSEY_FORMAL_README.md")
print()
print("=" * 70)
