#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP Test Server — Level B integration endpoint.

Exposes a minimal JSON-RPC 2.0 server on http://127.0.0.1:8506/jsonrpc that
implements the ``network.checkResonance`` method backed by the QCAL resonance
engine.

Usage:
    # Simulation mode (default for CI):
    python tests/mcp_test_server.py

    # Real-observer mode (physical data):
    export QCAL_REAL_TESTS=1
    python tests/mcp_test_server.py

    # Query a node:
    curl -s -X POST http://127.0.0.1:8506/jsonrpc \\
        -H "Content-Type: application/json" \\
        -d '{"jsonrpc":"2.0","id":1,"method":"network.checkResonance",
             "params":{"node":"auron-governor"}}' | python3 -m json.tool
"""

from __future__ import annotations

import json
import os
import socketserver
import sys
from http.server import BaseHTTPRequestHandler
from typing import Any, Dict

# Allow running from the repo root as well as from within tests/.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import mcp_network  # noqa: E402 — triggers observer auto-registration
from mcp_network.resonance import check_node_resonance  # noqa: E402

HOST = "127.0.0.1"
PORT = int(os.getenv("MCP_SERVER_PORT", "8506"))
PATH = "/jsonrpc"

# ---------------------------------------------------------------------------
# JSON-RPC 2.0 helpers
# ---------------------------------------------------------------------------

_PARSE_ERROR = -32700
_INVALID_REQUEST = -32600
_METHOD_NOT_FOUND = -32601
_INVALID_PARAMS = -32602
_INTERNAL_ERROR = -32603


def _ok(request_id: Any, result: Any) -> bytes:
    return json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "result": result},
        ensure_ascii=False,
    ).encode()


def _error(request_id: Any, code: int, message: str) -> bytes:
    return json.dumps(
        {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}},
        ensure_ascii=False,
    ).encode()


def _dispatch(body: bytes) -> bytes:
    """Parse a JSON-RPC 2.0 request and return an encoded response."""
    try:
        req: Dict[str, Any] = json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return _error(None, _PARSE_ERROR, "Parse error")

    request_id = req.get("id")
    method = req.get("method", "")
    params = req.get("params", {})

    if not isinstance(params, dict):
        return _error(request_id, _INVALID_PARAMS, "params must be an object")

    if method == "network.checkResonance":
        node = params.get("node")
        if not node or not isinstance(node, str):
            return _error(request_id, _INVALID_PARAMS, "Missing or invalid 'node' parameter")
        try:
            result = check_node_resonance(
                node_name=node,
                latency_ms=params.get("latency_ms"),
                phase_offset_rad=params.get("phase_offset_rad"),
                heartbeat_ok=params.get("heartbeat_ok"),
                schema_ok=params.get("schema_ok"),
                reachable=params.get("reachable", True),
            )
        except Exception as exc:  # pragma: no cover
            return _error(request_id, _INTERNAL_ERROR, str(exc))
        return _ok(request_id, result)

    return _error(request_id, _METHOD_NOT_FOUND, f"Method not found: {method!r}")


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class _Handler(BaseHTTPRequestHandler):
    """Minimal HTTP handler — only accepts POST /jsonrpc."""

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        # Suppress default Apache-style access log; replace with compact output.
        pass

    def do_POST(self) -> None:  # noqa: N802
        if self.path != PATH:
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        response_body = _dispatch(body)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            body = json.dumps({"status": "ok", "protocol": "QCAL-SYMBIO-BRIDGE v1.0.1"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


# ---------------------------------------------------------------------------
# Server lifecycle helpers (used by integration tests)
# ---------------------------------------------------------------------------

class MCPTestServer:
    """Context manager / helper wrapping the TCP server thread."""

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self._server: socketserver.TCPServer | None = None

    def start(self) -> None:
        socketserver.TCPServer.allow_reuse_address = True
        self._server = socketserver.TCPServer((self.host, self.port), _Handler)
        import threading
        t = threading.Thread(target=self._server.serve_forever, daemon=True)
        t.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None

    def __enter__(self) -> "MCPTestServer":
        self.start()
        return self

    def __exit__(self, *_: Any) -> None:
        self.stop()

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}{PATH}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    real_mode = os.getenv("QCAL_REAL_TESTS", "0") in {"1", "true", "yes", "on"}
    mode_label = "REAL (observadores físicos)" if real_mode else "SIM (valores sintéticos)"

    print(f"🚀 MCP Test Server escuchando en http://{HOST}:{PORT}{PATH}")
    print(f"   Modo: {mode_label}")
    print(f"   Método expuesto: network.checkResonance")
    print(f"   Health check:    http://{HOST}:{PORT}/health")
    print("   Presiona Ctrl-C para detener.\n")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), _Handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido.")


if __name__ == "__main__":
    main()
