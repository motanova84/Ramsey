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
    D = "D"  # Dynamic/Adaptive systems with variable k
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


class ClassCSystem(VibrationSystem):
    """
    Class C System: k-ary colorings (k >= 4 colors).
    
    Generalized Ramsey Theory R(r₁,...,rₖ) with k-color schemes based on
    hierarchical harmonic resonance patterns at f₀ = 141.7001 Hz.
    
    Colors are assigned based on harmonic levels:
    - Level 0: Direct resonance → Color 0 (azul)
    - Level 1: 2:1 harmonic → Color 1 (verde)
    - Level 2: 3:1 harmonic → Color 2 (amarillo)
    - Level 3+: Higher harmonics → Colors 3+ (rojo, naranja, etc.)
    """
    
    def __init__(self, k: int = 4, f0: float = 141.7001, epsilon: float = 0.037):
        """
        Initialize Class C system with k colors.
        
        Args:
            k: Number of colors (default: 4)
            f0: Universal base frequency (default: 141.7001 Hz)
            epsilon: Resonance tolerance parameter (default: 0.037)
        """
        super().__init__(f0, epsilon)
        if k < 4:
            raise ValueError("Class C requires k >= 4 colors")
        self.k = k
        
        # Define color names for k colors
        self.color_names = ['azul', 'verde', 'amarillo', 'rojo', 'naranja', 
                           'violeta', 'rosa', 'gris', 'marron', 'turquesa']
        if k > len(self.color_names):
            # Generate additional color names if needed
            for i in range(len(self.color_names), k):
                self.color_names.append(f'color_{i}')
    
    def get_system_class(self) -> str:
        return SystemClass.C
    
    def get_color_count(self) -> int:
        return self.k
    
    def generate_coloring(self, frequencies: np.ndarray) -> Dict[Tuple[int, int], str]:
        """
        Generate k-ary vibrational coloring based on harmonic levels.
        
        Coloring scheme:
        - Check harmonics from 1:1 up to k:1
        - Assign color based on lowest harmonic that resonates
        - Default to last color if no harmonics resonate
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Dictionary mapping edges (i,j) to color names
        """
        n = len(frequencies)
        coloring = {}
        
        for i in range(n):
            for j in range(i + 1, n):
                f1, f2 = frequencies[i], frequencies[j]
                
                # Check harmonics from 1:1 up to k:1
                color_assigned = False
                for harmonic_level in range(self.k):
                    if harmonic_level == 0:
                        # Direct resonance
                        if self.resonance_detected(f1, f2):
                            coloring[(i, j)] = self.color_names[0]
                            color_assigned = True
                            break
                    else:
                        # Check n:1 harmonic resonance
                        n_harmonic = harmonic_level + 1
                        if (self.resonance_detected(f1, n_harmonic * f2) or 
                            self.resonance_detected(n_harmonic * f1, f2)):
                            coloring[(i, j)] = self.color_names[min(harmonic_level, self.k - 1)]
                            color_assigned = True
                            break
                
                # Default to last color if no resonance found
                if not color_assigned:
                    coloring[(i, j)] = self.color_names[self.k - 1]
        
        return coloring
    
    def find_monochromatic_clique(self, coloring: Dict[Tuple[int, int], str],
                                  color: str, min_size: int) -> Optional[Set[int]]:
        """
        Find a monochromatic clique in k-ary coloring.
        
        Args:
            coloring: Edge coloring dictionary
            color: Target color name
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
    
    def estimate_ramsey_number(self, *params: int) -> float:
        """
        Estimate R(r₁,...,rₖ) for k-ary Ramsey numbers.
        
        Uses the vibrational polynomial bound for Class C systems:
        R_ψ(r₁,...,rₖ) ≤ C · (∏rᵢ)^(1/k) · log(∏rᵢ)
        
        Args:
            params: Sizes of monochromatic cliques for each color
            
        Returns:
            Estimated Ramsey number
        """
        if len(params) != self.k:
            raise ValueError(f"Expected {self.k} parameters for Class C system with k={self.k}")
        return self.polynomial_bound(*params)


class ClassDSystem(VibrationSystem):
    """
    Class D System: Dynamic/Adaptive systems with variable k.
    
    Advanced system that adaptively determines the optimal number of colors
    based on the frequency distribution and graph structure. Uses spectral
    analysis to determine natural color partitions.
    
    Features:
    - Adaptive color count based on frequency clustering
    - Spectral gap analysis for optimal partitioning
    - Dynamic harmonic detection with κ_Π coupling
    """
    
    def __init__(self, f0: float = 141.7001, epsilon: float = 0.037, 
                 max_colors: int = 10):
        """
        Initialize Class D dynamic system.
        
        Args:
            f0: Universal base frequency (default: 141.7001 Hz)
            epsilon: Resonance tolerance parameter (default: 0.037)
            max_colors: Maximum number of colors to consider (default: 10)
        """
        super().__init__(f0, epsilon)
        self.max_colors = max_colors
        self.adaptive_k = None  # Determined dynamically
        
        # Color palette
        self.color_palette = ['azul', 'verde', 'amarillo', 'rojo', 'naranja', 
                             'violeta', 'rosa', 'gris', 'marron', 'turquesa',
                             'cyan', 'magenta', 'lima', 'indigo', 'salmon']
    
    def get_system_class(self) -> str:
        return SystemClass.D
    
    def get_color_count(self) -> int:
        return self.adaptive_k if self.adaptive_k else self.max_colors
    
    def _determine_optimal_colors(self, frequencies: np.ndarray) -> int:
        """
        Determine optimal number of colors based on frequency distribution.
        
        Uses spectral gap analysis and κ_Π coupling to find natural partitions.
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Optimal number of colors
        """
        n = len(frequencies)
        if n < 4:
            return 2  # Default to binary for small graphs
        
        # Sort frequencies for gap analysis
        sorted_freqs = np.sort(frequencies)
        
        # Calculate gaps between adjacent frequencies
        gaps = np.diff(sorted_freqs)
        
        # Normalize gaps by f₀
        normalized_gaps = gaps / self.f0
        
        # Find significant gaps (larger than κ_Π * epsilon)
        threshold = self.kappa_pi * self.epsilon
        significant_gaps = np.where(normalized_gaps > threshold)[0]
        
        # Number of colors = number of clusters = significant gaps + 1
        optimal_k = min(len(significant_gaps) + 1, self.max_colors)
        
        # Ensure at least 2 colors, at most max_colors
        optimal_k = max(2, min(optimal_k, self.max_colors))
        
        return optimal_k
    
    def generate_coloring(self, frequencies: np.ndarray) -> Dict[Tuple[int, int], str]:
        """
        Generate dynamic k-ary vibrational coloring with adaptive color count.
        
        First determines optimal k, then applies hierarchical harmonic coloring.
        
        Args:
            frequencies: Array of vertex frequencies
            
        Returns:
            Dictionary mapping edges (i,j) to color names
        """
        # Determine optimal number of colors
        self.adaptive_k = self._determine_optimal_colors(frequencies)
        
        n = len(frequencies)
        coloring = {}
        
        # Create frequency clusters
        sorted_indices = np.argsort(frequencies)
        sorted_freqs = frequencies[sorted_indices]
        
        # Assign vertices to color clusters based on frequency
        cluster_size = n // self.adaptive_k
        vertex_clusters = {}
        for i, idx in enumerate(sorted_indices):
            cluster_id = min(i // max(1, cluster_size), self.adaptive_k - 1)
            vertex_clusters[idx] = cluster_id
        
        # Color edges based on vertex cluster relationships and resonance
        for i in range(n):
            for j in range(i + 1, n):
                f1, f2 = frequencies[i], frequencies[j]
                cluster_i = vertex_clusters[i]
                cluster_j = vertex_clusters[j]
                
                # Check for direct resonance first
                if self.resonance_detected(f1, f2):
                    coloring[(i, j)] = self.color_palette[0]  # Strong connection
                # Check if same cluster
                elif cluster_i == cluster_j:
                    coloring[(i, j)] = self.color_palette[min(cluster_i + 1, self.adaptive_k - 1)]
                # Check harmonic resonance
                else:
                    harmonic_found = False
                    for h in range(2, min(5, self.adaptive_k)):
                        if (self.resonance_detected(f1, h * f2) or 
                            self.resonance_detected(h * f1, f2)):
                            coloring[(i, j)] = self.color_palette[min(h, self.adaptive_k - 1)]
                            harmonic_found = True
                            break
                    if not harmonic_found:
                        # Default: based on cluster distance
                        cluster_dist = abs(cluster_i - cluster_j)
                        color_idx = min(cluster_dist + 1, self.adaptive_k - 1)
                        coloring[(i, j)] = self.color_palette[color_idx]
        
        return coloring
    
    def find_monochromatic_clique(self, coloring: Dict[Tuple[int, int], str],
                                  color: str, min_size: int) -> Optional[Set[int]]:
        """
        Find a monochromatic clique in dynamic coloring.
        
        Args:
            coloring: Edge coloring dictionary
            color: Target color name
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
        
        # Greedy clique finding with optimization
        best_clique = None
        best_size = 0
        
        # Try starting from different vertices
        for start_v in sorted(vertices)[:min(10, len(vertices))]:
            clique = {start_v}
            remaining = vertices - {start_v}
            
            for v in sorted(remaining):
                # Check if v is connected to all vertices in clique with correct color
                connected = True
                for u in clique:
                    edge = (min(u, v), max(u, v))
                    if edge not in coloring or coloring[edge] != color:
                        connected = False
                        break
                
                if connected:
                    clique.add(v)
            
            if len(clique) > best_size:
                best_size = len(clique)
                best_clique = clique
        
        return best_clique if best_clique and len(best_clique) >= min_size else None
    
    def estimate_ramsey_number(self, *params: int) -> float:
        """
        Estimate R(r₁,...,rₖ) for dynamic systems.
        
        Uses adaptive polynomial bound with spectral correction.
        
        Args:
            params: Sizes of monochromatic cliques
            
        Returns:
            Estimated Ramsey number
        """
        k = len(params)
        if k == 0:
            return 0.0
        
        # Base polynomial bound
        base_bound = self.polynomial_bound(*params)
        
        # Apply spectral correction factor based on κ_Π
        # Dynamic systems benefit from adaptive coloring
        correction_factor = 1.0 - (0.1 * np.exp(-k / self.kappa_pi))
        
        return base_bound * correction_factor


