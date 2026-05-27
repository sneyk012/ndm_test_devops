#!/usr/bin/env python3
"""HTTP-сервис для проверки заголовка X-Forwarded-For."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    server_version = "xff-demo/1.0"

    def do_GET(self) -> None:
        xff = self.headers.get("X-Forwarded-For", "")
        real_ip = self.headers.get("X-Real-IP", "")
        remote = self.client_address[0]

        hops = [h.strip() for h in xff.split(",") if h.strip()]

        body = "\n".join(
            [
                "=== X-Forwarded-For test stand ===",
                f"Request path: {self.path}",
                f"TCP client (direct to app): {remote}",
                f"X-Forwarded-For (raw): {xff or '(empty)'}",
                f"X-Forwarded-For hops ({len(hops)}):",
                *[f"  [{i + 1}] {ip}" for i, ip in enumerate(hops)],
                f"X-Real-IP: {real_ip or '(empty)'}",
                "",
                "Expected chain format:",
                "  <client_ip>, <nginx1_ip>, <nginx2_ip>, ...",
            ]
        )

        payload = (body + "\n").encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args) -> None:
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
