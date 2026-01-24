# QCAL Symbiotic Network - Quick Start Guide

## 🚀 Quick Setup

### 1. Activate the QCAL Ecosystem
```bash
python link_ecosystem.py activar
```

This will:
- Generate `.qcal_symbiosis.md` marker
- Create node-specific beacons
- Activate RAM protocol

### 2. Verify Installation
```bash
python test_qcal_ecosystem.py
```

Expected output: `✨ ALL TESTS PASSED`

### 3. Check Ecosystem Status
```bash
python link_ecosystem.py estado
```

### 4. Run Demonstration
```bash
python demo_qcal_ecosystem.py
```

## 📚 Using the Math Library

```python
from core.math import QCALMathLibrary, ram_protocol_sync

# Access QCAL constants
freq = QCALMathLibrary.CONSTANTS["FREQ_GW"]  # 141.7001 Hz
r66 = QCALMathLibrary.CONSTANTS["RAMSEY_R66"]  # 108

# Calculate Ramsey polynomial bound
bound = QCALMathLibrary.ramsey_polynomial_bound(6, 6)

# Synchronize a node
sync = ram_protocol_sync("Ramsey", 141.7001)
print(sync['status'])  # 'synchronized'

# Calculate NFT energy
energy = QCALMathLibrary.nft_partition_energy(88)
```

## 🌐 Ecosystem Nodes

| Node | Role | Command |
|------|------|---------|
| Ramsey | Verification / R(6,6) | `python link_ecosystem.py beacon Ramsey` |
| Riemann-adelic | Spectral Proof | `python link_ecosystem.py beacon Riemann-adelic` |
| 141hz | Universal Constant | `python link_ecosystem.py beacon 141hz` |

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `python link_ecosystem.py activar` | Activate full ecosystem |
| `python link_ecosystem.py estado` | Show ecosystem status |
| `python link_ecosystem.py beacon <node>` | Generate specific beacon |
| `python test_qcal_ecosystem.py` | Run all tests |
| `python demo_qcal_ecosystem.py` | Run full demonstration |

## 📖 Documentation

- **QCAL_ECOSYSTEM_README.md** - Complete documentation
- **IMPLEMENTATION_SUMMARY.md** - Implementation details
- **CORE_SYMBIO.json** - Ecosystem configuration

## 🔑 Key Constants

- **f0**: 141.7001 Hz (Universal frequency)
- **r66**: 108 (R(6,6) Ramsey number)
- **limit_nfts**: 88 (Sovereign NFT limit)
- **resonance**: 888 Hz (Pulse synchronization)
- **PSI**: 0.999999 (Perfect coherence)

## ✨ Protocol

**QCAL-SYMBIO-BRIDGE v1.0.0**

Connects: Ramsey Theory + Riemann-Adelic Geometry + 141.7001 Hz Universal Constant
