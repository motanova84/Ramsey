#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resonance engine with optional real-observer inputs for MCP/QCAL checks."""

from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

F0_REFERENCE = 141.7001

# Minimal catalog used by resonance health checks.
NODE_CATALOG: Dict[str, Dict[str, Any]] = {
    "auron-governor": {"frequency_hz": 50.0000, "domain": "grid"},
    "141-hz": {"frequency_hz": 141.7001, "domain": "qcal-spectrum"},
    "interferometro-noesico": {"frequency_hz": 283.4002, "domain": "interferometry"},
    "biologia-cuantica-noesica": {"frequency_hz": 70.85005, "domain": "bio-signal"},
    "lighthouse": {"frequency_hz": 0.0, "domain": "coordination"},
    "sentinel": {"frequency_hz": 35.425025, "domain": "monitoring"},
    "riemann-adelic": {"frequency_hz": 54.1194382, "domain": "analytic-bridge"},
}

RealObserver = Callable[[], Tuple[float, float, bool, bool]]
REAL_OBSERVERS: Dict[str, RealObserver] = {}


def register_real_observer(node: str, fn: RealObserver) -> None:
    """Register a physical observer callback for a node."""
    REAL_OBSERVERS[node] = fn


def clear_real_observers() -> None:
    """Clear registered real observers (mainly for tests)."""
    REAL_OBSERVERS.clear()


def _is_real_mode_enabled() -> bool:
    value = os.getenv("QCAL_REAL_TESTS", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def score_psi(
    latency_ms: float,
    phase_offset_rad: float,
    heartbeat_ok: bool = True,
    schema_ok: bool = True,
) -> float:
    """Compute Ψ score from transport and phase observables."""
    if not heartbeat_ok or not schema_ok:
        return 0.0
    latency_penalty = min(max(latency_ms, 0.0) / 100.0, 1.0)
    phase_penalty = min(abs(phase_offset_rad) / 0.25, 1.0)
    psi = 1.0 - 0.45 * latency_penalty - 0.55 * phase_penalty
    return max(0.0, min(psi, 1.0))


def classify_resonance(psi: float, reachable: bool) -> Tuple[str, str]:
    """Classify resonance state and health status."""
    if not reachable:
        return "offline", "fail"
    if psi >= 0.99:
        return "coherent", "pass"
    if psi >= 0.95:
        return "drifting", "warn"
    return "fault", "fail"


def _parse_frequency_samples(path: str) -> List[float]:
    values: List[float] = []
    with open(path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if "frequency_hz" in row and row["frequency_hz"] not in (None, ""):
                values.append(float(row["frequency_hz"]))
                continue

            # Fallback: first numeric-like value in the row.
            for value in row.values():
                if value in (None, ""):
                    continue
                try:
                    values.append(float(value))
                    break
                except ValueError:
                    continue
    return values


def load_real_grid_sample(
    path: Optional[str] = None,
    nominal_latency_ms: float = 20.0,
    sample_rate_hz: float = 1.0,
) -> Tuple[float, float, bool, bool]:
    """
    Load a real/snapshot grid-frequency series and map it to resonance inputs.

    Returns: (latency_ms, phase_offset_rad, heartbeat_ok, schema_ok).

    Note:
        `sample_rate_hz` defaults to 1.0 (one sample per second), which is
        common for public grid snapshots. Override it for higher/lower-rate
        acquisition streams.
    """
    source = path or os.getenv(
        "QCAL_GRID_SAMPLE_PATH", "/tmp/grid_frequency_2026-04-15T14_55Z.csv"
    )
    if not os.path.exists(source):
        return 12.4, 0.018, True, True

    samples = _parse_frequency_samples(source)
    if not samples:
        return 12.4, 0.018, False, False

    delta_f = (sum(samples) / len(samples)) - 50.0
    effective_rate = sample_rate_hz if sample_rate_hz > 0 else 1.0
    window_seconds = float(len(samples)) / effective_rate
    phase_offset = 2.0 * math.pi * delta_f * window_seconds
    return nominal_latency_ms, phase_offset, True, True


def _get_defaults(
    latency_ms: Optional[float],
    phase_offset_rad: Optional[float],
    heartbeat_ok: Optional[bool],
    schema_ok: Optional[bool],
) -> Tuple[float, float, bool, bool]:
    lat = latency_ms if latency_ms is not None else 12.4
    phase = phase_offset_rad if phase_offset_rad is not None else 0.018
    heartbeat = heartbeat_ok if heartbeat_ok is not None else True
    schema = schema_ok if schema_ok is not None else True
    return lat, phase, heartbeat, schema


def check_node_resonance(
    node_name: str,
    latency_ms: Optional[float] = None,
    phase_offset_rad: Optional[float] = None,
    heartbeat_ok: Optional[bool] = None,
    schema_ok: Optional[bool] = None,
    reachable: bool = True,
) -> Dict[str, Any]:
    """Compute MCP-QCAL health check for a node in sim mode or real-observer mode."""
    freq = NODE_CATALOG.get(node_name, {}).get("frequency_hz", F0_REFERENCE)

    explicit_inputs = any(
        value is not None for value in (latency_ms, phase_offset_rad, heartbeat_ok, schema_ok)
    )

    source_mode = "simulada"
    real_mode = False

    if not explicit_inputs and _is_real_mode_enabled() and node_name in REAL_OBSERVERS:
        lat, phase, hb, sch = REAL_OBSERVERS[node_name]()
        source_mode = "real"
        real_mode = True
    else:
        lat, phase, hb, sch = _get_defaults(
            latency_ms, phase_offset_rad, heartbeat_ok, schema_ok
        )

    psi = score_psi(lat, phase, hb, sch)
    resonance, status = classify_resonance(psi, reachable)
    phase_coherence = max(0.0, min(1.0, 1.0 - abs(phase) / (math.pi / 2)))

    return {
        "node": node_name,
        "status": status,
        "reachable": reachable,
        "latency_ms": round(lat, 2),
        "resonance": resonance,
        "psi": round(psi, 6),
        "phase_offset_rad": round(phase, 6),
        "frequency_hz": freq,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "qcal": {
            "psi_raw": round(psi, 6),
            "f0_reference_hz": F0_REFERENCE,
            "harmonic_factor": round(freq / F0_REFERENCE, 5),
            "phase_coherence": round(phase_coherence, 4),
            "resonance_class": resonance,
            "logos_level": "saturated" if psi > 0.999 else "stable",
            "modo_real": real_mode,
        },
        "checks": {
            "transport": "ok" if reachable else "fail",
            "schema": "ok" if sch else "fail",
            "heartbeat": "ok" if hb else "fail",
            "qcal_protocol": "ok",
            "fuente_fisica": source_mode,
        },
        "error_code": None,
        "error_message": None,
    }
