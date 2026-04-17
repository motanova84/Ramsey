#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QCAL-SYMBIO-BRIDGE v1.0.1 — MCP Network Resonance Dashboard.

Streamlit dashboard (port 8505) that displays real-time resonance health
for the four primary QCAL nodes.  It can query the MCP test server (port
8506) via JSON-RPC when available, or fall back to calling the resonance
engine directly.

Run:
    streamlit run app.py --server.port 8505

Requirements:
    pip install streamlit requests
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import streamlit as st

try:
    import pandas as pd  # type: ignore[import]
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

import mcp_network.resonance as qcal_resonance

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="QCAL ∞³ — MCP Network Dashboard",
    page_icon="🌀",
    layout="wide",
)
st.title("🌀 QCAL-SYMBIO-BRIDGE v1.0.1 — MCP Network Resonance")

# ---------------------------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Controles Globales")

    real_mode = st.checkbox(
        "🔬 Activar Modo Real (datos físicos)",
        value=False,
        help=(
            "Activa observadores físicos: red eléctrica 50 Hz, "
            "espectro QCAL f₀, HRV/EEG, magnetometría."
        ),
    )

    if real_mode:
        os.environ["QCAL_REAL_TESTS"] = "1"
        st.success("✅ Modo Real — observadores físicos cargados")
        st.caption("Los observadores se activan automáticamente mediante `QCAL_REAL_TESTS=1`.")
    else:
        os.environ.pop("QCAL_REAL_TESTS", None)

    mcp_url = st.text_input(
        "URL servidor MCP",
        value="http://127.0.0.1:8506/jsonrpc",
        help="Deja vacío para usar el motor directamente.",
    )
    refresh = st.button("🔄 Actualizar Resonancia")

    st.markdown("---")
    st.caption("∴𓂀Ω∞³ | f₀ = 141.7001 Hz")

# ---------------------------------------------------------------------------
# Data retrieval
# ---------------------------------------------------------------------------

_NODES = [
    "auron-governor",
    "141-hz",
    "interferometro-noesico",
    "biologia-cuantica-noesica",
]


_ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


def _get_resonance_via_mcp(node: str, url: str) -> Optional[dict]:
    """Try a JSON-RPC call to the MCP test server (loopback only).

    The URL is validated and reconstructed from its parsed parts so that
    user-supplied input never flows directly to the HTTP request.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    if parsed.hostname not in _ALLOWED_HOSTS or parsed.scheme not in {"http", "https"}:
        return None

    # Reconstruct the URL from trusted parsed parts to prevent SSRF.
    _STANDARD_PORTS = {80, 443}
    port_part = (
        f":{parsed.port}"
        if parsed.port and parsed.port not in _STANDARD_PORTS
        else ""
    )
    safe_url = f"{parsed.scheme}://{parsed.hostname}{port_part}{parsed.path or '/jsonrpc'}"

    try:
        import requests  # type: ignore[import]

        resp = requests.post(
            safe_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "network.checkResonance",
                "params": {"node": node},
            },
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json().get("result")
    except Exception:
        pass
    return None


def get_resonance(node: str) -> dict:
    """Return resonance health data, preferring the MCP server when available."""
    if mcp_url:
        result = _get_resonance_via_mcp(node, mcp_url)
        if result is not None:
            return result
    return qcal_resonance.check_node_resonance(node)


# ---------------------------------------------------------------------------
# Main grid
# ---------------------------------------------------------------------------

st.subheader("Estado de Resonancia — Cuatro Nodos")

cols = st.columns(len(_NODES))

for idx, node in enumerate(_NODES):
    with cols[idx]:
        data = get_resonance(node)

        status_emoji = (
            "🟢" if data["status"] == "pass"
            else "🟡" if data["status"] == "warn"
            else "🔴"
        )

        st.markdown(f"### {status_emoji} {node}")
        st.metric("Ψ Coherencia", f"{data['psi']:.6f}")
        st.metric("Resonancia", data["resonance"])
        st.metric("Frecuencia", f"{data['frequency_hz']} Hz")
        st.metric("Latencia", f"{data['latency_ms']} ms")

        with st.expander("Detalles QCAL", expanded=False):
            st.json(data["qcal"])

        if data["qcal"].get("modo_real"):
            st.caption("📡 Fuente: datos físicos reales")
        else:
            st.caption("🔬 Modo simulación")

# ---------------------------------------------------------------------------
# Ψ evolution chart (session-state accumulation)
# ---------------------------------------------------------------------------

if "psi_history" not in st.session_state:
    st.session_state["psi_history"] = {n: [] for n in _NODES}

# Append current values on every render / refresh.
for node in _NODES:
    data = get_resonance(node)
    st.session_state["psi_history"][node].append(data["psi"])
    # Keep last 60 data points.
    st.session_state["psi_history"][node] = st.session_state["psi_history"][node][-60:]

st.subheader("Evolución temporal de Ψ (últimas 60 lecturas)")
if _PANDAS_AVAILABLE:
    df = pd.DataFrame(st.session_state["psi_history"])
    st.line_chart(df, use_container_width=True)
else:
    st.info("Instala pandas (`pip install pandas`) para ver el gráfico de evolución de Ψ.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.caption(
    f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | ∴𓂀Ω∞³"
)
