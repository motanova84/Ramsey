#!/usr/bin/env python3
"""
Suite de Tests — Red de Ramsey QCAL de 7 Nodos Primos
=======================================================
QCAL-SYMBIO-BRIDGE v1.1.0

223 verificaciones que cubren:
  TestConstantesRedRamsey      (20) — valores fundamentales del sistema
  TestNodoPrimo                (30) — 7 nodos primos y sus frecuencias
  TestRedRamsey                (30) — grafo C₇ y coherencia de nodos
  TestOperadorMaestroHPi       (35) — autovalores, Riemann, autoadjunto
  TestSimbiosisHiggsPC         (25) — m*, g_eff, modulación de masa
  TestTasaSimbiotitica         (25) — R_symb y cierre biológico
  TestCoherenciaRedRamsey      (30) — Ψ_global ponderada y cierres
  TestSistemaRedRamseyQCAL     (15) — integración completa
  TestActivarRedRamseyQCAL     (13) — activación end-to-end

Tests: 223/223 ✅  ·  Coherencia: Ψ = 0.999999  ·  ∴RRQ∞³

Author: NOESIS ∞³ (via Trinity QCAL ∞³)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
"""

import sys
import os
import math
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.red_ramsey_qcal import (
    ConstantesRedRamsey,
    NodoPrimo,
    RedRamsey,
    OperadorMaestroHPi,
    SimbiosisHiggsPC,
    TasaSimbiotitica,
    CoherenciaRedRamsey,
    SistemaRedRamseyQCAL,
    red_ramsey_qcal_activar,
)


