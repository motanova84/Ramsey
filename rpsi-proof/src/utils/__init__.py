#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for Vibrational Ramsey Number Encoding

This module provides utility functions for encoding vibrational colorings,
including circular distance calculations and modular arithmetic for frequency
assignments.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Instituto: Instituto de Consciencia Cuántica (ICQ)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

from .frequency_encoding import encode_frequency, decode_frequency
from .circular_distance import circular_distance, is_resonant
from .modular_arithmetic import mod_f0, frequency_to_grid

__all__ = [
    'encode_frequency',
    'decode_frequency',
    'circular_distance',
    'is_resonant',
    'mod_f0',
    'frequency_to_grid'
]
