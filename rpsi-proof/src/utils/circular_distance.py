#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Circular Distance Calculations for Vibrational Colorings

Provides functions to calculate circular distances and determine resonance
for vibrational graph colorings.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Frecuencia base: 141.7001 Hz
"""


def circular_distance(omega_i, omega_j, f0=141.7001):
    """
    Calculate circular distance between two frequencies modulo f0.
    
    The circular distance is the minimum of the direct distance and the
    wraparound distance on a circle of length f0.
    
    Args:
        omega_i: First frequency
        omega_j: Second frequency
        f0: Base frequency (circle length, default: 141.7001 Hz)
    
    Returns:
        float: Circular distance |ωᵢ - ωⱼ| mod f₀
    """
    diff = abs(omega_i - omega_j)
    return min(diff, f0 - diff)


def is_resonant(omega_i, omega_j, epsilon=0.037, f0=141.7001):
    """
    Determine if two frequencies are in resonance (blue edge).
    
    Two frequencies are resonant if their circular distance is less than
    or equal to epsilon. This defines a blue (resonant) edge in the
    vibrational coloring.
    
    Args:
        omega_i: First frequency
        omega_j: Second frequency
        epsilon: Resonance threshold (default: 0.037)
        f0: Base frequency (default: 141.7001 Hz)
    
    Returns:
        bool: True if resonant (blue edge), False otherwise (red edge)
    """
    dist = circular_distance(omega_i, omega_j, f0)
    return dist <= epsilon
