#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modular Arithmetic Functions for Frequency Calculations

Provides modular arithmetic operations for frequency assignments
in vibrational Ramsey number problems.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Frecuencia base: 141.7001 Hz
"""


def mod_f0(value, f0=141.7001):
    """
    Compute value modulo f0, normalized to [0, f0).
    
    Args:
        value: Input value
        f0: Base frequency (default: 141.7001 Hz)
    
    Returns:
        float: value mod f0, normalized to [0, f0)
    """
    return value % f0


def frequency_to_grid(omega, f0=141.7001, grid=128):
    """
    Convert frequency to grid index with modular wraparound.
    
    Args:
        omega: Frequency value
        f0: Base frequency (default: 141.7001 Hz)
        grid: Grid resolution (default: 128)
    
    Returns:
        int: Grid index k ∈ [0, grid)
    """
    normalized = mod_f0(omega, f0)
    k = int(round((normalized * grid) / f0))
    return k % grid