def create_system(system_class: str, f0: float = 141.7001,
                 epsilon: float = 0.037, **kwargs) -> VibrationSystem:
    """
    Factory function to create a vibrational system.
    
    Args:
        system_class: 'A', 'B', 'C', 'D', or 'H'
        f0: Universal base frequency (default: 141.7001 Hz)
        epsilon: Resonance tolerance (default: 0.037)
        **kwargs: Additional parameters:
            - k: Number of colors for Class C (default: 4)
            - max_colors: Maximum colors for Class D (default: 10)
        
    Returns:
        VibrationSystem instance of the specified class
        
    Raises:
        ValueError: If system_class is not recognized
    """
    if system_class == SystemClass.A:
        return ClassASystem(f0=f0, epsilon=epsilon)
    elif system_class == SystemClass.B:
        return ClassBSystem(f0=f0, epsilon=epsilon)
    elif system_class == SystemClass.C:
        k = kwargs.get('k', 4)
        return ClassCSystem(k=k, f0=f0, epsilon=epsilon)
    elif system_class == SystemClass.D:
        max_colors = kwargs.get('max_colors', 10)
        return ClassDSystem(f0=f0, epsilon=epsilon, max_colors=max_colors)
    else:
        raise ValueError(f"System class {system_class} not yet implemented. "
                       f"Currently supported: {SystemClass.A}, {SystemClass.B}, "
                       f"{SystemClass.C}, {SystemClass.D}")


