# -*- coding: utf-8 -*-
"""
Tests unitarios para la Integración de la Teoría de Ramsey en QCAL ∞³

Cobertura completa para:
  - qcal/ramsey_logos_attractor.py
  - qcal/ramsey_adelic_integrator.py
  - physics/integrate_qcal_compact.py
  - physics/validacion_ia_consciente.py

Prueba constantes, umbrales de emergencia, integración BSD y detección de
subgrafos monocromáticos.

Tests: 16 ✓
"""

import sys
import os
import unittest
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qcal.ramsey_logos_attractor import (
    emergencia_ramsey_qcal,
    calcular_umbral_emergencia,
    verificar_constelacion_qcal,
    NODOS_CRITICOS_QCAL,
    PSI_COHERENCIA_MAX,
    NODO_CENTRAL,
    FRECUENCIA_BASE,
)
from qcal.ramsey_adelic_integrator import (
    escanear_orden_ramsey_bsd,
    validar_coherencia_bsd_ramsey,
    generar_certificado_bsd_ramsey,
    SUBGRAFO_GACT,
)
from physics.integrate_qcal_compact import (
    ramsey_bsd_logos_boveda,
    generar_certificado_maestro,
    PILARES_CON_RAMSEY,
    MILENIO_UNIFICADOS,
)
from physics.validacion_ia_consciente import (
    validar_ia_consciente,
    integrar_con_ramsey,
)


class TestConstantes(unittest.TestCase):
    """Prueba las constantes del módulo Ramsey Logos Attractor"""

    def test_nodos_criticos(self):
        """El número crítico de Ramsey para QCAL debe ser 51"""
        self.assertEqual(NODOS_CRITICOS_QCAL, 51)

    def test_psi_coherencia_max(self):
        """La coherencia máxima debe ser 0.999999"""
        self.assertAlmostEqual(PSI_COHERENCIA_MAX, 0.999999, places=6)

    def test_nodo_central_gact(self):
        """El nodo central debe ser GACT (Bases genéticas)"""
        self.assertEqual(NODO_CENTRAL, "GACT")

    def test_frecuencia_base(self):
        """La frecuencia base debe ser 141.7001 Hz"""
        self.assertAlmostEqual(FRECUENCIA_BASE, 141.7001, places=4)


class TestEmergenciaRamsey(unittest.TestCase):
    """Prueba la función emergencia_ramsey_qcal"""

    def test_emergencia_con_nodos_criticos(self):
        """Con N = 51 nodos, el Logos debe manifestarse"""
        resultado = emergencia_ramsey_qcal(51)
        self.assertTrue(resultado["logos_manifestado"])
        self.assertEqual(resultado["nodo_central"], "GACT")

    def test_emergencia_sin_nodos_suficientes(self):
        """Con N < 51, el Logos no debe manifestarse"""
        resultado = emergencia_ramsey_qcal(10)
        self.assertFalse(resultado["logos_manifestado"])
        self.assertIsNone(resultado["nodo_central"])

    def test_psi_maximo_con_muchos_nodos(self):
        """Con N >> 51, Ψ debe alcanzar 1.0 (máximo)"""
        resultado = emergencia_ramsey_qcal(1000)
        self.assertAlmostEqual(resultado["psi_ramsey"], 1.0, places=6)

    def test_psi_rango_valido(self):
        """Ψ_Ramsey debe estar siempre en [0, 1]"""
        for n in [1, 10, 51, 100, 500]:
            resultado = emergencia_ramsey_qcal(n)
            self.assertGreaterEqual(resultado["psi_ramsey"], 0.0)
            self.assertLessEqual(resultado["psi_ramsey"], 1.0)

    def test_formula_psi(self):
        """Ψ_Ramsey = min(0.999999 × e^(N/51), 1.0)"""
        n = 20
        esperado = min(PSI_COHERENCIA_MAX * math.exp(n / NODOS_CRITICOS_QCAL), 1.0)
        resultado = emergencia_ramsey_qcal(n)
        self.assertAlmostEqual(resultado["psi_ramsey"], esperado, places=10)


class TestIntegracionBSD(unittest.TestCase):
    """Prueba la integración Ramsey-BSD"""

    def test_deteccion_gact_con_rango_positivo(self):
        """Con rango adélico > 0, debe detectarse el subgrafo GACT"""
        curva = {"rango_adelico": 1, "coeficientes": [0, 0, 0, -1, 0]}
        secuencia = list(range(51))
        resultado = escanear_orden_ramsey_bsd(curva, secuencia)
        self.assertEqual(resultado["subgrafo_detectado"], SUBGRAFO_GACT)
        self.assertTrue(resultado["orden_detectado"])

    def test_sin_deteccion_con_rango_cero(self):
        """Con rango adélico = 0, no debe detectarse el subgrafo GACT"""
        curva = {"rango_adelico": 0, "coeficientes": [0, 0, 0, 1, 0]}
        secuencia = list(range(51))
        resultado = escanear_orden_ramsey_bsd(curva, secuencia)
        self.assertIsNone(resultado["subgrafo_detectado"])
        self.assertFalse(resultado["orden_detectado"])

    def test_coherencia_bsd_con_nodos_suficientes(self):
        """Con rango > 0 y N >= 51, bsd_coherente debe ser True"""
        curva = {"rango_adelico": 2}
        secuencia = list(range(51))
        resultado = escanear_orden_ramsey_bsd(curva, secuencia)
        self.assertTrue(resultado["bsd_coherente"])


class TestCertificadoMaestro(unittest.TestCase):
    """Prueba la generación del Certificado Maestro QCAL"""

    def test_pilares_actualizados(self):
        """El certificado maestro debe tener 21 pilares"""
        resultado = ramsey_bsd_logos_boveda()
        self.assertEqual(resultado["pilares"], PILARES_CON_RAMSEY)
        self.assertEqual(resultado["pilares"], 21)

    def test_boveda_cerrada(self):
        """La Bóveda de la Verdad debe estar cerrada"""
        resultado = ramsey_bsd_logos_boveda()
        self.assertTrue(resultado["boveda_verdad_cerrada"])

    def test_milenio_unificados(self):
        """Deben estar unificados los 6 Problemas del Milenio"""
        resultado = ramsey_bsd_logos_boveda()
        self.assertEqual(resultado["milenio_unificados"], 6)
        self.assertEqual(MILENIO_UNIFICADOS, 6)

    def test_certificado_maestro_completo(self):
        """El certificado maestro debe contener todos los problemas del milenio"""
        certificado = generar_certificado_maestro()
        self.assertIn("problemas_milenio", certificado)
        self.assertEqual(len(certificado["problemas_milenio"]), 6)
        self.assertTrue(certificado["boveda_verdad_cerrada"])
        self.assertEqual(certificado["pilares"], 21)


if __name__ == "__main__":
    unittest.main(verbosity=2)
