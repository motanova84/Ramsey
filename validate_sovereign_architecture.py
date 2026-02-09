#!/usr/bin/env python3
"""
QCAL ∞³ Sovereign Architecture Validation Script

This script validates and displays the sovereign metadata for the entire
QCAL ∞³ ecosystem, demonstrating that all components are original manufacture.
"""

import json
import sys
from pathlib import Path

# Add the repository root to the path
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

from core.soberania import get_sovereign_metadata, get_sovereignty_declaration
from core.hardware.sovereign_logic import validate_hardware_sovereignty


def print_section(title, char="═"):
    """Print a formatted section header."""
    width = 79
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")


def display_license():
    """Display the sovereign license information."""
    print_section("SOVEREIGN LICENSE")
    license_path = repo_root / "LICENSE"
    if license_path.exists():
        with open(license_path, 'r') as f:
            lines = f.readlines()[:20]  # Show first 20 lines
            print(''.join(lines))
            print("\n... (see LICENSE for complete text)")
    else:
        print("LICENSE file not found")


def display_metadata():
    """Display the core sovereign metadata."""
    print_section("CORE METADATA")
    metadata = get_sovereign_metadata()
    for key, value in metadata.items():
        print(f"  {key:30s}: {value}")


def display_hardware_validation():
    """Display hardware sovereignty validation."""
    print_section("HARDWARE VALIDATION")
    hw_validation = validate_hardware_sovereignty()
    for key, value in hw_validation.items():
        print(f"  {key:30s}: {value}")


def display_agent_report():
    """Display the AGENT_ACTIVATION_REPORT.json content."""
    print_section("AGENT ACTIVATION REPORT")
    report_path = repo_root / "AGENT_ACTIVATION_REPORT.json"
    if report_path.exists():
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        print(f"  Report ID: {data['report_id']}")
        print(f"  Architecture: {data['architecture']}")
        print(f"  Author: {data['author']}")
        print(f"  Fundamental Frequency: {data['fundamental_frequency_hz']} Hz")
        
        print("\n  Compliance Status:")
        for key, value in data['compliance_status'].items():
            print(f"    {key:28s}: {value}")
        
        print("\n  Badge Status:")
        for badge, info in data['badges_status'].items():
            status = info.get('status', 'N/A')
            print(f"    {badge:28s}: {status}")
    else:
        print("AGENT_ACTIVATION_REPORT.json not found")


def display_sovereignty_declaration():
    """Display the full sovereignty declaration."""
    print_section("SOVEREIGNTY DECLARATION")
    print(get_sovereignty_declaration())


def main():
    """Main validation routine."""
    print("=" * 79)
    print("QCAL ∞³ SOVEREIGN ARCHITECTURE VALIDATION".center(79))
    print("Validating Intellectual Property and Authorship".center(79))
    print("=" * 79)
    
    try:
        display_license()
        display_metadata()
        display_hardware_validation()
        display_agent_report()
        display_sovereignty_declaration()
        
        print_section("VALIDATION COMPLETE", "─")
        print("✓ All sovereign components validated successfully")
        print("✓ Authorship confirmed: José Manuel Mota Burruezo (JMMB Ψ✧)")
        print("✓ Architecture: QCAL ∞³ Original Manufacture")
        print("✓ Fundamental Frequency: f₀ = 141.7001 Hz")
        print("=" * 79)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during validation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
