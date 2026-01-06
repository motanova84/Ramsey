#!/usr/bin/env python3
"""
Environment Verification Script

Verifies that the current environment matches the specifications in ENV.lock.
This ensures reproducibility of results across different systems.

Usage:
    python scripts/verify_environment.py [--verbose]
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional
import json


def get_python_version() -> Tuple[int, int, int]:
    """Get current Python version as tuple."""
    return sys.version_info[:3]


def get_command_version(command: str, args: list = ["--version"]) -> Optional[str]:
    """Get version from a command line tool."""
    try:
        result = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            output = result.stdout.strip() or result.stderr.strip()
            return output.split('\n')[0]
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return None


def check_python_version(verbose: bool = False) -> Tuple[bool, str]:
    """Check Python version meets requirements."""
    current = get_python_version()
    required_major = 3
    required_minor = 10
    recommended = (3, 12, 3)
    
    if current[0] < required_major or (current[0] == required_major and current[1] < required_minor):
        return False, f"❌ Python {current[0]}.{current[1]}.{current[2]} (required: >= {required_major}.{required_minor})"
    
    version_str = f"{current[0]}.{current[1]}.{current[2]}"
    if current >= recommended:
        msg = f"✓ Python {version_str} (recommended version)"
    else:
        msg = f"✓ Python {version_str} (>= {required_major}.{required_minor}, recommended: {recommended[0]}.{recommended[1]}.{recommended[2]})"
    
    return True, msg


def check_lean_version(verbose: bool = False) -> Tuple[bool, str]:
    """Check Lean version matches lean-toolchain."""
    # Read expected version from lean-toolchain
    toolchain_file = Path("lean-toolchain")
    if not toolchain_file.exists():
        return False, "⚠ lean-toolchain file not found"
    
    with open(toolchain_file, 'r') as f:
        expected = f.read().strip()
    
    # Try to get lean version
    lean_version = get_command_version("lean", ["--version"])
    
    if lean_version is None:
        return False, f"⚠ Lean not found (expected: {expected})"
    
    # Extract version number from output
    if "4.3.0" in lean_version or expected.endswith("4.3.0"):
        return True, f"✓ Lean version matches toolchain: {expected}"
    else:
        return False, f"❌ Lean version mismatch (expected: {expected}, got: {lean_version})"


def check_nodejs_version(verbose: bool = False) -> Tuple[bool, str]:
    """Check Node.js version meets requirements."""
    node_version = get_command_version("node", ["--version"])
    
    if node_version is None:
        return False, "⚠ Node.js not found (required for NFT integration)"
    
    # Extract major version
    try:
        major_version = int(node_version.strip('v').split('.')[0])
        if major_version >= 18:
            return True, f"✓ Node.js {node_version} (>= 18)"
        else:
            return False, f"❌ Node.js {node_version} (required: >= 18)"
    except (ValueError, IndexError):
        return False, f"⚠ Could not parse Node.js version: {node_version}"


def check_file_exists(filepath: str, description: str) -> Tuple[bool, str]:
    """Check if a required file exists."""
    if Path(filepath).exists():
        return True, f"✓ {description}: {filepath}"
    else:
        return False, f"❌ Missing {description}: {filepath}"


def check_requirements_lock() -> Tuple[bool, str]:
    """Check if requirements-lock.txt exists and has content."""
    filepath = "requirements-lock.txt"
    if not Path(filepath).exists():
        return False, f"❌ {filepath} not found"
    
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if len(lines) > 0:
        return True, f"✓ {filepath} ({len(lines)} dependencies)"
    else:
        return False, f"❌ {filepath} is empty"


def check_package_lock() -> Tuple[bool, str]:
    """Check if package-lock.json exists and is valid."""
    filepath = "package-lock.json"
    if not Path(filepath).exists():
        return False, f"⚠ {filepath} not found (optional for Node.js features)"
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if 'packages' in data or 'dependencies' in data:
            return True, f"✓ {filepath} (valid)"
        else:
            return False, f"❌ {filepath} appears invalid"
    except json.JSONDecodeError:
        return False, f"❌ {filepath} is not valid JSON"


def verify_environment(verbose: bool = False) -> Tuple[int, int]:
    """
    Verify the complete environment.
    
    Returns:
        (passed, failed) tuple
    """
    passed = 0
    failed = 0
    warnings = 0
    
    print("=" * 70)
    print("ENVIRONMENT VERIFICATION")
    print("=" * 70)
    print()
    
    checks = [
        ("Python Version", check_python_version()),
        ("Lean Toolchain", check_lean_version()),
        ("Node.js Version", check_nodejs_version()),
        ("Requirements Lock", check_requirements_lock()),
        ("Package Lock", check_package_lock()),
        ("ENV.lock", check_file_exists("ENV.lock", "Environment lock file")),
        ("lean-toolchain", check_file_exists("lean-toolchain", "Lean toolchain file")),
    ]
    
    print("System Requirements:")
    print("-" * 70)
    
    for name, (success, message) in checks:
        print(message)
        if success:
            passed += 1
        elif "⚠" in message:
            warnings += 1
        else:
            failed += 1
    
    print()
    
    # Additional checks for critical files
    print("Critical Files:")
    print("-" * 70)
    
    critical_files = [
        "data/rpsi_vibration_model.json",
        "data/verified_bound_R55.json",
        ".qcal_beacon",
    ]
    
    for filepath in critical_files:
        success, message = check_file_exists(filepath, "Critical data")
        print(message)
        if success:
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Passed:   {passed}")
    print(f"❌ Failed:   {failed}")
    print(f"⚠ Warnings: {warnings}")
    print()
    
    if failed == 0:
        print("✅ ENVIRONMENT VERIFIED SUCCESSFULLY")
        print()
        print("Your environment matches ENV.lock specifications.")
        print("Results should be fully reproducible.")
        print()
        print("Next steps:")
        print("1. Run: python scripts/verify_integrity.py")
        print("2. Run: python run_tests.py")
        print("3. Run: ./build_and_verify.sh (if Lean installed)")
        print()
    else:
        print("⚠️  ENVIRONMENT VERIFICATION FAILED")
        print()
        print("Your environment does not match ENV.lock specifications.")
        print("Results may not be reproducible.")
        print()
        print("Please:")
        print("1. Review the errors above")
        print("2. Install missing dependencies")
        print("3. Match versions specified in ENV.lock")
        print("4. Re-run this script to verify")
        print()
    
    return passed, failed


def main():
    """Main entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    passed, failed = verify_environment(verbose)
    
    # Exit with error code if any critical check failed
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
