#!/usr/bin/env python3
"""
CS2 Major Simulation Web UI
A full-featured web interface for the CS2 Major simulation engine.
"""

import sys
import os
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.web.server import run_simulation, predict_matchup, get_teams
from src.web.html_template import get_html

HOST = "127.0.0.1"
PORT = 8080


class CSDONDOHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._serve_html()
        elif path == "/api/teams":
            self._serve_json(get_teams())
        elif path == "/api/simulate":
            num_sims = int(params.get("sims", [1000])[0])
            try:
                result = run_simulation(num_sims)
                self._serve_json(result)
            except Exception as e:
                self._serve_json({"error": str(e)}, 500)
        elif path == "/api/predict":
            team1 = params.get("team1", [""])[0]
            team2 = params.get("team2", [""])[0]
            bo_n = int(params.get("bo", [3])[0])
            if not team1 or not team2:
                self._serve_json({"error": "Provide team1 and team2 params"}, 400)
            else:
                try:
                    result = predict_matchup(team1, team2, bo_n)
                    self._serve_json(result)
                except Exception as e:
                    self._serve_json({"error": str(e)}, 500)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

    def _serve_html(self):
        html = get_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _serve_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main():
    server = HTTPServer((HOST, PORT), CSDONDOHandler)
    url = f"http://{HOST}:{PORT}"
    print(f"CS2 Major Simulation Engine - Web UI")
    print(f"Open your browser: {url}")
    print(f"Press Ctrl+C to stop")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
