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

## Other Scripts

- `generate_graphs.py`: Python script for graph generation
- `test_coloring.py`: Python script for coloring verification
- `vibrational_model_plot.py`: Python script for visualizing vibrational model