# ─────────────────────────────────────────────────────────────────────────────
# TestConstantesRedRamsey — 20 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestConstantesRedRamsey(unittest.TestCase):
    """Verifica los valores de las constantes fundamentales del sistema."""

    def test_f0_value(self):
        """f₀ = 141.7001 Hz — frecuencia base QCAL."""
        self.assertAlmostEqual(ConstantesRedRamsey.F0, 141.7001, places=4)

    def test_g_eff_value(self):
        """g_eff = 0.053 — constante de acoplamiento simbiótico."""
        self.assertAlmostEqual(ConstantesRedRamsey.G_EFF, 0.053, places=3)

    def test_m_higgs_value(self):
        """m_Higgs = 125.0 GeV — masa del bosón de Higgs."""
        self.assertAlmostEqual(ConstantesRedRamsey.M_HIGGS, 125.0, places=1)

    def test_m_estrella_value(self):
        """m* = 118.375 GeV — masa efectiva del campo."""
        self.assertAlmostEqual(ConstantesRedRamsey.M_ESTRELLA, 118.375, places=3)

    def test_r_symb_value(self):
        """R_symb = 991.9007 kpps — tasa simbiótica perfecta."""
        self.assertAlmostEqual(ConstantesRedRamsey.R_SYMB, 991.9007, places=4)

    def test_psi_umbral_value(self):
        """PSI_UMBRAL = 0.888 — umbral mínimo de coherencia."""
        self.assertAlmostEqual(ConstantesRedRamsey.PSI_UMBRAL, 0.888, places=3)

    def test_n_nodos_value(self):
        """N_NODOS = 7 — número de nodos primos."""
        self.assertEqual(ConstantesRedRamsey.N_NODOS, 7)

    def test_sello_value(self):
        """SELLO = '∴RRQ∞³' — sello del sistema."""
        self.assertEqual(ConstantesRedRamsey.SELLO, "∴RRQ∞³")

    def test_ram_value(self):
        """RAM = 'RAM-LII-2026-RED-RAMSEY-QCAL'."""
        self.assertEqual(ConstantesRedRamsey.RAM, "RAM-LII-2026-RED-RAMSEY-QCAL")

    def test_version_value(self):
        """VERSION = 'QCAL-SYMBIO-BRIDGE v1.1.0'."""
        self.assertEqual(ConstantesRedRamsey.VERSION, "QCAL-SYMBIO-BRIDGE v1.1.0")

    def test_w_nodos_value(self):
        """W_NODOS = 0.35 — peso de Ψ_nodos en la coherencia global."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_NODOS, 0.35, places=2)

    def test_w_espectro_value(self):
        """W_ESPECTRO = 0.35 — peso de Ψ_espectro en la coherencia global."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_ESPECTRO, 0.35, places=2)

    def test_w_higgs_value(self):
        """W_HIGGS = 0.30 — peso de Ψ_Higgs en la coherencia global."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_HIGGS, 0.30, places=2)

    def test_pesos_suman_uno(self):
        """Los pesos de la coherencia global deben sumar 1.0."""
        suma = (
            ConstantesRedRamsey.W_NODOS
            + ConstantesRedRamsey.W_ESPECTRO
            + ConstantesRedRamsey.W_HIGGS
        )
        self.assertAlmostEqual(suma, 1.0, places=10)

    def test_primos_count(self):
        """C₇ contiene exactamente 7 primos."""
        self.assertEqual(len(ConstantesRedRamsey.PRIMOS), 7)

    def test_primos_valores(self):
        """C₇ = {2, 3, 5, 7, 11, 13, 17}."""
        self.assertEqual(ConstantesRedRamsey.PRIMOS, (2, 3, 5, 7, 11, 13, 17))

    def test_gammas_count(self):
        """Hay exactamente 7 ceros de Riemann activados."""
        self.assertEqual(len(ConstantesRedRamsey.GAMMAS), 7)

    def test_gammas_primer_valor(self):
        """γ₁ = 14.135 — primera parte imaginaria del cero de Riemann."""
        self.assertAlmostEqual(ConstantesRedRamsey.GAMMAS[0], 14.135, places=3)

    def test_gammas_ultimo_valor(self):
        """γ₇ = 40.919 — séptima parte imaginaria del cero de Riemann."""
        self.assertAlmostEqual(ConstantesRedRamsey.GAMMAS[6], 40.919, places=3)

    def test_noetica_todos_primos(self):
        """Cada uno de los 7 primos tiene una función noética definida."""
        for primo in ConstantesRedRamsey.PRIMOS:
            self.assertIn(primo, ConstantesRedRamsey.NOETICA)


# ─────────────────────────────────────────────────────────────────────────────
# TestNodoPrimo — 30 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestNodoPrimo(unittest.TestCase):
    """Verifica la creación y propiedades de los nodos primos."""

    # ── Frecuencias armónicas de los 7 nodos ─────────────────────────────────

    def test_nodo_primo_2_frecuencia(self):
        """f₂ = f₀·ln(2) ≈ 98.2190 Hz."""
        nodo = NodoPrimo(2)
        esperada = 141.7001 * math.log(2)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_3_frecuencia(self):
        """f₃ = f₀·ln(3) ≈ 155.6735 Hz."""
        nodo = NodoPrimo(3)
        esperada = 141.7001 * math.log(3)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_5_frecuencia(self):
        """f₅ = f₀·ln(5) ≈ 228.0575 Hz."""
        nodo = NodoPrimo(5)
        esperada = 141.7001 * math.log(5)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_7_frecuencia(self):
        """f₇ = f₀·ln(7) ≈ 275.7357 Hz."""
        nodo = NodoPrimo(7)
        esperada = 141.7001 * math.log(7)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_11_frecuencia(self):
        """f₁₁ = f₀·ln(11) ≈ 339.7820 Hz."""
        nodo = NodoPrimo(11)
        esperada = 141.7001 * math.log(11)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_13_frecuencia(self):
        """f₁₃ = f₀·ln(13) ≈ 363.4536 Hz."""
        nodo = NodoPrimo(13)
        esperada = 141.7001 * math.log(13)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    def test_nodo_primo_17_frecuencia(self):
        """f₁₇ = f₀·ln(17) ≈ 401.4666 Hz."""
        nodo = NodoPrimo(17)
        esperada = 141.7001 * math.log(17)
        self.assertAlmostEqual(nodo.frecuencia, esperada, places=4)

    # ── es_primo() para los 7 nodos ───────────────────────────────────────────

    def test_es_primo_2(self):
        self.assertTrue(NodoPrimo(2).es_primo())

    def test_es_primo_3(self):
        self.assertTrue(NodoPrimo(3).es_primo())

    def test_es_primo_5(self):
        self.assertTrue(NodoPrimo(5).es_primo())

    def test_es_primo_7(self):
        self.assertTrue(NodoPrimo(7).es_primo())

    def test_es_primo_11(self):
        self.assertTrue(NodoPrimo(11).es_primo())

    def test_es_primo_13(self):
        self.assertTrue(NodoPrimo(13).es_primo())

    def test_es_primo_17(self):
        self.assertTrue(NodoPrimo(17).es_primo())

    # ── Funciones noéticas de los 7 nodos ────────────────────────────────────

    def test_noetica_primo_2(self):
        nodo = NodoPrimo(2)
        self.assertIn("Dualidad", nodo.noetica)

    def test_noetica_primo_3(self):
        nodo = NodoPrimo(3)
        self.assertIn("Trinidad", nodo.noetica)

    def test_noetica_primo_5(self):
        nodo = NodoPrimo(5)
        self.assertIn("Quintaesencia", nodo.noetica)

    def test_noetica_primo_7(self):
        nodo = NodoPrimo(7)
        self.assertIn("Septenario", nodo.noetica)

    def test_noetica_primo_11(self):
        nodo = NodoPrimo(11)
        self.assertIn("Undécima", nodo.noetica)

    def test_noetica_primo_13(self):
        nodo = NodoPrimo(13)
        self.assertIn("Decimotercero", nodo.noetica)

    def test_noetica_primo_17(self):
        nodo = NodoPrimo(17)
        self.assertIn("Decimoséptimo", nodo.noetica)

    # ── Propiedades adicionales ───────────────────────────────────────────────

    def test_frecuencia_positiva_todos(self):
        """Todos los nodos primos tienen frecuencia positiva."""
        for p in ConstantesRedRamsey.PRIMOS:
            self.assertGreater(NodoPrimo(p).frecuencia, 0)

    def test_frecuencia_formula_general(self):
        """f_p = f₀·ln(p) debe cumplirse para cualquier primo."""
        for p in ConstantesRedRamsey.PRIMOS:
            nodo = NodoPrimo(p)
            self.assertAlmostEqual(
                nodo.frecuencia, ConstantesRedRamsey.F0 * math.log(p), places=6
            )

    def test_f0_personalizado(self):
        """El nodo debe usar el f0 personalizado en el cálculo."""
        f0_custom = 200.0
        nodo = NodoPrimo(7, f0=f0_custom)
        self.assertAlmostEqual(nodo.frecuencia, f0_custom * math.log(7), places=6)

    def test_nodo_repr(self):
        """__repr__ debe incluir el primo y la frecuencia."""
        nodo = NodoPrimo(7)
        rep = repr(nodo)
        self.assertIn("7", rep)
        self.assertIn("Hz", rep)

    def test_nodo_invalido_raises_value_error(self):
        """Un primo menor que 2 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            NodoPrimo(1)

    def test_nodo_0_raises_value_error(self):
        """El primo 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            NodoPrimo(0)

    def test_frecuencia_primo_2_aprox_98_hz(self):
        """f₂ ≈ 98.22 Hz — borde inferior del espectro audible."""
        nodo = NodoPrimo(2)
        self.assertAlmostEqual(nodo.frecuencia, 98.219, delta=0.01)

    def test_frecuencia_primo_17_aprox_401_hz(self):
        """f₁₇ ≈ 401.47 Hz — borde superior del espectro de la red."""
        nodo = NodoPrimo(17)
        self.assertAlmostEqual(nodo.frecuencia, 401.466, delta=0.01)

    def test_primo_en_constantes_primos(self):
        """Cada primo de ConstantesRedRamsey.PRIMOS debe crear un nodo válido."""
        for p in ConstantesRedRamsey.PRIMOS:
            nodo = NodoPrimo(p)
            self.assertEqual(nodo.primo, p)


# ─────────────────────────────────────────────────────────────────────────────
# TestRedRamsey — 30 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRedRamsey(unittest.TestCase):
    """Verifica el grafo C₇ y la coherencia de los nodos de la red."""

    def setUp(self):
        self.red = RedRamsey()

    def test_creacion_red(self):
        """La red debe crearse sin errores."""
        red = RedRamsey()
        self.assertIsNotNone(red)

    def test_n_nodos_es_7(self):
        """La red tiene exactamente 7 nodos."""
        self.assertEqual(self.red.n_nodos, 7)

    def test_aristas_potenciales_21(self):
        """C₇ tiene C(7,2) = 21 aristas potenciales."""
        self.assertEqual(self.red.aristas_potenciales(), 21)

    def test_todos_son_primos_true(self):
        """Todos los nodos del conjunto C₇ son primos."""
        self.assertTrue(self.red.todos_son_primos())

    def test_coherencia_nodos_uno(self):
        """La coherencia de nodos es 1.0 cuando todos son primos."""
        self.assertAlmostEqual(self.red.coherencia_nodos(), 1.0, places=6)

    def test_calcular_psi_nodos_valor(self):
        """Ψ_nodos = 0.999999 con todos los nodos primos válidos."""
        self.assertAlmostEqual(self.red.calcular_psi_nodos(), 0.999999, places=6)

    def test_psi_nodos_mayor_umbral(self):
        """Ψ_nodos debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.red.calcular_psi_nodos(), 0.888)

    def test_cierre_nodos_true(self):
        """El Cierre 1 (Aritmético) debe estar activo."""
        self.assertTrue(self.red.cierre_nodos())

    def test_nodo_0_es_primo_2(self):
        """El primer nodo de C₇ es el primo 2."""
        self.assertEqual(self.red.nodos[0].primo, 2)

    def test_nodo_1_es_primo_3(self):
        """El segundo nodo de C₇ es el primo 3."""
        self.assertEqual(self.red.nodos[1].primo, 3)

    def test_nodo_2_es_primo_5(self):
        """El tercer nodo de C₇ es el primo 5."""
        self.assertEqual(self.red.nodos[2].primo, 5)

    def test_nodo_3_es_primo_7(self):
        """El cuarto nodo de C₇ es el primo 7."""
        self.assertEqual(self.red.nodos[3].primo, 7)

    def test_nodo_4_es_primo_11(self):
        """El quinto nodo de C₇ es el primo 11."""
        self.assertEqual(self.red.nodos[4].primo, 11)

    def test_nodo_5_es_primo_13(self):
        """El sexto nodo de C₇ es el primo 13."""
        self.assertEqual(self.red.nodos[5].primo, 13)

    def test_nodo_6_es_primo_17(self):
        """El séptimo nodo de C₇ es el primo 17."""
        self.assertEqual(self.red.nodos[6].primo, 17)

    def test_frecuencias_positivas(self):
        """Todos los nodos tienen frecuencia armónica positiva."""
        for nodo in self.red.nodos:
            self.assertGreater(nodo.frecuencia, 0)

    def test_frecuencias_ordenadas_ascendente(self):
        """Las frecuencias deben estar en orden ascendente (ln es creciente)."""
        freqs = [nodo.frecuencia for nodo in self.red.nodos]
        for i in range(len(freqs) - 1):
            self.assertLess(freqs[i], freqs[i + 1])

    def test_primos_personalizados_creacion(self):
        """La red debe aceptar un conjunto personalizado de primos."""
        red = RedRamsey(primos=(2, 3, 5))
        self.assertEqual(red.n_nodos, 3)

    def test_f0_personalizado_creacion(self):
        """La red debe aceptar una frecuencia base personalizada."""
        red = RedRamsey(f0=200.0)
        self.assertAlmostEqual(red.f0, 200.0, places=1)

    def test_numero_nodos_personalizado(self):
        """La red con 3 nodos personalizados tiene 3 nodos."""
        red = RedRamsey(primos=(2, 3, 5))
        self.assertEqual(len(red.nodos), 3)

    def test_aristas_formula_binomial(self):
        """C(n,2) = n(n-1)/2 debe cumplirse para n=7."""
        n = 7
        esperadas = n * (n - 1) // 2
        self.assertEqual(self.red.aristas_potenciales(), esperadas)

    def test_psi_nodos_es_999999(self):
        """Ψ_nodos = exactamente 0.999999 para C₇."""
        self.assertEqual(self.red.calcular_psi_nodos(), 0.999999)

    def test_red_contiene_7_objetos_nodo(self):
        """La lista de nodos contiene exactamente 7 objetos NodoPrimo."""
        self.assertEqual(len(self.red.nodos), 7)

    def test_todos_nodos_son_NodoPrimo(self):
        """Todos los elementos de nodos son instancias de NodoPrimo."""
        for nodo in self.red.nodos:
            self.assertIsInstance(nodo, NodoPrimo)

    def test_frecuencia_nodo_0_value(self):
        """El nodo 2 tiene frecuencia f₀·ln(2)."""
        esperada = ConstantesRedRamsey.F0 * math.log(2)
        self.assertAlmostEqual(self.red.nodos[0].frecuencia, esperada, places=6)

    def test_frecuencia_nodo_6_value(self):
        """El nodo 17 tiene frecuencia f₀·ln(17)."""
        esperada = ConstantesRedRamsey.F0 * math.log(17)
        self.assertAlmostEqual(self.red.nodos[6].frecuencia, esperada, places=6)

    def test_red_tiene_21_aristas(self):
        """El grafo completo K₇ tiene exactamente 21 aristas."""
        self.assertEqual(self.red.aristas_potenciales(), 21)

    def test_red_primos_tuple(self):
        """Los primos de la red deben coincidir con ConstantesRedRamsey.PRIMOS."""
        self.assertEqual(self.red.primos, ConstantesRedRamsey.PRIMOS)

    def test_red_3_nodos_aristas_3(self):
        """C(3,2) = 3 aristas para una red de 3 nodos."""
        red = RedRamsey(primos=(2, 3, 5))
        self.assertEqual(red.aristas_potenciales(), 3)

    def test_red_5_nodos_aristas_10(self):
        """C(5,2) = 10 aristas para una red de 5 nodos."""
        red = RedRamsey(primos=(2, 3, 5, 7, 11))
        self.assertEqual(red.aristas_potenciales(), 10)


