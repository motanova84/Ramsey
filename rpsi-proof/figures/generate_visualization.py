#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualize Vibrational Ramsey Coloring on a Circle

This script generates a visualization of the vibrational coloring constraints
for Rψ(5,5). It shows:
- Frequencies ω arranged on a circle of length f₀
- Blue (resonant) edges when |ωᵢ - ωⱼ| mod f₀ < ε
- Red (non-resonant) edges otherwise
- Example impossible configuration (no monochromatic K₅)

Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
Frecuencia: 141.7001 Hz - Campo QCAL ∞³
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def circular_distance(omega_i, omega_j, f0=141.7001):
    """Calculate circular distance between two frequencies."""
    diff = abs(omega_i - omega_j)
    return min(diff, f0 - diff)


def is_resonant(omega_i, omega_j, epsilon=0.037, f0=141.7001):
    """Check if two frequencies are resonant (blue edge)."""
    return circular_distance(omega_i, omega_j, f0) <= epsilon


def generate_vibrational_coloring_visualization():
    """Generate visualization of vibrational coloring on a circle."""
    
    f0 = 141.7001
    epsilon = 0.037
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # ===== LEFT PANEL: Circular Representation =====
    
    # Example frequencies for 16 vertices
    # Spread them somewhat uniformly but show resonance patterns
    n = 16
    frequencies = np.array([
        0.0, 9.2, 18.5, 27.7, 37.0, 46.2, 55.4, 64.7,
        73.9, 83.1, 92.4, 101.6, 110.9, 120.1, 129.3, 138.6
    ])
    
    # Normalize to [0, 2π) for circle visualization
    angles = (frequencies / f0) * 2 * np.pi
    
    # Draw circle
    circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
    ax1.add_patch(circle)
    
    # Mark epsilon regions (resonance zones)
    epsilon_angle = (epsilon / f0) * 2 * np.pi
    for angle in angles:
        arc = patches.Wedge(
            (0, 0), 1.05, 
            np.degrees(angle - epsilon_angle), 
            np.degrees(angle + epsilon_angle),
            width=0.1, 
            facecolor='lightblue', 
            alpha=0.3,
            edgecolor='none'
        )
        ax1.add_patch(arc)
    
    # Draw vertices
    for i, angle in enumerate(angles):
        x = np.cos(angle)
        y = np.sin(angle)
        
        # Draw vertex
        ax1.plot(x, y, 'o', markersize=12, color='darkblue', zorder=10)
        
        # Label vertex
        label_r = 1.2
        label_x = label_r * np.cos(angle)
        label_y = label_r * np.sin(angle)
        ax1.text(label_x, label_y, f'v{i}', 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Draw some example edges
    # Blue edges (resonant)
    for i in range(n):
        for j in range(i+1, n):
            if is_resonant(frequencies[i], frequencies[j], epsilon, f0):
                x1, y1 = np.cos(angles[i]), np.sin(angles[i])
                x2, y2 = np.cos(angles[j]), np.sin(angles[j])
                ax1.plot([x1, x2], [y1, y2], 'b-', alpha=0.2, linewidth=0.5)
    
    # Highlight one blue triangle as example
    blue_triangle = [0, 1, 2]
    for i in range(3):
        for j in range(i+1, 3):
            vi, vj = blue_triangle[i], blue_triangle[j]
            x1, y1 = np.cos(angles[vi]), np.sin(angles[vi])
            x2, y2 = np.cos(angles[vj]), np.sin(angles[vj])
            ax1.plot([x1, x2], [y1, y2], 'b-', linewidth=2, alpha=0.7)
    
    # Highlight one red triangle as example
    red_triangle = [6, 10, 14]
    for i in range(3):
        for j in range(i+1, 3):
            vi, vj = red_triangle[i], red_triangle[j]
            x1, y1 = np.cos(angles[vi]), np.sin(angles[vi])
            x2, y2 = np.cos(angles[vj]), np.sin(angles[vj])
            ax1.plot([x1, x2], [y1, y2], 'r-', linewidth=2, alpha=0.7)
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Vibrational Coloring on Circle\n' + 
                  f'f₀ = {f0} Hz, ε = {epsilon}', 
                  fontsize=12, fontweight='bold')
    
    # Add legend
    blue_line = plt.Line2D([0], [0], color='blue', linewidth=2, label='Blue (resonant) |ω| < ε')
    red_line = plt.Line2D([0], [0], color='red', linewidth=2, label='Red (non-resonant) |ω| ≥ ε')
    epsilon_patch = patches.Patch(facecolor='lightblue', alpha=0.3, label='Resonance zones')
    ax1.legend(handles=[blue_line, red_line, epsilon_patch], loc='upper left')
    
    # ===== RIGHT PANEL: Impossible Triangle =====
    
    # Draw triangle showing contradiction
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 3.5)
    ax2.axis('off')
    
    # Triangle vertices
    v1 = np.array([2, 3])
    v2 = np.array([1, 1])
    v3 = np.array([3, 1])
    
    # Draw vertices
    for v, label in zip([v1, v2, v3], ['A', 'B', 'C']):
        ax2.plot(v[0], v[1], 'o', markersize=20, color='darkblue')
        ax2.text(v[0], v[1], label, ha='center', va='center', 
                color='white', fontsize=12, fontweight='bold')
    
    # Draw edges with colors showing contradiction
    # Edge AB: red
    ax2.plot([v1[0], v2[0]], [v1[1], v2[1]], 'r-', linewidth=4, label='Red')
    ax2.text((v1[0]+v2[0])/2 - 0.3, (v1[1]+v2[1])/2, 'RED', 
            fontsize=10, color='red', fontweight='bold')
    
    # Edge AC: red
    ax2.plot([v1[0], v3[0]], [v1[1], v3[1]], 'r-', linewidth=4)
    ax2.text((v1[0]+v3[0])/2 + 0.3, (v1[1]+v3[1])/2, 'RED', 
            fontsize=10, color='red', fontweight='bold')
    
    # Edge BC: blue
    ax2.plot([v2[0], v3[0]], [v2[1], v3[1]], 'b-', linewidth=4, label='Blue')
    ax2.text((v2[0]+v3[0])/2, (v2[1]+v3[1])/2 - 0.3, 'BLUE', 
            fontsize=10, color='blue', fontweight='bold')
    
    ax2.set_title('Impossible Configuration\nfor Circular Distance', 
                  fontsize=12, fontweight='bold')
    
    # Add constraint equations
    constraint_text = (
        'Constraints:\n'
        '|ωₐ - ωᵦ| mod f₀ ≥ ε  (RED)\n'
        '|ωₐ - ωᴄ| mod f₀ ≥ ε  (RED)\n'
        '|ωᵦ - ωᴄ| mod f₀ < ε  (BLUE)\n\n'
        'But: |ωₐ - ωᵦ| + |ωᵦ - ωᴄ| ≥ |ωₐ - ωᴄ|\n'
        '(Circular triangle inequality)\n\n'
        '⇒ CONTRADICTION for ε << f₀'
    )
    ax2.text(2, 0.2, constraint_text, ha='center', va='top',
            fontsize=8, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Overall title
    fig.suptitle('Vibrational Ramsey Coloring: Rψ(5,5) ≤ 16', 
                fontsize=14, fontweight='bold', y=0.98)
    
    # Add footer
    fig.text(0.5, 0.02, 
            'QCAL ∞³ Field - Frequency: 141.7001 Hz - José Manuel Mota Burruezo',
            ha='center', fontsize=8, style='italic')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    return fig


if __name__ == '__main__':
    # Generate visualization
    fig = generate_vibrational_coloring_visualization()
    
    # Save figure
    output_path = 'rpsi-coloring-circle.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Visualization saved to: {output_path}")
    
    # Also save as PDF for high quality
    pdf_path = 'rpsi-coloring-circle.pdf'
    fig.savefig(pdf_path, bbox_inches='tight')
    print(f"✓ PDF version saved to: {pdf_path}")
    
    # Show
    plt.show()
