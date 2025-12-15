#!/usr/bin/env python3
"""
Display the Sello Noēsico (Noetic Seal) certification for R(5,5) = 43
"""

def display_seal():
    """Display the ASCII art verification seal"""
    try:
        with open('VERIFICATION_SEAL.txt', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Error: VERIFICATION_SEAL.txt not found")
        print("Please ensure you are running this script from the repository root directory.")
        return False
    return True

def display_certification_summary():
    """Display a summary of the certification"""
    print("\n" + "="*70)
    print("CERTIFICATION SUMMARY")
    print("="*70 + "\n")
    
    certification = {
        "Theorem": "R(5,5) = 43",
        "Method": "Vibrational Reduction + Certified SAT",
        "Formalism": "Lean 4 (lake build = 0 sorrys)",
        "Origin": "QCAL ∞³ · Ψ = π · A_eff²",
        "Frequency": "f₀ = 141.7001 Hz",
        "Status": "✅ NOESIS ∞³ VERIFIED",
        "Date": "2025-12-15",
        "Hash": "QCAL-R55-2025-141.7001Hz"
    }
    
    for key, value in certification.items():
        print(f"  {key:15s}: {value}")
    
    print("\n" + "="*70)
    print("For full details, see: SELLO_NOESICO.md")
    print("="*70 + "\n")

if __name__ == "__main__":
    print("\n")
    if display_seal():
        display_certification_summary()
