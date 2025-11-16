# Certificates Directory

This directory contains UNSAT certificates for vibrational Ramsey proofs.

## Purpose

UNSAT certificates provide independently verifiable proofs that SAT instances are unsatisfiable. These certificates can be checked by certificate verifiers without re-running the SAT solver.

## Files

### `rpsi_5_5_n16_unsat.lrat` (To Be Generated)

LRAT (Linear Resolution with Asymmetric Tautology) certificate for R_ψ(5,5) ≤ 16.

This certificate can be generated using proof-producing SAT solvers:
- **Kissat**: Modern CDCL solver with LRAT output
- **CaDiCaL**: Efficient solver with proof generation
- **drat-trim**: DRAT to LRAT converter

## Generating Certificates

### Using Kissat

```bash
# Install Kissat
git clone https://github.com/arminbiere/kissat
cd kissat && ./configure && make

# Run with proof generation
./kissat --lrat=cert/rpsi_5_5_n16_unsat.lrat data/rpsi_5_5_n16.cnf
```

### Using CaDiCaL

```bash
# Install CaDiCaL
git clone https://github.com/arminbiere/cadical
cd cadical && ./configure && make

# Run with proof generation
./cadical data/rpsi_5_5_n16.cnf cert/rpsi_5_5_n16_unsat.drat
# Convert DRAT to LRAT
drat-trim data/rpsi_5_5_n16.cnf cert/rpsi_5_5_n16_unsat.drat -L cert/rpsi_5_5_n16_unsat.lrat
```

## Verifying Certificates

### Using lrat-check

```bash
# Install lrat-check
git clone https://github.com/marijnheule/lrat-check
cd lrat-check && gcc lrat-check.c -o lrat-check

# Verify certificate
./lrat-check data/rpsi_5_5_n16.cnf cert/rpsi_5_5_n16_unsat.lrat
```

Expected output:
```
c verification succeeded
s VERIFIED UNSAT
```

## Certificate Format

LRAT certificates contain:
- **Resolution steps**: Clause derivations from original CNF
- **RAT additions**: Resolution Asymmetric Tautology additions
- **Deletion information**: Clause removals to manage memory

## Importance

UNSAT certificates provide:
1. **Independent verification**: Check proofs without trusting the SAT solver
2. **Reproducibility**: Results can be verified by anyone
3. **Long-term validation**: Certificates remain valid even if solvers change
4. **Formal proof integration**: Can be translated to Lean/Coq/Isabelle proofs

## Integration with Lean

The LRAT certificate can be integrated into the Lean proof by:
1. Verifying the certificate independently
2. Trusting the LRAT checker as an oracle
3. Using proof reconstruction tactics in Lean

See `proofs/Rpsi_5_5_le_16.lean` for the corresponding Lean theorem.
