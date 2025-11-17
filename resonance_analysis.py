#!/usr/bin/env python3
"""
Statistical Resonance Analysis for Vibrational Ramsey Theory

Analyzes the distribution of Δω = |ωᵢ − ωⱼ| mod f₀ and visualizes
resonance patterns in vibrational graph colorings.

Usage:
    python resonance_analysis.py --n=10 --save-plot=resonance.png
    python resonance_analysis.py --graph-viz --r=4 --s=4
"""

import argparse
import numpy as np
import sys
from pathlib import Path

# Try to import plotting libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    print("Warning: matplotlib not installed. Visualization disabled.")
    print("Install with: pip install matplotlib")
    HAS_MATPLOTLIB = False

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    print("Warning: networkx not installed. Graph visualization disabled.")
    print("Install with: pip install networkx")
    HAS_NETWORKX = False


# Constants
F0 = 141.7001  # Hz - Universal coherence frequency
EPSILON = 0.001  # Hz - Coherence threshold


def generate_frequencies(n, distribution='uniform', seed=None):
    """
    Generate n frequencies in [0, f₀)
    
    Args:
        n: Number of frequencies
        distribution: 'uniform', 'clustered', or 'random'
        seed: Random seed for reproducibility
    """
    if seed is not None:
        np.random.seed(seed)
    
    if distribution == 'uniform':
        return np.linspace(0, F0, n, endpoint=False)
    elif distribution == 'clustered':
        # Create clusters around harmonic frequencies
        num_clusters = max(1, n // 5)
        cluster_centers = np.random.uniform(0, F0, num_clusters)
        cluster_assignments = np.random.choice(num_clusters, n)
        offsets = np.random.normal(0, F0/50, n)
        return (cluster_centers[cluster_assignments] + offsets) % F0
    else:  # random
        return np.random.uniform(0, F0, n)


def compute_pairwise_differences(frequencies):
    """
    Compute all pairwise frequency differences modulo f₀
    
    Returns:
        Array of differences, taking minimum of diff and f₀-diff
    """
    n = len(frequencies)
    differences = []
    
    for i in range(n):
        for j in range(i+1, n):
            diff = abs(frequencies[i] - frequencies[j])
            # Take minimum due to wrap-around
            min_diff = min(diff, F0 - diff)
            differences.append(min_diff)
    
    return np.array(differences)


def classify_edges(differences, epsilon=EPSILON):
    """
    Classify edges as resonant (blue) or non-resonant (red)
    
    Returns:
        Dictionary with counts and lists
    """
    blue_edges = differences < epsilon
    red_edges = ~blue_edges
    
    return {
        'blue_count': np.sum(blue_edges),
        'red_count': np.sum(red_edges),
        'blue_diffs': differences[blue_edges],
        'red_diffs': differences[red_edges],
        'total': len(differences)
    }


def plot_distribution_histogram(differences, epsilon=EPSILON, filename=None):
    """
    Create histogram of frequency differences with resonance bands marked
    """
    if not HAS_MATPLOTLIB:
        print("Cannot create plot: matplotlib not installed")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram
    n_bins = 50
    counts, bins, patches = ax.hist(
        differences, 
        bins=n_bins,
        density=True,
        alpha=0.7,
        color='gray',
        edgecolor='black'
    )
    
    # Color bars in resonance band differently
    for i, (patch, bin_left, bin_right) in enumerate(zip(patches, bins[:-1], bins[1:])):
        if bin_right <= epsilon:
            patch.set_facecolor('blue')
            patch.set_alpha(0.8)
        elif bin_left >= F0/2 - epsilon:
            patch.set_facecolor('blue')
            patch.set_alpha(0.8)
    
    # Mark resonance bands
    ax.axvline(epsilon, color='blue', linestyle='--', linewidth=2, label=f'Resonance threshold (ε={epsilon} Hz)')
    ax.axvspan(0, epsilon, alpha=0.2, color='blue', label='Resonance band')
    
    # Labels and title
    ax.set_xlabel('Δω = |ωᵢ − ωⱼ| mod f₀ (Hz)', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.set_title(f'Distribution of Pairwise Frequency Differences (f₀={F0} Hz)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add statistics box
    n_resonant = np.sum(differences < epsilon)
    n_total = len(differences)
    stats_text = f'Resonant edges: {n_resonant}/{n_total} ({100*n_resonant/n_total:.1f}%)'
    ax.text(0.98, 0.98, stats_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Histogram saved to {filename}")
    else:
        plt.savefig('resonance_histogram.png', dpi=300, bbox_inches='tight')
        print(f"✓ Histogram saved to resonance_histogram.png")
    
    plt.close()


def build_graph(frequencies, epsilon=EPSILON):
    """
    Build NetworkX graph with vibrational coloring
    """
    if not HAS_NETWORKX:
        return None
    
    n = len(frequencies)
    G = nx.Graph()
    
    # Add nodes with frequency attributes
    for i in range(n):
        G.add_node(i, frequency=frequencies[i])
    
    # Add edges with color attributes
    for i in range(n):
        for j in range(i+1, n):
            diff = abs(frequencies[i] - frequencies[j])
            min_diff = min(diff, F0 - diff)
            
            if min_diff < epsilon:
                G.add_edge(i, j, color='blue', resonant=True, diff=min_diff)
            else:
                G.add_edge(i, j, color='red', resonant=False, diff=min_diff)
    
    return G


def visualize_graph(G, filename=None):
    """
    Visualize colored graph with resonance structure
    """
    if not HAS_MATPLOTLIB or not HAS_NETWORKX:
        print("Cannot visualize graph: matplotlib or networkx not installed")
        return
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Extract edge colors
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    
    # Draw graph
    nx.draw_networkx_nodes(
        G, pos,
        node_color='lightgray',
        node_size=500,
        ax=ax
    )
    
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=2,
        alpha=0.6,
        ax=ax
    )
    
    nx.draw_networkx_labels(
        G, pos,
        font_size=10,
        font_weight='bold',
        ax=ax
    )
    
    # Title and legend
    n_blue = sum(1 for _, _, data in G.edges(data=True) if data['color'] == 'blue')
    n_red = len(G.edges()) - n_blue
    
    ax.set_title(
        f'Vibrational Graph Coloring (n={len(G.nodes())})\n'
        f'Blue (resonant) edges: {n_blue}, Red edges: {n_red}',
        fontsize=14,
        fontweight='bold'
    )
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='blue', linewidth=2, label='Resonant (Δω < ε)'),
        Line2D([0], [0], color='red', linewidth=2, label='Non-resonant')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    ax.axis('off')
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Graph visualization saved to {filename}")
    else:
        plt.savefig('resonance_graph.png', dpi=300, bbox_inches='tight')
        print(f"✓ Graph visualization saved to resonance_graph.png")
    
    plt.close()


def find_cliques(G, color):
    """
    Find maximal monochromatic cliques in graph
    """
    if not HAS_NETWORKX:
        return []
    
    # Create subgraph with only edges of specified color
    edges = [(u, v) for u, v, data in G.edges(data=True) if data['color'] == color]
    H = nx.Graph()
    H.add_edges_from(edges)
    
    # Find all maximal cliques
    cliques = list(nx.find_cliques(H))
    
    # Sort by size
    cliques.sort(key=len, reverse=True)
    
    return cliques


def print_statistics(frequencies, differences, classification):
    """
    Print comprehensive statistics about resonance structure
    """
    n = len(frequencies)
    
    print("\n" + "="*70)
    print("RESONANCE STATISTICS")
    print("="*70)
    
    print(f"\nGraph Parameters:")
    print(f"  Vertices: {n}")
    print(f"  Total edges: {classification['total']} = C({n},2)")
    print(f"  Coherence frequency: f₀ = {F0} Hz")
    print(f"  Resonance threshold: ε = {EPSILON} Hz")
    
    print(f"\nEdge Classification:")
    blue_pct = 100 * classification['blue_count'] / classification['total']
    red_pct = 100 * classification['red_count'] / classification['total']
    print(f"  Blue (resonant) edges: {classification['blue_count']} ({blue_pct:.1f}%)")
    print(f"  Red (non-resonant) edges: {classification['red_count']} ({red_pct:.1f}%)")
    
    print(f"\nFrequency Statistics:")
    print(f"  Mean frequency: {np.mean(frequencies):.2f} Hz")
    print(f"  Std deviation: {np.std(frequencies):.2f} Hz")
    print(f"  Range: [{np.min(frequencies):.2f}, {np.max(frequencies):.2f}] Hz")
    
    print(f"\nDifference Statistics:")
    print(f"  Mean Δω: {np.mean(differences):.4f} Hz")
    print(f"  Median Δω: {np.median(differences):.4f} Hz")
    print(f"  Std deviation: {np.std(differences):.4f} Hz")
    
    if classification['blue_count'] > 0:
        print(f"\nResonant Edge Statistics:")
        print(f"  Mean Δω (blue): {np.mean(classification['blue_diffs']):.6f} Hz")
        print(f"  Max Δω (blue): {np.max(classification['blue_diffs']):.6f} Hz")
    
    if classification['red_count'] > 0:
        print(f"\nNon-Resonant Edge Statistics:")
        print(f"  Mean Δω (red): {np.mean(classification['red_diffs']):.4f} Hz")
        print(f"  Min Δω (red): {np.min(classification['red_diffs']):.4f} Hz")
    
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Statistical resonance analysis for vibrational Ramsey theory'
    )
    parser.add_argument(
        '--n',
        type=int,
        default=10,
        help='Number of vertices (default: 10)'
    )
    parser.add_argument(
        '--distribution',
        choices=['uniform', 'clustered', 'random'],
        default='random',
        help='Frequency distribution (default: random)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--save-histogram',
        type=str,
        help='Save histogram to file'
    )
    parser.add_argument(
        '--graph-viz',
        action='store_true',
        help='Generate graph visualization'
    )
    parser.add_argument(
        '--save-graph',
        type=str,
        help='Save graph visualization to file'
    )
    parser.add_argument(
        '--cliques',
        action='store_true',
        help='Find and display maximal cliques'
    )
    
    args = parser.parse_args()
    
    print(f"\nGenerating {args.n} frequencies with {args.distribution} distribution...")
    frequencies = generate_frequencies(args.n, args.distribution, args.seed)
    
    print("Computing pairwise differences...")
    differences = compute_pairwise_differences(frequencies)
    
    print("Classifying edges...")
    classification = classify_edges(differences)
    
    # Print statistics
    print_statistics(frequencies, differences, classification)
    
    # Generate histogram
    if HAS_MATPLOTLIB:
        print("\nGenerating histogram...")
        plot_distribution_histogram(differences, filename=args.save_histogram)
    
    # Generate graph visualization
    if args.graph_viz or args.save_graph:
        if HAS_NETWORKX:
            print("\nBuilding graph...")
            G = build_graph(frequencies)
            
            print("Visualizing graph...")
            visualize_graph(G, filename=args.save_graph)
            
            # Find cliques if requested
            if args.cliques:
                print("\nFinding maximal cliques...")
                blue_cliques = find_cliques(G, 'blue')
                red_cliques = find_cliques(G, 'red')
                
                print(f"\nMaximal Blue Cliques (top 5):")
                for i, clique in enumerate(blue_cliques[:5], 1):
                    print(f"  {i}. Size {len(clique)}: {clique}")
                
                print(f"\nMaximal Red Cliques (top 5):")
                for i, clique in enumerate(red_cliques[:5], 1):
                    print(f"  {i}. Size {len(clique)}: {clique}")
        else:
            print("Cannot generate graph: networkx not installed")
    
    print("\nAnalysis complete!")


if __name__ == '__main__':
    main()
