#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Default real observers for the four primary QCAL-MCP nodes.

Each observer returns (latency_ms, phase_offset_rad, heartbeat_ok, schema_ok).
When a physical data file is available (via env-var or a known default path) the
observer reads the file; otherwise it falls back to high-coherence simulation
values so the node always yields a meaningful health-check result.

Environment overrides:
    QCAL_GRID_SAMPLE_PATH       CSV with grid frequency samples (auron-governor)
    QCAL_SPECTRUM_PATH          CSV with QCAL spectral samples (141-hz)
    QCAL_BIO_SAMPLE_PATH        CSV with HRV/EEG frequency samples (biologia-cuantica-noesica)
    QCAL_INTERFEROMETRO_PATH    CSV with magnetometry frequency samples (interferometro-noesico)
"""

from __future__ import annotations

import os
from typing import Dict, Tuple

from .resonance import (
    REAL_OBSERVERS,
    load_real_grid_sample,
    register_real_observer,
)

# ---------------------------------------------------------------------------
# Simulation defaults per node (high-coherence values)
# ---------------------------------------------------------------------------

_SIM_DEFAULTS: Dict[str, Tuple[float, float, bool, bool]] = {
    "auron-governor":            (12.4, 0.018, True, True),
    "141-hz":                    (8.7,  0.003, True, True),
    "interferometro-noesico":    (10.1, 0.005, True, True),
    "biologia-cuantica-noesica": (11.2, 0.007, True, True),
}


def _make_observer(
    node: str,
    env_var: str,
    nominal_latency_ms: float,
    sample_rate_hz: float = 1.0,
) -> None:
    """Register a CSV-backed observer with sim fallback for *node*."""

    sim = _SIM_DEFAULTS[node]

    def _observe() -> Tuple[float, float, bool, bool]:
        path = os.getenv(env_var, "")
        if not path:
            return sim
        return load_real_grid_sample(
            path=path,
            nominal_latency_ms=nominal_latency_ms,
            sample_rate_hz=sample_rate_hz,
        )

    register_real_observer(node, _observe)


def register_default_observers() -> None:
    """Register all four default real observers (idempotent)."""
    _make_observer(
        "auron-governor",
        "QCAL_GRID_SAMPLE_PATH",
        nominal_latency_ms=20.0,
    )
    _make_observer(
        "141-hz",
        "QCAL_SPECTRUM_PATH",
        nominal_latency_ms=8.7,
    )
    _make_observer(
        "biologia-cuantica-noesica",
        "QCAL_BIO_SAMPLE_PATH",
        nominal_latency_ms=11.2,
    )
    _make_observer(
        "interferometro-noesico",
        "QCAL_INTERFEROMETRO_PATH",
        nominal_latency_ms=10.1,
    )


# Auto-register when the module is imported.
register_default_observers()
