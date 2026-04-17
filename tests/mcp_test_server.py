#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor MCP de prueba - network.checkResonance (Nivel B)."""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp_network.resonance import check_node_resonance


class MCPTestHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 (http.server callback naming)
        if self.path != "/jsonrpc":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            request_raw = self.rfile.read(content_length)
            request = json.loads(request_raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
            )
            return

        method = request.get("method")
        req_id = request.get("id")

        if method == "network.checkResonance":
            params = request.get("params") or {}
            node = params.get("node")
            result = check_node_resonance(str(node) if node is not None else "")
            response = {"jsonrpc": "2.0", "id": req_id, "result": result}
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Method not found"},
            }

        self._send_json(response)

    def _send_json(self, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = 8506
    server = HTTPServer(("127.0.0.1", port), MCPTestHandler)
    print(f"🚀 MCP Test Server escuchando en http://127.0.0.1:{port}/jsonrpc")
    print("Método expuesto: network.checkResonance")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
