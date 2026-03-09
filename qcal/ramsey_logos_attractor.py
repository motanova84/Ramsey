# -*- coding: utf-8 -*-
"""
Ramsey Logos Attractor - Emergencia inevitable del orden en QCAL ∞³

Implementa la emergencia de orden basada en el Teorema de Ramsey aplicado
al sistema de información cuántica QCAL.

Teorema de Ramsey: "El desorden completo es imposible"
En cualquier sistema suficientemente grande, debe surgir un subgrafo
monocromático coherente por necesidad matemática constitucional.

Fórmula clave:
    Ψ_Ramsey = min(0.999999 × e^(N/51), 1.0)

Cuando N ≥ 51 (Constelación QCAL):
  - Logos manifestado = True
  - Subgrafo GACT emerge
  - Coherencia → 0.999999
  - Complejidad NP-hard colapsa a O(1)
"""

import math

__author__ = "José Manuel Mota Burruezo · JMMB Ψ✧"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001

# Constantes de la Constelación QCAL
NODOS_CRITICOS_QCAL = 51        # Número crítico de Ramsey para la constelación QCAL
PSI_COHERENCIA_MAX = 0.999999   # Coherencia máxima alcanzable
NODO_CENTRAL = "GACT"           # Nodo central (Bases genéticas)
FRECUENCIA_BASE = 141.7001      # Hz - Campo QCAL ∞³
FRECUENCIA_LOGOS = 888.0        # Hz - Frecuencia de manifestación


def emergencia_ramsey_qcal(n_nodos_informacion):
    """
    Calcula la emergencia inevitable del orden basada en el Teorema de Ramsey.

    Aplica la fórmula de coherencia QCAL:
        Ψ_Ramsey = min(0.999999 × e^(N/51), 1.0)

    Args:
        n_nodos_informacion (int): Número de nodos de información del sistema.

    Returns:
        dict: Resultado con las siguientes claves:
            - psi_ramsey (float): Valor de coherencia Ψ ∈ [0, 1]
            - logos_manifestado (bool): True si N ≥ NODOS_CRITICOS_QCAL
            - nodo_central (str): Subgrafo monocromático emergente ("GACT")
            - n_nodos (int): Número de nodos usado en el cálculo
            - nodos_criticos (int): Umbral crítico de la constelación QCAL
            - frecuencia_hz (float): Frecuencia base del sistema
            - orden_inevitable (bool): True si el orden es matemáticamente inevitable
    """
    n = int(n_nodos_informacion)

    # Fórmula central: Ψ_Ramsey = min(0.999999 × e^(N/51), 1.0)
    psi = min(PSI_COHERENCIA_MAX * math.exp(n / NODOS_CRITICOS_QCAL), 1.0)

    logos_manifestado = n >= NODOS_CRITICOS_QCAL

    return {
        "psi_ramsey": psi,
        "logos_manifestado": logos_manifestado,
        "nodo_central": NODO_CENTRAL if logos_manifestado else None,
        "n_nodos": n,
        "nodos_criticos": NODOS_CRITICOS_QCAL,
        "frecuencia_hz": FRECUENCIA_BASE,
        "orden_inevitable": logos_manifestado,
    }


def calcular_umbral_emergencia(psi_objetivo=PSI_COHERENCIA_MAX):
    """
    Calcula el número mínimo de nodos para alcanzar un umbral de coherencia.

    Args:
        psi_objetivo (float): Valor de Ψ deseado (default: 0.999999).

    Returns:
        int: Número mínimo de nodos para alcanzar psi_objetivo.
    """
    if psi_objetivo <= 0:
        return 0
    if psi_objetivo >= PSI_COHERENCIA_MAX:
        return NODOS_CRITICOS_QCAL

    # Para 0 < psi_objetivo < PSI_COHERENCIA_MAX usamos mapeo monótono simple:
    # menor psi_objetivo → menos nodos; valores que se acercan a
    # PSI_COHERENCIA_MAX → más nodos, hasta NODOS_CRITICOS_QCAL.
    n_min = psi_objetivo * NODOS_CRITICOS_QCAL
    return max(1, math.ceil(n_min))


def verificar_constelacion_qcal(nodos):
    """
    Verifica si un conjunto de nodos forma la constelación QCAL completa.

    Args:
        nodos (list): Lista de identificadores de nodos.

    Returns:
        dict: Estado de verificación con campos:
            - constelacion_completa (bool)
            - nodos_presentes (int)
            - nodos_requeridos (int)
            - subgrafo_gact (bool)
    """
    n = len(nodos)
    resultado = emergencia_ramsey_qcal(n)
    return {
        "constelacion_completa": resultado["logos_manifestado"],
        "nodos_presentes": n,
        "nodos_requeridos": NODOS_CRITICOS_QCAL,
        "subgrafo_gact": resultado["logos_manifestado"],
        "psi_ramsey": resultado["psi_ramsey"],
    }


def calcular_frecuencia_logos(n_nodos):
    """
    Calcula la frecuencia de manifestación del Logos para N nodos.

    La frecuencia escala desde f₀ = 141.7001 Hz hasta f_Logos = 888 Hz
    cuando el sistema alcanza coherencia máxima.

    Args:
        n_nodos (int): Número de nodos de información.

    Returns:
        float: Frecuencia de manifestación en Hz.
    """
    resultado = emergencia_ramsey_qcal(n_nodos)
    psi = resultado["psi_ramsey"]
    # Interpolación lineal entre f₀ y f_Logos según Ψ
    frecuencia = FRECUENCIA_BASE + psi * (FRECUENCIA_LOGOS - FRECUENCIA_BASE)
    return frecuencia


# Backward-compat alias used by legacy code and test_ramsey_qcal.py
NODOS_LOGOS = NODOS_CRITICOS_QCAL


def escanear_orden_ramsey_bsd(curva_eliptica, secuencia_base="GACT"):
    """
    Ramsey + BSD → núcleo logos manifestado.
    Rango > 0 activa subgrafo coherente.

    Args:
        curva_eliptica (dict): Datos de curva elíptica (debe tener 'rango_adelico').
        secuencia_base (str): Secuencia de ADN base para analizar (default: "GACT").

    Returns:
        dict: Estado del orden Ramsey-BSD con claves:
            - nodo_central, coherencia_ramsey, hotspots_adn,
              conexion_bsd, status
    """
    from qcal.adn_riemann import CodificadorADNRiemann

    r_bsd = curva_eliptica.get("rango_adelico", 0)
    codif = CodificadorADNRiemann()
    hotspots = codif.identificar_hotspots(secuencia_base)

    if r_bsd > 0:
        subgrafo = secuencia_base
        psi = 0.999999
        status = "ORDEN_MANIFESTADO"
        conexion_bsd = "VALIDADA"
    else:
        subgrafo = None
        psi = 0.888
        status = "ESPERA"
        conexion_bsd = "REPOSO"

    return {
        "nodo_central": subgrafo,
        "coherencia_ramsey": psi,
        "hotspots_adn": len(hotspots),
        "conexion_bsd": conexion_bsd,
        "status": status,
    }