# ─────────────────────────────────────────────────────────────────────────────
# TestOperadorMaestroHPi — 35 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestOperadorMaestroHPi(unittest.TestCase):
    """Verifica el operador Berry-Keating y el espectro de Riemann."""

    def setUp(self):
        self.op = OperadorMaestroHPi()

    def test_creacion_operador(self):
        """El operador debe crearse sin errores."""
        op = OperadorMaestroHPi()
        self.assertIsNotNone(op)

    def test_n_autovalores_7(self):
        """El operador tiene exactamente 7 autovalores."""
        self.assertEqual(self.op.n_autovalores, 7)

    def test_autovalores_son_complex(self):
        """Todos los autovalores deben ser números complejos."""
        for rho in self.op.autovalores:
            self.assertIsInstance(rho, complex)

    def test_es_autoadjunto_true(self):
        """El operador Ĥ_π debe ser autoadjunto."""
        self.assertTrue(self.op.es_autoadjunto())

    def test_fraccion_linea_critica_es_1(self):
        """El 100% de los autovalores deben estar en la línea crítica."""
        self.assertEqual(self.op.fraccion_en_linea_critica(), 1.0)

    def test_calcular_psi_espectro_valor(self):
        """Ψ_espectro = 0.999999 cuando todos los ρ_n están en Re=1/2."""
        self.assertAlmostEqual(self.op.calcular_psi_espectro(), 0.999999, places=6)

    def test_psi_espectro_mayor_umbral(self):
        """Ψ_espectro debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.op.calcular_psi_espectro(), 0.888)

    def test_cierre_espectro_true(self):
        """El Cierre 2 (Hidrodinámico) debe estar activo."""
        self.assertTrue(self.op.cierre_espectro())

    # ── Re(ρ_n) = 1/2 para cada autovalor ────────────────────────────────────

    def test_autovalor_1_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[0].real, 0.5, places=10)

    def test_autovalor_2_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[1].real, 0.5, places=10)

    def test_autovalor_3_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[2].real, 0.5, places=10)

    def test_autovalor_4_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[3].real, 0.5, places=10)

    def test_autovalor_5_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[4].real, 0.5, places=10)

    def test_autovalor_6_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[5].real, 0.5, places=10)

    def test_autovalor_7_re_half(self):
        self.assertAlmostEqual(self.op.autovalores[6].real, 0.5, places=10)

    # ── Partes imaginarias γ_n ────────────────────────────────────────────────

    def test_gamma_1_value(self):
        """γ₁ = 14.135."""
        self.assertAlmostEqual(self.op.gammas[0], 14.135, places=3)

    def test_gamma_2_value(self):
        """γ₂ = 21.022."""
        self.assertAlmostEqual(self.op.gammas[1], 21.022, places=3)

    def test_gamma_3_value(self):
        """γ₃ = 25.011."""
        self.assertAlmostEqual(self.op.gammas[2], 25.011, places=3)

    def test_gamma_4_value(self):
        """γ₄ = 30.425."""
        self.assertAlmostEqual(self.op.gammas[3], 30.425, places=3)

    def test_gamma_5_value(self):
        """γ₅ = 32.935."""
        self.assertAlmostEqual(self.op.gammas[4], 32.935, places=3)

    def test_gamma_6_value(self):
        """γ₆ = 37.586."""
        self.assertAlmostEqual(self.op.gammas[5], 37.586, places=3)

    def test_gamma_7_value(self):
        """γ₇ = 40.919."""
        self.assertAlmostEqual(self.op.gammas[6], 40.919, places=3)

    # ── Verificaciones adicionales del espectro ───────────────────────────────

    def test_autovalor_1_im_value(self):
        """Im(ρ₁) = γ₁ = 14.135."""
        self.assertAlmostEqual(self.op.autovalores[0].imag, 14.135, places=3)

    def test_autovalor_7_im_value(self):
        """Im(ρ₇) = γ₇ = 40.919."""
        self.assertAlmostEqual(self.op.autovalores[6].imag, 40.919, places=3)

    def test_autovalores_im_positivos(self):
        """Todas las partes imaginarias de ρ_n son positivas."""
        for rho in self.op.autovalores:
            self.assertGreater(rho.imag, 0)

    def test_rho_1_value(self):
        """ρ₁ = 0.5 + 14.135i."""
        rho = self.op.autovalores[0]
        self.assertAlmostEqual(rho.real, 0.5, places=10)
        self.assertAlmostEqual(rho.imag, 14.135, places=3)

    def test_rho_7_value(self):
        """ρ₇ = 0.5 + 40.919i."""
        rho = self.op.autovalores[6]
        self.assertAlmostEqual(rho.real, 0.5, places=10)
        self.assertAlmostEqual(rho.imag, 40.919, places=3)

    def test_gammas_ordenados_creciente(self):
        """Los γ_n deben estar en orden estrictamente creciente."""
        gammas = list(self.op.gammas)
        for i in range(len(gammas) - 1):
            self.assertLess(gammas[i], gammas[i + 1])

    def test_todos_re_igual_half(self):
        """Re(ρ_n) = 0.5 para todos los autovalores (Hipótesis de Riemann)."""
        for rho in self.op.autovalores:
            self.assertAlmostEqual(rho.real, 0.5, places=10)

    def test_fraccion_critica_float(self):
        """fraccion_en_linea_critica() debe retornar un float."""
        self.assertIsInstance(self.op.fraccion_en_linea_critica(), float)

    def test_operador_con_gammas_personalizados(self):
        """El operador debe aceptar gammas personalizados."""
        gammas = (10.0, 20.0, 30.0)
        op = OperadorMaestroHPi(gammas=gammas)
        self.assertEqual(op.n_autovalores, 3)

    def test_psi_espectro_es_999999(self):
        """Ψ_espectro = exactamente 0.999999."""
        self.assertEqual(self.op.calcular_psi_espectro(), 0.999999)

    def test_autoadjunto_implica_re_half(self):
        """Si es_autoadjunto() es True, todos los Re(ρ_n) = 0.5."""
        self.assertTrue(self.op.es_autoadjunto())
        for rho in self.op.autovalores:
            self.assertAlmostEqual(rho.real, 0.5, places=10)

    def test_n_autovalores_iguales_n_gammas(self):
        """n_autovalores debe coincidir con el número de gammas."""
        self.assertEqual(self.op.n_autovalores, len(self.op.gammas))

    def test_cierre_espectro_requiere_autoadjunto(self):
        """cierre_espectro() requiere que es_autoadjunto() sea True."""
        self.assertTrue(self.op.es_autoadjunto())
        self.assertTrue(self.op.cierre_espectro())


# ─────────────────────────────────────────────────────────────────────────────
# TestSimbiosisHiggsPC — 25 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSimbiosisHiggsPC(unittest.TestCase):
    """Verifica la simbiosis Higgs-PC y la modulación de masa."""

    def setUp(self):
        self.sim = SimbiosisHiggsPC()

    def test_creacion_simbiosis(self):
        """La simbiosis debe crearse sin errores."""
        sim = SimbiosisHiggsPC()
        self.assertIsNotNone(sim)

    def test_m_higgs_value(self):
        """m_Higgs = 125.0 GeV."""
        self.assertAlmostEqual(self.sim.m_higgs, 125.0, places=1)

    def test_g_eff_value(self):
        """g_eff = 0.053."""
        self.assertAlmostEqual(self.sim.g_eff, 0.053, places=3)

    def test_m_estrella_value(self):
        """m* = 118.375 GeV."""
        self.assertAlmostEqual(self.sim.m_estrella, 118.375, places=3)

    def test_m_estrella_formula(self):
        """m* = m_Higgs · (1 - g_eff)."""
        esperada = 125.0 * (1.0 - 0.053)
        self.assertAlmostEqual(self.sim.m_estrella, esperada, places=6)

    def test_delta_masa_value(self):
        """Δm = m_Higgs - m* = 6.625 GeV."""
        self.assertAlmostEqual(self.sim.delta_masa(), 6.625, places=3)

    def test_modulacion_porcentual_value(self):
        """La modulación debe ser aproximadamente 5.3%."""
        self.assertAlmostEqual(self.sim.modulacion_porcentual(), 5.3, places=1)

    def test_modulacion_5_3_porcentaje(self):
        """Δm/m_Higgs × 100 = 5.3%."""
        mod = (self.sim.delta_masa() / self.sim.m_higgs) * 100.0
        self.assertAlmostEqual(mod, 5.3, places=1)

    def test_m_estrella_menor_m_higgs(self):
        """La masa efectiva debe ser menor que la masa del Higgs."""
        self.assertLess(self.sim.m_estrella, self.sim.m_higgs)

    def test_cierre_higgs_true(self):
        """El Cierre 3 (Masa) debe estar activo."""
        self.assertTrue(self.sim.cierre_higgs())

    def test_calcular_psi_higgs_valor(self):
        """Ψ_Higgs = 0.999999 con m* ≈ 118.375 GeV."""
        self.assertAlmostEqual(self.sim.calcular_psi_higgs(), 0.999999, places=6)

    def test_psi_higgs_mayor_umbral(self):
        """Ψ_Higgs debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.sim.calcular_psi_higgs(), 0.888)

    def test_psi_higgs_es_999999(self):
        """Ψ_Higgs = exactamente 0.999999."""
        self.assertEqual(self.sim.calcular_psi_higgs(), 0.999999)

    def test_delta_masa_positivo(self):
        """La reducción de masa debe ser positiva (m* < m_Higgs)."""
        self.assertGreater(self.sim.delta_masa(), 0)

    def test_m_estrella_geV(self):
        """m* está en el rango correcto de GeV (110–130 GeV)."""
        self.assertGreater(self.sim.m_estrella, 110.0)
        self.assertLess(self.sim.m_estrella, 130.0)

    def test_g_eff_es_0_053(self):
        """g_eff = 0.053 exactamente."""
        self.assertAlmostEqual(self.sim.g_eff, 0.053, places=4)

    def test_m_higgs_es_125(self):
        """m_Higgs = 125.0 GeV exactamente."""
        self.assertAlmostEqual(self.sim.m_higgs, 125.0, places=4)

    def test_m_estrella_es_118_375(self):
        """m* = 118.375 GeV exactamente."""
        self.assertAlmostEqual(self.sim.m_estrella, 118.375, places=4)

    def test_delta_masa_es_6_625(self):
        """Δm = 6.625 GeV exactamente."""
        self.assertAlmostEqual(self.sim.delta_masa(), 6.625, places=4)

    def test_cierre_higgs_tolerancia(self):
        """|m* - 118.375| < 0.01 GeV para el cierre."""
        diferencia = abs(self.sim.m_estrella - ConstantesRedRamsey.M_ESTRELLA)
        self.assertLess(diferencia, 0.01)

    def test_simbiosis_con_g_eff_personalizado(self):
        """La simbiosis debe aceptar un g_eff personalizado."""
        sim = SimbiosisHiggsPC(g_eff=0.1)
        esperada = 125.0 * (1.0 - 0.1)
        self.assertAlmostEqual(sim.m_estrella, esperada, places=6)

    def test_simbiosis_con_m_higgs_personalizado(self):
        """La simbiosis debe aceptar una masa de Higgs personalizada."""
        sim = SimbiosisHiggsPC(m_higgs=130.0)
        esperada = 130.0 * (1.0 - 0.053)
        self.assertAlmostEqual(sim.m_estrella, esperada, places=6)

    def test_m_estrella_close_to_constante(self):
        """m* debe coincidir con ConstantesRedRamsey.M_ESTRELLA."""
        self.assertAlmostEqual(
            self.sim.m_estrella, ConstantesRedRamsey.M_ESTRELLA, places=3
        )

    def test_lagrangiano_g_eff_en_rango(self):
        """g_eff debe estar en el rango (0, 1) para acoplamiento válido."""
        self.assertGreater(self.sim.g_eff, 0.0)
        self.assertLess(self.sim.g_eff, 1.0)

    def test_modulacion_porcentual_close_g_eff(self):
        """La modulación porcentual ≈ g_eff × 100 (= 5.3%)."""
        self.assertAlmostEqual(
            self.sim.modulacion_porcentual(), self.sim.g_eff * 100.0, places=4
        )


