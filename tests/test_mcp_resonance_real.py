"""Real observer tests for MCP resonance checks."""

import csv
import math
import os
import unittest
from pathlib import Path

from mcp_network import resonance
from mcp_network.resonance import F0_REFERENCE, check_node_resonance


def _mean_from_csv(path: Path, column: str) -> float:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        values = [float(row[column]) for row in reader]
    return sum(values) / len(values)


@unittest.skipUnless(os.getenv("QCAL_REAL_TESTS") == "1", "Set QCAL_REAL_TESTS=1 to run real observer tests.")
class TestCheckNodeResonanceRealObservers(unittest.TestCase):
    """Real-observer integration checks."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).resolve().parent / "data"
        cls.hrv_path = cls.data_dir / "hrv_eeg_biologia_cuantica.csv"
        cls.mag_path = cls.data_dir / "magnetometer_interferometer.csv"

    def test_biologia_cuantica_psi_above_gate(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        self.assertGreaterEqual(health["psi"], health["checks"]["psi_gate"])
        self.assertEqual(health["resonance"], "coherent")

    def test_biologia_cuantica_phase_calculation(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        rr_mean = _mean_from_csv(self.hrv_path, "rr_interval_ms")
        expected_rr = 1000.0 / (F0_REFERENCE / 2.0)
        expected_phase = 2.0 * math.pi * ((rr_mean - expected_rr) / 1000.0) * 60.0
        self.assertAlmostEqual(health["phase_offset_rad"], expected_phase, places=12)
        self.assertLess(abs(health["phase_offset_rad"]), 0.25)

    def test_biologia_cuantica_harmonic_factor(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        self.assertEqual(health["qcal"]["harmonic_factor"], 0.5)

    def test_biologia_cuantica_real_source(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        self.assertEqual(health["checks"]["fuente_fisica"], "real")

    def test_biologia_cuantica_real_mode(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        self.assertTrue(health["qcal"]["modo_real"])

    def test_biologia_cuantica_latency_positive(self):
        health = check_node_resonance("biologia-cuantica-noesica")
        self.assertGreater(health["latency_ms"], 0.0)

    def test_biologia_cuantica_observer_registered(self):
        self.assertIn("biologia-cuantica-noesica", resonance._REAL_OBSERVERS)

    def test_interferometro_psi_above_gate(self):
        health = check_node_resonance("interferometro-noesico")
        self.assertGreaterEqual(health["psi"], health["checks"]["psi_gate"])
        self.assertEqual(health["resonance"], "coherent")

    def test_interferometro_phase_from_magnetometer(self):
        health = check_node_resonance("interferometro-noesico")
        peak_freq = _mean_from_csv(self.mag_path, "frequency_hz")
        target = F0_REFERENCE * 2.0
        expected_phase = 2.0 * math.pi * (peak_freq - target) / target
        self.assertAlmostEqual(health["phase_offset_rad"], expected_phase, places=12)
        self.assertLess(abs(health["phase_offset_rad"]), 0.25)

    def test_interferometro_harmonic_factor(self):
        health = check_node_resonance("interferometro-noesico")
        self.assertEqual(health["qcal"]["harmonic_factor"], 2.0)

    def test_interferometro_real_source(self):
        health = check_node_resonance("interferometro-noesico")
        self.assertEqual(health["checks"]["fuente_fisica"], "real")

    def test_interferometro_real_mode(self):
        health = check_node_resonance("interferometro-noesico")
        self.assertTrue(health["qcal"]["modo_real"])

    def test_interferometro_latency_positive(self):
        health = check_node_resonance("interferometro-noesico")
        self.assertGreater(health["latency_ms"], 0.0)

    def test_interferometro_observer_registered(self):
        self.assertIn("interferometro-noesico", resonance._REAL_OBSERVERS)


class TestCheckNodeResonanceFallbacks(unittest.TestCase):
    def test_unknown_node_returns_error(self):
        health = check_node_resonance("nodo-inexistente")
        self.assertEqual(health["resonance"], "unknown")
        self.assertEqual(health["error"], "observer_not_registered")
        self.assertFalse(health["checks"]["psi_above_gate"])

