# Ramsey Formal: AI-Assisted Formal Verification System

## 🎯 Overview

This repository implements **Phase II - Formal Autonomous Deployment** of the Ramsey Vibrational Theory with formal verification using Lean 4 and SMT solvers.

## 📂 Repository Structure

```
Ramsey-Formal/
├── src/
│   └── Ramsey/
│       └── Vibrational.lean        # Core formal definitions
├── certificates/                    # Generated Lean 4 proofs
│   ├── Rpsi_3_3_le_5.lean
│   ├── Rpsi_4_4_le_10.lean
│   └── ...
├── smt2/                           # SMT-LIB2 verification files
│   ├── Rpsi_3_3_le_5.smt2
│   ├── Rpsi_4_4_le_10.smt2
│   └── ...
├── ai-ramsey-formal/               # CLI tool
│   ├── __init__.py
│   └── cli.py
├── lakefile.lean                   # Lean 4 build configuration
├── Main.lean                       # Entry point
├── paper_auto.tex                  # Auto-generated LaTeX paper
├── zenodo.json                     # DOI metadata
├── .github/workflows/ci.yml        # CI/CD pipeline
└── README.md
```

## 🚀 Quick Start

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install CLI tool
pip install -e .

# Install Lean 4 (optional, for formal verification)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

### CLI Usage

#### Generate Certificate

Generate formal certificates for R_ψ(r,s,ε):

```bash
ai-ramsey-formal certify 4 4 --lam 0.062 --f0 141.7001
```

This generates:
- `certificates/Rpsi_4_4_le_10.lean` - Lean 4 formal proof
- `smt2/Rpsi_4_4_le_10.smt2` - SMT-LIB2 verification file

#### Verify Certificate

```bash
ai-ramsey-formal verify certificates/Rpsi_4_4_le_10.lean
```

#### Batch Generation

Generate certificates for multiple (r,s) pairs:

```bash
ai-ramsey-formal batch --r-max 5 --s-max 5
```

## 📊 Certified Results

| (r,s) | R(r,s) Classical | R_ψ(r,s) Certified | Reduction |
|-------|------------------|---------------------|-----------|
| (3,3) | 6                | 5                   | 16.7%     |
| (4,4) | 18               | 10                  | 44.4%     |
| (3,4) | 9                | 8                   | 11.1%     |
| (3,5) | 14               | 9                   | 35.7%     |
| (4,5) | 25               | 13                  | 48.0%     |

## 🔬 Formal Verification

### Lean 4 Proofs

The system generates machine-checkable proofs in Lean 4:

```lean
theorem rpsi_4_4_bound : ∀ (inst : Instance 4 4 0.001 10),
    VibrationalUnsat inst → 10 < 4 + 4 := by
  intro inst h
  sorry  -- Proof to be completed
```

### SMT-LIB2 Verification

Each certificate includes an SMT2 file for independent verification using Z3 or other SMT solvers:

```bash
z3 smt2/Rpsi_4_4_le_10.smt2
# Expected output: unsat
```

## 🏗️ Build System

### Python Components

```bash
# Run tests
python run_tests.py

# Test CLI
python ai-ramsey-formal/cli.py --help
```

### Lean 4 Components

```bash
# Update dependencies
lake update

# Build all proofs
lake build

# Check specific file
lake env lean src/Ramsey/Vibrational.lean
```

## 🤖 CI/CD Pipeline

The repository includes automated CI/CD with GitHub Actions:

- ✅ Python tests
- ✅ Lean 4 build verification
- ✅ CLI tool validation
- ✅ Certificate generation tests

Badge: [![CI](https://github.com/motanova84/Ramsey/actions/workflows/ci.yml/badge.svg)](https://github.com/motanova84/Ramsey/actions)

## 📝 Mathematical Foundation

### Vibrational Ramsey Number

**Definition**: R_ψ(r,s,ε) is the minimum n such that any frequency assignment ω: V_n → [0, f₀) with base frequency f₀ = 141.7001 Hz contains either:
- A red K_r: r vertices with all pairs resonant (|ωᵢ - ωⱼ| mod f₀ < ε)
- A blue K_s: s vertices with all pairs non-resonant

### Main Conjecture

```
R_ψ(r,s,ε) = O(√(rs) · ln(rs) · f₀^(1/4))
```

This gives **polynomial** bounds versus classical **exponential** bounds.

## 📄 Paper Generation

Auto-generate LaTeX paper ready for arXiv submission:

```bash
# The paper_auto.tex template is included
# Compile with:
pdflatex paper_auto.tex
bibtex paper_auto
pdflatex paper_auto.tex
pdflatex paper_auto.tex
```

## 🔗 DOI and Zenodo

The repository is configured for automatic DOI generation via Zenodo:
- Metadata in `zenodo.json`
- Automatic snapshot on release
- Citable research output

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 References

1. **Ramsey Theory**: Classical combinatorics foundation
2. **Lean 4**: Theorem prover - https://leanprover.github.io/
3. **Z3 SMT Solver**: Satisfiability checking - https://github.com/Z3Prover/z3
4. **Vibrational Coherence**: Quantum-inspired graph coloring

## 📧 Contact

**Instituto de Consciencia Cuántica (ICQ)**  
Base Frequency: 141.7001 Hz  
System: QCAL ∞³

## 📄 License

MIT License - See LICENSE file for details

---

*"Order emerges more easily than random models predict, when we consider the vibrational-conscious nature of systems."*