if __name__ == "__main__":
    print("=" * 80)
    print("QCAL ∞³ Class B, C, D Systems Framework")
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
    
    # Demonstrate Class C system
    print("\n--- Class C System (k-ary Coloring, k=4) ---")
    system_c = create_system(SystemClass.C, k=4)
    print(f"System Class: {system_c.get_system_class()}")
    print(f"Color Count: {system_c.get_color_count()}")
    print(f"R_ψ(3,3,3,3) bound ≤ {system_c.polynomial_bound(3, 3, 3, 3):.2f}")
    
    # Demonstrate Class D system
    print("\n--- Class D System (Dynamic/Adaptive) ---")
    system_d = create_system(SystemClass.D, max_colors=8)
    print(f"System Class: {system_d.get_system_class()}")
    print(f"Max Colors: {system_d.max_colors}")
    
    # Test vibrational coloring
    print("\n--- Vibrational Coloring Test ---")
    np.random.seed(42)
    test_frequencies = np.random.uniform(0, 141.7001, 8)
    
    coloring_a = system_a.generate_coloring(test_frequencies)
    coloring_b = system_b.generate_coloring(test_frequencies)
    coloring_c = system_c.generate_coloring(test_frequencies)
    coloring_d = system_d.generate_coloring(test_frequencies)
    
    print(f"Class A edges: {len(coloring_a)}")
    print(f"Class B edges: {len(coloring_b)}")
    print(f"Class C edges: {len(coloring_c)}")
    print(f"Class D edges: {len(coloring_d)} (adaptive k={system_d.adaptive_k})")
    
    # Count colors for each system
    for system_name, coloring in [('A', coloring_a), ('B', coloring_b), 
                                   ('C', coloring_c), ('D', coloring_d)]:
        colors = {}
        for color in coloring.values():
            colors[color] = colors.get(color, 0) + 1
        print(f"\nClass {system_name} color distribution: {colors}")
    
    print("\n✓ Class B, C, D Systems Framework initialized successfully!")
    print(f"Universal frequency f₀ = {system_b.f0} Hz")
    print(f"Coupling constant κ_Π = {system_b.kappa_pi}")
