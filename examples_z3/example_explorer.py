"""
Explorer Example: Automatic Parameter Space Exploration

This example shows how to use the automatic explorer to scan multiple
parameter combinations and generate comprehensive results.
"""

import sys
sys.path.insert(0, '..')

from ramsey_z3_verification import (
    explore_parameters,
    save_results_to_csv,
    generate_results_table
)


def example_1_small_exploration():
    """Example 1: Small parameter space exploration"""
    print("=" * 70)
    print("EXAMPLE 1: Small Parameter Space")
    print("=" * 70)
    print("\nExploring a small parameter space:\n")
    
    results = explore_parameters(
        r_values=[3, 4],
        s_values=[3, 4],
        eps_values=[0.2],
        M=1000,
        nmax=12
    )
    
    # Display results table
    generate_results_table(results)
    
    # Save to CSV
    save_results_to_csv(results, 'results_small.csv')
    
    return results


def example_2_epsilon_range():
    """Example 2: Explore epsilon range for fixed (r,s)"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Epsilon Range Exploration")
    print("=" * 70)
    print("\nExploring epsilon values for (3,3):\n")
    
    results = explore_parameters(
        r_values=[3],
        s_values=[3],
        eps_values=[0.15, 0.2, 0.25, 0.3],
        M=1000,
        nmax=12
    )
    
    # Display results
    generate_results_table(results)
    
    # Save to CSV
    save_results_to_csv(results, 'results_epsilon_range.csv')
    
    return results


def example_3_systematic_scan():
    """Example 3: Systematic scan of (r,s) pairs"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Systematic (r,s) Scan")
    print("=" * 70)
    print("\nScanning multiple (r,s) combinations:\n")
    
    results = explore_parameters(
        r_values=[3, 4, 5],
        s_values=[3, 4, 5],
        eps_values=[0.2, 0.25],
        M=1000,
        nmax=15
    )
    
    # Display results
    generate_results_table(results)
    
    # Save to CSV
    save_results_to_csv(results, 'results_systematic.csv')
    
    # Print summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    valid_results = [r for r in results if r['R_psi'] is not None]
    if valid_results:
        import numpy as np
        R_psi_values = [r['R_psi'] for r in valid_results]
        times = [r['duration_seconds'] for r in valid_results]
        
        print(f"\nTotal computations: {len(results)}")
        print(f"Successful: {len(valid_results)}")
        print(f"Failed: {len(results) - len(valid_results)}")
        print(f"\nR_psi range: [{min(R_psi_values)}, {max(R_psi_values)}]")
        print(f"Average R_psi: {np.mean(R_psi_values):.2f}")
        print(f"\nTotal computation time: {sum(times):.2f}s")
        print(f"Average time per case: {np.mean(times):.2f}s")
    
    return results


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RAMSEY Z3 VERIFICATION: EXPLORER EXAMPLES")
    print("=" * 70)
    
    # Run examples
    # Uncomment the example you want to run
    
    # Example 1: Quick exploration
    example_1_small_exploration()
    
    # Example 2: Epsilon sensitivity (faster)
    # example_2_epsilon_range()
    
    # Example 3: Comprehensive scan (slower, comment out for quick test)
    # example_3_systematic_scan()
    
    print("\n" + "=" * 70)
    print("✓ Explorer examples completed!")
    print("  Check the generated CSV files for detailed results")
    print("=" * 70 + "\n")
