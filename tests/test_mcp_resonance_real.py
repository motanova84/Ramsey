#!/usr/bin/env python3
"""Tests for MCP resonance real/simulation observer mode."""

import os
import tempfile
import unittest
from unittest.mock import patch

from mcp_network.resonance import (
    check_node_resonance,
    clear_real_observers,
    load_real_grid_sample,
    register_real_observer,
)


class TestMCPResonanceRealMode(unittest.TestCase):
    """Validate real-observer toggling and physical sample loading."""

    def setUp(self):
        clear_real_observers()

    def tearDown(self):
        clear_real_observers()

    def test_real_observer_activates_with_env_flag(self):
        register_real_observer("auron-governor", lambda: (8.0, 0.002, True, True))
        with patch.dict(os.environ, {"QCAL_REAL_TESTS": "1"}, clear=False):
            result = check_node_resonance("auron-governor")

        self.assertTrue(result["qcal"]["modo_real"])
        self.assertEqual(result["checks"]["fuente_fisica"], "real")
        self.assertAlmostEqual(result["latency_ms"], 8.0, places=2)

    def test_real_observer_ignored_without_env_flag(self):
        register_real_observer("auron-governor", lambda: (8.0, 0.002, True, True))
        with patch.dict(os.environ, {"QCAL_REAL_TESTS": "0"}, clear=False):
            result = check_node_resonance("auron-governor")

        self.assertFalse(result["qcal"]["modo_real"])
        self.assertEqual(result["checks"]["fuente_fisica"], "simulada")
        self.assertAlmostEqual(result["latency_ms"], 12.4, places=2)

    def test_load_real_grid_sample_fallback_when_missing(self):
        lat, phase, hb, schema = load_real_grid_sample("/tmp/not_existing_grid_sample.csv")
        self.assertEqual((hb, schema), (True, True))
        self.assertAlmostEqual(lat, 12.4, places=2)
        self.assertAlmostEqual(phase, 0.018, places=6)

    def test_load_real_grid_sample_from_csv(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv") as handle:
            handle.write("timestamp,frequency_hz\n")
            handle.write("t1,50.01\n")
            handle.write("t2,50.00\n")
            handle.write("t3,49.99\n")
            sample_path = handle.name

        try:
            lat, phase, hb, schema = load_real_grid_sample(sample_path, nominal_latency_ms=21.0)
        finally:
            os.remove(sample_path)

        self.assertEqual((hb, schema), (True, True))
        self.assertAlmostEqual(lat, 21.0, places=2)
        self.assertAlmostEqual(phase, 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
