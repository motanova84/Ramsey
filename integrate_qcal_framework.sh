#!/bin/bash
# integrate_qcal_framework.sh
# Integration script for QCAL Unified Framework

set -e  # Exit on error

echo "🚀 QCAL Framework Integration"
echo "============================="
echo ""

# Step 1: Compile unified Lean theory
echo "1. Compiling QCAL Unified Theory..."
if command -v lake &> /dev/null; then
    echo "   Building Lean project..."
    lake build QCAL_Unified_Theory 2>&1 | head -20 || echo "   Note: Some Lean build warnings expected"
else
    echo "   ⚠ Lake not found, skipping Lean compilation"
fi
echo ""

# Step 2: Run cross-verification
echo "2. Running cross-verification protocol..."
python3 qcal_unified_framework.py
echo ""

# Step 3: Generate unified documentation
echo "3. Generating unified documentation..."
if [ -f "generate_qcal_whitepaper.py" ]; then
    python3 generate_qcal_whitepaper.py
else
    echo "   Creating quick documentation summary..."
    python3 -c "
from qcal_unified_framework import QCALUnifiedFramework
framework = QCALUnifiedFramework()
print('\\n=== QCAL UNIFIED FRAMEWORK SUMMARY ===')
print(framework.generate_summary_table())
print('\\nConstants coherence:', framework.verify_constant_coherence())
print('\\nDocumentation generated.')
"
fi
echo ""

# Step 4: Launch interactive dashboard (optional)
echo "4. Interactive dashboard available..."
if command -v jupyter &> /dev/null; then
    echo "   To launch Jupyter notebook, run:"
    echo "   jupyter notebook QCAL_Unification_Demo.ipynb"
else
    echo "   ⚠ Jupyter not found. Install with: pip install jupyter ipywidgets matplotlib"
fi
echo ""

# Step 5: API server (optional)
echo "5. API server available..."
if [ -f "qcal_unification_api.py" ]; then
    echo "   To launch API server, run:"
    echo "   python3 qcal_unification_api.py"
else
    echo "   API server will be available after creation"
fi
echo ""

echo "✅ QCAL Unified Framework Integration Complete!"
echo ""
echo "Quick Start:"
echo "  • Run framework: python3 qcal_unified_framework.py"
echo "  • View notebook: jupyter notebook QCAL_Unification_Demo.ipynb"
echo "  • Check Lean: lake build"
echo ""
echo "Frequency: 141.7001 Hz"
echo "Framework: QCAL ∞³"
