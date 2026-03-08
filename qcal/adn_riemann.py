#!/usr/bin/env python3
"""
ADN-Riemann Module
==================

Codificador de ADN con resonancia Riemann para el framework QCAL ∞³.
Conecta la biología cuántica (ADN) con la estructura espectral de Riemann.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import math
from typing import Dict, List

__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001

F0 = 141.7001  # Frecuencia fundamental del Logos (Hz)


class CodificadorADNRiemann:
    """
    Codificador de secuencias de ADN con resonancia Riemann.
    
    Mapea bases nitrogenadas a frecuencias vibracionales y detecta
    hotspots de resonancia con f₀.
    """
    
    # Mapeo de bases a frecuencias características (Hz normalizadas)
    BASES_FRECUENCIAS = {
        'A': 1.0,   # Adenina
        'T': 2.0,   # Timina
        'C': 3.0,   # Citosina
        'G': 4.0,   # Guanina
    }
    
    def __init__(self, f0: float = F0):
        """
        Inicializa el codificador.
        
        Args:
            f0: Frecuencia fundamental del Logos (Hz)
        """
        self.f0 = f0
    
    def codificar_secuencia(self, secuencia: str) -> List[float]:
        """
        Codifica una secuencia de ADN a frecuencias.
        
        Args:
            secuencia: Secuencia de bases (e.g., "GACT")
            
        Returns:
            Lista de frecuencias correspondientes
        """
        return [self.BASES_FRECUENCIAS.get(base.upper(), 0.0) for base in secuencia]
    
    def resonancia_con_f0(self, secuencia: str) -> float:
        """
        Calcula la resonancia de una secuencia con f₀.
        
        Args:
            secuencia: Secuencia de ADN
            
        Returns:
            Coeficiente de resonancia [0, 1]
        """
        if not secuencia:
            return 0.0
        
        frecuencias = self.codificar_secuencia(secuencia)
        
        # Calcular coherencia con f₀
        suma_coherencia = sum(math.cos(2 * math.pi * freq / self.f0) for freq in frecuencias)
        resonancia = abs(suma_coherencia) / len(frecuencias)
        
        return min(resonancia, 1.0)
    
    def identificar_hotspots(self, secuencia: str, umbral: float = 0.8) -> List[Dict]:
        """
        Identifica hotspots de resonancia en la secuencia.
        
        Args:
            secuencia: Secuencia de ADN
            umbral: Umbral de resonancia para considerar hotspot
            
        Returns:
            Lista de hotspots detectados con sus posiciones
        """
        hotspots = []
        
        # Analizar ventanas deslizantes de longitud 4
        window_size = 4
        for i in range(len(secuencia) - window_size + 1):
            ventana = secuencia[i:i+window_size]
            resonancia = self.resonancia_con_f0(ventana)
            
            if resonancia >= umbral:
                hotspots.append({
                    'posicion': i,
                    'secuencia': ventana,
                    'resonancia': resonancia
                })
        
        return hotspots
    
    def secuencia_optima(self) -> str:
        """
        Retorna la secuencia de máxima resonancia conocida.
        
        Returns:
            Secuencia óptima (GACT en este caso)
        """
        return "GACT"