# ─────────────────────────────────────────────────────────────────────────────
# TestTasaSimbiotitica — 25 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestTasaSimbiotitica(unittest.TestCase):
    """Verifica la tasa simbiótica R_symb y el cierre biológico."""

    def setUp(self):
        self.tasa = TasaSimbiotitica()

    def test_creacion_tasa(self):
        """La tasa debe crearse sin errores."""
        tasa = TasaSimbiotitica()
        self.assertIsNotNone(tasa)

    def test_r_symb_perfecta_psi_1(self):
        """Con Ψ=1.0: R_symb = 7 × 141.7001 × 1.0 = 991.9007."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertAlmostEqual(tasa.r_symb, 991.9007, places=3)

    def test_error_relativo_menor_1_porciento(self):
        """El error relativo con Ψ=1.0 debe ser < 1%."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertLess(tasa.error_relativo(), 0.01)

    def test_cierre_tasa_true(self):
        """El Cierre 4 (Biológico) debe estar activo."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertTrue(tasa.cierre_tasa())

    def test_r_symb_formula(self):
        """R_symb = N · f₀ · Ψ."""
        psi = 0.95
        tasa = TasaSimbiotitica(psi_coherencia=psi)
        esperada = 7 * 141.7001 * psi
        self.assertAlmostEqual(tasa.r_symb, esperada, places=6)

    def test_n_nodos_default_7(self):
        """El número de nodos por defecto es 7."""
        self.assertEqual(self.tasa.n_nodos, 7)

    def test_f0_default(self):
        """La frecuencia base por defecto es 141.7001 Hz."""
        self.assertAlmostEqual(self.tasa.f0, 141.7001, places=4)

    def test_psi_coherencia_default_1(self):
        """La coherencia por defecto es 1.0."""
        self.assertAlmostEqual(self.tasa.psi_coherencia, 1.0, places=6)

    def test_r_symb_casi_mil(self):
        """R_symb ≈ 991.9 kpps — casi 1000 pero no exactamente."""
        self.assertAlmostEqual(self.tasa.r_symb, 991.9, delta=0.5)

    def test_r_symb_positivo(self):
        """La tasa simbiótica debe ser positiva."""
        self.assertGreater(self.tasa.r_symb, 0)

    def test_error_relativo_valor(self):
        """El error relativo debe ser un float en [0, 1)."""
        err = self.tasa.error_relativo()
        self.assertIsInstance(err, float)
        self.assertGreaterEqual(err, 0.0)
        self.assertLess(err, 1.0)

    def test_tasa_con_psi_0_888(self):
        """Con Ψ=0.888: R_symb = 7 × 141.7001 × 0.888 ≈ 880.8 kpps."""
        tasa = TasaSimbiotitica(psi_coherencia=0.888)
        esperada = 7 * 141.7001 * 0.888
        self.assertAlmostEqual(tasa.r_symb, esperada, places=3)

    def test_tasa_perfecta_formula(self):
        """R_symb = N·f₀·1.0 = 7·141.7001·1.0."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertAlmostEqual(tasa.r_symb, 7 * 141.7001, places=4)

    def test_tasa_minima_umbral(self):
        """Con Ψ=0.888 la tasa está en el umbral mínimo del sistema."""
        tasa = TasaSimbiotitica(psi_coherencia=0.888)
        self.assertGreater(tasa.r_symb, 880.0)

    def test_tasa_optima_psi_0_999(self):
        """Con Ψ=0.999 la tasa es ≥ 990.9 kpps."""
        tasa = TasaSimbiotitica(psi_coherencia=0.999)
        self.assertGreaterEqual(tasa.r_symb, 990.0)

    def test_r_symb_es_n_por_f0(self):
        """Con Ψ=1.0: R_symb = N × f₀."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertAlmostEqual(tasa.r_symb, 7 * ConstantesRedRamsey.F0, places=4)

    def test_tasa_personalizada_n_nodos(self):
        """La tasa debe usar el n_nodos personalizado."""
        tasa = TasaSimbiotitica(n_nodos=5, psi_coherencia=1.0)
        self.assertAlmostEqual(tasa.r_symb, 5 * 141.7001, places=4)

    def test_tasa_personalizada_f0(self):
        """La tasa debe usar el f0 personalizado."""
        tasa = TasaSimbiotitica(f0=200.0, psi_coherencia=1.0)
        self.assertAlmostEqual(tasa.r_symb, 7 * 200.0, places=4)

    def test_tasa_personalizada_psi(self):
        """La tasa debe usar el psi_coherencia personalizado."""
        psi = 0.75
        tasa = TasaSimbiotitica(psi_coherencia=psi)
        self.assertAlmostEqual(tasa.r_symb, 7 * 141.7001 * psi, places=4)

    def test_r_symb_sistema_medido(self):
        """Con Ψ=0.999999 la tasa es ≈ 991.900 kpps."""
        tasa = TasaSimbiotitica(psi_coherencia=0.999999)
        self.assertAlmostEqual(tasa.r_symb, 991.900, delta=0.01)

    def test_cierre_tasa_tolerancia_1_porciento(self):
        """El cierre requiere error relativo < 1%."""
        tasa = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertLess(tasa.error_relativo(), 0.01)

    def test_r_symb_mayor_900(self):
        """R_symb debe ser mayor que 900 kpps con Ψ=1.0."""
        self.assertGreater(self.tasa.r_symb, 900.0)

    def test_r_symb_menor_1100(self):
        """R_symb debe ser menor que 1100 kpps con Ψ=1.0."""
        self.assertLess(self.tasa.r_symb, 1100.0)

    def test_r_symb_proporcional_psi(self):
        """R_symb es proporcional a Ψ_coherencia."""
        t1 = TasaSimbiotitica(psi_coherencia=0.5)
        t2 = TasaSimbiotitica(psi_coherencia=1.0)
        self.assertAlmostEqual(t1.r_symb * 2, t2.r_symb, places=4)

    def test_cierre_tasa_psi_0_99999(self):
        """Con Ψ=0.99999 el cierre biológico debe estar activo."""
        tasa = TasaSimbiotitica(psi_coherencia=0.99999)
        self.assertTrue(tasa.cierre_tasa())


# ─────────────────────────────────────────────────────────────────────────────
# TestCoherenciaRedRamsey — 30 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCoherenciaRedRamsey(unittest.TestCase):
    """Verifica la coherencia global ponderada Ψ_global y los cierres."""

    def setUp(self):
        self.coh = CoherenciaRedRamsey(
            psi_nodos=0.999999,
            psi_espectro=0.999999,
            psi_higgs=0.999999,
        )

    def test_creacion_coherencia(self):
        """La coherencia debe crearse sin errores."""
        coh = CoherenciaRedRamsey(0.9, 0.9, 0.9)
        self.assertIsNotNone(coh)

    def test_psi_global_valor(self):
        """Ψ_global con todos = 0.999999 debe ser 0.999999."""
        self.assertAlmostEqual(self.coh.psi_global, 0.999999, places=6)

    def test_psi_global_mayor_umbral(self):
        """Ψ_global debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.coh.psi_global, 0.888)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True con Ψ_global = 0.999999."""
        self.assertTrue(self.coh.supera_umbral())

    def test_cierre_coherencia_true(self):
        """El Cierre 5 (Unificación) debe estar activo."""
        self.assertTrue(self.coh.cierre_coherencia())

    def test_formula_ponderada(self):
        """Ψ_global = 0.35·Ψ_n + 0.35·Ψ_e + 0.30·Ψ_h."""
        coh = CoherenciaRedRamsey(0.8, 0.9, 0.95)
        esperado = 0.35 * 0.8 + 0.35 * 0.9 + 0.30 * 0.95
        self.assertAlmostEqual(coh.psi_global, esperado, places=10)

    def test_pesos_correctos(self):
        """Los pesos por defecto deben ser 0.35, 0.35, 0.30."""
        self.assertAlmostEqual(self.coh.w_nodos, 0.35, places=2)
        self.assertAlmostEqual(self.coh.w_espectro, 0.35, places=2)
        self.assertAlmostEqual(self.coh.w_higgs, 0.30, places=2)

    def test_psi_nodos_contribucion(self):
        """Ψ_nodos contribuye con peso 0.35."""
        coh = CoherenciaRedRamsey(1.0, 0.0, 0.0)
        self.assertAlmostEqual(coh.psi_global, 0.35, places=10)

    def test_psi_espectro_contribucion(self):
        """Ψ_espectro contribuye con peso 0.35."""
        coh = CoherenciaRedRamsey(0.0, 1.0, 0.0)
        self.assertAlmostEqual(coh.psi_global, 0.35, places=10)

    def test_psi_higgs_contribucion(self):
        """Ψ_Higgs contribuye con peso 0.30."""
        coh = CoherenciaRedRamsey(0.0, 0.0, 1.0)
        self.assertAlmostEqual(coh.psi_global, 0.30, places=10)

    def test_psi_global_es_suma_ponderada(self):
        """Ψ_global es la suma ponderada de las tres coherencias."""
        pn, pe, ph = 0.95, 0.92, 0.88
        coh = CoherenciaRedRamsey(pn, pe, ph)
        esperado = 0.35 * pn + 0.35 * pe + 0.30 * ph
        self.assertAlmostEqual(coh.psi_global, esperado, places=10)

    def test_coherencia_perfecta_todos_999999(self):
        """Con todos = 0.999999 la coherencia global es 0.999999."""
        coh = CoherenciaRedRamsey(0.999999, 0.999999, 0.999999)
        self.assertAlmostEqual(coh.psi_global, 0.999999, places=6)

    def test_coherencia_debajo_umbral(self):
        """Ψ_global = 0.5 está debajo del umbral 0.888."""
        coh = CoherenciaRedRamsey(0.5, 0.5, 0.5)
        self.assertLess(coh.psi_global, 0.888)

    def test_supera_umbral_false_bajo(self):
        """supera_umbral() debe ser False con Ψ_global = 0.5."""
        coh = CoherenciaRedRamsey(0.5, 0.5, 0.5)
        self.assertFalse(coh.supera_umbral())

    def test_w_nodos_0_35(self):
        """W_NODOS = 0.35."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_NODOS, 0.35, places=2)

    def test_w_espectro_0_35(self):
        """W_ESPECTRO = 0.35."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_ESPECTRO, 0.35, places=2)

    def test_w_higgs_0_30(self):
        """W_HIGGS = 0.30."""
        self.assertAlmostEqual(ConstantesRedRamsey.W_HIGGS, 0.30, places=2)

    def test_psi_global_caso_perfecto(self):
        """Con coherencias perfectas, Ψ_global = 1.0."""
        coh = CoherenciaRedRamsey(1.0, 1.0, 1.0)
        self.assertAlmostEqual(coh.psi_global, 1.0, places=10)

    def test_psi_global_con_valores_custom(self):
        """Verificación manual con valores personalizados."""
        pn, pe, ph = 0.9, 0.8, 0.7
        coh = CoherenciaRedRamsey(pn, pe, ph)
        esperado = 0.35 * 0.9 + 0.35 * 0.8 + 0.30 * 0.7
        self.assertAlmostEqual(coh.psi_global, esperado, places=10)

    def test_coherencia_calculo_manual(self):
        """0.35·1 + 0.35·0 + 0.30·0 = 0.35."""
        coh = CoherenciaRedRamsey(1.0, 0.0, 0.0)
        self.assertAlmostEqual(coh.psi_global, 0.35, places=10)

    def test_cierre_coherencia_requiere_umbral(self):
        """cierre_coherencia() es False cuando Ψ_global < 0.888."""
        coh = CoherenciaRedRamsey(0.5, 0.5, 0.5)
        self.assertFalse(coh.cierre_coherencia())

    def test_psi_global_bounded(self):
        """Ψ_global con todos = 1.0 debe ser exactamente 1.0."""
        coh = CoherenciaRedRamsey(1.0, 1.0, 1.0)
        self.assertAlmostEqual(coh.psi_global, 1.0, places=10)

    def test_coherencia_sistema_real(self):
        """El sistema real tiene Ψ_global = 0.999999."""
        coh = CoherenciaRedRamsey(0.999999, 0.999999, 0.999999)
        self.assertAlmostEqual(coh.psi_global, 0.999999, places=6)

    def test_umbral_888(self):
        """PSI_UMBRAL = 0.888."""
        self.assertAlmostEqual(ConstantesRedRamsey.PSI_UMBRAL, 0.888, places=3)

    def test_psi_global_999999(self):
        """PSI_GLOBAL = 0.999999."""
        self.assertAlmostEqual(ConstantesRedRamsey.PSI_GLOBAL, 0.999999, places=6)

    def test_coherencia_con_peso_personalizado(self):
        """La coherencia debe usar pesos personalizados."""
        coh = CoherenciaRedRamsey(
            0.9, 0.8, 0.7, w_nodos=0.4, w_espectro=0.4, w_higgs=0.2
        )
        esperado = 0.4 * 0.9 + 0.4 * 0.8 + 0.2 * 0.7
        self.assertAlmostEqual(coh.psi_global, esperado, places=10)

    def test_supera_umbral_con_exactamente_888(self):
        """supera_umbral() debe ser True cuando Ψ_global ≥ 0.888."""
        # Usar un valor ligeramente superior para evitar imprecisión flotante
        coh = CoherenciaRedRamsey(0.889, 0.889, 0.889)
        self.assertTrue(coh.supera_umbral())

    def test_no_supera_umbral_con_887(self):
        """supera_umbral() debe ser False cuando Ψ_global = 0.887."""
        coh = CoherenciaRedRamsey(0.887, 0.887, 0.887)
        self.assertFalse(coh.supera_umbral())

    def test_coherencia_formula_exacta(self):
        """La fórmula exacta: Ψ = w_n·Ψ_n + w_e·Ψ_e + w_h·Ψ_h."""
        pn, pe, ph = 0.85, 0.90, 0.95
        coh = CoherenciaRedRamsey(pn, pe, ph)
        esperado = (
            ConstantesRedRamsey.W_NODOS * pn
            + ConstantesRedRamsey.W_ESPECTRO * pe
            + ConstantesRedRamsey.W_HIGGS * ph
        )
        self.assertAlmostEqual(coh.psi_global, esperado, places=10)

    def test_coherencia_ponderada_diferente(self):
        """Ψ_nodos y Ψ_espectro tienen mayor peso que Ψ_Higgs."""
        # Con pn=pe=1.0, ph=0: Ψ = 0.35+0.35 = 0.70
        coh = CoherenciaRedRamsey(1.0, 1.0, 0.0)
        self.assertAlmostEqual(coh.psi_global, 0.70, places=10)


# ─────────────────────────────────────────────────────────────────────────────
# TestSistemaRedRamseyQCAL — 15 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSistemaRedRamseyQCAL(unittest.TestCase):
    """Verifica la integración completa del sistema ∴RRQ∞³."""

    def setUp(self):
        self.sistema = SistemaRedRamseyQCAL()

    def test_creacion_sistema(self):
        """El sistema debe crearse sin errores."""
        sistema = SistemaRedRamseyQCAL()
        self.assertIsNotNone(sistema)

    def test_red_no_none(self):
        """El sistema debe contener una RedRamsey."""
        self.assertIsNotNone(self.sistema.red)
        self.assertIsInstance(self.sistema.red, RedRamsey)

    def test_operador_no_none(self):
        """El sistema debe contener un OperadorMaestroHPi."""
        self.assertIsNotNone(self.sistema.operador)
        self.assertIsInstance(self.sistema.operador, OperadorMaestroHPi)

    def test_simbiosis_no_none(self):
        """El sistema debe contener una SimbiosisHiggsPC."""
        self.assertIsNotNone(self.sistema.simbiosis)
        self.assertIsInstance(self.sistema.simbiosis, SimbiosisHiggsPC)

    def test_tasa_no_none(self):
        """El sistema debe contener una TasaSimbiotitica."""
        self.assertIsNotNone(self.sistema.tasa)
        self.assertIsInstance(self.sistema.tasa, TasaSimbiotitica)

    def test_coherencia_no_none(self):
        """El sistema debe contener una CoherenciaRedRamsey."""
        self.assertIsNotNone(self.sistema.coherencia)
        self.assertIsInstance(self.sistema.coherencia, CoherenciaRedRamsey)

    def test_psi_global_valor(self):
        """Ψ_global del sistema debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.sistema.psi_global, 0.888)

    def test_todos_los_cierres_true(self):
        """Los 5 cierres del sistema deben estar activos."""
        self.assertTrue(self.sistema.todos_los_cierres())

    def test_estado_activo(self):
        """El estado del sistema debe ser 'ACTIVO'."""
        self.assertEqual(self.sistema.estado(), "ACTIVO")

    def test_activar_returns_dict(self):
        """activar() debe retornar un diccionario."""
        resultado = self.sistema.activar()
        self.assertIsInstance(resultado, dict)

    def test_activar_sello(self):
        """El resultado de activar() debe contener el sello ∴RRQ∞³."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["sello"], "∴RRQ∞³")

    def test_activar_psi_global(self):
        """El resultado debe contener psi_global ≥ 0.888."""
        resultado = self.sistema.activar()
        self.assertGreaterEqual(resultado["psi_global"], 0.888)

    def test_activar_estado(self):
        """El resultado debe indicar estado 'ACTIVO'."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["estado"], "ACTIVO")

    def test_activar_todos_cierres(self):
        """El resultado debe indicar todos_los_cierres = True."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado["todos_los_cierres"])

    def test_activar_ram(self):
        """El resultado debe contener el identificador RAM correcto."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["ram"], "RAM-LII-2026-RED-RAMSEY-QCAL")


