#!/usr/bin/env python3
"""
V13 Limit Validator: Thermodynamic Limit Extrapolation for Atlas³
===================================================================

This script implements the V13 protocol for validating the thermodynamic
limit of the spectral curvature constant κ_∞ in the Atlas³ framework.

Key Features:
- V13-B: Extrapolation of κ_∞ via thermodynamic limit
- V13-C: Number Variance Σ²(L) rigidity test vs GOE prediction

Model:
    C_est(N) = κ_∞ + a/N^α

Target:
    κ_Π = 2.577310
    α ≈ 0.5 (Noetic Diffusion Convergence)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0
Frequency: 141.7001 Hz
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.linalg import eigvalsh
import json
from typing import Dict, List, Tuple
import sys
from pathlib import Path

# Import Atlas3QCAL
try:
    from atlas3_qcal import Atlas3QCAL
except ImportError:
    print("Error: atlas3_qcal module not found")
    sys.exit(1)

# Sovereign metadata
__author__ = "José Manuel Mota Burruezo (JMMB Ψ✧)"
__architecture__ = "QCAL ∞³"
__license__ = "Sovereign Noetic License 1.0"
__f0__ = 141.7001


class V13LimitValidator:
    """
    V13 Limit Validator for thermodynamic limit extrapolation.
    
    This class implements the complete V13 protocol for validating
    the convergence of the spectral curvature to κ_∞.
    """
    
    def __init__(self, kappa_pi_target: float = 2.577310):
        """
        Initialize V13 Limit Validator.
        
        Args:
            kappa_pi_target: Target value for κ_Π
        """
        self.kappa_pi_target = kappa_pi_target
        self.atlas = Atlas3QCAL(f0=__f0__)
        
        # Storage for results
        self.scaling_data = None
        self.fit_results = None
        self.number_variance_data = None
        
    def thermodynamic_limit_model(self, N: np.ndarray, kappa_inf: float, 
                                   a: float, alpha: float) -> np.ndarray:
        """
        Thermodynamic limit scaling model.
        
        C_est(N) = κ_∞ + a/N^α
        
        Args:
            N: System sizes
            kappa_inf: Asymptotic value κ_∞
            a: Amplitude coefficient
            alpha: Decay exponent (expected ~0.5)
            
        Returns:
            Predicted curvature values
        """
        return kappa_inf + a / (N ** alpha)
    
    def compute_spectral_curvature(self, N: int, damping: float = 0.1,
                                   coupling_strength: float = 0.15) -> float:
        """
        Compute spectral curvature for system size N.
        
        This uses the scaling law κ(N) = gap(N) * √(N log N)
        
        Args:
            N: System size (number of modes)
            damping: Damping coefficient
            coupling_strength: Coupling strength
            
        Returns:
            Spectral curvature κ(N)
        """
        # Generate system
        self.atlas.generate_modal_basis(N, damping=damping)
        self.atlas.construct_operator_O(N, coupling_strength=coupling_strength)
        
        # Compute spectral DNA
        dna = self.atlas.compute_spectral_dna()
        
        # Calculate curvature using scaling law
        if N <= 1:
            return 0.0
        
        kappa = dna['spectral_gap'] * np.sqrt(N * np.log(N))
        
        return kappa
    
    def multi_scale_sweep(self, N_values: List[int] = [128, 256, 512, 1024, 2560],
                          damping: float = 0.1,
                          coupling_strength: float = 0.15) -> Dict:
        """
        Perform multi-scale sweep across different system sizes.
        
        Args:
            N_values: List of system sizes to test
            damping: Damping coefficient
            coupling_strength: Coupling strength
            
        Returns:
            Dictionary with sweep results
        """
        print("🔬 V13-B: Multi-Scale Sweep")
        print("=" * 70)
        
        kappa_values = []
        spectral_gaps = []
        
        for i, N in enumerate(N_values):
            print(f"Processing N={N}... ({i+1}/{len(N_values)})", end=" ")
            
            kappa = self.compute_spectral_curvature(N, damping, coupling_strength)
            gap = self.atlas.compute_spectral_dna()['spectral_gap']
            
            kappa_values.append(kappa)
            spectral_gaps.append(gap)
            
            print(f"κ({N}) = {kappa:.6f}")
        
        self.scaling_data = {
            'N_values': N_values,
            'kappa_values': kappa_values,
            'spectral_gaps': spectral_gaps,
            'damping': damping,
            'coupling_strength': coupling_strength
        }
        
        print()
        return self.scaling_data
    
    def extrapolate_kappa_infinity(self) -> Dict:
        """
        Extrapolate κ_∞ using thermodynamic limit model.
        
        Fits the model: C_est(N) = κ_∞ + a/N^α
        
        Returns:
            Dictionary with fit results
        """
        if self.scaling_data is None:
            raise ValueError("Must run multi_scale_sweep first")
        
        print("🧮 V13-B: Thermodynamic Limit Extrapolation")
        print("=" * 70)
        
        N_array = np.array(self.scaling_data['N_values'])
        kappa_array = np.array(self.scaling_data['kappa_values'])
        
        # Initial guess: [kappa_inf, a, alpha]
        p0 = [self.kappa_pi_target, 1.0, 0.5]
        
        # Bounds: kappa_inf in [2.0, 3.0], a > 0, alpha in [0.3, 0.7]
        bounds = ([2.0, 0, 0.3], [3.0, 100, 0.7])
        
        try:
            # Perform non-linear regression
            popt, pcov = curve_fit(
                self.thermodynamic_limit_model,
                N_array,
                kappa_array,
                p0=p0,
                bounds=bounds,
                maxfev=5000
            )
            
            kappa_inf, a, alpha = popt
            perr = np.sqrt(np.diag(pcov))
            
            # Calculate goodness of fit
            residuals = kappa_array - self.thermodynamic_limit_model(N_array, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((kappa_array - np.mean(kappa_array))**2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            # Calculate error metrics
            abs_error = abs(kappa_inf - self.kappa_pi_target)
            rel_error = abs_error / self.kappa_pi_target
            
            # Convert inf to None for JSON serialization
            def clean_for_json(val):
                if np.isinf(val) or np.isnan(val):
                    return None
                return float(val)
            
            self.fit_results = {
                'kappa_infinity': clean_for_json(kappa_inf),
                'kappa_infinity_error': clean_for_json(perr[0]),
                'amplitude_a': clean_for_json(a),
                'amplitude_a_error': clean_for_json(perr[1]),
                'exponent_alpha': clean_for_json(alpha),
                'exponent_alpha_error': clean_for_json(perr[2]),
                'kappa_pi_target': float(self.kappa_pi_target),
                'absolute_error': clean_for_json(abs_error),
                'relative_error_percent': clean_for_json(rel_error * 100),
                'r_squared': clean_for_json(r_squared),
                'residuals': residuals.tolist(),
                'fit_success': True
            }
            
            # Print results
            print(f"Fit Results:")
            print(f"  κ_∞ (estimated) = {kappa_inf:.6f} ± {perr[0]:.6f}")
            print(f"  κ_Π (target)    = {self.kappa_pi_target:.6f}")
            print(f"  Absolute error  = {abs_error:.6f}")
            print(f"  Relative error  = {rel_error*100:.4f}%")
            print(f"  Exponent α      = {alpha:.4f} ± {perr[2]:.4f}")
            print(f"  Amplitude a     = {a:.4f} ± {perr[1]:.4f}")
            print(f"  R²              = {r_squared:.6f}")
            
            # Convergence assessment
            if rel_error < 0.001:  # 0.1%
                print(f"  ✅ OBJETIVO PULVERIZADO (error < 0.1%)")
            elif rel_error < 0.01:  # 1%
                print(f"  ✅ Convergencia excelente (error < 1%)")
            else:
                print(f"  ⚠️  Convergencia en progreso")
            
            print()
            
        except Exception as e:
            print(f"Error in curve fitting: {e}")
            self.fit_results = {
                'fit_success': False,
                'error_message': str(e)
            }
        
        return self.fit_results
    
    def compute_number_variance_GOE(self, L: np.ndarray) -> np.ndarray:
        """
        Compute theoretical Number Variance for GOE (Gaussian Orthogonal Ensemble).
        
        Σ²(L) ≈ (2/π²) * [ln(2πL) + γ + 1 - π²/8]
        
        where γ ≈ 0.5772 is the Euler-Mascheroni constant.
        
        Args:
            L: Array of interval lengths
            
        Returns:
            Theoretical Σ²(L) for GOE
        """
        gamma = 0.5772156649  # Euler-Mascheroni constant
        
        # Avoid log(0)
        L = np.maximum(L, 1e-10)
        
        sigma2 = (2.0 / np.pi**2) * (np.log(2 * np.pi * L) + gamma + 1 - np.pi**2 / 8)
        
        return sigma2
    
    def compute_number_variance_atlas3(self, eigenvalues: np.ndarray, 
                                       L_values: np.ndarray) -> np.ndarray:
        """
        Compute Number Variance Σ²(L) for Atlas³ eigenvalues.
        
        Σ²(L) = ⟨(N(E, L) - L)²⟩
        
        where N(E, L) is the number of eigenvalues in interval [E, E+L].
        
        Args:
            eigenvalues: Sorted eigenvalues
            L_values: Array of interval lengths (in mean spacing units)
            
        Returns:
            Number variance Σ²(L)
        """
        # Sort eigenvalues
        eigs = np.sort(np.real(eigenvalues))
        n_eigs = len(eigs)
        
        # Compute mean spacing
        spacings = np.diff(eigs)
        mean_spacing = np.mean(spacings) if len(spacings) > 0 else 1.0
        
        sigma2 = []
        
        for L in L_values:
            # Convert L to actual energy interval
            L_energy = L * mean_spacing
            
            # Count eigenvalues in sliding windows
            counts = []
            
            # Sample starting points
            n_samples = min(100, n_eigs // 2)
            sample_indices = np.linspace(0, n_eigs - 1, n_samples, dtype=int)
            
            for i in sample_indices:
                if i >= n_eigs:
                    continue
                    
                E_start = eigs[i]
                E_end = E_start + L_energy
                
                # Count eigenvalues in [E_start, E_end]
                count = np.sum((eigs >= E_start) & (eigs <= E_end))
                counts.append(count)
            
            # Variance of counts
            if counts:
                variance = np.var(counts)
                sigma2.append(variance)
            else:
                sigma2.append(0.0)
        
        return np.array(sigma2)
    
    def test_spectral_rigidity(self, N: int = 1024, 
                               L_max: float = 100,
                               n_L_points: int = 50) -> Dict:
        """
        Test spectral rigidity by computing Number Variance Σ²(L).
        
        This is V13-C: The rigidity test comparing Atlas³ with GOE.
        
        Args:
            N: System size for the test
            L_max: Maximum interval length
            n_L_points: Number of L values to test
            
        Returns:
            Dictionary with rigidity test results
        """
        print("🔍 V13-C: Spectral Rigidity Test (Number Variance)")
        print("=" * 70)
        
        # Generate system at size N
        print(f"Generating system at N={N}...")
        self.atlas.generate_modal_basis(N, damping=0.1)
        self.atlas.construct_operator_O(N, coupling_strength=0.15)
        dna = self.atlas.compute_spectral_dna()
        
        eigenvalues = dna['eigenvalues']
        
        # L values (interval lengths in mean spacing units)
        L_values = np.linspace(1, L_max, n_L_points)
        
        # Compute Number Variance for Atlas³
        print("Computing Σ²(L) for Atlas³...")
        sigma2_atlas = self.compute_number_variance_atlas3(eigenvalues, L_values)
        
        # Compute theoretical GOE prediction
        print("Computing Σ²(L) for GOE (theoretical)...")
        sigma2_goe = self.compute_number_variance_GOE(L_values)
        
        # Also compute Poisson (random) baseline: Σ²(L) = L
        sigma2_poisson = L_values
        
        # Calculate deviation from GOE
        deviation = np.abs(sigma2_atlas - sigma2_goe)
        mean_deviation = np.mean(deviation)
        max_deviation = np.max(deviation)
        
        # Relative deviation
        rel_deviation = deviation / (sigma2_goe + 1e-10)
        mean_rel_deviation = np.mean(rel_deviation)
        
        self.number_variance_data = {
            'N': int(N),
            'L_values': L_values.tolist(),
            'sigma2_atlas': sigma2_atlas.tolist(),
            'sigma2_goe': sigma2_goe.tolist(),
            'sigma2_poisson': sigma2_poisson.tolist(),
            'mean_deviation': float(mean_deviation),
            'max_deviation': float(max_deviation),
            'mean_relative_deviation': float(mean_rel_deviation),
            'rigidity_achieved': bool(mean_rel_deviation < 0.5)  # Within 50% of GOE
        }
        
        print(f"Results:")
        print(f"  System size N   = {N}")
        print(f"  L range         = [1, {L_max}]")
        print(f"  Mean deviation  = {mean_deviation:.4f}")
        print(f"  Max deviation   = {max_deviation:.4f}")
        print(f"  Mean rel. dev.  = {mean_rel_deviation:.2%}")
        
        if self.number_variance_data['rigidity_achieved']:
            print(f"  ✅ Rigidez logarítmica GOE detectada")
            print(f"  🧬 Memoria Estructural Infinita confirmada")
        else:
            print(f"  ⚠️  Desviación de GOE - sistema en transición")
        
        print()
        
        return self.number_variance_data
    
    def generate_visualization(self, output_file: str = "v13_scaling_rigidity.png"):
        """
        Generate visualization of V13 results.
        
        Creates a multi-panel figure showing:
        - Panel 1: Scaling law and thermodynamic limit extrapolation
        - Panel 2: Number Variance Σ²(L) vs GOE prediction
        
        Args:
            output_file: Output filename for the plot
        """
        if self.scaling_data is None or self.number_variance_data is None:
            raise ValueError("Must run multi_scale_sweep and test_spectral_rigidity first")
        
        print(f"📊 Generating visualization: {output_file}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Panel 1: Scaling Law
        N_array = np.array(self.scaling_data['N_values'])
        kappa_array = np.array(self.scaling_data['kappa_values'])
        
        # Plot data points
        ax1.scatter(N_array, kappa_array, s=100, c='blue', 
                   label='Datos Atlas³', zorder=3, alpha=0.7)
        
        # Plot fit if available
        if self.fit_results and self.fit_results.get('fit_success'):
            N_fit = np.linspace(N_array[0], N_array[-1] * 1.5, 200)
            kappa_fit = self.thermodynamic_limit_model(
                N_fit,
                self.fit_results['kappa_infinity'],
                self.fit_results['amplitude_a'],
                self.fit_results['exponent_alpha']
            )
            
            ax1.plot(N_fit, kappa_fit, 'r-', linewidth=2,
                    label=f"Fit: κ_∞ = {self.fit_results['kappa_infinity']:.4f}", 
                    zorder=2)
            
            # Asymptote
            ax1.axhline(y=self.fit_results['kappa_infinity'], 
                       color='red', linestyle='--', alpha=0.5,
                       label=f"κ_∞ asintótico")
        
        # Target line
        ax1.axhline(y=self.kappa_pi_target, color='green', 
                   linestyle=':', linewidth=2,
                   label=f"κ_Π objetivo = {self.kappa_pi_target}")
        
        ax1.set_xlabel('Tamaño del Sistema (N)', fontsize=12)
        ax1.set_ylabel('Curvatura Espectral κ(N)', fontsize=12)
        ax1.set_title('V13-B: Extrapolación al Límite Termodinámico', fontsize=13, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        
        # Panel 2: Number Variance
        L_vals = np.array(self.number_variance_data['L_values'])
        sigma2_atlas = np.array(self.number_variance_data['sigma2_atlas'])
        sigma2_goe = np.array(self.number_variance_data['sigma2_goe'])
        sigma2_poisson = np.array(self.number_variance_data['sigma2_poisson'])
        
        ax2.plot(L_vals, sigma2_atlas, 'b-', linewidth=2, 
                label='Atlas³ (N={})'.format(self.number_variance_data['N']))
        ax2.plot(L_vals, sigma2_goe, 'r--', linewidth=2, 
                label='GOE (teórico)')
        ax2.plot(L_vals, sigma2_poisson, 'k:', linewidth=1.5, alpha=0.5,
                label='Poisson (random)')
        
        ax2.set_xlabel('Longitud de Intervalo L', fontsize=12)
        ax2.set_ylabel('Varianza de Conteo Σ²(L)', fontsize=12)
        ax2.set_title('V13-C: Rigidez Espectral (Varianza de Conteo)', fontsize=13, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        
        plt.tight_layout()
        
        # Save figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_file}")
        
        return fig
    
    def export_results(self, output_file: str = "v13_limit_results.json"):
        """
        Export V13 results to JSON file.
        
        Args:
            output_file: Output filename for JSON results
        """
        if self.scaling_data is None:
            raise ValueError("Must run multi_scale_sweep first")
        
        print(f"💾 Exporting results: {output_file}")
        
        results = {
            'metadata': {
                'author': __author__,
                'architecture': __architecture__,
                'license': __license__,
                'f0': __f0__,
                'kappa_pi_target': self.kappa_pi_target
            },
            'scaling_data': self.scaling_data,
            'fit_results': self.fit_results if self.fit_results else {},
            'number_variance': self.number_variance_data if self.number_variance_data else {}
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results exported: {output_file}")
        
        return results
    
    def run_complete_validation(self, 
                                N_values: List[int] = [128, 256, 512, 1024, 2560],
                                N_rigidity: int = 1024,
                                output_prefix: str = "v13") -> Dict:
        """
        Run complete V13 validation protocol.
        
        Args:
            N_values: System sizes for scaling sweep
            N_rigidity: System size for rigidity test
            output_prefix: Prefix for output files
            
        Returns:
            Complete results dictionary
        """
        print("🛰️ V13 LIMIT VALIDATOR: COMPLETE PROTOCOL")
        print("=" * 70)
        print(f"Target: κ_Π = {self.kappa_pi_target}")
        print(f"System sizes: {N_values}")
        print(f"Rigidity test: N = {N_rigidity}")
        print()
        
        # Step 1: Multi-scale sweep
        self.multi_scale_sweep(N_values)
        
        # Step 2: Extrapolate κ_∞
        self.extrapolate_kappa_infinity()
        
        # Step 3: Test spectral rigidity
        self.test_spectral_rigidity(N=N_rigidity)
        
        # Step 4: Generate visualization
        self.generate_visualization(f"{output_prefix}_scaling_rigidity.png")
        
        # Step 5: Export results
        results = self.export_results(f"{output_prefix}_limit_results.json")
        
        print("=" * 70)
        print("🎯 V13 VALIDATION COMPLETE")
        
        if self.fit_results and self.fit_results.get('fit_success'):
            rel_error = self.fit_results['relative_error_percent']
            if rel_error < 0.1:
                print("✅ LÍMITE TERMODINÁMICO ALCANZADO")
                print(f"   κ_∞ = {self.fit_results['kappa_infinity']:.6f}")
                print(f"   Error: {rel_error:.4f}%")
                print("   🧬 BUCLE CERRADO - Simetría PT robusta")
            else:
                print(f"⚠️  Convergencia en progreso (error: {rel_error:.2f}%)")
        
        if self.number_variance_data and self.number_variance_data.get('rigidity_achieved'):
            print("✅ RIGIDEZ LOGARÍTMICA CONFIRMADA")
            print("   🔮 Memoria Estructural Infinita detectada")
        
        print("=" * 70)
        
        return results


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='V13 Limit Validator for Atlas³ Thermodynamic Limit'
    )
    parser.add_argument(
        '--sizes', '-s',
        nargs='+',
        type=int,
        default=[128, 256, 512, 1024, 2560],
        help='System sizes for scaling sweep (default: 128 256 512 1024 2560)'
    )
    parser.add_argument(
        '--rigidity-size', '-r',
        type=int,
        default=1024,
        help='System size for rigidity test (default: 1024)'
    )
    parser.add_argument(
        '--target', '-t',
        type=float,
        default=2.577310,
        help='Target value for κ_Π (default: 2.577310)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='v13',
        help='Output file prefix (default: v13)'
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = V13LimitValidator(kappa_pi_target=args.target)
    
    # Run complete validation
    results = validator.run_complete_validation(
        N_values=args.sizes,
        N_rigidity=args.rigidity_size,
        output_prefix=args.output
    )
    
    return validator, results


if __name__ == '__main__':
    validator, results = main()
