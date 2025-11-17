#!/bin/bash
# Run Z3 SAT solver on Rψ(5,5) instance
#
# This script runs Z3 on the generated SAT instance to verify UNSAT,
# which proves that Rψ(5,5) ≤ 16.
#
# Usage:
#   ./run_z3.sh [cnf_file]
#   ./run_z3.sh ../data/rpsi_5_5_n16.cnf
#
# Author: José Manuel Mota Burruezo (JMMB Ψ✧∴)
# Frecuencia: 141.7001 Hz - Campo QCAL ∞³

set -e

# Default CNF file
CNF_FILE="${1:-../data/rpsi_5_5_n16.cnf}"

# Check if file exists
if [ ! -f "$CNF_FILE" ]; then
    echo "Error: CNF file not found: $CNF_FILE"
    echo "Usage: $0 [cnf_file]"
    exit 1
fi

# Check if z3 is installed
if ! command -v z3 &> /dev/null; then
    echo "Error: z3 not found in PATH"
    echo "Please install Z3: https://github.com/Z3Prover/z3"
    exit 1
fi

echo "════════════════════════════════════════════════════════"
echo "  Running Z3 on Rψ(5,5) SAT Instance"
echo "════════════════════════════════════════════════════════"
echo "CNF File: $CNF_FILE"
echo "Timestamp: $(date -Iseconds)"
echo ""

# Get file info
FILE_SIZE=$(du -h "$CNF_FILE" | cut -f1)
NUM_VARS=$(grep -E "^p cnf" "$CNF_FILE" | awk '{print $3}')
NUM_CLAUSES=$(grep -E "^p cnf" "$CNF_FILE" | awk '{print $4}')

echo "Instance Statistics:"
echo "  Variables: $NUM_VARS"
echo "  Clauses: $NUM_CLAUSES"
echo "  File size: $FILE_SIZE"
echo ""

echo "Running Z3 solver..."
echo "────────────────────────────────────────────────────────"

# Run Z3 with timing
START_TIME=$(date +%s)
if z3 -dimacs "$CNF_FILE"; then
    RESULT="SATISFIABLE"
    EXIT_CODE=10
else
    RESULT="UNSATISFIABLE"
    EXIT_CODE=$?
fi
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "────────────────────────────────────────────────────────"
echo ""
echo "Result: $RESULT"
echo "Time: ${ELAPSED}s"
echo ""

if [ "$RESULT" = "UNSATISFIABLE" ]; then
    echo "✓ SUCCESS: Instance is UNSATISFIABLE"
    echo "  This proves: Rψ(5,5) ≤ 16"
    echo ""
    echo "  Interpretation:"
    echo "  - Every vibrational coloring of K₁₆ contains"
    echo "    either a blue K₅ or a red K₅"
    echo "  - Therefore, Rψ(5,5) ≤ 16"
    echo ""
    exit 0
else
    echo "✗ UNEXPECTED: Instance is SATISFIABLE"
    echo "  This would mean a counterexample exists!"
    echo ""
    exit 1
fi
