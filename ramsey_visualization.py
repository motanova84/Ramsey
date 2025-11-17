"""
Visualization module for Ramsey Vibrational Numbers

Provides visualization capabilities for exploration results including:
- Heatmaps of R_psi values
- Parameter sensitivity plots
- Comparison charts
"""

import csv
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_results_from_csv(filename='ramsey_results.csv'):
    """
    Load results from CSV file.
    
    Args:
        filename: Input CSV filename
    
    Returns:
        List of result dictionaries
    """
    results = []
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert numeric fields
                result = {
                    'r': int(row['r']),
                    's': int(row['s']),
                    'epsilon': float(row['epsilon']),
                    'R_psi': int(row['R_psi']) if row['R_psi'] and row['R_psi'] != 'None' else None,
                    'duration_seconds': float(row['duration_seconds']),
                    'timestamp': row['timestamp']
                }
                results.append(result)
        return results
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []


def plot_heatmap(results, output_file='ramsey_heatmap.png'):
    """
    Create a heatmap of R_psi values for different (r,s) pairs at a fixed epsilon.
    
    Args:
        results: List of result dictionaries
        output_file: Output image filename
    """
    if not results:
        print("No results to visualize.")
        return
    
    # Filter results for a specific epsilon (use the first one found)
    eps_value = results[0]['epsilon']
    filtered = [r for r in results if r['epsilon'] == eps_value and r['R_psi'] is not None]
    
    if not filtered:
        print("No valid results for heatmap.")
        return
    
    # Extract unique r and s values
    r_values = sorted(list(set(r['r'] for r in filtered)))
    s_values = sorted(list(set(r['s'] for r in filtered)))
    
    # Create matrix
    matrix = np.zeros((len(r_values), len(s_values)))
    for result in filtered:
        i = r_values.index(result['r'])
        j = s_values.index(result['s'])
        matrix[i, j] = result['R_psi']
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix, cmap='viridis', aspect='auto')
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(s_values)))
    ax.set_yticks(np.arange(len(r_values)))
    ax.set_xticklabels(s_values)
    ax.set_yticklabels(r_values)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('R_psi value', rotation=270, labelpad=20)
    
    # Add value annotations
    for i in range(len(r_values)):
        for j in range(len(s_values)):
            if matrix[i, j] > 0:
                ax.text(j, i, int(matrix[i, j]),
                             ha="center", va="center", color="w", fontsize=12)
    
    ax.set_xlabel('s (blue clique size)', fontsize=12)
    ax.set_ylabel('r (red clique size)', fontsize=12)
    ax.set_title(f'Vibrational Ramsey Numbers R_psi(r,s) at epsilon={eps_value}', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Heatmap saved to {output_file}")
    plt.close()


def plot_epsilon_sensitivity(results, output_file='epsilon_sensitivity.png'):
    """
    Plot how R_psi varies with epsilon for different (r,s) pairs.
    
    Args:
        results: List of result dictionaries
        output_file: Output image filename
    """
    if not results:
        print("No results to visualize.")
        return
    
    # Group by (r,s) pairs
    pairs = {}
    for result in results:
        if result['R_psi'] is not None:
            key = (result['r'], result['s'])
            if key not in pairs:
                pairs[key] = []
            pairs[key].append((result['epsilon'], result['R_psi']))
    
    if not pairs:
        print("No valid results for sensitivity plot.")
        return
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for (r, s), data in sorted(pairs.items()):
        data.sort()  # Sort by epsilon
        epsilons, R_psis = zip(*data)
        ax.plot(epsilons, R_psis, marker='o', label=f'({r},{s})', linewidth=2, markersize=8)
    
    ax.set_xlabel('Epsilon (resonance threshold)', fontsize=12)
    ax.set_ylabel('R_psi value', fontsize=12)
    ax.set_title('Vibrational Ramsey Numbers: Epsilon Sensitivity', fontsize=14)
    ax.legend(loc='best', title='(r,s) pairs')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Sensitivity plot saved to {output_file}")
    plt.close()


def plot_computation_time(results, output_file='computation_time.png'):
    """
    Plot computation time for different parameter combinations.
    
    Args:
        results: List of result dictionaries
        output_file: Output image filename
    """
    if not results:
        print("No results to visualize.")
        return
    
    # Prepare data
    labels = [f"({r['r']},{r['s']},{r['epsilon']:.2f})" for r in results]
    times = [r['duration_seconds'] for r in results]

    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart of computation times
    x_pos = np.arange(len(labels))
    ax1.bar(x_pos, times, color='steelblue', alpha=0.7)
    ax1.set_xlabel('Parameter combination (r,s,epsilon)', fontsize=11)
    ax1.set_ylabel('Computation time (seconds)', fontsize=11)
    ax1.set_title('Computation Time by Parameters', fontsize=13)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Scatter plot: R_psi vs computation time
    valid_results = [r for r in results if r['R_psi'] is not None]
    if valid_results:
        R_psi_vals = [r['R_psi'] for r in valid_results]
        time_vals = [r['duration_seconds'] for r in valid_results]
        ax2.scatter(R_psi_vals, time_vals, c='coral', s=100, alpha=0.6, edgecolors='black')
        ax2.set_xlabel('R_psi value', fontsize=11)
        ax2.set_ylabel('Computation time (seconds)', fontsize=11)
        ax2.set_title('Computation Time vs R_psi Value', fontsize=13)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Computation time plot saved to {output_file}")
    plt.close()


def generate_all_visualizations(csv_filename='ramsey_results.csv', output_dir='visualizations'):
    """
    Generate all visualizations from results CSV.
    
    Args:
        csv_filename: Input CSV filename
        output_dir: Directory for output images
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load results
    results = load_results_from_csv(csv_filename)
    
    if not results:
        print("No results found. Run the explorer first to generate data.")
        return
    
    print(f"\nGenerating visualizations from {len(results)} results...")
    print("=" * 70)
    
    # Generate plots
    plot_heatmap(results, f'{output_dir}/ramsey_heatmap.png')
    plot_epsilon_sensitivity(results, f'{output_dir}/epsilon_sensitivity.png')
    plot_computation_time(results, f'{output_dir}/computation_time.png')
    
    print("\n" + "=" * 70)
    print(f"✓ All visualizations saved to {output_dir}/")
    print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RAMSEY VIBRATIONAL VISUALIZATION")
    print("=" * 70)
    
    # Generate visualizations from existing CSV
    generate_all_visualizations('ramsey_results.csv', 'visualizations')
