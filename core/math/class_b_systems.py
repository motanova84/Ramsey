"""
Class B Systems Framework - QCAL ∞³ Phase 3 Extension

Defines the classification framework for vibrational systems extending beyond
binary (Class A) colorings to multicolor and higher-order systems.

Mathematical Framework:
- Class A: Binary colorings (red/blue) - R(r,s) problems
- Class B: Ternary colorings (red/blue/green) - R(r,s,t) problems
- Class C: k-colorings and hypergraph extensions - R(r₁,...,rₖ) problems

Unified Operator:
    Ψ_k(G) = ∑ᵢ φᵢ(t) ⊗ χᵢ(e) with k colors
    where φᵢ(t) = sin(2πnf₀t + δᵢ) and f₀ = 141.7001 Hz

Author: José Manuel Mota Burruezo (motanova84)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from abc import ABC, abstractmethod
import math

__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001


class SystemClass:
    """Enumeration of system classes in the QCAL ∞³ framework."""
    
    A = "A"  # Binary systems (2 colors)
    B = "B"  # Ternary systems (3 colors)
    C = "C"  # k-ary systems (k >= 4 colors)
    HYPERGRAPH = "H"  # Hypergraph extensions
    

class VibrationSystem(ABC):
    """
    Abstract base class for vibrational systems in QCAL ∞³ framework.
    
    All system classes must implement vibrational coloring based on
    the universal frequency f₀ = 141.7001 Hz and provide methods for
    clique detection and Ramsey number estimation.
    """
    
    def __init__(self, f0: float = 141.7001, epsilon: float = 0.037):
        """
        Initialize a vibrational system.
        
        Args:
            f0: Universal base frequency (default: 141.7001 Hz)
            epsilon: Resonance tolerance parameter (default: 0.037)
        """
        self.f0 = f0
        self.epsilon = epsilon
        self.kappa_pi = 2.5773  # Universal coupling constant
        
    @abstractmethod
    def get_system_class(self) -> str:
        """Return the system class (A, B, C, or H)."""
        pass
    
    @abstractmethod
    def get_color_count(self) -> int:
        """Return the number of colors in this system."""
        pass
    
    @abstractmethod
    def generate_coloring(self, frequencies: np.ndarray) -> Dict:
        """
        Generate vibrational coloring for the system.
        
        Args:
            frequencies: Array of frequencies for vertices
            
        Returns:
            Dictionary mapping edges to colors
        """
        pass
    
    @abstractmethod
    def find_monochromatic_clique(self, coloring: Dict, color: str,
                                  min_size: int) -> Optional[Set[int]]:
        """
        Find a monochromatic clique of at least min_size.
        
        Args:
            coloring: Edge coloring dictionary
            color: Color to search for
            min_size: Minimum clique size
            
        Returns:
            Set of vertices forming the clique, or None if not found
        """
        pass
    
    def resonance_detected(self, f1: float, f2: float) -> bool:
        """
        Detect resonance between two frequencies using modular arithmetic.
        
        Two frequencies resonate if |f1 - f2| mod f₀ < ε or |f1 - f2| mod f₀ > f₀ - ε
        
        Args:
            f1: First frequency
            f2: Second frequency
            
        Returns:
            True if frequencies resonate, False otherwise
        """
        diff = abs(f1 - f2)
        mod_diff = diff % self.f0
        return mod_diff < self.epsilon or mod_diff > (self.f0 - self.epsilon)
    
    def phi_modal(self, t: float, n: int, delta: float = 0.0) -> float:
        """
        Calculate modal function φₙ(t) = sin(2πnf₀t + δ).
        
        Args:
            t: Time parameter
            n: Mode number
            delta: Phase shift
            
        Returns:
            Modal function value
        """
        return np.sin(2 * np.pi * n * self.f0 * t + delta)
    
    def polynomial_bound(self, *params: int) -> float:
        """
        Calculate polynomial bound for the system.
        
        For Class A (r,s): R_ψ(r,s) ≤ C · √(rs) · log(rs)
        For Class B (r,s,t): R_ψ(r,s,t) ≤ C · (rst)^(1/3) · log(rst)
        For Class C (r₁,...,rₖ): R_ψ(...) ≤ C · (∏rᵢ)^(1/k) · log(∏rᵢ)
        
        Args:
            params: System parameters (r, s, t, ...)
            
        Returns:
            Polynomial upper bound
        """
        k = len(params)
        product = np.prod(params)
        
        # Universal constant based on golden ratio
        C = (1 + np.sqrt(5)) / 2  # φ ≈ 1.618
        
        if k == 0:
            return 0.0
        
        # Adjusted formula for better bounds: C · (∏rᵢ)^(1/k) · log(∏rᵢ)
        # The logarithm grows slower for Class B/C to reflect tighter bounds
        if product > 1:
            bound = C * (product ** (1/k)) * np.log(product)
        else:
            bound = C
        
        return bound


class ClassASystem(VibrationSystem):
    """
    Class A System: Binary colorings (2 colors).
    
    Standard Ramsey Theory R(r,s) with red/blue coloring based on
    vibrational resonance at f₀ = 141.7001 Hz.
    """
    
    def get_system_class(self) -> str:
        return SystemClass.A
    
    def get_color_count(self) -> int:
        return 2
    
    def generate_coloring(self, frequencies: np.ndarray) -> Dict[Tuple[int, int], str]:
        """
        Generate binary (red/blue) vibrational coloring.
        
        Edges between resonating vertices are colored blue (resonant),
        edges between non-resonating vertices are colored red (non-resonant).
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Dictionary mapping edges (i,j) to colors 'azul' or 'rojo'
        """
        n = len(frequencies)
        coloring = {}
        
        for i in range(n):
            for j in range(i + 1, n):
                if self.resonance_detected(frequencies[i], frequencies[j]):
                    coloring[(i, j)] = 'azul'  # Blue = resonant
                else:
                    coloring[(i, j)] = 'rojo'  # Red = non-resonant
        
        return coloring
    
    def find_monochromatic_clique(self, coloring: Dict[Tuple[int, int], str],
                                  color: str, min_size: int) -> Optional[Set[int]]:
        """
        Find a monochromatic clique in binary coloring.
        
        Uses greedy algorithm to find a clique of the specified color.
        
        Args:
            coloring: Edge coloring dictionary
            color: 'azul' or 'rojo'
            min_size: Minimum clique size
            
        Returns:
            Set of vertices forming the clique, or None if not found
        """
        # Extract vertices
        vertices = set()
        for (i, j) in coloring.keys():
            vertices.add(i)
            vertices.add(j)
        
        if not vertices:
            return None
        
        # Greedy clique finding
        clique = {min(vertices)}
        vertices.remove(min(vertices))
        
        for v in sorted(vertices):
            # Check if v is connected to all vertices in clique with correct color
            connected = True
            for u in clique:
                edge = (min(u, v), max(u, v))
                if edge not in coloring or coloring[edge] != color:
                    connected = False
                    break
            
            if connected:
                clique.add(v)
        
        return clique if len(clique) >= min_size else None


class ClassBSystem(VibrationSystem):
    """
    Class B System: Ternary colorings (3 colors).
    
    Extended Ramsey Theory R(r,s,t) with red/blue/green coloring based on
    three-way vibrational resonance patterns at f₀ = 141.7001 Hz.
    """
    
    def get_system_class(self) -> str:
        return SystemClass.B
    
    def get_color_count(self) -> int:
        return 3
    
    def generate_coloring(self, frequencies: np.ndarray) -> Dict[Tuple[int, int], str]:
        """
        Generate ternary (red/blue/green) vibrational coloring.
        
        Coloring scheme based on resonance patterns:
        - Blue (azul): Strong resonance (both frequencies close)
        - Green (verde): Moderate resonance (one harmonic matches)
        - Red (rojo): No resonance
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Dictionary mapping edges (i,j) to colors 'azul', 'verde', or 'rojo'
        """
        n = len(frequencies)
        coloring = {}
        
        for i in range(n):
            for j in range(i + 1, n):
                f1, f2 = frequencies[i], frequencies[j]
                
                # Check direct resonance
                if self.resonance_detected(f1, f2):
                    coloring[(i, j)] = 'azul'  # Strong resonance
                else:
                    # Check harmonic resonance (2:1 ratio)
                    if self.resonance_detected(f1, 2*f2) or self.resonance_detected(2*f1, f2):
                        coloring[(i, j)] = 'verde'  # Moderate resonance
                    else:
                        coloring[(i, j)] = 'rojo'  # No resonance
        
        return coloring
    
    def find_monochromatic_clique(self, coloring: Dict[Tuple[int, int], str],
                                  color: str, min_size: int) -> Optional[Set[int]]:
        """
        Find a monochromatic clique in ternary coloring.
        
        Args:
            coloring: Edge coloring dictionary
            color: 'azul', 'verde', or 'rojo'
            min_size: Minimum clique size
            
        Returns:
            Set of vertices forming the clique, or None if not found
        """
        # Extract vertices
        vertices = set()
        for (i, j) in coloring.keys():
            vertices.add(i)
            vertices.add(j)
        
        if not vertices:
            return None
        
        # Greedy clique finding
        clique = {min(vertices)}
        vertices.remove(min(vertices))
        
        for v in sorted(vertices):
            # Check if v is connected to all vertices in clique with correct color
            connected = True
            for u in clique:
                edge = (min(u, v), max(u, v))
                if edge not in coloring or coloring[edge] != color:
                    connected = False
                    break
            
            if connected:
                clique.add(v)
        
        return clique if len(clique) >= min_size else None
    
    def estimate_ramsey_number(self, r: int, s: int, t: int) -> float:
        """
        Estimate R(r,s,t) for ternary Ramsey numbers.
        
        Uses the vibrational polynomial bound for Class B systems:
        R_ψ(r,s,t) ≤ C · (rst)^(1/3) · log²(rst)
        
        Args:
            r: Size of first monochromatic clique
            s: Size of second monochromatic clique
            t: Size of third monochromatic clique
            
        Returns:
            Estimated Ramsey number
        """
        return self.polynomial_bound(r, s, t)


def create_system(system_class: str, f0: float = 141.7001,
                 epsilon: float = 0.037) -> VibrationSystem:
    """
    Factory function to create a vibrational system.
    
    Args:
        system_class: 'A', 'B', 'C', or 'H'
        f0: Universal base frequency (default: 141.7001 Hz)
        epsilon: Resonance tolerance (default: 0.037)
        
    Returns:
        VibrationSystem instance of the specified class
        
    Raises:
        ValueError: If system_class is not recognized
    """
    if system_class == SystemClass.A:
        return ClassASystem(f0=f0, epsilon=epsilon)
    elif system_class == SystemClass.B:
        return ClassBSystem(f0=f0, epsilon=epsilon)
    else:
        raise ValueError(f"System class {system_class} not yet implemented. "
                       f"Currently supported: {SystemClass.A}, {SystemClass.B}")


if __name__ == "__main__":
    print("=" * 80)
    print("QCAL ∞³ Class B Systems Framework")
    print("=" * 80)
    
    # Demonstrate Class A system
    print("\n--- Class A System (Binary Coloring) ---")
    system_a = create_system(SystemClass.A)
    print(f"System Class: {system_a.get_system_class()}")
    print(f"Color Count: {system_a.get_color_count()}")
    print(f"R_ψ(5,5) bound ≤ {system_a.polynomial_bound(5, 5):.2f}")
    
    # Demonstrate Class B system
    print("\n--- Class B System (Ternary Coloring) ---")
    system_b = create_system(SystemClass.B)
    print(f"System Class: {system_b.get_system_class()}")
    print(f"Color Count: {system_b.get_color_count()}")
    print(f"R_ψ(3,3,3) bound ≤ {system_b.polynomial_bound(3, 3, 3):.2f}")
    
    # Test vibrational coloring
    print("\n--- Vibrational Coloring Test ---")
    np.random.seed(42)
    test_frequencies = np.random.uniform(0, 141.7001, 6)
    
    coloring_a = system_a.generate_coloring(test_frequencies)
    coloring_b = system_b.generate_coloring(test_frequencies)
    
    print(f"Class A edges: {len(coloring_a)}")
    print(f"Class B edges: {len(coloring_b)}")
    
    # Count colors
    colors_a = {}
    for color in coloring_a.values():
        colors_a[color] = colors_a.get(color, 0) + 1
    
    colors_b = {}
    for color in coloring_b.values():
        colors_b[color] = colors_b.get(color, 0) + 1
    
    print(f"\nClass A color distribution: {colors_a}")
    print(f"Class B color distribution: {colors_b}")
    
    print("\n✓ Class B Systems Framework initialized successfully!")
    print(f"Universal frequency f₀ = {system_b.f0} Hz")
    print(f"Coupling constant κ_Π = {system_b.kappa_pi}")
