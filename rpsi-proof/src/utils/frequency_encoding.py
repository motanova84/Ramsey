#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frequency Encoding Functions for Vibrational Ramsey Numbers

Provides functions to encode and decode frequency assignments to/from grid positions.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Frecuencia base: 141.7001 Hz
"""


def encode_frequency(omega, f0=141.7001, grid=128):
    """
    Encode a frequency ω to a grid position k.
    
    Args:
        omega: Frequency value in [0, f0)
        f0: Base frequency (default: 141.7001 Hz)
        grid: Grid resolution (default: 128)
    
    Returns:
        int: Grid position k ∈ [0, grid) where omega ≈ k * (f0/grid)
    """
    k = int(round((omega * grid) / f0))
    return k % grid


def decode_frequency(k, f0=141.7001, grid=128):
    """
    Decode a grid position k to a frequency ω.
    
    Args:
        k: Grid position k ∈ [0, grid)
        f0: Base frequency (default: 141.7001 Hz)
        grid: Grid resolution (default: 128)
    
    Returns:
        float: Frequency ω = k * (f0/grid)
    """
    return (k * f0) / grid