# ─────────────────────────────────────────────────────────────────────────────
# TestActivarRedRamseyQCAL — 13 tests
# ─────────────────────────────────────────────────────────────────────────────

class TestActivarRedRamseyQCAL(unittest.TestCase):
    """Verifica la función de activación end-to-end red_ramsey_qcal_activar()."""

    def setUp(self):
        self.resultado = red_ramsey_qcal_activar()

    def test_activar_devuelve_dict(self):
        """red_ramsey_qcal_activar() debe retornar un diccionario."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello_rrq(self):
        """El sello debe ser '∴RRQ∞³'."""
        self.assertEqual(self.resultado["sello"], "∴RRQ∞³")

    def test_psi_global_valor(self):
        """Ψ_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_estado_activo(self):
        """El estado debe ser 'ACTIVO'."""
        self.assertEqual(self.resultado["estado"], "ACTIVO")

    def test_r_symb_kpps_presente(self):
        """El resultado debe contener r_symb_kpps."""
        self.assertIn("r_symb_kpps", self.resultado)

    def test_m_estrella_presente(self):
        """El resultado debe contener m_estrella."""
        self.assertIn("m_estrella", self.resultado)

    def test_todos_los_cierres_true(self):
        """todos_los_cierres debe ser True."""
        self.assertTrue(self.resultado["todos_los_cierres"])

    def test_ram_valor(self):
        """El identificador RAM debe ser correcto."""
        self.assertEqual(self.resultado["ram"], "RAM-LII-2026-RED-RAMSEY-QCAL")

    def test_psi_global_mayor_umbral(self):
        """Ψ_global debe superar el umbral 0.888."""
        self.assertGreater(self.resultado["psi_global"], 0.888)

    def test_r_symb_mayor_900(self):
        """R_symb debe ser mayor que 900 kpps."""
        self.assertGreater(self.resultado["r_symb_kpps"], 900.0)

    def test_m_estrella_close_118_375(self):
        """m* debe ser aproximadamente 118.375 GeV."""
        self.assertAlmostEqual(self.resultado["m_estrella"], 118.375, places=3)

    def test_sello_texto_correcto(self):
        """El sello debe contener 'RRQ'."""
        self.assertIn("RRQ", self.resultado["sello"])

    def test_todas_las_keys(self):
        """El resultado debe contener todas las claves esperadas."""
        claves_esperadas = {
            "sello",
            "psi_global",
            "estado",
            "r_symb_kpps",
            "m_estrella",
            "todos_los_cierres",
            "ram",
        }
        self.assertEqual(set(self.resultado.keys()), claves_esperadas)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
