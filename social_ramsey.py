#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Network Community Detection using Ramsey Vibrational Theory
QCAL ∞³ Framework

This module applies vibrational Ramsey theory to detect communities
in social networks based on resonance patterns.

Communities emerge as resonant cliques where members share similar
"frequency signatures" representing their interaction patterns.

Author: José Manuel Mota Burruezo
Frequency: 141.7001 Hz - Campo QCAL ∞³
"""

import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict
from ramsey_vibracional import (
    generar_coloracion_vibracional,
    encontrar_clique_maximo,
    resonancia_detectada
)


class CommunityDetector:
    """
    Community detection in social networks using Ramsey vibrational theory.
    
    Each node (person) is assigned a "social frequency" based on their
    interaction patterns. Communities emerge as groups with resonant frequencies.
    
    Parameters:
        network: Dictionary representing the social network graph
                 Format: {(node1, node2): weight, ...}
        resonance_threshold: Threshold for resonance detection (default: 0.01)
        f0: Base frequency for normalization (default: 141.7001 Hz)
    """
    
    def __init__(
        self,
        network: Optional[Dict[Tuple[int, int], float]] = None,
        resonance_threshold: float = 0.01,
        f0: float = 141.7001
    ):
        self.network = network or {}
        self.threshold = resonance_threshold
        self.f0 = f0
        self.nodes = self._extract_nodes()
        self.frequencies = {}
        self.resonant_graph = {}
        
    def _extract_nodes(self) -> Set[int]:
        """Extract all unique nodes from the network."""
        nodes = set()
        for (u, v) in self.network.keys():
            nodes.add(u)
            nodes.add(v)
        return nodes
    
    def compute_social_frequencies(self, method: str = 'degree') -> Dict[int, float]:
        """
        Compute social frequency for each node.
        
        The frequency represents a node's interaction pattern:
        - High frequency: Very active, many connections
        - Low frequency: Less active, fewer connections
        
        Args:
            method: Method to compute frequency ('degree', 'centrality', or 'activity')
            
        Returns:
            Dictionary mapping node_id -> frequency
        """
        if method == 'degree':
            # Frequency based on node degree
            degree = defaultdict(int)
            for (u, v) in self.network.keys():
                degree[u] += 1
                degree[v] += 1
            
            max_degree = max(degree.values()) if degree else 1
            for node in self.nodes:
                # Normalize to [0, f0] range
                self.frequencies[node] = (degree[node] / max_degree) * self.f0
                
        elif method == 'centrality':
            # Frequency based on betweenness centrality (simplified)
            # For full implementation, would need shortest paths computation
            # Here we use a proxy based on weighted connections
            centrality = defaultdict(float)
            for (u, v), weight in self.network.items():
                centrality[u] += weight
                centrality[v] += weight
            
            max_centrality = max(centrality.values()) if centrality else 1
            for node in self.nodes:
                self.frequencies[node] = (centrality[node] / max_centrality) * self.f0
                
        elif method == 'activity':
            # Frequency based on interaction strength
            activity = defaultdict(float)
            for (u, v), weight in self.network.items():
                activity[u] += weight
                activity[v] += weight
            
            max_activity = max(activity.values()) if activity else 1
            for node in self.nodes:
                self.frequencies[node] = (activity[node] / max_activity) * self.f0
        
        return self.frequencies
    
    def build_resonant_graph(self) -> Dict[Tuple[int, int], str]:
        """
        Build resonant graph based on frequency similarities.
        
        Two nodes are connected by a "resonant" edge if their social
        frequencies are within the resonance threshold.
        
        Returns:
            Dictionary with edge colors ('azul' = resonant, 'rojo' = non-resonant)
        """
        if not self.frequencies:
            self.compute_social_frequencies()
        
        nodes_list = sorted(self.nodes)
        
        for i, u in enumerate(nodes_list):
            for v in nodes_list[i+1:]:
                freq_u = self.frequencies[u]
                freq_v = self.frequencies[v]
                
                if resonancia_detectada(freq_u, freq_v, eps=self.threshold, f0=self.f0):
                    self.resonant_graph[(u, v)] = 'azul'  # Resonant
                else:
                    self.resonant_graph[(u, v)] = 'rojo'  # Non-resonant
        
        return self.resonant_graph
    
    def find_resonant_communities(self) -> List[Tuple]:
        """
        Find communities as resonant cliques.
        
        Communities are groups of nodes with mutually resonant frequencies,
        representing tight-knit groups in the social network.
        
        Returns:
            List of communities (each community is a tuple of node IDs)
        """
        if not self.resonant_graph:
            self.build_resonant_graph()
        
        # Find maximum resonant clique
        max_community = encontrar_clique_maximo(self.resonant_graph, 'azul')
        
        communities = [max_community] if max_community else []
        
        return communities
    
    def get_community_stats(self, community: Tuple[int, ...]) -> Dict:
        """
        Get statistics for a community.
        
        Args:
            community: Tuple of node IDs in the community
            
        Returns:
            Dictionary with community statistics
        """
        if not community:
            return {}
        
        freqs = [self.frequencies[node] for node in community]
        
        # Internal connections (within community)
        internal_edges = 0
        total_weight = 0.0
        for i, u in enumerate(community):
            for v in community[i+1:]:
                edge = (min(u, v), max(u, v))
                if edge in self.network:
                    internal_edges += 1
                    total_weight += self.network[edge]
        
        return {
            'size': len(community),
            'members': community,
            'mean_frequency': np.mean(freqs),
            'std_frequency': np.std(freqs),
            'min_frequency': np.min(freqs),
            'max_frequency': np.max(freqs),
            'internal_edges': internal_edges,
            'total_weight': total_weight,
            'density': internal_edges / (len(community) * (len(community) - 1) / 2) if len(community) > 1 else 0
        }
    
    def visualize_communities(self, communities: List[Tuple], save_path: Optional[str] = None):
        """
        Visualize detected communities.
        
        Args:
            communities: List of communities to visualize
            save_path: Optional path to save the visualization
        """
        try:
            import matplotlib.pyplot as plt
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Plot 1: Frequency distribution by community
            for idx, community in enumerate(communities[:5]):  # Max 5 communities
                freqs = [self.frequencies[node] for node in community]
                axes[0].hist(freqs, bins=20, alpha=0.6, label=f'Community {idx+1}')
            
            axes[0].set_title('Community Frequency Distributions')
            axes[0].set_xlabel('Social Frequency (Hz)')
            axes[0].set_ylabel('Count')
            axes[0].legend()
            axes[0].axvline(self.f0, color='red', linestyle='--', alpha=0.5, label='f₀')
            
            # Plot 2: Community sizes
            if communities:
                sizes = [len(c) for c in communities]
                axes[1].bar(range(len(sizes)), sizes, color='purple', alpha=0.7)
                axes[1].set_title('Community Sizes')
                axes[1].set_xlabel('Community Index')
                axes[1].set_ylabel('Number of Members')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"   Visualization saved to {save_path}")
            else:
                plt.show()
                
        except ImportError:
            print("   Matplotlib not available for visualization")


def create_sample_network(num_nodes: int = 50, num_edges: int = 150) -> Dict[Tuple[int, int], float]:
    """
    Create a sample social network for testing.
    
    Args:
        num_nodes: Number of nodes (people)
        num_edges: Number of edges (connections)
        
    Returns:
        Network dictionary
    """
    np.random.seed(42)
    network = {}
    
    # Create random edges with weights
    for _ in range(num_edges):
        u = np.random.randint(0, num_nodes)
        v = np.random.randint(0, num_nodes)
        
        if u != v:
            edge = (min(u, v), max(u, v))
            weight = np.random.exponential(1.0)  # Interaction strength
            network[edge] = weight
    
    return network


def demo_social_ramsey():
    """Demonstrate social network community detection."""
    print("=" * 70)
    print("  Social Network Community Detection")
    print("  Using Ramsey Vibrational Theory")
    print("  Frequency: 141.7001 Hz - Campo QCAL ∞³")
    print("=" * 70)
    print()
    
    # Create sample network
    print("1. NETWORK GENERATION")
    print("-" * 70)
    network = create_sample_network(num_nodes=30, num_edges=80)
    print(f"   Nodes: 30 people")
    print(f"   Edges: {len(network)} connections")
    print(f"   Average weight: {np.mean(list(network.values())):.2f}")
    print()
    
    # Initialize detector
    print("2. COMMUNITY DETECTION INITIALIZATION")
    print("-" * 70)
    detector = CommunityDetector(
        network=network,
        resonance_threshold=0.01,
        f0=141.7001
    )
    print(f"   Resonance threshold: {detector.threshold}")
    print(f"   Base frequency: {detector.f0} Hz")
    print()
    
    # Compute social frequencies
    print("3. SOCIAL FREQUENCY COMPUTATION")
    print("-" * 70)
    frequencies = detector.compute_social_frequencies(method='degree')
    print(f"   Computed frequencies for {len(frequencies)} nodes")
    print(f"   Frequency range: [{min(frequencies.values()):.2f}, {max(frequencies.values()):.2f}] Hz")
    print(f"   Mean frequency: {np.mean(list(frequencies.values())):.2f} Hz")
    print()
    
    # Build resonant graph
    print("4. RESONANT GRAPH CONSTRUCTION")
    print("-" * 70)
    resonant_graph = detector.build_resonant_graph()
    resonant_edges = sum(1 for color in resonant_graph.values() if color == 'azul')
    total_edges = len(resonant_graph)
    print(f"   Total potential edges: {total_edges}")
    print(f"   Resonant edges: {resonant_edges}")
    print(f"   Non-resonant edges: {total_edges - resonant_edges}")
    print(f"   Resonance ratio: {resonant_edges/total_edges*100:.1f}%")
    print()
    
    # Find communities
    print("5. COMMUNITY DETECTION")
    print("-" * 70)
    communities = detector.find_resonant_communities()
    
    if communities and communities[0]:
        print(f"   Found {len(communities)} community/communities")
        
        for idx, community in enumerate(communities):
            stats = detector.get_community_stats(community)
            print(f"\n   Community {idx + 1}:")
            print(f"      Size: {stats['size']} members")
            print(f"      Members: {stats['members'][:10]}..." if stats['size'] > 10 else f"      Members: {stats['members']}")
            print(f"      Mean frequency: {stats['mean_frequency']:.2f} Hz")
            print(f"      Frequency std: {stats['std_frequency']:.2f} Hz")
            print(f"      Internal density: {stats['density']:.2f}")
    else:
        print("   No large resonant communities found")
        print("   (Try adjusting resonance threshold or network structure)")
    print()
    
    print("=" * 70)
    print("  Applications:")
    print("-" * 70)
    print("  • Social media community detection")
    print("  • Organizational structure analysis")
    print("  • Recommendation systems (find similar users)")
    print("  • Fraud detection (identify coordinated behavior)")
    print("  • Network optimization (group similar interaction patterns)")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_social_ramsey()
