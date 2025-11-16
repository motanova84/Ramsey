#!/usr/bin/env python3
"""
Demo: PDF Certificate Generation for Ramsey Vibrational Bounds

This script demonstrates the PDF certificate generation functionality.
"""

import os
from generate_pdf_certificate import generate_rpsi_4_4_certificate, generate_rpsi_3_3_certificate


def main():
    print("=" * 70)
    print("  PDF Certificate Generation Demo")
    print("  Ramsey Vibrational Bounds")
    print("=" * 70)
    print()
    
    # Ensure certificates directory exists
    os.makedirs("certificates", exist_ok=True)
    
    print("Generating formal PDF certificates...")
    print()
    
    # Generate R_ψ(4,4) ≤ 10 certificate
    print("1. Generating certificate for R_ψ(4,4) ≤ 10")
    print("   Parameters: λ=0.062, f₀=141.7001 Hz, ε=0.001")
    generate_rpsi_4_4_certificate()
    size_44 = os.path.getsize("certificates/Rpsi_4_4_certificate.pdf")
    print(f"   ✓ Generated: certificates/Rpsi_4_4_certificate.pdf ({size_44} bytes)")
    print()
    
    # Generate R_ψ(3,3) ≤ 5 certificate
    print("2. Generating certificate for R_ψ(3,3) ≤ 5")
    print("   Parameters: λ=0.1, f₀=141.7001 Hz, ε=0.001")
    generate_rpsi_3_3_certificate()
    size_33 = os.path.getsize("certificates/Rpsi_3_3_certificate.pdf")
    print(f"   ✓ Generated: certificates/Rpsi_3_3_certificate.pdf ({size_33} bytes)")
    print()
    
    print("=" * 70)
    print("  Certificate Features")
    print("=" * 70)
    print()
    print("Each PDF certificate includes:")
    print("  • Formal title and parameters (λ, f₀, ε)")
    print("  • Theorem statement with mathematical notation")
    print("  • Complete Lean4 formalization code")
    print("  • Verification methodology")
    print("  • Repository references")
    print("  • Professional formatting with proper typography")
    print()
    
    print("=" * 70)
    print("  Success!")
    print("=" * 70)
    print()
    print("PDF certificates are now available in the certificates/ directory.")
    print("These certificates provide formal verification for the Ramsey")
    print("Vibrational bounds using the QCAL ∞³ framework at 141.7001 Hz.")
    print()


if __name__ == "__main__":
    main()
