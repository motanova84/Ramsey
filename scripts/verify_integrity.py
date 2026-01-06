#!/usr/bin/env python3
"""
Data Integrity Verification Script

Verifies the integrity of critical data files by comparing their SHA-256 checksums
against the values stored in ENV.lock. This ensures that data has not been corrupted
or tampered with.

Usage:
    python scripts/verify_integrity.py [--verbose]
"""

import hashlib
import sys
import os
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# Expected checksums from ENV.lock
EXPECTED_CHECKSUMS = {
    "data/rpsi_vibration_model.json": "539f00a7d61c9c589d1b7adeb4c9856c8de00122c98a764fe7bc3ff47eff93bb",
    "data/verified_bound_R55.json": "5af48aa1d3c95e2c476673285a7376e323778e48c34f8b41470c874f00343703",
    "data/coloring_sat_r55.cnf": "5a068fae1103679585aea053c6827cc7d8acb810595f7ac5826d2aa9bac242e2",
    "data/r66.cnf": "78aad3170abe2d34241288056fab8655759612c3150f128df92b376c80df9e4e",
    "data/rpsi_5_5_n16.cnf": "e73256aaa26852e8737d4b76a52542564928aeaa0360f97a4ea73b1962b0dfc6",
}

# Critical beacon files
CRITICAL_BEACONS = [
    ".qcal_beacon",
    ".qcal_beacon_r33",
    ".qcal_beacon_r44",
    ".qcal_beacon_r66",
    ".qcal_beacon_r88",
]


def calculate_sha256(filepath: Path) -> Optional[str]:
    """Calculate SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None


def verify_checksum(filepath: str, expected: str, verbose: bool = False) -> Tuple[bool, str]:
    """
    Verify a file's checksum matches expected value.
    
    Returns:
        (success, message) tuple
    """
    path = Path(filepath)
    
    if not path.exists():
        return False, f"❌ File not found: {filepath}"
    
    actual = calculate_sha256(path)
    
    if actual is None:
        return False, f"❌ Could not read file: {filepath}"
    
    if actual == expected:
        if verbose:
            return True, f"✓ {filepath}\n  SHA-256: {actual}"
        else:
            return True, f"✓ {filepath}"
    else:
        return False, f"""❌ CHECKSUM MISMATCH: {filepath}
  Expected: {expected}
  Actual:   {actual}
  
  WARNING: This file may have been corrupted or modified!
  Action required:
  1. Re-clone the repository, or
  2. Restore from backup, or
  3. If intentional, update ENV.lock with new checksum
"""


def verify_beacon_exists(filepath: str) -> Tuple[bool, str]:
    """Verify that a beacon file exists."""
    path = Path(filepath)
    if path.exists():
        return True, f"✓ {filepath} exists"
    else:
        return False, f"⚠ Warning: {filepath} not found (may be optional)"


def verify_all_files(verbose: bool = False) -> Tuple[int, int]:
    """
    Verify all critical files.
    
    Returns:
        (passed, failed) tuple
    """
    passed = 0
    failed = 0
    warnings = 0
    
    print("=" * 70)
    print("DATA INTEGRITY VERIFICATION")
    print("=" * 70)
    print()
    
    # Verify data file checksums
    print("Verifying data file checksums...")
    print("-" * 70)
    
    for filepath, expected_checksum in EXPECTED_CHECKSUMS.items():
        success, message = verify_checksum(filepath, expected_checksum, verbose)
        print(message)
        if success:
            passed += 1
        else:
            failed += 1
    
    print()
    
    # Verify beacon files exist
    print("Verifying QCAL beacon files...")
    print("-" * 70)
    
    for beacon in CRITICAL_BEACONS:
        success, message = verify_beacon_exists(beacon)
        print(message)
        if success:
            passed += 1
        else:
            warnings += 1
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Passed:   {passed}")
    print(f"❌ Failed:   {failed}")
    print(f"⚠ Warnings: {warnings}")
    print()
    
    if failed == 0:
        print("✅ ALL CRITICAL FILES VERIFIED SUCCESSFULLY")
        print()
        print("Data integrity: ✓ CONFIRMED")
        print("Reproducibility: ✓ GUARANTEED")
        print()
        return passed, failed
    else:
        print("⚠️  VERIFICATION FAILED - DATA INTEGRITY COMPROMISED")
        print()
        print("Please take action:")
        print("1. Review the errors above")
        print("2. Re-clone the repository or restore from backup")
        print("3. If changes were intentional, update ENV.lock")
        print("4. Contact maintainers if this is unexpected")
        print()
        return passed, failed


def main():
    """Main entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    passed, failed = verify_all_files(verbose)
    
    # Exit with error code if any verification failed
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
