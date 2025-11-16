# Lean Tests for R_ψ(5,5) ≤ 16 Proof

This directory contains Lean 4 test files for verifying the formal proof structure.

## Test Files

### test_reduction.lean
Checks that the Ramsey.Instance type is properly defined.

### test_r55.lean
Checks that the main theorem rpsi_5_5_bound is accessible.

## Running Tests

With Lean 4 installed:

```bash
lake build
```

## Structure

The tests verify that:
1. All imports resolve correctly
2. Type definitions are accessible
3. Theorem statements are well-formed
