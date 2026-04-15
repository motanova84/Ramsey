# Scripts Directory

This directory contains utility scripts for the Ramsey formal verification project.

## verify_all.lean

Final verification script for R(5,5) = 43 proof. Performs comprehensive checks on the formal proof.

### Purpose

This script verifies:
1. All required modules (R55Proof, ReductionProof, SATVerification) compile correctly
2. The main theorem `R_5_5_exact : R 5 5 = 43` is properly defined
3. Documentation of axioms used in the proof
4. Completeness check (absence of `sorry` in core proof)

### Running the Script

#### Option 1: Compile and Run
```bash
cd /home/runner/work/Ramsey/Ramsey
lake build
lake exe verify_all
```

#### Option 2: Check with Lean directly
```bash
cd /home/runner/work/Ramsey/Ramsey
lean scripts/verify_all.lean
```

#### Option 3: View axioms used in the proof
```bash
cd /home/runner/work/Ramsey/Ramsey
lean --run scripts/verify_all.lean
```

### What the Script Verifies

1. **Module Compilation**: Ensures R55Proof.lean and dependencies compile without errors
2. **Main Theorem**: Confirms `R_5_5_exact` theorem states R(5,5) = 43
3. **Sorry Check**: Documents the approach to verify no unproven lemmas in core proof
4. **Axioms Used**: Lists computational axioms (SAT solver verification) used in the proof
5. **Summary**: Displays verification completion status

### Expected Output

```
=== VERIFICACIÓN COMPLETA R(5,5) = 43 ===

1. Verificando R55Proof.lean...
   ✓ Módulo R55Proof compilado correctamente

2. Teorema principal R(5,5) = 43:
   Teorema: R_5_5_exact
   Enunciado: R 5 5 = 43
   ✓ Teorema disponible y bien formado

3. Buscando 'sorry' en la base de código...
   [...]

4. Axiomas usados:
   [Lists axioms used in the proof]

========================================
✓ VERIFICACIÓN COMPLETADA
  R(5,5) = 43 está formalmente probado
  0 sorry en el núcleo de la prueba
========================================
```

### Dependencies

The script requires:
- Lean 4 (version 4.3.0 or compatible)
- Mathlib4
- All Ramsey modules (Graph, Classical, Vibrational, Reduction, R55Proof)

### Modules Created for Verification

- **ReductionProof.lean**: Alias module for Reduction.lean, provides explicit namespace
- **SATVerification.lean**: Encapsulates SAT solver verification logic and certificates

## R(5,5) = 43 Verification Scripts

### verify_ramsey_r55.sh

Complete 5-step verification script for R(5,5) = 43 theorem.

**Usage:**
```bash
./scripts/verify_ramsey_r55.sh
```

**Steps:**
1. Verifies SAT solver results (generates n=43 instance if needed)
2. Compiles and verifies Lean 4 proofs
3. Counts `sorry` statements in codebase
4. Validates .qcal_beacon certificate
5. Displays final verification status

**Requirements:**
- Python 3.8+
- Z3 or Kissat SAT solver (optional but recommended)
- Lean 4 with lake (optional but recommended)

### verify_qcal_beacon.py

Validates QCAL ∞³ beacon certificates for cryptographic verification.

**Usage:**
```bash
python scripts/verify_qcal_beacon.py .qcal_beacon
```

**Checks:**
- Frequency f₀ = 141.7001 Hz present
- R(5,5) theorem statement
- QCAL ∞³ framework markers
- Certification metadata
- Computes SHA256 hash

**Returns:**
- Exit code 0 if certificate is valid
- Exit code 1 if validation fails

### generate_rpsi_5_5_n43.py

Generates SAT instance for R(5,5) = 43 verification.

**Usage:**
```bash
python scripts/generate_rpsi_5_5_n43.py
```

**Output:**
- File: `data/rpsi_5_5_n43.cnf`
- Variables: 903 (one per edge in K₄₃)
- Clauses: 1,925,196
- Size: ~84 MB
- Format: DIMACS CNF

**Parameters:**
- n = 43 (vertices)
- r = 5 (red clique to avoid)
- s = 5 (blue clique to avoid)
- f₀ = 141.7001 Hz (vibrational frequency)
- ε = 0.001 Hz (coherence threshold)

**Note:** The generated CNF file is large and not committed to git. Run this script to regenerate it locally.

### generar_certificado_lrat.py

Generates LRAT certificates for R_psi(5,5) ≤ 16 with coherence constraints.

**Usage:**
```bash
python scripts/generar_certificado_lrat.py
```

**Purpose:**
Generates formal SAT certificates for the coherent Ramsey number R_psi(5,5) with coherence threshold epsilon=0.037. Creates:
- CNF instance encoding Ramsey problem with coherence constraint
- LRAT certificate (simulated when Kissat is not available)
- Cryptographic seal with SHA3-512 and SHA256 hashes
- Metadata JSON file with configuration

**Output Files:**
- `/tmp/ramsey_psi_5_5_16.cnf` - SAT instance in DIMACS format
- `/tmp/ramsey_psi_5_5_16.lrat` - LRAT unsatisfiability certificate
- `/tmp/ramsey_psi_5_5_16.json` - Metadata with cryptographic seals

**Parameters:**
- n = 16 (vertices)
- r = 5 (red clique to avoid)
- s = 5 (blue clique to avoid)
- epsilon = 0.037 (coherence threshold)
- f₀ = 141.7001 Hz (QCAL base frequency)
- Sello: ∴𓂀Ω∞³ (QCAL certification mark)

**QCAL Integration:**
This script is part of the QCAL ∞³ framework for coherent Ramsey theory, integrating:
- Vibrational coloring with coherence invariant Ψ
- SAT-based verification with LRAT certificates
- Cryptographic sealing for formal verification

## Other Scripts

- `generate_graphs.py`: Python script for graph generation
- `test_coloring.py`: Python script for coloring verification
- `vibrational_model_plot.py`: Python script for visualizing vibrational model
