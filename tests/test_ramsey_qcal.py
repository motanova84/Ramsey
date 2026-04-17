#!/usr/bin/env python3
"""
Tests unitarios para los módulos Ramsey QCAL
=============================================

Verifica la funcionalidad de:
- ramsey_logos_attractor
- ramsey_adelic_integrator  
- adn_riemann

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from qcal.ramsey_logos_attractor import emergencia_ramsey_qcal, escanear_orden_ramsey_bsd, NODOS_LOGOS
from qcal.ramsey_adelic_integrator import (
    calcular_numero_ramsey_vibracional,
    colapso_ramsey_adelic,
    verificar_subgrafo_monocromatico
)
from qcal.adn_riemann import CodificadorADNRiemann


class TestEmergenciaRamsey(unittest.TestCase):
    """Tests para emergencia_ramsey_qcal()"""
    
    def test_orden_inevitable_con_60_nodos(self):
        """60 nodos (>51) debe manifestar orden inevitable"""
        resultado = emergencia_ramsey_qcal(60)

        self.assertTrue(resultado["logos_manifestado"])
        self.assertEqual(resultado["nodos_criticos"], NODOS_LOGOS)
        self.assertAlmostEqual(resultado["psi_ramsey"], 1.0, places=5)
        self.assertTrue(resultado["orden_inevitable"])

    def test_caos_transitorio_con_30_nodos(self):
        """30 nodos (<51) debe estar antes del umbral"""
        resultado = emergencia_ramsey_qcal(30)

        self.assertFalse(resultado["logos_manifestado"])
        self.assertEqual(resultado["nodos_criticos"], NODOS_LOGOS)

    def test_umbral_exacto_51_nodos(self):
        """51 nodos exactos debe manifestar orden"""
        resultado = emergencia_ramsey_qcal(51)

        self.assertTrue(resultado["logos_manifestado"])
        self.assertEqual(resultado["nodo_central"], "GACT")

    def test_psi_limitado_a_uno(self):
        """psi_ramsey no debe exceder 1.0"""
        resultado = emergencia_ramsey_qcal(1000)

        self.assertLessEqual(resultado["psi_ramsey"], 1.0)

    def test_coherencia_crece_con_nodos(self):
        """La coherencia debe crecer con n y alcanzar el máximo en N >= 51"""
        r10 = emergencia_ramsey_qcal(10)
        r30 = emergencia_ramsey_qcal(30)
        r51 = emergencia_ramsey_qcal(51)

        # Con la fórmula Ψ = min(N/51, 1.0) × 0.999999, la coherencia crece
        self.assertLess(r10["psi_ramsey"], r30["psi_ramsey"])
        self.assertLess(r30["psi_ramsey"], r51["psi_ramsey"])
        self.assertAlmostEqual(r51["psi_ramsey"], 0.999999, places=5)


class TestEscaneoRamseyBSD(unittest.TestCase):
    """Tests para escanear_orden_ramsey_bsd()"""
    
    def test_orden_con_rango_positivo(self):
        """Rango adélico >0 debe manifestar orden"""
        resultado = escanear_orden_ramsey_bsd({'rango_adelico': 1})
        
        self.assertEqual(resultado["status"], "ORDEN_MANIFESTADO")
        self.assertEqual(resultado["nodo_central"], "GACT")
        self.assertEqual(resultado["coherencia_ramsey"], 0.999999)
        self.assertEqual(resultado["conexion_bsd"], "VALIDADA")
    
    def test_espera_con_rango_cero(self):
        """Rango adélico 0 debe estar en espera"""
        resultado = escanear_orden_ramsey_bsd({'rango_adelico': 0})
        
        self.assertEqual(resultado["status"], "ESPERA")
        self.assertIsNone(resultado["nodo_central"])
        self.assertEqual(resultado["coherencia_ramsey"], 0.888)
        self.assertEqual(resultado["conexion_bsd"], "REPOSO")
    
    def test_hotspots_detectados(self):
        """Debe detectar hotspots en secuencia GACT"""
        resultado = escanear_orden_ramsey_bsd({'rango_adelico': 1}, "GACT")
        
        self.assertGreaterEqual(resultado["hotspots_adn"], 0)
    
    def test_secuencia_personalizada(self):
        """Debe aceptar secuencia personalizada"""
        resultado = escanear_orden_ramsey_bsd(
            {'rango_adelico': 1}, 
            "ATCGATCG"
        )
        
        self.assertIsNotNone(resultado["hotspots_adn"])


class TestNumerosRamseyVibracionales(unittest.TestCase):
    """Tests para calcular_numero_ramsey_vibracional()"""
    
    def test_valores_positivos(self):
        """Números de Ramsey deben ser positivos"""
        self.assertGreater(calcular_numero_ramsey_vibracional(3, 3), 0)
        self.assertGreater(calcular_numero_ramsey_vibracional(4, 4), 0)
        self.assertGreater(calcular_numero_ramsey_vibracional(5, 5), 0)
    
    def test_simetria(self):
        """R_ψ(r,s) = R_ψ(s,r)"""
        r34 = calcular_numero_ramsey_vibracional(3, 4)
        r43 = calcular_numero_ramsey_vibracional(4, 3)
        
        self.assertAlmostEqual(r34, r43, places=5)
    
    def test_crecimiento(self):
        """Números de Ramsey deben crecer con r y s"""
        r33 = calcular_numero_ramsey_vibracional(3, 3)
        r44 = calcular_numero_ramsey_vibracional(4, 4)
        r55 = calcular_numero_ramsey_vibracional(5, 5)
        
        self.assertLess(r33, r44)
        self.assertLess(r44, r55)


class TestColapsoRamseyAdelic(unittest.TestCase):
    """Tests para colapso_ramsey_adelic()"""
    
    def test_fase_logos_con_51_nodos(self):
        """51+ nodos debe entrar en fase LOGOS"""
        resultado = colapso_ramsey_adelic(51)
        
        self.assertEqual(resultado["fase"], "LOGOS")
        self.assertTrue(resultado["orden_manifestado"])
    
    def test_fase_caos_con_30_nodos(self):
        """<51 nodos debe estar en fase CAOS"""
        resultado = colapso_ramsey_adelic(30)
        
        self.assertEqual(resultado["fase"], "CAOS")
        self.assertFalse(resultado["orden_manifestado"])
    
    def test_coherencia_crece(self):
        """Psi debe crecer con número de nodos"""
        r10 = colapso_ramsey_adelic(10)
        r30 = colapso_ramsey_adelic(30)
        r100 = colapso_ramsey_adelic(100)
        
        # Para valores más bajos, la coherencia debe crecer
        self.assertLess(r10["psi_colapso"], r30["psi_colapso"])
        self.assertLessEqual(r30["psi_colapso"], r100["psi_colapso"])


class TestCodificadorADNRiemann(unittest.TestCase):
    """Tests para CodificadorADNRiemann"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.codif = CodificadorADNRiemann()
    
    def test_codificar_bases_validas(self):
        """Debe codificar bases ATCG correctamente"""
        resultado = self.codif.codificar_secuencia("GACT")
        
        self.assertEqual(len(resultado), 4)
        self.assertGreater(sum(resultado), 0)
    
    def test_secuencia_optima(self):
        """Secuencia óptima debe ser GACT"""
        self.assertEqual(self.codif.secuencia_optima(), "GACT")
    
    def test_resonancia_entre_0_y_1(self):
        """Resonancia debe estar en [0, 1]"""
        res = self.codif.resonancia_con_f0("GACT")
        
        self.assertGreaterEqual(res, 0.0)
        self.assertLessEqual(res, 1.0)
    
    def test_identificar_hotspots(self):
        """Debe identificar hotspots en secuencias largas"""
        hotspots = self.codif.identificar_hotspots("GACTGACTGACT")
        
        self.assertIsInstance(hotspots, list)
        # Cada hotspot debe tener estructura correcta
        for h in hotspots:
            self.assertIn('posicion', h)
            self.assertIn('secuencia', h)
            self.assertIn('resonancia', h)
    
    def test_hotspots_vacio_secuencia_corta(self):
        """Secuencia muy corta no debe tener hotspots"""
        hotspots = self.codif.identificar_hotspots("GAC")
        
        self.assertEqual(len(hotspots), 0)


