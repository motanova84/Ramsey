#!/bin/bash
set -e

echo "============================================"
echo "FINAL TEST: Demonstration Methodology"
echo "============================================"
echo

echo "[1/5] Testing demo.py..."
timeout 30 python demo.py > /dev/null 2>&1
echo "✓ demo.py works"

echo "[2/5] Testing tutorial_methodology.py..."
timeout 15 python tutorial_methodology.py --no-wait > /dev/null 2>&1
echo "✓ tutorial_methodology.py works"

echo "[3/5] Testing validation script..."
python validate_demonstration.py --quick > /dev/null 2>&1
echo "✓ validate_demonstration.py works"

echo "[4/5] Checking documentation..."
for file in DEMO_METHODOLOGY.md QUICKSTART_DEMO.md DIAGRAMS_METHODOLOGY.md DEMO_IMPLEMENTATION_SUMMARY.md; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done

echo "[5/5] Checking tutorial modes..."
python tutorial_methodology.py --pillar=1 --no-wait > /dev/null 2>&1
echo "  ✓ Pillar 1 mode works"
python tutorial_methodology.py --pillar=2 --no-wait > /dev/null 2>&1
echo "  ✓ Pillar 2 mode works"
python tutorial_methodology.py --pillar=3 --no-wait > /dev/null 2>&1
echo "  ✓ Pillar 3 mode works"

echo
echo "============================================"
echo "✅ ALL FINAL TESTS PASSED"
echo "============================================"
echo
echo "The demonstration is ready for users!"
echo "Start with: python demo.py"
