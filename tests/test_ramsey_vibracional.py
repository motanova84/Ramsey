"""
Tests unitarios para el módulo de Ramsey Vibracional

Verifica funcionalidad básica sin ejecutar cálculos SAT costosos.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import numpy as np
from ramsey_vibracional import (
    resonancia_detectada,
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    estimar_conjetura
)

class TestResonancia(unittest.TestCase):
    """Tests para el operador de resonancia"""
    
    def test_resonancia_exacta(self):
        """Frecuencias idénticas deben resonar"""
        self.assertTrue(resonancia_detectada(10.0, 10.0, eps=0.001))
    
    def test_resonancia_cercana(self):
        """Frecuencias muy cercanas deben resonar"""
        self.assertTrue(resonancia_detectada(10.0, 10.0005, eps=0.001))
    
    def test_no_resonancia(self):
        """Frecuencias lejanas no deben resonar"""
        self.assertFalse(resonancia_detectada(10.0, 50.0, eps=0.001))
    
    def test_resonancia_modular(self):
        """Resonancia debe considerar módulo f0"""
        f0 = 141.7001
        # Frecuencias que difieren en ~f0 deben resonar
        self.assertTrue(resonancia_detectada(1.0, 1.0 + f0 - 0.0005, eps=0.001, f0=f0))


class TestColoracion(unittest.TestCase):
    """Tests para coloración vibracional"""
    
    def test_coloracion_basica(self):
        """Coloración debe producir diccionario de aristas"""
        frecuencias = [10.0, 10.5, 50.0]
        grafo = generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001)
        
        self.assertIsInstance(grafo, dict)
        self.assertEqual(len(grafo), 3)  # 3 vértices → 3 aristas
    
    def test_coloracion_simetria(self):
        """Coloración debe ser simétrica: (i,j) = (j,i)"""
        frecuencias = [10.0, 20.0, 30.0]
        grafo = generar_coloracion_vibracional(frecuencias, eps=0.001, f0=141.7001)
        
        # Todas las aristas deben tener (i < j)
        for (i, j) in grafo.keys():
            self.assertLess(i, j)
    
    def test_colores_validos(self):
        """Solo debe haber colores 'azul' o 'rojo'"""
        frecuencias = np.random.uniform(0, 141.7001, 5)
        grafo = generar_coloracion_vibracional(frecuencias)
        
        for color in grafo.values():
            self.assertIn(color, ['azul', 'rojo'])


class TestCliques(unittest.TestCase):
    """Tests para detección de cliques"""
    
    def test_clique_trivial(self):
        """Un vértice aislado es clique de tamaño 1"""
        grafo = {(0, 1): 'rojo', (0, 2): 'rojo', (1, 2): 'rojo'}
        clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
        
        self.assertGreaterEqual(len(clique_rojo), 1)
    
    def test_clique_completo(self):
        """Grafo completamente azul tiene clique de todos los vértices"""
        grafo = {(0, 1): 'azul', (0, 2): 'azul', (1, 2): 'azul'}
        clique_azul = encontrar_clique_maximo(grafo, 'azul')
        
        self.assertEqual(len(clique_azul), 3)
    
    def test_clique_vacio(self):
        """Sin aristas del color, clique máximo es 1"""
        grafo = {(0, 1): 'azul', (0, 2): 'azul', (1, 2): 'azul'}
        clique_rojo = encontrar_clique_maximo(grafo, 'rojo')
        
        self.assertEqual(len(clique_rojo), 1)


class TestConjetura(unittest.TestCase):
    """Tests para estimaciones teóricas"""
    
    def test_conjetura_positiva(self):
        """Conjetura debe dar valores positivos"""
        self.assertGreater(estimar_conjetura(3, 3), 0)
        self.assertGreater(estimar_conjetura(4, 4), 0)
        self.assertGreater(estimar_conjetura(5, 5), 0)
    
    def test_conjetura_creciente(self):
        """Conjetura debe crecer con r,s"""
        self.assertLess(estimar_conjetura(3, 3), estimar_conjetura(4, 4))
        self.assertLess(estimar_conjetura(4, 4), estimar_conjetura(5, 5))
    
    def test_conjetura_simetrica(self):
        """Conjetura debe ser simétrica: R_ψ(r,s) = R_ψ(s,r)"""
        self.assertEqual(estimar_conjetura(3, 4), estimar_conjetura(4, 3))
        self.assertEqual(estimar_conjetura(5, 7), estimar_conjetura(7, 5))
    
    def test_conjetura_valores_conocidos(self):
        """Conjetura debe estar cerca de valores conocidos"""
        # Valores aproximados esperados
        self.assertAlmostEqual(estimar_conjetura(3, 3), 5, delta=2)
        self.assertAlmostEqual(estimar_conjetura(4, 4), 10, delta=3)


class TestRedNeuronal(unittest.TestCase):
    """Tests para aplicación a redes neuronales"""
    
    def test_red_basica(self):
        """Red debe tener estructura válida"""
        from ramsey_vibracional import red_neuronal_ramsey
        
        conexiones, frecuencias = red_neuronal_ramsey(
            num_neuronas=10,
            target_clique_size=3
        )
        
        self.assertEqual(len(frecuencias), 10)
        self.assertIsInstance(conexiones, list)
    
    def test_frecuencias_rango(self):
        """Frecuencias deben estar en rango válido"""
        from ramsey_vibracional import red_neuronal_ramsey
        
        conexiones, frecuencias = red_neuronal_ramsey(
            num_neuronas=20,
            target_clique_size=4
        )
        
        for freq in frecuencias:
            self.assertGreaterEqual(freq, 0)
            self.assertLessEqual(freq, 141.7001)


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
