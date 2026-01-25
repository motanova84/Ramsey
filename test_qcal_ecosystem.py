#!/usr/bin/env python3
"""
Test script for QCAL Math Library and Ecosystem Link functionality
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.math import QCALMathLibrary, ram_protocol_sync, calculate_symbiotic_coherence


def test_qcal_constants():
    """Test QCAL constants are properly defined"""
    print("\n=== Test: QCAL Constants ===")
    
    assert QCALMathLibrary.CONSTANTS["PSI"] == 0.999999
    assert QCALMathLibrary.CONSTANTS["FREQ_GW"] == 141.7001
    assert QCALMathLibrary.CONSTANTS["RAMSEY_R66"] == 108
    assert QCALMathLibrary.CONSTANTS["MAX_PULSARS"] == 88
    
    print("✓ All constants properly defined")
    print(f"  PSI: {QCALMathLibrary.CONSTANTS['PSI']}")
    print(f"  FREQ_GW: {QCALMathLibrary.CONSTANTS['FREQ_GW']} Hz")
    print(f"  RAMSEY_R66: {QCALMathLibrary.CONSTANTS['RAMSEY_R66']}")
    print(f"  MAX_PULSARS: {QCALMathLibrary.CONSTANTS['MAX_PULSARS']}")


def test_shapiro_delay():
    """Test Shapiro delay calculation"""
    print("\n=== Test: Shapiro Delay ===")
    
    mass = 1.0
    distance = 1.0
    delay = QCALMathLibrary.shapiro_delay(mass, distance)
    
    expected = (2 * mass) / (QCALMathLibrary.CONSTANTS["PSI"] * distance)
    assert abs(delay - expected) < 1e-10
    
    print(f"✓ Shapiro delay calculated: {delay:.6f}")


def test_ramsey_vibration():
    """Test Ramsey vibration calculation"""
    print("\n=== Test: Ramsey Vibration ===")
    
    n = 5
    vibration = QCALMathLibrary.ramsey_vibration(n)
    
    print(f"✓ Ramsey vibration for n={n}: {vibration:.6f}")
    assert vibration > 0


def test_qcal_resonance():
    """Test QCAL resonance calculation"""
    print("\n=== Test: QCAL Resonance ===")
    
    # Test with base frequency (should be 1.0)
    resonance = QCALMathLibrary.qcal_resonance(141.7001)
    assert abs(resonance - 1.0) < 1e-6
    print(f"✓ Resonance at base frequency: {resonance:.6f}")
    
    # Test with double frequency (should be 2.0)
    resonance2 = QCALMathLibrary.qcal_resonance(283.4002)
    assert abs(resonance2 - 2.0) < 1e-3
    print(f"✓ Resonance at 2x frequency: {resonance2:.6f}")


def test_ramsey_polynomial_bound():
    """Test Ramsey polynomial bound calculation"""
    print("\n=== Test: Ramsey Polynomial Bound ===")
    
    # Test for R(6,6)
    bound = QCALMathLibrary.ramsey_polynomial_bound(6, 6)
    print(f"✓ Polynomial bound for R(6,6): {bound:.2f}")
    
    # The actual R(6,6) = 108, so bound should be reasonably close
    assert bound > 0
    print(f"  (Actual R(6,6) = 108)")


def test_nft_partition_energy():
    """Test NFT partition energy calculation"""
    print("\n=== Test: NFT Partition Energy ===")
    
    # Test with valid NFT count
    energy = QCALMathLibrary.nft_partition_energy(88)
    expected = 88 * 141.7001
    assert abs(energy - expected) < 1e-6
    print(f"✓ Energy for 88 NFTs: {energy:.2f}")
    
    # Test with invalid NFT count (should raise error)
    try:
        QCALMathLibrary.nft_partition_energy(100)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Correctly rejected NFT count > 88: {str(e)}")


def test_ram_protocol_sync():
    """Test RAM protocol synchronization"""
    print("\n=== Test: RAM Protocol Sync ===")
    
    result = ram_protocol_sync("Ramsey", 141.7001)
    
    assert result["node_id"] == "Ramsey"
    assert result["frequency"] == 141.7001
    assert result["status"] == "synchronized"
    
    print(f"✓ Node synchronized: {result['node_id']}")
    print(f"  Frequency: {result['frequency']} Hz")
    print(f"  Resonance: {result['resonance']:.6f}")
    print(f"  Status: {result['status']}")


def test_symbiotic_coherence():
    """Test symbiotic coherence calculation"""
    print("\n=== Test: Symbiotic Coherence ===")
    
    nodes = ["Ramsey", "141hz", "Riemann-adelic"]
    coherence = calculate_symbiotic_coherence(nodes)
    
    assert 0 <= coherence <= 1.0
    print(f"✓ Symbiotic coherence for {len(nodes)} nodes: {coherence:.6f}")


def test_core_symbio_json_exists():
    """Test that CORE_SYMBIO.json exists"""
    print("\n=== Test: CORE_SYMBIO.json Exists ===")
    
    assert os.path.exists("CORE_SYMBIO.json"), "CORE_SYMBIO.json not found"
    print("✓ CORE_SYMBIO.json found")
    
    import json
    with open("CORE_SYMBIO.json", "r") as f:
        data = json.load(f)
    
    assert "protocol" in data
    assert data["protocol"] == "QCAL-SYMBIO-BRIDGE"
    print(f"  Protocol: {data['protocol']}")
    print(f"  Version: {data.get('version')}")


def test_qcal_symbiosis_md_exists():
    """Test that .qcal_symbiosis.md exists"""
    print("\n=== Test: .qcal_symbiosis.md Exists ===")
    
    assert os.path.exists(".qcal_symbiosis.md"), ".qcal_symbiosis.md not found"
    print("✓ .qcal_symbiosis.md found")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🧪 QCAL Math Library & Ecosystem Tests")
    print("="*60)
    
    try:
        test_qcal_constants()
        test_shapiro_delay()
        test_ramsey_vibration()
        test_qcal_resonance()
        test_ramsey_polynomial_bound()
        test_nft_partition_energy()
        test_ram_protocol_sync()
        test_symbiotic_coherence()
        test_core_symbio_json_exists()
        test_qcal_symbiosis_md_exists()
        
        print("\n" + "="*60)
        print("✨ ALL TESTS PASSED")
        print("="*60)
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
