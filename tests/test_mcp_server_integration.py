#!/usr/bin/env python3
"""Integration tests for the MCP test server (Level B).

Starts the server in a daemon thread on a free port, sends HTTP/JSON-RPC 2.0
requests using only the standard library, and validates response structure.
"""

from __future__ import annotations

import json
import os
import sys
import time
import unittest
import urllib.request
from typing import Any, Dict
from unittest.mock import patch

# Ensure repo root is importable.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from mcp_network.resonance import clear_real_observers
from tests.mcp_test_server import MCPTestServer

# Use a non-default port to avoid conflicts with a running server.
_TEST_PORT = 18506


def _post(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read())


class TestMCPServerIntegration(unittest.TestCase):
    """Starts MCPTestServer in a thread and sends JSON-RPC calls."""

    @classmethod
    def setUpClass(cls) -> None:
        clear_real_observers()
        cls.server = MCPTestServer(port=_TEST_PORT)
        cls.server.start()
        # Give the server a brief moment to start accepting connections.
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.stop()
        clear_real_observers()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _rpc(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return _post(
            self.server.url,
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        )

    # ------------------------------------------------------------------
    # Tests — response shape
    # ------------------------------------------------------------------

    def test_check_resonance_returns_jsonrpc_envelope(self) -> None:
        resp = self._rpc("network.checkResonance", {"node": "auron-governor"})
        self.assertEqual(resp.get("jsonrpc"), "2.0")
        self.assertEqual(resp.get("id"), 1)
        self.assertIn("result", resp)

    def test_result_contains_required_fields(self) -> None:
        resp = self._rpc("network.checkResonance", {"node": "auron-governor"})
        result = resp["result"]
        for field in ("node", "status", "psi", "resonance", "frequency_hz", "latency_ms",
                      "qcal", "checks"):
            self.assertIn(field, result, msg=f"Missing field: {field}")

    def test_psi_in_valid_range(self) -> None:
        for node in ("auron-governor", "141-hz", "interferometro-noesico",
                     "biologia-cuantica-noesica"):
            with self.subTest(node=node):
                resp = self._rpc("network.checkResonance", {"node": node})
                psi = resp["result"]["psi"]
                self.assertGreaterEqual(psi, 0.0)
                self.assertLessEqual(psi, 1.0)

    def test_status_values_are_known(self) -> None:
        resp = self._rpc("network.checkResonance", {"node": "141-hz"})
        self.assertIn(resp["result"]["status"], {"pass", "warn", "fail"})

    def test_frequency_hz_matches_catalog(self) -> None:
        resp = self._rpc("network.checkResonance", {"node": "interferometro-noesico"})
        self.assertAlmostEqual(resp["result"]["frequency_hz"], 283.4002, places=3)

    def test_node_not_in_catalog_uses_f0_reference(self) -> None:
        resp = self._rpc("network.checkResonance", {"node": "unknown-node"})
        self.assertAlmostEqual(resp["result"]["frequency_hz"], 141.7001, places=4)

    # ------------------------------------------------------------------
    # Tests — JSON-RPC protocol errors
    # ------------------------------------------------------------------

    def test_unknown_method_returns_method_not_found(self) -> None:
        resp = self._rpc("network.unknownMethod", {"node": "141-hz"})
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32601)

    def test_missing_node_param_returns_invalid_params(self) -> None:
        resp = self._rpc("network.checkResonance", {})
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32602)

    def test_invalid_json_body_returns_parse_error(self) -> None:
        data = b"{not valid json"
        req = urllib.request.Request(
            self.server.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read())
        self.assertIn("error", body)
        self.assertEqual(body["error"]["code"], -32700)

    # ------------------------------------------------------------------
    # Tests — health endpoint
    # ------------------------------------------------------------------

    def test_health_endpoint_returns_ok(self) -> None:
        url = f"http://127.0.0.1:{_TEST_PORT}/health"
        with urllib.request.urlopen(url, timeout=5) as resp:
            body = json.loads(resp.read())
        self.assertEqual(body.get("status"), "ok")

    # ------------------------------------------------------------------
    # Tests — real-observer mode
    # ------------------------------------------------------------------

    def test_sim_mode_fuente_simulada(self) -> None:
        with patch.dict(os.environ, {"QCAL_REAL_TESTS": "0"}, clear=False):
            resp = self._rpc("network.checkResonance", {"node": "auron-governor"})
        self.assertEqual(resp["result"]["checks"]["fuente_fisica"], "simulada")

    def test_real_mode_fuente_real_when_observer_present(self) -> None:
        from mcp_network.resonance import register_real_observer
        register_real_observer("auron-governor", lambda: (9.0, 0.001, True, True))
        with patch.dict(os.environ, {"QCAL_REAL_TESTS": "1"}, clear=False):
            resp = self._rpc("network.checkResonance", {"node": "auron-governor"})
        self.assertEqual(resp["result"]["checks"]["fuente_fisica"], "real")
        self.assertTrue(resp["result"]["qcal"]["modo_real"])


if __name__ == "__main__":
    unittest.main()