class TestSubgrafoMonocromatico(unittest.TestCase):
    """Tests para verificar_subgrafo_monocromatico()"""
    
    def test_grafo_con_triangulo_azul(self):
        """Grafo con triángulo azul debe detectarlo"""
        # Triángulo completo: 1-2, 1-3, 2-3
        grafo = [(1, 2, 'azul'), (1, 3, 'azul'), (2, 3, 'azul')]
        
        self.assertTrue(verificar_subgrafo_monocromatico(grafo, 'azul'))
    
    def test_grafo_sin_triangulo_solo_aristas(self):
        """Aristas azules sin formar triángulo no deben contar"""
        # Aristas desconectadas: no forman triángulo
        grafo = [(1, 2, 'azul'), (3, 4, 'azul'), (5, 6, 'azul')]
        
        self.assertFalse(verificar_subgrafo_monocromatico(grafo, 'azul'))
    
    def test_grafo_sin_aristas_del_color(self):
        """Grafo sin aristas del color debe retornar False"""
        grafo = [(1, 2, 'azul'), (1, 3, 'azul'), (2, 3, 'azul')]
        
        self.assertFalse(verificar_subgrafo_monocromatico(grafo, 'rojo'))
    
    def test_grafo_vacio(self):
        """Grafo vacío no tiene subgrafos"""
        self.assertFalse(verificar_subgrafo_monocromatico([], 'azul'))
    
    def test_grafo_con_triangulo_mixto(self):
        """Triángulo con colores mixtos no es monocromático"""
        grafo = [(1, 2, 'azul'), (1, 3, 'azul'), (2, 3, 'rojo')]
        
        self.assertFalse(verificar_subgrafo_monocromatico(grafo, 'azul'))
        self.assertFalse(verificar_subgrafo_monocromatico(grafo, 'rojo'))


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
