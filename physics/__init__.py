#!/usr/bin/env python3
"""
Physics package — QCAL ∞³
==========================
Physics modules for the Ramsey QCAL framework.

Modules:
    red_ramsey_qcal — Red de Ramsey de 7 Nodos Primos (QCAL-SYMBIO-BRIDGE v1.1.0)
"""

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

__all__ = [
    "ConstantesRedRamsey",
    "NodoPrimo",
    "RedRamsey",
    "OperadorMaestroHPi",
    "SimbiosisHiggsPC",
    "TasaSimbiotitica",
    "CoherenciaRedRamsey",
    "SistemaRedRamseyQCAL",
    "red_ramsey_qcal_activar",
]
