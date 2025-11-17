#!/bin/bash
echo "=========================================="
echo "Universal Coherence Features Demo"
echo "=========================================="
echo ""

echo "1. Universal Coherence Mode (R(3,3)):"
echo "--------------------------------------"
python ai_ramsey_formal.py 3 3 --universal-coherence --lam 0.037 --nmax 10 --grid 64 | head -30
echo ""

echo "2. Infinite Prediction Mode:"
echo "--------------------------------------"
python ai_ramsey_formal.py --max-r 20 --predict-infinite | head -30
echo ""

echo "3. Generate Demo Scripts:"
echo "--------------------------------------"
rm -f r1010_demo.py ramsey_infinite.py
python ai_ramsey_formal.py --generate-scripts
echo ""

echo "4. Test ramsey_infinite.py:"
echo "--------------------------------------"
python ramsey_infinite.py
echo ""

echo "5. Legacy certify command (backward compatibility):"
echo "--------------------------------------"
python ai_ramsey_formal.py certify 3 3 --lam 0.037 --nmax 10 --grid 64 | head -10
echo ""

echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
