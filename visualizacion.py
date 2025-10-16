"""
Utilidades de Visualización para Ramsey Cuántico Vibracional

Proporciona funciones para visualizar grafos vibracionales y sus coloraciones.
Nota: Requiere matplotlib (opcional, no incluido en requirements.txt)
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Advertencia: matplotlib no disponible. Instalando...")
    print("Ejecuta: pip install matplotlib")

import numpy as np
from ramsey_vibracional import generar_coloracion_vibracional


def visualizar_grafo_vibracional(frecuencias, eps=0.001, f0=141.7001, 
                                  filename=None, show=True):
    """
    Visualiza un grafo vibracional con su coloración
    
    Args:
        frecuencias: Lista de frecuencias para cada vértice
        eps: Umbral de coherencia
        f0: Frecuencia base
        filename: Nombre de archivo para guardar (opcional)
        show: Si mostrar el gráfico
    """
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib no está disponible para visualización")
        return
    
    n = len(frecuencias)
    grafo = generar_coloracion_vibracional(frecuencias, eps, f0)
    
    # Configurar posiciones en círculo
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    pos = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Dibujar aristas
    for (i, j), color in grafo.items():
        x1, y1 = pos[i]
        x2, y2 = pos[j]
        
        col = '#0066CC' if color == 'azul' else '#CC0000'
        width = 2 if color == 'azul' else 0.5
        alpha = 0.8 if color == 'azul' else 0.3
        
        ax.plot([x1, x2], [y1, y2], color=col, linewidth=width, 
                alpha=alpha, zorder=1)
    
    # Dibujar vértices
    for i in range(n):
        x, y = pos[i]
        # Color basado en frecuencia
        norm_freq = frecuencias[i] / max(frecuencias)
        color = plt.cm.viridis(norm_freq)
        
        ax.scatter(x, y, s=500, c=[color], edgecolors='black', 
                  linewidths=2, zorder=2)
        ax.text(x, y, str(i), ha='center', va='center', 
               fontsize=12, fontweight='bold', zorder=3)
        
        # Mostrar frecuencia
        ax.text(x*1.15, y*1.15, f'{frecuencias[i]:.1f} Hz', 
               ha='center', va='center', fontsize=8)
    
    # Leyenda
    azul_patch = mpatches.Patch(color='#0066CC', label='Azul (Resonante)')
    rojo_patch = mpatches.Patch(color='#CC0000', label='Rojo (No Resonante)')
    ax.legend(handles=[azul_patch, rojo_patch], loc='upper right', fontsize=12)
    
    # Título
    azules = sum(1 for c in grafo.values() if c == 'azul')
    rojas = len(grafo) - azules
    ax.set_title(f'Grafo Vibracional K_{n}\nf₀={f0} Hz, ε={eps} Hz\n'
                f'Azules: {azules}, Rojas: {rojas}', 
                fontsize=14, fontweight='bold')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado en: {filename}")
    
    if show:
        plt.show()
    
    return fig, ax


def visualizar_espectro_frecuencias(frecuencias, f0=141.7001, filename=None, show=True):
    """
    Visualiza el espectro de frecuencias en relación con f0
    
    Args:
        frecuencias: Lista de frecuencias
        f0: Frecuencia base
        filename: Nombre de archivo para guardar (opcional)
        show: Si mostrar el gráfico
    """
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib no está disponible para visualización")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Gráfico 1: Distribución de frecuencias
    ax1.scatter(range(len(frecuencias)), frecuencias, s=100, alpha=0.7)
    ax1.axhline(y=f0, color='r', linestyle='--', linewidth=2, 
               label=f'f₀ = {f0} Hz')
    ax1.set_xlabel('Índice de Vértice', fontsize=12)
    ax1.set_ylabel('Frecuencia (Hz)', fontsize=12)
    ax1.set_title('Distribución de Frecuencias Vibracionales', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Módulo respecto a f0
    modulos = [f % f0 for f in frecuencias]
    ax2.scatter(range(len(modulos)), modulos, s=100, alpha=0.7, c='green')
    ax2.axhline(y=0, color='r', linestyle='--', linewidth=2, label='Resonancia perfecta')
    ax2.set_xlabel('Índice de Vértice', fontsize=12)
    ax2.set_ylabel('Frecuencia mod f₀ (Hz)', fontsize=12)
    ax2.set_title('Distancia a Resonancia (mod f₀)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-5, f0 + 5)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado en: {filename}")
    
    if show:
        plt.show()
    
    return fig, (ax1, ax2)


def ejemplo_visualizacion():
    """Ejemplo de uso de visualización"""
    print("\n" + "="*70)
    print("EJEMPLO: Visualización de Grafo Vibracional")
    print("="*70)
    
    if not MATPLOTLIB_AVAILABLE:
        print("\nPor favor instala matplotlib para usar visualizaciones:")
        print("  pip install matplotlib")
        return
    
    # Crear frecuencias de ejemplo
    n = 8
    frecuencias = [
        0.0, 0.0005,      # Grupo en resonancia cerca de 0
        50.0, 50.0003,    # Grupo en resonancia cerca de 50
        100.0, 100.5,     # No resonantes
        141.7001, 141.7005  # Grupo en resonancia cerca de f0
    ]
    
    print(f"\nVisualizando grafo K_{n} con frecuencias:")
    for i, f in enumerate(frecuencias):
        print(f"  v{i}: {f} Hz")
    
    # Visualizar grafo
    visualizar_grafo_vibracional(frecuencias, show=False, 
                                filename='grafo_vibracional.png')
    
    # Visualizar espectro
    visualizar_espectro_frecuencias(frecuencias, show=False,
                                   filename='espectro_frecuencias.png')
    
    print("\n✓ Visualizaciones generadas:")
    print("  - grafo_vibracional.png")
    print("  - espectro_frecuencias.png")


if __name__ == "__main__":
    ejemplo_visualizacion()
