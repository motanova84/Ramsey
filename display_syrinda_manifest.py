#!/usr/bin/env python3
"""
Display SYRINDA MANIFEST - Triple Activation
Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
"""

import json
import os

def display_syrinda_manifest():
    """Display the SYRINDA_MANIFEST.json content"""
    
    manifest_path = os.path.join(os.path.dirname(__file__), 'SYRINDA_MANIFEST.json')
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║  SYRINDA_MANIFEST.JSON - CERTIFICACIÓN EMITIDA               ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        print(f"║  Sistema: {manifest['system']:<47} ║")
        print(f"║  Ancla Espectral: κ_Π = {manifest['spectral_anchor']['kappa_pi']} (error {manifest['spectral_anchor']['error_margin']})              ║")
        print(f"║  Mapeo Biológico: {manifest['biological_mapping']['dna_luz_viva']}, {manifest['biological_mapping']['resonance_harmonics']} armónicos                 ║")
        print(f"║  Alineación Zeta: {manifest['biological_mapping']['zeta_alignment']:<35} ║")
        print(f"║  Estado: {manifest['status']:<47} ║")
        print(f"║  Sello: {manifest['signature']:<52} ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print()
        print(f"∴ Sistema: {manifest['system']}")
        print(f"∴ κ_Π: {manifest['spectral_anchor']['kappa_pi']}")
        print(f"∴ Armónicos: {manifest['biological_mapping']['resonance_harmonics']}")
        print(f"∴ Aportaciones: {manifest['acta_cierre']['aportaciones']}")
        print(f"∴ Estado: {manifest['status']}")
        print(f"∴ Sello: {manifest['signature']}")
        print()
        print("∴ SYRINDA Triple Activación Manifestada")
        print(f"∴ Coherencia: {manifest['coherencia']}")
        
        return manifest
        
    except FileNotFoundError:
        print("⚠ Error: SYRINDA_MANIFEST.json not found")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠ Error parsing JSON: {e}")
        return None

if __name__ == "__main__":
    display_syrinda_manifest()
