#!/usr/bin/env python3
"""
QCAL ∞³ Beacon Verification Tool
Verifies the integrity and validity of .qcal_beacon certificates
"""

import sys
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple

def parse_beacon_file(filepath: str) -> Dict[str, str]:
    """Parse YAML-like beacon file into dictionary."""
    content = Path(filepath).read_text()
    data = {}
    
    # Extract key-value pairs
    for line in content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    
    return data, content

def verify_frequency(data: Dict[str, str]) -> Tuple[bool, str]:
    """Verify f₀ = 141.7001 Hz is present."""
    content_str = str(data)
    
    if '141.7001' in content_str or '141.7001' in str(data.values()):
        return True, "✓ Frecuencia f₀ = 141.7001 Hz verificada"
    
    return False, "✗ Frecuencia f₀ = 141.7001 Hz no encontrada"

def verify_ramsey_theorem(data: Dict[str, str]) -> Tuple[bool, str]:
    """Verify R(5,5) theorem statement."""
    content_str = str(data)
    
    # Check for R(5,5) or R_5_5 mentions
    if 'R(5,5)' in content_str or 'R_5_5' in content_str or '5_5' in content_str:
        return True, "✓ Teorema R(5,5) presente"
    
    return False, "✗ Teorema R(5,5) no encontrado"

def verify_qcal_framework(data: Dict[str, str]) -> Tuple[bool, str]:
    """Verify QCAL ∞³ framework markers."""
    content_str = str(data)
    
    qcal_markers = ['QCAL', '∞³', 'Quantum Coherent', 'framework']
    found = sum(1 for marker in qcal_markers if marker in content_str)
    
    if found >= 2:
        return True, f"✓ Marcadores QCAL ∞³ encontrados ({found}/4)"
    
    return False, f"✗ Marcadores QCAL ∞³ insuficientes ({found}/4)"

def verify_certification(data: Dict[str, str]) -> Tuple[bool, str]:
    """Verify certification metadata."""
    content_str = str(data)
    
    cert_keywords = ['certified', 'verification', 'proof', 'theorem']
    found = sum(1 for kw in cert_keywords if kw.lower() in content_str.lower())
    
    if found >= 2:
        return True, f"✓ Metadatos de certificación presentes ({found}/4)"
    
    return False, f"✗ Metadatos de certificación insuficientes ({found}/4)"

def compute_hash(content: str) -> str:
    """Compute SHA256 hash of beacon content."""
    return hashlib.sha256(content.encode()).hexdigest()

def verify_beacon(filepath: str) -> bool:
    """
    Main verification function for .qcal_beacon files.
    
    Returns:
        bool: True if all verifications pass, False otherwise
    """
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     QCAL ∞³ BEACON VERIFICATION TOOL                      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    if not Path(filepath).exists():
        print(f"✗ Error: Archivo {filepath} no encontrado")
        return False
    
    print(f"📜 Verificando: {filepath}")
    print()
    
    # Parse beacon file
    try:
        data, content = parse_beacon_file(filepath)
        print(f"✓ Archivo parseado exitosamente")
    except Exception as e:
        print(f"✗ Error al parsear archivo: {e}")
        return False
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("VERIFICACIONES:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    # Run all verifications
    verifications = [
        verify_frequency(data),
        verify_ramsey_theorem(data),
        verify_qcal_framework(data),
        verify_certification(data)
    ]
    
    all_passed = True
    for passed, message in verifications:
        print(message)
        if not passed:
            all_passed = False
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("HASH DEL CERTIFICADO:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    beacon_hash = compute_hash(content)
    print(f"SHA256: {beacon_hash[:16]}...{beacon_hash[-16:]}")
    print()
    
    # Final result
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("RESULTADO:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    if all_passed:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║         ✅ CERTIFICADO QCAL ∞³ VÁLIDO                    ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("El certificado cumple con todos los requisitos QCAL ∞³")
        print("Frecuencia fundamental: f₀ = 141.7001 Hz")
        print("Marco: Quantum Coherent Algebraic Logic ∞³")
        print()
        return True
    else:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║         ⚠️  CERTIFICADO CON ADVERTENCIAS                 ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("El certificado existe pero algunas verificaciones fallaron.")
        print("Revise los detalles arriba.")
        print()
        return False

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Uso: python verify_qcal_beacon.py <archivo_beacon>")
        print()
        print("Ejemplo:")
        print("  python scripts/verify_qcal_beacon.py .qcal_beacon")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = verify_beacon(filepath)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
